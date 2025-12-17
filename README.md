# YouTube Study Notes Generator

Convert YouTube videos into structured, consultant-optimized study notes using AI.

---

## Features

- **Two workflow options** — API-based workflow (`ytnotes`) or Cursor workflow (`ytcursor`) with built-in LLM
- **Batch processing** — Download transcripts for multiple videos and process them all at once (Cursor workflow)
- **Multi-provider support** — Choose between Google Gemini, Groq, OpenRouter, or Z.AI (API workflow)
- **Easy provider configuration** — Add new providers via `providers.py` without code changes
- **Dual subtitle download** — Uses yt-dlp (primary) with youtube-transcript-api fallback for reliable subtitle fetching
- **SRT + TXT formats** — Saves both timestamped SRT files and plain text transcripts
- **YouTube chapters integration** — Uses built-in video chapters as key moments when available
- **Multiple prompt templates** — Choose from different note formats via CLI or interactive menu
- **Menu navigation** — Restart option in interactive menus to go back to URL input
- **Smart overwriting** — Re-running on the same video updates the existing note
- **Transcript caching** — Transcripts are saved locally to avoid re-fetching
- **Progress indicator** — Visual feedback during generation
- **Token usage stats** — See context usage and rate limits before selecting a provider
- **Compact filenames** — Uses provider nicknames for shorter output filenames
- **Notion integration** — Automatically publish notes to a Notion database (optional)

---

## Supported AI Providers

| Provider | Model | Context | Free Tier | Best For |
|----------|-------|---------|-----------|----------|
| **Cursor Built-in** | Your choice (Claude, GPT-4, etc.) | 200K+ tokens | ✅ With subscription | IDE integration, no API costs |
| **Google Gemini** | gemini-2.5-flash | 1M tokens | ✅ 15 req/min | Long videos, high quality |
| **Groq** | Llama 3.3 70B | 128K tokens | ✅ 12K TPM limit | Short videos, fast results |
| **OpenRouter** | Amazon Nova 2 Lite | 32K tokens | ✅ Free | General purpose |
| **Z.AI** | GLM-4.6 | 32K tokens | ❌ Paid | Existing subscribers |

