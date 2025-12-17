# 🎯 Using Cursor's Built-in LLM for Study Notes

This guide explains how to generate YouTube study notes using **Cursor's built-in LLM** instead of external API keys.

---

## 🌟 Why Use This Workflow?

- ✅ **No external API costs** - Uses your Cursor subscription
- ✅ **Uses your preferred Cursor model** - Claude, GPT-4, etc.
- ✅ **Integrated in your IDE** - No context switching
- ✅ **Full control** - Edit and refine in real-time

---

## 🚀 Quick Start

### Method 1: Automatic (Recommended)

```bash
# Run from project directory
./cursor_notes.sh "https://www.youtube.com/watch?v=VIDEO_ID"
```

This will:
1. Download the video transcript
2. Create a task file (`CURSOR_TASK.md`)
3. Open the task file in Cursor
4. You then tell Cursor Chat: "Complete the task in CURSOR_TASK.md"

### Method 2: Manual Steps

```bash
# Step 1: Download transcript
python cursor_workflow.py "YOUTUBE_URL"

# Step 2: Open CURSOR_TASK.md in Cursor

# Step 3: In Cursor Chat/Composer, say:
"Complete the task described in CURSOR_TASK.md"
```

---

## 📋 How It Works

### 1. Transcript Download (No LLM Required)

The Python script handles the "dumb" work:
- Extracts video ID from URL
- Downloads transcript using `youtube-transcript-api`
- Saves transcript to `YouTubeNotes/transcripts/`
- Creates a task instruction file

### 2. Cursor AI Processing (Uses Built-in LLM)

Cursor's AI then:
- Reads the transcript file
- Applies your prompt template (`prompts/study-notes.md`)
- Generates comprehensive study notes
- Saves output to `YouTubeNotes/`
- **Automatically publishes to Notion** (if configured) - no manual step needed!

**Key Benefit:** This uses the same LLM you're already paying for with Cursor!

---

## 🎨 What Gets Generated

The workflow creates two files:

1. **CURSOR_TASK.md** - Instructions for Cursor AI
   - Contains video metadata
   - File paths for transcript and output
   - Clear instructions for processing

2. **YouTubeNotes/transcripts/{video_id}.txt** - The video transcript
   - Plain text format
   - Ready for processing

3. **YouTubeNotes/{video_id}_title_study-notes_cursor.md** - Generated study notes
   - Comprehensive notes following your prompt template
   - Automatically published to Notion (if configured)

---

## 📤 Notion Publishing (Automatic)

**Good news!** If you have Notion configured (see README.md for setup), Cursor will automatically publish your notes to Notion after generating them. No manual step needed!

The workflow:
1. Cursor generates and saves notes locally
2. Cursor automatically runs the publish script
3. Notes appear in your Notion database with all metadata

**If Notion isn't configured:** Notes are still saved locally - you just won't get the Notion page. You can manually publish later using:
```bash
./publish_latest.sh
```

---

## 💬 Using Cursor Chat/Composer

### Simple Prompt

```
Complete the task in CURSOR_TASK.md
```

### Detailed Prompt (if you prefer)

```
Read the transcript from YouTubeNotes/transcripts/{video_id}.txt 
and generate comprehensive study notes following the format in 
prompts/study-notes.md. Save the output to YouTubeNotes/ with 
an appropriate filename.
```

### Custom Prompt Template

```
Use the quick-summary prompt instead: Complete the task in 
CURSOR_TASK.md but use prompts/quick-summary.md as the template
```

---

## 🎯 .cursorrules Integration

The `.cursorrules` file in this project teaches Cursor AI how to:
- Recognize study note generation tasks
- Read transcript files
- Apply prompt templates
- Format output correctly
- Save files with proper naming convention

**This means:** Cursor automatically understands your workflow context!

---

## 🔄 Comparison: Old vs New Workflow

### Old Workflow (External APIs)
```
URL → Python fetches transcript → Calls Gemini/Groq API → Saves notes
```
**Requires:** API keys, credits/billing

### New Workflow (Cursor)
```
URL → Python fetches transcript → Cursor AI processes → Saves notes
```
**Requires:** Cursor subscription (which you already have!)

---

## 💡 Tips & Tricks

### 1. Choose Your Model

In Cursor, you can select which model processes your task:
- Claude 3.5 Sonnet (best quality)
- GPT-4 (fast and capable)
- Claude Opus (most powerful)

Just select your preferred model in Cursor's settings before processing.

