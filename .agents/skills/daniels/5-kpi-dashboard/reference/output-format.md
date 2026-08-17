# Output Format

## 1 — What to show in chat

Show this before anything gets built, so the user can argue with the metric set while it's still
cheap to change.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DASHBOARD — <title>
Window: <period>   ·   Source: <file>   ·   As of: <date>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SO WHAT
<3-5 sentences: what changed, why it likely changed (labeled as
inference), what it means for the decision, what this data can't tell you.>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  <Metric 1>          <value>     <comp> vs <prior>   ▲ good
  <Metric 2>          <value>     <comp> vs target    ▼ watch
  <Metric 3>          <value>     <comp> vs LY        — flat

  <Metric 4>          <value>     <comp>
  <Metric 5>          <value>     <comp>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEFINITIONS
  <Metric 1>  <numerator> ÷ <denominator>, <filter>, <window>
  <Metric 2>  …
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CAVEATS
  • <what the audit flagged that affects a tile>
  • <what this dashboard cannot tell you>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 2 — The deliverable → `2_Outputs/.agents/Use-Case/KPI-Dashboard.md`

Written quietly. This is the durable artifact — the definitions outlive whatever gets built.

```markdown
---
type: kpi-dashboard
session: L2.1
decision: <one line from the L1.2 frame>
source_file: <path>
window: <period>
date: <today>
---

# <Title> Dashboard

## So what

<The 3-5 sentence summary. Facts and inferences separated.>

## Metrics

| # | Metric | Value | Comparison | Direction | Owner |
|---|---|---|---|---|---|
| 1 | | | | higher is better | |

## Definitions

### <Metric 1>
- **Numerator:** …
- **Denominator:** …
- **Excludes:** …
- **Window:** …
- **Source:** …
- **Note:** <if the organization defines this more than one way, say so here>

## Context (not KPIs)

<Metrics that failed the "so what" filter but are worth having nearby.>

## Caveats and limitations

| Item | Effect on the dashboard |
|---|---|
| <audit finding> | <which tile it touches and how> |

## What this cannot tell you

<One short paragraph. The questions someone will ask that this dashboard can't answer.>

## Build spec

**Surface:** <Excel / artifact / Claude Code / hand to BI team>
**Refresh:** <one-time / monthly, and who does it>
**Layout:** <top three large, next four smaller, definitions in a footer>
**Charts:** <chart type per metric, per 5_Library/method/chart-choices.md>
**Inputs:** <file(s) and the columns each tile needs>
```

## 3 — The essence into ground truth

`util_get_org_info` `set(03_Metrics, …)` — the definitions, under a stable header. This is the part
that compounds: the next analysis reads these instead of re-litigating what "retention" means.

```markdown
## Metric Definitions

**<Metric>** — <numerator> ÷ <denominator>, <filter>, <window>. Source: <system>.
Owner: <role>. <Note any competing definition in use elsewhere in the org.>
```

Also `set(07_Insights, …)` if the dashboard surfaced something worth remembering:

```markdown
## Insights

- **<date>** — <the finding, one line, with the number in it>
```
