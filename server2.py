from flask import Flask, send_from_directory, jsonify, request
import os, random, threading, time
from pydub import AudioSegment
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"

# Core imports (from your old working pipeline)
from image_analysis.color_extractor import extract_dominant_colors
from image_analysis.swar_mapper import get_swar_and_freq_from_rgb
from image_analysis.feature_analysis import extract_image_features, derive_music_params_from_features
from music_generation.raga_selector import choose_raga_from_colors, get_raga_swars
from music_generation.swar_arranger import arrange_swar_sequence, enhance_swar_sequence
from music_generation.harmonium_synth import synthesize_sequence_to_audio
from enhance_tune import generate_from_clean_swar_sequence
from config import RAGA_LIBRARY


app = Flask(__name__, static_folder="static2", template_folder="static2")

IMAGE_DIR = "random_images"
TUNE_DIR = "generated_tunes"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(TUNE_DIR, exist_ok=True)

# Global state variables
lock = threading.Lock()
running = False
start_time = 0
processed = 0
selected_images = []  # List of 10 selected images
current_index = 0     # Current playing index (0-9)
generation_complete = False
playback_start_time = 0

def generate_real_tune(image_path, duration, output_path):
    """Generate a single tune from an image"""
    try:
        # 1. Extract features
        raga = random.choice(list(RAGA_LIBRARY.keys()))
        swar_source = get_raga_swars(raga)

        features = extract_image_features(image_path)
        music_params = derive_music_params_from_features(features)

        # 2. Sequence generation
        sequence = enhance_swar_sequence(
            swar_source=swar_source,
            total_duration=duration,
            music_params=music_params
        )

        # 3. Synthesize to audio
        temp_path = output_path + ".temp.wav"
        synthesize_sequence_to_audio(sequence, temp_path, duration)
        generate_from_clean_swar_sequence(sequence, output_file=output_path, max_duration=duration)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return True
    except Exception as e:
        print(f"Error generating tune for {image_path}: {e}")
        return False

def batch_tune_generator(duration):
    """Generate tunes for all 10 selected images"""
    global running, processed, generation_complete, playback_start_time, current_index, selected_images
    
    try:
        # Generate tunes for all selected images
        for i, image_name in enumerate(selected_images):
            if not running:  # Check if stopped during generation
                break
                
            image_path = os.path.join(IMAGE_DIR, image_name)
            tune_name = f"{os.path.splitext(image_name)[0]}_tune.wav"
            tune_path = os.path.join(TUNE_DIR, tune_name)
            
            print(f"Generating tune {i+1}/10: {image_name}")
            
            success = generate_real_tune(image_path, duration, tune_path)
            
            with lock:
                if success:
                    processed += 1
                else:
                    print(f"Failed to generate tune for {image_name}")
        
        # Mark generation as complete and start playback
        with lock:
            if running and processed > 0:
                generation_complete = True
                current_index = 0
                playback_start_time = time.time()
                print(f"Generation complete! Generated {processed} tunes. Starting playback...")
            
    except Exception as e:
        print(f"Error in batch generation: {e}")
        with lock:
            running = False

def select_random_images():
    """Select 10 random images from the directory"""
    try:
        available_images = [
            f for f in os.listdir(IMAGE_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        
        if len(available_images) < 10:
            # If less than 10 images, repeat some to make 10
            selected = available_images * (10 // len(available_images) + 1)
            return selected[:10]
        else:
            return random.sample(available_images, 10)
            
    except Exception as e:
        print(f"Error selecting images: {e}")
        return []

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/start", methods=["POST"])
def start():
    global running, processed, start_time, selected_images, generation_complete, current_index, playback_start_time
    
    try:
        data = request.get_json()
        duration = int(data.get("duration", 15)) if data else 15
    except (ValueError, TypeError):
        duration = 15
    
    with lock:
        if not running:
            # Reset all state
            running = True
            processed = 0
            generation_complete = False
            current_index = 0
            start_time = time.time()
            playback_start_time = 0
            
            # Select 10 random images
            selected_images = select_random_images()
            
            if not selected_images:
                running = False
                return jsonify({"status": "error", "message": "No images found in directory"})
            
            print(f"Selected {len(selected_images)} images for generation")
            
            # Start batch generation in background thread
            threading.Thread(target=batch_tune_generator, args=(duration,), daemon=True).start()
            
            return jsonify({"status": "started", "selected_count": len(selected_images)})
        else:
            return jsonify({"status": "already_running"})

@app.route("/stop", methods=["POST"])
def stop():
    global running, generation_complete, current_index, playback_start_time
    
    with lock:
        running = False
        generation_complete = False
        current_index = 0
        playback_start_time = 0
        
    return jsonify({"status": "stopped"})

@app.route("/status")
def status():
    global running, start_time, processed, selected_images, generation_complete, playback_start_time, current_index
    
    with lock:
        now = time.time()
        elapsed = int(now - start_time) if running else 0
        
        response_data = {
            "elapsed": elapsed,
            "count": processed,
            "total_images": len(selected_images),
            "generation_complete": generation_complete,
            "running": running
        }
        
        if generation_complete and running and processed > 0 and len(selected_images) > 0:
            # Calculate which tune should be playing based on time
            time_since_playback = now - playback_start_time
            tune_duration = 15  # Default duration, should match the actual duration
            
            # Calculate current index based on elapsed time
            calculated_index = int(time_since_playback // tune_duration) % len(selected_images)
            
            # Update current index if it's time for the next tune
            if calculated_index != current_index:
                current_index = calculated_index
                playback_start_time = now - (calculated_index * tune_duration)
            
            # Get current image and tune
            if current_index < len(selected_images):
                current_image = selected_images[current_index]
                current_tune = f"{os.path.splitext(current_image)[0]}_tune.wav"
                
                # Calculate remaining time for current tune
                time_in_current_tune = time_since_playback % tune_duration
                remaining_time = max(0, tune_duration - time_in_current_tune)
                
                response_data.update({
                    "image": current_image,
                    "tune": current_tune,
                    "current_index": current_index + 1,  # 1-based for display
                    "remaining": round(remaining_time, 1),
                    "progress": round((time_in_current_tune / tune_duration) * 100, 1)
                })
        
        return jsonify(response_data)

@app.route("/image/<filename>")
def get_image(filename):
    try:
        return send_from_directory(IMAGE_DIR, filename)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404

@app.route("/tune/<filename>")
def get_tune(filename):
    try:
        return send_from_directory(TUNE_DIR, filename)
    except FileNotFoundError:
        return jsonify({"error": "Tune not found"}), 404

# Health check endpoint
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "running": running,
        "processed": processed,
        "total_images": len(selected_images)
    })

if __name__ == "__main__":
    print("Starting Harmonium Server...")
    print(f"Image directory: {IMAGE_DIR}")
    print(f"Tune directory: {TUNE_DIR}")
    
    # Check if directories exist and have content
    if os.path.exists(IMAGE_DIR):
        image_count = len([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        print(f"Found {image_count} images in {IMAGE_DIR}")
    else:
        print(f"Warning: {IMAGE_DIR} directory not found!")
    
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
