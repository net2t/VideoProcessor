# 🎬 VideoProcessor

Automatic post-processor for **Bright Little Stories** videos with logo overlay, trimming, and custom endscreen.

Works **two ways** — same script, same settings:

| Mode | How to run | When to use |
|------|-----------|-------------|
| ☁️ **Cloud** | GitHub Actions (automatic) | No PC needed — runs on schedule |
| 💻 **Local** | `python process.py` on your PC | Manual runs, testing |

---

## What It Does to Each Video

1. **Logo overlay** — Places logo on top-left corner to cover the MagicLight.AI watermark
2. **Trim end** — Cuts the last N seconds (default: 4) to remove the MagicLight outro
3. **Add endscreen** — Appends your custom endscreen video (auto-detected duration)
4. **Crossfade** — Smooth transition between main video and endscreen
5. **Upload to Drive** — Uploads processed video to Google Drive folder
6. **Local copy** — Saves processed video locally before upload
7. **Update Sheet** — Sets Status → `Processed` and writes Drive URL to column O (cloud mode)

---

## Project Structure

```
VideoProcessor/
├── process.py                   ← Main script (cloud + local)
├── assets/
│   ├── logo.png                 ← Your watermark cover logo
│   └── endscreen.mp4           ← Your custom endscreen video
├── .env                         ← Your config (never commit this)
├── .env.example                 ← Template — copy to .env
├── auth.json                   ← OAuth credentials (never commit this)
├── requirements.txt             ← Python packages
├── .gitignore
├── downloads/                   ← Default local scan folder (auto-created)
└── .github/
    └── workflows/
        └── process.yml          ← GitHub Actions with manual options
```

---

## Setup — Step by Step

### Step 1 — Clone or Create the Repo

```bash
# Option A: Clone this repo
git clone https://github.com/net2t/VideoProcessor.git
cd VideoProcessor

# Option B: Create new repo on GitHub, then clone it
```

### Step 2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Install FFmpeg (local PC only)

FFmpeg is **pre-installed** on GitHub Actions runners automatically.

For your local PC (Windows):
```bash
# Option 1 — easiest via pip
pip install imageio-ffmpeg

# Option 2 — install system-wide
# Download from https://ffmpeg.org/download.html
# Extract to C:\ffmpeg\
# Add C:\ffmpeg\bin to your Windows PATH
```

### Step 4 — Create OAuth Credentials (Recommended)

OAuth authentication uses your personal Google Drive quota (no storage limits).

1. Go to https://console.cloud.google.com/
2. Select your project
3. **APIs & Services → Library** — enable:
   - ✅ Google Drive API
   - ✅ Google Sheets API
4. **APIs & Services → Credentials → + Create Credentials → OAuth 2.0 Client ID**
   - Application type: Desktop app
   - Name: `video-processor`
   - Click Create
5. Download the JSON file and save it as `auth.json` in this project folder
6. **IMPORTANT**: Add `http://localhost:8080/` to Authorized redirect URIs

### Step 5 — Share Sheet and Drive

Open `auth.json` and find `"client_email"` — copy that email address.

- Open your **Google Sheet** → Share → paste email → Editor → Send
- Open your **Drive folder** → Right-click → Share → paste email → Editor → Done

### Step 6 — Configure .env

```bash
# Copy the template
copy .env.example .env     # Windows
cp .env.example .env       # Mac/Linux

# Edit .env and fill in your values
```

### Step 7 — Add Assets

Create an `assets/` folder and add:
- `assets/logo.png` — Your logo to cover the watermark (300px width recommended)
- `assets/endscreen.mp4` — Your endscreen video (5-10 seconds)

### Step 8 — Add column O to your Sheet

Open your Google Sheet → click cell O1 → type `Processed Video URL`

---

## Configuration (.env)

```ini
# Google Sheet ID (from Sheet URL)
SPREADSHEET_ID=your_sheet_id_here

# Google Drive Folder ID (from folder URL)
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here

# Video Processing
TRIM_SECONDS=4

# Logo Settings
LOGO_PATH=assets/logo.png
LOGO_X=7
LOGO_Y=5
LOGO_WIDTH=300
LOGO_OPACITY=1.0

# Endscreen Settings
ENDSCREEN_ENABLED=true
ENDSCREEN_VIDEO=assets/endscreen.mp4
ENDSCREEN_DURATION=auto

# Local Mode Settings
INPUT_FOLDER=E:\Pythons\VideoProcessor\downloads
OUTPUT_FOLDER=E:\Pythons\VideoProcessor\Done
```

---

## Running Locally (PC)

```bash
# Local mode (scans INPUT_FOLDER)
python process.py --mode local

# Cloud mode (reads from Sheet + Drive)
python process.py --mode cloud

# Auto-detect mode (default)
python process.py

# Dry run (preview only)
python process.py --dry-run

# Limit number of videos
python process.py --max 3
```

---

## GitHub Actions (Cloud)

### Manual Run Options

The workflow includes manual inputs for:
- Logo X/Y position
- Logo width
- Trim seconds
- Endscreen enable/disable
- Endscreen duration
- Dry run option

### Setup GitHub Secrets

Go to: **GitHub → Your Repo → Settings → Secrets and variables → Actions**

Add these secrets:
- `SPREADSHEET_ID` — Your Google Sheet ID
- `GOOGLE_CREDENTIALS` — Full contents of `auth.json`

### Schedule

Default: Daily at 1:00 PM Pakistan time (08:00 UTC).

---

## Features

### ✨ **Smart Authentication**
- OAuth with personal Google Account (recommended)
- No storage quota limits
- Automatic token refresh

### 🎨 **Logo Overlay**
- Customizable position and size
- Opacity control
- Covers MagicLight watermark completely

### ✂️ **Smart Trimming**
- Removes MagicLight outro
- Configurable duration
- Preserves main content

### 🎬 **Dynamic Endscreen**
- Auto-detects video duration
- Supports any length (5s, 7s, etc.)
- Smooth crossfade transition

### 📁 **Dual Output**
- Local copy for backup
- Google Drive upload for sharing
- Maintains folder structure

---

## Troubleshooting

**OAuth redirect error**
→ Add `http://localhost:8080/` to Authorized redirect URIs in Google Cloud Console

**No credentials found**
→ Place `auth.json` in project folder

**Logo not found**
→ Check `LOGO_PATH` in .env (should be `assets/logo.png`)

**Endscreen not found**
→ Check `ENDSCREEN_VIDEO` in .env (should be `assets/endscreen.mp4`)

**No videos processed**
→ Local mode: Add videos to INPUT_FOLDER
→ Cloud mode: Set Sheet rows to Status="Done"

---

## Author

**Nadeem** · github.com/net2t · Bright Little Stories
