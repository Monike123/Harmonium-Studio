# image_analysis/color_extractor.py

import cv2
import numpy as np
from sklearn.cluster import KMeans

def extract_dominant_colors(image_path, num_colors=7):
    """
    Extract dominant RGB colors from an image using KMeans clustering.
    
    Args:
        image_path (str): Path to the image.
        num_colors (int): Number of dominant colors to extract.

    Returns:
        List of RGB tuples.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Convert from BGR (OpenCV default) to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize image for faster processing
    image = cv2.resize(image, (200, 200))
    pixels = image.reshape(-1, 3)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=num_colors, n_init='auto')
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)

    return [tuple(color) for color in dominant_colors]
