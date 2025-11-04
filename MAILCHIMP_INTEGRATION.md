# Mailchimp Integration Guide

## Overview
After creating a newsletter using the TWEEE workflow, Tiff can send it directly to Mailchimp for distribution to her yoga community.

---

## Setup Requirements

### 1. Mailchimp Account Information
You'll need:
- **API Key** - From Mailchimp account settings
- **Audience ID** - Your subscriber list ID
- **Server Prefix** - Part of your API key (e.g., `us19`)

### 2. Get Your Mailchimp API Key
1. Log into Mailchimp
2. Click profile icon → **Account & Billing**
3. Navigate to **Extras** → **API keys**
4. Create a new API key or use existing one
5. **IMPORTANT:** Store securely - treat like a password

### 3. Get Your Audience ID
1. In Mailchimp, go to **Audience** → **All contacts**
2. Click **Settings** → **Audience name and defaults**
3. Find **Audience ID** (looks like: `a1b2c3d4e5`)

---

## Integration Options

### Option A: GPT Action (Recommended for Tiff)
**Best for:** Non-technical users who want to stay in the GPT interface

**Setup:**
1. Configure Custom GPT with Mailchimp Action
2. Tiff creates newsletter in GPT
3. Reviews/refines draft
4. Says: "Send this to Mailchimp"
5. GPT creates campaign and optionally schedules/sends

**Pros:**
- No coding required
- Natural conversation flow
- Stays in familiar interface

**Cons:**
- Requires ChatGPT Plus/Team/Enterprise
- API key stored in OpenAI (secure, but third-party)

---

### Option B: Python Script
**Best for:** Technical users or automation workflows

**Setup:**
1. Install Mailchimp Python library
2. Run script with newsletter content
3. Script creates campaign in Mailchimp

**Pros:**
- Full control over process
- Can integrate with other tools
- Can automate scheduling

**Cons:**
- Requires Python knowledge
- Separate step outside GPT

---

### Option C: Manual Copy-Paste
**Best for:** Maximum control, minimal setup

**Process:**
1. GPT generates newsletter
2. Tiff copies final HTML
3. Pastes into Mailchimp campaign editor
4. Reviews preview and sends

**Pros:**
- No API setup needed
- Full manual review in Mailchimp
- See exactly how it looks

**Cons:**
- Extra manual step
- More time-consuming

---

## Detailed Setup: Option A (GPT Action)

### Step 1: Configure GPT Action

