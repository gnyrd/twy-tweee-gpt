#!/usr/bin/env python3
# Copyright © 2025 Ninsim, Inc. All rights reserved.
"""
Create thumbnail versions of newsletter images for quick review.
"""
import os
from PIL import Image
from pathlib import Path

SOURCE_DIR = "sources/all_newsletter_images"
THUMB_DIR = "sources/thumbnails"
MAX_SIZE = (400, 400)

def create_thumbnails():
    """Create thumbnails of all images."""
    Path(THUMB_DIR).mkdir(parents=True, exist_ok=True)
    
    images = sorted(Path(SOURCE_DIR).glob("*.png"))
    print(f"Creating thumbnails for {len(images)} images...")
    
    for img_path in images:
        thumb_path = Path(THUMB_DIR) / img_path.name
        
        if thumb_path.exists():
            continue
            
        try:
            with Image.open(img_path) as img:
                img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                img.save(thumb_path, "PNG", optimize=True)
            print(f"✓ {img_path.name}")
        except Exception as e:
            print(f"✗ {img_path.name}: {e}")
    
    print(f"\nThumbnails created in {THUMB_DIR}/")

if __name__ == "__main__":
    create_thumbnails()
