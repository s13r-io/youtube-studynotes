# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Study Notes Generator — converts YouTube videos into structured, AI-powered study notes using multiple LLM providers (Gemini, Groq, OpenRouter, Z.AI). Supports both direct API calls and Cursor IDE batch processing.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then add at least one API key
```

## Running

```bash
# Unified entry point (recommended)
python main.py                            # interactive: prompts for URL, then workflow
python main.py "https://youtube.com/..."  # URL provided, shows workflow selection menu
python main.py -q "URL"                   # quick mode: auto API + youtube-summary prompt + Notion

# Shell wrapper (same behavior, activates venv)
./run.sh
./run.sh "URL"
./run.sh -q "URL"

# Direct workflow access (backward compat)
python app.py "URL" --prompt study-notes
python cursor_workflow.py "URL"
```

## Testing

```bash
python test_chunking.py   # unit tests for TPM-based transcript chunking logic
```

No formal test framework or linting tools are configured.

## Architecture

### Two Workflows

1. **API Workflow** (`app.py`) — select a prompt template and AI provider, generates a `.md` file in `YouTubeNotes/`.
2. **Cursor Workflow** (`cursor_workflow.py`) — queues a transcript path to `CURSOR_TASK.md`; user then tells Cursor IDE: *"Complete the task in CURSOR_TASK.md"*. Cursor processes all queued videos sequentially using `.cursorrules` instructions and optionally auto-publishes to Notion.

### Code Organization

| File | Role |
|------|------|
| `main.py` | Unified entry point — downloads transcript, routes to API or Cursor workflow |
| `app.py` | Full API workflow implementation (~1500 lines) |
| `cursor_workflow.py` | Cursor workflow — queues transcripts to `CURSOR_TASK.md` |
| `transcript_utils.py` | **Shared** transcript download, caching, metadata extraction, token estimation |
| `providers.py` | AI provider configurations (model, context window, API type, rate limits) |
| `publish_to_notion.py` | Notion API integration |
| `remove_from_queue.py` | Removes processed items from `CURSOR_TASK.md` |

### Key Patterns

- **Transcript download is centralized** in `transcript_utils.py` — dual fallback: yt-dlp (primary) → youtube-transcript-api. Both `main.py` and `cursor_workflow.py` call these shared utils; never duplicate this logic.
- **Providers are data, not code** — `providers.py` exports a `PROVIDERS` dict. OpenAI-compatible APIs require no code changes, just a new entry. Custom APIs (non-OpenAI) need a handler added in `app.py`.
- **Prompts are files** — any `.md` file added to `prompts/` becomes selectable automatically.
- **Output caching** — transcripts cached in `YouTubeNotes/transcripts/{video_id}.txt` and `.srt`. Always check cache before downloading.
- **Quick mode** (`-q`) — skips all interactive menus; uses first available provider + `youtube-summary` prompt + auto-publishes to Notion if configured.

### Provider API Types

Each provider entry in `providers.py` has an `api_type` field:
- `"openai"` — standard OpenAI-compatible REST (Groq, OpenRouter)
- `"gemini"` — Google Gemini SDK
- `"zai"` — Z.AI custom API
- `"cursor"` — handled by Cursor IDE itself (not via API calls)

### Output Files

Generated notes are saved as `YouTubeNotes/{video_id}_{prompt_nickname}_{provider_nickname}.md` with metadata headers (title, channel, duration, URL, timestamp).
