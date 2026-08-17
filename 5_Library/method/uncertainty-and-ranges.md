# Uncertainty and Ranges

**The rule: never give a single number where a range belongs.**

A forecast, a scenario output, a model score, and a survey percentage are all estimates. Presenting
one as a fact is the most common way analysis misleads people, and it's usually accidental — the
range existed in the analysis and got dropped somewhere between the spreadsheet and the slide.

---

## Why the range is the honest part

"The new pricing yields $2.4M" and "the new pricing yields somewhere between $0.9M and $3.1M, most
likely around $2.4M" are the same analysis. The first will be quoted for a year and treated as a
commitment. The second tells the reader how much weight the number can bear.

The width of the range is itself information. A tight range says you know something. A wide one says
the decision is being made under real uncertainty — which is often the single most useful thing the
analysis can tell anyone.

---

## Where uncertainty comes from

Four sources, and they need different treatment:

**Sampling.** You measured some, not all. A survey of 240 people, an A/B test of 8,600 visitors. This
one is calculable — confidence intervals exist for exactly this.

**Estimation.** The model is approximate. Forecast error, model residuals. Measurable by backtesting
— hold out data the model hasn't seen and see how wrong it was.

**Assumption.** Somebody guessed. Attrition, adoption, competitor response. Not calculable; must be
elicited as a range and labeled as judgment.

**Structural.** The model might be wrong about how the world works. Not quantifiable at all — and
this is why "the model says" is never a complete answer. Name the structural assumptions and let the
reader judge them.

The first two are what statistics handles. The last two are where analyses actually go wrong, and
they're addressed by writing things down, not by computing.

---

## Three ways to express a range

**Confidence interval.** "The lift is +0.73pp, 95% CI [+0.12, +1.34]." Precise, standard, and
routinely misunderstood — including by people who use the term. The honest plain-language version:
*"a range that's consistent with what we observed."*

**Scenario range.** "Between $0.9M and $3.1M depending on downgrade rate." Better for models built
on assumptions, because it names what the range depends on rather than implying a probability
nobody computed.

**Probability of an outcome.** "There's a 23% chance this doesn't clear the hurdle rate." Usually the
most decision-relevant framing there is, when you can compute it. Executives handle this better
than any interval.

---

## What a confidence interval does and doesn't mean

Worth getting right, because the wrong version gets said out loud in meetings constantly.

**What it means, in practice:** the range of values consistent with the data you observed. If the
procedure were repeated many times, about 95% of the intervals it produced would contain the true
value.

**What it does not mean:** "there's a 95% chance the true value is in this range." That's a different
claim about a fixed unknown quantity, and while the distinction rarely changes a business decision,
the sloppy version is the one that gets challenged by the person in the room who did study this.

**What it definitely does not cover:** anything other than sampling variation. Not bias, not a broken
data pipeline, not the possibility that the population changes next quarter. A confidence interval
is narrow in scope, and its narrowness is routinely mistaken for completeness.

The safe plain-language phrasing: *"the range that's consistent with our data."*

---

## Rounding

Precision beyond what the data supports is a form of lying, and it's the tell that gives away
somebody who hasn't thought about their inputs.

If attrition is "somewhere between 10 and 20 percent," the output is not $2,847,193. It's "about
$2.8M." If your sample is 240 people, a percentage to one decimal is already overstating.

**Rule of thumb:** two significant figures for anything with real uncertainty. Match the precision of
the output to the precision of the least certain input.

---

## When they ask for one number

They will. The honest response is to give them the base case **with the range attached in the same
breath**, every time:

> $2.4M (range $0.9M – $3.1M)

Say once, plainly: *"The range is the honest part. If the parenthetical gets dropped on the way to
the slide, the number stops being true."* Then let it go. It's their meeting and they know their
audience.

What you should not do is drop the range yourself to make the answer cleaner. That's how a model
becomes a promise, and the person who has to explain the miss is you.
