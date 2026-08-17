# L1.3 — Audit the Data

**Lesson 1 (6:00–7:50 PM), third block.** About 45 minutes. Find out whether your data can carry the weight you're
about to put on it.

## The idea

Two rules separate an audit from "cleaning a spreadsheet":

**1. You never clean silently.** Every change gets logged with the reason and the row count. The log
is the deliverable. When someone challenges a number three weeks from now — and someone will — the
log is what settles it. "I think I removed some duplicates" is not an answer.

**2. The agent doesn't decide what's wrong.** An outlier might be an error or it might be the single
most important month in four years of data. A blank might be a zero, a not-applicable, or a system
failure. The agent surfaces each one with the options and the consequences; **you choose**, because
you know the business.

## What you do

Open `L1.3-Data-Audit-Template.md` and start the `data-audit` skill: *"audit my data."*

The skill profiles the file, runs seven families of checks, and brings you each finding with
options. Your job is the judgment calls — and writing down why you made them.

## The seven checks

| Check | The question |
|---|---|
| Missingness | What's absent, and is it absent at random? |
| Types and formats | Is a number stored as a number? Is a date stored as a date? |
| Duplicates | Is any row here twice? |
| Outliers | What's extreme, and is it real? |
| Categorical drift | Is one category written four ways? |
| Logical consistency | Do the values make sense together? |
| Definition drift | Does this column still mean what it meant three years ago? |

The last one is the hardest to spot and the most damaging. Ask whoever owns the source system
whether anything changed — a migration, a new definition, a reorg. Almost every organization has
one and almost nobody wrote it down.

## Two traps in the practice data, if you're using it

`customer_accounts.csv` has both, deliberately:

- **A leakage column.** `cancellation_reason` is only filled in for accounts that already churned —
  it's recorded *after* the outcome. Any model that includes it will look spectacular in testing and
  be useless in production, because you'd never have that field for an account that hasn't churned
  yet. This is the single most common way a churn model fails in the real world.
- **Non-random missingness.** `nps_score` is blank 18% of the time, and the blanks churn at a higher
  rate. Filling them with the column average quietly erases the signal. Deciding what to do about it
  is the actual analytical judgment, and it belongs in your log.

## Where work goes

- **You fill** `L1.3-Data-Audit-Template.md` by hand — the judgment calls and the reasoning.
- The agent writes `2_Outputs/.agents/L1.3-Data-Audit/Data-Audit.md` and `Cleaning-Log.md`.
- The cleaned data becomes a **new file** — `<original>-clean.csv`. The original is never modified;
  it's the audit trail.

## The line to hold

If the audit says the data can't support what you framed in L1.2, that's not a failure of the
session. It's the session working. Narrow the question to what the data *can* answer, and note what
you'd need to answer the original. That's a real finding and it's often the most useful thing
anyone brings back to their team.
