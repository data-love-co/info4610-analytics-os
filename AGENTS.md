# Analytics OS — Daniels Professional MBA

Your analytics workspace for the two AI use-case sessions — and for the work you go back to
on Monday. This repo is an **agentic operating system**: a folder of markdown files,
conventions, and skills that an AI agent (Claude) reads and works inside. You point it at a
real decision from your own job, load whatever data you're allowed to use, and run the chain:
frame the decision → audit the data → build the analysis tool → write the memo → ship it.

You own every artifact it helps you produce. The agent coaches, structures, and drafts; you
make the calls and you sign your name to the recommendation.

## Getting started

Open this folder in **Claude Code** (CLI, desktop app, or VS Code extension) — or any
`AGENTS.md`-aware agent — and say **"get me started."** The `analyst-bootstrap` skill detects
your OS, creates the `CLAUDE.md → AGENTS.md` link, then interviews you to build your profile
(`0_User/`) and your work context (`0_Org/`).

Optional script form of the same setup checks:

```
node 0_System/bootstrap/setup.mjs
```

## Repo structure

```
0_System/           # Repo engine: bootstrap script, skill scanner, file converter, sample-data generator
0_User/             # You — role, function, tools, how you like to work (bootstrap builds this)
0_Org/              # GROUND TRUTH — your organization: what it does, who decides, what it measures
1_Class/            # The two sessions — one subfolder each; holds the template YOU fill by hand
2_Outputs/          # Agent work products, in a hidden .agents/<session>/ layer (don't hand-edit)
3_Projects/         # Non-build working projects — research, SOPs, analyses that stay in markdown
4_Build_Projects/   # Things you build — dashboards, calculators, apps (YYYY.MM Short Name)
5_Library/
  sources/raw/      #   Drop zone, any format — GITIGNORED, never leaves the machine
  sources/processed/#   Standardized markdown/CSV — what the skills actually read
  templates/        #   Master no-AI fallback templates for every stage
  method/           #   Short teaching notes: KPI choice, uncertainty, tests, forecasting, BLUF
  build-surfaces/   #   Which Claude surface to build in, and how
  sample-data/      #   Deliberately messy practice datasets (use these if your real data can't leave work)
.agents/skills/     # Bucketed skills — auto-discovered via find-skills/ and scan-skills.py
  find-skills/      #   THE finder: one skill that locates all the others
  daniels/          #   Course skills, numbered in run order:
    1-analyst-bootstrap/     #   "Get me started" onboarding
    2-ingest-data/           #   raw → processed standardization
    3-frame-the-decision/    #   the question, the audience, the threshold  ← everything starts here
    4-data-audit/            #   missing values, duplicates, outliers, cleaning log
    5-kpi-dashboard/         #  ─┐
    6-scenario-calculator/   #   │
    7-forecast/              #   │
    8-risk-scorer/           #   ├─ the ten use cases — pick one or two
    9-ab-test-readout/       #   │
    10-feedback-synthesizer/ #   │
    11-meeting-to-actions/   #   │
    12-knowledge-assistant/  #  ─┘
    13-decision-memo/        #   turn the analysis into a BLUF memo
    14-build-and-ship/       #   pick the Claude surface, build it, prep the demo
    util_/                   #   file-access utilities (0_User/, 0_Org/, input lookup)
```

## The chain

**Set up → frame → audit → build → memo → ship.** Skills 1–2 set you up. Skill 3 is the one
nobody should skip: an analysis with no decision attached is a hobby. Skill 4 tells you whether
the data can carry the weight you're about to put on it. Skills 5–12 are the ten use cases —
you pick one or two, not all ten. Skill 13 turns whatever you built into something an executive
will actually read, and 14 gets it in front of the room.

Each skill reads your **hand-completed template** in `1_Class/<session>/`, evidence in
`5_Library/sources/processed/`, and ground truth in `0_Org/`; it writes its full output to
`2_Outputs/.agents/<session>/` (agent-owned, hidden) and folds the essence back into `0_Org/`
for the next skill. **You fill the template by hand — the skill never does.** A missing input
is never a dead end: skills recover with you (offer to ingest or gather it, then continue).

| # | Skill | Session | Writes (under `2_Outputs/.agents/`) |
|---|---|---|---|
| 1 | `analyst-bootstrap` | L1.1 | `0_User/` + `0_Org/` topic files |
| 2 | `ingest-data` *(optional)* | L1.1 | `5_Library/sources/processed/` |
| 3 | `frame-the-decision` | L1.2 | `L1.2-Decision-Frame/Decision-Frame.md` |
| 4 | `data-audit` | L1.3 | `L1.3-Data-Audit/Data-Audit.md` + `Cleaning-Log.md` |
| 5–12 | the ten use cases | L2.1 | `Use-Case/<Name>.md` + a build spec |
| 13 | `decision-memo` | L2.2 | `L2.2-Decision-Memo/Decision-Memo.md` |
| 14 | `build-and-ship` | L2.1 · L2.3 | `L2.3-Demo/Demo-Notes.md` |

## The ten use cases

