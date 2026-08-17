---
name: find-skills
description: >
  Locates the right skill across all buckets. Trigger when the user asks:
  "what skills are available", "which skill should I use", "find a skill",
  "what can you do", "show me the skills", "what's in this system", "I have a spreadsheet,
  now what", "which use case fits my problem", or otherwise wants to know what exists and which
  one to reach for next.
---

# find-skills — Skill Finder

The entry point for the Analytics OS skill catalog. When someone asks what's available, or isn't
sure which skill to run next, this skill finds the right one by reading the skills **on disk** —
each `SKILL.md` frontmatter is the source of truth for what that skill does and when it fires.

---

## How to find and route (the procedure)

1. **List what exists.** Glob `.agents/skills/**/SKILL.md` and read each file's frontmatter `name`
   + `description`. The `description` spells out exactly when that skill should fire — match the
   user's ask against it. Do this every time; do not rely on a list kept inside this file.
2. **Respect enabled state.** Read `.agents/skills/skills.json` — a slim registry of
   `{name, path, enabled}`. Skip any skill marked `enabled: false`. A skill that exists on disk but
   is missing from the registry is treated as **enabled** (the registry just hasn't been
   regenerated yet — it never overrides what's on disk).
3. **Route.** Point the user to the best-matching skill. If two plausibly fit, name both and ask
   which they want.

> **Why disk-first:** `skills.json` stores only enabled flags — never descriptions — so it cannot go
> stale against the real skills. The directory is always the truth; the registry just says what's
> turned off. If the registry looks out of date, regenerate it:
> `python 0_System/scripts/scan-skills.py`.

---

## Routing by what the user actually says

People rarely ask for a skill by name. They describe a mess. Match on the shape of the problem:

| What they say | Where to send them |
|---|---|
| "I have a decision to make and no idea where to start" | `frame-the-decision` — always start here |
| "This spreadsheet is a disaster" | `data-audit` |
| "Leadership wants a dashboard" / "what are our numbers" | `kpi-dashboard` |
| "What happens if we raise price / add headcount / cut budget" | `scenario-calculator` |
| "What will next quarter look like" | `forecast` |
| "Which customers are we about to lose" / "who's likely to convert" | `risk-scorer` |
| "We ran a test and I don't know if it worked" | `ab-test-readout` |
| "I have 400 survey comments" | `feedback-synthesizer` |
| "I need to write this up for the VP" | `decision-memo` |
| "I have meeting notes and no follow-up" | `meeting-to-actions` |
| "People keep asking me questions that are answered in a document" | `knowledge-assistant` |
| "Where do I actually build this thing" | `build-and-ship` |

**The most common routing mistake** is sending someone straight to a use-case skill when they
haven't framed the decision. If the user can't say what decision the analysis informs, route them
to `frame-the-decision` first, even if they asked for a dashboard. It takes fifteen minutes and it
is the difference between a chart and an answer.

---

## How skills are organised

Skills live in buckets under `.agents/skills/`:

- **`find-skills/`** — this finder (you are here); always available.
- **`daniels/`** — the course chain, numbered in run order (`1-…` → `14-…`). Read the folder names
  and each `SKILL.md` description (step 1) for the current set and what each does.
  - **`daniels/util_/`** — file-access utilities (`util_get_user_info`, `util_get_org_info`,
    `util_get_inputs`) that own the `0_User/` / `0_Org/` file contracts and the central input
    lookup. Mostly invoked BY other skills — but `util_get_user_info` and `util_get_org_info` are
    also the direct path when someone wants to view or update their own profile or work context.
- **anything else** — general or third-party skills added over time.

That's the stable structure. The specific skills, their order, and their triggers come from the
`SKILL.md` files themselves (step 1) — not from a catalog maintained here, which would drift.
