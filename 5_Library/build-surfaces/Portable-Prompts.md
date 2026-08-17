# Portable Prompts

Paste-ready versions of the chain for any assistant that cannot read this folder. Each prompt is
self-contained: no file paths, no references to the skills, nothing that assumes the tool can see
the repo.

**How to use these**

1. Copy one prompt into your assistant
2. Replace anything in `[SQUARE BRACKETS]`
3. Upload your data file if the prompt needs one, or paste your text
4. Fill your template in `1_Class/<session>/` by hand as you go
5. When you move to the next stage, paste your filled-in template in as context. That is how you
   carry the chain forward by hand

The guardrails inside these prompts are the point. Do not trim them to save space, because they are
what keep the output honest.

---

## 1. Frame the decision

Do this one first, whatever tool you are using. It works perfectly well in a free chat tool.

```
You are helping me frame an analytical decision before I touch any data.
Work through this one question at a time. Do not move on from a vague answer,
and do not write my answers for me. Ask, wait, then push if the answer is not
specific enough to be wrong.

My situation: [DESCRIBE IT IN 2-3 SENTENCES. What was asked of you, or what
problem you have noticed.]

Work through these five fields with me, in order:

1. THE DECISION. Not the topic, the choice. Push me until there is a verb and
   at least two real options on the table. "Understand our staffing situation"
   is a topic. "Should we extend contractors or fill the open reqs" is a
   decision.

2. THE OWNER. A named person or role who can actually make this call. If I say
   "leadership" or "the committee," ask me who signs.

3. THE TRIGGER AND DEADLINE. What forces this decision, and when? If nothing
   forces it, ask me whether this decision is real.

4. WHAT WOULD CHANGE THEIR MIND. If the analysis came back saying the opposite
   of what the owner expects, what would it have to show for them to change
   course? If my honest answer is "nothing," tell me plainly that the decision
   is already made and ask what I want to do about that.

5. GOOD ENOUGH TO ACT ON. How wrong could this be and still lead to the same
   choice? "As accurate as possible" is not an answer. Push me to a tolerance.

Then pressure-test against reality: is the data available and can I get it, is
there time before the deadline, am I in a position to act on the answer, and is
there a privacy or political constraint that shapes what I can analyze.

Finally, recommend which of these fits my decision, and why in one sentence:
KPI dashboard, scenario calculator, forecast, risk scorer, A/B test readout,
feedback synthesis, data audit, decision memo, meeting to action items, or a
knowledge assistant.
```

---

## 2. Audit the data

Needs a tool that can run code. Upload the file first.

```
I am about to analyze the attached file. Audit it first and do not clean
anything without asking me.

Rules for how you work:
- Never modify the source. Any cleaned version is a new file.
- Never clean silently. Every change gets logged with the reason and the number
  of rows affected.
- You do not decide what is wrong. Surface each finding with the options and
  what each option costs, then let me choose. I know the business, you know
  the pattern.

Step 1. Profile it before judging it. Tell me rows, columns, and what ONE ROW
represents, stated out loud. For each column: type as stored, type as intended,
distinct values, missing count, and range or top values.

Step 2. Run these seven checks and report what you find:
  1. Missingness. What is absent, and is it absent at random? Cross-tab
     missingness against the outcome or key segment. Count the six ways people
     write nothing: empty, N/A, n/a, -, null, a single space.
  2. Types and formats. Numbers stored as text, currency symbols, percentages
     as text, multiple date formats in one column, lost leading zeros.
  3. Duplicates. Exact duplicate rows, and duplicates on the key with
     conflicting values.
  4. Outliers. Use the interquartile range, not standard deviations, since
     business data is usually skewed. For each one, tell me whether it looks
     like a data error, a real but exceptional event, or just the tail of the
     distribution.
  5. Categorical drift. One category written several ways: case, whitespace,
     synonyms, renamed over time.
  6. Logical consistency. Impossible values, ordering violations, components
     that do not sum to totals.
  7. Definition drift. A level shift with no business explanation, a column
     empty before a date and populated after. Then ask me whether the way
     anything is counted changed partway through.

For each finding tell me: what, where, how much, and WHY IT MATTERS for my
analysis. The last one is the only one that makes it a finding rather than
trivia.

Step 3. Bring me each decision one at a time with the options and their
consequences. Record my reasoning, not just my choice.

Step 4. End with three lines: what this data CAN support, what it can support
WITH CAVEATS, and what it CANNOT support. The third line is the one that
saves me.
```

---

## 3. KPI dashboard

