# 🎹 Harmonium Studio

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

> Transform random images into mesmerizing Indian Classical music using AI-powered raga synthesis

---

## 📖 Description

**Harmonium Studio** is an innovative AI-based music generation system that bridges visual art and Indian classical music. The application intelligently analyzes random images and maps them to traditional ragas, creating authentic swar sequences that follow the rules of Hindustani classical music theory.

Unlike conventional music generators, Harmonium Studio employs sophisticated backtracking algorithms and smooth transition logic to ensure melodic coherence. The system avoids repetitive 2-3 note patterns, instead crafting dynamic melodies that respect the raga's characteristics while maintaining musical flow. Each generated tune is synthesized into high-quality WAV audio and served through an elegant Flask web interface with real-time playback and automatic regeneration capabilities.

Whether you're a music enthusiast, AI researcher, or cultural tech explorer, Harmonium Studio offers a unique intersection of machine learning, audio synthesis, and the rich tradition of Indian classical music.

---

## 🎥 Demo

https://github.com/user-attachments/assets/6cb769b0-4218-43c8-94b5-a76976214435

---

## ✨ Features

- 🖼️ **AI-Based Image → Raga Mapping**: Intelligent analysis of visual input to select appropriate ragas
- 🎼 **WAV Tune Synthesis**: High-quality audio generation with randomized swar sequences
- 🔄 **Smooth Transitions**: Advanced backtracking ensures melodic continuity and flow
- 🚫 **No Repetition**: Sophisticated algorithm prevents monotonous 2-3 note patterns
- 🌐 **Flask Web Interface**: Real-time browser-based playback and tune regeneration
- 🔁 **Automatic Looping**: Continuous music generation with seamless transitions
- 💾 **Export Capability**: Save generated tunes as WAV files for offline use
- 🎨 **Random Image Processing**: Uses diverse image inputs for varied musical outputs

---

## ⚙️ How It Works

1️⃣ **Input**: A random image is selected from the repository or uploaded by the user  
2️⃣ **Analysis**: The system extracts tonal and visual characteristics from the image  
3️⃣ **Raga Mapping**: AI maps these features to a suitable Indian classical raga  
4️⃣ **Swar Generation**: Creates melodic sequences following raga rules with intelligent variation  
5️⃣ **Synthesis**: Converts the swar sequence into a high-quality WAV audio file  
6️⃣ **Playback**: The Flask backend serves the tune with automatic looping and regeneration

---

## 🧩 Tech Stack

- **Python 3.x** - Core programming language
- **Flask** - Web framework for the backend and API
- **Pydub** - Audio processing and WAV synthesis
- **Custom Melody Engine** - Proprietary backtracking and transition algorithms
- **PIL/Pillow** - Image processing and analysis
- **NumPy** - Numerical computations for audio generation
- **HTML/CSS/JavaScript** - Frontend interface

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Monike123/Harmonium-Studio.git

# Navigate to project directory
cd Harmonium-Studio

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will start on `http://localhost:5000`

---

## 🖥️ Usage

1. **Launch the Web App**: Open your browser and navigate to `http://localhost:5000`
2. **Generate Tune**: Click the "Generate" button to create a new raga-based tune
3. **Listen**: The tune will automatically play in your browser with looping
4. **Regenerate**: Click "Regenerate" to create a new variation with different images
5. **Export**: Download generated tunes as WAV files from the `generated_tunes/` directory
6. **Explore**: View the random images used for generation in the interface

---

## 📂 Project Structure

```
Harmonium-Studio/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
│
├── static2/               # Static assets (CSS, JS, audio files)
│   ├── css/
│   ├── js/
│   └── audio/
│
├── random_images/         # Source images for raga mapping
│   └── *.jpg/png
│
├── generated_tunes/       # Output WAV files
│   └── *.wav
│
├── templates/             # HTML templates
│   └── index.html
│
└── utils/                 # Helper modules
    ├── raga_engine.py    # Raga logic and swar generation
    ├── audio_synth.py    # WAV synthesis
    └── image_processor.py # Image analysis
```

---

## 🤝 Contributing

Contributions are welcome! Whether you want to:

- 🐛 Report bugs
- 💡 Suggest new ragas or features
- 🎨 Improve the UI/UX
- 📝 Enhance documentation
- 🔧 Optimize the melody engine

Feel free to open an issue or submit a pull request. Let's make Harmonium Studio even better together!

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Developed by Manas Sawant**  
*AI Developer & Music Tech Enthusiast*

🔗 [GitHub](https://github.com/Monike123) | 🌐 [LinkedIn](#) | 📧 [Email](#)

---

<div align="center">
  
### 🎶 *Where Visual Art Meets Classical Music* 🎶

**Star ⭐ this repository if you find it interesting!**

</div>
