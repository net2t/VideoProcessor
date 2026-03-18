# ============================================================
# generate_images.py
# Step 2: Generate scene images using Pollinations.ai (FREE)
# No API key required — completely free image generation
# Output: images/scene_01.jpg to scene_12.jpg
# ============================================================

import requests
import os
import time
import urllib.parse
from generate_story import load_story
from config import IMAGE_FOLDER, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_MODEL

def build_image_url(prompt: str, seed: int) -> str:
    """
    Build Pollinations.ai URL for image generation
    Format: https://image.pollinations.ai/prompt/{encoded_prompt}
    """
    encoded = urllib.parse.quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={IMAGE_WIDTH}"
        f"&height={IMAGE_HEIGHT}"
        f"&model={IMAGE_MODEL}"
        f"&seed={seed}"
        f"&nologo=true"
        f"&enhance=true"
    )
    return url


def download_image(url: str, save_path: str, scene_no: int, retries: int = 3) -> bool:
    """
    Download image from Pollinations.ai with retry logic
    """
    for attempt in range(1, retries + 1):
        try:
            print(f"  [IMG] Scene {scene_no:02d} — Attempt {attempt}/{retries}...")
            response = requests.get(url, timeout=60)

            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                size_kb = os.path.getsize(save_path) // 1024
                print(f"  [IMG] ✓ Scene {scene_no:02d} saved ({size_kb} KB) → {os.path.basename(save_path)}")
                return True
            else:
                print(f"  [IMG] ✗ HTTP {response.status_code} — Retrying...")
                time.sleep(3)

        except requests.Timeout:
            print(f"  [IMG] ✗ Timeout — Retrying in 5 seconds...")
            time.sleep(5)

        except Exception as e:
            print(f"  [IMG] ✗ Error: {e}")
            time.sleep(3)

    print(f"  [IMG] ✗ Failed after {retries} attempts for scene {scene_no:02d}")
    return False


def generate_all_images():
    """
    Load story JSON and generate image for every scene
    """
    print("=" * 50)
    print("  STEP 2 — IMAGE GENERATOR (Pollinations.ai)")
    print("=" * 50)

    # Load story
    story = load_story()
    scenes = story.get("scenes", [])

    if not scenes:
        print("[IMG] ✗ No scenes found in story.json")
        return

    # Create image folder
    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    total = len(scenes)
    success = 0
    failed = []

    print(f"\n[IMG] Generating {total} images...")
    print(f"[IMG] Resolution: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
    print(f"[IMG] Model: {IMAGE_MODEL}")
    print(f"[IMG] Output: {IMAGE_FOLDER}\n")

    for scene in scenes:
        scene_no  = int(scene["scene"])
        prompt    = scene["image_prompt"]
        save_path = os.path.join(IMAGE_FOLDER, f"scene_{scene_no:02d}.jpg")

        # Skip if already downloaded
        if os.path.exists(save_path):
            size_kb = os.path.getsize(save_path) // 1024
            if size_kb > 10:  # Valid image (not empty/corrupted)
                print(f"  [IMG] Scene {scene_no:02d} already exists — skipping")
                success += 1
                continue

        # Build URL and download
        url = build_image_url(prompt, seed=scene_no * 42)
        ok  = download_image(url, save_path, scene_no)

        if ok:
            success += 1
        else:
            failed.append(scene_no)

        # Polite delay between requests to avoid rate limiting
        time.sleep(2)

    # Summary
    print(f"\n[IMG] ─── Summary ───────────────────────")
    print(f"[IMG] ✓ Success : {success}/{total}")
    if failed:
        print(f"[IMG] ✗ Failed  : Scenes {failed}")
        print(f"[IMG]   Tip: Run again — failed scenes will be retried")
    else:
        print(f"[IMG] ✓ All images downloaded!")
    print(f"[IMG] ✓ Step 2 Complete! Run generate_audio.py next.")


# ─── Run directly ────────────────────────────────────────────
if __name__ == "__main__":
    generate_all_images()
