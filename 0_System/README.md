# 0_System — Repo Engine

The machinery that makes this workspace work. You rarely need to open this folder — the bootstrap
and the skills drive everything.

## What's here

| Path | Purpose |
|---|---|
| `bootstrap/setup.mjs` | Creates `CLAUDE.md` from `AGENTS.md` (symlink on Mac/Linux, copy on Windows) and runs readiness checks for Node, git, and Python. Cross-platform, dependency-free, safe to re-run |
| `scripts/scan-skills.py` | Regenerates `.agents/skills/skills.json` — a slim `{name, path, enabled}` registry — from the SKILL.md files on disk. Run after adding or removing a skill: `python 0_System/scripts/scan-skills.py` |
| `scripts/parse-sources.py` | Tiered `raw/ → processed/` converter (the `ingest-data` engine). Auto-uses the best converter installed (Docling → MarkItDown → built-in text/CSV), mirrors subfolders, and **recommends installs but never runs them**. `--plan` dry-runs the analysis; `--force` reconverts |
| `scripts/make-sample-data.py` | Generates the deliberately messy practice datasets in `5_Library/sample-data/`. Fixed seed, standard library only. `--clean` removes them |

## How the pieces fit

- **`AGENTS.md` is the source of truth.** `CLAUDE.md` is generated from it by `setup.mjs` and is
  gitignored. Edit `AGENTS.md`, re-run setup, never hand-edit `CLAUDE.md`.
- **Skills are auto-discovered** from `.agents/skills/` — each `SKILL.md`'s frontmatter is the source
  of truth for what it does and when it fires. `skills.json` records only `name`, `path`, and
  `enabled`, so it can't go stale against the real skills. `scan-skills.py` preserves enabled flags
  when it rescans.
- **No servers, no background processes.** This repo is plain files; everything runs inside the agent
  session.

## Adding your own skill

The point of this structure is that you can extend it. To add one:

1. Create `.agents/skills/<bucket>/<name>/SKILL.md` with YAML frontmatter containing `name` and a
   `description` that spells out **when it should fire** — the description is what routing matches
   against, so write it as trigger phrases, not as a summary.
2. Put long procedures in `<name>/reference/*.md` and load them from the SKILL.md at the step where
   they're needed. Keeps the main file readable.
3. Run `python 0_System/scripts/scan-skills.py` to register it.
4. If it reads inputs from elsewhere in the workspace, add a row to the task map in
   `util_get_inputs` rather than hardcoding paths in your skill.

The existing skills are the pattern. `daniels/3-frame-the-decision/` is a good one to copy: an
orchestrator SKILL.md that loads reference files at each step.

## Python notes

Everything here is standard library and runs on Python 3.8+. Console output is deliberately ASCII —
the default Windows terminal encoding can't print check marks or arrows, and a script that crashes
on its own success message is a bad first experience for someone who just installed Python.
