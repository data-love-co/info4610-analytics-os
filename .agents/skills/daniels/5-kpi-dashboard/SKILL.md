---
name: kpi-dashboard
description: >
  Turns a messy spreadsheet into a clean executive dashboard — the handful of metrics that actually
  matter, defined precisely, plus a short "so what" summary that says what to do about them. Use
  when: "build me a dashboard", "make this spreadsheet presentable", "what are our numbers",
  "leadership wants a scorecard", "visualize this data", "monthly business review deck". Session
  L2.1. Make sure to use this skill whenever someone wants to see where things currently stand
  across several measures.
---

# kpi-dashboard — Executive KPI Dashboard

You are building the thing an executive looks at for ninety seconds before a meeting. That
constraint drives every choice: few metrics, unambiguous definitions, obvious direction of travel,
and a sentence at the top that says what it means.

The failure mode of this use case is a beautiful dashboard nobody uses. It happens when the metrics
were chosen because they were available rather than because they inform a decision. That's what
Phase 1 is for.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("kpi-dashboard")`), then pull each source:

- **The decision frame** *(primary)* — `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md`
- **The audit** *(primary)* — `2_Outputs/.agents/L1.3-Data-Audit/Data-Audit.md` and the cleaned
  file it produced. **Use the cleaned file, not the original.** If no audit exists, say so and
  offer to run `data-audit` first — building a dashboard on an unaudited extract is how a duplicate
  row becomes a growth story.
- **The data** *(primary)* — `5_Library/sources/processed/`, or `5_Library/sample-data/
  regional_sales_monthly.csv` for practice.
- **Org ground truth** *(primary)* — via `util_get_org_info`, especially `03_Metrics` (existing
  definitions) and `05_Stakeholders` (who's reading this).
- **User profile** *(supplementary)* — via `util_get_user_info`. Technical comfort decides where
  this gets built.

## Phase 1 — Choose the metrics (the part that matters)

**Load `reference/metric-selection.md`** and work through it with the user. The output is five to
seven metrics, each with a written definition, a direction, and a comparison.

Two rules to hold:

- **Every metric answers "so what?"** For each candidate, ask: *"If this number moved 20% next
  month, what would someone do differently?"* If the answer is "nothing," it's context, not a KPI.
  Context can go in a supporting section; it doesn't get a tile.
- **Five to seven, not fifteen.** More tiles means less attention per tile. If the user wants
  fifteen, ask which three they'd look at first in a crisis, and build outward from those.

Write each definition down explicitly, including the denominator. "Retention" is not a definition.
"Logo retention: accounts active at period end ÷ accounts active at period start, excluding
accounts that never onboarded" is.

## Phase 2 — Compute, with the comparison built in

A number alone is not information. Every metric needs at least one comparison — versus last period,
versus the same period last year, versus target, or versus the rest of the portfolio. Pick the
comparison that matches how the decision gets made.

While computing:

- **Respect the audit.** If the audit flagged a column as unreliable, either don't use it or show
  it with the caveat attached to the tile.
- **State the window.** "Last 12 months" and "year to date" produce different numbers and different
  conclusions. Put the window on the dashboard, not just in your head.
- **Handle the outliers explicitly.** If a single event distorts a metric, show the metric with and
  without it, or annotate it. Never quietly exclude.
- **Round to the precision the decision needs.** `$1.2M`, not `$1,247,382.19`.

## Phase 3 — Write the "so what"

Three to five sentences at the top of the dashboard. This is the part people actually read.

Structure it as: **what changed → why it likely changed → what it means for the decision.**

- Lead with the largest real movement, not the first metric alphabetically.
- Separate what the data shows from what you infer. "Revenue is down 8% in the South" is a fact.
  "Likely driven by the September outage" is an inference, and it gets labeled as one.
- Name what you can't tell from this data. One line.
- End on the decision from L1.2, if there is one. "On the staffing question: the backlog trend
  supports the contractor bridge over hiring, unless Q4 volume comes in below the forecast."

**Never write a "so what" that just restates the tiles.** "Revenue was $4.2M, up 6%" is a caption.
"Growth is holding, but it's all coming from one region, which makes the number more fragile than
it looks" is a so-what.

## Phase 4 — Build it

Ask where it should live, or read `02_Expertise` and recommend. Load
`5_Library/build-surfaces/Choosing-Your-Surface.md` for the routing. Short version:

| Their situation | Build in |
|---|---|
| Lives in Excel, needs to hand it to someone who also lives in Excel | Excel / Sheets, with formulas visible |
| Wants something to show once, in a meeting | An artifact or a single HTML file |
| Needs it to refresh every month with new data | Claude Code — a script plus a rendered page |
| Their org runs Tableau / Power BI | Build the logic and definitions here; hand the spec over |

Then hand off to **`build-and-ship`** for the actual build, or build it directly if the surface is
simple. Follow `5_Library/method/chart-choices.md` for chart selection — the dataviz rules there
are not decoration, they're what makes a dashboard readable in ninety seconds.

## Closing

**Load `reference/output-format.md`** and:

1. Show the metric set with definitions and the "so what" in chat, so the user can react to it
   before anything is built.
2. Ask what's missing and what they'd cut. Adjust, re-show, repeat.
3. Quietly write `2_Outputs/.agents/Use-Case/KPI-Dashboard.md` — the metric definitions, the
   computed values, the "so what," and the build spec.
4. Fold the metric definitions into ground truth via `util_get_org_info` (`set(03_Metrics, …)`).
   Definitions outlive dashboards; this is the durable part.

## Guardrails

- **Never show a metric you can't define.** If the definition is contested inside the organization,
  put both definitions on the dashboard or pick one and label it. Ambiguity in a KPI is not a
  rounding error; it's the reason two teams report different numbers to the same executive.
- **Never present a computed number without its window and its comparison.**
- Never let the chart choice fight the message — see `5_Library/method/chart-choices.md`. No pie
  charts with eight slices, no dual axes implying a relationship that isn't there, no truncated
  y-axis that turns a 2% move into a cliff.
- Don't build fifteen tiles because fifteen metrics exist.
- If the underlying data can't support a metric the user wants, say so and offer the nearest thing
  it can support.
- The "so what" is written by you but owned by the user. Show it, let them argue with it, revise.
  They're the one who has to defend it.
