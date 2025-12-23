#!/usr/bin/env python3
# Copyright © 2025 Ninsim, Inc. All rights reserved.
"""
Extract ALL large images from ALL newsletters
Saves them with numbered prefixes so you can see all options
"""

import email
import re
import requests
from pathlib import Path
from collections import defaultdict

def extract_all_images_from_newsletter(eml_path, output_dir):
    """Extract all images over 500KB from a newsletter"""
    
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    newsletter_name = Path(eml_path).stem
    newsletter_date = newsletter_name.split('_')[0]
    
    # Look for HTML content
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Find all image URLs
            img_tags = re.findall(r'<img[^>]+src=["\'](https://[^"\']+)["\']', html_content, re.IGNORECASE)
            
            image_count = 0
            for url in img_tags:
                # Skip obvious non-hero images
                if any(skip in url for skip in ['track/open', 'beacon', 'social-block', 'facebook', 'instagram', 'tiktok', 'youtube', '-40.png', '-48.png']):
                    continue
                
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    size = len(response.content)
                    
                    # Only save images over 500KB
                    if size > 500000:
                        image_count += 1
                        
                        # Determine extension
                        if url.endswith('.png') or 'png' in url:
                            ext = 'png'
                        else:
                            ext = 'jpg'
                        
                        # Save with prefix number so you can see all options
                        filename = f"{newsletter_date}_{image_count}.{ext}"
                        filepath = output_dir / filename
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"✅ {newsletter_date} #{image_count}: {size/1024/1024:.1f}MB")
                
                except Exception as e:
                    continue
            
            if image_count > 0:
                return image_count
    
    return 0

def main():
    eml_dir = Path('/Users/ganyard/Repos/TWEEE_gpt/sources/newsletters_eml')
    output_dir = Path('/Users/ganyard/Repos/TWEEE_gpt/sources/all_newsletter_images')
    output_dir.mkdir(exist_ok=True)
    
    print("Extracting ALL large images from newsletters...\n")
    
    eml_files = sorted(eml_dir.glob('*.eml'), reverse=True)
    
    total_images = 0
    newsletters_with_images = 0
    
    for eml_file in eml_files:
        count = extract_all_images_from_newsletter(eml_file, output_dir)
        if count > 0:
            newsletters_with_images += 1
            total_images += count
    
    print(f"\n✅ Complete!")
    print(f"   {total_images} images from {newsletters_with_images} newsletters")
    print(f"   Saved to: {output_dir}")
    print(f"\nNow review and move your favorites to sources/hero_images/")

if __name__ == "__main__":
    main()
