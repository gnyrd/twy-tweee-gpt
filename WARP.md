<!-- Copyright © 2025 Ninsim, Inc. All rights reserved. -->

# WARP.md - Documentation Index

**Last Updated:** 2025-12-27  
**Version:** v2.6

---

## 🚀 Start Here

This repository contains a custom GPT system (TWEEE) for Tiffany Wood Yoga: newsletter generation and distribution.

**Choose your starting point:**

| Need | File | Purpose |
|------|------|----------|
| **What's happening now?** | [STATUS.md](STATUS.md) | Current system state, health, recent changes |
| **What should I work on?** | [TASKS.md](TASKS.md) | Near-term work (1-4 weeks), priorities |
| **What's planned?** | [FEATURES.md](FEATURES.md) | Future plans and strategic roadmap |
| **What's been done?** | [HISTORY.md](HISTORY.md) | Completed milestones, technical decisions |

---

## 📋 Core System

### Newsletter Generation Workflow
- **Quick Capture** (5-10 min): Tiff provides seed content
- **AI Generation** (automated): GPT creates in Tiff's voice using templates
- **Refinement** (10-15 min): Tiff reviews, iterates, approves
- **Total time:** 15-25 minutes (vs. 60-90 min previously)

**Key resources:**
- `NEWSLETTER_INPUT_TEMPLATES.md` — 5 template types for quick capture
- `NEWSLETTER_GPT_PROMPTS.md` — Generation instructions
- `NEWSLETTER_QUALITY_CHECKLIST.md` — 10-point voice verification
- `NEWSLETTER_WORKFLOW_GUIDE.md` — Complete workflow documentation
- `NEWSLETTER_REFINEMENT_PATTERNS.md` — Common iteration patterns

### Newsletter Distribution System
- **Mailchimp API integration** with GPT Actions
- **Test environment** (2 contacts) for safe iteration
- **Production environment** (880 subscribers) ready to send
- **Python CLI tool** (`send_to_mailchimp.py`) for local testing

**Key resources:**
- `send_to_mailchimp.py` — CLI tool for campaign creation
- `switch_mailchimp_env.sh` — Switch between test/prod
- `.env.mailchimp.test` & `.env.mailchimp.prod` — Configuration files
- `mailchimp_gpt_action.json` — GPT Actions schema

### GPT Configuration
- **Dual-mode system:** Collaborate FOR Tiff or speak AS Tiff
- **Voice training corpus:** 15 newsletters + 7 philosophy books + analysis docs
- **Philosophy:** Non-dual Tantra, Anusara Yoga, goddess archetypes, householder path

**Key resources:**
- `INSTRUCTIONS.md` — System prompt for GPT configuration
- `knowledge/` — All training materials (upload to GPT)
- `GLOSSARY_AND_CONCEPTS.md` — Philosophical reference
- `GPT_TRAINING_PATTERNS.md` — Voice patterns and templates

---

## 📁 Repository Structure

```
TWEEE_gpt/
├── STATUS.md                          # Current state & health
├── TASKS.md                           # Work in progress (1-4 weeks)
├── FEATURES.md                        # Strategic roadmap
├── HISTORY.md                         # Completed milestones
├── WARP.md                            # This file
│
├── INSTRUCTIONS.md                    # GPT system prompt
├── NEWSLETTER_*.md                    # Newsletter system docs (5 files)
├── mailchimp_gpt_action.json          # GPT Actions schema
├── send_to_mailchimp.py               # Mailchimp CLI tool
├── switch_mailchimp_env.sh            # Environment switcher
├── .env.mailchimp.test                # Test configuration
├── .env.mailchimp.prod                # Production configuration
│
├── knowledge/                         # GPT training materials (upload these)
│   ├── 01_When_Everything_Falls_Away.pdf
│   ├── 02_Householder_Yogis_Know_Better.pdf
│   ├── ... (13 more curated newsletters)
│   ├── ANALYSIS_SUMMARY.md
│   ├── GLOSSARY_AND_CONCEPTS.md
│   ├── GPT_TRAINING_PATTERNS.md
│   ├── README.md
│   └── ... (7 philosophy books)
│
├── sources/                           # Raw materials (not uploaded)
│   └── TWY Newsletters/
│       ├── 2024/ (66 newsletters)
│       └── 2025/ (48 newsletters)
│
├── config.json                        # Project configuration
├── CHANGELOG.md                       # Detailed changelog
└── .gitignore
```

---

## 🔑 Key Metrics

| Metric | Current | Baseline | Improvement |
|--------|---------|----------|----------|
| Newsletter creation time | 15-25 min | 60-90 min | 78-86% faster |
| Voice authenticity | 8.5/10 avg | N/A | Consistently high |
| Quality checklist pass rate | 95% | N/A | Reliable |
| Time to send | 5-10 min | 20-30 min | 60-75% faster |
| Training corpus | 133MB | N/A | Comprehensive |

---

## 🎯 Current Status

- ✅ Newsletter generation system: Fully validated
- ✅ Mailchimp integration: Complete with test environment
- ✅ GPT configuration: Ready for OpenAI setup
- ⏳ First production newsletter: Pending (see TASKS.md)
- 💡 Analytics dashboard: Planned

**Next major milestone:** Send first production newsletter to 880 subscribers.

---

## 📖 For AI Agents

**When you see questions about this project:**

- "What's the current status?" → Check `STATUS.md`
- "What should I work on?" → Check `TASKS.md` (see "Next Up" section)
- "What's planned?" → Check `FEATURES.md`
- "What's been done?" → Check `HISTORY.md`
- "How does the workflow work?" → Check `NEWSLETTER_WORKFLOW_GUIDE.md`
- "Is feature X working?" → Check `STATUS.md` (Active Components)
- "What's blocking progress?" → Check `TASKS.md` (Blocked section)

**Rules:**
1. Always read STATUS.md first to understand current state
2. Check TASKS.md before suggesting work (avoid duplicates)
3. When work completes: update TASKS.md (mark ✅), add to STATUS.md (Recent Changes)
4. After 30 days: migrate completed items from TASKS.md to HISTORY.md
5. Minor refactoring/internal changes need NO documentation update

---

## 🔄 Maintenance Schedule

- **Daily:** Update TASKS.md when starting/completing work
- **Weekly:** Review TASKS.md priorities, migrate old ✅ items to HISTORY.md
- **Monthly:** Update STATUS.md "Last Verified" date, review FEATURES.md
- **Quarterly:** Audit all docs for staleness, reorganize as needed

---

## 🎓 Historical Context

This project evolved through 5 sessions:

1. **Session 1 (2025-10-29):** Initial repository setup
2. **Session 2 (2025-10-29):** Analyzed 114 newsletters, curated training corpus
3. **Session 3 (2025-10-30):** Created unified GPT instructions
4. **Session 4 (2025-11-01):** Built newsletter generation workflow (78-86% time savings)
5. **Session 5 (2025-11-03):** Built Mailchimp integration (end-to-end distribution)
6. **Session 6 (2025-11-18):** Implemented STATUS/FEATURES/HISTORY documentation system

Full details available in `HISTORY.md`.

---

**System Status:** 🟢 All Systems Operational  
**Last Verified:** 2025-12-27
