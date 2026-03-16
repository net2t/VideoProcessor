# File: E:\Pythons\StoryGenerator\build_video.py
# Purpose: Combine scene images + audio into a single video (90 sec story)
# Requirements: pip install moviepy

import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

# Paths
image_folder = r"E:\Pythons\StoryGenerator\images"
audio_folder = r"E:\Pythons\StoryGenerator\audio"
output_video = r"E:\Pythons\StoryGenerator\video\story_01.mp4"

# Create video directory if it doesn't exist
os.makedirs(os.path.dirname(output_video), exist_ok=True)

# Scene setup
scene_files = [f"{image_folder}\\scene_{i:02d}.jpg" for i in range(1, 11)]
audio_files = [f"{audio_folder}\\scene_{i:02d}.mp3" for i in range(1, 11)]

clips = []

for img, aud in zip(scene_files, audio_files):
    # Load image as video clip (duration = audio length)
    audio_clip = AudioFileClip(aud)
    img_clip = ImageClip(img).with_duration(audio_clip.duration)
    img_clip = img_clip.with_audio(audio_clip)
    
    # Optional: add fade-in/out (commented out for now)
    # img_clip = img_clip.crossfadein(0.5).crossfadeout(0.5)
    
    clips.append(img_clip)

# Concatenate all scenes
final_clip = concatenate_videoclips(clips, method="compose")

# Export final video
final_clip.write_videofile(output_video, fps=24, codec="libx264")

print(" Video generated successfully:", output_video)