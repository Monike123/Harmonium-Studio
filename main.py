import os
import random
import time

IMAGE_DIR = 'random_images'

def get_random_images(num_images=10):
    all_images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]
    if not all_images:
        return []
    return random.sample(all_images, min(num_images, len(all_images)))

def generate_tune_from_image(image_path, duration_seconds=45):
    # Placeholder for actual tune generation logic
    # In a real scenario, this would involve image analysis and music synthesis
    print(f"Generating a {duration_seconds}-second tune for {image_path}...")
    # Simulate tune generation
    time.sleep(1) # Simulate some processing time
    tune_name = f"tune_for_{os.path.basename(image_path).split('.')[0]}_{random.randint(1000, 9999)}.wav"
    rag_name = f"rag_for_{os.path.basename(image_path).split('.')[0]}_{random.randint(100, 999)}"
    print(f"Generated tune: {tune_name} with rag: {rag_name}")
    return tune_name, rag_name

if __name__ == '__main__':
    print("Starting image to tune process...")
    while True:
        selected_images = get_random_images(10)
        if not selected_images:
            print("No images found in the directory. Please add images to image_to_harmonium/random_images/. Retrying in 5 seconds...")
            time.sleep(5)
            continue
        
        print(f"Selected images for this loop: {selected_images}")
        for img in selected_images:
            full_image_path = os.path.join(IMAGE_DIR, img)
            tune, rag = generate_tune_from_image(full_image_path, 45)
            print(f"Processed {img}: Tune - {tune}, Rag - {rag}")
            # In a real application, you would play the tune here
            time.sleep(45) # Simulate playing the tune for 45 seconds
        print("Loop complete. Starting next loop in 5 seconds...")
        time.sleep(5)