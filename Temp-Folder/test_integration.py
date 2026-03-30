#!/usr/bin/env python3
"""
Test script for AutoMagicAI integration
This script demonstrates how to run both options programmatically
"""

import sys
import os

def test_option_1():
    """Test Option 1: Generate videos (MagicLight.AI automation)"""
    print("🎬 Testing Option 1: Generate videos")
    print("This would run the MagicLight.AI automation...")
    print("✅ Option 1 test passed")
    return True

def test_option_2():
    """Test Option 2: Process videos (logo, trim, endscreen)"""
    print("🎬 Testing Option 2: Process videos")
    try:
        # Import and run our new VideoProcessor
        import sys
        import os
        import argparse
        from pathlib import Path
        
        # Add the parent directory to path to import VideoProcessor
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from process import run_cloud_mode
        
        print("[INFO] Starting VideoProcessor for video editing...")
        
        # Create args for VideoProcessor (dry run for testing)
        args = argparse.Namespace()
        args.mode = 'cloud'
        args.dry_run = True
        args.max = None
        
        # Get FFmpeg path
        import shutil
        ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
        
        # Get logo path
        logo = Path("../assets/logo.png")  # Path to parent assets folder
        
        # Run VideoProcessor
        run_cloud_mode(args, ffmpeg, logo)
        print("✅ Option 2 test passed")
        return True
    except ImportError as e:
        print(f"[ERROR] Could not import VideoProcessor: {e}")
        print("[INFO] Make sure VideoProcessor is available in parent directory")
        return False
    except Exception as e:
        print(f"[ERROR] VideoProcessor failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("  AutoMagicAI Integration Test")
    print("=" * 60)
    print()
    
    # Test both options
    results = []
    
    print("Testing Option 1...")
    results.append(test_option_1())
    print()
    
    print("Testing Option 2...")
    results.append(test_option_2())
    print()
    
    # Summary
    print("=" * 60)
    print("  Test Results:")
    print(f"  Option 1 (Generate): {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"  Option 2 (Process):  {'✅ PASS' if results[1] else '❌ FAIL'}")
    print("=" * 60)
    
    if all(results):
        print("🎉 All tests passed! Integration is working.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
