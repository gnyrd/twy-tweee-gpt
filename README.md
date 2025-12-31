<!-- Copyright © 2025 Ninsim, Inc. All rights reserved. -->

# twy-tweee-gpt

TWEEE: A custom GPT system for Tiffany Wood Yoga newsletter generation and class planning.

---

## 📚 Documentation

### Core Files (STATUS-FEATURES-HISTORY System)
Start here to understand the project:

- **[STATUS.md](STATUS.md)** - Current system state and health
- **[TASKS.md](TASKS.md)** - Work in progress (1-4 weeks)
- **[FEATURES.md](FEATURES.md)** - Future plans and roadmap
- **[HISTORY.md](HISTORY.md)** - Completed milestones and decisions
- **[TIME.md](TIME.md)** - Time spent and effort breakdown

### Detailed Guides

- **[docs/guides/TWEEE-GPT-INSTRUCTIONS-CONDENSED.md](docs/guides/TWEEE-GPT-INSTRUCTIONS-CONDENSED.md)** - GPT system prompt (use this for OpenAI)
- **[docs/guides/TWEEE-GPT-INSTRUCTIONS.md](docs/guides/TWEEE-GPT-INSTRUCTIONS.md)** - Full GPT instructions (reference)
- **[docs/guides/GPT_SETUP_GUIDE.md](docs/guides/GPT_SETUP_GUIDE.md)** - OpenAI configuration
- **[docs/guides/GPT_ACTION_SETUP.md](docs/guides/GPT_ACTION_SETUP.md)** - Mailchimp GPT Actions
- **[docs/guides/MAILCHIMP_INTEGRATION.md](docs/guides/MAILCHIMP_INTEGRATION.md)** - Distribution system
- **[WARP.md](WARP.md)** - Documentation index

### Knowledge Base

- `knowledge/` - GPT training materials (upload to ChatGPT)
  - NEWSLETTER_VOICE_TRAINING.pdf - 15 curated newsletters (113MB)
  - TIFFS_EVOLUTION.md - Voice timeline (2024 → 2025)
  - COMBINED_TRAINING_GUIDE.md - Complete voice/philosophy guide
  - 6 philosophy books (960 pages)
  - 5 newsletter system guides
  - 3 Anusara teaching materials (RTF)

### Archives

- `docs/archive/` - Historical documents and superseded guides

---

## 🚀 Quick Start

1. **Understand current state:** Read [STATUS.md](STATUS.md)
2. **See what's planned:** Check [TASKS.md](TASKS.md) and [FEATURES.md](FEATURES.md)
3. **Configure GPT:** Follow [docs/guides/GPT_SETUP_GUIDE.md](docs/guides/GPT_SETUP_GUIDE.md)
4. **Setup Mailchimp:** Follow [docs/guides/MAILCHIMP_INTEGRATION.md](docs/guides/MAILCHIMP_INTEGRATION.md)

---

## 📁 Project Structure

```
twy-tweee-gpt/
├── STATUS.md, TASKS.md, FEATURES.md, HISTORY.md, TIME.md  # Core docs
├── WARP.md                                                 # Index + AI rules
├── README.md                                               # This file
├── config.json                                             # GPT configuration
├── .mailchimp.env                                          # Local credentials (gitignored)
│
├── docs/
│   ├── guides/                                             # Detailed setup guides
│   │   ├── TWEEE-GPT-INSTRUCTIONS.md
│   │   ├── GPT_SETUP_GUIDE.md
│   │   ├── GPT_ACTION_SETUP.md
│   │   └── MAILCHIMP_INTEGRATION.md
│   └── archive/                                            # Superseded documentation
│
├── knowledge/                                              # GPT training materials
│   ├── *.pdf                                               # Newsletters + philosophy books
│   ├── NEWSLETTER_GPT_PROMPTS.md
│   ├── NEWSLETTER_INPUT_TEMPLATES.md
│   ├── NEWSLETTER_QUALITY_CHECKLIST.md
│   └── ... (6 more training files)
│
├── sources/                                                # Raw materials (not uploaded)
│   └── TWY Newsletters/
│       ├── 2024/ (66 newsletters)
│       └── 2025/ (48 newsletters)
│
└── .gitignore, .gitattributes, .mailchimp.env             # Configuration
```

---

## 🔄 Maintenance

- **Daily:** Update TASKS.md when starting/completing work
- **Weekly:** Review priorities, migrate completed items to HISTORY.md
- **Monthly:** Update STATUS.md "Last Verified" date
- **Quarterly:** Audit documentation for staleness

See [WARP.md](WARP.md) for complete maintenance schedule and AI agent rules.
