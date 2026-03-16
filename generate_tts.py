# File: E:\Pythons\StoryGenerator\generate_tts_working.py
# Purpose: Generate TTS from CSV + merge working background music
# Requirements: pip install gtts pandas pydub

import pandas as pd
from gtts import gTTS
from pydub import AudioSegment
import os

# Paths
csv_file = r"E:\Pythons\StoryGenerator\manual_input_stories.csv"
audio_folder = r"E:\Pythons\StoryGenerator\audio"
bg_music_file = r"E:\Pythons\StoryGenerator\audio\background_music.mp3"

os.makedirs(audio_folder, exist_ok=True)

# Load CSV with proper encoding
try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, encoding='latin-1')

for idx, row in df.iterrows():
    scene_no = int(row['Scene No'])
    text = row['Story Text (90 sec total split into 10 scenes)']
    output_file = f"{audio_folder}\\scene_{scene_no:02d}.mp3"

    # Generate TTS
    tts = gTTS(text, lang='en')
    tts.save(output_file)
    print(f"✅ TTS generated for scene {scene_no}")

    # Merge with background music
    try:
        voice = AudioSegment.from_file(output_file)
        bg = AudioSegment.from_file(bg_music_file)

        # Reduce BG volume
        bg = bg - 15  # approx 20% volume

        # Loop/cut background music to match voice length
        while len(bg) < len(voice):
            bg += bg
        bg = bg[:len(voice)]

        # Overlay voice on background
        combined = voice.overlay(bg)
        combined.export(output_file, format="mp3")
        print(f"🎵 Background music merged for scene {scene_no}")

    except FileNotFoundError:
        print(f"⚠️ Background music not found. Skipping BG for scene {scene_no}")