| Skill | What you end up with |
|---|---|
| `kpi-dashboard` | A clean dashboard from a messy spreadsheet, plus a short "so what" |
| `scenario-calculator` | A pricing / staffing / budget simulator that shows ranges, not single guesses |
| `forecast` | Trend + seasonality forecast with honest uncertainty bands |
| `risk-scorer` | Churn / conversion / default scores with the top drivers exposed |
| `ab-test-readout` | A full hypothesis-test readout ending in ship, iterate, or hold |
| `feedback-synthesizer` | Themes, sentiment, and representative quotes from open-ended text |
| `data-audit` | Missing values, duplicates, outliers — and a cleaning log you can defend |
| `decision-memo` | Bottom line up front: question, evidence, recommendation, risks |
| `meeting-to-actions` | Decisions, owners, deadlines, and a draft follow-up email |
| `knowledge-assistant` | Grounded Q&A over documents your team actually uses |

## Data convention

- **`5_Library/sources/raw/`** — drop everything here: spreadsheet exports, survey responses,
  meeting notes, policy documents, ticket dumps. Any format; organize into subfolders if you
  like — the layout is mirrored into `processed/`. **Gitignored** — raw data never leaves your
  machine through this repo.
- **`5_Library/sources/processed/`** — cleaned, standardized markdown/CSV the skills read.
  The optional `ingest-data` skill runs a tiered converter
  (`0_System/scripts/parse-sources.py`) that auto-uses the best engine installed
  (Docling → MarkItDown → built-in text/CSV) and stubs what it can't convert. It recommends
  installs but never runs them.
- **No usable work data?** That is normal and it is fine. `5_Library/sample-data/` has messy
  practice datasets built for these exercises — generate more with
  `python 0_System/scripts/make-sample-data.py`.

## Conventions

- `AGENTS.md` (this file) is the source of truth for agent instructions; `CLAUDE.md` is a link
  to it created at bootstrap — never hand-edit `CLAUDE.md` directly
- Build folders in `4_Build_Projects/` use `YYYY.MM Short Name` naming
  (e.g. `2026.08 Regional Staffing Model`)
- Skills are bucketed under `.agents/skills/`: use `find-skills` to locate the right one;
  each `SKILL.md` frontmatter is the source of truth, and `0_System/scripts/scan-skills.py`
  records enabled state in `skills.json`
- Skills are thought partners — they coach, draft, and structure, but you make the calls and
  you own the artifacts. Read what they produce; don't let generated content you never read
  feed back into the system
- Use YAML frontmatter on processed source files (type, date, source) so the agent can index them

## How to be useful here — the analysis ethic

These rules are not style preferences. They are the difference between an analysis that holds
up in a room full of executives and one that gets taken apart in the first two minutes.

- **State the decision first.** Every analysis names the decision it informs, who owns that
  decision, and what would change their mind. If the user can't name one, help them find it
  before touching the data.
- **Never give a single number where a range belongs.** Forecasts, scenarios, and scores carry
  uncertainty. Show it — intervals, sensitivity, best/base/worst — and say where it comes from.
- **Show the assumptions as a list the user can argue with.** Every model has them. Hidden
  assumptions are how analyses fail in public.
- **Say what the data cannot support.** Sample too small, window too short, confounded
  comparison, survivorship in the extract — name it plainly rather than burying a caveat.
- **Correlation is not a driver.** When surfacing "top drivers," say they are associations and
  what it would take to establish cause.
- **Round like a human.** Executives don't need four decimal places; they need the magnitude
  and the direction. Precision beyond what the data supports is a form of lying.
- **Plain language over jargon.** Write for a smart reader who does not do statistics for a
  living. Expand every acronym on first use. If a technical term earns its place, define it in
  the same sentence.
- **No dead ends.** If something can't be done with what's available, say what *can* be done
  and what would unlock the rest.

## Key reference files

| Question | File |
|---|---|
| Who am I working with? | `0_User/` (via `util_get_user_info`) |
| What is this organization? | `0_Org/` (via `util_get_org_info`) |
| What data do we have? | `5_Library/sources/processed/` |
| What skills are available? | `.agents/skills/` SKILL.md files (use `find-skills`) |
| How does the engine work? | `0_System/README.md` |
| Where are the no-AI templates? | `5_Library/templates/` |
| How do I pick which method to use? | `5_Library/method/` |
| Where should I build this? | `5_Library/build-surfaces/Choosing-Your-Surface.md` |

## Boundaries — do not

- **Never put confidential employer data anywhere it can be committed or shared.** Everyone
  here has a day job and a duty to their employer. Before any file lands in
  `5_Library/sources/processed/` (which IS tracked in git), confirm it is safe to share. When
  in doubt, keep it in `raw/`, which is gitignored, or use `5_Library/sample-data/` instead.
- **Never write personal identifiers into a tracked file.** Names, emails, employee or customer
  IDs, account numbers, health or salary detail tied to a person. Aggregate, mask, or drop them
  — and tell the user what you dropped.
- Commit `.env` or any secret
- Edit `CLAUDE.md` directly — it is generated from `AGENTS.md`; edit this file instead
- Send data to external services without the user's explicit say-so
- Present a model's output as fact — every number the agent produces gets a method note and a
  limitation next to it
- Fabricate data to fill a gap. If a field is missing, it is missing; say so. Simulated data is
  allowed only when the user asks for it and it is labeled **simulated** in the output
- Generate large volumes of artifacts nobody asked for — one artifact per stage, owned and
  edited by the user
- Fill in the user's session template for them — **they complete it by hand** in
  `1_Class/<session>/`; derived markdown goes only to `2_Outputs/.agents/<session>/`
