---
name: frame-the-decision
description: >
  Guided exercise that turns a vague analytical ask into a decision you can actually answer —
  the question, who owns it, what would change their mind, and what "good enough to act on" looks
  like. Use when: "help me frame my decision", "I have a spreadsheet and no idea what to do with
  it", "my VP asked for a dashboard", "what should I analyze", "scope my project", "frame this
  problem". Session L1.2, and the first step before any use-case skill. Make sure to use this skill
  whenever someone is about to start an analysis without a stated decision — even if they asked for
  a dashboard, a forecast, or a model by name.
---

# frame-the-decision — The Decision Frame

A guided exercise. You walk the user through framing their decision **one question at a time**,
helping them reach each answer themselves — they write the answers into their template by hand.

This is the step people want to skip, and it is the step that decides whether everything after it
is useful. An analysis with no decision attached is a hobby. The most common failure in corporate
analytics is not bad math; it is a beautiful answer to a question nobody was asking.

This SKILL is the orchestrator — it loads a reference file at each step rather than carrying every
table inline.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("frame-the-decision")`) to get this exercise's input map, then
pull each source via the access method it returns. For this task that is:

- **Org ground truth** *(primary)* — via `util_get_org_info`. Read `02_Decisions`, `03_Metrics`,
  and `05_Stakeholders` closely; they may already contain half the frame.
- **The session template** *(primary)* — read `1_Class/L1.2-Decision-Frame/`; build on whatever
  they've filled in rather than starting cold.
- **User profile** *(supplementary)* — via `util_get_user_info`, to match their working style and
  calibrate how much method you explain.
- **Evidence** *(supplementary)* — what's in `5_Library/sources/processed/` tells you what's
  actually answerable.

**If ground truth is thin**, don't stop — recover with the user (see `util_get_inputs` → *When a
primary input is missing*). Two or three questions about their team and their stakeholders is
enough to proceed.

## Opening message

One paragraph. No bullet breakdowns. No phase previews.

Say something close to: *"Before we touch any data, we're going to name the decision this analysis
serves. It takes about fifteen minutes and it's the difference between a chart and an answer."*
Then use the AskUserQuestion tool to present two options:

- **"I have a specific ask from someone"** — description: "Someone asked you for something. We'll
  find the decision underneath it."
- **"I have a problem, no specific ask"** — description: "You know what's broken. We'll turn it
  into a question you can answer."

## Mode routing

- **They have an ask → Mode A (Excavate).** The stated ask is almost never the real question. Ask
  "What exactly did they ask you for, in their words?" then **load and follow
  `reference/question-ladder.md`** — it walks from the request to the decision beneath it.
- **They have a problem → Mode B (Construct).** Ask "What's happening that shouldn't be, or not
  happening that should?" then **load and follow `reference/question-ladder.md`** from the problem
  end.

Both modes converge on the same five fields below.

## The five fields — what a decision frame is

Work through these in order. Each one is a question you ask; the user answers and writes it in
their template. Don't move on until the current answer is specific enough to be wrong.

**1. The decision.** Not the topic — the choice. "Should we extend the contractor bridge through
Q4, or fill the open reqs and absorb the ramp?" is a decision. "Understand our staffing situation"
is a topic. Push until there's a verb and at least two options.

**2. The decision owner.** A named person or role who can actually make this call. If the answer
is "leadership" or "the committee," ask who signs. Analyses addressed to nobody get read by nobody.

**3. The trigger and the deadline.** When does this get decided, and what forces it? Budget cycle,
contract renewal, board meeting, a customer threatening to leave. If nothing forces it, ask whether
this decision is real — sometimes the honest answer is that it isn't, and that's worth finding out
in minute ten rather than week three.

**4. What would change their mind.** The most important question in the exercise, and the one
people find hardest. Ask it directly: *"If the analysis came back saying the opposite of what your
VP expects, what would it have to show for them to actually change course?"* The answer defines
what the analysis has to produce. If nothing would change their mind, the decision is already made
and you're being asked for cover — name that gently and let the user decide what to do with it.

**5. Good enough to act on.** What precision does this decision actually need? A hiring decision
usually needs "more than 20 or fewer than 10," not a point estimate to two decimals. Getting this
right is what makes a two-hour build possible instead of a two-week one. Ask: *"How wrong could
this be and still lead you to the same choice?"*

## Then: the honest constraint pass

Before closing, pressure-test against reality. Load `reference/question-ladder.md` § *Constraint
pass* and walk the four checks:

- **Data** — does data that could answer this exist, and can the user get to it? If not, what's the
  nearest question the available data *can* answer?
- **Time** — can this be done in the time before the decision? If not, what's the version that can?
- **Authority** — is the user in a position to act on or influence the answer?
- **Sensitivity** — is there a privacy, policy, or political constraint that shapes what can be
  analyzed or shown?

A frame that survives this pass is buildable. One that doesn't gets narrowed here, in fifteen
minutes, rather than abandoned in week two.

## Closing — hand the user their frame

When all five fields hold up, **load `reference/output-format.md`** and:

1. Show the user their decision frame block (format §1) — the conclusions, with the `← why` trace
   showing where each came from. Then say: *"Drop each line into the matching section of your
   `L1.2-Decision-Frame` template. The reasoning next to each is so you remember why it's there
   when someone challenges it."*
2. **Recommend a use case.** Based on the frame, name the one or two use-case skills that fit, and
   say why in one sentence each. Use the routing table in `reference/output-format.md` §4. If the
   frame points at a use case the available data can't support, say that plainly and name what
   would.
3. Ask: *"Anything you want to sharpen before you lock it in?"* Adjust one thing at a time, re-show
   the block, and ask again until they're satisfied.

### Quietly record the deliverable

Write the derived deliverable to `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md` using
the file template in `reference/output-format.md` §2. Do this **silently** — don't announce the
path or make the user manage a file.

Then fold the essence into ground truth via `util_get_org_info`: the decision statement to
`set(02_Decisions, …)` and the audience to `set(05_Stakeholders, …)`, per
`reference/output-format.md` §3. One short section each, under stable headers so they update in
place.

## Guardrails

- **Never write the decision statement for the user.** Create the conditions, ask the question,
  let them write it. A frame they didn't author is a frame they can't defend in the room.
- The template in `1_Class/L1.2-Decision-Frame/` is theirs and human-owned. Guide them to fill it;
  never fill it for them.
- **Do not let them skip to the data.** If they push to start analyzing, say: *"We'll get there in
  ten minutes, and you'll analyze half as much."* Hold the line once; if they insist, note the risk
  and continue — it's their call, not yours.
- If the stated ask is a solution rather than a question ("build me a dashboard"), don't argue with
  it — ask what they'd do differently once they had it. The answer is the real frame.
- If nothing would change the decision-owner's mind, name it once, without cynicism, and ask what
  they want to do. Sometimes the right move is a different question; sometimes it's a different
  audience.
- Resolve inputs through `util_get_inputs`; read `0_Org/` and `0_User/` only through their
  utilities.

## Quick reference

| Field | Core question | Done when |
|---|---|---|
| Decision | What choice is being made? | There's a verb and at least two options |
| Owner | Who signs? | A person or role, not a committee noun |
| Trigger | What forces it, and when? | A date and a reason |
| Mind-changer | What evidence would move them? | Something specific enough to go look for |
| Good enough | How precise does this need to be? | A tolerance, not "as accurate as possible" |
