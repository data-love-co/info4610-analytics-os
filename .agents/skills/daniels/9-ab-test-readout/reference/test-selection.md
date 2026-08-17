# Test Selection and Validity

Load at Phases 1 and 2.

---

## Validity checks — run these before any test

Each of these can invalidate the analysis. They are more often the problem than the arithmetic.

### Sample ratio mismatch (run this first, always)

If the split was designed 50/50, check that it landed near 50/50. A chi-square goodness-of-fit test
against the intended ratio takes one line.

A meaningful imbalance — say 51.8/48.2 on 20,000 users — means something broke: a redirect failing
for one arm, a bot filter applied unevenly, an assignment bug, a logging gap. **When the ratio is
off, stop and investigate.** Every other number in the readout is suspect until it's explained.
This is the single highest-value diagnostic in experiment analysis and it takes ten seconds.

### Assignment

- **Random at the unit level?** Then causal language is licensed.
- **Assigned by region, team, store, or time period?** Cluster assignment. The effective sample size
  is the number of clusters, not the number of individuals, and the naive test will be dramatically
  overconfident. Say so.
- **Self-selected?** Not an experiment. It's an observational comparison, and the readout says
  "associated with," names the confounders, and does not recommend on causal grounds.

### Contamination

Did anyone see both versions? Shared accounts, multiple devices, users clearing cookies, a
switchover partway through. Contamination biases toward finding no difference, so a null result on
a contaminated test is especially weak evidence.

### Stopping rule

Ask plainly: *"How did you decide when to stop?"*

Stopping when the result looked good — "peeking" — substantially inflates the false-positive rate.
If it happened, don't discard the test; report it, note the p-value is optimistic, and treat the
result as a hypothesis worth confirming rather than a conclusion.

### Novelty and primacy effects

A change can produce a temporary bump because it's new, or a temporary dip because it's unfamiliar.
If the test ran less than two full business cycles, plot the effect by day. A trend toward zero
across the test window is a warning sign.

### Unit of analysis

If one person can appear multiple times, rows are not independent. Aggregate to the unit that was
randomized (usually the visitor) before testing. Failing to do this understates variance and
overstates significance, sometimes by a lot.

---

## The test decision table

| Outcome type | Groups | Design | Test | Notes |
|---|---|---|---|---|
| Proportion | 2 | independent | Two-proportion z-test | Needs ≥ ~10 events per arm |
| Proportion | 2 | independent, few events | Fisher's exact test | Small samples |
| Proportion | 3+ | independent | Chi-square test of independence | Then pairwise with correction |
| Proportion | 2 | paired (same units, before/after) | McNemar's test | |
| Mean | 2 | independent | **Welch's t-test** | Default. Doesn't assume equal variances |
| Mean | 2 | paired | Paired t-test | Same subjects measured twice |
| Mean | 3+ | independent, one factor | **One-way ANOVA** | Then Tukey HSD for pairwise |
| Mean | 3+ | two factors | **Two-way ANOVA** | Also tests the interaction |
| Mean | 3+ | repeated measures | Repeated-measures ANOVA | Same subjects across conditions |
| Mean | 2 | heavily skewed | Mann-Whitney U, or t-test on logs, or bootstrap | Revenue per user is almost always skewed |
| Count / rate | 2 | independent | Poisson rate test | Events per unit of exposure |
| Time to event | 2 | independent | Log-rank test | Time to churn, time to conversion |

**Why Welch's by default:** the equal-variance t-test requires an assumption that's rarely checked
and often false. Welch's costs almost nothing in power when variances are equal and protects you
when they aren't. Use it unless there's a specific reason not to.

---

## ANOVA, in plain terms

**What it does:** tests whether the means of three or more groups are all equal, using one test
instead of many pairwise ones — which is what controls the false-positive rate.

**Why not just run every pair:** with α = 0.05, three groups means three comparisons and about a
14% chance of at least one false positive. Five groups means ten comparisons and roughly 40%. The
overall test comes first for a reason.

**How to read the output for a business audience:**

- The **F statistic** is the ratio of variation between groups to variation within groups. Large F
  means the groups differ by more than the internal noise would explain.
- The **p-value** answers: if all groups truly had the same mean, how often would we see spread this
  large?
- A significant result says **at least one group differs**. It does not say which. That's what the
  post-hoc test is for.

**Post-hoc:** Tukey HSD for all pairwise comparisons; Bonferroni if you only planned a few specific
comparisons. Report the adjusted p-values and say which correction was used.

**Assumptions, and how much they matter:**

| Assumption | How to check | If violated |
|---|---|---|
| Independent observations | Think about the design, not the data | Serious. Fix the unit of analysis |
| Roughly normal within groups | Plot; or rely on large n | Mild. ANOVA is robust with decent group sizes |
| Similar variances | Levene's test, or compare group SDs | Use Welch's ANOVA, or transform |

**Effect size for ANOVA:** report eta-squared (η²) — the share of total variance explained by group
membership. A significant F with η² = 0.01 means the groups differ reliably and the difference
explains 1% of what's going on. That's a very different message from significance alone, and it's
usually the more honest one.

---

## Confidence intervals — the calculations worth knowing

**Difference in two proportions:**

```
diff = p2 - p1
se   = sqrt( p1(1-p1)/n1 + p2(1-p2)/n2 )
CI95 = diff ± 1.96 * se
```

**Difference in two means (Welch):**

```
diff = m2 - m1
se   = sqrt( s1²/n1 + s2²/n2 )
CI95 = diff ± t(df) * se        # Welch-Satterthwaite df
```

**When the outcome is skewed** (revenue per user, session duration), bootstrap the interval instead
— resample with replacement a few thousand times, take the 2.5th and 97.5th percentiles of the
differences. No distributional assumption, twelve lines of code, and it handles the long tail
honestly.

---

## Power — what it would take to settle it

When a result is inconclusive, the useful answer is not "not significant." It's **how much more
data would settle this.**

Rough sample size per arm for a proportions test:

```
n ≈ 16 * p(1-p) / (MDE)²
```

where `p` is the baseline rate and `MDE` is the minimum detectable effect in absolute terms, for
80% power at α = 0.05.

At a 4% baseline and a 0.5 percentage point MDE: n ≈ 16 × 0.0384 / 0.000025 ≈ 24,600 per arm.

That calculation is often the most actionable output of an inconclusive readout: *"To detect the
effect you'd care about, this needs about 25,000 per arm. You ran 8,600. At current traffic that's
about six more weeks — or pick a bigger swing to test."*
