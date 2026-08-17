# L1.1 — Setup and Data

**Lesson 1, first block.** Get the workspace running and get your data (or the practice data) in
place.

## What you do

1. **Clone this repo** and open the folder in Claude Code.
2. **Say "get me started."** The `analyst-bootstrap` skill detects your OS, creates `CLAUDE.md`,
   checks prerequisites, then runs a short interview that builds your profile (`0_User/`) and your
   work context (`0_Org/`). Five to ten minutes.
3. **Put data in `5_Library/sources/raw/`**, then say "ingest my data."

## Before you put anything in `raw/` — the one question

**Is this data you're allowed to have on this machine?**

You all have day jobs and obligations to your employer. If the answer is no, or if you're not sure,
that is completely fine and it does not limit what you can do here.

`5_Library/sources/raw/` is gitignored, so nothing you put there gets committed. But
`5_Library/sources/processed/` **is** tracked, and ingestion is what moves data across that line.
The agent is instructed to flag identifying columns and offer to drop or mask them — but you're the
one who decides.

**If in doubt, use `5_Library/sample-data/.`** It has messy practice datasets built for every use
case in this workspace: four years of regional sales, 1,200 customer accounts with a churn outcome,
an A/B test with 17,200 visitors, 240 survey responses, meeting notes, and a policy handbook.

You can build the entire method on practice data and re-point it at real data inside your own
systems later. For most people in this room, that's the right answer, and it costs you nothing
pedagogically.

## What good looks like at the end of this block

- `CLAUDE.md` exists at the repo root
- `0_User/` has your profile, and it says accurately how comfortable you are with analysis — this
  drives what every later skill recommends, so don't inflate it
- `0_Org/` has your work context, including **metric definitions**, not just metric names
- Something readable is in `5_Library/sources/processed/`, or you know which sample file you're
  using

## Using something other than Claude Code

Fine. Nobody is blocked, and the whole thing is plain markdown and CSV.

| You have | What you get |
|---|---|
| **Copilot agent mode, Codex, Cursor, Gemini CLI, Windsurf, Zed** | Everything. They read `AGENTS.md` natively, same as Claude Code. **Copilot is free for verified students** |
| **ChatGPT Plus, Gemini, Claude on the web** | All ten use cases. Upload the data file, paste the stage prompt from `5_Library/build-surfaces/Portable-Prompts.md`, carry context between stages yourself |
| **A free chat tool, no code execution** | Decision framing, meeting notes, feedback synthesis, the memo, and the knowledge assistant. Not the numeric ones, because a tool that can't run code shouldn't be trusted with a number you'll present |

Full detail, including how to get Copilot free with your university email:
`5_Library/build-surfaces/Using-Another-Assistant.md`.

## When something doesn't install

Work laptops block things. None of it stops you:

- No Node? Copy `AGENTS.md` to `CLAUDE.md` by hand.
- No Python? The sample CSVs are already committed. You only lose the file converter.
- No git? The workspace is plain markdown; it works, you just can't version it.

Say so in class and move on. The analysis is the point, not the toolchain.

## Where work goes

Nothing to fill in by hand this block. The bootstrap writes `0_User/` and `0_Org/` through the
utility skills, and you review and correct what it wrote.
