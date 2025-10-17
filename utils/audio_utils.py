# utils/audio_utils.py

import numpy as np

def normalize_audio(audio):
    """
    Normalize a NumPy waveform to the 16-bit range.
    """
    audio = audio / np.max(np.abs(audio))
    return np.int16(audio * 32767)

def apply_fade(audio, fade_in_duration=0.05, fade_out_duration=0.05, sample_rate=44100):
    """
    Apply fade-in and fade-out to the waveform.
    """
    fade_in_samples = int(sample_rate * fade_in_duration)
    fade_out_samples = int(sample_rate * fade_out_duration)

    fade_in = np.linspace(0, 1, fade_in_samples)
    fade_out = np.linspace(1, 0, fade_out_samples)

    audio[:fade_in_samples] *= fade_in
    audio[-fade_out_samples:] *= fade_out

    return audio
