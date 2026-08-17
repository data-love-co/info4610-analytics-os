# sources/ — Your Data

Two folders and one line between them that matters.

```
5_Library/sources/
├── raw/         # GITIGNORED — drop anything here, any format. Never leaves your machine
└── processed/   # TRACKED IN GIT — standardized markdown/CSV. What the skills read
```

## raw/

Drop everything here: spreadsheet exports, survey results, meeting notes, policy documents, ticket
dumps, PDFs, slide decks. Any format. Organize into subfolders if you like — the layout is mirrored
into `processed/`.

**This folder is gitignored.** Nothing you put here gets committed, and nothing leaves your machine
through this repo.

The `ingest-data` skill never modifies anything here. It reads and converts; the original stays.

## processed/

Clean markdown, or CSV for tabular data, mirroring the `raw/` layout. This is the single place the
chain skills look for evidence.

**This folder is tracked in git.** Ingestion is the moment data crosses from private to shareable,
which is why the `ingest-data` skill runs a confidentiality check before it converts anything —
naming the specific columns that carry identifiers and offering to drop, mask, or leave the file
where it is.

## The question to ask before you drop anything in raw/

**Is this data you're allowed to have on this machine?**

You have a day job and an obligation to your employer. If the answer is no, or you're not sure,
that's completely fine and it does not limit what you can do here.

**Use `5_Library/sample-data/` instead.** It has messy practice datasets built for every use case in
this workspace. You can build the entire method on practice data and re-point it at real data inside
your own systems later — which, for a lot of people in this room, is the right answer anyway.

## What "standardized" means

- **Tabular stays tabular.** A spreadsheet export becomes a CSV, not a markdown table. The analysis
  skills need to compute on it.
- **Prose gets structure preserved.** Section numbering survives, because that's what makes a
  citation checkable later.
- **Nothing gets cleaned.** Blanks, duplicates, mixed date formats, and outliers pass through
  untouched. Cleaning happens in `data-audit`, with a log. An undocumented clean during ingestion is
  how a number quietly breaks three weeks later.
- **Verbatim stays verbatim.** Open-ended responses and meeting statements are raw material. Never
  paraphrased.
