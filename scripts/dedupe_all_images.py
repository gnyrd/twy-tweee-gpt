#!/usr/bin/env python3
# Copyright © 2025 Ninsim, Inc. All rights reserved.
"""
Remove duplicate images, keeping only unique ones
"""

import hashlib
from pathlib import Path
from collections import defaultdict

def get_file_hash(filepath):
    """Calculate MD5 hash"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

images_dir = Path('/Users/ganyard/Repos/TWEEE_gpt/sources/all_newsletter_images')

# Group by hash
hash_to_files = defaultdict(list)

print("Calculating hashes...\n")

for img_file in images_dir.glob('*'):
    if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
        file_hash = get_file_hash(img_file)
        hash_to_files[file_hash].append(img_file)

# Remove duplicates (keep first, delete rest)
removed = 0
for file_hash, files in hash_to_files.items():
    if len(files) > 1:
        # Keep the first one (usually earliest date)
        keeper = sorted(files)[0]
        for dup in files[1:]:
            import twy_deletions as deletions
            approval = deletions.gate(
                job="tweee_gpt_image_dedupe",
                resource=str(dup),
                kind="duplicate image (hash match)",
                reason=f"Byte-identical to {keeper.name} (kept)",
                size_bytes=dup.stat().st_size,
                backup_location=f"identical content kept at {keeper.name}",
                backup_verified="content-hash match",
            )
            if approval is None:
                print(f"AWAITING JP APPROVAL: {dup.name}")
                continue
            dup.unlink()
            removed += 1
            print(f"🗑️  Removed: {dup.name} (duplicate of {keeper.name})")

print(f"\n✅ Removed {removed} duplicates")
print(f"   {len(hash_to_files)} unique images remaining")
