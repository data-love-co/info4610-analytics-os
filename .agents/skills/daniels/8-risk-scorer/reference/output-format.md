# Output Format

## 1 — What to show in chat

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RISK SCORE — <outcome>, <window>
Model: <method>   ·   Trained on <n> cases   ·   Base rate <x>%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEAKAGE CHECK
  Excluded: <feature> — <why it wouldn't exist at scoring time>
  Clean:    <n> features retained

DOES IT WORK?
  AUC (out of time)     0.78
  Existing rule (no login 60d)   AUC 0.64      ← the bar
  At the top 50 accounts:
    23 real risks, 27 false alarms   (46% precision)
    catches 32% of all churn         (3.1x lift over random)

WHERE TO SET THE LINE
  Top  25   →  14 real,  11 false   ·  20% of churn caught
  Top  50   →  23 real,  27 false   ·  32% of churn caught   ← your capacity
  Top 100   →  37 real,  63 false   ·  52% of churn caught

TOP DRIVERS  (associations, not causes)
  1. Days since last login    45+ days → ~3x base rate
  2. Support tickets (90d)    each ticket → ~1.5x odds
  3. Plan = Basic             ~1.9x odds vs Standard
  4. NPS not answered         ~1.6x odds vs answered

  → The model says WHO to call. It does not say why, and it does not
    say that changing these changes the outcome.

TOP 10 RIGHT NOW
  ACC-10422   0.81   silent 71d · 6 tickets · Basic
  …
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Does this list look right to you? You know these accounts.
```

That last question is not a courtesy. Domain review catches errors no metric will.

## 2 — The deliverable → `2_Outputs/.agents/Use-Case/Risk-Scorer.md`

```markdown
---
type: risk-model
session: L2.1
outcome: <event, precisely defined>
window: <prediction window>
method: <model>
auc: <out-of-time>
date: <today>
---

# <Outcome> Risk Model

## The decision this serves

<From L1.2. Include the action that follows a high score and the team's capacity.>

## Outcome definition

- **Event:** <exactly what counts — not "churn" but "did not renew within 90 days of renewal date">
- **Window:** <period>
- **Population:** <who's in, who's excluded and why>
- **Scoring point:** <when the score is used — this defines which features are legitimate>

## Leakage review

| Feature | Verdict | Reason |
|---|---|---|
| `cancellation_reason` | **Excluded** | Only populated after the outcome |
| `days_since_last_login` | Kept | Available at scoring time |

**Snapshot rule:** every feature computed from data available as of <date/rule>.

## Model

**Method:** <logistic regression / other>. **Why:** <interpretability, calibration, fit>

| Model | AUC (out of time) | Precision @ 50 | Recall @ 50 |
|---|---|---|---|
| Existing rule | | | |
| Logistic regression | | | |
| <alternative> | | | |

**Validation:** trained on <period>, tested on <period>. Out-of-time split.

## Performance at the operating threshold

<Confusion matrix, precision, recall, lift — with each translated into a sentence about work.>

## Calibration

<Decile table, or a plain statement: "well calibrated" / "ranks are reliable, probabilities are not
— do not quote them as percentages".>

## Drivers

| Rank | Feature | Direction | Rough magnitude |
|---|---|---|---|

**These are associations.** <The caveat paragraph, in full, so it travels with the document.>

**To establish cause:** <the experiment that would test it — this is often the best next project>

## Threshold and capacity

| Cutoff | Cases flagged | Real | False | Recall | Team capacity fit |
|---|---|---|---|---|---|

**Recommended:** top <n>, because <capacity reason>.

## What this model cannot do

<Population it doesn't cover, drift risk, what would break it. One paragraph.>

## Fairness and use limits

<If the scores could affect a person's employment, credit, housing, or service access — say so
here, explicitly, and flag that adverse-impact review is outside this exercise's scope.>

## Monitoring

**Recheck when:** <drift condition — base rate shifts, a product change, a quarter passes>
**Watch:** <the metric that tells you the model is decaying>
```

## 3 — The scored list

Write `2_Outputs/.agents/Use-Case/Risk-Scores.csv` — every case with its score, rank, and the two
or three features driving it. **Include the reason columns.** A list of IDs and probabilities gets
ignored; a list with "silent 71 days, 6 tickets" gets worked.

## 4 — The essence into ground truth

`util_get_org_info` `set(07_Insights, …)`:

```markdown
## Insights

- **<date>** — <outcome> model: AUC <x> out of time, beats the existing <rule> baseline (<y>).
  Top drivers: <a>, <b>, <c> — associations only. Top <n> list covers <z>% of expected <outcome>.
  Detail at `2_Outputs/.agents/Use-Case/Risk-Scorer.md`.
```
