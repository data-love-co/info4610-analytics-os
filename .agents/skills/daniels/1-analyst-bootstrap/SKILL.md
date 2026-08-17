---
name: analyst-bootstrap
description: >
  Onboards a working professional into Analytics OS — detects OS, creates CLAUDE.md, checks
  prerequisites, optionally ingests any data already in 5_Library/sources/raw/ so the interview is
  grounded, builds the 0_User/ profile and 0_Org/ ground-truth topic files via a short interview,
  and confirms the workspace is ready. Triggers when the user says "get me started", "set me up",
  "I'm new here", or otherwise signals first-time setup. Session L1.1. Users bring their own agent
  — no model key required.
---

# analyst-bootstrap — Onboarding

You are setting up a working professional's machine to run their own analytics workspace. Be calm
and step-by-step. Do one step, confirm it worked, then move on.

Assume nothing about technical background. The people using this run finance, operations,
marketing, HR, and general management — they are experienced professionals who may never have
opened a terminal before. Explain what each step does in one plain sentence before running it, and
never make someone feel behind for asking what a repo is.

---

## Step 0 — Link CLAUDE.md + detect OS

Detect the OS (`uname -s` → Darwin/Linux; `$env:OS` → Windows_NT), state it, and confirm. Then
ensure `CLAUDE.md` exists at the repo root — if not, run:

```bash
node 0_System/bootstrap/setup.mjs
```

It detects the OS, creates `CLAUDE.md` from `AGENTS.md` (symlink on Mac/Linux, generated copy on
Windows), and checks the environment. If Node is unavailable, see the manual steps in
[reference/os-setup.md](reference/os-setup.md) — the file is a copy, so it can be created by hand.

---

## Step 1 — Confirm the agent

Confirm they're on **Claude Code** (CLI, desktop, or VS Code extension) — the supported path. Other
`AGENTS.md`-aware tools work since this repo is plain markdown, but live help in session is Claude
Code-first. **No model key required.**

If they're working in the Claude desktop or web app instead of Claude Code, that's fine for most of
the chain — say so, and note that the skills which write files (everything from L1.2 on) need
Claude Code or a file-capable surface. See `5_Library/build-surfaces/Choosing-Your-Surface.md`.

---

## Step 2 — Check prerequisites

Confirm **git** (`git --version`), **Node 18+** (`node --version`), and **Python 3**
(`python --version` or `python3 --version`). If any is missing, give the install command for their
OS — see [reference/prerequisites.md](reference/prerequisites.md).

None of these is a hard blocker. Node is only needed for `setup.mjs`; Python only for the file
converter and the sample-data generator. If something's missing, note it and continue.

---

## Step 3 — Data first (optional, and there's no wrong answer)

The interview in Steps 4–5 is sharper if you've already seen their data, so make the offer now.

Explain the convention in two sentences: *"Anything you want the agent to work from goes in
`5_Library/sources/raw/` — any format. I can standardize it into `5_Library/sources/processed/` and
use it to ask better questions while we set up your profile."*

Then **raise the confidentiality question yourself, before they have to.** This is the single most
important moment in the bootstrap for this audience:

> "Before you put anything here — is this data you're allowed to have on this machine? If you're
> not sure, or if the answer is no, that's completely fine. There's practice data in
> `5_Library/sample-data/` built for every use case in this workspace, and you can build the whole
> thing on that and re-point it at real data inside your own systems later."

Then make the determination:

1. Check `5_Library/sources/raw/`. If it has files, run the dry-run plan (writes nothing):

   ```bash
   python 0_System/scripts/parse-sources.py --plan
   ```

2. **Decide and offer:**
   - **Files present** → offer to process them now: *"Want me to standardize these first so the
     interview uses them?"* If yes, hand to `ingest-data`. If the plan shows files needing a
     converter that isn't installed, surface the one-line install command — **never install it
     yourself** — and let them choose: install then ingest, ingest with what's available, or defer.
   - **`raw/` is empty** → invite them to drop files now if they have any they can use. If not,
     point at `5_Library/sample-data/` and move on.
   - **They decline** → fine. Ingestion is never required to proceed.

