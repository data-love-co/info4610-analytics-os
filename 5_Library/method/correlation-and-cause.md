# Correlation and Cause

Someone says "X drives Y." Almost always, what they have is "X and Y move together." The gap between
those two statements is where a lot of money gets spent badly.

---

## Why this matters more than it sounds

The failure is not academic. It's concrete and it repeats:

A churn model finds that support tickets predict churn. Someone proposes making tickets harder to
file. Ticket volume drops, churn doesn't move, and the team has destroyed its own early-warning
signal.

The model was right — tickets *do* predict churn. It was never evidence that tickets *cause* churn,
and acting on it as though it were cost them the one thing the model was actually good for.

---

## Four reasons X and Y move together

1. **X causes Y.** What everyone assumes.
2. **Y causes X.** Reverse causation, and more common than people expect. Do support tickets cause
   churn, or do customers who are already leaving file more tickets?
3. **Something else causes both.** A confounder. Usage decline causes both the ticket spike and the
   churn; neither causes the other.
4. **Chance.** With enough variables, some will correlate. Test twenty things and one will look
   significant at the 5% level, by construction.

An observed association is consistent with all four. The data alone cannot distinguish them.

---

## What would establish cause

**Experiment.** Randomly assign the intervention, compare outcomes. Randomization is what breaks the
link between the treatment and everything else — it's the whole reason experiments work. This is the
gold standard and it's usually more achievable than people assume: pilot with a random subset of
accounts rather than the ones your team likes.

**Natural experiment.** Something outside your control assigned the treatment in a way unrelated to
the outcome — a policy change, a staggered rollout, a system outage that hit some regions. Weaker,
but often available when a real experiment isn't.

**Careful observational design.** Difference-in-differences, matching, instrumental variables,
regression discontinuity. These can support causal claims, but each rests on assumptions you have to
state and defend. They are not "controlling for confounders in a regression," which is much weaker
than it sounds.

**Not evidence of cause:** a big coefficient, a small p-value, a plausible mechanism, or a strong
prior belief. Those make a hypothesis worth testing. They don't test it.

---

## How to say it correctly

**Instead of:** "Support tickets drive churn."
**Say:** "Accounts with more support tickets churn at about three times the rate. That's an
association — we haven't established that tickets cause churn, and reducing tickets wouldn't
necessarily reduce churn."

**Instead of:** "The training program improved retention 12%."
**Say:** "People who took the training retained 12 points better. They also self-selected into it,
so some of that gap is likely who they already were. To separate the two, we'd need to assign
training randomly."

**Instead of:** "Our top driver of conversion is email engagement."
**Say:** "Email engagement is the strongest predictor in the model. That's likely partly because
people already intending to buy open more emails — the arrow may run the other way."

The pattern: state the association, name the alternative explanation, say what would settle it.

---

## When a predictive model is enough

Not every analysis needs causation, and pretending otherwise is its own error.

**Prediction is sufficient when you're deciding who to look at.** A churn model that ranks accounts
is useful regardless of causation — you're using it to allocate attention, not to intervene on a
driver. "Call these fifty accounts" needs no causal claim at all.

**Causation is required when you're deciding what to change.** Any recommendation of the form "if we
do X, Y will improve" is a causal claim and needs causal evidence.

**The line, stated plainly:**

- Fine: *"The model says call these accounts."*
- Not established: *"The model says reducing tickets will reduce churn."*

Say which one you're making. Every time.

---

## Two things worth knowing

**Simpson's paradox.** A relationship can reverse when you disaggregate. A treatment can look worse
overall and better in every single subgroup, if the subgroups differ in size and baseline risk.
Whenever an aggregate result surprises you, break it down before you believe it.

**Regression to the mean.** Extreme values tend to be followed by less extreme ones, with no
intervention at all. Target your worst-performing region, do something, and it improves — that would
likely have happened anyway. This is why "we intervened on the worst cases and they got better" is
weak evidence, and why a control group matters even when it feels wasteful.

---

## The practical upshot

When a model surfaces drivers, the most valuable next step is usually not a bigger model. It's an
experiment on the top driver.

That's a concrete, cheap, and unusually persuasive recommendation to put in a memo: *"Days since
last login is the strongest signal. Before we build a re-engagement program around it, let's run it
on a random half of the flagged accounts for a quarter and see whether it actually moves anything."*
