# Analytics OS

A cloneable analytics workspace for the AI use-case sessions in the Daniels College of Business
Professional MBA. You run both sessions inside this repo — and you keep it after.

It's an **agentic operating system**: a folder of markdown files, conventions, and skills that an
AI agent (Claude) reads and works in. You point it at a real decision from your own job, load
whatever data you're allowed to use, and run the chain — frame the decision → audit the data →
build the tool → write the memo → ship it. Each skill reads the previous one's output, so you
stop re-explaining context every time you open a new chat.

Two goals, in order:

1. **Run the two sessions.** Clone, bootstrap, pick a use case, and walk out with a working
   analysis tool and a memo an executive would actually read.
2. **Outlast the sessions.** Everything here is plain markdown you can edit, extend with your
   own skills, and hand to your team on Monday.

## Quickstart

1. **Open [Claude Code](https://claude.com/claude-code)** (desktop app, CLI, or VS Code extension)
   and ask it to fetch this workspace for you. Copy this in:

   > Clone https://github.com/data-love-co/info4610-analytics-os into a folder called
   > `info4610` directly inside my user folder, then open it and follow the setup.

   **Where it lands matters, for two reasons.** Put it straight in your user folder
   (`C:\Users\<you>\info4610` on Windows, `~/info4610` on Mac), *not* in Documents, Desktop, or any
   OneDrive or Google Drive folder. Synced drives corrupt the hidden `.git` folder, and deeply
   nested paths trip the Windows 260-character filename limit. A short, unsynced path avoids both.

   No git installed? Ask Claude to download the ZIP instead and it will handle it, or grab it
   yourself from the green **Code** button above.

2. **Say "get me started."** Bootstrap detects your OS, creates the `CLAUDE.md` link, then runs a
   short interview that builds your profile (`0_User/`) and your work context (`0_Org/`).
3. **Put data in `5_Library/sources/raw/`** — a spreadsheet export, survey responses, meeting
   notes, whatever your use case needs. Then say "ingest my data."
   No data you're allowed to use? Say so — `5_Library/sample-data/` has messy practice datasets
   built for every use case here.

Then say **"help me frame my decision"** and the chain takes it from there.

## The two sessions

| Session | What happens |
|---|---|
| **Lesson 1 — Scope and data** | L1.1 setup + ingest · L1.2 frame the decision · L1.3 audit the data |
| **Lesson 2 — Build and demo** | L2.1 build your use case · L2.2 write the decision memo · L2.3 demo it |

You come to Lesson 2 with a framed decision and audited data. That's what makes a two-hour build
possible.

## The ten use cases — pick one, maybe two

| Use case | You end up with |
|---|---|
| **Executive KPI dashboard** | A clean dashboard from a messy spreadsheet, plus a short "so what" |
| **What-if scenario calculator** | A pricing / staffing / budget simulator with ranges, not single guesses |
| **Forecast tool** | Trend + seasonality forecast with honest uncertainty bands |
| **Churn or risk scorer** | Scores for customers or accounts, with the top drivers exposed |
| **A/B test readout** | A full hypothesis-test readout ending in ship, iterate, or hold |
| **Survey / feedback synthesizer** | Themes, sentiment, and representative quotes from open-ended text |
| **Data cleaning assistant** | Missing values, duplicates, outliers — and a cleaning log you can defend |
| **Executive decision memo** | Bottom line up front: question, evidence, recommendation, risks |
| **Meeting-to-action-items** | Decisions, owners, deadlines, and a draft follow-up email |
| **Internal knowledge assistant** | Grounded Q&A over documents your team actually uses |

Every one of them has a skill. Ask `find-skills` — "which skill should I use?" — if you're not sure
which fits your decision.

## What's inside

```
0_System/           # Repo engine: bootstrap, skill scanner, file converter, sample-data generator
0_User/             # You — built by the bootstrap interview
0_Org/              # GROUND TRUTH — your organization: what it does, who decides, what it measures
1_Class/            # The two sessions — one self-contained subfolder per block
2_Outputs/          # Full work products: decision frame, audit, analysis, memo, demo notes
3_Projects/         # Non-build working projects (after the sessions)
4_Build_Projects/   # Things you build — dashboards, calculators, apps
5_Library/
  sources/raw/      #   Your data as it arrives — any format (gitignored, stays local)
  sources/processed/#   Standardized markdown/CSV — what the skills actually read
  templates/        #   No-AI fallback templates for every exercise
  method/           #   Short teaching notes: KPI choice, uncertainty, tests, forecasting, BLUF
  build-surfaces/   #   Claude Code vs. Claude Design vs. Cowork vs. Artifacts — and when
  sample-data/      #   Deliberately messy practice datasets
.agents/skills/     # Bucketed skills — find-skills/ finder + daniels/<n>-skill/ chain
```

## The chain

Run in order. Every skill reads your hand-completed template from `1_Class/<session>/`, plus
evidence from `5_Library/sources/processed/` and ground truth from `0_Org/`. You fill the template
by hand; the skill's markdown output lands in `2_Outputs/.agents/<session>/`, and its distilled
essence folds back into `0_Org/` for the next skill.

| # | Skill | Session | Writes (under `2_Outputs/.agents/`) |
|---|---|---|---|
| 1 | `analyst-bootstrap` | L1.1 | `0_User/` + `0_Org/` topic files |
| 2 | `ingest-data` *(optional)* | L1.1 | `5_Library/sources/processed/` |
| 3 | `frame-the-decision` | L1.2 | `L1.2-Decision-Frame/Decision-Frame.md` |
| 4 | `data-audit` | L1.3 | `L1.3-Data-Audit/Data-Audit.md` · `Cleaning-Log.md` |
| 5–12 | your chosen use case | L2.1 | `Use-Case/<Name>.md` + build spec |
| 13 | `decision-memo` | L2.2 | `L2.2-Decision-Memo/Decision-Memo.md` |
| 14 | `build-and-ship` | L2.1 · L2.3 | `L2.3-Demo/Demo-Notes.md` |

Prefer to work without AI on any stage? Every exercise has a plain template in
`5_Library/templates/`.

## Your data, your obligation

You have a day job and a duty to your employer. This repo is built around that:

- `5_Library/sources/raw/` is **gitignored** — data you drop there never leaves your machine
  through this repo. `processed/` **is** tracked, so check what's in it before you push anywhere.
- **When in doubt, use the sample data.** `5_Library/sample-data/` exists precisely so nobody has
  to choose between doing the exercise and honoring a confidentiality obligation.
- Aggregate or mask personal identifiers — names, emails, employee/customer IDs, salary or health
  detail. The agent is instructed to flag these; you are the one who decides.
- Nothing here calls an external service on its own. Bring your own agent; no key to store.

## The one rule that matters

Every number the agent gives you comes with a method note and a limitation. Read both. An analysis
you can't defend in the second question of Q&A isn't finished — and the second question is always
"how do you know?"

---

Built for the Daniels College of Business Professional MBA · adapted from the WNCP AI Founder OS