3. Non-blocking either way. If they ingested, read the resulting `processed/` tree before the
   interview so you can ask informed follow-ups.

---

## Step 4 — Your profile (the interview)

Tell them: *"I'm going to ask a few questions so every future session adapts to you. Five minutes."*
Then ask conversationally, one at a time. If you ingested data in Step 3, lead with what you
learned and ask them to confirm or correct it.

1. Name, title, and what function you sit in (finance, operations, marketing, HR, product, general
   management, something else).
2. What your team is responsible for — what lands on your desk.
3. Your comfort with analysis: have you done statistics coursework, do you live in spreadsheets, do
   you write SQL or code? **Ask plainly and record the answer plainly.** There is no wrong answer
   and no need to soften it.
4. What tools you actually use day to day — Excel, Sheets, Tableau, Power BI, SQL, Python, none of
   the above.
5. How you like to work with an assistant: short and direct, or explained step by step?
   Recommendation first, or options first?

Write the answers into `0_User/` by calling **`util_get_user_info`** — use its `set(file, content)`
interface for each topic file (`01_Overview`, `02_Expertise`, `03_Preferences`, `04_Goals`; deep
background to `Z_Library`). Read the result back in one short paragraph and let them correct it.

**Record technical comfort accurately.** Every downstream skill reads it to decide whether to build
in a spreadsheet, a no-code surface, or Python — and whether to show the method or just apply it.
Inflating it here makes everything after this harder for them.

---

## Step 5 — Work context

From the same interview, plus anything you ingested, build the `0_Org/` topic files by calling
**`util_get_org_info`** — use its `set(file, essence)` interface for each topic. Ask follow-ups
only where thin. Seed at minimum:

- `01_Overview` — the organization, the industry, roughly how big, the unit they work in
- `02_Decisions` — what decisions their team makes, who owns them, on what cadence
- `03_Metrics` — what the org measures. **Push for definitions, not just names.** If they say "we
  track retention," ask what they mean — logo, revenue, seat, gross, net. This one question saves
  more rework than anything else in the bootstrap.
- `04_Data` — where the data lives (CRM, ERP, ticketing, HRIS, a shared drive of spreadsheets),
  whether they can get an extract, and how sensitive it is
- `05_Stakeholders` — who they'd present an analysis to, and what that person cares about
- `06_Constraints` — privacy or policy limits, timing, approvals

These topic files — not chat memory — are what every later skill reads. They can extend them any
time, and each chain skill folds its output essence back in as the sessions progress.

**Confidentiality check before writing.** `0_Org/` is tracked in git. Don't write customer names,
employee names, account numbers, or salary figures tied to a person. Capture the shape without the
identifying detail, and say so when you do.

---

## Step 6 — Verify and recap

Final checklist — confirm each:

- [ ] `CLAUDE.md` exists at the repo root
- [ ] `0_User/` topic files exist (via `util_get_user_info`) and they approved them
- [ ] `0_Org/` topic files exist (via `util_get_org_info`) and they approved them
- [ ] `.agents/skills/skills.json` lists the chain skills
- [ ] `5_Library/sources/raw/` and `processed/` exist
- [ ] Data ingested — or they know where the practice data is

Recap what completed vs. what's pending. Then set the picture:

*"From here the chain runs: frame the decision → audit the data → build your use case → write the
memo → demo it. Each skill reads the last one's output, so you won't have to re-explain your
situation. The next step is `frame-the-decision` — say 'help me frame my decision' when you're
ready. Do that one before you touch any data; it's the step that decides whether the rest of this
is useful."*

---

## Guardrails

- Never make someone feel behind. "What's a terminal" is a reasonable question from a director of
  finance and gets a real answer, not a workaround.
- Raise the confidentiality question yourself in Step 3 — don't wait for them to worry about it.
- Never install anything on their machine. Surface the command; they run it.
- Record analytics comfort as stated, without inflating it.
- Push for metric **definitions** in Step 5, not just metric names.
- Everything here is local. Nothing leaves the machine.
