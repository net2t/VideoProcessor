# ============================================================
# build_video.py
# Step 4: Combine images + audio + captions → final MP4 video
# Output: video/story_final.mp4 (1920x1080, YouTube ready)
# ============================================================

import os
import sys
from PIL import Image as PILImage
import numpy as np

from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)

from generate_story import load_story
from config import (
    IMAGE_FOLDER, AUDIO_FOLDER, VIDEO_OUTPUT,
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, VIDEO_CODEC,
    CAPTION_FONT, CAPTION_FONTSIZE, CAPTION_COLOR,
    CAPTION_STROKE, CAPTION_STROKEWIDTH, CAPTION_POSITION
)


def resize_image_to_canvas(img_path: str) -> np.ndarray:
    """
    Load image and resize/crop to exactly 1920x1080
    Fills black bars if aspect ratio doesn't match
    """
    img = PILImage.open(img_path).convert("RGB")

    # Target canvas
    canvas_w, canvas_h = VIDEO_WIDTH, VIDEO_HEIGHT
    img_w, img_h = img.size

    # Scale to fill height, then crop width
    scale = canvas_h / img_h
    new_w = int(img_w * scale)
    new_h = canvas_h

    if new_w < canvas_w:
        # Scale to fill width instead
        scale = canvas_w / img_w
        new_w = canvas_w
        new_h = int(img_h * scale)

    img = img.resize((new_w, new_h), PILImage.LANCZOS)

    # Center crop to exact canvas size
    left = (new_w - canvas_w) // 2
    top  = (new_h - canvas_h) // 2
    img  = img.crop((left, top, left + canvas_w, top + canvas_h))

    return np.array(img)


def build_scene_clip(scene: dict, scene_no: int) -> CompositeVideoClip | None:
    """
    Build one scene clip = image + audio + caption overlay
    Returns None if files are missing
    """
    img_path   = os.path.join(IMAGE_FOLDER, f"scene_{scene_no:02d}.jpg")
    audio_path = os.path.join(AUDIO_FOLDER, f"scene_{scene_no:02d}.mp3")
    caption    = str(scene.get("caption", ""))

    # Check files exist
    if not os.path.exists(img_path):
        print(f"  [VID] ✗ Missing image: {img_path} — skipping scene {scene_no}")
        return None

    if not os.path.exists(audio_path):
        print(f"  [VID] ✗ Missing audio: {audio_path} — skipping scene {scene_no}")
        return None

    try:
        # Load audio (duration comes from audio)
        audio_clip = AudioFileClip(audio_path)
        duration   = audio_clip.duration

        # Load and resize image
        img_array  = resize_image_to_canvas(img_path)
        img_clip   = ImageClip(img_array).with_duration(duration)
        img_clip   = img_clip.with_audio(audio_clip)

        # Build caption text clip
        layers = [img_clip]

        if caption.strip():
            # Wrap long captions
            max_chars = 60
            if len(caption) > max_chars:
                # Simple word wrap
                words = caption.split()
                lines, current = [], ""
                for word in words:
                    if len(current) + len(word) + 1 <= max_chars:
                        current += (" " if current else "") + word
                    else:
                        lines.append(current)
                        current = word
                if current:
                    lines.append(current)
                caption = "\n".join(lines)

            txt_clip = TextClip(
                text=caption,
                font=CAPTION_FONT,
                font_size=CAPTION_FONTSIZE,
                color=CAPTION_COLOR,
                stroke_color=CAPTION_STROKE,
                stroke_width=CAPTION_STROKEWIDTH,
                method="caption",
                size=(VIDEO_WIDTH - 100, None),  # Padding 50px each side
                text_align="center"
            )

            # Position at bottom center
            txt_clip = txt_clip.with_position(("center", VIDEO_HEIGHT - txt_clip.h - 50))
            txt_clip = txt_clip.with_duration(duration)

            layers.append(txt_clip)

        # Compose scene
        scene_clip = CompositeVideoClip(layers, size=(VIDEO_WIDTH, VIDEO_HEIGHT))
        print(f"  [VID] ✓ Scene {scene_no:02d} — {duration:.1f}s — '{caption[:40]}...' " if len(caption) > 40 else f"  [VID] ✓ Scene {scene_no:02d} — {duration:.1f}s")
        return scene_clip

    except Exception as e:
        print(f"  [VID] ✗ Scene {scene_no:02d} error: {e}")
        return None


def build_video():
    """
    Build complete video from all scenes
    """
    print("=" * 50)
    print("  STEP 4 — VIDEO BUILDER (MoviePy)")
    print("=" * 50)

    # Load story
    story  = load_story()
    scenes = story.get("scenes", [])

    if not scenes:
        print("[VID] ✗ No scenes found in story.json")
        return

    # Create output folder
    os.makedirs(os.path.dirname(VIDEO_OUTPUT), exist_ok=True)

    print(f"\n[VID] Story  : {story.get('story_title', 'Untitled')}")
    print(f"[VID] Scenes : {len(scenes)}")
    print(f"[VID] Output : {VIDEO_OUTPUT}")
    print(f"[VID] Size   : {VIDEO_WIDTH}x{VIDEO_HEIGHT} @ {VIDEO_FPS}fps\n")

    # Build each scene clip
    clips = []
    for scene in scenes:
        scene_no = int(scene["scene"])
        clip = build_scene_clip(scene, scene_no)
        if clip:
            clips.append(clip)

    if not clips:
        print("[VID] ✗ No valid clips built — check images and audio folders")
        return

    print(f"\n[VID] Concatenating {len(clips)} scenes...")

    # Concatenate all scenes
    final = concatenate_videoclips(clips, method="compose")

    total_duration = sum(c.duration for c in clips)
    print(f"[VID] Total duration : {total_duration:.1f} seconds ({total_duration/60:.1f} min)")
    print(f"[VID] Rendering video — this may take a few minutes...\n")

    # Export video
    final.write_videofile(
        VIDEO_OUTPUT,
        fps=VIDEO_FPS,
        codec=VIDEO_CODEC,
        audio_codec="aac",
        threads=2,           # Safe for low-end CPU
        preset="medium",     # Balance speed vs quality
        logger="bar"
    )

    print(f"\n[VID] ✓ Video saved: {VIDEO_OUTPUT}")
    print(f"[VID] ✓ Step 4 Complete! Your story video is ready.")

    # Print YouTube metadata
    yt = story.get("youtube", {})
    if yt:
        print(f"\n{'='*50}")
        print(f"  YouTube Upload Info")
        print(f"{'='*50}")
        print(f"  Title      : {yt.get('title', '')}")
        print(f"  Hook       : {yt.get('hook_line', '')}")
        print(f"  Tags       : {yt.get('tags', '')}")
        print(f"  Alt Title  : {yt.get('alt_title', '')}")


# ─── Run directly ────────────────────────────────────────────
if __name__ == "__main__":
    build_video()
