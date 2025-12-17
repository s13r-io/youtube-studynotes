# 🎯 Cursor Workflow - Quick Reference

## One-Liner

```bash
./cursor_notes.sh "YOUTUBE_URL" && echo "Now tell Cursor: 'Complete the task in CURSOR_TASK.md'"
```

---

## Step-by-Step

### 1️⃣ Download Transcript
```bash
./cursor_notes.sh "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2️⃣ Tell Cursor (in Chat/Composer)
```
Complete the task in CURSOR_TASK.md
```

### 3️⃣ Done! ✅
Notes saved to `YouTubeNotes/`

---

## Alternative Commands for Cursor

### Simple
```
Complete CURSOR_TASK.md
```

### Explicit
```
Read the transcript in YouTubeNotes/transcripts/ and generate 
study notes using prompts/study-notes.md template
```

### Custom Template
```
Complete CURSOR_TASK.md but use prompts/quick-summary.md
```

---

## Files Created

```
CURSOR_TASK.md                           # Task instructions (temporary)
YouTubeNotes/transcripts/{video_id}.txt  # Transcript
YouTubeNotes/{video_id}_title_study-notes_cursor.md  # Output
```

---

## What Uses Cursor's LLM?

- ❌ Downloading transcript - **No LLM** (just API call)
- ✅ Generating study notes - **Cursor's LLM** (your subscription)
- ❌ Saving files - **No LLM** (just file I/O)

**Result:** Only the "smart" work uses your Cursor subscription - no external API costs!

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: cursor_notes.sh` | Run from project directory: `cd ~/Movies/YouTube` |
| `Module not found` | Activate venv: `source venv/bin/activate` |
| Script not executable | Run: `chmod +x cursor_notes.sh` |
| Cursor doesn't understand | Reload `.cursorrules`: Restart Cursor |

---

## Model Selection

Before running the workflow, choose your model in Cursor:
- **Claude 3.5 Sonnet** - Best quality (recommended)
- **GPT-4** - Fast and reliable
- **Claude Opus** - Most powerful

Settings → Models → Select your preferred model

---

## Cost Comparison

### With External APIs
- Gemini: Free tier (15 req/min)
- Groq: Free tier (12K TPM limit)
- OpenRouter: Pay per token
- Anthropic: ~$3 per million tokens

### With Cursor
- **$0 additional** (uses existing subscription)
- No token counting
- No rate limits (within Cursor's fair use)
- Can use premium models (Opus, GPT-4)

---

## Tips

1. **Batch Processing**: Run script multiple times, process in Cursor sequentially
2. **Custom Prompts**: Create your own in `prompts/` folder
3. **Interactive Editing**: Refine notes in real-time with Cursor
4. **Version Control**: Cursor's AI helps with git commits too!

---

## Full Docs

📖 [CURSOR_WORKFLOW_GUIDE.md](CURSOR_WORKFLOW_GUIDE.md) - Complete guide
📖 [README.md](README.md) - Project overview

