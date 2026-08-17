---
name: meeting-to-actions
description: >
  Turns meeting notes or a transcript into decisions, action items with owners and deadlines, open
  questions, and a draft follow-up email — flagging what was discussed but never actually decided.
  Use when: "turn these notes into action items", "who owns what from this meeting", "draft a
  follow-up email", "summarize this meeting", "what did we decide", "extract next steps". Session
  L2.1. Make sure to use this skill whenever someone has meeting notes and needs accountability out
  of them.
---

# meeting-to-actions — Meeting to Accountability

You are producing the document that determines whether anything from that meeting actually happens.

The value here is not summarization — anyone can summarize. The value is **separating four things
that meeting notes routinely blur together**:

| Category | Test |
|---|---|
| **Decision** | Something was settled. A choice was made and nobody is still weighing it. |
| **Action** | Someone will do something. It has an owner and, ideally, a date. |
| **Open question** | It was raised and not resolved. Somebody needs to close it. |
| **Discussion** | It was talked about. Nothing follows from it. |

The most useful output is usually the third category — **the thing everyone left believing was
decided, that wasn't.** Finding those is the job.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("meeting-to-actions")`), then pull:

- **The notes** *(primary)* — `5_Library/sources/processed/`, pasted text, or
  `5_Library/sample-data/meeting-notes-q3-planning.md` for practice.
- **Org ground truth** *(supplementary)* — via `util_get_org_info`, especially `05_Stakeholders`
  for who these people are and `02_Decisions` for what was already in play.
- **User profile** *(supplementary)* — the follow-up email should sound like them, not like an
  assistant.

Establish first: **who was in the meeting, what it was about, and what the user's role is.** Whether
they chaired it, attended it, or is writing up someone else's notes changes the tone of everything
you draft.

## Phase 1 — Extract, category by category

Work through the notes and assign every substantive item to one of the four categories. Be strict.

**Decisions.** A decision has a subject, an outcome, and no remaining conditionality. "We'll go with
August 15th for the maintenance window" is a decision. "August 15th seems like it could work" is
not, no matter how the room felt about it.

For each: what was decided, who decided it, and any stated conditions.

**Actions.** An action has a verb and a person. For each, capture:

- **What** — specific enough that the owner knows they're done
- **Who** — a named person. `[UNASSIGNED]` if it isn't clear. Never guess.
- **When** — a date. `[NO DATE]` if none was set. Never invent one.
- **The exact wording** it came from, so the owner can check your reading against theirs

**Open questions.** Anything raised and left hanging: an unresolved conflict, a number nobody had, a
disagreement that got talked past rather than through. **This is the highest-value section.** In
the practice notes, the writer needing to be in two places in August is exactly this — two people
each left assuming they had them.

**Discussion.** Context worth keeping, with nothing following from it. Keep it short.

## Phase 2 — Flag the gaps explicitly

Don't quietly fill holes. Surface them as a list the user can act on before sending anything:

- **Unassigned actions** — "Someone needs to model the overtime cost. Dana offered, but nobody
  confirmed she owns it."
- **Undated actions** — "Aisha will write up what changed in implementation. No date was set."
- **Conflicting commitments** — "Tom needs the writer for the help center in August. Aisha needs the
  same writer for onboarding docs in August. This wasn't resolved."
- **Decisions that were assumed, not made** — "Everyone proceeded as though the deflection work is
  shipping in August, but the writer conflict makes that conditional."
- **Ambiguous ownership** — where "we should" never became "I will."

**This list is the deliverable that changes outcomes.** Put it near the top.

## Phase 3 — Draft the follow-up email

Load `reference/output-format.md` § *Email* for the structure. Principles:

- **Short.** Decisions, actions in a table, open questions, one closing line. Anything longer goes
  unread and the actions go undone.
- **Actions as a table** with owner and date. Tables get scanned; prose does not.
- **Name the gaps as questions**, not accusations. "Dana — confirming you're taking the overtime
  model?" not "Dana was assigned but didn't confirm."
- **Match the user's voice.** Read `03_Preferences` from `0_User/`. A direct writer's follow-up
  should not arrive full of hedges.
- **Never invent a commitment.** If nobody agreed to a date, the email asks for one.

Then show it and say plainly: *"Read this before sending. I've marked three places where I inferred
ownership that wasn't stated explicitly."*

## Closing

**Load `reference/output-format.md`** and:

1. Show the four categories, the gaps list, and the draft email in chat.
2. Ask them to correct the ownership and dates — they were there and you weren't.
3. Quietly write `2_Outputs/.agents/Use-Case/Meeting-Actions.md`.
4. If the meeting touched a decision already tracked in `0_Org/`, fold the update in via
   `util_get_org_info` (`set(02_Decisions, …)`).

## Guardrails

- **Never invent an owner or a date.** `[UNASSIGNED]` and `[NO DATE]` are correct answers and they
  are more useful than a plausible guess, because they prompt someone to fix it.
- **Never upgrade a discussion to a decision.** If the notes are ambiguous, it goes in open
  questions. The whole value of this skill is that discipline.
- **Never send anything.** You draft; the user reviews and sends. Say so explicitly.
- Never editorialize about people. "Marcus was resistant" doesn't belong in a follow-up. Record what
  was said, not how you read the room.
- Never drop a disagreement that was left unresolved. Notes that smooth over conflict produce
  meetings that repeat.
- If the notes reference personnel matters, compensation, or anything confidential, flag it before
  writing to a tracked file and ask whether it belongs there.
- Quote the source wording for every action. It lets the owner check your reading against theirs,
  and it settles disputes about what was actually said.
