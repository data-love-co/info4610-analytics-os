# Output Format

## 1 — What to show in chat

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FEEDBACK SYNTHESIS — <source>, <n> responses
Question asked: "<the exact survey question>"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Theme                    n     %      Sentiment
  1. Reporting gaps       58   26%     ██████████  negative
  2. Pricing and value    51   23%     █████████   negative
  3. Onboarding           44   20%     ████████    mixed
  4. Support quality      37   17%     ███████     mixed
  5. Reliability          21    9%     ████        split
     Uncoded / unclear    11    5%

  Denominator: 222 responses with usable content (of 240 received).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHERE IT SPLITS
  Onboarding dominates for accounts under 6 months (61% of that group).
  Pricing dominates past 2 years (44%). Different problems, different
  fixes, and they're currently averaged together in the overall ranking.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IN THEIR WORDS

  Reporting gaps
    "Cannot schedule a recurring report to my leadership team,
     which is the whole job."                    — Manager, 1-2 years
    "I export to Excel to do anything real."     — Director, 2+ years
    Dissent: "Dashboards are fine for what I need." — Analyst, <6mo

  Pricing and value
    …

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT THIS CAN'T TELL YOU
  • Who didn't respond, and whether they'd say something different
  • What people do, as opposed to what they say
  • Whether these themes are growing — this is one survey wave
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Does this match your read? Anything you'd merge or split?
```

## 2 — The deliverable → `2_Outputs/.agents/Use-Case/Feedback-Synthesis.md`

```markdown
---
type: feedback-synthesis
session: L2.1
source: <file>
responses: <n received> / <n usable>
themes: <n>
date: <today>
---

# Feedback Synthesis — <source>

## What was asked

> "<the exact question wording>"

<One line on why the wording matters for how to read the results.>

## Who answered

- **Responses:** <n> received, <n> with usable content, <n> blank or non-substantive
- **Response rate:** <x>% of <population>, if known
- **Composition:** <breakdown by role, tenure, segment>
- **Known skew:** <who is over- or under-represented, and what that likely does to the results>

## Themes

| # | Theme | n | % of usable | Sentiment | Definition |
|---|---|---|---|---|---|

**Uncoded:** <n> (<x>%) — <what they were: too short, off-topic, genuinely ambiguous>

## Codebook

### <Theme name>
- **Definition:** …
- **Includes:** …
- **Excludes:** … *(and where those went instead)*

## Cross-tabs

### Theme by <dimension>

| Theme | <seg A> | <seg B> | <seg C> |
|---|---|---|---|

*Cell counts: <n> / <n> / <n>. <Note where counts are too small to read.>*

## Representative quotes

### <Theme>
> "<verbatim>" — <segment attribution>, `R-2014`
> "<verbatim>" — <segment attribution>, `R-2087`
>
> **Dissent:** "<verbatim>" — <segment>, `R-2109`

## What this suggests

<Two or three paragraphs. Clearly separated from the section above — that section is what people
said, this section is your reading of it.>

## What this cannot tell you

<Non-response, stated vs. revealed preference, single wave, question framing. One paragraph.>

## Ranked for action

If the decision frame asked what to fix first:

| Rank | Theme | Frequency | Severity | Rationale |
|---|---|---|---|---|

**Ranking method:** <frequency / frequency × severity / frequency within the deciding segment> —
stated explicitly, because different rankings give different answers.
```

## 3 — The coded data → `2_Outputs/.agents/Use-Case/Feedback-Coded.csv`

Every response with its ID, original text, assigned themes, and sentiment. This file is what makes
the synthesis auditable — anyone can filter it and check that a theme with 58 responses has 58
responses.

| response_id | text | theme_1 | theme_2 | sentiment | segment | rating |
|---|---|---|---|---|---|---|

**Check for personal identifiers before writing this file.** Open-ended text is where people write
names, account numbers, and their own contact details. Mask before it lands anywhere tracked.

## 4 — The essence into ground truth

`util_get_org_info` `set(07_Insights, …)`:

```markdown
## Insights

- **<date>** — <source> synthesis (<n> responses): top themes <a> (<x>%), <b> (<y>%), <c> (<z>%).
  Splits by <dimension>: <the one sentence that matters>.
  Detail at `2_Outputs/.agents/Use-Case/Feedback-Synthesis.md`.
```
