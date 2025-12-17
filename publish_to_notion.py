#!/usr/bin/env python3
"""
Publish study notes to Notion database.
Can be used to publish notes generated via Cursor workflow.
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Import Notion functions from app.py
sys.path.insert(0, str(Path(__file__).parent))
from app import publish_to_notion, extract_title_from_notes, generate_tags_from_content

def get_video_metadata(video_id):
    """Get video metadata using yt-dlp."""
    try:
        import yt_dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'channel': info.get('uploader', info.get('channel', 'Unknown')),
                'duration': info.get('duration', 0),
            }
    except Exception as e:
        return {'title': 'Unknown', 'channel': 'Unknown', 'duration': 0}

def extract_video_id_from_filename(filename):
    """Extract video ID from notes filename.
    
    Format: {video_id}_summary_cursor.md
    """
    # Match pattern: video_id_summary_cursor.md
    match = re.match(r'^([A-Za-z0-9_-]{11})_summary_cursor\.md$', Path(filename).name)
    if match:
        return match.group(1)
    return None

def publish_notes_file(notes_file_path, video_id, video_title, channel, duration="Unknown"):
    """Publish a notes file to Notion."""
    
    # Read the notes file
    notes_path = Path(notes_file_path)
    if not notes_path.exists():
        print(f"❌ Notes file not found: {notes_file_path}")
        return None
    
    with open(notes_path, "r", encoding="utf-8") as f:
        notes_content = f.read()
    
    # Check if Notion is configured
    notion_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_key or not database_id:
        print("❌ Notion not configured. Set NOTION_API_KEY and NOTION_DATABASE_ID in .env")
        return None
    
    # Use "cursor" as provider and "youtube-summary" as prompt for Cursor-generated notes
    provider = "cursor"  # Must match key in providers.py
    prompt_name = "youtube-summary"
    
    print(f"📤 Publishing to Notion...")
    print(f"   Video: {video_title}")
    print(f"   Channel: {channel}")
    
    try:
        notion_url = publish_to_notion(
            notes=notes_content,
            video_title=video_title,
            video_id=video_id,
            channel=channel,
            duration=duration,
            provider=provider,
            prompt_name=prompt_name,
        )
        print(f"   ✅ Published to Notion")
        print(f"   🔗 {notion_url}")
        return notion_url
    except Exception as e:
        print(f"   ⚠️  Notion publish failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python publish_to_notion.py <notes_file> [video_id] [title] [channel] [duration]")
        print("\nExample:")
        print('  python publish_to_notion.py "YouTubeNotes/OOO_x3Oh2nE_summary_cursor.md"')
        print('  python publish_to_notion.py "YouTubeNotes/OOO_x3Oh2nE_summary_cursor.md" OOO_x3Oh2nE "Video Title" "Channel Name"')
        sys.exit(1)
    
    notes_file = sys.argv[1]
    
    # Extract video_id from filename first
    video_id = extract_video_id_from_filename(notes_file)
    
    # If not found in filename, try command line argument
    if not video_id and len(sys.argv) > 2:
        video_id = sys.argv[2]
    
    # If still not found, try to extract from notes file content (look for YouTube URL)
    if not video_id:
        try:
            with open(notes_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Look for YouTube URL pattern
                url_match = re.search(r'youtube\.com/watch\?v=([A-Za-z0-9_-]{11})', content)
                if url_match:
                    video_id = url_match.group(1)
        except Exception:
            pass
    
    if not video_id:
        print("❌ Video ID not found. Could not extract from filename or content.")
        print("   Filename should be: {video_id}_summary_cursor.md")
        sys.exit(1)
    
    # Get metadata from command line args or fetch from YouTube
    if len(sys.argv) > 3:
        video_title = sys.argv[3]
        channel = sys.argv[4] if len(sys.argv) > 4 else "Unknown"
        duration = sys.argv[5] if len(sys.argv) > 5 else "Unknown"
    else:
        # Fetch metadata from YouTube
        print(f"📊 Fetching metadata for video {video_id}...")
        metadata = get_video_metadata(video_id)
        video_title = metadata['title']
        channel = metadata['channel']
        duration = metadata['duration']
        if duration:
            # Format duration
            hours, remainder = divmod(int(duration), 3600)
            minutes, secs = divmod(remainder, 60)
            if hours > 0:
                duration = f"{hours}:{minutes:02d}:{secs:02d}"
            else:
                duration = f"{minutes}:{secs:02d}"
        else:
            duration = "Unknown"
    
    publish_notes_file(notes_file, video_id, video_title, channel, duration)

