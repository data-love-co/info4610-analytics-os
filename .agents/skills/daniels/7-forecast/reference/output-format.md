# Output Format

## 1 — What to show in chat

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORECAST — <series>, <horizon>
Method: <chosen>   ·   History: <n> periods (<start> to <end>)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Period      Forecast      80% range          vs LY
  2026-09     $1.42M        $1.28M – $1.57M    +6.1%
  2026-10     $1.51M        $1.33M – $1.72M    +5.4%
  2026-11     $1.68M        $1.44M – $1.95M    +7.2%

  Adjustments applied
    + Contract signed 8/2        + $180K   (known)
    - Product X discontinued     - $ 65K   (known)

DID IT EARN ITS KEEP?
  Seasonal naive          MAPE 8.4%
  Seasonal naive + drift  MAPE 6.9%   ← chosen
  Holt-Winters            MAPE 6.6%   (0.3pp better, materially more complex)

WHAT THIS MEANS
  On the last <n> months this method missed by about <x>% on average.
  Treat the 3-month forecast as roughly ±<2x>%.

WHAT IT DOESN'T KNOW
  <Anything the history can't see. One or two lines.>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 2 — The deliverable → `2_Outputs/.agents/Use-Case/Forecast.md`

```markdown
---
type: forecast
session: L2.1
series: <what is being forecast>
horizon: <n periods>
method: <chosen method>
mape: <out-of-sample>
date: <today>
---

# Forecast — <series>

## The decision this serves

<One line from the L1.2 frame, including the horizon that actually matters.>

## What the history shows

- **Coverage:** <n> periods, <start> to <end>
- **Trend:** <direction and shape>
- **Seasonality:** <pattern>, based on **<n> full cycles** — that is <n> observations of each month
- **Level shifts:** <any, with cause>
- **Outliers:** <from the audit, with explanations and how they were handled>

## Method

**Chosen:** <method>. **Why:** <one sentence, referencing the backtest>

| Method | MAPE | MAE | Notes |
|---|---|---|---|
| Naive | | | baseline |
| Seasonal naive | | | baseline |
| Seasonal naive + drift | | | |
| <candidate> | | | |

Validation: rolling origin, <n> windows, <h>-period horizon, minimum training window <n>.

## Forecast

| Period | Forecast | 80% low | 80% high | vs prior year |
|---|---|---|---|---|

**How the interval was built:** empirical percentiles of out-of-sample backtest error at each
horizon step. It widens with horizon because the errors do.

## Known adjustments

| Adjustment | Amount | Basis | Applied to |
|---|---|---|---|

These sit **on top of** the model, not inside it. The model line is math; these are judgment.

## Accuracy, in plain language

<One paragraph the user can say out loud in a meeting. Include the typical miss and what that
implies for how much weight to put on the number.>

## What this forecast cannot account for

<Everything outside the history: competitive moves, macro conditions, pricing changes, product
decisions not yet made. One paragraph. This is the section that protects the user.>

## Monitoring

**Watch:** <the leading indicator that would tell you early the forecast is going wrong>
**Revisit when:** <condition — e.g. two consecutive months outside the 80% band>
```

## 3 — The chart

One chart, per `5_Library/method/chart-choices.md`:

- History as a solid line, forecast as a dashed continuation of the same line — same color, so it
  reads as one series
- The interval as a light shaded band, widening with horizon
- The vertical "today" divider labeled
- Actual values plotted over any backtest period, so a reader can see how the method did on data it
  didn't have
- Y-axis starting at zero for revenue and counts. If you truncate for a legitimate reason, mark the
  break and say why

**No second y-axis.** If two series need different scales, use two charts stacked with a shared
x-axis.

## 4 — The essence into ground truth

`util_get_org_info` `set(07_Insights, …)`:

```markdown
## Insights

- **<date>** — <series> forecast: <value> for <period>, range <low>–<high>.
  Method: <method>, out-of-sample MAPE <x>%. Full detail at
  `2_Outputs/.agents/Use-Case/Forecast.md`.
```
