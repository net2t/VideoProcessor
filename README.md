# StoryGenerator — Free Stack

Fully automated kids story video generator.
**100% Free** — No paid subscriptions needed.

---

## Stack

| Step | Tool | Cost |
|------|------|------|
| Story Generation | Gemini 1.5 Flash API | Free (aistudio.google.com) |
| Image Generation | Pollinations.ai | Free (no key needed) |
| Voice Over | Edge-TTS (Microsoft) | Free |
| Video Build | MoviePy | Free |

---

## Setup (One Time)

### Step 1 — Install Python packages
```bash
pip install -r requirements.txt
```

### Step 2 — Install FFmpeg
Download from https://ffmpeg.org/download.html
Add to system PATH.

### Step 3 — Get Gemini API Key (Free)
1. Go to https://aistudio.google.com
2. Sign in with Google
3. Click "Get API Key"
4. Copy the key

### Step 4 — Set your API key
Open `config.py` and set:
```python
GEMINI_API_KEY = "your_actual_key_here"
```

### Step 5 — Set your base folder path
In `config.py`:
```python
BASE_DIR = r"E:\Pythons\StoryGenerator"
```

---

## Usage

```bash
python main.py
```

Then select from menu:
- **1** — Generate story from theme
- **2** — Generate scene images
- **3** — Generate voice audio
- **4** — Build final video
- **5** — Run all steps at once (recommended)

---

## Folder Structure

```
StoryGenerator/
├── config.py              ← All settings here
├── main.py                ← Run this
├── generate_story.py      ← Gemini API story
├── generate_images.py     ← Pollinations.ai images
├── generate_audio.py      ← Edge-TTS voice
├── build_video.py         ← MoviePy video
├── requirements.txt       ← pip install
│
├── story.json             ← Generated story data
├── images/                ← scene_01.jpg to scene_12.jpg
├── audio/                 ← scene_01.mp3 to scene_12.mp3
├── video/                 ← story_final.mp4
└── music/
    └── bg_music.mp3       ← Optional background music
```

---

## Output

- **Video**: 1920x1080, YouTube ready MP4
- **Captions**: Bold yellow text, black outline
- **Duration**: ~90 seconds (12 scenes × ~7 seconds each)

---

## Tips

- Background music is optional — place `bg_music.mp3` in `music/` folder
- If an image fails to download, run Step 2 again — it skips completed ones
- Each step is independent — re-run any step without losing other work
- Use Option 6 in menu to see current story info anytime
