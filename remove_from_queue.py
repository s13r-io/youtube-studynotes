#!/usr/bin/env python3
"""
Remove a transcript file path from CURSOR_TASK.md queue.
Helper script for Cursor to use when processing videos.
"""

import sys
from pathlib import Path

def remove_from_queue(transcript_path):
    """Remove a transcript path from CURSOR_TASK.md."""
    queue_file = Path("CURSOR_TASK.md")
    
    if not queue_file.exists():
        print(f"⚠️  CURSOR_TASK.md not found")
        return False
    
    # Read all lines
    with open(queue_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Filter out the line matching the transcript path
    original_count = len([l for l in lines if l.strip()])
    filtered_lines = [line for line in lines if line.strip() != transcript_path.strip()]
    new_count = len([l for l in filtered_lines if l.strip()])
    
    # Write back (preserve empty lines structure)
    with open(queue_file, "w", encoding="utf-8") as f:
        f.writelines(filtered_lines)
    
    if original_count > new_count:
        print(f"✅ Removed from queue: {transcript_path}")
        print(f"   Remaining: {new_count} video(s)")
        return True
    else:
        print(f"⚠️  Transcript path not found in queue: {transcript_path}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_from_queue.py <transcript_path>")
        print("\nExample:")
        print('  python remove_from_queue.py "YouTubeNotes/transcripts/OOO_x3Oh2nE.txt"')
        sys.exit(1)
    
    transcript_path = sys.argv[1]
    remove_from_queue(transcript_path)

