# ============================================================
# generate_story.py
# Step 1: Generate kids story
# PRIMARY  → Phi-2 Local GGUF model (100% offline, free)
# FALLBACK → Gemini API (if local fails and key is set)
# ============================================================

import json
import os
import sys
import re
import time
from config import (
    GEMINI_API_KEY,
    STORY_JSON,
    TOTAL_SCENES,
    TARGET_AGE,
    PHI2_MODEL_PATH,
    USE_LOCAL_LLM
)


# ════════════════════════════════════════════════════════════
# SECTION 1 — PROMPT BUILDER
# ════════════════════════════════════════════════════════════

def build_prompt(theme: str) -> str:
    """
    Build a very structured prompt that guides Phi-2
    to produce clean JSON output scene by scene.
    Phi-2 is small — we keep instructions short and direct.
    """
    return f"""You are a kids story writer. Write a story about "{theme}".
Output ONLY valid JSON. No extra text. No explanation.

Rules:
- Animal main character with short name
- Exactly 8 scenes
- Simple English for age 4-8
- Each scene: scene number, time, image_prompt, voice_over, caption

JSON structure to fill:
{{
  "story_title": "...",
  "story_moral": "...",
  "character_1": "...",
  "character_2": "",
  "character_3": "",
  "image_style": "3D Pixar-style, bright colors, cinematic lighting, children's animation",
  "video_style": "3D animated kids story, smooth motion, colorful, cinematic",
  "scenes": [
    {{"scene": 1, "time": "0:00-0:08", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}},
    {{"scene": 2, "time": "0:08-0:16", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}},
    {{"scene": 3, "time": "0:16-0:24", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}},
    {{"scene": 4, "time": "0:24-0:32", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}},
    {{"scene": 5, "time": "0:32-0:40", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}},
    {{"scene": 6, "time": "0:40-0:48", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}},
    {{"scene": 7, "time": "0:48-0:56", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}},
    {{"scene": 8, "time": "0:56-1:04", "image_prompt": "..., 3D Pixar-style, bright colors, cinematic lighting, children's animation", "voice_over": "...", "caption": "..."}}
  ],
  "youtube": {{
    "title": "...",
    "hook_line": "...",
    "description": "...",
    "tags": "kids story, animation, bedtime story, moral story, {theme}",
    "alt_title": "...",
    "thumbnail_prompt": "..., 3D Pixar-style, bright colors",
    "background_music_prompt": "soft gentle kids background music, warm and magical"
  }}
}}

Now write the story about "{theme}":
"""


# ════════════════════════════════════════════════════════════
# SECTION 2 — JSON FIXER
# Phi-2 sometimes produces slightly broken JSON
# This function tries to clean and repair it
# ════════════════════════════════════════════════════════════

def extract_and_fix_json(raw_text: str) -> dict:
    """
    Try multiple strategies to extract valid JSON from LLM output.
    Phi-2 is not perfectly reliable with JSON — we handle that here.
    """

    # Strategy 1: Find JSON block between { and last }
    start = raw_text.find("{")
    end   = raw_text.rfind("}") + 1

    if start == -1 or end == 0:
        raise ValueError("No JSON object found in output")

    json_text = raw_text[start:end]

    # Strategy 2: Try direct parse
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        pass

    # Strategy 3: Fix common Phi-2 issues
    # Remove trailing commas before } or ]
    json_text = re.sub(r",\s*([}\]])", r"\1", json_text)

    # Fix unescaped quotes inside strings (basic)
    # Replace smart quotes with straight quotes
    json_text = json_text.replace("\u201c", '"').replace("\u201d", '"')
    json_text = json_text.replace("\u2018", "'").replace("\u2019", "'")

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        pass

    # Strategy 4: Extract just the scenes manually and build structure
    print("[STORY] ⚠ JSON broken — attempting manual scene extraction...")
    return manual_scene_extract(raw_text)