### 2. Interactive Refinement

Since Cursor is interactive, you can:
- Ask for clarifications mid-generation
- Request format adjustments
- Add sections or expand on topics
- Fix any issues in real-time

### 3. Batch Processing

Process multiple videos:
```bash
./cursor_notes.sh "URL1"
# Tell Cursor to complete task

./cursor_notes.sh "URL2"
# Tell Cursor to complete task
```

### 4. Custom Prompts

Want different note styles?
```
Complete CURSOR_TASK.md but use prompts/quick-summary.md instead
```

Or create your own prompt template in `prompts/` folder!

---

## 🛠️ Troubleshooting

### "Module not found" error
```bash
# Ensure virtual environment is activated
source venv/bin/activate
python cursor_workflow.py "URL"
```

### Cursor doesn't understand the task
- Make sure `.cursorrules` file exists in project root
- Restart Cursor to reload rules
- Use more explicit instructions in your prompt

### Transcript download fails
- Check internet connection
- Verify video has captions enabled
- Try the URL in a browser first

### Output not saving
- Check `YouTubeNotes/` folder exists
- Verify file permissions
- Ask Cursor to show you the output path it's using

---

## 📊 Token Usage

**Approximate usage per video:**
- 10-minute video: ~5,000 tokens (transcript) + ~3,000 tokens (output) = **8K tokens**
- 30-minute video: ~15,000 tokens + ~5,000 tokens = **20K tokens**
- 60-minute video: ~30,000 tokens + ~8,000 tokens = **38K tokens**

These are within Cursor's generous context windows and usage limits!

---

## 🎓 Example Session

```bash
$ ./cursor_notes.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

🎬 YouTube Study Notes - Cursor Workflow
============================================================
📹 Video ID: dQw4w9WgXcQ
📊 Fetching video metadata...
📝 Title: How AI Agents Work
👤 Channel: Tech Explained
📥 Downloading transcript...
✅ Transcript downloaded: ~3,500 words

============================================================
✅ READY FOR CURSOR!
============================================================

📄 Task file created: CURSOR_TASK.md
📄 Transcript saved: YouTubeNotes/transcripts/dQw4w9WgXcQ.txt

🎯 NEXT STEPS:
   1. Open CURSOR_TASK.md in Cursor
   2. In Cursor Chat, say:
      'Complete the task in CURSOR_TASK.md'

🚀 Opening task file in Cursor...
```

**Then in Cursor Chat:**
```
You: Complete the task in CURSOR_TASK.md

Cursor: I'll generate study notes from the transcript...
[Processes with built-in LLM]
✅ Notes saved to: YouTubeNotes/dQw4w9WgXcQ_How_AI_Agents_Work_study-notes_cursor.md
```

---

## 🆚 When to Use Each Method

### Use Cursor Workflow When:
- You have an active Cursor subscription
- You want interactive control and refinement
- Token limits aren't a concern
- You prefer working in your IDE

### Use API Workflow (Original) When:
- Automating bulk processing
- Running on servers/CI/CD
- Need programmatic access
- Want specific model guarantees (e.g., always Gemini 2.5)

**Good news:** Both workflows can coexist! Use whichever fits your needs.

---

## 🚀 Advanced: Alias Setup

Add to your `~/.zshrc`:

```bash
# YouTube notes with Cursor
alias ycursor='cd /Users/saurabh.karmakar/Movies/YouTube && ./cursor_notes.sh'
```

Then from anywhere:
```bash
ycursor "https://youtube.com/watch?v=..."
```

---

## 📚 Files Created by This Workflow

```
YouTube/
├── cursor_workflow.py      # Transcript downloader + task generator
├── cursor_notes.sh         # Convenience launcher script
├── .cursorrules            # Teaches Cursor your workflow
├── CURSOR_TASK.md          # Generated task instructions (temporary)
├── CURSOR_WORKFLOW_GUIDE.md # This guide
└── YouTubeNotes/
    ├── transcripts/
    │   └── {video_id}.txt
    └── {video_id}_title_study-notes_cursor.md
```

---

## 🎉 Summary

You now have a **zero-API-cost** workflow that leverages your existing Cursor subscription to generate study notes from YouTube videos!

The workflow is:
1. **Simple** - One command to prepare
2. **Integrated** - Works within Cursor IDE
3. **Flexible** - Use any Cursor model
4. **Interactive** - Refine results in real-time
5. **Cost-effective** - No additional API fees

Happy note-taking! 📝✨