In your Custom GPT settings, add this Action:

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Mailchimp Campaign API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://{server}.api.mailchimp.com/3.0",
      "variables": {
        "server": {
          "default": "us19",
          "description": "Your Mailchimp server prefix (from API key)"
        }
      }
    }
  ],
  "paths": {
    "/campaigns": {
      "post": {
        "operationId": "createCampaign",
        "summary": "Create a new email campaign",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["regular"],
                    "default": "regular"
                  },
                  "recipients": {
                    "type": "object",
                    "properties": {
                      "list_id": {
                        "type": "string",
                        "description": "Mailchimp audience ID"
                      }
                    }
                  },
                  "settings": {
                    "type": "object",
                    "properties": {
                      "subject_line": {
                        "type": "string"
                      },
                      "preview_text": {
                        "type": "string"
                      },
                      "title": {
                        "type": "string",
                        "description": "Internal campaign name"
                      },
                      "from_name": {
                        "type": "string",
                        "default": "Tiff"
                      },
                      "reply_to": {
                        "type": "string"
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Campaign created successfully"
          }
        }
      }
    },
    "/campaigns/{campaign_id}/content": {
      "put": {
        "operationId": "setCampaignContent",
        "summary": "Set the HTML content of a campaign",
        "parameters": [
          {
            "name": "campaign_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "html": {
                    "type": "string",
                    "description": "Full HTML content"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Content updated successfully"
          }
        }
      }
    },
    "/campaigns/{campaign_id}/actions/send": {
      "post": {
        "operationId": "sendCampaign",
        "summary": "Send the campaign immediately",
        "parameters": [
          {
            "name": "campaign_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Campaign sent successfully"
          }
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "basicAuth": {
        "type": "http",
        "scheme": "basic"
      }
    }
  },
  "security": [
    {
      "basicAuth": []
    }
  ]
}
```

### Step 2: Authentication Setup

In GPT Action settings:
- **Authentication Type:** Basic Auth
- **Username:** `anystring` (Mailchimp ignores this)
- **Password:** Your Mailchimp API key

### Step 3: Update GPT Instructions

Add to `INSTRUCTIONS.md`:

```markdown
## Mailchimp Distribution (Optional)

When user says "send to Mailchimp" or "create campaign":

1. Confirm newsletter is finalized
2. Ask for:
   - Subject line (if not already in newsletter)
   - Preview text (50-100 chars, enticing hook)
   - Send now or schedule for later?
3. Create campaign using createCampaign action
4. Set content using setCampaignContent action
5. If user confirms, send using sendCampaign action
6. Provide Mailchimp campaign link for review

**Default settings:**
- From name: "Tiff"
- Reply-to: [Tiff's email]
- Audience: [Default audience ID]

**Safety checks:**
- Always show preview link before sending
- Confirm send action explicitly
- Never auto-send without user confirmation
```

---

## Detailed Setup: Option B (Python Script)

### Installation

```bash
pip install mailchimp-marketing
```

### Script: `send_to_mailchimp.py`

```python
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
MAILCHIMP_SERVER = os.getenv('MAILCHIMP_SERVER', 'us19')
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
        print(f"✅ Campaign created: {campaign_id}")
        
        # Set content
        client.campaigns.set_content(campaign_id, {
            "html": html_content
        })
        print(f"✅ Content uploaded")
        
        # Get preview link
        print(f"\n🔗 Preview: https://{MAILCHIMP_SERVER}.admin.mailchimp.com/campaigns/edit?id={campaign['web_id']}")
        
        # Ask before sending
        response = input("\n📤 Send campaign now? (yes/no): ")
        if response.lower() == 'yes':
            client.campaigns.send(campaign_id)
            print("✅ Campaign sent!")
        else:
            print("📝 Campaign saved as draft. Review and send from Mailchimp.")
        
        return campaign_id
        
    except ApiClientError as error:
        print(f"❌ Error: {error.text}")
        sys.exit(1)

def main():
    # Check environment variables
    if not all([MAILCHIMP_API_KEY, MAILCHIMP_AUDIENCE_ID, REPLY_TO]):
        print("❌ Missing required environment variables:")
        print("   MAILCHIMP_API_KEY")
        print("   MAILCHIMP_AUDIENCE_ID")
        print("   MAILCHIMP_REPLY_TO")
        sys.exit(1)
    
    # Read newsletter file
    if len(sys.argv) < 2:
        print("Usage: python send_to_mailchimp.py newsletter.html")
        sys.exit(1)
    
    newsletter_file = sys.argv[1]
    with open(newsletter_file, 'r') as f:
        html_content = f.read()
    
    # Get campaign details
    subject = input("📧 Subject line: ")
    preview_text = input("👀 Preview text (50-100 chars): ")
    
    # Create and send
    create_campaign(subject, preview_text, html_content)

if __name__ == "__main__":
    main()
```

### Setup Environment Variables

Add to `~/.zshrc`:

```bash
# Mailchimp Configuration
export MAILCHIMP_API_KEY="your_api_key_here"
export MAILCHIMP_SERVER="us19"  # Your server prefix
export MAILCHIMP_AUDIENCE_ID="your_audience_id"
export MAILCHIMP_FROM_NAME="Tiff"
export MAILCHIMP_REPLY_TO="tiff@example.com"
```

Then: `source ~/.zshrc`

### Usage

```bash
# Save newsletter HTML from GPT to file
# Then run:
python send_to_mailchimp.py newsletter.html
```

---

## Workflow Integration

### Updated Newsletter Creation Flow

**Stage 1: Quick Capture** (5-10 min)
- Tiff provides seed content

**Stage 2: AI Generation** (automated)
- GPT generates draft

**Stage 3: Refinement** (10-15 min)
- Tiff reviews and refines

**Stage 4: Distribution** (NEW - 2-5 min)
- **Option A:** "Send to Mailchimp" in GPT
- **Option B:** Run Python script
- **Option C:** Copy-paste to Mailchimp
- Review preview
- Schedule or send

**Total time: 17-30 min** (vs 60-90 min previously)

---

## Security Best Practices

1. **Never commit API keys to Git**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Restrict API key permissions**
   - In Mailchimp, limit key to campaign creation only
   - Don't grant billing or account management access

3. **Store keys securely**
   - Use password manager for backup
   - Rotate keys periodically

4. **Review before sending**
   - Always check preview link
   - Confirm recipient list
   - Test email to yourself first

---

## Troubleshooting

### "Invalid API Key"
- Check server prefix matches API key (e.g., `us19`)
- Verify key is active in Mailchimp settings

### "Resource Not Found"
- Audience ID might be wrong
- Check ID in Mailchimp → Audience → Settings

### "Forbidden"
- API key lacks required permissions
- Generate new key with campaign access

### Newsletter formatting issues
- Ensure HTML is valid
- Test with Mailchimp's email preview tool
- Check mobile rendering

---

## Next Steps

1. **Choose integration option** (A, B, or C)
2. **Gather credentials** (API key, Audience ID, reply-to email)
3. **Test with draft campaign** (don't send to full list initially)
4. **Document Tiff's preference** (schedule vs immediate send)
5. **Update newsletter workflow docs** to include distribution step

---

## Questions to Answer

Before implementing, clarify:

- **Which option fits Tiff's workflow best?**
- **Default send time?** (e.g., Thursdays 10am PT)
- **Segment audience?** (all subscribers vs specific groups)
- **Test sends?** (should GPT/script send test to Tiff first?)
- **HTML template?** (plain text + basic styling vs Mailchimp template)

---

**Last Updated:** November 3, 2025
