# Output Format

## The memo → `2_Outputs/.agents/L2.2-Decision-Memo/Decision-Memo.md`

```markdown
---
type: decision-memo
session: L2.2-Decision-Memo
to: <reader>
from: <user>
decision_needed_by: <date>
date: <today>
---

**To:** <Name, Title>
**From:** <Name, Title>
**Date:** <date>
**Re:** <The decision, in six words or fewer>

---

## Recommendation

<3-5 sentences. The recommendation with a verb. The single strongest reason, with the
number in it. What it costs or risks. What you need from the reader, by when.>

## Why

**1. <Claim with a number in it.>**
<One or two sentences. Source. What it does and doesn't establish.>

**2. <Claim with a number in it.>**
<…>

**3. <Claim with a number in it.>**
<…>

**The strongest case against:** <The best counterargument, stated fairly, then why the
recommendation still holds — or what would have to be true for it not to.>

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## What this analysis could not determine

<One short paragraph. What data didn't exist, what the method can't answer, what
remains uncertain. Specific, not defensive.>

## Next steps

| # | Action | Owner | By |
|---|---|---|---|

**Revisit if:** <the condition that would change the recommendation>

---

*Method, data sources, and full analysis: `2_Outputs/.agents/Use-Case/<file>.md`.
Data cleaning log: `2_Outputs/.agents/L1.3-Data-Audit/Cleaning-Log.md`.*
```

**Appendix** — separate section below the memo, or a separate file. Method detail, supporting
charts, the full data table, anything a skeptical reader would want but a busy one wouldn't.

---

## Audience calibration

The same analysis produces different memos. Adjust on four dimensions, from Phase 1.

| Reader | Lead with | Include | Cut |
|---|---|---|---|
| **CFO / Finance** | The dollar impact and its range | Assumptions, sensitivity, downside case, payback | Method narrative, anything qualitative without a number |
| **Operations leader** | What changes for the team on Monday | Headcount, capacity, timeline, what breaks first | Statistical detail, model internals |
| **Your direct manager** | What you're recommending and what you need from them | More method than an exec gets — they may have to defend it upward | Background they already have |
| **A committee or board** | The decision and the two or three options | The options table, the recommendation, the dissent | Everything else. Appendix it |
| **A skeptical reader** | The recommendation, then the counterargument early | Limitations up front, method available, sources cited | Confident language the evidence doesn't support |

**When the recommendation contradicts what the reader believes:** name it in the second sentence.
*"This runs against the assumption we've been working from — the data points the other way, and
here's why."* A contrary finding discovered by the reader in paragraph six reads as an attempt to
slip it past them.

**When the reader has to carry this to someone else:** the memo has a second audience it will be
explained to secondhand. Make the recommendation and the top reason quotable, and make sure the
numbers are the kind that survive being repeated from memory.

---

## Tests — run all four before writing the file

**1. The ninety-second test.** Read only the recommendation paragraph. Could the reader act
correctly on that alone? If they'd need to read further to avoid a mistake, the paragraph is wrong.

**2. The skeptic test.** Imagine the reader's sharpest colleague reading it. What's the first
question they ask? If the memo doesn't answer it, add it. If the answer is weak, say so rather than
hoping nobody asks.

**3. The forward test.** Six months from now, the recommendation was followed and it went badly.
Someone pulls this memo up. Does it hold? Did it state the risk that materialized? A memo that only
looks good when things go well isn't a good memo.

**4. The hostile-quote test.** Which single sentence would someone pull out of context to
misrepresent the analysis? Rewrite it so it can't be. Usually it's an unhedged claim that needed a
qualifier, or a number missing its base.

Report the results of all four in chat, honestly. If it fails one, fix it before writing the file.

---

## Language

**Numbers.** Round to the precision the analysis supports. `$1.2M`, not `$1,247,382`. Percentages
always with their base — "up 18% from 3.97%" not "up 18%." Percentage points and percent are
different units and the difference has caused real confusion in real board meetings; say which.

**Hedges.** Keep the ones carrying real uncertainty ("the range runs from X to Y"). Delete the ones
softening tone ("it would appear that perhaps"). Every unnecessary hedge weakens the necessary ones.

**Jargon.** Expand every acronym on first use. Replace statistical terms with plain equivalents
where you can do it without losing meaning: "we can rule out chance as the explanation" for "p <
0.05," "the range that's consistent with our data" for "the confidence interval." If a technical
term earns its place, define it in the same sentence.

**Attribution.** "The data shows" for facts. "I read this as" or "this suggests" for inference.
Never let those blur — it's the single most common way a memo overstates what's known.

**Voice.** Match `03_Preferences` in `0_User/`. A direct writer's memo shouldn't arrive full of
qualifications; a careful writer's shouldn't arrive blunt. The user signs this, and it has to sound
like them.

---

## The essence into ground truth

`util_get_org_info` `set(02_Decisions, …)`:

```markdown
## Current Decision

<Decision>. Recommended <what>, on <date>, to <reader>. Basis: <the one-line reason>.
Status: <awaiting decision / approved / declined>. Revisit if <condition>.
Memo at `2_Outputs/.agents/L2.2-Decision-Memo/Decision-Memo.md`.
```
