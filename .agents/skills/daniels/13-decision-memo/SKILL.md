---
name: decision-memo
description: >
  Turns an analysis into a bottom-line-up-front executive memo — the question, the recommendation,
  the evidence, the risks, and what happens next — written for a specific reader who will spend
  ninety seconds on it. Use when: "write this up for my VP", "turn this into a memo", "executive
  summary", "how do I present this", "BLUF memo", "brief leadership on this", "I need a
  one-pager". Session L2.2. Make sure to use this skill whenever an analysis needs to travel to
  someone who wasn't part of it.
---

# decision-memo — Executive Decision Memo

You are writing the document that carries an analysis to the person who acts on it.

The governing constraint: **your reader will spend ninety seconds on it, and they will read the
first paragraph carefully and the rest selectively.** Everything follows from that. The
recommendation goes first — not the background, not the methodology, not a narrative of how the
analysis unfolded. If they read only the opening paragraph, they should be able to act correctly.

Most people write these backwards, in the order the work happened. Resist it.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("decision-memo")`), then pull:

- **The analysis** *(primary)* — whatever is in `2_Outputs/.agents/Use-Case/`. This is what you're
  translating.
- **The decision frame** *(primary)* — `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md`.
  It holds the question, the owner, the deadline, and — critically — **what would change the
  owner's mind.** The memo is aimed at that.
- **The session template** *(primary)* — `1_Class/L2.2-Decision-Memo/`.
- **Stakeholders** *(primary)* — via `util_get_org_info` (`05_Stakeholders`). Who reads this and
  what they care about.
- **The audit** *(supplementary)* — its limitations become the memo's caveats.

If there's no analysis yet, this skill is early. Say so and route to the right use-case skill first.

## Phase 1 — Fix the reader in mind

Before writing a word, establish four things and say them back:

1. **Who reads it?** A named person or role. Everything below depends on this.
2. **What do they already believe?** If the recommendation contradicts their prior, the memo needs
   to address that directly rather than hoping they notice. Burying a contrary finding in paragraph
   six is how analyses get ignored politely.
3. **What do they optimize for?** Cost, risk, speed, headcount, a specific number they're measured
   on. The recommendation gets framed in those terms or it doesn't land.
4. **What's their decision latitude?** Can they approve this alone, or do they need to carry it
   somewhere else? If they need to carry it, the memo has a second audience they'll never meet, and
   it has to survive being explained secondhand.

**Load `reference/output-format.md` § Audience calibration** for how each of these changes the
draft.

## Phase 2 — Write the BLUF

The first paragraph. Three to five sentences. It contains:

1. **The recommendation** — a verb and an object. "Extend the contractor bridge through Q4 and
   defer two of the five open reqs to January."
2. **The single most important reason** — one sentence, with the number in it.
3. **What it costs or risks** — stated, not hidden. Credibility is built here.
4. **What you need from the reader** — approval, a decision by a date, or nothing (informational).

**Test it:** if the reader read only this paragraph and acted, would they act correctly? If not,
rewrite. If it takes more than five sentences, the recommendation isn't sharp enough yet.

**Never open with background.** "As you know, the support backlog has been growing since Q2" wastes
the only paragraph you're guaranteed to have read.

## Phase 3 — Evidence, ranked by weight

Three to five points, strongest first. Each one:

- **A claim, in a sentence, with a number in it.** "Backlog grew 46% in eleven days" not "the
  backlog has grown considerably."
- **The source**, briefly. "From the cleaned ticket export, 2022–2026."
- **What it does and doesn't establish.** One clause is enough: "this is an association, not a
  demonstrated cause."

**Separate fact from inference visibly.** Facts are what the data shows. Inferences are your
reading. A reader who can't tell them apart will either trust too much or too little, and both are
expensive.

**Include the strongest evidence against your recommendation.** Not buried — in the evidence
section, on its own. This is counterintuitive and it is what makes a memo credible. The reader who
finds the counterargument themselves, after the fact, discounts everything else you wrote.

## Phase 4 — Risks and what you don't know

Two sections that most memos omit and every good one has.

**Risks:** what could go wrong if the recommendation is followed. For each, its rough likelihood,
its impact, and what would mitigate it. Be specific — "market conditions could change" is not a
risk, it's a hedge.

**Limitations:** what this analysis could not determine, and why. Data that didn't exist, a window
too short, a comparison that was confounded, a question the method can't answer.

Stating limitations plainly makes a memo *more* persuasive, not less. It signals that the analyst
knows where the edges are — and it prevents the far worse outcome of someone else finding a
limitation you didn't disclose.

## Phase 5 — Next steps

Specific, owned, dated. Not "continue monitoring." Include:

- What happens if the recommendation is approved — the first action, its owner, its date
- What decision is needed from the reader, and by when
- What would trigger revisiting this — the condition under which the recommendation changes

## Phase 6 — Cut it

**One page.** Roughly 400–500 words for the memo proper. Detail goes in an appendix or stays in the
analysis document and gets referenced.

Cutting passes, in order:

1. Delete every sentence that doesn't serve the decision. Interesting findings that don't bear on
   the recommendation go in the appendix — that's what it's for.
2. Delete methodology from the body. One line: "Method and limitations in the appendix."
3. Replace every hedge that isn't carrying real uncertainty. "It appears that costs may potentially
   increase" → "costs increase." Keep the hedges that are doing genuine work; delete the ones that
   are only softening tone.
4. Cut adjectives. "Significant," "substantial," and "considerable" are all replaceable by the
   number.
5. Read the first paragraph alone. Does it work?

## Closing

**Load `reference/output-format.md`** and:

1. Show the full memo in chat.
2. **Run the four tests** in `reference/output-format.md` § Tests — the ninety-second test, the
   skeptic test, the forward test, and the hostile-quote test — and report the results honestly.
   If it fails one, fix it before writing the file.
3. Ask: *"Does this sound like you? Would <reader> act on this?"* Revise.
4. Quietly write `2_Outputs/.agents/L2.2-Decision-Memo/Decision-Memo.md`.
5. Fold the recommendation into `util_get_org_info` (`set(02_Decisions, …)`).

## Guardrails

- **Never bury the recommendation.** BLUF means bottom line up front, and it means literally first.
- **Never omit the strongest counterargument.** Include it, address it, move on.
- **Never overstate confidence.** If the analysis was inconclusive, the memo says so and recommends
  what to do about the uncertainty — that's still a recommendation, and often a better one.
- **Never present an inference as a fact.** Label your reading as your reading.
- **Never recommend something the analysis doesn't support.** If the honest recommendation is "we
  don't know yet, here's what would settle it," write that memo. It's a real memo and it beats a
  confident wrong one.
- Never let the memo carry a number the analysis document can't reproduce.
- Never use a percentage without its base, or a comparison without its baseline.
- The user signs this. It has to sound like them and they have to be able to defend every line in a
  meeting you won't be in.
