# StoryGenerator

A local Python application for generating animated stories with text-to-speech narration and video compilation.

## Features

- 🎭 **Story Generation**: Generate scene-wise stories (LLM integration ready)
- 🎤 **Text-to-Speech**: Convert story text to natural-sounding audio using gTTS
- 🎵 **Background Music**: Optional background music mixing with voice narration
- 🎬 **Video Creation**: Combine images and audio into complete story videos
- 💻 **Offline Operation**: Works completely offline once dependencies are installed

## Requirements

- Python 3.11+
- FFmpeg (for video processing)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StoryGenerator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv311
   .\venv311\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install gtts pandas moviepy pydub ffmpeg-python
   ```

4. **Install FFmpeg**
   - Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Add to system PATH

## Usage

### Option 1: Interactive Menu
```bash
python main.py
```

### Option 2: Individual Scripts

1. **Generate TTS Audio**
   ```bash
   python generate_tts.py
   ```

2. **Build Video**
   ```bash
   python build_video.py
   ```

## Project Structure

```
StoryGenerator/
├── main.py              # Interactive menu interface
├── generate_tts.py      # TTS generation script
├── build_video.py       # Video compilation script
├── manual_input_stories.csv  # Story content
├── audio/               # Generated audio files
├── images/              # Scene images
├── video/               # Final video output
├── venv311/            # Virtual environment
└── README.md
```

## Setup Instructions

### 1. Prepare Story Content
Edit `manual_input_stories.csv` with your story scenes:
- Scene No: 1-10
- Story Text: Scene narration text
- Image Prompt: Visual description for each scene
- Voice Script: Voice style notes
- Music Command: Background music cues

### 2. Generate Scene Images
Create 10 scene images (scene_01.jpg to scene_10.jpg) and place them in the `images/` folder.

### 3. Add Background Music (Optional)
Place `background_music.mp3` in the `audio/` folder for automatic mixing.

### 4. Run the Application
```bash
python main.py
```
Select options from the menu to:
1. Generate stories
2. Create audio narration
3. Build final video

## Output

- **Audio Files**: `audio/scene_01.mp3` to `audio/scene_10.mp3`
- **Final Video**: `video/story_01.mp4`

## Customization

### Story Generation
Replace the stub in `generate_stories()` with your preferred LLM (TinyLlama, GPT, etc.).

### Voice Settings
Modify `gTTS` parameters in the audio generation functions:
- Language: `lang='en'`
- Speed: `slow=False`
- Voice: `tld='com'`

### Video Settings
Adjust video parameters in `build_video()`:
- FPS: `fps=24`
- Codec: `codec="libx264"`
- Resolution: Add `.resize()` to image clips

## Troubleshooting

### Python 3.13 Compatibility
If using Python 3.13, you may encounter `audioop` module issues. Use Python 3.11 for best compatibility.

### FFmpeg Not Found
Ensure FFmpeg is installed and added to system PATH:
```bash
ffmpeg -version
```

### MoviePy Import Issues
Use direct imports instead of `moviepy.editor`:
```python
from moviepy import ImageClip, AudioFileClip
```

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Happy Storytelling! 🎭✨**
