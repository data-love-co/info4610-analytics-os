---
name: ingest-data
description: >
  Standardizes raw files so the chain skills can read them. Triggers when the user says "ingest my
  data", "process my files", "standardize this spreadsheet", "I dropped a PDF in there", drops
  files into 5_Library/sources/raw/, or in session L1.1. Converts every raw file — spreadsheet
  exports, survey results, meeting notes, transcripts, policy documents, ticket dumps, PDFs, slide
  decks — into clean markdown or CSV in 5_Library/sources/processed/, files them with frontmatter,
  and reports what exists, what's thin, and what's ready for the chain.
---

# ingest-data — Raw → Processed

You are standardizing files into the format every chain skill reads. Work file by file. Preserve
the evidence — never summarize away the user's raw material.

## The confidentiality gate — do this first, every time

`5_Library/sources/raw/` is gitignored. `5_Library/sources/processed/` **is tracked in git**.
Ingestion is the moment data moves from private to shareable, so it's the moment to check.

Before converting anything, look at what's in `raw/` and ask yourself: does this contain customer
names, employee names, account numbers, email addresses, salary figures, health information, or
anything under NDA? If it might:

1. **Say so specifically.** "This export has a `customer_email` column and full names in
   `contact_name`." Name the columns; don't give a general warning.
2. **Offer the three options:** drop the identifying columns during conversion, replace them with
   stable anonymous IDs, or leave the file in `raw/` and work from it there without producing a
   tracked copy.
3. **Do what they choose, and record it** in the processed file's frontmatter
   (`redactions: dropped customer_email, contact_name`) so the decision is visible later.

Never quietly copy identifying data into `processed/`.

## The convention

- **`5_Library/sources/raw/`** — input. Anything, any format (xlsx, csv, docx, pdf, pptx, txt, md,
  exported chats, photos of a whiteboard). Subfolders welcome — the layout is mirrored into
  `processed/`. Gitignored; never modified by this skill.
- **`5_Library/sources/processed/`** — output. Clean markdown, or CSV for tabular data, mirroring
  the `raw/` layout. This is the single place chain skills look. Tracked in git.

## Step 1 — Inventory

List every file in `5_Library/sources/raw/`. For each, identify what it is and which use case it
could feed. Ask only when a file's nature is genuinely unclear.

Common arrivals and where they go:

| What it is | Feeds |
|---|---|
| Monthly or weekly metrics export | `kpi-dashboard`, `forecast` |
| Customer/account list with an outcome column | `risk-scorer` |
| Experiment or campaign results | `ab-test-readout` |
| Survey export with open-ended columns | `feedback-synthesizer` |
| Meeting notes, transcript, recording summary | `meeting-to-actions` |
| Policy manual, onboarding doc, SOP, FAQ | `knowledge-assistant` |
| Cost/rate/capacity assumptions | `scenario-calculator` |

## Step 2 — Run the tiered converter

Office documents and PDFs can't be read by plain file tools, so a converter does the extraction.
It auto-detects the best engine installed (Docling → MarkItDown → stdlib for text/CSV) and mirrors
`raw/` subfolders into `processed/`:

```bash
python 0_System/scripts/parse-sources.py
```

The script **never installs anything.** For files it can't convert it writes a `status: stub`
placeholder naming the exact install command. After it runs:

- **Converted files** — a mechanical first pass. Refine in Step 3.
- **Stubbed PDFs / images** — read the file yourself and replace the stub with real content. No
  install needed.
- **Stubbed Office docs (docx/pptx/xlsx)** — surface the install command
  (`pip install "markitdown[docx,pptx,xlsx]"`), let the user run it, then re-run the converter.
  **Never install it yourself.** If they can't install on a work laptop, offer the fallback: save
  the file as CSV or plain text from Excel/Word and re-drop it.
- **Stubbed audio/video** — ask for a transcript, or point at `pip install faster-whisper`.

## Step 3 — Refine each file

Turn the converter's first pass into the house convention: one processed file per raw source,
semantic name, proper frontmatter. Full naming table and frontmatter spec:
[reference/naming-and-frontmatter.md](reference/naming-and-frontmatter.md).

**Tabular data stays tabular.** A spreadsheet export becomes a CSV in `processed/`, not a markdown
table — the analysis skills need to compute on it. Convert to markdown only when the content is
genuinely prose.

**Do not clean the data here.** This step standardizes *format*, not *content*. Blanks, duplicates,
weird dates, and outliers stay exactly as they are — auditing and cleaning them is the `data-audit`
skill's job, and it produces a log of what changed. An undocumented clean during ingestion is the
kind of thing that quietly breaks a number three weeks later.

**Keep verbatim text verbatim.** Open-ended survey responses, interview quotes, and meeting
statements are the raw material for later analysis. Don't paraphrase them.

## Step 4 — Confirm the tree

No index to maintain — the chain reads `5_Library/sources/processed/` directly. List the resulting
tree so the user sees what landed where, with row counts and column names for anything tabular.

## Step 5 — Report: what you have, what's thin

End with a short readiness report in chat:

1. **What you have** — by type and size ("one 4-year monthly sales export, 195 rows, 7 columns; one
   survey, 240 responses with an open-ended column")
2. **What's thin** — gaps that will constrain specific use cases ("no outcome column, so
   `risk-scorer` has nothing to learn from"; "18 months of history — enough for trend, thin for
   seasonality")
3. **What it's ready for** — name the use-case skills this data can actually support, and the ones
   it can't
4. **What was redacted**, if anything

Then fold what exists into ground truth via `util_get_org_info` (`set(04_Data, …)`) — a short
inventory of what data is on hand and where it came from, under a `## Available Data` header.

## Guardrails

- Never modify or delete anything in `5_Library/sources/raw/`.
- **Never install or upgrade a converter yourself.** Surface the command; the user decides what
  goes on their machine.
- **Never copy identifying data into `processed/` without an explicit decision.** See the
  confidentiality gate above.
- **Never clean during ingestion.** Format only. Cleaning belongs to `data-audit`, with a log.
- Never send data to external services — all processing is local.
- Don't editorialize about the user's organization in processed files.
