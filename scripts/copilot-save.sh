#!/usr/bin/env bash
# Simple script to append Copilot/assistant prompts to .copilot/requests.md
# Usage:
#   scripts/copilot-save.sh "My prompt here"
#   printf "Multi-line prompt\n" | scripts/copilot-save.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="$ROOT_DIR/.copilot"
TARGET_FILE="$TARGET_DIR/requests.md"

mkdir -p "$TARGET_DIR"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [ -t 0 ] && [ "$#" -gt 0 ]; then
  PROMPT="$*"
else
  PROMPT="$(cat -)"
fi

printf "### %s\n\n%s\n\n" "$TS" "$PROMPT" >> "$TARGET_FILE"
echo "Saved to $TARGET_FILE"
