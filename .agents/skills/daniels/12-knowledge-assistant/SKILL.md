---
name: knowledge-assistant
description: >
  Builds a grounded question-answering assistant over documents a team actually uses — a policy
  manual, onboarding docs, SOPs, an FAQ — that cites its source for every answer and says "not
  covered" when the documents don't answer the question. Use when: "build a chatbot for our
  handbook", "answer questions from these documents", "internal knowledge base", "people keep
  asking me things that are in the manual", "make our SOPs searchable", "a bot for onboarding
  questions". Session L2.1.
---

# knowledge-assistant — Grounded Q&A Over Your Documents

You are building something that answers questions from a specific set of documents and **refuses to
answer from anywhere else.**

That refusal is the entire product. A general assistant that answers policy questions from general
knowledge will be plausible, fluent, and occasionally wrong about this organization's actual policy
— which is worse than useless, because people will act on it. An assistant that says *"the handbook
doesn't cover that — here's who to ask"* is trustworthy, and trustworthiness is what determines
whether anyone uses it twice.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("knowledge-assistant")`), then pull:

- **The corpus** *(primary)* — documents in `5_Library/sources/processed/`, or
  `5_Library/sample-data/policy-handbook-excerpt.md` for practice.
- **Org ground truth** *(supplementary)* — via `util_get_org_info`; `06_Constraints` may bear on
  what can be exposed and to whom.
- **User profile** *(supplementary)* — technical comfort decides the build surface.

## Phase 1 — Define the boundary

Before anything else, establish four things. Most failures of this use case trace to skipping this.

1. **What's in scope?** Which documents, which versions, effective as of when. A handbook from 2024
   answering questions in 2026 is a liability, not an asset.
2. **Who asks?** New hires, managers, the whole company, external customers. This determines both
   the tone and what must not be exposed.
3. **What happens when the answer isn't there?** Every assistant needs a defined fallback: a named
   person, a team alias, a ticket queue. **"I don't know" with no next step is a dead end**, and
   dead ends are how internal tools get abandoned.
4. **What questions must it refuse?** Anything requiring individual judgment, anything about a
   specific person's situation, anything with legal consequence. "How much PTO do I have?" is a
   systems question, not a handbook question, and the assistant should say so.

## Phase 2 — Prepare the corpus

**Load `reference/retrieval-patterns.md`** for the mechanics. The essentials:

- **Preserve structure.** Section numbers and headings are what make a citation useful. "Section
  7.2" is a checkable answer; "the handbook says" is not.
- **Chunk on semantic boundaries** — sections, not fixed character counts. A chunk that splits a
  policy mid-sentence retrieves badly and cites worse.
- **Keep the metadata**: document name, version, effective date, section. Every answer carries it.
- **Find the contradictions before users do.** Documents accumulate. The practice handbook has a
  stipend amount stated two ways and a carryover exception whose criteria are "under review." Real
  corpora are worse. Surface every conflict you find and ask which version governs.
- **Note the coverage gaps.** The practice excerpt covers Sections 4 and 7 only. Anyone asking about
  expenses gets nothing, and the assistant should say that clearly rather than improvising.

## Phase 3 — Set the answering rules

These are the assistant's operating instructions, and they are the deliverable as much as the code:

1. **Answer only from the corpus.** Never from general knowledge, never from what's typical at other
   companies. If it isn't in the documents, it isn't an answer.
2. **Cite every claim** — document, section, and version. Inline, not in a footnote nobody reads.
3. **Quote for anything consequential.** For amounts, deadlines, and eligibility, quote the sentence
   rather than paraphrasing. Paraphrase is where policy errors enter.
4. **Say "not covered" plainly**, then give the fallback. Never approximate an answer from an
   adjacent section.
5. **Surface conflicts rather than resolving them.** "Section 7.4 says $750; an earlier revision
   said $500. The current handbook version is 4.2, which states $750." Let the reader see the
   conflict.
6. **Flag anything time-sensitive.** Policies with review dates, pending exceptions, or "under
   review" language get that caveat attached every time.
7. **Never give individual advice.** "The policy says X" is in scope. "You should do X" is not.
8. **Escalate the sensitive categories** by design: anything touching medical leave, accommodation,
   harassment, termination, or compensation disputes routes to a human immediately. State this
   rule explicitly in the build.

## Phase 4 — Build it

Match the surface to what the user needs. Load
`5_Library/build-surfaces/Choosing-Your-Surface.md`:

| Situation | Build |
|---|---|
| A handful of documents, occasional questions | A Claude Project with the documents attached and the answering rules as instructions. Fastest, and often sufficient |
| Many documents, frequent use, a shared team | Retrieval over a chunked index — the `reference/retrieval-patterns.md` approach |
| Just needs a better FAQ | Honestly, a better FAQ. Say so if that's the answer |
| Company-wide deployment | Out of scope for this session. Note the requirements: access control, audit logging, version management, an owner |

**The "honestly, a better FAQ" row is a real recommendation.** If forty questions cover ninety
percent of what people ask, a well-organized page beats a chatbot on every dimension including cost.
Say it when it's true.

## Phase 5 — Test it against the hard cases

Before declaring it works, run these categories and show the results:

| Test | Expected behavior |
|---|---|
| Question answered directly in the docs | Correct answer with citation |
| Answer requires combining two sections | Correct, citing both |
| Answer genuinely not in the corpus | "Not covered" + the fallback. **No improvisation** |
| Corpus contradicts itself | Both versions surfaced, current one identified |
| Question about an individual's situation | Declines, routes to a person |
| Question in a sensitive category | Routes to a human immediately |
| Question near the corpus boundary | States what the documents do and don't cover |

**The "not covered" test is the one that matters.** An assistant that answers everything is an
assistant that hallucinates. Write out at least five questions the corpus genuinely cannot answer
and confirm it declines all five.

Using the practice handbook, good test questions: *"How do I submit an expense report?"* (Section 6,
not included), *"Can I work from Portugal for a month?"* (7.3 covers it — and the answer is a
process, not a yes), *"How much is the home office stipend?"* (the contradiction case), *"I'm
pregnant and want to know about accommodation"* (sensitive — route to a person).

## Closing

**Load `reference/retrieval-patterns.md` § Output**, then:

1. Show the corpus inventory, the conflicts found, the coverage gaps, and the test results.
2. Show ten sample Q&A pairs — including the ones it correctly refuses.
3. Quietly write `2_Outputs/.agents/Use-Case/Knowledge-Assistant.md` with the corpus manifest,
   answering rules, and test results.
4. Note the maintenance question explicitly: **who updates this when the handbook changes?** An
   assistant serving a stale policy is worse than no assistant, and this question has no technical
   answer.

## Guardrails

- **Never answer from outside the corpus.** This is the entire product.
- **Never paraphrase an amount, a deadline, or an eligibility rule.** Quote it.
- **Never resolve a contradiction on the assistant's own authority.** Surface both, name the current
  version, route the judgment to a human.
- **Never give individual advice**, and never answer a question that requires knowing someone's
  personal circumstances.
- Route sensitive categories — medical, accommodation, harassment, termination, compensation
  disputes — to a human, by design, every time.
- Never deploy without an owner and a review date. Say this out loud even though it isn't technical.
- If the corpus contains personal data, flag it before anything reaches a tracked file.
- If a well-organized FAQ would serve better than a chatbot, say so. Building the smaller thing is
  a legitimate outcome of this exercise.
