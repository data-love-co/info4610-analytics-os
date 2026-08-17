# Coding Method

Load at Phase 2. Three passes. The third is what makes the counts trustworthy.

---

## Pass 1 — Open coding

Read every response. Tag each with one or more short descriptive labels, close to the respondent's
own language. Don't organize yet; don't judge yet.

```
R-2014  "Setup took three weeks longer than we were told."
        → [onboarding-delay] [expectation-mismatch]

R-2015  "The per-seat price is hard to justify when half our seats are read-only."
        → [pricing-model] [seat-based-pricing] [value-perception]

R-2016  "Support responds fast but escalations disappear for days."
        → [support-responsiveness+] [escalation-process-] [mixed]
```

Rules for this pass:

- **Stay close to their words.** `[seat-based-pricing]` not `[monetization-strategy]`. Abstracting
  too early is how you end up with themes that describe your assumptions rather than their input.
- **Multiple labels are normal.** People raise more than one thing in a sentence.
- **Mark mixed sentiment when you see it.** "X is great but Y is broken" is one of the most
  informative shapes a response takes and it gets flattened if you force a single valence.
- **Don't skip the boring ones.** "It's fine" is data — it's the middle of the distribution, and
  the middle is usually underrepresented in what people remember from reading feedback.

---

## Pass 2 — Build the codebook

Group the labels into themes. For each theme, write:

| Element | Example |
|---|---|
| **Name** | Pricing and value perception |
| **Definition** | Comments about cost, pricing structure, or whether the product justifies its price |
| **Includes** | Per-seat model, renewal increases, tier structure, value-for-money |
| **Excludes** | Billing errors and invoicing problems (those go to Billing Operations) |
| **Source labels** | `[pricing-model]`, `[seat-based-pricing]`, `[renewal-increase]`, `[value-perception]` |

**The definition and the exclusions are what make the count mean something.** "Pricing: 62
responses" is uninterpretable without knowing whether billing complaints are in there.

**Target five to nine themes.** If a theme covers more than ~40% of responses, split it — it's
absorbing everything and telling you nothing. If a theme has three responses, ask whether it's a
theme or an interesting individual comment. Both are worth reporting; only one gets a row in the
frequency table.

**Watch for the two axes problem.** Sometimes responses vary along two independent dimensions — say
*what part of the product* and *what kind of problem*. If your themes keep overlapping, you may be
trying to collapse two dimensions into one list. Code both and cross-tab them; it's usually the
better analysis.

---

## Pass 3 — Recode

Go back through every response and apply the codebook consistently. This pass exists because pass 1
labels drift — a response coded early gets a different label than an identical response coded
later, once you've seen more.

Track and report:

- **Responses recoded** — a measure of how much pass 1 drifted
- **Residual** — responses that fit no theme. Report this number honestly. Coding 100% of responses
  into a tidy five-theme structure almost always means the fit was forced.
- **Ambiguous** — responses where you genuinely couldn't tell what was meant. Also a real number.

---

## Sentiment

Assign per response, or per theme-within-response when they differ:

| Value | Meaning |
|---|---|
| Positive | Clearly favorable |
| Negative | Clearly unfavorable |
| Mixed | Both, explicitly — "great CSM, terrible reporting" |
| Neutral | Factual, a feature request with no valence, a description |

**Be honest about the method.** You are reading and judging. That's legitimate qualitative practice
and it's what you're doing — say so rather than implying a computed score.

**Cross-check against any rating field.** Where the stated rating and the text sentiment disagree,
look closer. A 9/10 rating attached to a paragraph of complaints usually means the person likes the
relationship and hates one specific thing, and that distinction matters enormously for what to do
about it.

---

## What to cross-tab

The single-column frequency table is the least interesting output. The insight is almost always in
the cross-tabs:

| Cross-tab | What it usually reveals |
|---|---|
| Theme × rating | Which complaints actually drive dissatisfaction versus which are grumbles from happy users |
| Theme × tenure | Onboarding problems concentrate early; value problems concentrate at renewal |
| Theme × role | What an analyst hates and what a VP hates are different, and they have different budget authority |
| Theme × segment | Enterprise and SMB usually have inverted priority lists |
| Theme × time | Whether a theme is growing — the most decision-relevant cut, and the one that needs multiple survey waves |

Report a cross-tab only where cell counts support it. Six responses split across four segments is
not a finding; it's noise with a table around it. State the cell counts.

---

## Frequency, honestly

**Always state the denominator.** These are three different numbers and they get confused
constantly:

- % of all responses received (including blanks) — the most conservative
- % of responses with any usable content — usually the right default
- % of responses that mentioned this topic area at all — the narrowest, and easy to misread

**Don't over-read small differences.** With 240 responses, a theme at 26% and one at 22% are not
meaningfully different. Report the counts and let the reader see the scale rather than ranking
noise.

**Frequency is not importance.** Ten people mentioning a data-loss bug matters more than sixty
mentioning the color scheme. When the decision is "what do we fix first," rank by frequency ×
severity, or by frequency within the segment that drives the decision — and say which ranking you
used.
