---
name: util_get_org_info
description: >
  The single read/write path for the work context — organizational ground truth every skill reads
  before it runs. Triggers when the user says "update my org info", "what do you know about my
  company", "update how we measure that", "our team reorganized", "add my stakeholders", "log what
  I learned", or any correction to organizational facts. Also invoked by chain skills
  (3-frame-the-decision, 4-data-audit, the use-case skills, 13-decision-memo) to read ground truth
  before running and to fold distilled essence back in after producing output. That compounding —
  each skill reading the latest ground truth, then writing its essence back — is what lets the
  chain run across sessions without re-explaining context. All reads and writes go through this
  skill; no other skill touches 0_Org/ directly.
---

# util_get_org_info — Organizational Ground Truth

You are the sole gatekeeper for `0_Org/`. Every skill reads work context through you before it
runs, and writes its distilled essence back through you after. Essence only — full work products
go to `2_Outputs/.agents/<session>/`, not here.

## Why this matters

Each chain skill reads `0_Org/` before it runs, so it starts with full context rather than the
last message. After producing output, each skill folds a short essence back in via `set()`. The
next skill picks up richer ground truth than the one before it. This is what turns a set of
disconnected exercises into one coherent piece of work.

## The folder contract

`0_Org/` holds facts about the organization and the work — what it does, who decides, what it
measures, what data exists. Personal facts about the user never go here; those belong in `0_User/`
via `util_get_user_info`.

```
0_Org/
├── 01_Overview.md       # the organization, the unit, what it does, for whom
├── 02_Decisions.md      # decisions in play, who owns each, what a decision costs to get wrong
├── 03_Metrics.md        # what the org measures, how each metric is defined, who reports it
├── 04_Data.md           # systems of record, what data exists, access, sensitivity
├── 05_Stakeholders.md   # who the analysis is for, and what each one actually cares about
├── 06_Constraints.md    # policy, privacy, budget, timing, political constraints
├── 07_Insights.md       # running takeaways across the sessions, dated
└── Z_Library.md         # deeper detail; referenced by file name + section header
```

The folder starts empty. Bootstrap seeds it from the onboarding interview via `set()`. Chain skills
fold essence back in via `set()` after each exercise.

## Seeded-by and essence map

| File | Seeded by | Chain essence folds in |
|---|---|---|
| `01_Overview.md` | bootstrap (L1.1) | — |
| `02_Decisions.md` | bootstrap | `3-frame-the-decision` (the decision statement) |
| `03_Metrics.md` | bootstrap | `5-kpi-dashboard` (the metric set + definitions) |
| `04_Data.md` | bootstrap | `2-ingest-data`, `4-data-audit` (what exists, what's trustworthy) |
| `05_Stakeholders.md` | bootstrap | `3-frame-the-decision` (the audience), `13-decision-memo` |
| `06_Constraints.md` | bootstrap | any skill that hits a constraint worth remembering |
| `07_Insights.md` | — | running takeaways from any chain skill |
| `Z_Library.md` | — | deep detail routed from any topic file |

## Interface

These are the only entry points. No skill reads or writes `0_Org/` any other way.

### get()

Read and return the whole folder in one pass — each file `01_Overview.md` through
`07_Insights.md` plus `Z_Library.md`. Skip missing files silently.

### get(file)

Read and return the named topic file (e.g. `get(03_Metrics)`). If it doesn't exist yet, return
empty and note that it hasn't been created.

### set(file, essence)

Write distilled essence into a topic file or section. **Never write full work products here.**
Full outputs — `Decision-Frame.md`, `Data-Audit.md`, `Decision-Memo.md` — live in
`2_Outputs/.agents/<session>/` with Title-Case filenames.

1. If the file doesn't exist, create it with `essence` as the full body.
2. If it exists, read it first. Locate the section matching `essence`'s top-level `##` or `###`
   header. Replace that section in place, leaving other sections intact. If no matching header
   exists, append as a new section.
3. If the incoming content runs long (more than ~40 lines) or is too detailed for a concise topic
   file, route the detail into `Z_Library.md` under a `##` header named for the topic, and write a
   short summary in the topic file with a note: `→ see Z_Library.md § <section>`.
4. After writing, read the file back and confirm the result looks correct before returning.

## Step-by-step: reading ground truth

1. Read each topic file that exists in `0_Org/`.
2. Return the contents cleanly, grouped by file heading. Do not editorialize.
3. If a topic file is missing or empty, note the gap so the calling skill knows what's absent.

## Step-by-step: folding essence back in

1. Identify which topic file(s) the essence belongs to (use the map above).
2. Distill to core facts — one to three short paragraphs.
3. Call `set(file, essence)`.
4. Read the file back. Confirm the update in one short sentence before returning.

## Topic guide

| File | What goes here |
|---|---|
| `01_Overview.md` | Organization, industry, size, the unit the user works in, what it's responsible for |
| `02_Decisions.md` | Decisions in play, who owns each, the cadence they're made on, cost of being wrong |
| `03_Metrics.md` | Metric names **and their definitions** — including where two teams define the same metric differently |
| `04_Data.md` | Systems of record (CRM, ERP, ticketing, HRIS), what each holds, how the user gets an extract, sensitivity level |
| `05_Stakeholders.md` | Audience by name or role, what each cares about, how much detail each wants |
| `06_Constraints.md` | Privacy and policy limits, budget, timing, approvals, known political sensitivities |
| `07_Insights.md` | Running takeaways — one dated bullet per insight |
| `Z_Library.md` | Extended background, long metric definitions, anything too long for a topic file |

## Guardrails

- Organizational facts only — never write personal facts about the user into `0_Org/`. Those
  belong in `0_User/` via `util_get_user_info`.
- **Never write confidential detail that shouldn't be in a tracked file.** `0_Org/` is tracked in
  git. Customer names, employee names, account numbers, salary figures tied to a person, anything
  under NDA — leave it out, or write the shape of it without the identifying detail. Ask the user
  when it's a close call.
- Never write full work products here. Only distilled essence.
- Keep each topic file short and skimmable. Push length into `Z_Library.md`.
- Metric definitions matter more than metric names. When the user says "we track retention," find
  out what they mean by it — logo, revenue, seat, gross, net — and write the definition down.
- Always read the file back after writing and confirm before returning.
- Never send the user's data to external services — all reads and writes are local.
