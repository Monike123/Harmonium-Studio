def synthesize_sequence_to_audio(sequence, output_path="output.wav", total_duration=7.0):
    from scipy.io.wavfile import write
    from utils.audio_utils import normalize_audio, apply_fade
    import numpy as np

    sample_rate = 44100
    audio = np.zeros(0)

    for note in sequence:
        swar = note['swar']
        freq = note['frequency']
        duration = note['duration']
        volume = note['volume']

        print(f"▶️ {swar} - {freq:.2f} Hz for {duration:.2f}s (vol: {volume:.2f})")

        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        tone = np.sin(2 * np.pi * freq * t) * volume
        tone = apply_fade(tone, 0.05, 0.05, sample_rate)
        audio = np.concatenate([audio, tone])

    audio = normalize_audio(audio)
    write(output_path, sample_rate, audio.astype(np.int16))
    print(f"\n✅ Audio saved to {output_path} ({total_duration:.1f} sec)")
