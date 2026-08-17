---
name: scenario-calculator
description: >
  Builds a what-if simulator for a pricing, staffing, budget, or capacity decision — one that shows
  a realistic range of outcomes instead of a single-point guess, and exposes which assumptions
  actually drive the answer. Use when: "what if we raise prices", "model a staffing scenario",
  "build a budget calculator", "how many people do we need", "what happens if volume doubles",
  "break-even analysis", "sensitivity analysis". Session L2.1. Make sure to use this skill whenever
  a decision depends on assumptions nobody can know for certain.
---

# scenario-calculator — What-If Simulator

You are building the model someone uses in a room to answer "and what if we're wrong about that?"

The whole value of this use case is in refusing the single number. A spreadsheet that says the new
pricing yields $2.4M in incremental revenue is worse than useless — it is confidently wrong, and it
will be quoted for a year. A model that says "somewhere between $0.9M and $3.1M, and it hinges
almost entirely on how many customers downgrade" is honest, and it tells you what to go find out.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("scenario-calculator")`), then pull:

- **The decision frame** *(primary)* — `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md`.
  The options in the frame are the scenarios; the tolerance tells you how precise the model needs
  to be.
- **The data** *(primary)* — whatever grounds the assumptions:
  `5_Library/sources/processed/`, or `5_Library/sample-data/staffing_model_inputs.csv` for practice.
- **Org ground truth** *(primary)* — via `util_get_org_info`, especially `03_Metrics` and
  `06_Constraints`.
- **The audit** *(supplementary)* — if the input data was audited, respect what it flagged.
- **User profile** *(supplementary)* — technical comfort decides where this gets built.

## Phase 1 — Write the model as an equation, in words, before any numbers

Ask the user to state the outcome and how it's produced, in plain language. Then write it back as a
structure and get their agreement. Example:

> Annual support cost = (tickets per month × 12) ÷ (tickets per FTE per year) × fully loaded
> cost per FTE, plus (hires × cost to hire), plus (overtime hours × blended rate × 1.5)

**Do not skip this.** Ninety percent of what goes wrong in scenario models is a structural error —
a double count, a missing cost, a rate applied to the wrong base — not a bad assumption value. A
structural error survives every sensitivity test you run on it.

Then classify every term. **Load `reference/model-structure.md`** for the full method. The short
version:

| Type | Meaning | Treatment |
|---|---|---|
| **Lever** | Something the decision-maker controls | Varies by scenario |
| **Assumption** | Something uncertain that must be estimated | Gets a range, always |
| **Constant** | Known and stable | Single value, cited |
| **Constraint** | A hard limit reality imposes | Bounds the output |

If a term can't be classified, the structure isn't finished. Go back.

## Phase 2 — Put a range on every assumption

This is the step people resist and the step that makes the model worth building.

For each assumption, ask for three values: **low, expected, high.** Frame it in a way people can
actually answer:

- Not: *"What's the standard deviation of your attrition rate?"*
- Yes: *"What would attrition have to be for you to be genuinely surprised? On the low side? On the
  high side?"*

Then record **where each range came from** — historical data, a vendor quote, someone's judgment,
or a guess. Label the guesses as guesses. A model where three inputs come from four years of
history and one is a hunch behaves very differently from one where everything is a hunch, and the
reader deserves to know which they're holding.

**Anchor to history wherever it exists.** If the data has four years of attrition, the range should
reflect what actually happened, not what someone remembers happening.

## Phase 3 — Run the scenarios

Produce, at minimum:

1. **Base case** — every assumption at its expected value.
2. **Downside** — the assumptions that hurt, at their unfavorable end. Not every assumption at its
   worst simultaneously; that compounds into a scenario with a vanishingly small probability. Pick
   the two or three that plausibly go wrong together.
3. **Upside** — the same logic, favorable direction.
4. **One scenario per option** in the decision frame, so the options are directly comparable.

If the user is comfortable with it and the model has more than three uncertain inputs, run a simple
Monte Carlo — sample each assumption from its range a few thousand times and report the
distribution. Ten lines of Python. It converts "somewhere between X and Y" into "70% of the time
it lands between X and Y," which is a materially better sentence to say in a meeting.
`reference/model-structure.md` § *Monte Carlo* has the method and when it's overkill.

## Phase 4 — Find what actually drives the answer

**This is the deliverable people remember.** Vary one assumption at a time across its range, holding
the rest at expected, and rank by how much the outcome moves. A tornado chart if you're building
visuals; a ranked table if not.

Then say the useful thing out loud: *"The answer hinges on downgrade rate. Everything else is
noise. If you're going to spend a week researching one number before this decision, spend it
there."*

That sentence is often worth more than the model.

## Phase 5 — Find the break-even

For each option, solve for the value that flips the decision. *"This pays for itself if monthly
volume stays above 1,850 tickets. You've been above that for eleven of the last twelve months."*

Break-even framing is how a model becomes usable by someone who will never open it. It converts a
range into a single thing to watch.

## Closing

**Load `reference/output-format.md`** and:

1. Show the scenario table, the sensitivity ranking, and the break-even in chat.
2. Ask which assumptions they want to challenge. Re-run. Repeat until they stop arguing with it —
   that's the sign it's ready to show someone else.
3. Quietly write `2_Outputs/.agents/Use-Case/Scenario-Calculator.md` with the structure, the
   assumption register, the scenarios, the sensitivity ranking, and the build spec.
4. Fold the decision-relevant finding into `util_get_org_info` (`set(07_Insights, …)`).

Then hand to **`build-and-ship`** if they want an interactive version — sliders on the levers, the
outcome and range updating live. That's a good artifact and a fast build.

## Guardrails

- **Never report a single number as the answer.** Every output is a range with a stated basis. If
  the user insists on one number for a slide, give them the base case *with the range printed next
  to it* and say plainly that the range is the honest part.
- **Never present a guess as an estimate.** The assumption register records the source of every
  range, and guesses are labeled.
- **Never compound every assumption to its worst simultaneously** and call it the downside — that's
  a scenario that will essentially never occur, and it makes the model easy to dismiss.
- Show the structure before the numbers. A structural error is invisible in the output.
- Don't add precision the inputs don't support. If attrition is "somewhere between 10 and 20
  percent," the output is not $2,847,193.
- If the model's answer is dominated by one assumption nobody has data for, **say that the model
  can't decide this yet** and name what to go measure. That's a legitimate and valuable finding.
- The user owns the assumptions. You structure and compute; they supply and defend the numbers.
