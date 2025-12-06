# YouTube Study Notes Generator

Convert YouTube videos into structured, consultant-optimized study notes using AI.

---

## Features

- **Multi-provider support** — Choose between Google Gemini, Groq, or Z.AI
- **Automatic transcription** — Fetches YouTube's auto-generated captions
- **Custom note format** — Uses your `gpt-inst.md` template for consistent output
- **Smart overwriting** — Re-running on the same video updates the existing note
- **Progress indicator** — Visual feedback during generation

---

## Supported AI Providers

| Provider | Model | Context | Free Tier | Best For |
|----------|-------|---------|-----------|----------|
| **Google Gemini** | gemini-2.5-flash | 1M tokens | ✅ 15 req/min | Long videos, high quality |
| **Groq** | Llama 3.3 70B | 128K tokens | ✅ ~30 req/min | Fast results |
| **Z.AI** | GLM-4.6 | 32K tokens | ❌ Paid | Existing subscribers |

---

## Quick Start

### 1. Activate Environment
```bash
cd /Users/saurabh.karmakar/Movies/YouTube
source venv/bin/activate
```

### 2. Run the App
```bash
python app.py
```

Or with a URL directly:
```bash
python app.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 3. Select Provider & Wait
```
==================================================
  🤖 Select AI Provider
==================================================

  1. Google Gemini 2.5 Flash [FREE]
     Context: 1M tokens | Status: ✅

  2. Groq (Llama 3.3 70B) [FREE]
     Context: 128K tokens | Status: ✅

  3. Z.AI GLM-4.6 [PAID]
     Context: 32K tokens | Status: ✅

Enter choice (1-3): 1
```

### 4. Find Your Notes
```
YouTubeNotes/2025-12-06_Video_Title.md
```

---

## One-Liner

```bash
cd /Users/saurabh.karmakar/Movies/YouTube && source venv/bin/activate && python app.py "YOUTUBE_URL"
```

---

## Setup (First Time Only)

### Install Dependencies
```bash
cd /Users/saurabh.karmakar/Movies/YouTube
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure API Keys

Create a `.env` file with your API keys:

```bash
nano .env
```

Add the keys you have:

```env
# Google Gemini (FREE) — https://aistudio.google.com
GEMINI_API_KEY=your_key_here

# Groq (FREE) — https://console.groq.com
GROQ_API_KEY=your_key_here

# Z.AI (Paid) — https://z.ai
ZAI_API_KEY=your_key_here
```

**Note:** You only need ONE provider configured.

---

## Getting Free API Keys

### Google Gemini (Recommended)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with Google
3. Click **Get API Key** → **Create API key**
4. Copy and add to `.env`

### Groq
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Sign in
3. Go to **API Keys** → **Create API Key**
4. Copy and add to `.env`

---

## File Structure

```
YouTube/
├── app.py              # Main application
├── gpt-inst.md         # Note format template
├── requirements.txt    # Python dependencies
├── .env                # API keys (private)
├── venv/               # Virtual environment
├── README.md           # This guide
└── YouTubeNotes/       # Generated notes
    └── 2025-12-06_Video_Title.md
```

---

## Customizing Note Format

Edit `gpt-inst.md` to change how notes are structured. The AI follows this template when generating notes.

Current template sections:
1. Title & Discovery Tags
2. The Hook
3. Core Concept
4. How It Works
5. Three Scenarios
6. Consultant's Cheat Sheet
7. Key Terms Glossary
8. Memory Anchors

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| **No API keys configured** | Add at least one key to `.env` |
| **Transcripts are disabled** | Video owner turned off captions, try another video |
| **No transcript found** | Video has no captions, try another video |
| **Response truncated** | Rare with Gemini's 1M context; try Gemini for long videos |
| **Timeout** | Long videos take 1-3 min; be patient or try Groq (faster) |
| **Module not found** | Run `source venv/bin/activate` first |

---

## Technical Details

- **Transcription**: `youtube-transcript-api` (fetches YouTube's existing captions)
- **Video metadata**: `yt-dlp` (title extraction)
- **API calls**: `requests` (direct REST calls, no SDK dependencies)
- **Configuration**: `python-dotenv` (loads `.env` file)

---

## License

Personal use. API usage subject to respective provider terms.
