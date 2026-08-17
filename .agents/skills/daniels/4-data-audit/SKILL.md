---
name: data-audit
description: >
  Audits a spreadsheet or extract for missing values, duplicates, outliers, type problems, and
  definition drift — then produces a cleaning log that documents every change and why. Use when:
  "audit my spreadsheet", "clean this data", "is this data any good", "this spreadsheet is a
  disaster", "check my data before I analyze it", "why don't these numbers match". Session L1.3,
  and the step before any analysis that needs to survive scrutiny. Make sure to use this skill
  whenever someone is about to analyze an unfamiliar extract — even if they didn't ask for an
  audit.
---

# data-audit — Audit and Cleaning Log

You are finding out whether this data can carry the weight the user is about to put on it, and
producing a record of every change you make.

Two things make this different from "cleaning a spreadsheet":

1. **You never clean silently.** Every change is logged with the reason and the row count affected.
   The log is the deliverable. Anyone who later challenges a number should be able to trace it.
2. **You do not decide what's wrong on your own.** An outlier might be an error or the single most
   important month in the dataset. A blank might be a zero, a not-applicable, or a system failure.
   Surface each one and let the user choose — they know the business, you know the pattern.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("data-audit")`), then pull each source:

- **The data** *(primary)* — files in `5_Library/sources/processed/`, or `5_Library/sample-data/`
  if the user has nothing they can use here. Offer the sample data without apology.
- **The session template** *(primary)* — `1_Class/L1.3-Data-Audit/`.
- **The decision frame** *(primary)* — `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md`.
  It tells you which columns actually matter and how precise the analysis needs to be. Audit
  proportionally: a column nobody will use doesn't need a 20-minute discussion.
- **Org ground truth** *(supplementary)* — via `util_get_org_info`, especially `03_Metrics` for how
  the organization defines things.

If there's no decision frame, don't stop — ask what the data is for in one question and proceed.

## Step 1 — Profile before you judge

Read the file and report the shape before making any claim about quality:

- Rows, columns, and what one row represents. **Say the grain out loud** — "one row is one
  region-month-channel." Half of all spreadsheet confusion is two people assuming different grains.
- For each column: type as stored, type as intended, distinct values, missing count, and range or
  top values.
- Date coverage: earliest, latest, and any gaps in the sequence.

Show this as a compact table. It's the most useful thing you produce in the first five minutes.

## Step 2 — Run the checks

Work through **`reference/checks.md`** in order. It covers the seven families: missingness, types
and formats, duplicates, outliers, categorical drift, referential and logical consistency, and
definition drift.

For each finding, report four things and nothing more:

| What | Where | How much | Why it matters here |
|---|---|---|---|
| Four date formats in `month` | `month` | 195 rows, 4 formats | Sorting and any time-based grouping will be wrong |

The fourth column is the one that matters. "37 missing values" is trivia; "37 missing values in the
column you're about to average, concentrated in Q4" is a finding.

## Step 3 — Decide, one at a time

For each finding that needs a decision, present the options and the consequence of each, then ask.
Never batch these into a single "shall I clean it all?" question — that's how a judgment call gets
made by accident.

Format each decision like this:

> **`nps_score` is missing for 18% of accounts.** The missing rows churn at a higher rate than the
> filled ones, so this isn't random — people who stopped answering surveys were already
> disengaging.
> - **Impute the average** — keeps all 1,200 rows, but erases the signal that non-response carries.
> - **Add a "did not respond" flag and keep the blank** — preserves the signal, costs you a column.
> - **Exclude those rows** — clean, but drops 18% of your data and biases toward engaged accounts.
>
> Which one, and what's your reasoning? I'll log it either way.

**Record their reasoning, not just their choice.** Six weeks later the choice is indefensible
without it.

## Step 4 — Apply and log

Apply the chosen fixes. Write two outputs:

1. **The audit** → `2_Outputs/.agents/L1.3-Data-Audit/Data-Audit.md` — the profile, every finding,
   and the trustworthiness verdict.
2. **The cleaning log** → `2_Outputs/.agents/L1.3-Data-Audit/Cleaning-Log.md` — one row per change:
   what changed, how many rows, the rule applied, the reason, and who decided.

Full formats in **`reference/output-format.md`**.

**Write the cleaned data as a new file.** Never overwrite the source. Name it
`<original-stem>-clean.csv` in `5_Library/sources/processed/`. The original stays exactly as it
arrived, so anyone can reproduce the path from raw to clean.

## Step 5 — The verdict

End with a plain-language verdict on what this data can and cannot support. Three lines:

1. **Can support:** [the analyses this data is genuinely good enough for]
2. **Can support with caveats:** [what's possible if you state a limitation alongside it]
3. **Cannot support:** [what someone will ask for that this data can't answer, and why]

That third line is the one that saves people. Say it before they build, not after.

Then fold the essence into ground truth via `util_get_org_info` (`set(04_Data, …)`) — a short
paragraph on what this dataset is, its grain, and its known limitations, under a
`## Data Quality Notes` header.

## Guardrails

- **Never modify the source file.** Clean data goes to a new file; the original is the audit trail.
- **Never clean without logging.** An unlogged change is worse than a known defect, because nobody
  will find it.
- **Never delete an outlier because it's large.** Investigate it, ask what happened, and let the
  user decide. The 3.4x month in the sample sales data is a real bulk order; deleting it would hide
  the most interesting event in four years.
- **Never impute silently.** Filling blanks with an average is a modeling decision with a
  consequence, and it gets the same treatment as any other decision: options, consequences, choice,
  reason, log.
- Audit proportionally to the decision. Not every column deserves equal attention.
- If the data contains personal identifiers, flag them and offer to drop or mask before anything
  lands in a tracked file.
- Say "I don't know why this is here" when you don't. Speculating about the cause of a data defect
  is how wrong stories get repeated in meetings.

## Quick reference

| Check family | The question | Typical finding |
|---|---|---|
| Missingness | What's absent, and is it absent at random? | Non-response correlated with the outcome |
| Types & formats | Is a number stored as a number? | `$1,234.00` and `1.2M` in a revenue column |
| Duplicates | Is any row here twice? | Double-paste during month-end close |
| Outliers | What's extreme, and is it real? | A bulk order, an outage, a decimal slip |
| Categorical drift | Is one category written four ways? | `West`, `WEST`, `west`, `West ` |
| Logical consistency | Do the values make sense together? | Negative units, renewal before start |
| Definition drift | Does this column mean what you think? | "Revenue" changed to net of returns in 2024 |
