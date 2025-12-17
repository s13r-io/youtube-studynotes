#!/bin/bash
# Publish the most recently created summary file to Notion

# Activate virtual environment
source "$(dirname "$0")/venv/bin/activate"

# Find the most recent cursor-generated summary file
LATEST_FILE=$(find YouTubeNotes -name "*_summary_cursor.md" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)

if [ -z "$LATEST_FILE" ]; then
    echo "❌ No cursor-generated summary files found in YouTubeNotes/"
    echo "   Looking for files matching: *_summary_cursor.md"
    exit 1
fi

echo "📤 Publishing latest summary to Notion..."
echo "   File: $LATEST_FILE"
echo ""

# Run the publish script
python publish_to_notion.py "$LATEST_FILE"