def manual_scene_extract(raw_text: str) -> dict:
    """
    Last resort: if JSON is too broken, extract scenes manually
    using regex and build a valid structure ourselves
    """
    scenes = []

    # Find all voice_over values
    voice_overs = re.findall(r'"voice_over"\s*:\s*"([^"]+)"', raw_text)
    captions    = re.findall(r'"caption"\s*:\s*"([^"]+)"', raw_text)
    img_prompts = re.findall(r'"image_prompt"\s*:\s*"([^"]+)"', raw_text)
    story_title = re.search(r'"story_title"\s*:\s*"([^"]+)"', raw_text)
    story_moral = re.search(r'"story_moral"\s*:\s*"([^"]+)"', raw_text)
    character_1 = re.search(r'"character_1"\s*:\s*"([^"]+)"', raw_text)

    if not voice_overs:
        raise ValueError("Could not extract any scenes from model output")

    total = len(voice_overs)
    times = [f"0:{i*8:02d}-0:{(i+1)*8:02d}" for i in range(total)]

    for i in range(total):
        scenes.append({
            "scene":        i + 1,
            "time":         times[i] if i < len(times) else f"0:{i*8:02d}",
            "image_prompt": (img_prompts[i] if i < len(img_prompts) else voice_overs[i])
                            + ", 3D Pixar-style, bright colors, cinematic lighting, children's animation",
            "voice_over":   voice_overs[i],
            "caption":      captions[i] if i < len(captions) else voice_overs[i][:40]
        })

    return {
        "story_title":  story_title.group(1) if story_title else "A Wonderful Story",
        "story_moral":  story_moral.group(1) if story_moral else "Always work together",
        "character_1":  character_1.group(1) if character_1 else "A brave little animal",
        "character_2":  "",
        "character_3":  "",
        "image_style":  "3D Pixar-style, bright colors, cinematic lighting, children's animation",
        "video_style":  "3D animated kids story, smooth motion, colorful, cinematic",
        "scenes":       scenes,
        "youtube": {
            "title":                    story_title.group(1) if story_title else "A Kids Story",
            "hook_line":                "A story your kids will love!",
            "description":              "A beautiful animated kids story with a moral lesson.",
            "tags":                     "kids story, animation, bedtime story, moral story",
            "alt_title":                "A Story For Kids",
            "thumbnail_prompt":         "cute animal character in colorful forest, 3D Pixar-style",
            "background_music_prompt":  "soft gentle kids background music, warm and magical"
        }
    }


# ════════════════════════════════════════════════════════════
# SECTION 3 — LOCAL PHI-2 GENERATOR
# ════════════════════════════════════════════════════════════

def generate_with_phi2(theme: str) -> dict:
    """
    Generate story using local Phi-2 GGUF model
    Runs 100% offline — no internet needed
    """
    print("[STORY] Loading Phi-2 model from local disk...")
    print("[STORY] ⚠ First load takes 30-60 seconds on your CPU — please wait...")

    try:
        from llama_cpp import Llama
    except ImportError:
        print("[STORY] ✗ llama-cpp-python not installed!")
        print("[STORY]   Run: pip install llama-cpp-python")
        sys.exit(1)

    if not os.path.exists(PHI2_MODEL_PATH):
        print(f"[STORY] ✗ Model file not found: {PHI2_MODEL_PATH}")
        print("[STORY]   Check PHI2_MODEL_PATH in config.py")
        sys.exit(1)

    # Load model
    # n_ctx=2048 → enough for our prompt + response
    # n_threads=2 → safe for i5-4210U (2 cores, 4 threads)
    # verbose=False → hide llama.cpp internal logs
    llm = Llama(
        model_path=PHI2_MODEL_PATH,
        n_ctx=2048,
        n_threads=2,
        n_gpu_layers=0,    # CPU only — no GPU on your PC
        verbose=False
    )

    print("[STORY] ✓ Model loaded successfully!")
    print("[STORY] Generating story — this takes 2-5 minutes on CPU...")
    print("[STORY] Please be patient ☕")

    prompt = build_prompt(theme)

    start_time = time.time()

    output = llm(
        prompt,
        max_tokens=1800,    # Enough for 8 scenes
        temperature=0.7,    # Balanced creativity
        top_p=0.9,
        repeat_penalty=1.1, # Avoid repetition
        stop=["```", "###", "Note:", "Note :", "Explanation"]
    )

    elapsed = time.time() - start_time
    print(f"[STORY] ✓ Generation complete in {elapsed:.0f} seconds")

    raw_text = output["choices"][0]["text"]

    print("[STORY] Parsing and fixing JSON output...")
    story_data = extract_and_fix_json(raw_text)

    return story_data


