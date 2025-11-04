#!/usr/bin/env python3
"""
Send TWEEE newsletter to Mailchimp
Usage: python send_to_mailchimp.py newsletter.html
"""

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os
import sys
from datetime import datetime

# Configuration (use environment variables for security)
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_SERVER = os.getenv('MAILCHIMP_SERVER', 'us21')
MAILCHIMP_AUDIENCE_ID = os.getenv('MAILCHIMP_AUDIENCE_ID')
FROM_NAME = os.getenv('MAILCHIMP_FROM_NAME', 'Tiff')
REPLY_TO = os.getenv('MAILCHIMP_REPLY_TO')

def create_campaign(subject, preview_text, html_content):
    """Create and populate a Mailchimp campaign"""
    
    # Initialize client
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": MAILCHIMP_API_KEY,
        "server": MAILCHIMP_SERVER
    })
    
    try:
        # Create campaign
        campaign_name = f"Newsletter - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(f"Creating campaign: {campaign_name}")
        
        campaign = client.campaigns.create({
            "type": "regular",
            "recipients": {
                "list_id": MAILCHIMP_AUDIENCE_ID
            },
            "settings": {
                "subject_line": subject,
                "preview_text": preview_text,
                "title": campaign_name,
                "from_name": FROM_NAME,
                "reply_to": REPLY_TO
            }
        })
        
        campaign_id = campaign["id"]
        web_id = campaign["web_id"]
        print(f"✅ Campaign created: {campaign_id}")
        
        # Set content
        print("Uploading content...")
        client.campaigns.set_content(campaign_id, {
            "html": html_content
        })
        print(f"✅ Content uploaded")
        
        # Get preview link
        preview_url = f"https://{MAILCHIMP_SERVER}.admin.mailchimp.com/campaigns/edit?id={web_id}"
        print(f"\n🔗 Preview campaign in Mailchimp:")
        print(f"   {preview_url}")
        
        # Ask before sending
        print(f"\n📧 Campaign details:")
        print(f"   Subject: {subject}")
        print(f"   Preview: {preview_text}")
        print(f"   To: Audience {MAILCHIMP_AUDIENCE_ID}")
        print(f"   From: {FROM_NAME}")
        print(f"   Reply-to: {REPLY_TO}")
        
        response = input("\n📤 Send campaign now? (yes/no): ")
        if response.lower() == 'yes':
            print("Sending...")
            client.campaigns.send(campaign_id)
            print("✅ Campaign sent!")
        else:
            print("📝 Campaign saved as draft. Review and send from Mailchimp.")
        
        return campaign_id
        
    except ApiClientError as error:
        print(f"❌ Mailchimp API Error: {error.text}")
        sys.exit(1)

def main():
    # Check environment variables
    if not MAILCHIMP_API_KEY:
        print("❌ Missing MAILCHIMP_API_KEY environment variable")
        print("   Run: source ~/.zshrc")
        sys.exit(1)
    
    if not MAILCHIMP_AUDIENCE_ID:
        print("❌ Missing MAILCHIMP_AUDIENCE_ID environment variable")
        print("   Run: source ~/.zshrc")
        sys.exit(1)
        
    if not REPLY_TO:
        print("❌ Missing MAILCHIMP_REPLY_TO environment variable")
        print("   Run: source ~/.zshrc")
        sys.exit(1)
    
    print(f"Using Mailchimp configuration:")
    print(f"  Server: {MAILCHIMP_SERVER}")
    print(f"  Audience: {MAILCHIMP_AUDIENCE_ID}")
    print(f"  From: {FROM_NAME}")
    print(f"  Reply-to: {REPLY_TO}\n")
    
    # Read newsletter file
    if len(sys.argv) < 2:
        print("Usage: python send_to_mailchimp.py newsletter.html")
        sys.exit(1)
    
    newsletter_file = sys.argv[1]
    
    if not os.path.exists(newsletter_file):
        print(f"❌ File not found: {newsletter_file}")
        sys.exit(1)
    
    with open(newsletter_file, 'r') as f:
        html_content = f.read()
    
    print(f"📄 Loaded newsletter from: {newsletter_file}")
    print(f"   Content length: {len(html_content)} characters\n")
    
    # Get campaign details
    subject = input("📧 Subject line: ")
    if not subject:
        print("❌ Subject line is required")
        sys.exit(1)
        
    preview_text = input("👀 Preview text (50-100 chars): ")
    
    # Create and send
    create_campaign(subject, preview_text, html_content)

if __name__ == "__main__":
    main()
