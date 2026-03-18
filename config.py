# ============================================================
# config.py
# Central configuration — edit ONLY this file
# StoryGenerator — Local Phi-2 + Gemini Fallback Version
# ============================================================

import os

# ────────────────────────────────────────────────────────────
# 1. LLM MODE — Choose your story generator
# ────────────────────────────────────────────────────────────
#   True  → Use local Phi-2 model (offline, free, slower)
#   False → Use Gemini API (online, faster, needs API key)
USE_LOCAL_LLM = True

# ────────────────────────────────────────────────────────────
# 2. LOCAL MODEL PATH (Phi-2)
# ────────────────────────────────────────────────────────────
PHI2_MODEL_PATH = r"E:\Pythons\LLM_Models\phi2\Phi-2-2.7B.gguf"

# ────────────────────────────────────────────────────────────
# 3. GEMINI API KEY (only needed if USE_LOCAL_LLM = False)
#    Get free key: https://aistudio.google.com
# ────────────────────────────────────────────────────────────
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# ────────────────────────────────────────────────────────────
# 4. PROJECT PATHS
# ────────────────────────────────────────────────────────────
BASE_DIR     = r"E:\Pythons\StoryGenerator"

STORY_JSON   = os.path.join(BASE_DIR, "story.json")
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
AUDIO_FOLDER = os.path.join(BASE_DIR, "audio")
VIDEO_FOLDER = os.path.join(BASE_DIR, "video")
MUSIC_FILE   = os.path.join(BASE_DIR, "music", "bg_music.mp3")

# ────────────────────────────────────────────────────────────
# 5. STORY SETTINGS
# ────────────────────────────────────────────────────────────
# Note: When using Phi-2, TOTAL_SCENES is fixed at 8
# (small model can't reliably generate 12+ scenes)
# When using Gemini, you can increase this to 12
TOTAL_SCENES = 8
TARGET_AGE   = "4 to 8"

# ────────────────────────────────────────────────────────────
# 6. IMAGE SETTINGS (Pollinations.ai — FREE)
# ────────────────────────────────────────────────────────────
IMAGE_WIDTH  = 1792
IMAGE_HEIGHT = 1024
IMAGE_MODEL  = "flux"    # flux = best quality on Pollinations

# ────────────────────────────────────────────────────────────
# 7. AUDIO / TTS SETTINGS (Edge-TTS — FREE)
# ────────────────────────────────────────────────────────────
TTS_VOICE      = "en-US-AriaNeural"   # Warm female voice — great for kids
TTS_RATE       = "+5%"
TTS_VOLUME     = "+0%"
BG_MUSIC_VOLUME = 0.15

# ────────────────────────────────────────────────────────────
# 8. VIDEO SETTINGS
# ────────────────────────────────────────────────────────────
VIDEO_WIDTH   = 1920
VIDEO_HEIGHT  = 1080
VIDEO_FPS     = 24
VIDEO_CODEC   = "libx264"
VIDEO_OUTPUT  = os.path.join(VIDEO_FOLDER, "story_final.mp4")

# ────────────────────────────────────────────────────────────
# 9. CAPTION SETTINGS
# ────────────────────────────────────────────────────────────
CAPTION_FONT        = "Arial-Bold"
CAPTION_FONTSIZE    = 48
CAPTION_COLOR       = "yellow"
CAPTION_STROKE      = "black"
CAPTION_STROKEWIDTH = 3
CAPTION_POSITION    = ("center", 0.85)
