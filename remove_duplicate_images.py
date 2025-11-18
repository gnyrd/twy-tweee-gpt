#!/usr/bin/env python3
"""
Remove duplicate hero images, keeping only unique ones
Updates metadata to reflect which newsletters share the same image
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict

def get_file_hash(filepath):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    images_dir = Path('/Users/ganyard/Repos/TWEEE_gpt/sources/hero_images')
    metadata_file = images_dir / 'hero_images_metadata.json'
    
    # Load metadata
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Group images by hash
    hash_to_images = defaultdict(list)
    
    print("Calculating file hashes...\n")
    
    for entry in metadata:
        image_path = images_dir / entry['image_filename']
        
        if image_path.exists():
            file_hash = get_file_hash(image_path)
            hash_to_images[file_hash].append(entry)
    
    # Identify duplicates
    unique_count = 0
    duplicate_count = 0
    updated_metadata = []
    
    for file_hash, entries in hash_to_images.items():
        unique_count += 1
        
        if len(entries) > 1:
            # Multiple newsletters use the same image
            # Keep the first one, delete the rest
            keeper = entries[0]
            duplicates = entries[1:]
            
            # Update keeper metadata to list all newsletters using this image
            keeper['shared_by_newsletters'] = [e['newsletter_eml'] for e in entries]
            keeper['usage_count'] = len(entries)
            
            updated_metadata.append(keeper)
            
            # Delete duplicate image files
            for dup in duplicates:
                dup_path = images_dir / dup['image_filename']
                if dup_path.exists():
                    dup_path.unlink()
                    duplicate_count += 1
                    print(f"🗑️  Removed: {dup['image_filename']}")
                    print(f"   (same as {keeper['image_filename']})")
        else:
            # Unique image
            entry = entries[0]
            entry['shared_by_newsletters'] = [entry['newsletter_eml']]
            entry['usage_count'] = 1
            updated_metadata.append(entry)
    
    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(updated_metadata, f, indent=2)
    
    print(f"\n✅ Results:")
    print(f"   Unique images: {unique_count}")
    print(f"   Duplicates removed: {duplicate_count}")
    print(f"   Images remaining: {unique_count}")
    print(f"\n📄 Updated metadata: {metadata_file}")

if __name__ == "__main__":
    main()
