# Hypothesis Testing, in Business Terms

You're comparing groups and you want to know whether a difference is real. That's the whole subject.

---

## Two questions, not one

People collapse these constantly, and almost every misread of a test result comes from it.

**1. Is it real?** Could a difference this size plausibly have appeared by chance if there were no
true difference? That's statistical significance.

**2. Is it big enough to matter?** Given what it costs to act, is this difference worth acting on?
That's practical significance, and no statistical test will answer it — it requires knowing the
business.

A result can be highly significant and commercially irrelevant: with 500,000 users you can detect a
0.02 percentage point lift that isn't worth the engineering. It can also be economically enormous
and statistically inconclusive: a 40% improvement on a sample of 30. **Answer both, separately.**

---

## What a p-value actually says

> If there were truly no difference, how often would we see a gap at least this large, just from
> random variation?

p = 0.02 means: about 2 times in 100. That's it.

**What it does not say:**

- Not the probability that your hypothesis is true
- Not the probability the result is a fluke
- Not the size of the effect — a tiny p-value can accompany a trivial difference
- Not that the finding will replicate

**The 0.05 threshold is a convention, not a law of nature.** p = 0.049 and p = 0.051 are essentially
the same evidence. Treating one as a discovery and the other as a failure is the single most
distorting habit in applied statistics.

**Report the effect size and its interval first. The p-value second.** The interval tells you what
you learned; the p-value tells you one narrow thing about chance.

---

## "Not significant" is not "no effect"

This is the most consequential misreading in the whole subject, and it happens in real meetings
weekly.

Two very different situations produce the same "not significant" label:

**Narrow interval containing zero.** "The difference is +0.05pp, CI [-0.10, +0.20]." You have
genuinely ruled out anything meaningful. **This is a real finding and it's worth publishing** — it
saves the organization from building something that doesn't work.

**Wide interval containing zero.** "The difference is +0.8pp, CI [-1.2, +2.8]." You learned almost
nothing. The effect could be substantially positive, substantially negative, or absent.

Calling both "not significant" and both "it didn't work" is how organizations discard good ideas and
learn nothing from expensive tests. **Say "inconclusive"** for the second case, and report how much
data would settle it.

---

## Choosing the test

| Comparing | Groups | Test |
|---|---|---|
| Proportions (converted yes/no) | 2 | Two-proportion z-test |
| Proportions | 3+ | Chi-square test of independence |
| Means (revenue, time, score) | 2 | Welch's t-test |
| Means | 3+ | **One-way ANOVA**, then pairwise with a correction |
| Means, two factors | any | Two-way ANOVA |
| Same subjects, before and after | 2 | Paired t-test |
| Heavily skewed outcome | 2 | Mann-Whitney, or bootstrap |

**Use Welch's t-test by default** rather than the equal-variance version. It costs essentially
nothing when variances are equal and protects you when they aren't — and nobody checks.

---

## Why ANOVA exists

With three or more groups, running every pairwise comparison inflates your false-positive rate.
Three groups is three comparisons and about a 14% chance of at least one false positive at α = 0.05.
Five groups is ten comparisons and roughly 40%.

ANOVA tests the whole set at once: **are all the group means equal?** A significant result says at
least one group differs. It does not say which — that's what the post-hoc test (Tukey, Bonferroni)
is for, and post-hoc tests apply a correction precisely because you're making many comparisons.

**Read the output like this:**

- **F statistic** — the ratio of variation *between* groups to variation *within* groups. Large F
  means the groups differ by more than the internal noise would explain.
- **p-value** — if all groups truly had the same mean, how often would we see spread this large?
- **η² (eta-squared)** — the share of total variance explained by group membership. **Report this.**
  A significant F with η² = 0.01 means the groups differ reliably and it explains 1% of what's going
  on, which is a very different message from significance alone.

---

## The multiple-comparisons problem, generally

Every additional comparison is another chance at a false positive. This applies far beyond ANOVA:

- Testing five segments after a null result
- Trying four metrics until one is significant
- Peeking at a test daily and stopping when it looks good

All three inflate the false-positive rate, sometimes dramatically. All three are extremely common.

**The practical defenses:**

1. **Declare the primary metric before the data comes in.** One metric. Everything else is
   exploratory and gets labeled as such.
2. **Say how many comparisons you made.** It lets the reader calibrate.
3. **Treat post-hoc findings as hypotheses for the next test**, never as conclusions from this one.

**Never let a segment rescue a failed test.** "It didn't work overall but it worked on mobile" is the
most common way experiment programs fool themselves. If mobile looks promising, the honest next step
is a mobile-targeted test — not a reinterpretation of the one that failed.

---

## Power, and the question worth asking

Power is the probability of detecting an effect that's genuinely there. Low power means an
inconclusive result even when the effect is real.

The useful move: when a result is inconclusive, don't report "not significant." Report **how much
data would settle it.**

For proportions, roughly:

```
n per arm ≈ 16 × p(1-p) / (minimum detectable effect)²
```

At a 4% baseline detecting a 0.5 percentage point difference: about 24,600 per arm for 80% power.

*"To detect the effect you'd care about, this needs about 25,000 per arm. You ran 8,600. That's six
more weeks at current traffic — or pick a bigger change to test."* That sentence is often the most
actionable output of a failed experiment.

---

## What tests can't do

- **They can't fix a broken design.** If assignment wasn't random, no test makes the comparison
  causal.
- **They can't tell you the effect will persist.** A two-week test measures two weeks.
- **They can't tell you it will generalize** to other segments, seasons, or markets.
- **They can't establish cause from observational data.** For that you need an experiment, or a
  serious causal design and a set of assumptions you're willing to defend.