# ════════════════════════════════════════════════════════════
# SECTION 4 — GEMINI FALLBACK GENERATOR
# ════════════════════════════════════════════════════════════

def generate_with_gemini(theme: str) -> dict:
    """
    Fallback: Generate story using Gemini API
    Only used if USE_LOCAL_LLM = False in config.py
    """
    print("[STORY] Using Gemini API (online fallback)...")

    try:
        from google import genai
    except ImportError:
        print("[STORY] ✗ google-genai not installed. Run: pip install google-genai")
        sys.exit(1)

    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("[STORY] ✗ Gemini API key not set in config.py")
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Gemini gets fuller prompt since it's more capable
    prompt = f"""
You are a creative AI that writes structured kids story data for animated YouTube videos.
Theme: {theme}
Generate a kids story with exactly {TOTAL_SCENES} scenes for age {TARGET_AGE}.

RETURN ONLY valid JSON matching this structure exactly:
{{
  "story_title": "...",
  "story_moral": "...",
  "character_1": "animal name and description",
  "character_2": "",
  "character_3": "",
  "image_style": "3D animated Pixar-style, bright vivid colors, cinematic lighting, children's animation style",
  "video_style": "3D animated Pixar-like kids video, smooth motion, cinematic lighting",
  "scenes": [
    {{"scene": 1, "time": "0:00-0:08",
      "image_prompt": "scene description, 3D animated Pixar-style, bright vivid colors, cinematic lighting, children's animation style",
      "voice_over": "narration text",
      "caption": "short caption max 8 words"
    }}
  ],
  "youtube": {{
    "title": "...", "hook_line": "...", "description": "...",
    "tags": "...", "alt_title": "...",
    "thumbnail_prompt": "...", "background_music_prompt": "..."
  }}
}}
"""

    MODELS = ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash"]

    for model_name in MODELS:
        print(f"[STORY] Trying: {model_name}...")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            raw = response.text.strip()
            if raw.startswith("```"):
                lines = [l for l in raw.split("\n") if not l.strip().startswith("```")]
                raw = "\n".join(lines).strip()
            return json.loads(raw)

        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"[STORY] ✗ Quota exceeded for {model_name} — trying next...")
                time.sleep(5)
            else:
                print(f"[STORY] ✗ Error: {e}")
            continue

    print("[STORY] ✗ All Gemini models failed. Switch to local in config.py")
    sys.exit(1)


# ════════════════════════════════════════════════════════════
# SECTION 5 — MAIN ENTRY POINT
# ════════════════════════════════════════════════════════════

def generate_story(theme: str) -> dict:
    """
    Main function — routes to local or online based on config
    """
    if USE_LOCAL_LLM:
        print("[STORY] Mode: LOCAL (Phi-2 offline)")
        return generate_with_phi2(theme)
    else:
        print("[STORY] Mode: ONLINE (Gemini API)")
        return generate_with_gemini(theme)


def save_story(story_data: dict):
    """Save story JSON to file"""
    os.makedirs(os.path.dirname(STORY_JSON), exist_ok=True)
    with open(STORY_JSON, "w", encoding="utf-8") as f:
        json.dump(story_data, f, indent=2, ensure_ascii=False)
    print(f"[STORY] ✓ Saved: {STORY_JSON}")


def load_story() -> dict:
    """Load existing story JSON"""
    if not os.path.exists(STORY_JSON):
        print(f"[STORY] ✗ story.json not found. Run Step 1 first.")
        sys.exit(1)
    with open(STORY_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


# ─── Run directly ────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  STEP 1 — STORY GENERATOR")
    print(f"  Mode: {'LOCAL Phi-2' if USE_LOCAL_LLM else 'Gemini API'}")
    print("=" * 50)

    theme = input("\nEnter story theme: ").strip()
    if not theme:
        theme = "friendship"
        print(f"[STORY] Using default theme: '{theme}'")

    story = generate_story(theme)
    save_story(story)

    print("\n── Story Preview ──────────────────────")
    print(f"  Title   : {story.get('story_title', 'N/A')}")
    print(f"  Moral   : {story.get('story_moral', 'N/A')}")
    print(f"  Char 1  : {story.get('character_1', 'N/A')}")
    print(f"  Scenes  : {len(story.get('scenes', []))}")
    print("─" * 40)
    print("[STORY] ✓ Done! Run generate_images.py next.")
