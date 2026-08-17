# Processed file naming, frontmatter & conversion rules

Refine the converter's output (and any files you read directly) into this convention — one
processed file per raw source. Merge only trivial fragments.

## Naming

| What it is | Processed filename |
|---|---|
| Metrics / analytics export | `metrics-<subject>-<YYYY.MM>.csv` |
| Customer or account list | `accounts-<source>-<YYYY.MM>.csv` |
| Experiment or campaign results | `experiment-<name>.csv` |
| Survey results | `survey-<topic>-<YYYY.MM>.csv` |
| Open-ended text extracted from a survey | `survey-<topic>-openends.csv` |
| Meeting notes or transcript | `notes-<topic>-<YYYY.MM.DD>.md` |
| Policy, SOP, handbook, onboarding doc | `policy-<topic>.md` |
| Research or market document | `research-<topic>.md` |
| Cost, rate, or capacity assumptions | `assumptions-<subject>.csv` |

Use the date **of the data**, not of the conversion. `metrics-support-tickets-2026.07.csv` tells
someone what period it covers; `export_final_v2.csv` tells them nothing.

## Frontmatter

Every processed **markdown** file starts with:

```yaml
---
type: metrics | accounts | experiment | survey | notes | policy | research | assumptions
source: <original filename in 5_Library/sources/raw/>
date: <date of the data itself, if known>
processed: <today's date>
redactions: <what was dropped or masked, or "none">
---
```

CSV files can't carry frontmatter. Record the same information in a sibling `<name>.README.md`, or
in a `## Sources` section of the ingest report. Never lose the provenance — six weeks later,
"where did this number come from" is the question, every time.

The converter's first pass writes a coarser `type` (usually the file extension) and may add an
`engine:` line recording which converter produced it. **Keep `engine:` as provenance** and upgrade
`type` to the semantic value above as you refine.

## Conversion rules

- **Tabular data stays tabular.** A spreadsheet export becomes a CSV, not a markdown table. The
  analysis skills need to compute on it, and a markdown table with 1,200 rows helps nobody.
- **Keep the header row exactly as it arrived**, even if the names are ugly. Renaming columns during
  ingestion breaks the trace back to the source system. If names need cleaning, that's a logged
  change in `data-audit`.
- **Keep verbatim text verbatim.** Open-ended survey responses, meeting statements, and interview
  quotes are the raw material for later analysis. Fix obvious transcription noise; never
  paraphrase.
- **Structure with headers, don't rewrite.** For prose documents, preserve section numbering — it's
  what makes a citation checkable later.
- **Do not clean the data.** Blanks, duplicates, mixed date formats, and outliers pass through
  untouched. Cleaning is `data-audit`'s job, and it produces a log. An undocumented clean during
  ingestion is the kind of thing that quietly breaks a number three weeks later.
- **Redact identifiers when the user chooses to** — names become roles, emails and account numbers
  are dropped or replaced with stable anonymous IDs. Record what you did in `redactions:`.
- **Never invent or infer data that isn't in the source.** A blank stays blank.
