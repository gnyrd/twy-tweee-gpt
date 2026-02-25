# TWY Class Plan Format

This document defines every field in a class plan and how to populate it correctly.
Tweee uses this as the authoritative reference when drafting or updating plans.

---

## Fields

### `date`
**Format:** `YYYY-MM-DD`
The date of the class. This is also the file key — only one plan per date (append `-2` if needed).
**Example:** `2026-03-01`

---

### `time`
**Format:** `HH:MM` (24-hour)
Scheduled start time.
**Defaults by day of week:**
- Monday → `17:30`
- Tuesday → `08:00`
- Thursday → `08:00`
- Saturday → `09:00`

---

### `duration`
**Format:** integer (minutes)
Common values: `60`, `75`, `90`.
**Defaults:** Mon/Tue/Thu → `60`, Sat → `90`

---

### `class_type`
One of the following exact strings:
- `Strength`
- `Stretch`
- `Flow`
- `Principles of Anusara®`
- `Dynamic Flow`
- `Slow Flow`
- `Expansion`
- `Meditation`
- `Integration`
- `Final Integration`

---

### `title`
Short, evocative class name. 2–5 words. Poetic or thematic.
**Example:** `"No Strain"`, `"Root and Rise"`, `"Open the Gates"`

---

### `subtitle`
Optional thematic expansion of the title. Often uses `~` as a separator.
**Example:** `"Rooted Rhythm ~ Sacred Vessel of Strength"`

---

### `description`
Maximum 3 sentences. Describes what the class explores, the arc, and the takeaway.
Written in third person, present tense.
**Example:**
> This class explores Muscular Energy as the primary means of creating sustainable strength.
> Students move from standing balance into asymmetrical hip and hamstring preparation.
> The emphasis is on intelligent containment before depth.

---

### `affirmation`
A first-person present-tense statement aligned with the class theme.
**Example:** `"I organize my strength and bear only what is mine to carry."`

---

### `energetic_pulse`
The energetic action or quality that animates the class. Usually a short phrase.
**Example:** `"Hug to Center then Expand with Integrity"`

---

### `apex_pose`
The peak pose or pose family the class builds toward.
**Example:** `"Akarna Pidasana and Vasisthasana (Tree Leg Variation)"`

---

### `physical_arc`
A single paragraph describing the physical sequence arc: how the class opens, builds, and closes.
Covers warming, preparation, peak, and integration/restoration.

---

### `upas_key_actions`
The Universal Principles of Alignment (UPAs) or key physical actions featured. Comma-separated or short list.
**Example:** `"Open to Grace; Muscular Energy — Hug periphery to core before expansion"`

---

### `level`
Comma-separated string. Valid values: `Fundamentals`, `1`, `2`
- `Fundamentals` — beginner-friendly, foundational
- `1` — some experience recommended
- `2` — intermediate
**Example:** `"1,2"` or `"Fundamentals"` or `"2"`

---

### `categories`
Array of strings. Choose all that apply from this exact list:
- `Heart Openers & Backbend Strategies`
- `Upper Body Strength & Arm Balances`
- `Hip Openers`
- `Forward Folds & Twists`
- `Core Strength`
- `Slow Flow`
- `Flow`
- `Meditation`
- `Therapy`
- `Integration: Deepening Basics Anusara®`

---

### `props`
Comma-separated list of props. Default: `"mat, 2 blocks, 1 strap, 1-2 blankets"`
Adjust only if the class needs something different (e.g. chair, wall).

---

### `opening_story`
A short narrative (1–3 paragraphs) that grounds the class theme philosophically or poetically.
Tiffany reads or riffs on this at the start of class. Should connect to the title, affirmation, and energetic pulse.

---

### `closing_reflection`
A short closing passage (1–3 paragraphs) Tiffany offers at the end of class — during Savasana or as students are settling.
Should echo the class theme, land the affirmation, and leave students with a sense of completion and integration.

---

### `notes`
Free-form internal notes. Not displayed publicly. Used for reminders, cues, or variations.

