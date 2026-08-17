# The Seven Check Families

Run in order. Earlier checks change what later ones find — deduplicate before you compute an
outlier threshold, or the duplicates skew it.

---

## 1. Missingness

**Count it per column**, then ask the question that matters: *is it missing at random?*

- Cross-tab missingness against the outcome or key segment. If rows missing `nps_score` churn at
  38% and rows with it churn at 19%, the blanks carry information and imputing the mean destroys it.
- Look for **structural** missingness — a field that's only populated for some record types. That
  isn't a defect; it's a grain problem in disguise.
- Look for **six ways of writing nothing**: empty, `N/A`, `n/a`, `-`, `null`, `NULL`, `unknown`,
  a single space, `0` where zero means "not recorded." Count them together or your missing count is
  wrong.
- Check whether missingness clusters in time. Blanks concentrated in one quarter usually mean a
  system change, not random loss.

**Never impute without surfacing it.** Options are always: impute (say with what and why), flag and
keep, or exclude. Each has a cost; state all three.

---

## 2. Types and formats

The most common defect and the easiest to miss, because spreadsheets display things helpfully.

- **Numbers stored as text** — currency symbols, thousands separators, trailing spaces, `1.2M`,
  parentheses for negatives `(1,234)`. Any one of these silently turns a column into text, and
  averages computed on it either fail or quietly exclude rows.
- **Percent as text** — `18%` is a string. `0.18` and `18` are different numbers. Find out which
  the source meant.
- **Dates** — the classic. Multiple formats in one column, two-digit years, Excel serial numbers
  (`45231`), text like `Jan 2022` that has no day, and dates that don't exist (`2022-13-01`).
  Ambiguous `01/02/2022` is January 2 or February 1 depending on where the file was made; if the
  file has any day above 12, you can infer the convention. If it doesn't, ask.
- **Leading zeros lost** — ZIP codes, account numbers, employee IDs. `01234` became `1234` when
  someone opened it in Excel, and it can't be recovered by guessing.
- **Booleans** — `Yes`/`yes`/`Y`/`TRUE`/`1` in one column.

---

## 3. Duplicates

- **Exact duplicate rows** — every field identical. Usually a double-paste or a re-run of an
  export. Almost always safe to drop, but count and report them.
- **Duplicate on the key** — same `account_id`, different values. Never drop blindly. Ask which is
  correct, or whether the grain is actually finer than assumed (one row per account, or one per
  account per month?).
- **Near-duplicates** — `Acme Corp`, `Acme Corp.`, `ACME Corporation`. These inflate counts and
  split aggregations. Surface the candidate groups; let the user confirm the matches. Fuzzy
  matching without confirmation creates errors that are very hard to find later.

---

## 4. Outliers

**The rule: investigate, don't delete.** An outlier is a question, not a defect.

Find them with more than one lens, because each catches different things:

- More than 3 standard deviations from the mean — only meaningful if the distribution is roughly
  normal. Revenue and account size usually aren't; they're right-skewed, and this method will flag
  perfectly ordinary large customers.
- Outside 1.5 × the interquartile range — more robust for skewed data, and the better default here.
- Impossible on its face — negative counts, percentages above 100, a tenure longer than the
  company has existed, a date in the future.

For each one, ask: **is there an explanation?** Check the `notes` column, check whether it's one
row or a cluster, check whether the same period is odd in other columns.

Three kinds and three responses:

| Kind | Example | What to do |
|---|---|---|
| Data error | Decimal slip, unit mismatch, `1.2M` in a number column | Fix if the correct value is knowable; exclude and log if not |
| Real but exceptional | Bulk order, outage, one enormous customer | **Keep it.** Consider reporting with and without it |
| Real and routine | Long tail of a skewed distribution | Keep. The distribution is the finding — say so |

---

## 5. Categorical drift

One concept, several spellings. Computers treat them as different values; humans reading the
dashboard never notice.

- Case: `West` / `WEST` / `west`
- Whitespace: `West ` / ` West`
- Synonyms: `Mid-Market` / `Midmarket` / `MM`
- Renamed over time: a segment renamed in 2024 appears as two categories across the history
- Free-text where a dropdown should have been: 40 spellings of six real values

List the distinct values with counts. The count column makes the answer obvious — six values with
hundreds of rows each and eleven with three rows each is a spelling problem, not a taxonomy.

---

## 6. Logical and referential consistency

Cross-column checks. These catch things no single-column profile will.

- **Ordering** — start date after end date, renewal before signup, "days since last login" larger
  than tenure.
- **Arithmetic** — do components sum to the total? Does revenue minus returns match net revenue
  where both are present?
- **Range by category** — a value that's plausible overall but impossible for its segment.
- **Referential** — IDs in this file that don't exist in the file they're supposed to join to.
  Check the join before you build on it; a silent 30% drop in an inner join has ended more analyses
  than bad math.
- **Coverage** — every period present? A missing month in a monthly series will read as a
  catastrophic decline on any chart that doesn't fill gaps.

---

## 7. Definition drift

The hardest to detect, because the data looks fine. Something changed about what a column *means*,
partway through the history.

Signals to look for:

- A level shift with no business explanation — a step change in a metric at a specific date, with
  no corresponding event
- A column that's empty before a date and populated after — the field was added
- A distribution that changes shape at a boundary — a category that starts or stops appearing
- Values that suddenly get more precise, or less

Then ask the human question: *"Did the way you count this change at any point? A system migration,
a new definition, a reorg that moved accounts between segments?"* Almost every organization has one
of these, and almost nobody documents it.

**When it's confirmed:** the honest options are to analyze only the consistent period, restate the
history if the mapping is knowable, or split the analysis at the break and compare cautiously.
Analyzing across an undocumented break and presenting it as a trend is how a career-limiting slide
gets made.

**`03_Metrics` in `0_Org/` is where the answer often lives** — if the bootstrap captured the
organization's metric definitions, check the column against them. If two teams define the same
metric differently, that's a finding worth its own line in the audit.
