# File: build_video.py
# Purpose: Combine images + audio + subtitles into video
# MoviePy v2 compatible

import os
import pandas as pd

from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)

# -----------------------------
# PATHS
# -----------------------------

workspace = r"E:\Pythons\StoryGenerator"

image_folder = os.path.join(workspace, "images")
audio_folder = os.path.join(workspace, "audio")
video_folder = os.path.join(workspace, "video")
csv_file = os.path.join(workspace, "manual_input_stories.csv")

output_video = os.path.join(video_folder, "story_01.mp4")

os.makedirs(video_folder, exist_ok=True)

# -----------------------------
# LOAD STORY TEXT
# -----------------------------

try:
    df = pd.read_csv(csv_file, encoding="utf-8")
except:
    df = pd.read_csv(csv_file, encoding="latin-1")

clips = []

# -----------------------------
# BUILD SCENES
# -----------------------------

for i, row in df.iterrows():

    scene_no = int(row["Scene No"])
    subtitle_text = row["Story Text (90 sec total split into 10 scenes)"]

    img_path = f"{image_folder}\\scene_{scene_no:02d}.jpg"
    audio_path = f"{audio_folder}\\scene_{scene_no:02d}.mp3"

    if not os.path.exists(img_path) or not os.path.exists(audio_path):
        print("Missing file for scene", scene_no)
        continue

    audio_clip = AudioFileClip(audio_path)

    img_clip = ImageClip(img_path).with_duration(audio_clip.duration)

    img_clip = img_clip.with_audio(audio_clip)

    # -----------------------------
    # SUBTITLE
    # -----------------------------

    subtitle = (
        TextClip(
            text=subtitle_text,
            font_size=40,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(900, None)
        )
        .with_duration(audio_clip.duration)
        .with_position(("center", "bottom"))
    )

    final_scene = CompositeVideoClip([img_clip, subtitle])

    clips.append(final_scene)

# -----------------------------
# FINAL VIDEO
# -----------------------------

final_clip = concatenate_videoclips(clips, method="compose")

final_clip.write_videofile(
    output_video,
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

print("VIDEO GENERATED:", output_video)