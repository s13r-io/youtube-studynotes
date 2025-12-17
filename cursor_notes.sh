#!/bin/bash
# YouTube Study Notes - Cursor Workflow Launcher

# Activate virtual environment
source "$(dirname "$0")/venv/bin/activate"

# Run the workflow
python "$(dirname "$0")/cursor_workflow.py" "$@"

# Open CURSOR_TASK.md in Cursor (if it was created)
if [ -f "$(dirname "$0")/CURSOR_TASK.md" ]; then
    echo ""
    echo "🚀 Opening task file in Cursor..."
    cursor "$(dirname "$0")/CURSOR_TASK.md"
fi

