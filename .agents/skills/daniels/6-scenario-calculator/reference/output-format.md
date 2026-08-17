# Output Format

## 1 — What to show in chat

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENARIO MODEL — <decision>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE MODEL
<outcome> = <the equation, in words>

SCENARIOS
                        Downside      Base        Upside
  Option A            $  <low>    $ <base>    $ <high>
  Option B            $  <low>    $ <base>    $ <high>
  Do nothing          $  <low>    $ <base>    $ <high>

WHAT DRIVES IT
  <assumption 1>   ████████████████████   ± <swing>
  <assumption 2>   ████████               ± <swing>
  <assumption 3>   ███                    ± <swing>

  → This decision is a bet on <top driver>. The rest barely moves it.

BREAK-EVEN
  Option A pays for itself if <driver> stays above <value>.
  For reference, it has been <historical context>.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASSUMPTIONS — argue with these
  <name>   <low>–<high>  (expected <x>)   source: <history / quote / judgment / GUESS>
  …
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If a Monte Carlo was run, add:

```
DISTRIBUTION (10,000 runs)
  10th pct  $<x>   median  $<x>   90th pct  $<x>
  Probability of <threshold event>: <n>%
```

## 2 — The deliverable → `2_Outputs/.agents/Use-Case/Scenario-Calculator.md`

```markdown
---
type: scenario-model
session: L2.1
decision: <one line from the L1.2 frame>
date: <today>
---

# <Decision> — Scenario Model

## The question this answers

<One line, from the decision frame.>

## Model structure

<outcome> = <equation in words>

| Term | Type | Value / range | Source |
|---|---|---|---|
| Price per seat | lever | $149 / $169 / $189 | scenario input |
| Downgrade rate | assumption | 8% – 22% (exp. 13%) | 3 yrs history, `accounts-clean.csv` |
| Fully loaded cost | constant | $74,240 | Finance, 2026 rate card |
| Approved reqs | constraint | max 5 | Q3 budget |

## Assumption register

| Assumption | Low | Expected | High | Basis | Confidence |
|---|---|---|---|---|---|
| Downgrade rate | 8% | 13% | 22% | 3 years of renewals | Grounded in history |
| Competitor response | none | partial match | full match | Judgment — <name> | **Guess. No data.** |

Label guesses as guesses. This table is the honest part of the model.

## Scenarios

| Scenario | Option A | Option B | Do nothing |
|---|---|---|---|
| Downside | | | |
| Base | | | |
| Upside | | | |

**How downside was constructed:** <which assumptions were moved and why those move together>

## Sensitivity

| Assumption | Range tested | Outcome swing | Rank |
|---|---|---|---|

**Reading:** <the one sentence about what this decision is actually a bet on>

## Break-even

| Option | Breaks even when | Current value | Headroom |
|---|---|---|---|

## What this model cannot tell you

<Interactions not modeled, second-order effects, anything the data doesn't cover. One paragraph.>

## Recommendation input

<Not the recommendation — that's the decision memo's job. What the model contributes to it:
which option dominates, under what conditions, and what would need to be true for the other to win.>

## Build spec

**Surface:** <interactive artifact with sliders / Excel with an input block / Python script>
**Levers exposed:** <which inputs the user should be able to change live>
**Outputs shown:** <base + range, always together>
**Refresh:** <one-time or maintained>
```

## 3 — The essence into ground truth

`util_get_org_info` `set(07_Insights, …)`:

```markdown
## Insights

- **<date>** — <decision> hinges on <top driver>, currently <value>. Break-even at <value>.
  Model at `2_Outputs/.agents/Use-Case/Scenario-Calculator.md`.
```

If the model revealed a constraint worth remembering, also `set(06_Constraints, …)`.

## 4 — If they want one number for a slide

They will ask. Give them this, not a bare figure:

```
$2.4M   (range $0.9M – $3.1M)
```

And say once, plainly: *"The range is the honest part. If the parenthetical gets dropped on the way
to the slide, the number stops being true."* Then let it go — it's their meeting.
