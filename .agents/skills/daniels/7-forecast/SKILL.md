---
name: forecast
description: >
  Turns monthly or weekly history into a forecast with trend, seasonality, and honest uncertainty
  bands — validated against a naive baseline so you know whether the model earns its complexity.
  Use when: "forecast next quarter", "project demand", "what will sales be", "budget projection",
  "how many people will we need", "extrapolate this trend", "is this seasonal". Session L2.1. Make
  sure to use this skill whenever a decision depends on what a number will be in a future period.
---

# forecast — Forecast with Uncertainty Bands

You are producing a number someone will be held to. Treat it that way.

Two disciplines separate a forecast from a guess with a chart: **it beats a naive baseline on data
it hasn't seen**, and **it comes with an interval that reflects real error, not a decoration around
the line**. Skip either one and you've produced a shape, not a forecast.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("forecast")`), then pull:

- **The decision frame** *(primary)* — it tells you the horizon that matters and the tolerance.
  Forecasting 24 months out when the decision is about next quarter wastes the accuracy you have.
- **The audit** *(primary)* — `2_Outputs/.agents/L1.3-Data-Audit/`. **Forecasting is the use case
  most damaged by unaudited data.** A duplicate row becomes a spike; a missing month becomes a
  cliff; four date formats becomes a scrambled sequence. If no audit exists, run `data-audit`
  first. Say this plainly rather than proceeding.
- **The series** *(primary)* — `5_Library/sources/processed/`, or
  `5_Library/sample-data/regional_sales_monthly.csv` for practice.
- **Org ground truth** *(supplementary)* — via `util_get_org_info`; `06_Constraints` may hold known
  future events the history can't know about.

## Phase 1 — Look at the series before modeling it

Plot it. Describe what you see in plain language, and get the user to confirm or correct it:

- **Trend** — direction, and whether it's roughly linear or compounding
- **Seasonality** — a repeating within-year pattern, and how many full cycles the history contains
- **Level shifts** — a step change with a business cause (a price change, a system migration, an
  acquisition, a definition change caught in the audit)
- **One-off events** — the outliers the audit flagged, with their explanations
- **Recency** — has the pattern changed in the last few periods?

Then ask the question the data can't answer: *"Is anything happening in the forecast window that
the history doesn't know about?"* A signed contract, a discontinued product, a planned campaign, a
competitor entering. **A model cannot know this and will be confidently wrong about it.** Capture
these as named adjustments, applied on top of the model and shown separately from it.

## Phase 2 — Count your observations honestly

Before choosing a method, state what the history actually supports.

**The rule that saves people:** for monthly seasonality, you need at least two full years, and
three is better. With four years of monthly data you have 48 observations — but only **four
observations of each December.** Any seasonal factor you estimate rests on four numbers. Say this
out loud; it calibrates everything downstream.

Then match the horizon to the history. Forecasting 12 months from 18 months of data is
extrapolation dressed as analysis. A reasonable default: forecast no further than a third of your
history, and less if the series is volatile.

## Phase 3 — Baseline first, always

**Before any model, compute the naive baselines.** They are the bar:

- **Last value** — next period equals this period. Astonishingly hard to beat for short horizons.
- **Seasonal naive** — next period equals the same period last year. The right baseline for
  anything with a yearly pattern.
- **Moving average** — the last k periods averaged.
- **Drift** — last value plus the average change per period.

Any model that doesn't beat these on held-out data is worse than useless, because it costs more to
maintain and it invites more trust. Report the comparison honestly, including when the naive
baseline wins. **When it wins, use it.** "The best forecast is last year's number plus 6%" is a
completely respectable finding and it will still be accurate next year.

## Phase 4 — Choose a method and backtest it

**Load `reference/method-selection.md`** for the decision table and implementations. Match the
method to the history you actually have, not the sophistication you'd like to display.

Then **backtest**: hold out the last several periods, fit on the rest, forecast forward, and
measure the error. Report MAPE (mean absolute percentage error) or MAE, alongside the same number
for each naive baseline. One holdout window is a start; rolling-origin evaluation across several
windows is much more honest and costs a few extra lines of code.

**Backtest error is where the uncertainty band comes from.** Not from a formula, not from a default
setting — from how wrong this method was on this series when it didn't know the answer.

## Phase 5 — Build the interval, and say what it means

Report a central forecast and an interval. Then state, in one sentence, what the interval means and
what it excludes:

> *"The 80% band means that if the future behaves like the past, roughly 8 times out of 10 the
> actual lands inside it. It does not account for anything the history hasn't seen — a new
> competitor, a recession, or the contract you're about to sign."*

That second sentence is what keeps a forecast from being used as a promise.

**The interval widens with horizon.** If it doesn't in your output, something is wrong. Month one
is much more knowable than month twelve, and the picture should show it.

## Phase 6 — Apply known adjustments separately

Take the named future events from Phase 1 and apply them on top of the model output, shown as their
own line item:

```
Model base                    $1.42M
+ Contract signed 8/2         + $180K   (known, contract value ÷ 12)
- Product X discontinued      - $ 65K   (known, trailing 3-mo average)
= Adjusted forecast           $1.54M    (range $1.21M – $1.87M)
```

Never bury an adjustment inside the model. Someone will ask which part is math and which part is
judgment, and they're entitled to the answer.

## Closing

**Load `reference/output-format.md`** and:

1. Show the forecast table, the backtest comparison against baselines, and the chart in chat.
2. State the accuracy in words the user can repeat: *"On the last twelve months this method was off
   by about 7% on average. Treat the forecast as roughly ±14% at three months out."*
3. Ask what they know that the data doesn't. Re-run with adjustments.
4. Quietly write `2_Outputs/.agents/Use-Case/Forecast.md`.
5. Fold the headline into `util_get_org_info` (`set(05_Stakeholders, …)` is not it —
   use `set(07_Insights, …)`).

## Guardrails

- **Never publish a forecast without a backtest against a naive baseline.** If the model loses,
  report that and use the baseline.
- **Never publish a point forecast without an interval.** A single line implies a certainty nobody
  has.
- **Never claim seasonality from fewer than two full cycles.** With three years you have three
  observations of each month; say so rather than presenting a seasonal factor as established.
- Never forecast further than the history supports, even when asked. Offer the shorter horizon and
  explain what breaks past it.
- Never let a model absorb a known future event silently — adjustments are line items.
- Don't reach for a complicated method when the simple one wins the backtest. Sophistication that
  doesn't improve accuracy is a maintenance liability.
- If the series has a level shift the audit couldn't explain, **stop and resolve it.** Forecasting
  across an unexplained structural break produces a number with no meaning.
- The user owns the forecast. Show your work so they can defend it when the actual comes in
  different — and it will.
