# File: main.py
# Purpose: Local Story Generator, TTS, and Video Builder (Offline)
# Python 3.11+ compatible

import os
import pandas as pd
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

# -----------------------------
# Paths (update if required)
# -----------------------------
workspace = r"E:\Pythons\StoryGenerator"
csv_file = os.path.join(workspace, "manual_input_stories.csv")
audio_folder = os.path.join(workspace, "audio")
images_folder = os.path.join(workspace, "images")
video_folder = os.path.join(workspace, "video")
bg_music_file = os.path.join(audio_folder, "background_music.mp3")  # optional

# Create folders if missing
os.makedirs(audio_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

# -----------------------------
# Story Generation Stub (LLM)
# -----------------------------
def generate_stories():
    # Example: replace this with TinyLlama inference code
    print("\n[INFO] Story generation via TinyLlama (stub)")
    stories = []
    for i in range(1, 11):
        stories.append(f"Scene {i}: The hero embarks on adventure #{i}.")
    # Save to CSV
    df = pd.DataFrame({
        "Scene No": list(range(1, 11)),
        "Story Text (90 sec total split into 10 scenes)": stories
    })
    df.to_csv(csv_file, index=False, encoding='utf-8')
    print("[DONE] Stories saved to manual_input_stories.csv")

# -----------------------------
# Audio Generation (TTS + optional BG)
# -----------------------------
def generate_audio():
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except:
        df = pd.read_csv(csv_file, encoding='latin-1')

    for idx, row in df.iterrows():
        scene_no = int(row['Scene No'])
        text = row['Story Text (90 sec total split into 10 scenes)']
        output_file = os.path.join(audio_folder, f"scene_{scene_no:02d}.mp3")

        # TTS
        tts = gTTS(text, lang='en')
        tts.save(output_file)
        print(f"✅ TTS generated: scene {scene_no}")

        # Optional: Merge BG music (simple MoviePy approach)
        if os.path.exists(bg_music_file):
            try:
                voice_clip = AudioFileClip(output_file)
                bg_clip = AudioFileClip(bg_music_file).volumex(0.2)
                bg_clip = bg_clip.set_duration(voice_clip.duration)
                final_clip = CompositeAudioClip([bg_clip, voice_clip])
                final_clip.write_audiofile(output_file, verbose=False, logger=None)
                print(f"🎵 BG music merged: scene {scene_no}")
            except Exception as e:
                print(f"⚠️ BG music merge failed for scene {scene_no}: {e}")

# -----------------------------
# Video Builder
# -----------------------------
def build_video():
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except:
        df = pd.read_csv(csv_file, encoding='latin-1')

    clips = []
    for idx, row in df.iterrows():
        scene_no = int(row['Scene No'])
        img_path = os.path.join(images_folder, f"scene_{scene_no:02d}.jpg")
        audio_path = os.path.join(audio_folder, f"scene_{scene_no:02d}.mp3")
        
        if not os.path.exists(img_path) or not os.path.exists(audio_path):
            print(f"⚠️ Missing file for scene {scene_no}, skipping...")
            continue
        
        img_clip = ImageClip(img_path).set_duration(AudioFileClip(audio_path).duration)
        audio_clip = AudioFileClip(audio_path)
        img_clip = img_clip.set_audio(audio_clip)
        clips.append(img_clip)

    if clips:
        final_video_path = os.path.join(video_folder, "story_01.mp4")
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(final_video_path, fps=24)
        print(f"[DONE] Video created: {final_video_path}")
    else:
        print("[ERROR] No clips to build video")

# -----------------------------
# Main Menu
# -----------------------------
def main_menu():
    while True:
        print("\n=== StoryGenerator Local Menu ===")
        print("1. Generate Stories (LLM)")
        print("2. Generate Audio (TTS + optional BG music)")
        print("3. Build Video")
        print("4. Exit")
        choice = input("Select option (1-4): ").strip()
        if choice == "1":
            generate_stories()
        elif choice == "2":
            generate_audio()
        elif choice == "3":
            build_video()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("⚠️ Invalid choice, try again.")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main_menu()