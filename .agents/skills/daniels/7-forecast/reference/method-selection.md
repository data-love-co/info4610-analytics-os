# Choosing a Forecast Method

Load at Phase 4. Match the method to the history you have, not to the sophistication you'd like to
display.

---

## The decision table

| History available | Pattern | Use | Why |
|---|---|---|---|
| < 12 periods | anything | Naive or drift, **plus a written caveat** | There is no seasonality to find and barely a trend. Say so. |
| 12–23 periods | trend, no clear season | Linear trend or simple exponential smoothing | Not enough cycles to estimate seasonality |
| 24+ periods | clear yearly season | Seasonal naive, or Holt-Winters (additive) | Two cycles is the practical minimum for seasonal factors |
| 36+ periods | season + trend | Holt-Winters, or seasonal decomposition + trend | Three cycles makes the seasonal estimate meaningfully more stable |
| Any | driven by a known external variable | Regression on the driver | If you can forecast the driver better than the outcome |
| Weekly with multiple cycles | week + year | Prophet-style decomposition, or per-week seasonal naive | Multiple overlapping seasonalities need explicit handling |

**Default for a business monthly series with 3+ years: seasonal naive with drift as the baseline,
Holt-Winters as the candidate.** Backtest both. Use whichever wins. It is very often the baseline.

---

## The baselines — implement these first

```python
# Seasonal naive: this month next year = this month last year
def seasonal_naive(series, season=12, h=6):
    return [series[-season + i] if -season + i < 0 else series[-1] for i in range(h)]

# Seasonal naive with drift: adds the average year-over-year change
def seasonal_naive_drift(series, season=12, h=6):
    yoy = [series[i] - series[i - season] for i in range(season, len(series))]
    drift = sum(yoy) / len(yoy)
    return [series[-season + i] + drift for i in range(h)]

# Naive: tomorrow is today
def naive(series, h=6):
    return [series[-1]] * h
```

Three functions, no dependencies. Beating these is the entire test.

---

## Holt-Winters, in plain terms

Three components updated each period: **level** (where the series is now), **trend** (how fast it's
moving), and **seasonal** (the repeating offset for each position in the cycle). Each has a
smoothing parameter between 0 and 1 controlling how quickly it adapts.

- **Additive seasonality** — the seasonal swing is roughly the same size in dollars regardless of
  level. December is always about $200K above the trend.
- **Multiplicative seasonality** — the swing scales with the level. December is always about 20%
  above the trend. **Choose this when the series is growing and the seasonal peaks grow with it** —
  which is most revenue series.

Pick by looking at the plot: if the seasonal swings get visibly bigger as the series grows, it's
multiplicative.

`statsmodels` has `ExponentialSmoothing` if it's available. It usually isn't on a work laptop, and
it doesn't have to be — the baselines above plus a fitted trend get you most of the way, and they
are far easier to explain in a meeting, which matters more than the last two points of accuracy.

---

## Backtesting properly

**One holdout is a start. Rolling origin is honest.**

```python
def rolling_backtest(series, method, h=3, min_train=24):
    """Refit at each origin, forecast h ahead, collect errors."""
    errors = []
    for t in range(min_train, len(series) - h + 1):
        train, actual = series[:t], series[t:t + h]
        pred = method(train, h=h)
        errors += [(a - p) / a for a, p in zip(actual, pred) if a]
    return errors

mape = sum(abs(e) for e in errors) / len(errors)
```

Report for every candidate **and** every baseline:

| Method | MAPE (3-mo horizon) | MAE | Beats seasonal naive? |
|---|---|---|---|
| Seasonal naive | 8.4% | $94K | — |
| Seasonal naive + drift | 6.9% | $77K | yes |
| Holt-Winters (mult.) | 6.6% | $74K | marginally |

In a table like that, the honest recommendation is seasonal naive with drift. Holt-Winters buys
0.3 percentage points of accuracy for real added complexity and a model somebody has to maintain.
**Say that out loud** — it's the kind of judgment the exercise is meant to teach.

**Which error metric:** MAPE is intuitive and travels well in a meeting, but it breaks near zero
and punishes under-forecasting less than over-forecasting. MAE is in the units of the thing, which
executives often prefer. Report both when it's cheap.

---

## Building the interval from backtest error

The defensible interval comes from observed error, not from a distributional assumption.

1. Collect backtest errors **separately for each horizon step** — one-step-ahead errors, two-step,
   three-step. They grow, and the interval should reflect that.
2. For each step, take the empirical percentiles of the error distribution — the 10th and 90th for
   an 80% band.
3. Apply those to the point forecast for that step.

```python
# errors_by_step[1] = list of one-step-ahead percentage errors, etc.
lo = point * (1 + percentile(errors_by_step[step], 10))
hi = point * (1 + percentile(errors_by_step[step], 90))
```

This produces bands that widen naturally with horizon, because the errors do. If your interval is
the same width at month one and month twelve, it wasn't built from data.

**With very little history**, there aren't enough backtest errors to take percentiles of. Say so,
use a wider heuristic band, and label it as a rough estimate rather than an empirical one.

---

## Traps

| Trap | What happens | Fix |
|---|---|---|
| Fitting on all data, reporting in-sample fit | The model looks excellent and forecasts badly | Always hold out; report out-of-sample error only |
| Forecasting across an unexplained level shift | The model averages two different regimes | Resolve the shift first, or forecast only the current regime |
| Seasonality from one cycle | A single unusual December becomes "the seasonal pattern" | Require two cycles; state how many you have |
| Extrapolating a compounding trend far out | Exponential growth forever | Cap the horizon; sanity-check against capacity constraints |
| Ignoring a known future event | Model can't see the signed contract | Apply as a labeled adjustment, outside the model |
| Forecasting a ratio directly | Noisy denominators make ratios wild | Forecast numerator and denominator separately, then divide |
| Treating the point forecast as the deliverable | The interval gets dropped en route to the slide | Put the range in the same cell, the same sentence, every time |
| Over-tuning to the backtest | Parameters picked to win the holdout, then failing live | Prefer the simpler method when errors are close |
