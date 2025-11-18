#!/usr/bin/env python3
"""
Download images from newsletter .eml files (including external URLs)
"""

import email
import sys
import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse

def download_images_from_eml(eml_path, output_dir=None):
    """Extract and download all images from an .eml file"""
    
    if output_dir is None:
        output_dir = Path(eml_path).parent / "extracted_images"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Read the .eml file
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    newsletter_name = Path(eml_path).stem
    images_found = []
    
    print(f"📧 Newsletter: {newsletter_name}\n")
    
    # Look for HTML content
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Find all img src URLs
            img_tags = re.findall(r'<img[^>]+src=["\'](https://[^"\']+)["\']', html_content, re.IGNORECASE)
            
            print(f"Found {len(img_tags)} external images\n")
            
            for i, url in enumerate(img_tags):
                # Skip tracking pixels (very small images)
                if 'track/open' in url or 'beacon' in url:
                    print(f"⏭️  [{i+1}] Skipping tracking pixel")
                    continue
                
                # Extract filename from URL
                parsed_url = urlparse(url)
                url_path = parsed_url.path
                
                # Get file extension
                if '/' in url_path:
                    url_filename = url_path.split('/')[-1]
                else:
                    url_filename = f"image_{i+1}.jpg"
                
                # Clean filename
                safe_filename = f"{newsletter_name}_{i+1}_{url_filename}"
                safe_filename = re.sub(r'[<>:"/\\|?*]', '_', safe_filename)
                
                output_path = output_dir / safe_filename
                
                # Download image
                try:
                    print(f"📥 [{i+1}] Downloading: {url[:60]}...")
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    with open(output_path, 'wb') as img_file:
                        img_file.write(response.content)
                    
                    images_found.append({
                        'filename': safe_filename,
                        'size': len(response.content),
                        'url': url
                    })
                    
                    print(f"   ✅ Saved: {safe_filename} ({len(response.content)} bytes)\n")
                    
                except Exception as e:
                    print(f"   ❌ Error: {str(e)}\n")
    
    return images_found

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 download_newsletter_images.py <path_to_eml_file>")
        sys.exit(1)
    
    eml_path = sys.argv[1]
    
    if not os.path.exists(eml_path):
        print(f"❌ File not found: {eml_path}")
        sys.exit(1)
    
    images = download_images_from_eml(eml_path)
    
    if images:
        print(f"\n✅ Downloaded {len(images)} image(s)")
        print(f"📁 Saved to: {Path(eml_path).parent / 'extracted_images'}")
    else:
        print(f"\n⚠️  No images downloaded")
