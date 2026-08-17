# Output Format

Two files, written quietly. The verdict goes in chat.

## 1 — The audit → `2_Outputs/.agents/L1.3-Data-Audit/Data-Audit.md`

```markdown
---
type: data-audit
session: L1.3-Data-Audit
source_file: <path to the file audited>
date: <today>
rows_in: <n>
rows_out: <n>
---

# Data Audit — <file name>

**Grain:** one row is one <what>.
**Coverage:** <earliest> to <latest>, <n> periods, <n> gaps.
**Audited against:** <the decision from L1.2, one line>

## Column profile

| Column | Stored as | Should be | Distinct | Missing | Range / top values |
|---|---|---|---|---|---|
| month | text | date | 48 | 0 | 2022-01 to 2025-12 |

## Findings

Ordered by how much they affect the decision, not by severity in the abstract.

### 1. <Finding> — <n> rows

**What:** <the defect, stated plainly>
**Where:** <column(s), row count, concentration>
**Why it matters here:** <the effect on this specific analysis>
**Decision:** <what the user chose, and their reasoning>

### 2. …

## Not fixed, on purpose

| Item | Why it was left alone |
|---|---|
| <e.g. the 3.4x West month> | Real bulk order, documented in notes. Kept; will be reported with and without. |

## Verdict

**Can support:** <analyses this data is genuinely good enough for>

**Can support with caveats:** <what's possible if a limitation is stated alongside>

**Cannot support:** <what someone will ask for that this can't answer, and why>
```

## 2 — The cleaning log → `2_Outputs/.agents/L1.3-Data-Audit/Cleaning-Log.md`

One row per change. This is the file that gets pulled up when someone challenges a number.

```markdown
---
type: cleaning-log
session: L1.3-Data-Audit
source_file: <original>
output_file: <original-stem>-clean.csv
date: <today>
---

# Cleaning Log — <file name>

Source: `<original path>` (unmodified)
Output: `<clean path>`
Rows in: <n>  →  Rows out: <n>

| # | Column | Change | Rows | Rule applied | Reason | Decided by |
|---|---|---|---|---|---|---|
| 1 | month | Normalized 4 date formats to ISO | 195 | Parse each format, output YYYY-MM-DD | Sorting and grouping were wrong | agent, mechanical |
| 2 | month | Dropped 1 invalid date (2022-13-01) | 1 | Unparseable, no recoverable value | Cannot infer intended month | Jordan — "not worth chasing one row" |
| 3 | revenue_usd | Stripped $ and commas, cast to number | 195 | Remove [$,], parse float | Column was text; averages failed | agent, mechanical |
| 4 | revenue_usd | Excluded 1 value "1.2M" | 1 | Ambiguous unit, could be 1.2M or 1,200,000 | Unresolvable without the source system | Jordan — "flag it, don't guess" |
| 5 | region | Trimmed whitespace, title-cased | 23 | strip() + title() | 4 spellings of 4 regions inflated the group count | agent, mechanical |
| 6 | (rows) | Removed 3 exact duplicate rows | 3 | All fields identical | Double-paste during close | Jordan |
| 7 | nps_score | Added `nps_missing` flag, kept blanks | 216 | New boolean column | Non-response correlates with churn; imputing would erase it | Jordan — "the silence is the signal" |

## Changes considered and rejected

| Proposed | Why not |
|---|---|
| Impute mean NPS for the 216 blanks | Non-response is informative here; mean-filling biases the churn model toward engaged accounts |
| Drop the West outlier month | Real bulk order. Removing it would hide the largest single event in the series |

## Reproducibility

Every change above is deterministic and applies to the source file as delivered. Re-running the
same rules on the same source produces the same output.
```

## 3 — The verdict, in chat

Three lines, plain language, no file paths:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA VERDICT — <file name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Can support:        <e.g. monthly trend by region, YoY comparison>
With caveats:       <e.g. seasonality — 4 years is 4 observations per month>
Cannot support:     <e.g. weekly forecasting, channel-level margin>

Cleaned file:       <n> rows, <n> changes, all logged.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 4 — The essence into ground truth

`util_get_org_info` `set(04_Data, …)`, under a stable header:

```markdown
## Data Quality Notes

**<file name>** — one row per <grain>, <coverage>. Cleaned <date>; log at
`2_Outputs/.agents/L1.3-Data-Audit/Cleaning-Log.md`.
Known limitations: <the one or two that will matter again>.
```
