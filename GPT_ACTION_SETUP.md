# GPT Action Setup Guide - Mailchimp Integration

## Overview
Configure your TWEEE Custom GPT to send newsletters directly to Mailchimp.

---

## Step 1: Open Your Custom GPT

1. Go to ChatGPT: https://chatgpt.com
2. Click your profile → **My GPTs**
3. Find your TWEEE GPT and click **Edit**

---

## Step 2: Add the Mailchimp Action

1. In the GPT editor, click **Actions** (in the left sidebar)
2. Click **Create new action**
3. Copy the entire contents of `mailchimp_gpt_action.json` 
4. Paste into the Schema field
5. Click **Save**

**Quick copy command:**
```bash
cat mailchimp_gpt_action.json | pbcopy
```

---

## Step 3: Configure Authentication

1. In the Action settings, scroll to **Authentication**
2. Set **Authentication Type:** `Basic Auth`
3. Enter credentials:
   - **Username:** `anystring` (Mailchimp ignores this, but it's required)
   - **Password:** `REDACTED_API_KEY`
4. Click **Save**

---

## Step 4: Update Instructions

Add this to your GPT's Instructions (in the **Configure** tab):

```markdown
## Mailchimp Distribution

When user says "send to Mailchimp" or "create campaign":

### Workflow:
1. **Confirm newsletter is finalized** - Ask if content is ready
2. **Gather details:**
   - Subject line (extract from newsletter if present)
   - Preview text (50-100 chars, enticing hook from opening)
   - Audience choice: Test (e1cfd6e694) or Production (TBD)
3. **Create campaign** using `createCampaign` action:
   - List ID: Default to test audience `e1cfd6e694`
   - From name: "Tiff"
   - Reply-to: "newsletters@tiffanywoodyoga.com"
   - Title: "Newsletter - [Date]"
4. **Upload content** using `setCampaignContent` action:
   - Convert newsletter to clean HTML
   - Wrap in basic email template if needed
5. **Provide preview link:**
   - Format: `https://us21.admin.mailchimp.com/campaigns/edit?id={web_id}`
   - Tell user to review before sending
6. **Ask before sending:**
   - "Would you like to send now, or review in Mailchimp first?"
   - Only call `sendCampaign` if user explicitly confirms

### Default Settings:
- **Test Audience ID:** `e1cfd6e694` (2 test contacts)
- **Production Audience ID:** (to be configured)
- **From Name:** "Tiff"
- **Reply-To:** "newsletters@tiffanywoodyoga.com"
- **Server:** us21

### Safety Checks:
- ✅ Always show preview link before sending
- ✅ Confirm send action explicitly ("yes" or "send now")
- ✅ Never auto-send without user confirmation
- ✅ Default to test audience unless user specifies production
- ✅ Validate HTML is properly formatted

### HTML Email Template:
If newsletter is plain text, wrap in this basic template:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Newsletter</title>
</head>
<body style="font-family: Georgia, serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
    [NEWSLETTER CONTENT HERE]
</body>
</html>
```

### Error Handling:
- If campaign creation fails: Show error, suggest checking Mailchimp
- If "recipients not ready": Audience has 0 contacts, ask user to add contacts first
- If send fails: Campaign saved as draft, provide link to review

### Example Conversation:

**User:** "Send this to Mailchimp"

**GPT:** "Great! Let me prepare this newsletter for Mailchimp.

📧 **Subject line:** [extracted or ask]
👀 **Preview text:** [suggest from opening or ask]
🎯 **Audience:** Test (2 contacts) or Production?

Ready to create the campaign?"

**User:** "Yes, test audience"

**GPT:** [calls createCampaign, then setCampaignContent]

"✅ Campaign created successfully!

🔗 **Preview:** [Mailchimp link]

The newsletter is ready to send to the test audience (2 contacts). Would you like to send it now, or review it in Mailchimp first?"

**User:** "Send now"

**GPT:** [calls sendCampaign]

"📤 Newsletter sent! Check your test inbox shortly."
```

---

## Step 5: Test the Action

### Test in GPT Editor:
1. Click **Test** (top right in Actions panel)
2. Try creating a test campaign:
```json
{
  "type": "regular",
  "recipients": {
    "list_id": "e1cfd6e694"
  },
  "settings": {
    "subject_line": "GPT Action Test",
    "preview_text": "Testing integration",
    "title": "Newsletter - GPT Test",
    "from_name": "Tiff",
    "reply_to": "newsletters@tiffanywoodyoga.com"
  }
}
```
3. Should return campaign ID and web_id

### Test in Conversation:
1. Click **Preview** (top right in GPT editor)
2. Say: "Create a test newsletter and send to Mailchimp"
3. Follow the prompts
4. Verify campaign appears in Mailchimp

---

## Step 6: Configure Production Audience

**When ready to use real subscriber list:**

1. Get production Audience ID from Mailchimp:
   - Go to **Audience** → [Your main list]
   - **Settings** → **Audience name and defaults**
   - Copy the Audience ID

2. Update GPT Instructions with production ID

3. Update `.env.mailchimp.prod` locally:
```bash
MAILCHIMP_AUDIENCE_ID="[production_id_here]"
```

4. Tell GPT to use production audience when sending real newsletters

---

## Conversation Starters

Add these to your GPT (in **Configure** tab):

1. "Help me create a newsletter for TWY community"
2. "Send this newsletter to Mailchimp"
3. "Create a test campaign"
4. "What's the newsletter workflow?"

---

## Troubleshooting

### "Action failed: 401 Unauthorized"
- Check API key is correct in Authentication settings
- Verify Basic Auth is selected (not OAuth)

### "Action failed: 400 Bad Request - recipients not ready"
- Test audience has 0 contacts
- Add at least one email to the test audience in Mailchimp

### "Schema validation error"
- Copy `mailchimp_gpt_action.json` exactly as-is
- Verify JSON is valid (no extra commas, brackets match)

### Campaign created but not appearing in conversation
- Check **Available Actions** in GPT settings
- Make sure action is enabled
- Try "Test" button in Actions panel first

---

## Security Notes

🔒 **API Key Storage:**
- Stored encrypted by OpenAI
- Only accessible to your GPT
- Not exposed in conversations

🔒 **Best Practices:**
- Use test audience for all testing
- Review preview link before every send
- Never auto-send without confirmation
- Rotate API keys periodically

---

## Complete! 🎉

Your TWEEE GPT can now:
1. ✅ Create newsletters with Tiff's voice
2. ✅ Send directly to Mailchimp
3. ✅ Manage test vs production audiences
4. ✅ Provide preview links for review
5. ✅ Send campaigns with user confirmation

**Total workflow time:** 17-30 minutes (vs 60-90 previously)

---

**Last Updated:** November 3, 2025
