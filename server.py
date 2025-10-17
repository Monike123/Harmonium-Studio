# server.py
from flask import Flask, request, jsonify, abort, send_file, Response
from werkzeug.utils import secure_filename
import os, re

app = Flask(__name__, static_folder="web", static_url_path="")
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/generate", methods=["POST"])
def generate_music():
    # 1) Validate upload
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    img = request.files["image"]
    fname = secure_filename(img.filename)
    in_path = os.path.join(UPLOAD_FOLDER, fname)
    img.save(in_path)

    # 2) Parse inputs
    try:
        user_duration = float(request.form.get("duration", 7.0))
    except ValueError:
        user_duration = 7.0
    user_raga = request.form.get("raga", "").strip()

    # 3) Core imports
    from image_analysis.color_extractor import extract_dominant_colors
    from image_analysis.swar_mapper import get_swar_and_freq_from_rgb
    from image_analysis.feature_analysis import extract_image_features, derive_music_params_from_features
    from music_generation.raga_selector import choose_raga_from_colors, get_raga_swars
    from music_generation.swar_arranger import arrange_swar_sequence, enhance_swar_sequence
    from music_generation.harmonium_synth import synthesize_sequence_to_audio
    from enhance_tune import generate_from_clean_swar_sequence

    # 4) Raga selection
    colors = extract_dominant_colors(in_path, 7)
    raga = user_raga or choose_raga_from_colors(colors)

    # 5) Build swar_source
    use_raga_mode = True
    if use_raga_mode:
        swar_source = get_raga_swars(raga)
    else:
        swar_source = [get_swar_and_freq_from_rgb(c) for c in colors]

    # 6) Music parameters
    features = extract_image_features(in_path)
    music_params = derive_music_params_from_features(features)

    # 7) Sequence generation
    use_enhanced = True  # toggle or read from form param
    if use_enhanced:
        sequence = enhance_swar_sequence(
            swar_source=swar_source,
            total_duration=user_duration,
            music_params=music_params
        )
    else:
        sequence = arrange_swar_sequence(
            swar_source=swar_source,
            total_duration=user_duration,
            music_params=music_params
        )

    # 8) Audio synthesis
    normal_path   = os.path.join(OUTPUT_FOLDER, "output.wav")
    enhanced_path = os.path.join(OUTPUT_FOLDER, "enhanced_tune.wav")
    synthesize_sequence_to_audio(sequence, normal_path, user_duration)
    generate_from_clean_swar_sequence(sequence, output_file=enhanced_path,max_duration=user_duration)

    # 9) JSON response
    return jsonify({
        "raga": raga,
        "swaras": [s for s, _ in swar_source],
        "normal_url": "/output/output.wav",
        "enhanced_url": "/output/enhanced_tune.wav"
    })

@app.route("/output/<path:filename>")
def serve_audio(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(path):
        abort(404)
    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(path, mimetype='audio/wav')
    size = os.path.getsize(path)
    m = re.match(r"bytes=(\d+)-(\d*)", range_header)
    if not m:
        abort(416)
    start, end = int(m.group(1)), int(m.group(2) or size-1)
    if start >= size or end >= size:
        abort(416)
    length = end - start + 1
    with open(path, 'rb') as f:
        f.seek(start)
        data = f.read(length)
    rv = Response(data, 206, mimetype='audio/wav', direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {start}-{end}/{size}')
    rv.headers.add('Accept-Ranges', 'bytes')
    rv.headers.add('Content-Length', str(length))
    return rv

if __name__ == "__main__":
    app.run(debug=True)