> **Tip:** If you have a Cursor subscription, see [Using Cursor's Built-in LLM](#using-cursors-built-in-llm-zero-api-costs) for a zero-API-cost workflow!

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/s13r-io/youtube-studynotes.git
cd youtube-studynotes
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If example exists, or create manually
```

Add your API keys (you only need ONE provider):

```env
# Google Gemini (FREE) — https://aistudio.google.com
GEMINI_API_KEY=your_key_here

# Groq (FREE) — https://console.groq.com
GROQ_API_KEY=your_key_here

# OpenRouter (FREE) — https://openrouter.ai
OPENROUTER_API_KEY=your_key_here

# Z.AI (Paid) — https://z.ai
ZAI_API_KEY=your_key_here

# Notion (Optional) — https://developers.notion.com
NOTION_API_KEY=your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
```

### 5. Run the App
```bash
python app.py
```

Or with a URL directly:
```bash
python app.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Or specify a prompt template:
```bash
python app.py "URL" --prompt study-notes
```

---

## Quick Commands

Shortcut commands are available so you don't need to activate the virtual environment manually.

### `ytnotes` - API-Based Workflow

Uses external APIs (Gemini, Groq, etc.) to generate notes.

**First time setup** (add to `~/.zshrc`):
```bash
alias ytnotes='cd /path/to/project && source venv/bin/activate && python app.py'
source ~/.zshrc
```

**Usage:**
```bash
ytnotes                              # Interactive mode
ytnotes "URL"                        # With URL
ytnotes "URL" --prompt study-notes   # With specific prompt
ytnotes "URL" -p quick-summary       # Short form
```

### `ytcursor` - Cursor Workflow

Uses Cursor's built-in LLM (no API keys needed). Supports batch processing.

**First time setup** (add to `~/.zshrc`):
```bash
alias ytcursor='cd /path/to/project && source venv/bin/activate && python cursor_workflow.py'
source ~/.zshrc
```

**Usage:**
```bash
ytcursor                              # Interactive mode (prompts for URL)
ytcursor "URL"                        # Add video to queue
ytcursor --help                       # Show help message

# Batch processing:
ytcursor "URL1"                       # Add first video
ytcursor "URL2"                       # Add second video
ytcursor "URL3"                       # Add third video
# Then in Cursor: "Complete the task in CURSOR_TASK.md"
# Cursor processes all videos sequentially
```

**See [Using Cursor's Built-in LLM](#using-cursors-built-in-llm-zero-api-costs) for complete documentation.**

---

## Using Cursor's Built-in LLM (Zero API Costs)

**New!** If you have a Cursor subscription, you can generate notes using Cursor's built-in LLMs instead of external APIs. This workflow supports **batch processing** - download transcripts for multiple videos and process them all at once.

### Quick Start with Cursor

**Option 1: Using the alias (recommended)**
```bash
# Add video to queue
ytcursor "https://www.youtube.com/watch?v=VIDEO_ID"

# Then in Cursor Chat/Composer, say:
"Complete the task in CURSOR_TASK.md"
```

**Option 2: Using the script directly**
```bash
# Run the Cursor workflow
./cursor_notes.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Or use Python directly
python cursor_workflow.py "URL"
```

### Batch Processing

The Cursor workflow supports batch processing - download transcripts for multiple videos, then process them all at once:

```bash
# Morning: Download transcripts for multiple videos
ytcursor "https://www.youtube.com/watch?v=VIDEO1"
ytcursor "https://www.youtube.com/watch?v=VIDEO2"
ytcursor "https://www.youtube.com/watch?v=VIDEO3"

# Afternoon: Process all at once
# In Cursor Chat: "Complete the task in CURSOR_TASK.md"
# Cursor processes all videos sequentially until queue is empty
```

**How it works:**
1. Each `ytcursor` command downloads a transcript and adds it to `CURSOR_TASK.md` queue
2. `CURSOR_TASK.md` contains just transcript file paths (one per line)
3. Tell Cursor once: "Complete the task in CURSOR_TASK.md"
4. Cursor processes all videos sequentially using `prompts/youtube-summary.md`
5. Each completed video is automatically removed from the queue
6. Process continues until queue is empty

### Benefits
- ✅ **No API keys required** - Uses your Cursor subscription
- ✅ **Choose your model** - Claude 3.5 Sonnet, GPT-4, Opus, etc.
- ✅ **Batch processing** - Process multiple videos with one command
- ✅ **Interactive refinement** - Edit and improve in real-time
- ✅ **IDE integration** - Work directly in Cursor
- ✅ **Automatic Notion publishing** - If configured, publishes after generation

### Output Format

Cursor workflow uses `youtube-summary.md` template and saves files as:
```
YouTubeNotes/{video_id}_summary_cursor.md
```

### Full Documentation
- **[CURSOR_WORKFLOW_GUIDE.md](CURSOR_WORKFLOW_GUIDE.md)** - Complete Cursor workflow guide
- **[BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md)** - Batch processing details
- **[CURSOR_QUICK_REF.md](CURSOR_QUICK_REF.md)** - Quick reference card

---

## Usage

### Interactive Mode
```bash
python app.py
```
You'll be prompted for a YouTube URL, then shown prompt and provider options.

### Direct URL Mode
```bash
python app.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### With Specific Prompt
```bash
python app.py "URL" --prompt study-notes      # Use study-notes template
python app.py --prompt quick-summary "URL"    # Argument order is flexible
python app.py -p study-notes "URL"            # Short form
```

### Prompt Selection
```
============================================================
  📝 Select Note Format
============================================================

  1. study-notes [DEFAULT]
     You are a Study-Note Generator creating notes for a profes

  2. quick-summary
     Create a concise bullet-point summary of the video

Options:
  [1-2]: Select option
  [r]: Restart from beginning

Enter choice (1-2) or press Enter for default [1]: 
```

### Provider Selection
```
============================================================
  🤖 Select AI Provider
============================================================

  📊 Transcript: ~15,000 words (~19,500 tokens)
------------------------------------------------------------

  1. Google Gemini 2.5 Flash [FREE] ⭐ Recommended
     Context: 1M tokens | ✅ Usage: 1.9%

  2. Groq (Llama 3.3 70B) [FREE]
     Context: 128K tokens | ⚠️ Exceeds 12K TPM rate limit

  3. OpenRouter (Amazon Nova 2 Lite) [FREE]
     Context: 32K tokens | ✅ Usage: 60.9%

  4. Z.AI GLM-4.6 [PAID]
     Context: 32K tokens | ✅ Usage: 60.9%

Options:
  [1-4]: Select option
  [r]: Restart from beginning

Enter choice (1-4): 1
```

> **Note:** Groq's free tier has a 12K tokens-per-minute (TPM) limit. For longer transcripts, use Gemini instead.

### Find Your Notes
Generated notes are saved to:
```
YouTubeNotes/<video_id>_<title>_<prompt>_<provider>.md
```

Example: `dC8e2hHXmgM_How_to_AI_Evals_study-notes_gemini2.5Flash.md`

Transcripts are cached in `YouTubeNotes/transcripts/`:
- `<video_id>.txt` — Plain text transcript (used for note generation)
- `<video_id>.srt` — SRT format with timestamps (bonus file for reference)

> **Tip:** If Notion is configured, notes are also automatically published to your Notion database. See [Notion Integration](#notion-integration-optional).

---

## Adding New Providers

One of the key features is the easy-to-extend provider system. Provider configurations are stored in `providers.py`, separate from the main application logic.

### For OpenAI-Compatible APIs

Most modern LLM providers use OpenAI-compatible APIs. To add one, simply add an entry to `providers.py`:

```python
"together": {
    "name": "Together AI (Llama 3.1 70B)",
    "model": "meta-llama/Llama-3.1-70B-Instruct-Turbo",
    "nickname": "together",           # Used in output filenames
    "env_key": "TOGETHER_API_KEY",    # Environment variable name
    "context": "128K tokens",         # Display string
    "context_tokens": 128_000,        # For usage calculations
    "free": False,
    "api_type": "openai",             # Use generic OpenAI handler
    "api_url": "https://api.together.xyz/v1/chat/completions",
},
```

**No code changes required!** The app automatically handles any OpenAI-compatible provider.

### Provider Configuration Fields

| Field | Description |
|-------|-------------|
| `name` | Display name shown in the UI |
| `model` | Model identifier for API calls |
| `nickname` | Short name used in output filenames |
| `env_key` | Environment variable name for API key |
| `context` | Human-readable context window size |
| `context_tokens` | Context window in tokens (for calculations) |
| `free` | Whether the provider offers a free tier |
| `api_type` | One of `"openai"`, `"gemini"`, or `"zai"` |
| `api_url` | API endpoint URL |
| `rate_limit_tpm` | (Optional) Tokens-per-minute rate limit |

### API Types

- **`openai`** — Standard OpenAI-compatible API (Groq, OpenRouter, Together, DeepSeek, Fireworks, etc.)
- **`gemini`** — Google's Gemini API (different request format)
- **`zai`** — Z.AI streaming API (uses SSE streaming)

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

### OpenRouter
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up / Sign in
3. Go to **Keys** → **Create Key**
4. Copy and add to `.env`

---

## Notion Integration (Optional)

Automatically publish your study notes to a Notion database. When configured, notes are saved both locally and to Notion.

### Setting Up Notion

#### 1. Create a Notion Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **+ New integration**
3. Give it a name (e.g., "YouTube Notes")
4. Select the workspace where your database will live
5. Click **Submit** → copy the **Internal Integration Token**
6. Add to `.env`: `NOTION_API_KEY=secret_xxx...`

#### 2. Create a Notion Database

Create a new database in Notion with these properties:

| Property | Type | Description |
|----------|------|-------------|
| **Name** | Title | Page title (auto-populated from notes) |
| **YouTube URL** | URL | Link to the source video |
| **Channel** | Text | Video channel name |
| **Duration** | Text | Video duration |
| **Provider** | Select | AI provider used (Gemini, Groq, etc.) |
| **Prompt** | Select | Prompt template used |
| **Tags** | Multi-select | Auto-generated content tags |
| **Date Added** | Date | When the note was created |

#### 3. Share Database with Integration

1. Open your database in Notion
2. Click **•••** (top-right) → **Connections** → **Connect to** → Select your integration
3. Copy the database ID from the URL:
   ```
   https://notion.so/workspace/DATABASE_ID?v=...
                            ^^^^^^^^^^^^^^^^
   ```
4. Add to `.env`: `NOTION_DATABASE_ID=abc123...`

### What Gets Published

- **Title**: Extracted from the notes (first heading)
- **Tags**: AI-generated tags from the `**Tags:**` line in notes, or auto-generated from metadata
- **Full Content**: Markdown converted to Notion blocks (headings, bullets, numbered lists, bold text, links)
- **Metadata**: YouTube URL, channel, duration, provider, prompt type, date

### Notion Limits Handled

- **100 blocks per request**: Large notes are automatically batched
- **2000 chars per text block**: Long paragraphs are split automatically
- **Rich text formatting**: Bold, links, and markdown links are preserved

---

## Project Structure

```
youtube-studynotes/
├── app.py                    # Main application logic (API workflow)
├── cursor_workflow.py        # Cursor workflow script (batch processing)
├── run.sh                    # Quick run script (used by ytnotes alias)
├── cursor_notes.sh           # Cursor workflow launcher
├── providers.py              # Provider configurations (add new providers here!)
├── publish_to_notion.py      # Notion publishing script
├── remove_from_queue.py      # Queue management helper
├── publish_latest.sh          # Publish latest summary to Notion
├── .cursorrules              # Cursor AI workflow instructions
├── CURSOR_TASK.md            # Queue file for batch processing (transcript paths)
├── prompts/                  # Prompt templates folder
│   ├── study-notes.md        # Default study notes format (API workflow)
│   └── youtube-summary.md    # Summary format (Cursor workflow)
├── requirements.txt          # Python dependencies
├── .env                      # API keys (create this, not committed)
├── .gitignore                # Git ignore rules
├── README.md                 # This guide
├── CURSOR_WORKFLOW_GUIDE.md  # Complete Cursor workflow documentation
├── BATCH_PROCESSING_GUIDE.md # Batch processing guide
└── YouTubeNotes/             # Generated notes output
    ├── transcripts/          # Cached transcripts
    │   ├── <video_id>.txt    # Plain text transcript
    │   └── <video_id>.srt    # SRT format with timestamps
    ├── <video_id>_<title>_<prompt>_<provider>.md  # API workflow output
    └── <video_id>_summary_cursor.md              # Cursor workflow output
```

---

## Customizing Note Format

### Using Different Prompts

The app supports multiple prompt templates stored in the `prompts/` folder. Each `.md` file is a separate template.

```bash
# Use default (study-notes)
python app.py "URL"

# Use a specific prompt
python app.py "URL" --prompt quick-summary

# Interactive selection
python app.py "URL"  # Shows menu if multiple prompts exist
```

### Creating Custom Prompts

1. Create a new `.md` file in the `prompts/` folder
2. The first line becomes the description shown in the selection menu
3. Write your system prompt instructions

Example: `prompts/quick-summary.md`
```markdown
Create a concise bullet-point summary of the video content.

## Instructions
- Summarize the main points in 5-10 bullet points
- Keep each point under 2 sentences
- Focus on actionable takeaways
...
```

### Default Template (study-notes.md)

The default `study-notes.md` template creates comprehensive study notes with:
1. **Title & Discovery Tags** — Clear title with hashtags
2. **The Hook** — Why this topic matters
3. **Core Concept** — The WHAT and WHY
4. **How It Works** — The mechanics and HOW
5. **Three Perspectives** — Real-world, technical, and pitfalls
6. **Practical Cheat Sheet** — Quick reference bullets
7. **Key Terms Glossary** — Important definitions
8. **Memory Anchors** — Summary, analogy, flashcards, deeper questions
9. **Key Moments** — Clickable timestamps (uses YouTube chapters when available, otherwise AI-generated)

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| **No API keys configured** | Add at least one key to `.env` |
| **Transcripts are disabled** | Video owner turned off captions, try another video |
| **No transcript found** | Video has no captions, try another video |
| **Groq 413: Exceeds TPM limit** | Transcript too large for Groq's 12K TPM free tier; use Gemini instead |
| **Response truncated** | Rare with Gemini's 1M context; try Gemini for long videos |
| **Timeout** | Long videos take 1-3 min; be patient or try Groq (faster) |
| **Module not found** | Ensure virtual environment is activated: `source venv/bin/activate` |
| **Permission denied** | Check file permissions in YouTubeNotes folder |
| **Notion publish failed** | Check `NOTION_API_KEY` and `NOTION_DATABASE_ID` in `.env`; ensure database is shared with integration |
| **Notion validation error** | Ensure database has all required properties (Name, YouTube URL, Channel, etc.) |

---

## Technical Details

- **Transcription**: `yt-dlp` (primary) + `youtube-transcript-api` (fallback) — Downloads subtitles in SRT format, extracts plain text, saves both formats
- **Video metadata**: `yt-dlp` — Title, channel, duration, and chapters extraction
- **API calls**: `requests` — Direct REST calls, no SDK dependencies
- **Notion publishing**: `notion-client` — Official Notion SDK for Python
- **Configuration**: `python-dotenv` — Loads `.env` file
- **Python**: 3.8+ recommended

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

Personal use. API usage subject to respective provider terms.
