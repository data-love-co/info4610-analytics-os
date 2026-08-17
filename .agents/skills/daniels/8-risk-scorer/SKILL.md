---
name: risk-scorer
description: >
  Scores customers, accounts, or cases on how likely an outcome is — churn, conversion, default,
  escalation — validates the model honestly, and exposes the top drivers as associations rather
  than causes. Use when: "which customers will churn", "score my accounts", "who's likely to
  convert", "predict default risk", "which deals will close", "flag at-risk accounts", "propensity
  model". Session L2.1. Make sure to use this skill whenever a decision is about which cases to act
  on first.
---

# risk-scorer — Churn / Conversion / Risk Scoring

You are producing a ranked list that changes who someone calls on Monday. Everything else about
this use case is in service of that.

Three things sink these models in the real world, and only one of them is math:

1. **Target leakage** — a column that quietly encodes the answer. The model looks brilliant in
   testing and is useless in production.
2. **No action attached** — a perfectly calibrated score nobody does anything with.
3. **Drivers read as causes** — "support tickets predict churn" becomes "stop them from filing
   tickets."

Guard all three. The math is the easy part.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("risk-scorer")`), then pull:

- **The decision frame** *(primary)* — specifically: what action follows a high score, and how many
  cases can actually be actioned. That number sets the threshold and it changes everything.
- **The audit** *(primary)* — `2_Outputs/.agents/L1.3-Data-Audit/`. Run `data-audit` first if it
  hasn't been.
- **Labeled data** *(primary)* — one row per case, with an outcome column. Practice data:
  `5_Library/sample-data/customer_accounts.csv` (which contains a deliberate leakage trap).
- **Org ground truth** *(supplementary)* — via `util_get_org_info`.

**If there's no outcome column, there is no model.** Say so immediately and offer the alternatives:
define the outcome from what's available (e.g. "no login in 90 days plus no renewal" as a churn
proxy), wait for labels to accumulate, or switch to a rules-based flag that encodes what the
business already believes. Don't build a classifier without labels and call it a prediction.

## Phase 1 — Define the outcome precisely

Before anything else, pin down four things. Ambiguity here invalidates everything downstream.

1. **What counts as the event?** Churn is not one thing. Non-renewal, cancellation, downgrade, and
   going dormant are four different events with four different models and four different responses.
2. **Over what window?** "Will churn" is unanswerable. "Will not renew within the next 90 days" is
   a question with an answer.
3. **Who's in the population?** Exclude cases that couldn't have the outcome — accounts not up for
   renewal in the window, deals already closed. Including them inflates every accuracy number you
   report.
4. **When is the score used?** This determines which features are legitimate. **Any feature not
   available at scoring time is leakage**, no matter how predictive.

## Phase 2 — Hunt for leakage before you model

**Load `reference/model-and-validation.md` § Leakage** and run the checks.

The fastest test, and the one to run first: **for each candidate feature, ask "would I have this
value, populated, for an account that hasn't churned yet?"** In the practice data,
`cancellation_reason` fails instantly — it's only filled in after cancellation. Any model including
it will score near-perfectly and predict nothing.

Other signals: a feature with implausibly high individual predictive power, a feature whose
missingness perfectly tracks the outcome, a timestamp after the event, anything created by a
downstream process.

**Say the rule out loud once:** if a model looks too good, it is. A churn model at 0.99 AUC has
leakage, not insight.

## Phase 3 — Build, simply

Start with **logistic regression**. For this audience and these decisions it is almost always the
right answer: coefficients readable as direction and rough magnitude, calibrated probabilities out
of the box, nothing to explain that can't be explained in a meeting.

Try a tree-based model as a comparison if the data warrants it, but only adopt it if it clearly
beats logistic regression on held-out data. Interpretability is a real feature here — the user has
to explain this to a VP, and "the gradient boosting ensemble said so" is not an explanation.

Also build the **rules baseline**: whatever the business already uses. "Flag accounts with no login
in 60 days." If the model doesn't beat the rule the team already follows, the honest finding is
that the rule is fine — and that's a valuable, publishable result.

## Phase 4 — Validate honestly

**Load `reference/model-and-validation.md` § Validation.** Non-negotiables:

- **Split out of time, not at random**, when the outcome unfolds over time. Train on earlier,
  test on later. A random split lets the model learn from the future.
- **Report AUC and a confusion matrix at the threshold you'll actually use.** Accuracy alone is
  meaningless with imbalanced classes — a model that predicts "no churn" for everyone is 78%
  accurate on the practice data and worth nothing.
- **Report precision and recall at the operating point**, in business terms: "of the 100 accounts
  you'd call, about 46 would actually have churned; you'd catch about a third of all churn."
- **Check calibration.** If the model says 30%, do about 30% of those cases actually churn? A
  ranked list can be useful while being badly calibrated — but only if nobody quotes the
  probabilities, and someone always does.

## Phase 5 — Set the threshold from capacity, not from statistics

The threshold is a business decision, and it is the one people get wrong.

Ask: *"How many accounts can your team actually work in a month?"* If the answer is 50, the
threshold is whatever puts 50 accounts on the list — not 0.5, and not whatever maximizes an
F1 score. Then show what that costs:

> "At the top 50, roughly 23 are genuine churn risks and 27 are false alarms. You'd catch about 31%
> of the churn that's coming. Going to the top 100 catches 52% but the hit rate drops to 38%."

If the user can quantify the cost of a miss versus the cost of a wasted call, work out the expected
value directly — that's the sharpest version of this conversation.

## Phase 6 — Explain the drivers, carefully

Report the top drivers with **direction, rough magnitude, and the association caveat attached every
single time**:

> "Days since last login is the strongest signal. Accounts silent for 45+ days churn at roughly
> three times the base rate. **This is an association, not a cause** — silence probably reflects
> disengagement that started earlier. Making people log in won't retain them; finding out why they
> stopped might."

Then draw the practical line explicitly:

- **Useful:** the score tells you who to call.
- **Not established:** that changing the driver changes the outcome.
- **What would establish it:** an experiment — intervene on a random subset, compare. Which is the
  `ab-test-readout` skill, and it's a natural next project.

## Closing

**Load `reference/output-format.md`** and:

1. Show validation results, the threshold table, and the drivers in chat.
2. **Show the top 10 scored cases with their reasons.** This is what makes the model real to the
   user — and it's where they'll spot a mistake you can't see, because they know account #4028.
3. Ask what looks wrong. Their domain knowledge is a validation set you can't compute.
4. Quietly write `2_Outputs/.agents/Use-Case/Risk-Scorer.md` and the scored list as a CSV.
5. Fold the finding into `util_get_org_info` (`set(07_Insights, …)`).

## Guardrails

- **Never ship a model without a leakage check.** State that you ran it and what you found.
- **Never report accuracy alone on imbalanced data.**
- **Never call a driver a cause.** Every driver statement carries the association caveat. Every one.
- **Never let a score reach a person as a verdict.** Scores rank cases for human attention. If the
  output could affect someone's employment, credit, housing, or access to a service, say so
  explicitly and flag that it needs review beyond this exercise — fairness, adverse-impact testing,
  and in some domains legal requirements that this workspace doesn't cover.
- Never validate on data the model trained on.
- Never tune the threshold to make the metrics look good. It comes from capacity.
- If the model doesn't beat the existing rule, say so plainly. That's a finding, not a failure.
- The user owns the list. They know which accounts are misclassified and why — listen to them.