```
Build me an executive dashboard from the attached file.

The decision it supports: [FROM YOUR DECISION FRAME]
Who reads it: [ROLE] and what they care about: [WHAT]

First, help me choose five to seven metrics. For each candidate ask me: "if
this moved 20% next month, what would someone do differently?" If the answer is
nothing, it is context, not a KPI, and it does not get a tile.

For each metric you keep, write a full definition: numerator, denominator, what
is excluded, the time window, and the source. "Retention" is not a definition.

Then compute them, and follow these rules:
- Every metric needs a comparison. A number with no comparison cannot be
  interpreted. Prior period, same period last year, or target.
- State the time window on the dashboard, not just in your head.
- Handle outliers explicitly. Show the metric with and without a distorting
  event rather than quietly excluding it.
- Round to the precision the data supports. $1.2M, not $1,247,382.19.

Then write a "so what" of three to five sentences, structured as: what changed,
why it likely changed (labeled clearly as inference, not fact), and what it
means for the decision. Do not just restate the tiles. "Revenue was $4.2M, up
6%" is a caption. Tell me what it means.

Finally, tell me what this dashboard cannot tell me.
```

---

## 4. Scenario calculator

```
Help me build a what-if model for this decision: [THE DECISION]

Do NOT give me a single number at any point. Every output is a range.

Step 1. Before any numbers, write the model as an equation in plain words and
get my agreement. Most errors in these models are structural (a double count, a
missing cost, a rate on the wrong base), and a structural error survives every
sensitivity test you run on it.

Step 2. Classify every term as one of: a LEVER I control, an ASSUMPTION that is
uncertain, a CONSTANT that is known, or a CONSTRAINT that is a hard limit.

Step 3. For every assumption, get three numbers from me: low, expected, high.
Ask it as "what would be low enough that you would be genuinely surprised?"
rather than asking for a standard deviation. Then ask what would have to happen
for it to land outside that range, and widen it if I can answer quickly.
Record the SOURCE of each range: history, a quote, judgment, or a guess. Label
the guesses as guesses.

Step 4. Run a base case, a downside, an upside, and one scenario per option.
For the downside, move only the two or three assumptions that plausibly go
wrong together. Do not set everything to its worst at once; that produces a
scenario that will essentially never happen and makes the model easy to
dismiss.

Step 5. Sensitivity. Vary one assumption at a time across its range, hold the
rest at expected, and rank by how much the answer moves. Then tell me in one
sentence what this decision is actually a bet on.

Step 6. Break-even. For each option, solve for the value that flips the
decision, and tell me how that compares to recent history.

End with what the model cannot tell me.
```

---

## 5. Forecast

```
Forecast [WHAT] from the attached history. Horizon: [N PERIODS].

Non-negotiable: you will not give me a forecast without a backtest against a
naive baseline, and you will not give me a point forecast without an interval.

Step 1. Describe what you see before modeling: trend, seasonality, level shifts
with a business cause, one-off events, and whether the pattern changed recently.
Then ask me what is happening in the forecast window that the history cannot
know about.

Step 2. Count observations honestly. Tell me how many FULL SEASONAL CYCLES I
have. With four years of monthly data I have 48 observations but only four
observations of each December, and any seasonal factor rests on those four. Say
this out loud.

Step 3. Compute the naive baselines first. These are the bar:
  - Last value carried forward
  - Seasonal naive (same period last year)
  - Seasonal naive plus average year-over-year drift
  - Moving average

Step 4. Try a real method, then BACKTEST all of them out of sample using a
rolling origin. Report the error for every candidate AND every baseline in one
table. If the naive baseline wins, say so and use it. "The best forecast is
last year plus 6%" is a respectable finding.

Step 5. Build the interval from the observed backtest errors at each horizon
step, not from a formula. It must widen with horizon. If it does not, something
is wrong.

Step 6. Apply any known future events as labeled line items ON TOP of the model
output, shown separately. Never bury judgment inside the math.

Then tell me in plain language: how wrong has this method typically been, and
what that implies about how much weight to put on the number. And tell me what
the forecast cannot account for.
```

---

## 6. Risk scorer

```
Score the attached records on [OUTCOME] so I know who to act on first.

Before anything else, run a LEAKAGE CHECK. For each column ask: "would this
value be filled in, right now, for a record that has NOT had the outcome yet?"
Anything that fails is leakage and must be excluded, no matter how predictive.
A model that scores near-perfectly has leakage, not insight. Tell me what you
excluded and why.

Then pin down the outcome precisely: what exactly counts as the event, over
what window, who is in the population, and at what moment the score gets used.

Build a logistic regression first. I need to explain this to a person, and
"the ensemble said so" is not an explanation. Also build the rule my team
already uses as a baseline: [DESCRIBE IT, e.g. "no login in 60 days"].

Validate honestly:
- Split OUT OF TIME, not randomly. Train on earlier, test on later.
- Do not report accuracy alone. With an uncommon outcome it is meaningless.
- Report precision and recall at the threshold I will actually use, translated
  into work: "of the 50 accounts you call, about N are real."
- Check calibration. If it says 30%, do about 30% of those actually happen?
- Tell me whether it beats the existing rule. If it does not, say so plainly.

Set the threshold from CAPACITY, not statistics. My team can work about [N]
cases per [PERIOD]. Show me what that cutoff costs in false alarms and missed
cases, and show me one tighter and one looser option.

Report the top drivers with direction and rough size, and attach the
association caveat to every single one. The model tells me WHO to look at. It
does not tell me why, and it does not establish that changing a driver changes
the outcome. Tell me what experiment would establish that.

Finally, show me the top 10 records with the two or three reasons each was
flagged, so I can sanity-check them against what I know.
```

