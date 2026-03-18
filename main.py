# ============================================================
# main.py
# Master control menu — run all steps from here
# StoryGenerator — Free Stack (Gemini + Pollinations + Edge-TTS)
# ============================================================

import os
import sys

def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║       STORY FACTORY — FREE STACK             ║
║  Gemini + Pollinations.ai + Edge-TTS         ║
╠══════════════════════════════════════════════╣
║  Stack:                                      ║
║  • Story   → Gemini 1.5 Flash (Free API)     ║
║  • Images  → Pollinations.ai  (100% Free)    ║
║  • Voice   → Edge-TTS         (Free)         ║
║  • Video   → MoviePy          (Local)        ║
╚══════════════════════════════════════════════╝
    """)


def check_config():
    """Warn user if API key is not set"""
    try:
        from config import GEMINI_API_KEY
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("⚠  WARNING: Gemini API key not set in config.py")
            print("   Get free key from: https://aistudio.google.com")
            print("   Then edit config.py → GEMINI_API_KEY = 'your_key'\n")
    except ImportError:
        print("✗ config.py not found in current directory")
        sys.exit(1)


def step_1_generate_story():
    print("\n── STEP 1: Generate Story ──────────────────")
    from generate_story import generate_story, save_story
    theme = input("Enter theme (e.g. friendship, bravery, sharing): ").strip()
    if not theme:
        theme = "friendship and helping others"
    story = generate_story(theme)
    save_story(story)
    print(f"\n✓ Story ready: {story['story_title']}")
    input("\nPress Enter to return to menu...")


def step_2_generate_images():
    print("\n── STEP 2: Generate Images ─────────────────")
    from generate_images import generate_all_images
    generate_all_images()
    input("\nPress Enter to return to menu...")


def step_3_generate_audio():
    print("\n── STEP 3: Generate Audio ──────────────────")
    from generate_audio import generate_all_audio
    generate_all_audio()
    input("\nPress Enter to return to menu...")


def step_4_build_video():
    print("\n── STEP 4: Build Video ─────────────────────")
    from build_video import build_video
    build_video()
    input("\nPress Enter to return to menu...")


def run_all_steps():
    print("\n── RUN ALL STEPS ───────────────────────────")
    print("This will run Steps 1 → 2 → 3 → 4 in sequence.")
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != "y":
        return

    from generate_story import generate_story, save_story
    from generate_images import generate_all_images
    from generate_audio  import generate_all_audio
    from build_video     import build_video

    theme = input("\nEnter theme: ").strip()
    if not theme:
        theme = "friendship and helping others"

    print("\n[1/4] Generating story...")
    story = generate_story(theme)
    save_story(story)

    print("\n[2/4] Generating images...")
    generate_all_images()

    print("\n[3/4] Generating audio...")
    generate_all_audio()

    print("\n[4/4] Building video...")
    build_video()

    print("\n✓ All steps complete! Check your video folder.")
    input("\nPress Enter to return to menu...")


def show_story_info():
    """Show current story.json summary"""
    try:
        from generate_story import load_story
        story = load_story()
        print(f"\n── Current Story ────────────────────────────")
        print(f"  Title    : {story.get('story_title', 'N/A')}")
        print(f"  Moral    : {story.get('story_moral', 'N/A')}")
        print(f"  Char 1   : {story.get('character_1', 'N/A')}")
        print(f"  Scenes   : {len(story.get('scenes', []))}")
        yt = story.get("youtube", {})
        print(f"  YT Title : {yt.get('title', 'N/A')}")
        print(f"  Tags     : {yt.get('tags', 'N/A')}")
    except SystemExit:
        print("  No story generated yet. Run Step 1 first.")
    input("\nPress Enter to return to menu...")


# ─── Main Menu Loop ──────────────────────────────────────────
if __name__ == "__main__":

    check_config()
    print_banner()

    while True:
        print("─" * 48)
        print("  MENU")
        print("─" * 48)
        print("  1  Generate Story       (Gemini API)")
        print("  2  Generate Images      (Pollinations.ai)")
        print("  3  Generate Audio       (Edge-TTS)")
        print("  4  Build Video          (MoviePy)")
        print("  ─────────────────────────────────────")
        print("  5  Run All Steps        (1 → 2 → 3 → 4)")
        print("  6  Show Current Story Info")
        print("  0  Exit")
        print("─" * 48)

        choice = input("Select option: ").strip()

        if   choice == "1": step_1_generate_story()
        elif choice == "2": step_2_generate_images()
        elif choice == "3": step_3_generate_audio()
        elif choice == "4": step_4_build_video()
        elif choice == "5": run_all_steps()
        elif choice == "6": show_story_info()
        elif choice == "0":
            print("\nGoodbye! Happy Storytelling 🎭✨")
            break
        else:
            print("  Invalid option — try again")
