# image_analysis/swar_mapper.py

import colorsys
from config import SWAR_FREQUENCIES, HUE_TO_SWAR, OCTAVE_MULTIPLIERS

def rgb_to_hsv(r, g, b):
    """
    Convert RGB [0-255] to HSV with Hue [0-179] for OpenCV compatibility.
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return int(h * 179), int(s * 255), int(v * 255)

def map_hue_to_swar(hue):
    """
    Map a hue value (0–179) to a swar based on predefined HUE_TO_SWAR ranges.
    """
    for (low, high), swar in HUE_TO_SWAR.items():
        if low <= hue <= high:
            return swar
    return 'Sa'  # default fallback

def get_swar_and_freq_from_rgb(rgb, octave='Madhya'):
    """
    Given an RGB tuple, return the closest swar and its frequency (with octave).
    
    Returns:
        (swar_name: str, frequency: float)
    """
    h, _, _ = rgb_to_hsv(*rgb)
    swar = map_hue_to_swar(h)
    freq = SWAR_FREQUENCIES[swar] * OCTAVE_MULTIPLIERS[octave]
    return swar, freq
