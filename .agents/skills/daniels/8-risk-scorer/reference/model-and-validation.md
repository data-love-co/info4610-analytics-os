# Modeling and Validation

Load at Phases 2 and 4.

---

## Leakage

A feature is leakage if it would not be available, populated, and correct **at the moment the score
is used**. Leakage is the single most common reason a model that tested beautifully fails in
production, and it is almost always discovered after someone has presented the results.

### The five checks

**1. The availability test.** For each feature ask: *would this be filled in, right now, for a case
that hasn't had the outcome yet?* In the practice data, `cancellation_reason` fails — it exists
only for accounts that already cancelled. So does anything named `*_date` that refers to the
outcome, and any status field updated by the process you're predicting.

**2. The suspiciously good test.** Fit a model on each feature individually. Any single feature
producing AUC above ~0.90 on its own is leakage until proven otherwise. Real business drivers land
in the 0.55–0.75 range individually.

**3. The missingness test.** Cross-tab each feature's missingness against the outcome. If a feature
is present for 100% of churned accounts and 2% of retained ones, its *presence* encodes the answer
— and a model will learn that even if you never look at the values.

**4. The timestamp test.** Any field derived from an event at or after the outcome. Final invoice
amount, offboarding survey, the last support ticket. All leakage.

**5. The aggregate test.** A feature computed over a window that includes the outcome period.
"Average monthly usage" computed over all history includes the months after churn (which are
zeros), so it encodes churn. Compute features over a window that ends **before** the prediction
point.

### The fix

Rebuild every feature as of a **snapshot date** that precedes the outcome window. If you're
predicting churn in the next 90 days, every feature is computed from data available as of day zero
— nothing after. This is more work than it sounds and it is the difference between a model and a
demonstration.

---

## Class imbalance

Most outcomes worth predicting are uncommon. Churn at 15%, default at 3%, conversion at 8%.

**What breaks:** accuracy. A model predicting "no" for everything is 97% accurate on a 3% base rate
and completely useless. Never report accuracy alone on imbalanced data.

**What to report instead:**

- **AUC** — probability the model ranks a random positive above a random negative. Insensitive to
  base rate, good for comparing models. Also somewhat abstract for a business audience.
- **Precision at k** — of the top k cases you'd actually work, how many are real? The most
  business-legible metric there is, because k is a real number of hours.
- **Recall at k** — of all the positives out there, what share does the top k catch?
- **Lift** — how much better than random. "The top 10% of the list contains 34% of all churn — 3.4x
  lift" is a sentence executives immediately understand.

**On resampling (SMOTE, class weights, undersampling):** it changes the ranking very little and it
destroys calibration, so predicted probabilities stop meaning anything. For a ranked-list use case,
skip it. Rank the raw probabilities and set the threshold from capacity.

---

## Validation

### Split correctly

**Out of time.** Train on cases whose outcome window closed earlier; test on later. Anything else
lets the model learn from the future through correlated cases, shared seasonality, or a company-wide
event that touched all accounts in the same month.

A random split on time-dependent data typically overstates performance by a wide margin, and the
gap doesn't reveal itself until the model is live.

### Report the confusion matrix at the operating point

Not at 0.5 — at the threshold set by capacity in Phase 5.

```
                     Predicted churn    Predicted stay
  Actually churned         23  (TP)          48  (FN)
  Actually stayed          27  (FP)         342  (TN)

  Precision  23/50  = 46%   → of 50 calls, 23 are real risks
  Recall     23/71  = 32%   → catches about a third of churn
  Lift       46%/15% = 3.1x → vs. calling accounts at random
```

Translate every one into a sentence about work. "Precision 0.46" means nothing to a VP of Support.
"Of the fifty accounts your team calls, about twenty-three are genuinely at risk" means everything.

### Check calibration

Bucket predictions into deciles. In each bucket, compare mean predicted probability to actual
outcome rate. They should track.

```
  Predicted 0.05–0.15  →  actual 0.11   ok
  Predicted 0.15–0.25  →  actual 0.19   ok
  Predicted 0.25–0.35  →  actual 0.41   over-fires
```

Miscalibration is tolerable if the score is only ever used to rank. It is not tolerable the moment
someone says "this account has a 60% chance of churning" in a meeting — and someone always does.
Either fix it or state clearly that the numbers are ranks, not probabilities.

### Sanity checks that catch real errors

- **Does the ranking make sense to someone who knows the accounts?** Show the top 10 with reasons.
  Domain review catches errors no metric will.
- **Is any single feature carrying the model?** Drop the top feature and refit. If performance
  collapses, look again for leakage.
- **Does it beat the existing rule?** If the team already flags "no login in 60 days," compare
  directly. Sometimes the rule wins, and that's a real finding worth reporting.

---

## Reading logistic regression coefficients

For a business audience, convert to odds ratios and speak in relative terms.

```
coefficient  0.42  on support_tickets_90d
odds ratio   e^0.42 = 1.52
```

Say: *"Each additional support ticket in the last 90 days is associated with roughly 50% higher
odds of churn, holding the other factors constant."*

Three things to watch:

1. **Scale matters.** A coefficient on a variable measured in dollars is not comparable to one on a
   0–10 scale. Standardize before comparing magnitudes, or report the effect of a realistic change
   ("going from 1 ticket to 5") rather than a one-unit change.
2. **Correlated features split credit.** If logins and days-since-login are both in the model, each
   gets part of the effect and both coefficients shrink. Don't read either as the standalone
   importance of usage.
3. **"Holding the other factors constant" is doing real work in that sentence** — and in the real
   world nothing is held constant. It's a statement about the model, not about the business.

---

## The causal line

Say this every time, in some form:

> These are associations. The model tells you **who** to look at. It does not tell you **why**, and
> it does not tell you that changing the driver changes the outcome.

The concrete failure this prevents: a churn model finds support tickets predict churn, so someone
proposes making tickets harder to file. Ticket volume drops, churn doesn't, and the team has
destroyed its own early-warning signal.

**What would establish causation:** an experiment. Intervene on a random subset of high-scoring
accounts, leave the rest as a control, compare outcomes. That's the `ab-test-readout` skill, and
proposing it is often the most valuable thing this analysis produces.
