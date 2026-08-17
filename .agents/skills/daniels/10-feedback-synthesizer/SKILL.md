---
name: feedback-synthesizer
description: >
  Turns a pile of open-ended survey responses, reviews, support tickets, or interview notes into
  themes with frequencies, sentiment, and representative verbatim quotes — traceable back to the
  source. Use when: "synthesize these survey responses", "what are people saying", "analyze this
  feedback", "code these open-ended answers", "themes from reviews", "what do the comments say",
  "read 400 tickets for me". Session L2.1. Make sure to use this skill whenever someone has a large
  volume of free text and needs to know what's in it.
---

# feedback-synthesizer — Themes, Sentiment, and Quotes

You are doing qualitative coding at a speed that makes it practical, without losing the two things
that make qualitative work credible: **the quotes are real** and **the counts are honest**.

The failure mode is a synthesis that sounds plausible and isn't traceable. Every theme you report
must be backed by responses you can point to, and every quote must be verbatim. If a reader can't
follow a claim back to the text, the whole document is just opinion with a chart on it.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("feedback-synthesizer")`), then pull:

- **The text** *(primary)* — `5_Library/sources/processed/`, or
  `5_Library/sample-data/survey_responses.csv` for practice.
- **The decision frame** *(supplementary but shapes everything)* — synthesis for "what do we fix
  first" looks different from synthesis for "why are people leaving."
- **Org ground truth** *(supplementary)* — via `util_get_org_info`.

**Read every response.** Not a sample, not the first fifty. If the volume genuinely exceeds what
can be read, say so explicitly and describe the sampling method — but for anything under a few
thousand responses, read them all. Sampling free text and reporting frequencies from the sample,
without saying so, is how a synthesis becomes fiction.

## Phase 1 — Understand what you're holding

Before coding, establish:

- **How many responses**, and how many are blank or useless ("n/a", "none", "."). Report both.
- **Who answered** — and, more importantly, **who didn't.** Response rate and any visible skew in
  who responded. Survey non-response is rarely random; the people most frustrated and the people
  most content both answer at different rates than the middle.
- **What question they were answering.** The wording drives the content. "What would you change?"
  produces a complaint list. "How has this helped you?" produces the opposite. Neither is a
  balanced view of sentiment, and the readout must say which question it's summarizing.
- **Structured fields alongside** — rating, role, tenure, segment. These let you cross-tab themes,
  which is where most of the insight lives.

## Phase 2 — Code the responses

**Load `reference/coding-method.md`** for the full procedure. In outline:

1. **First pass — open coding.** Read everything, tag each response with short descriptive labels.
   Multiple labels per response is normal and expected; people raise more than one thing.
2. **Second pass — build the codebook.** Group related labels into themes. Write a one-sentence
   definition of each theme and note what it excludes. The definitions are what make the counts
   mean anything.
3. **Third pass — recode against the codebook.** Apply consistently. This pass catches responses
   miscoded in pass one and is where the frequencies become trustworthy.
4. **Report residual.** How many responses didn't fit any theme? A synthesis that codes 100% of
   responses into five clean themes is usually forcing the fit. Some residual is a sign of honesty.

**Aim for five to nine themes.** Fewer and they're too coarse to act on; more and nobody can hold
them. If a theme covers more than about 40% of responses, it's too broad — split it.

## Phase 3 — Count, and say what the counts mean

For each theme report:

- **Count and percentage of coded responses** — with the denominator stated. Percentage of all
  responses, or of responses that mentioned anything? Say which.
- **Sentiment within the theme** — positive, negative, mixed. A theme can be frequent and positive;
  "support" often is.
- **Cross-tabs**, where they matter: theme by rating, by role, by tenure, by segment. This is
  usually where the finding is. "Pricing is the top theme overall" is thin. "Pricing dominates for
  accounts past their second year, while onboarding dominates in the first six months" is a
  roadmap.

**On sentiment scoring:** be honest about the method. If you're judging sentiment by reading, say
so — that's legitimate and it's what you're doing. Don't present a judgment as a computed score.
And check sentiment against any rating field present; where they disagree, that disagreement is
often the most interesting thing in the dataset.

## Phase 4 — Pull representative quotes

Two to four per theme, **verbatim, never edited for grammar or tone**. Selection rules:

- **Representative, not extreme.** The most quotable response is usually the least typical. Pick
  ones that say what most people in that theme are saying.
- **Include one dissent per theme** where it exists. A synthesis that shows only agreement is
  hiding variance.
- **Attribute by segment, not by person** — "Director, 2+ years" — and only when the structured
  fields support it.
- **Keep the response ID** so any claim can be traced back.
- **Never compose a quote** that summarizes several responses. If no single response says the thing
  well, that's evidence the theme needs rethinking.

## Phase 5 — Say what it means

Two or three paragraphs, and hold this line: **separate what people said from what you conclude.**

- What people said: frequencies, sentiment, quotes. Traceable.
- What it suggests: your reading. Labeled as interpretation.
- What it can't tell you: who didn't respond, what they'd say, and what people say versus what they
  do. Stated-preference data is not behavior.

If the decision frame asked "what do we fix first," rank the themes by something more useful than
frequency — frequency × severity, or frequency among the segment that matters most. The loudest
theme is not automatically the most important one.

## Closing

**Load `reference/output-format.md`** and:

1. Show the theme table with counts, sentiment, and one quote each.
2. Ask: *"Does this match your read? Anything here you'd merge or split?"* The user has usually read
   some of these responses and has intuitions worth incorporating.
3. Quietly write `2_Outputs/.agents/Use-Case/Feedback-Synthesis.md` plus a coded CSV so anyone can
   audit the coding.
4. Fold the top themes into `util_get_org_info` (`set(07_Insights, …)`).

## Guardrails

- **Never invent or paraphrase a quote.** Verbatim or nothing.
- **Never report a percentage without its denominator.**
- **Never claim a theme without the responses to back it.** Anyone should be able to filter the
  coded CSV and find them.
- **Never generalize from responders to the whole population** without flagging non-response.
- Never let one vivid response become a theme. Vividness is not frequency.
- Never present sentiment as computed when it was judged. Say which.
- If responses contain names, customer identifiers, or anything personally identifying, flag it
  before writing anything to a tracked file — and mask it in quotes.
- The themes are the user's to challenge. They know the business context that makes two apparently
  similar complaints actually different.
