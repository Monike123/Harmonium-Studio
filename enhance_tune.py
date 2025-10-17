import os
import re
import math
import random
import numpy as np
import librosa
from scipy.signal import fftconvolve
from pydub import AudioSegment
from pydub.effects import low_pass_filter, high_pass_filter

# ======== CONFIGURATION ========
DATA_DIR = "dataset_2"
OUTPUT_DIR = "output"
START_TUNE_PATH = os.path.join(DATA_DIR, "start_tune.wav")
END_TUNE_PATH   = os.path.join(DATA_DIR, "end_tune.wav")
IR_PATH         = os.path.join(DATA_DIR, "ir.wav")
OUTPUT_FILE     = os.path.join(OUTPUT_DIR, "enhanced_tune.wav")

SWAR_SAMPLE_MAP = {
    "Sa": "sa.wav",
    "Re": "re.wav",
    "Ga": "ga.wav",
    "Ma": "ma.wav",
    "Pa": "pa.wav",
    "Dha": "dha.wav",
    "Ni": "ni.wav",
    "Re(k)": "re_komal.wav",
    "Ga(k)": "ga_komal.wav",
    "Dha(k)": "dha_komal.wav",
    "Ni(k)": "ni_komal.wav",
    "Ma(tivra)": "ma_tivra.wav"
}

SWAR_SAMPLE_MAP = {k: os.path.join(DATA_DIR, fn) for k, fn in SWAR_SAMPLE_MAP.items()}

NOTES_PER_PHRASE       = 7
LONG_PRESS_MULTIPLIER  = 3.0
PHRASE_END_HOLD        = True
RUBATO_MAX_OFFSET_MS   = 4

CROSSFADE_BASE_MS        = 120
INTERVAL_CROSSFADE_FACTOR = 30
MAX_CROSSFADE_MS          = 450

BG_VOLUME_REDUCTION_DB = -20
RHYTHM_VOLUME_PATTERN  = [1.0,1.05,0.98,1.02,0.97,1.03,0.95,1.0,0.93,0.89]
SCALE_ORDER = ["Sa", "Re(k)", "Re", "Ga(k)", "Ga", "Ma", "Ma(tivra)", "Pa", "Dha(k)", "Dha", "Ni(k)", "Ni", "Sa"]

# ======== HUMANIZATION CONFIG ========
RANDOM_LONG_PRESS_PROB = 0.1   # 10% chance per note
RANDOM_LONG_PRESS_MULT = 1.5   # 1.5× duration when triggered
VIBRATO_FREQ_RANGE     = (5.5,7.0)
VIBRATO_DEPTH_RANGE    = (1.0,1.5)

# ======== LOAD IMPULSE RESPONSE ========
IR_SIGNAL = None
if os.path.exists(IR_PATH):
    IR_SIGNAL, sr = librosa.load(IR_PATH, sr=44100)
    IR_SIGNAL /= np.max(np.abs(IR_SIGNAL))

# ======== EFFECT UTILITIES ========
def apply_convolution_reverb(seg: AudioSegment) -> AudioSegment:
    samples = np.array(seg.get_array_of_samples(), dtype=float)
    samples = samples.reshape((seg.channels, -1))
    wet = fftconvolve(samples, IR_SIGNAL[np.newaxis, :], mode='full')[:, :samples.shape[1]]
    wet = wet / np.max(np.abs(wet)) * (seg.max / 32767)
    out = AudioSegment(
        wet.T.astype(np.int16).tobytes(),
        frame_rate=seg.frame_rate,
        sample_width=seg.sample_width,
        channels=seg.channels
    )
    return seg.overlay(out - 6)

def portamento(prev_seg: AudioSegment, curr_seg: AudioSegment, slide_ms=40, cents=20) -> AudioSegment:
    factor = 2 ** (cents / 1200)
    tail = prev_seg[-slide_ms:]._spawn(
        prev_seg[-slide_ms:].raw_data,
        overrides={'frame_rate': int(prev_seg.frame_rate * factor)}
    ).set_frame_rate(prev_seg.frame_rate)
    head = prev_seg[:-slide_ms]
    slid = tail.append(curr_seg, crossfade=slide_ms)
    return head + slid

def apply_vibrato(segment: AudioSegment, freq=6, depth_db=1.2) -> AudioSegment:
    modulated = segment
    for i in range(0, len(segment), 200):
        gain = math.sin(i/1000 * freq * 2*math.pi) * depth_db
        modulated = modulated.overlay(segment[i:i+200].apply_gain(gain), position=i)
    return modulated

