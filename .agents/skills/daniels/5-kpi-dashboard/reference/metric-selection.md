# Choosing the Metrics

Load this at Phase 1. Output: five to seven metrics, each with a definition, a direction, a
comparison, and a stated owner.

---

## Step 1 — Start from the decision, not the columns

Ask: *"What decision or conversation does this dashboard support, and how often does it happen?"*

The cadence tells you the metric set. A weekly operations review needs leading indicators that move
weekly. A quarterly business review needs outcomes and trends. Putting quarterly outcome metrics on
a weekly dashboard produces a wall of numbers that never change, which teaches people to stop
looking.

## Step 2 — Generate candidates from three angles

Don't start from what's in the spreadsheet. Start from these, then check what's available:

1. **Outcome** — did the thing we care about happen? Revenue, retention, resolution time, margin.
   Usually lagging, usually what leadership asks about.
2. **Driver** — what moves the outcome? Pipeline, ticket volume, headcount, conversion rate. These
   are where action lives.
3. **Health** — what would tell us this is breaking before the outcome does? Backlog age, time to
   first response, employee attrition, data freshness.

A dashboard with only outcome metrics tells you the score after the game. One with only drivers
tells you nothing about whether it's working. Aim for a mix, weighted toward whichever the decision
needs.

## Step 3 — Apply the "so what?" filter

For each candidate, ask the user directly:

> *"If this number moved 20% next month, what would you or someone else do differently?"*

- **Concrete answer** → it's a KPI. Keep it.
- **"I'd want to look into it"** → probe once. Look into what, and then what? Sometimes there's a
  real action underneath; sometimes it's curiosity.
- **"Nothing"** → it's context. Put it in a supporting table, not on a tile.

This filter usually cuts a list of fifteen down to six, and the six are better than the fifteen.

## Step 4 — Define each one precisely

Write the definition down. Every definition needs, at minimum:

| Element | Example |
|---|---|
| Numerator | Accounts with at least one login in the period |
| Denominator | Accounts with an active contract at period start |
| Population / filter | Excludes accounts in their first 30 days |
| Window | Trailing 90 days, refreshed monthly |
| Source | `customer_accounts-clean.csv`, from the CRM export of 2026-08-01 |

**The four questions that catch most definition problems:**

1. What exactly is in the denominator? Most metric disputes are denominator disputes.
2. Gross or net? Retention, revenue, and margin all have both, and they tell different stories.
3. What's excluded, and why? Trials, internal accounts, test records, employees.
4. Point-in-time or period-average? Headcount on the last day is not average headcount.

**If two teams in the organization define this metric differently**, that's a finding. Check
`03_Metrics` in `0_Org/`. Show both, or pick one and label it prominently. Don't silently choose —
whichever one you pick, somebody in the room uses the other.

## Step 5 — Set direction and comparison

Each metric needs:

- **Direction** — is up good? Say it explicitly. "Days to resolution: lower is better" prevents the
  most common misread of a dashboard.
- **Comparison** — at least one of: prior period, same period last year, target, or peer
  group/segment. A number with no comparison cannot be interpreted.
- **Target, if one exists** — and if it doesn't, say so rather than inventing one. A made-up target
  becomes real the moment it's on a slide.
- **Threshold for attention**, if the user has one. "Flag if backlog exceeds 2,000" is more useful
  than a color gradient.

## Step 6 — Name an owner

For each metric: who is accountable for it moving? Not who reports it — who owns it. Metrics
without owners get discussed and never acted on. If nobody owns it, ask whether it belongs on the
dashboard at all.

---

## The seven-tile discipline

If the list is still long, force the ranking:

> *"You're about to walk into a meeting and you have time to look at three numbers. Which three?"*

Those three go at the top, large. The next few go below, smaller. Everything else goes in a
supporting table or gets cut. This isn't a design preference — attention is finite and a dashboard
that doesn't rank its own contents makes the reader do the ranking, badly, under time pressure.

---

## Common traps

| Trap | Why it hurts | What to do instead |
|---|---|---|
| Metric chosen because the column exists | Optimizes for convenience, not decisions | Start from the decision, then check availability |
| Averages with no distribution | An average resolution time of 4 hours hides the 5% of tickets taking 3 days | Show median and a high percentile, or the distribution |
| Ratios without the raw counts | 100% conversion looks great until you see n=2 | Always show the denominator, at least on hover or in a footnote |
| Percentages of percentages | "Retention improved 3%" — points or percent? | State the unit: percentage points vs. relative change |
| Vanity metrics | Cumulative totals only go up. They always look good and never inform | Use period values, not running totals |
| Too many time windows at once | MTD, QTD, YTD, TTM on one screen invites comparing the wrong pair | Pick one primary window, put the rest in a secondary view |
| A target invented for the dashboard | It will be quoted back as a commitment | Use a real target or show none |
