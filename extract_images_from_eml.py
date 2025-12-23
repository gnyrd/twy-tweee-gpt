#!/usr/bin/env python3
# Copyright © 2025 Ninsim, Inc. All rights reserved.
"""
Extract images from .eml newsletter files
"""

import email
import sys
import os
from pathlib import Path

def extract_images_from_eml(eml_path, output_dir=None):
    """Extract all images from an .eml file"""
    
    if output_dir is None:
        output_dir = Path(eml_path).parent / "extracted_images"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Read the .eml file
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    newsletter_name = Path(eml_path).stem
    images_found = []
    
    # Walk through all parts of the email
    for part in msg.walk():
        content_type = part.get_content_type()
        
        # Look for image attachments
        if content_type.startswith('image/'):
            filename = part.get_filename()
            
            if filename:
                # Save the image
                img_data = part.get_payload(decode=True)
                
                # Create filename: newsletter_name + original filename
                safe_filename = f"{newsletter_name}_{filename}"
                output_path = output_dir / safe_filename
                
                with open(output_path, 'wb') as img_file:
                    img_file.write(img_data)
                
                images_found.append({
                    'filename': safe_filename,
                    'size': len(img_data),
                    'type': content_type
                })
                print(f"✅ Extracted: {safe_filename} ({len(img_data)} bytes, {content_type})")
    
    # Also look for inline/embedded images in HTML
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Look for data: URIs or external image references
            if 'img src=' in html_content.lower():
                print(f"\n📄 HTML content found ({len(html_content)} chars)")
                print("   Images may be referenced as external URLs or data URIs")
                
                # Count img tags
                import re
                img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
                print(f"   Found {len(img_tags)} <img> tags")
                
                for i, src in enumerate(img_tags[:5]):  # Show first 5
                    if src.startswith('http'):
                        print(f"   [{i+1}] External URL: {src[:80]}...")
                    elif src.startswith('data:'):
                        print(f"   [{i+1}] Data URI: {src[:80]}...")
                    elif src.startswith('cid:'):
                        print(f"   [{i+1}] Content-ID reference: {src}")
    
    return images_found

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_images_from_eml.py <path_to_eml_file>")
        sys.exit(1)
    
    eml_path = sys.argv[1]
    
    if not os.path.exists(eml_path):
        print(f"❌ File not found: {eml_path}")
        sys.exit(1)
    
    print(f"📧 Processing: {eml_path}\n")
    images = extract_images_from_eml(eml_path)
    
    if images:
        print(f"\n✅ Extracted {len(images)} image(s)")
    else:
        print(f"\n⚠️  No attached images found (may be external URLs or inline data)")