# ======== MAIN EXPORT FUNCTION ========
def generate_from_clean_swar_sequence(sequence, output_file=OUTPUT_FILE,max_duration=None):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Decide Intro/Outro Mode
    mode = random.choice(['none','intro','outro','both','swap'])
    master = AudioSegment.silent(0)
    # — RANDOMIZE RHYTHM & SCALE ORDER FOR FRESHNESS —
    pattern = RHYTHM_VOLUME_PATTERN.copy()
    random.shuffle(pattern)

    # create a working copy of the scale
    scale = SCALE_ORDER.copy()
    # 50% chance to reverse (descending feel)
    if random.random() < 0.5:
        scale.reverse()
    # rotate starting point by a random offset
    rot = random.randint(0, len(scale)-1)
    scale = scale[rot:] + scale[:rot]

    # 1) Intro handling
    if mode in ('intro','both') and os.path.exists(START_TUNE_PATH):
        master += AudioSegment.from_wav(START_TUNE_PATH)
    if mode == 'swap' and os.path.exists(END_TUNE_PATH):
        master += AudioSegment.from_wav(END_TUNE_PATH)

    # 2) Random Background
    bg = None
    # collect any .wav file starting with "bg" or "bf"
    candidates = []
    for fn in os.listdir(DATA_DIR):
        if (fn.lower().startswith("bg") or fn.lower().startswith("bf")) and fn.lower().endswith(".wav"):
            candidates.append(os.path.join(DATA_DIR, fn))
    if candidates:
        chosen = random.choice(candidates)
        bg = AudioSegment.from_file(chosen).apply_gain(BG_VOLUME_REDUCTION_DB)

    # 3) Load Swar Samples
    swars = {lbl: AudioSegment.from_wav(path)
             for lbl,path in SWAR_SAMPLE_MAP.items() if os.path.exists(path)}
    missing = [lbl for lbl in SWAR_SAMPLE_MAP if lbl not in swars]
    if missing:
        print(f"⚠️ Warning: Missing audio files for: {missing}")


    # 4) Build Melody
    main, prev_seg, prev_lbl = AudioSegment.silent(0), None, None
    pat = len(RHYTHM_VOLUME_PATTERN)
    for i, note in enumerate(sequence, 1):
        lbl = note['swar'].strip()
        if lbl not in swars: continue

        # Duration
        d = max(10, int(note['duration']*1000))
        if PHRASE_END_HOLD and i%NOTES_PER_PHRASE==0:
            d = int(d * LONG_PRESS_MULTIPLIER)
        if random.random() < RANDOM_LONG_PRESS_PROB:
            d = int(d * RANDOM_LONG_PRESS_MULT)

        # Rubato
        j = random.randint(-RUBATO_MAX_OFFSET_MS, RUBATO_MAX_OFFSET_MS)
        if j>0:
            main += AudioSegment.silent(j)
        elif j<0 and len(main)>abs(j):
            main = main[:-abs(j)]

        # Gain and filters
        breath = pattern[(i-1)%pat]
        accent = 4 if i%NOTES_PER_PHRASE==0 else 0
        g = (note['volume']*breath - 0.5)*20 + accent
        transpose_factor = 0.92  # 0.90–0.95 sounds natural; adjust if needed
        orig_seg = swars[lbl][:d]
        clip = orig_seg._spawn(orig_seg.raw_data, overrides={'frame_rate': int(orig_seg.frame_rate * transpose_factor)}).set_frame_rate(orig_seg.frame_rate).apply_gain(g)
        clip = low_pass_filter(clip,4000)
        clip = high_pass_filter(clip,150)

        # Dynamic vibrato
        vf = random.uniform(*VIBRATO_FREQ_RANGE)
        vd = random.uniform(*VIBRATO_DEPTH_RANGE)
        clip = apply_vibrato(clip, freq=vf, depth_db=vd)

        # Fades
        clip = clip.fade(to_gain=-3.0, start=0, duration=80)\
                   .fade(to_gain=-6.0, start=d-100, duration=80)

        # Crossfade based on scale distance
        cf = 0
        if prev_lbl:
            idx1 = scale.index(prev_lbl)
            idx2 = scale.index(lbl)
            steps = abs((idx2 - idx1) % len(SCALE_ORDER))
            cf = min(
                MAX_CROSSFADE_MS,
                CROSSFADE_BASE_MS + steps*INTERVAL_CROSSFADE_FACTOR,
                len(main),
                len(clip)//2
            )

        # Portamento for close moves
        if prev_seg and abs(scale.index(prev_lbl)-scale.index(lbl))<=2:
            clip = portamento(prev_seg, clip)

        # Append
        main = main.append(clip, crossfade=cf) if cf>0 else main + clip
        prev_seg, prev_lbl = clip, lbl

    # 5) Mix background
    if bg and len(main)>0:
        loops = math.ceil(main.duration_seconds / bg.duration_seconds)
        bg_loop = (bg*loops)[:len(main)]
        main = bg_loop.overlay(main)

    # 6) Outro handling
    if mode in ('outro','both') and os.path.exists(END_TUNE_PATH):
        master = master + main + AudioSegment.from_wav(END_TUNE_PATH)
    elif mode=='swap' and os.path.exists(START_TUNE_PATH):
        master = master + main + AudioSegment.from_wav(START_TUNE_PATH)
    else:
        master = master + main

    # 7) Reverb
    if IR_SIGNAL is not None:
        master = apply_convolution_reverb(master)

    # 8) Trim to max_duration if specified
    if max_duration is not None:
        max_ms = int(max_duration * 1000)
        master = master[:max_ms]

    # 9) Export
    master.export(output_file, format="wav")
    print(f"✅ Enhanced audio exported to: {output_file}")