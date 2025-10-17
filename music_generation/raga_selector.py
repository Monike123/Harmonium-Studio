# raga_selector.py

import numpy as np
from config import RAGA_LIBRARY, OCTAVE_MULTIPLIERS, SWAR_FREQUENCIES

def classify_warm_or_cool(hue_values):
    """
    Given a list of hue values (0–179), classify the image tone.
    Returns: 'warm', 'cool', or 'neutral'
    """
    warm = list(range(0, 40)) + list(range(160, 180))
    cool = list(range(80, 160))
    warm_count = sum(h in warm for h in hue_values)
    cool_count = sum(h in cool for h in hue_values)
    if warm_count > cool_count * 1.2:
        return 'warm'
    if cool_count > warm_count * 1.2:
        return 'cool'
    return 'neutral'

def select_raga_from_tone(tone_type):
    if tone_type == 'warm':
        return 'Yaman'
    if tone_type == 'cool':
        return 'Malkauns'
    return np.random.choice([
        'Bageshri', 'Bhairavi', 'Darbari Kanada',
        'Puriya Dhanashri', 'Bhopali', 'Kafi', 'Bhairav'
    ])

def choose_raga_from_colors(rgb_colors):
    from image_analysis.swar_mapper import rgb_to_hsv
    hues = [rgb_to_hsv(*rgb)[0] for rgb in rgb_colors]
    tone = classify_warm_or_cool(hues)
    raga = select_raga_from_tone(tone)
    print(f"🧠 Tone: {tone.upper()} → Raga: {raga}")
    return raga

# ────────────────────────────────────────────────── #
# Enhanced pool builder for richer swar variation
# ────────────────────────────────────────────────── #

def get_raga_swar_pool(raga_name, octaves=('Mandra','Madhya','Tara')):
    """
    Build a diverse list of (swar, octave) tuples for the given raga:
      • full aroha & avaroha in each octave
      • pakad motifs repeated
      • octave-shifted swars for color
    """
    raga = RAGA_LIBRARY.get(raga_name)
    if not raga:
        raise ValueError(f"Raga '{raga_name}' not found.")

    pool = []

    # 1. Aroha + Avaroha in each octave
    for octv in octaves:
        for swar in raga.get('aroha', []):
            pool.append((swar, octv))
        for swar in raga.get('avaroha', []):
            pool.append((swar, octv))

    # 2. Pakad motifs, repeated twice
    for _ in range(2):
        for swar in raga.get('pakad', []):
            for octv in octaves:
                pool.append((swar, octv))

    # 3. Core swars in all octaves
    for swar in raga.get('swars', []):
        for octv in octaves:
            pool.append((swar, octv))

    # 4. Remove duplicates and shuffle
    # Using dict.fromkeys to preserve one occurrence, then shuffle
    unique = list(dict.fromkeys(pool))
    np.random.shuffle(unique)
    return unique

def get_raga_swars(raga_name):
    """
    Public API: returns a diverse swar_source for any raga.
    """
    # You can adjust which octaves to include per raga:
    return get_raga_swar_pool(raga_name, octaves=('Mandra','Madhya','Tara'))
