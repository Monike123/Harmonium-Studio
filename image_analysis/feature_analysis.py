# image_analysis/feature_analysis.py

import cv2
import numpy as np

def extract_image_features(image_path):
    import cv2
    import numpy as np

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    brightness = np.mean(gray)
    contrast = np.std(gray)
    
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / (img.shape[0] * img.shape[1])

    # Optional: symmetry analysis later

    return {
        "brightness": brightness,
        "contrast": contrast,
        "edge_density": edge_density
    }

def derive_music_params_from_features(features):
    brightness = features["brightness"]
    contrast = features["contrast"]
    edge_density = features["edge_density"]

    # Map image stats to music logic
    avg_volume = np.interp(brightness, [0, 255], [0.4, 1.0])
    tempo_multiplier = np.interp(contrast, [0, 128], [0.7, 1.3])
    notes_per_phrase = int(np.interp(edge_density, [0, 0.2], [5, 20]))

    return {
        "volume_range": (avg_volume * 0.8, avg_volume * 1.2),
        "tempo_multiplier": tempo_multiplier,
        "notes_per_phrase": notes_per_phrase
    }

def analyze_brightness(image_path):
    """
    Compute average brightness of the image (0–255).
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    return np.mean(image)

def analyze_texture(image_path):
    """
    Estimate texture by computing the variance of the Laplacian.
    High variance → rough texture, low variance → smooth.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return laplacian.var()

def analyze_image_features(image_path):
    """
    High-level wrapper to return brightness + texture.
    """
    brightness = analyze_brightness(image_path)
    texture = analyze_texture(image_path)

    print(f"\n📊 Brightness: {brightness:.2f} | Texture (Laplacian Var): {texture:.2f}")
    return {
        'brightness': brightness,
        'texture': texture
    }
