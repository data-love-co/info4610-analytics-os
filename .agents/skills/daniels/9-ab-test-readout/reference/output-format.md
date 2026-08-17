# Output Format

## 1 — What to show in chat

Recommendation first. The reader decides how much of the rest they need.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXPERIMENT READOUT — <name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDATION:  ITERATE — extend the test before committing
The variant beat control by 0.65 percentage points and we can rule out
no-effect. But the pessimistic end of the range is +0.04 pp, which is
below the bar you set. We know the direction; we don't know the size.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE RESULT
                      n        conv      rate
  Control          8,600        347      4.03%
  Variant          8,600        403      4.69%

  Difference       +0.65 pp   (95% CI: +0.04 pp to +1.26 pp)
  Relative         +16.1%
  Test             two-proportion z-test,  z = 2.09,  p = 0.037

  In plain terms: if there were truly no difference, we'd see a gap
  this large or larger about 4 times in 100.

  At current volume that's roughly $10K to $2.0M incremental annual
  revenue. The width of that range is the finding.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IS IT BIG ENOUGH?
  Your threshold to ship:   +0.10 pp
  Pessimistic end of CI:    +0.04 pp     → does NOT clear it
  → Significant, but not yet decisive. Run it longer.

  Note what just happened: p = 0.037 says "real." The interval says
  "we don't know if it's worth doing." Both are true. This is exactly
  why the p-value is not the readout.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDITY
  Sample ratio     8,600 / 8,600   as designed          ok
  Assignment       random at visitor level              ok
  Duration         14 days, 2 full weekly cycles        ok
  Stopping         pre-set sample target                ok
  Primary metric   declared before launch               ok

CAVEATS
  • Two weeks. No read on whether the lift persists.
  • Order value not tested — the lift could come from smaller orders.
  • Segment results below are exploratory, not conclusions.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**When the result is inconclusive**, replace the recommendation block with this — never with the
phrase "not significant" on its own:

```
RECOMMENDATION:  INCONCLUSIVE — extend or redesign
The difference is +0.31 pp, but the range runs from -0.28 to +0.90.
That includes zero and it also includes an effect worth having.
We did not learn enough to decide.

To detect the effect you'd care about (+0.50 pp) you need roughly
24,600 per arm. You have 8,600. At current traffic, about six more
weeks — or test a bigger change.
```

## 2 — The deliverable → `2_Outputs/.agents/Use-Case/AB-Test-Readout.md`

```markdown
---
type: experiment-readout
session: L2.1
experiment: <name>
primary_metric: <metric>
recommendation: <ship | iterate | hold | inconclusive>
date: <today>
---

# <Experiment> — Readout

## Recommendation

**<SHIP / ITERATE / HOLD / INCONCLUSIVE>** — <two sentences: what to do and why>

## What was tested

- **Hypothesis:** <as stated before launch>
- **Change:** <what was different in the variant>
- **Primary metric:** <one metric, declared in advance>
- **Secondary metrics:** <tracked, exploratory>
- **Ran:** <start> to <end>, <n> days
- **Assignment:** <random at unit level / other>

## Result

| Arm | n | Events | Rate | Difference | 95% CI |
|---|---|---|---|---|---|

**Test:** <name>, <statistic> = <value>, p = <value>
**In plain terms:** <the one-sentence p-value translation>
**Effect size:** <in business units, with the interval>

## Practical significance

| Item | Value |
|---|---|
| Threshold to justify shipping | |
| Pessimistic end of CI | |
| Expected value at current scale | |
| Cost to implement and maintain | |

**Verdict:** <ship / iterate / hold, and the reasoning in one sentence>

## Validity checks

| Check | Result |
|---|---|
| Sample ratio mismatch | |
| Assignment mechanism | |
| Contamination risk | |
| Stopping rule | |
| Novelty / primacy | |
| Unit of analysis | |

## Secondary and segment results — exploratory

<n> comparisons were made. At α = 0.05 that implies roughly a <x>% chance of at least one false
positive among them. Treat everything here as a hypothesis for the next test.

| Segment | n | Control | Variant | Difference | 95% CI |
|---|---|---|---|---|---|

## What we did not learn

<Explicit. Durability, effect on order value, effect on segments not powered, downstream metrics.>

## Next

<The next test, if there is one, stated as a hypothesis with a target sample size.>
```

## 3 — The essence into ground truth

`util_get_org_info` `set(07_Insights, …)`. **Record negative and inconclusive results too** — the
organizational memory of what didn't work is worth as much as what did, and almost nobody keeps it.

```markdown
## Insights

- **<date>** — <experiment>: <result> (<effect> [CI]). Recommendation: <ship/hold/inconclusive>.
  Detail at `2_Outputs/.agents/Use-Case/AB-Test-Readout.md`.
```

## 4 — Charts

Two, at most, per `5_Library/method/chart-choices.md`:

1. **The difference with its confidence interval** — a point with error bars, and a reference line
   at zero and at the practical threshold. This single chart carries the entire readout.
2. **Cumulative rate by day per arm**, if novelty is a concern — it shows whether the effect is
   stable or fading.

**Not** a bar chart of two rates with a truncated y-axis. That is how a 0.7 percentage point
difference gets drawn as a mountain, and it is the most common misleading chart in experiment
reporting.
