#!/usr/bin/env python3
"""
Extract hero images from all newsletter .eml files for training
Creates a dataset linking each image to its source newsletter
"""

import email
import os
import re
import json
import requests
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict

def get_newsletter_text(msg):
    """Extract plain text content from newsletter"""
    text_content = ""
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            text_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            break
    return text_content

def extract_hero_image(eml_path, output_dir, metadata_list):
    """Extract the main hero image from a newsletter"""
    
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    newsletter_name = Path(eml_path).stem
    newsletter_date = newsletter_name.split('_')[0]  # YYYY-MM-DD from filename
    
    # Get subject line
    subject = msg.get('Subject', 'Unknown')
    
    # Get newsletter text
    newsletter_text = get_newsletter_text(msg)
    
    # Look for HTML content
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Find all image URLs (excluding tracking pixels and social icons)
            img_tags = re.findall(r'<img[^>]+src=["\'](https://[^"\']+)["\']', html_content, re.IGNORECASE)
            
            # Collect all candidate image URLs
            candidates = []
            
            for url in img_tags:
                # Skip tracking pixels
                if 'track/open' in url or 'beacon' in url:
                    continue
                
                # Skip social icons
                if 'social-block' in url or 'facebook' in url or 'instagram' in url or 'tiktok' in url or 'youtube' in url:
                    continue
                
                # Skip tiny images (likely logos/icons)
                if '-40.png' in url or '-48.png' in url or 'icon' in url.lower():
                    continue
                
                candidates.append(url)
            
            # Download all candidates and pick the largest
            largest_size = 0
            hero_image = None
            hero_data = None
            
            for url in candidates:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    size = len(response.content)
                    
                    # Only consider images > 100KB (excludes small logos)
                    if size > 100000 and size > largest_size:
                        largest_size = size
                        hero_image = url
                        hero_data = response.content
                except:
                    continue
            
            if hero_image and hero_data:
                # Use already-downloaded image data
                try:
                    # Determine file extension
                    parsed_url = urlparse(hero_image)
                    url_path = parsed_url.path
                    if url_path.endswith('.png'):
                        ext = 'png'
                    elif url_path.endswith('.jpg') or url_path.endswith('.jpeg'):
                        ext = 'jpg'
                    else:
                        ext = 'jpg'  # default
                    
                    # Save with clean filename: YYYY-MM-DD_descriptive-name.ext
                    safe_subject = re.sub(r'[<>:"/\\|?*]', '', subject)
                    safe_subject = safe_subject.replace(' ', '-')[:50]  # Truncate long subjects
                    
                    image_filename = f"{newsletter_date}_{safe_subject}.{ext}"
                    image_path = output_dir / image_filename
                    
                    with open(image_path, 'wb') as img_file:
                        img_file.write(hero_data)
                    
                    # Store metadata
                    metadata_list.append({
                        'image_filename': image_filename,
                        'newsletter_eml': Path(eml_path).name,
                        'newsletter_date': newsletter_date,
                        'subject': subject,
                        'image_url': hero_image,
                        'image_size_bytes': len(hero_data),
                        'text_preview': newsletter_text[:500] if newsletter_text else None
                    })
                    
                    print(f"✅ {newsletter_date}: {subject[:60]}")
                    return True
                    
                except Exception as e:
                    print(f"❌ {newsletter_date}: Error downloading - {str(e)}")
                    return False
    
    print(f"⚠️  {newsletter_date}: No hero image found")
    return False

def remove_duplicate_newsletters(eml_dir):
    """Remove duplicate .eml files based on date+subject"""
    
    eml_files = list(Path(eml_dir).glob('*.eml'))
    
    # Group by date and subject
    seen = {}
    duplicates = []
    
    for eml_file in eml_files:
        with open(eml_file, 'rb') as f:
            msg = email.message_from_binary_file(f)
        
        subject = msg.get('Subject', 'Unknown')
        date_received = msg.get('Date', '')
        
        # Create unique key
        key = f"{date_received}_{subject}"
        
        if key in seen:
            duplicates.append(eml_file)
        else:
            seen[key] = eml_file
    
    # Remove duplicates
    for dup in duplicates:
        dup.unlink()
        print(f"🗑️  Removed duplicate: {dup.name}")
    
    return len(duplicates)

def main():
    # Paths
    eml_dir = Path('/Users/ganyard/Repos/TWEEE_gpt/sources/newsletters_eml')
    output_dir = Path('/Users/ganyard/Repos/TWEEE_gpt/sources/hero_images')
    output_dir.mkdir(exist_ok=True)
    
    print("Step 1: Removing duplicate newsletters...\n")
    num_duplicates = remove_duplicate_newsletters(eml_dir)
    print(f"\n✅ Removed {num_duplicates} duplicate(s)\n")
    
    print("Step 2: Extracting hero images...\n")
    
    # Get all .eml files
    eml_files = sorted(Path(eml_dir).glob('*.eml'), reverse=True)  # Newest first
    
    metadata_list = []
    success_count = 0
    
    for eml_file in eml_files:
        if extract_hero_image(eml_file, output_dir, metadata_list):
            success_count += 1
    
    # Save metadata as JSON
    metadata_file = output_dir / 'hero_images_metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata_list, f, indent=2)
    
    print(f"\n✅ Extracted {success_count} hero images from {len(eml_files)} newsletters")
    print(f"📁 Images saved to: {output_dir}")
    print(f"📄 Metadata saved to: {metadata_file}")

if __name__ == "__main__":
    main()
