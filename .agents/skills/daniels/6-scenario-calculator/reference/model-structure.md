# Model Structure and Uncertainty

Load at Phase 1. Covers the four term types, how to elicit a range from someone who says "I don't
know," Monte Carlo, and the traps.

---

## The four term types

Every term in the model is exactly one of these. Classify all of them before computing anything.

**Lever** — the decision-maker controls it. Price, headcount, budget, scope, timing. Levers are
what the scenarios vary. If your model has no levers, it isn't a decision model; it's a forecast.

**Assumption** — uncertain, must be estimated, nobody controls it. Attrition, demand, conversion,
adoption, competitor response. **Every assumption gets a range.** No exceptions — an assumption
with a single value is a lie about how much you know.

**Constant** — known and stable over the model's horizon. Contracted rates, statutory tax rates,
existing salaries. Cite the source. Re-check anything called a constant that's more than a year
old.

**Constraint** — a hard limit. Physical capacity, a budget ceiling, a regulatory minimum, hours in
a week. Constraints bound the output and often matter more than the assumptions: a model that
outputs "we'd need 34 FTE" is useless if the approved req count is 5. Model the constraint
explicitly rather than letting an impossible answer through.

**The classification test:** if the user says "well, it depends," it's an assumption. If they say
"we could choose either," it's a lever. If they say "that's just what it costs," ask when it was
last checked, then it's a constant.

---

## Eliciting a range from someone who says "I don't know"

People are bad at stating uncertainty when asked directly and quite good at it when asked
sideways. Use these, in order:

1. **The surprise test.** *"What number would be low enough that you'd be genuinely surprised? What
   would be high enough?"* This produces something close to an 80–90% interval and people find it
   easy to answer.
2. **The history anchor.** *"What has it been for the last four quarters?"* Then ask whether next
   period is likely to be inside or outside that spread, and why.
3. **The bet.** *"If you had to bet your own money that it lands between X and Y, how wide would X
   and Y have to be before you'd take that bet?"*
4. **The reference class.** *"What does this look like at similar companies, or for the last three
   times we did something like this?"*

**Always widen the initial answer.** People are systematically overconfident about ranges — the
well-documented pattern is that intervals people call "90% confident" contain the true value far
less often than that. When someone gives you a range, ask: *"What would have to happen for it to
land outside that?"* If they can name something plausible in ten seconds, the range is too narrow.

**Record the source of every range** in the assumption register: `history` (with the period),
`vendor quote` (with the date), `judgment` (whose), or `guess`. A model built on four historical
ranges and one guess is a different object than one built on five guesses, and the reader can only
know which if you write it down.

---

## Running the scenarios

**Base case** — every assumption at expected. This is the number people will quote. Say the range
in the same breath, every time.

**Downside and upside** — the mistake here is setting every assumption to its worst simultaneously.
If you have six independent assumptions each at their 10th percentile, the combined scenario sits
somewhere around the 0.0001 percentile. It's not a downside; it's a fantasy, and a smart reader
will dismiss the whole model because of it.

Instead: **pick the two or three assumptions that plausibly move together in a bad direction, and
move those.** Volume down and attrition up during a downturn is a coherent story. Volume down,
attrition up, rates up, ramp time up, and a hiring freeze all at once is not — unless the user says
it is, in which case it's a named crisis scenario and gets labeled as one.

**Per-option scenarios** — one run per option in the decision frame, so options are directly
comparable on the same assumptions. This is what actually answers the decision.

---

## Sensitivity analysis (the part people remember)

Vary one assumption across its full range, hold everything else at expected, record the swing in
the outcome. Repeat for each assumption. Rank by swing size.

```
Downgrade rate      (8% – 22%)     ████████████████████  ±$1.9M
Volume growth       (0% – 9%)      ████████              ±$0.7M
Attrition           (11% – 19%)    ████                  ±$0.4M
Cost to hire     ($4k – $16k)      █                     ±$0.1M
```

Then say the sentence: *"This decision is a bet on downgrade rate. The rest barely matters."*

Two things follow from a good sensitivity ranking, and both are more valuable than the base case:

1. **Where to spend research time.** One week on the top driver beats a month on the rest.
2. **What to monitor after the decision.** The top driver is the leading indicator that tells you
   early whether the decision is going the way you assumed.

---

## Monte Carlo — when it's worth it

**Worth it when:** more than three uncertain assumptions, the outcome is nonlinear (thresholds,
caps, tiered pricing), or the assumptions interact.

**Overkill when:** two or three assumptions and a linear model. Low/base/high covers it, and it's
easier to explain.

The method, in plain terms: draw a random value for each assumption from its range, compute the
outcome, repeat several thousand times, look at the distribution of results.

```python
import random, statistics

def outcome(downgrade, growth, attrition):
    ...  # the model equation from Phase 1

runs = [outcome(random.triangular(0.08, 0.22, 0.13),   # low, high, mode
                random.triangular(0.00, 0.09, 0.04),
                random.triangular(0.11, 0.19, 0.15))
        for _ in range(10_000)]

runs.sort()
print("10th pct", runs[1000], "median", statistics.median(runs), "90th pct", runs[9000])
print("chance of losing money:", sum(1 for r in runs if r < 0) / len(runs))
```

A triangular distribution (low, high, most likely) is the right default here. It takes exactly the
three numbers people can actually give you, and it doesn't pretend to knowledge of a distribution's
shape that nobody has.

**What to report:** the 10th percentile, the median, the 90th percentile, and — usually the most
decision-relevant number in the whole model — **the probability of crossing whatever threshold
matters.** "There's a 23% chance this doesn't clear the hurdle rate" lands harder than any point
estimate.

**What not to claim:** Monte Carlo does not make the assumptions more accurate. It propagates the
uncertainty you declared; it does not reduce it. If the input ranges are guesses, the output
distribution is a well-organized guess. Say so.

---

## Traps

| Trap | What it looks like | Fix |
|---|---|---|
| Double counting | A cost captured in two terms — loaded salary *and* a separate benefits line | Write the equation in words first, and read it back aloud |
| Wrong base | A percentage applied to gross where the contract says net | State the base for every rate |
| Unit mismatch | Monthly rate times annual volume | Put units in every variable name |
| Silent extrapolation | A per-unit cost from 100 units applied to 10,000 | Ask where the rate breaks down; add a constraint |
| Missing the do-nothing option | Every scenario involves acting | Always model the status quo — it's the real comparison |
| Ignoring timing | Costs land immediately, benefits land in month nine | Model the period, not just the annual total |
| Precision theater | $2,847,193 from inputs that are ±30% | Round to the precision the inputs support |
| Sunk costs in the model | Money already spent influencing a forward decision | Only forward-looking cash belongs in the comparison |
