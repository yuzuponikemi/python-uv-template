#!/bin/bash

# SessionStart Hook - Read AGENTMASTER.md context
# This hook automatically loads the AGENTMASTER.md file at session start
# to ensure Claude is always aware of the repository's AI agent guidelines.

# Get the repository root (two levels up from .claude/hooks/)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTMASTER_FILE="$REPO_ROOT/AGENTMASTER.md"

# Check if the file exists
if [ -f "$AGENTMASTER_FILE" ]; then
    echo "📚 Loading AGENTMASTER.md context..."
    echo ""
    echo "=== AGENTMASTER Context ==="
    cat "$AGENTMASTER_FILE"
    echo ""
    echo "=== End of AGENTMASTER Context ==="
    echo ""
    echo "✅ AGENTMASTER.md loaded successfully!"
else
    echo "⚠️  Warning: AGENTMASTER.md not found at $AGENTMASTER_FILE"
    echo "   Please ensure AGENTMASTER.md exists in the repository root."
fi
