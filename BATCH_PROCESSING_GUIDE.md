# 📋 Batch Processing Guide

## Overview

The workflow now supports **batch processing** - you can download transcripts for multiple videos and process them all sequentially with a single command.

---

## How It Works

### 1. Building the Queue

Each time you run `cursor_workflow.py`, it:
- Downloads the transcript
- **Appends** the transcript file path to `CURSOR_TASK.md` (one line per video)
- Does NOT overwrite existing entries

**Example:**
```bash
./cursor_notes.sh "https://www.youtube.com/watch?v=VIDEO1"
./cursor_notes.sh "https://www.youtube.com/watch?v=VIDEO2"
./cursor_notes.sh "https://www.youtube.com/watch?v=VIDEO3"
```

**Result:** `CURSOR_TASK.md` now contains:
```
YouTubeNotes/transcripts/VIDEO1.txt
YouTubeNotes/transcripts/VIDEO2.txt
YouTubeNotes/transcripts/VIDEO3.txt
```

### 2. Processing All Videos

Tell Cursor once: **"Complete the task in CURSOR_TASK.md"**

Cursor will:
1. Read `CURSOR_TASK.md` line by line
2. Process each transcript using `prompts/youtube-summary.md`
3. Generate summary → Save → Publish to Notion → Remove from queue
4. Continue until queue is empty
5. Show completion summary

---

## File Structure

### `CURSOR_TASK.md` (Queue File)
- **Format:** One transcript file path per line
- **Purpose:** Simple queue/list of videos to process
- **No metadata:** Only file paths, no video details

**Example:**
```
YouTubeNotes/transcripts/CEvIs9y1uog.txt
YouTubeNotes/transcripts/IJ1SYhGssSU.txt
YouTubeNotes/transcripts/OOO_x3Oh2nE.txt
```

### `.cursorrules` (Processing Instructions)
- Contains ALL workflow logic and instructions
- Tells Cursor how to process the queue
- Uses `prompts/youtube-summary.md` template

### Output Files
- **Format:** `{video_id}_summary_cursor.md`
- **Location:** `YouTubeNotes/`
- **Template:** `prompts/youtube-summary.md`

---

## Workflow Example

### Morning: Download Transcripts
```bash
# Download 5 videos
./cursor_notes.sh "https://www.youtube.com/watch?v=CEvIs9y1uog"
./cursor_notes.sh "https://www.youtube.com/watch?v=IJ1SYhGssSU"
./cursor_notes.sh "https://www.youtube.com/watch?v=OOO_x3Oh2nE"
./cursor_notes.sh "https://www.youtube.com/watch?v=sNvuH-iTi4c"
./cursor_notes.sh "https://www.youtube.com/watch?v=Td_q0sHm6HU"
```

**CURSOR_TASK.md now has 5 transcript paths**

### Afternoon: Process All
```
You: Complete the task in CURSOR_TASK.md

Cursor: 
  📋 Found 5 videos in queue
  Processing Video 1/5: CEvIs9y1uog...
  ✅ Processed: CEvIs9y1uog (1/5)
  📄 Saved: YouTubeNotes/CEvIs9y1uog_summary_cursor.md
  📤 Published to Notion
  
  Processing Video 2/5: IJ1SYhGssSU...
  ✅ Processed: IJ1SYhGssSU (2/5)
  ...
  
  ✅ All 5 videos processed!
```

**CURSOR_TASK.md is now empty**

---

## Key Features

### ✅ Batch Processing
- Process multiple videos with one command
- Sequential processing (one at a time)
- Automatic queue management

### ✅ Minimal Queue File
- `CURSOR_TASK.md` only contains transcript paths
- No video metadata or instructions
- Easy to read and manage

### ✅ Automatic Cleanup
- Completed videos removed from queue automatically
- Queue file stays clean
- No manual cleanup needed

### ✅ Error Handling
- If one video fails, continue with next
- Errors logged but don't stop batch
- Failed videos still removed from queue

---

## Helper Scripts

### `remove_from_queue.py`
Manually remove a transcript from the queue:
```bash
python remove_from_queue.py "YouTubeNotes/transcripts/VIDEO_ID.txt"
```

### `publish_latest.sh`
Publish the most recent summary to Notion:
```bash
./publish_latest.sh
```

---

## Tips

1. **Download First, Process Later**
   - Download all transcripts in the morning
   - Process them all in one batch later
   - More efficient than one-by-one

2. **Check Queue Status**
   ```bash
   cat CURSOR_TASK.md
   wc -l CURSOR_TASK.md  # Count videos in queue
   ```

3. **Clear Queue Manually**
   ```bash
   > CURSOR_TASK.md  # Empty the file
   ```

4. **Process Specific Video**
   - Remove other videos from queue first
   - Or process one-by-one manually

---

## Troubleshooting

### Queue Not Processing
- Check `CURSOR_TASK.md` exists and has content
- Verify transcript files exist at specified paths
- Check `.cursorrules` is in project root

### Video Stuck in Queue
- Manually remove using `remove_from_queue.py`
- Or edit `CURSOR_TASK.md` directly

### Wrong Template Used
- Ensure `.cursorrules` specifies `youtube-summary.md`
- Check `prompts/youtube-summary.md` exists

---

## Migration from Old Format

If you have an old `CURSOR_TASK.md` with detailed instructions:

1. Extract transcript paths manually
2. Create new `CURSOR_TASK.md` with just paths:
   ```
   YouTubeNotes/transcripts/video1.txt
   YouTubeNotes/transcripts/video2.txt
   ```
3. Process normally

---

## Summary

- **Queue File:** `CURSOR_TASK.md` (minimal, just paths)
- **Template:** `prompts/youtube-summary.md` (for all videos)
- **Instructions:** `.cursorrules` (all workflow logic)
- **Output:** `{video_id}_summary_cursor.md`
- **Processing:** Sequential, automatic, until queue empty

