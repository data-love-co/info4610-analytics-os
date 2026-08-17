---
name: util_get_inputs
description: >
  The single place that tells a skill where its inputs come from. Chain skills call this at the
  start of a run to resolve "what should I read, and from where" for the task at hand, instead of
  hardcoding input locations. Routes to organizational ground truth (via util_get_org_info), the
  user profile (via util_get_user_info), standardized evidence (5_Library/sources/processed/),
  practice data (5_Library/sample-data/), the user's session template (1_Class/<session>/),
  upstream outputs (2_Outputs/.agents/<session>/), and any additional configured sources (.env,
  connected data, MCPs). Triggers whenever a skill needs to gather context, or the user asks "what
  does this exercise read".
---

# util_get_inputs — Input Lookup

You are the central map of where inputs come from. Chain skills call you before they run so they
never hardcode where to read. You return the ordered list of input sources for the task, how to
access each, and which are primary vs. supplementary. The calling skill pulls the content itself
using the access methods below — you return the map, not the content.

## Why this exists

Outputs are deterministic — each skill writes to one known place, hardcoded in the skill. Inputs
are not. A forecast can draw on a processed CSV, practice data, org ground truth, the user's own
profile, a prior output, or a source added later (a `.env` value, a connected system, an MCP).
Skills ask you rather than assume, so when a new source type appears we register it here once
instead of editing every skill.

## Access methods — how to read each source type

| Source | How to access |
|---|---|
| Org ground truth | call `util_get_org_info` (`get()`) — never read `0_Org/` directly |
| User profile | call `util_get_user_info` (`get()`) — never read `0_User/` directly |
| Evidence | read the files in `5_Library/sources/processed/` (the standardized ingest output) |
| Practice data | read `5_Library/sample-data/` — the fallback when the user has no data they can use |
| Session template | read the working template in `1_Class/<session>/` (human-owned; may be blank or partly filled) |
| Upstream output | read `2_Outputs/.agents/<upstream-session>/<File>.md` |
| Method notes | read `5_Library/method/<topic>.md` when a skill needs to explain or choose a method |
| Configured / external | a `.env` value, connected data source, or MCP — see "Registering a new source" |

## Interface

- `get(task)` → return the input map for `task` (rows below): each source tagged **primary** or
  **supplementary**, with its access method. The calling skill pulls from each.
- `get()` → return the whole map.

## The input map — task → sources

Sources are tagged **primary** (shapes a strong result) or **supplementary** (enriches). A missing
primary source is never a stop — the calling skill recovers it with the user.

| Task (skill / session) | Primary | Supplementary |
|---|---|---|
| `frame-the-decision` (L1.2) | org ground truth · `L1.2-Decision-Frame` session template | user profile · evidence |
| `data-audit` (L1.3) | evidence (or practice data) · `L1.3-Data-Audit` session template · `L1.2-Decision-Frame` output | org ground truth |
| `kpi-dashboard` (L2.1) | `L1.2-Decision-Frame` output · `L1.3-Data-Audit` output · evidence · org ground truth (`03_Metrics`) | user profile · method notes |
| `scenario-calculator` (L2.1) | `L1.2-Decision-Frame` output · evidence · org ground truth | `L1.3-Data-Audit` output · method notes |
| `forecast` (L2.1) | `L1.2-Decision-Frame` output · `L1.3-Data-Audit` output · time-series evidence | org ground truth · method notes |
| `risk-scorer` (L2.1) | `L1.2-Decision-Frame` output · `L1.3-Data-Audit` output · labeled evidence | org ground truth · method notes |
| `ab-test-readout` (L2.1) | experiment results (evidence or pasted) · `L1.2-Decision-Frame` output | org ground truth · method notes |
| `feedback-synthesizer` (L2.1) | open-ended text evidence · `L1.2-Decision-Frame` output | org ground truth · method notes |
| `meeting-to-actions` (L2.1) | meeting notes or transcript (evidence or pasted) | org ground truth (`05_Stakeholders`) · user profile |
| `knowledge-assistant` (L2.1) | the document corpus in `5_Library/sources/processed/` | org ground truth · user profile |
| `decision-memo` (L2.2) | the use-case output in `2_Outputs/.agents/Use-Case/` · `L1.2-Decision-Frame` output · `L2.2-Decision-Memo` session template | org ground truth (`05_Stakeholders`) · `L1.3-Data-Audit` output |
| `build-and-ship` (L2.1 · L2.3) | the use-case output · user profile (technical comfort) · `L2.1-Build` session template | `5_Library/build-surfaces/` · org ground truth (`06_Constraints`) |

`ingest-data` (L1.1) is intentionally absent: it produces evidence rather than consuming chain
inputs, so it does not call this lookup.

## When a primary input is missing — recover, never stop

A skill never stops because an upstream document or source is absent. People arrive from different
starting points — some ran the earlier session, some bring their own work, some are starting cold
on a Tuesday. So when a primary input is missing, recover *with* the user instead of gating:

1. **Say what's missing, plainly.** "I don't have your decision frame from the last session."
2. **Offer the choice.** In one question: do they have their own material for this (notes, a doc, a
   prior analysis) they'd like to use, or would they rather answer a few quick questions to fill
   the gap here?
3. **Use what they bring, or guide them through the gap.** If they share material, use it. If they
   pick the questions, pull the core questions from the upstream skill and walk through just those
   — enough to continue, not the whole exercise.
4. **Continue.** Flag anything still thin so the user knows that part is lighter than usual.

### Special case — no data the user is allowed to use

The most common real blocker in this room is not missing data. It is data that exists but cannot
leave the employer's systems. When a skill needs evidence and the user doesn't have any they can
put on this machine:

1. **Name the option immediately.** "You don't need to bring work data for this. There's practice
   data in `5_Library/sample-data/` built for exactly this use case."
2. **Point at the right file** for the task (see `5_Library/sample-data/README.md`).
3. **Offer the hybrid.** They can build the method on practice data here, and re-point it at real
   data inside their own environment later. Say so — it is usually what they actually want.
4. **Never pressure** the user to bring data they're unsure about. If they're weighing it, the
   answer is the sample data.

### Special case — evidence folder is empty

Ingestion is optional, so an empty `processed/` folder is normal, not an error.

1. **Offer ingestion first.** "I don't see any processed data. Want to run `ingest-data` to bring
   in your spreadsheet, notes, or documents first?"
2. **If yes** → pause, let them run it, then re-read `5_Library/sources/processed/` and continue.
3. **If no** → offer the practice data, then proceed on org ground truth and any prior outputs.
   Note that the stage is running lighter on evidence; never block.

## Registering a new source

When inputs start coming from a new place (a `.env` value, a connected system, an MCP), add it to
the access-methods table and the relevant task rows above — once, centrally — rather than teaching
each skill about it.

## Guardrails

- You return the map, not the content — the calling skill reads each source via its access method.
- Always route `0_Org/` and `0_User/` reads through their utilities; never name those files directly.
- A missing **primary** source is a recovery path, not a stop. Supplementary sources enrich but are
  never expected.
- Practice data is a first-class input, not a consolation prize. Offer it early and without
  apology.
- Keep this map current — it is the one place input locations live.
- Outputs are not your concern — each skill hardcodes its own single output destination.
