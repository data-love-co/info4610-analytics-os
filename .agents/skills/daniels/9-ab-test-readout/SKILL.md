---
name: ab-test-readout
description: >
  Turns raw experiment results into a full hypothesis-test readout — the right test, the effect
  size with a confidence interval, the practical-significance check, and a ship / iterate / hold
  recommendation. Use when: "we ran an A/B test", "did the campaign work", "is this difference
  significant", "compare these two groups", "read out my experiment", "did the pilot beat the
  control", "compare three regions". Session L2.1. Make sure to use this skill whenever someone is
  comparing groups and wants to know whether a difference is real.
---

# ab-test-readout — Experiment Readout

You are answering two questions that people constantly collapse into one:

1. **Is this difference real, or could it plausibly be noise?** (statistical significance)
2. **Is it big enough to act on?** (practical significance)

A result can be highly significant and commercially irrelevant. It can be economically enormous and
statistically inconclusive. The readout that serves a decision-maker answers both, separately, and
then makes a recommendation.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("ab-test-readout")`), then pull:

- **The results** *(primary)* — a file in `5_Library/sources/processed/`, pasted summary counts, or
  `5_Library/sample-data/ab_test_results.csv` for practice.
- **The decision frame** *(supplementary but valuable)* — what happens if it ships, what it costs,
  what the alternative is.
- **Org ground truth** *(supplementary)* — via `util_get_org_info`.

Summary counts are enough for a proportions test (conversions and totals per arm). Row-level data
lets you segment and check the assumptions properly. Say which you have and what it limits.

## Phase 1 — Establish what was actually run, before touching the numbers

Ask these before any test. Each one can invalidate the whole analysis, and each is more likely to
be a problem than the math.

1. **What was the hypothesis, and was it stated before the data came in?** A hypothesis formed
   after looking at the results is not a hypothesis; it's a description. It can still be worth
   pursuing — as the input to the *next* test.
2. **How were units assigned?** Random assignment is what licenses causal language. If groups were
   self-selected, assigned by region, or split by time period, this is an observational comparison
   and the readout must say so.
3. **What is the primary metric?** One. Decided in advance. If several were tracked, the others are
   secondary and get reported as exploratory.
4. **When did it stop, and why?** Stopping when the result "looked good" inflates false positives
   substantially. Ask directly and without judgment — it is extremely common.
5. **What's the unit of analysis?** Visitors, sessions, or orders? If one visitor can convert
   several times, treating orders as independent understates the variance and overstates
   significance.
6. **Was there a sample size target set in advance?** If not, note it. It doesn't invalidate the
   test, but it changes how much confidence a single result deserves.

**Load `reference/test-selection.md` § Validity checks** for the full list, including
sample-ratio mismatch — the single most useful diagnostic and the one almost nobody runs.

## Phase 2 — Pick the right test

**Load `reference/test-selection.md`** for the decision table. In brief:

| Comparing | Groups | Test |
|---|---|---|
| Proportions (converted yes/no) | 2 | Two-proportion z-test, or chi-square |
| Proportions | 3+ | Chi-square test of independence |
| Means (revenue, time, score) | 2 | Two-sample t-test (Welch's by default) |
| Means | 3+ | **One-way ANOVA**, then post-hoc pairwise with a correction |
| Means, 2 factors | any | Two-way ANOVA |
| Means, same subjects before/after | 2 | Paired t-test |
| Heavily skewed outcome | 2 | Mann-Whitney, or t-test on log values, or bootstrap |

State which you chose and why in one sentence. Check the assumptions and **say what you found** —
including when an assumption is violated and you proceeded anyway with a robust alternative.

**When there are three or more groups, do not run every pairwise t-test.** Three groups is three
comparisons and roughly a 14% chance of at least one false positive at α = 0.05; five groups is ten
comparisons and about 40%. Run ANOVA first to establish that *something* differs, then pairwise
with a correction (Tukey, or Bonferroni if you only care about a few planned comparisons).

## Phase 3 — Effect size and interval first, p-value second

Report in this order, deliberately:

1. **The observed difference**, in the units of the business. "+0.73 percentage points, from 3.97%
   to 4.70%."
2. **The confidence interval on the difference.** This is the most useful number in the readout,
   because its *width* tells you how much you actually learned. A 95% CI of [+0.12pp, +1.34pp] says
   the effect is probably real and could be anywhere from trivial to substantial.
3. **The relative change**, if it helps. "+18% relative." Always alongside the absolute — relative
   changes on small bases mislead badly.
4. **The p-value**, and what it means in one plain sentence: *"If there were truly no difference,
   we'd see a gap this large or larger about 2% of the time."*
5. **The business translation.** The interval converted into money or volume at current scale:
   "roughly $180K to $2.1M of incremental annual revenue."

**Never lead with the p-value.** It answers a narrow question that is not the one being asked.

## Phase 4 — Practical significance

This is the phase that separates a readout from a statistics exercise. Ask directly:

> *"How much would this have to move to be worth shipping — accounting for the engineering cost,
> the maintenance, and the opportunity cost of the next thing?"*

Then compare that threshold to the confidence interval:

| Situation | Recommendation |
|---|---|
| Whole CI above the threshold | **Ship.** Even the pessimistic end is worth it |
| CI straddles the threshold | **Iterate or extend.** You know the direction, not the magnitude |
| Whole CI below the threshold | **Hold.** Real, but not worth the cost. Say so plainly |
| CI includes zero, narrow | **Hold.** Genuinely no meaningful effect — a real finding, worth publishing |
| CI includes zero, wide | **Inconclusive.** Underpowered. Report what sample size would settle it |

**"Inconclusive" and "no effect" are different results and get different recommendations.** A wide
interval containing zero means you learned very little. Say that instead of "not significant," which
gets misheard as "it didn't work" roughly every time.

## Phase 5 — Segments, carefully

If asked to look at segments (device, region, new versus returning), do it — but frame it correctly:

- Segment results are **exploratory**, not confirmatory. Testing five segments means five chances
  at a false positive.
- Report them as hypotheses for the next test, not as findings.
- **Never let a segment rescue a failed test.** "It didn't work overall but it worked on mobile" is
  the most common way experiment programs fool themselves. If mobile looks promising, the honest
  next step is a mobile-targeted test, not a reinterpretation of this one.
- Say the number of comparisons out loud. It calibrates how much anyone should believe any of them.

## Closing

**Load `reference/output-format.md`** and:

1. Show the readout in chat — recommendation first, then the evidence, then the caveats.
2. Ask what the threshold for action is if they haven't said. It changes the recommendation more
   than any statistic will.
3. Quietly write `2_Outputs/.agents/Use-Case/AB-Test-Readout.md`.
4. Fold the result into `util_get_org_info` (`set(07_Insights, …)`) — including negative results.
   The organizational memory of what *didn't* work is worth as much as what did, and almost nobody
   keeps it.

## Guardrails

- **Never say "proves."** Say "the evidence supports," or "we can rule out no-effect at the 5%
  level." The distinction is not pedantry; it's what keeps a single test from becoming doctrine.
- **Never report significance without effect size and interval.**
- **Never treat a non-significant result as evidence of no effect** unless the interval is narrow
  enough to rule out a meaningful difference. Absence of evidence is not evidence of absence.
- **Never run pairwise tests across 3+ groups without a correction.** Say what correction you used.
- Never let a post-hoc segment become the headline.
- Never analyze an observational comparison in causal language. If assignment wasn't random, the
  readout says "associated with," names the plausible confounders, and stops there.
- If the test was stopped early on a peek, say so and note that the p-value is optimistic.
- If the sample ratio is off, investigate before interpreting anything else — it usually means the
  assignment or logging broke, and every other number is suspect.