---

## 7. A/B test readout

```
Read out this experiment. [UPLOAD OR PASTE THE RESULTS]

Answer two separate questions and do not collapse them: is the difference real,
and is it big enough to act on.

Step 1. Before any statistics, establish what was actually run:
  - Was the hypothesis stated before the data came in?
  - How were units assigned? Random assignment is what licenses causal
    language. If groups self-selected, this is observational and you must say
    so.
  - What is the ONE primary metric?
  - When did it stop, and why? Stopping because it looked good inflates false
    positives. Ask me directly and without judgment.
  - What is the unit of analysis? If one person can convert more than once,
    aggregate before testing.

Step 2. Check the sample ratio. If the split was designed 50/50, confirm it
landed there. A meaningful imbalance means something broke and every other
number is suspect. Run this first.

Step 3. Pick the right test and say why in one sentence. Two proportions: a
two-proportion z-test. Two means: Welch's t-test. Three or more groups: ANOVA
first, then pairwise with a correction, because running every pair inflates the
false positive rate badly.

Step 4. Report in THIS ORDER:
  1. The observed difference in business units
  2. The CONFIDENCE INTERVAL on the difference. This is the most useful number
     in the readout, because its width tells me how much I actually learned
  3. The relative change, alongside the absolute
  4. The p-value, with a plain-English translation of what it means
  5. The business translation: what the interval is worth in money or volume

Never lead with the p-value.

Step 5. Practical significance. Ask me what the effect would have to be to
justify shipping, given the cost. Then compare that threshold to the interval:
  - Whole interval above it: ship
  - Interval straddles it: iterate or extend, I know direction not magnitude
  - Whole interval below it: hold, it is real but not worth it
  - Interval includes zero and is narrow: genuinely no effect, a real finding
  - Interval includes zero and is wide: INCONCLUSIVE, not "no effect." Tell me
    what sample size would settle it

"Not significant" and "no effect" are different results. Do not conflate them.

End with a recommendation: ship, iterate, hold, or inconclusive, and what I did
not learn.
```

---

## 8. Feedback synthesis

```
Synthesize the attached open-ended responses. [OR PASTE THEM IN BATCHES]

The question people were answering was: "[EXACT WORDING]"

Read every response, not a sample. If the volume is too large to read, say so
and describe how you sampled.

Step 1. Tell me how many responses there are, how many are blank or
non-substantive, who answered, and what I should know about who did NOT answer.

Step 2. Code in three passes:
  1. Open coding. Tag each response with short labels close to the
     respondent's own words. Multiple labels per response is normal.
  2. Build a codebook. Group labels into five to nine themes. For each, write a
     one-sentence definition AND what it excludes. The exclusions are what make
     the counts mean anything.
  3. Recode everything against the codebook consistently, and tell me how many
     responses you recoded and how many fit no theme. Coding 100% into five
     tidy themes usually means the fit was forced.

Step 3. For each theme report the count, the percentage WITH ITS DENOMINATOR
stated, and the sentiment. Be honest that sentiment is your judgment from
reading, not a computed score.

Step 4. Cross-tab themes against [RATING / ROLE / TENURE / SEGMENT]. This is
where the insight usually is. Report cell counts and tell me where they are too
small to read.

Step 5. Give me two to four VERBATIM quotes per theme. Never edit them, never
compose one that summarizes several responses. Pick representative ones rather
than the most quotable, and include one dissenting voice per theme where it
exists.

End by separating clearly what people SAID from what you CONCLUDE, and tell me
what this cannot tell me: who did not respond, and the gap between what people
say and what they do.
```

---

## 9. Meeting to action items

