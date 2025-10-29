#!/bin/bash
# Script to help rename TWY newsletters to format: YYYY-MM-DD-short-descriptor.pdf
# Usage: This script lists files that need renaming. Manual review recommended for theme extraction.

echo "=== 2024 Newsletters to Rename ==="
echo ""
find "/Users/ganyard/Repos/TWEEE_gpt/knowledge/TWY Newsletters/2024" -name "*.pdf" -print0 | while IFS= read -r -d '' file; do
    basename "$file"
done | head -20

echo ""
echo "=== 2025 Newsletters to Rename ==="
echo ""
find "/Users/ganyard/Repos/TWEEE_gpt/knowledge/TWY Newsletters/2025" -name "*.pdf" -print0 | while IFS= read -r -d '' file; do
    basename "$file"
done | head -20

echo ""
echo "Total newsletters:"
echo "  2024: $(find "/Users/ganyard/Repos/TWEEE_gpt/knowledge/TWY Newsletters/2024" -name "*.pdf" | wc -l | tr -d ' ')"
echo "  2025: $(find "/Users/ganyard/Repos/TWEEE_gpt/knowledge/TWY Newsletters/2025" -name "*.pdf" | wc -l | tr -d ' ')"
echo ""
echo "Manual renaming recommended. Suggested format: YYYY-MM-DD-theme.pdf"
echo "Example: 2024-03-15-tara-courage.pdf"
