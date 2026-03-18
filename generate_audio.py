# ============================================================
# generate_audio.py
# Step 3: Generate voice-over audio using Edge-TTS (FREE)
# Microsoft neural voices — high quality, offline capable
# Optionally mixes background music at low volume
# Output: audio/scene_01.mp3 to scene_12.mp3
# ============================================================

import asyncio
import edge_tts
import os
import sys
from generate_story import load_story
from config import (
    AUDIO_FOLDER, MUSIC_FILE,
    TTS_VOICE, TTS_RATE, TTS_VOLUME,
    BG_MUSIC_VOLUME
)

# MoviePy for audio mixing (only if bg music exists)
try:
    from moviepy import AudioFileClip, CompositeAudioClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False


async def generate_tts(text: str, output_path: str, scene_no: int):
    """
    Generate TTS audio for one scene using Edge-TTS
    """
    communicate = edge_tts.Communicate(
        text=text,
        voice=TTS_VOICE,
        rate=TTS_RATE,
        volume=TTS_VOLUME
    )
    await communicate.save(output_path)
    size_kb = os.path.getsize(output_path) // 1024
    print(f"  [TTS] ✓ Scene {scene_no:02d} — voice saved ({size_kb} KB)")


def mix_with_background(voice_path: str, scene_no: int):
    """
    Mix voice audio with background music at low volume
    Overwrites the voice file with mixed version
    """
    if not MOVIEPY_AVAILABLE:
        print(f"  [BGM] MoviePy not available — skipping music mix")
        return

    if not os.path.exists(MUSIC_FILE):
        return  # No music file — skip silently

    try:
        voice = AudioFileClip(voice_path)
        music = AudioFileClip(MUSIC_FILE)

        # Trim/loop music to match voice duration
        if music.duration < voice.duration:
            # Loop music if shorter than voice
            loops = int(voice.duration / music.duration) + 1
            from moviepy import concatenate_audioclips
            music = concatenate_audioclips([music] * loops)

        music = music.subclipped(0, voice.duration)
        music = music.with_volume_scaled(BG_MUSIC_VOLUME)

        # Mix voice over music
        final = CompositeAudioClip([music, voice])
        final.write_audiofile(voice_path, logger=None)

        print(f"  [BGM] ✓ Scene {scene_no:02d} — background music mixed")

    except Exception as e:
        print(f"  [BGM] ✗ Scene {scene_no:02d} mix failed: {e}")
        print(f"  [BGM]   Using voice only (no music)")


def generate_all_audio():
    """
    Load story JSON and generate audio for every scene
    """
    print("=" * 50)
    print("  STEP 3 — AUDIO GENERATOR (Edge-TTS)")
    print("=" * 50)

    # Load story
    story = load_story()
    scenes = story.get("scenes", [])

    if not scenes:
        print("[TTS] ✗ No scenes found in story.json")
        return

    # Create audio folder
    os.makedirs(AUDIO_FOLDER, exist_ok=True)

    total   = len(scenes)
    success = 0
    failed  = []

    bg_music_exists = os.path.exists(MUSIC_FILE)
    print(f"\n[TTS] Voice    : {TTS_VOICE}")
    print(f"[TTS] Speed    : {TTS_RATE}")
    print(f"[TTS] Scenes   : {total}")
    print(f"[TTS] BG Music : {'✓ Found' if bg_music_exists else '✗ Not found (voice only)'}")
    print(f"[TTS] Output   : {AUDIO_FOLDER}\n")

    for scene in scenes:
        scene_no    = int(scene["scene"])
        voice_text  = str(scene["voice_over"])
        output_path = os.path.join(AUDIO_FOLDER, f"scene_{scene_no:02d}.mp3")

        # Skip if already exists
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) // 1024
            if size_kb > 5:
                print(f"  [TTS] Scene {scene_no:02d} already exists — skipping")
                success += 1
                continue

        try:
            # Generate TTS
            asyncio.run(generate_tts(voice_text, output_path, scene_no))

            # Mix with background music if available
            if bg_music_exists:
                mix_with_background(output_path, scene_no)

            success += 1

        except Exception as e:
            print(f"  [TTS] ✗ Scene {scene_no:02d} failed: {e}")
            failed.append(scene_no)

    # Summary
    print(f"\n[TTS] ─── Summary ───────────────────────")
    print(f"[TTS] ✓ Success : {success}/{total}")
    if failed:
        print(f"[TTS] ✗ Failed  : Scenes {failed}")
    else:
        print(f"[TTS] ✓ All audio files generated!")
    print(f"[TTS] ✓ Step 3 Complete! Run build_video.py next.")


# ─── Run directly ────────────────────────────────────────────
if __name__ == "__main__":
    generate_all_audio()