```
Turn these meeting notes into accountability. [PASTE THE NOTES]

My role in this meeting: [CHAIRED IT / ATTENDED / WRITING UP SOMEONE ELSE'S NOTES]

Sort everything into four categories and be strict about the boundaries:

DECISIONS. Something was settled, with no remaining conditionality. "We will go
with August 15th" is a decision. "August 15th seems like it could work" is not,
however the room felt about it.

ACTIONS. A verb and a person. For each: what, who, when, and the exact wording
it came from. Use [UNASSIGNED] if no owner was named and [NO DATE] if none was
set. Never guess either one. Those brackets are more useful than a plausible
invention, because they prompt someone to fix it.

OPEN QUESTIONS. Raised and not resolved. This is the highest-value section.
Look especially for the thing everyone left believing was decided that was not,
and for two people who committed to the same resource or the same week.

DISCUSSION. Context with nothing following from it. Keep it short.

Then give me a GAPS list: unassigned actions, undated actions, conflicting
commitments, and decisions that were assumed rather than made.

Finally, draft a follow-up email under 200 words: decisions as bullets, actions
as a table with owner and date, and the gaps phrased as questions to named
people rather than accusations. Mark every place where you inferred ownership
that was not explicitly stated, so I can check it before sending.

Do not invent a commitment that was not made. Where a date is missing, the
email asks for one.
```

---

## 10. Knowledge assistant

```
You will answer questions about the attached documents using ONLY those
documents. This constraint is the entire point: a confident answer from general
knowledge about our actual policy is worse than useless, because someone will
act on it.

First, audit what I gave you and tell me:
  - What is covered and what is NOT covered. Be specific about the gaps.
  - Any place the documents CONTRADICT each other. Show me both and tell me
    which appears current. Do not resolve it yourself.
  - Anything stale, pending, or marked under review.

Then follow these rules for every question I ask:
1. Answer only from these documents. Never from general knowledge or from what
   is typical elsewhere.
2. Cite the document and section for every claim.
3. Quote exactly for amounts, deadlines, and eligibility. Do not paraphrase
   these, because paraphrase is where policy errors enter.
4. If the documents do not answer it, say "That is not covered in these
   documents. For this, contact [FALLBACK PERSON]." Do not approximate from a
   related section.
5. Flag anything time-sensitive or under review, every time.
6. Never advise me on an individual's situation. State what the policy says and
   stop.
7. For anything involving medical leave, accommodation, harassment,
   termination, or a compensation dispute, do not answer. Route it to a person.

Then let me test you. I will ask questions the documents cannot answer, and
declining those correctly is how I know this works.
```

---

## 11. Decision memo

```
Turn this analysis into an executive memo. [PASTE YOUR ANALYSIS AND YOUR
DECISION FRAME]

Reader: [NAME / ROLE]
What they already believe about this: [WHAT]
What they optimize for: [COST / RISK / SPEED / HEADCOUNT / A NUMBER]
Can they decide alone, or do they carry it to someone else? [WHICH]

They will spend ninety seconds on this. Write accordingly.

Structure, in this order and no other:

1. RECOMMENDATION, first. Three to five sentences: the recommendation with a
   verb, the single strongest reason with a number in it, what it costs or
   risks, and what you need from them by when. Test it: if they read only this
   paragraph and acted, would they act correctly? Do not open with background.

2. WHY. Three to five points, strongest first, each with a number. Mark each as
   FACT (what the data shows) or INFERENCE (my reading). Then state the
   STRONGEST CASE AGAINST the recommendation, on its own, fairly. This feels
   like weakening the argument and does the opposite: a reader who finds the
   counterargument themselves afterward discounts everything else.

3. RISKS. Specific ones, with likelihood, impact, and mitigation. "Market
   conditions could change" is a hedge, not a risk.

4. WHAT THIS ANALYSIS COULD NOT DETERMINE. Plainly. This makes the memo more
   persuasive, not less.

5. NEXT STEPS. Owned and dated. Plus what would trigger revisiting this.

Then cut it to 400-500 words and run four tests, reporting the results:
  - Ninety-second test: does the first paragraph alone support correct action?
  - Skeptic test: what is the reader's sharpest colleague's first question, and
    is it answered?
  - Forward test: six months on it went badly and someone pulls this up. Does
    it hold? Did it name the risk that materialized?
  - Hostile-quote test: which sentence would someone pull out of context to
    misrepresent this? Rewrite it.

If the honest recommendation is "we do not know yet, here is what would settle
it," write that memo. It beats a confident answer the evidence does not support.
```

---

## Carrying the chain by hand

In Claude Code each stage reads the previous stage's output automatically. Without that, you are
the integration layer, and it takes about thirty seconds per handoff:

1. Finish a stage and fill in your template in `1_Class/<session>/`
2. Before starting the next stage, paste your filled template in as context, under a line that says
   "Here is my decision frame from the previous stage:"
3. Keep one document open with your running facts: the decision, the metric definitions you settled
   on, and the cleaning choices you made. Paste it into every new conversation

That third habit is worth keeping even if you later move to a fully agentic tool. It is the same
thing `0_Org/` does in this workspace, and it is the reason the chain compounds instead of
restarting every time.
