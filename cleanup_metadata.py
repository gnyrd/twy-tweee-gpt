#!/usr/bin/env python3
"""
Clean up metadata to only include images that still exist
"""

import json
from pathlib import Path

images_dir = Path('/Users/ganyard/Repos/TWEEE_gpt/sources/hero_images')
metadata_file = images_dir / 'hero_images_metadata.json'

# Load current metadata
with open(metadata_file, 'r') as f:
    metadata = json.load(f)

# Get list of existing image files
existing_images = {f.name for f in images_dir.glob('*.png')} | {f.name for f in images_dir.glob('*.jpg')}

# Filter metadata to only include existing images
filtered_metadata = [entry for entry in metadata if entry['image_filename'] in existing_images]

# Save updated metadata
with open(metadata_file, 'w') as f:
    json.dump(filtered_metadata, f, indent=2)

print(f"✅ Metadata updated")
print(f"   Kept: {len(filtered_metadata)} entries")
print(f"   Removed: {len(metadata) - len(filtered_metadata)} entries")
print(f"\nRemaining images:")
for entry in filtered_metadata:
    print(f"  - {entry['newsletter_date']}: {entry['subject'][:60]}")
