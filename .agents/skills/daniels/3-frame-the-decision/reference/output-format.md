# Output Format

Load this at the Closing step for the exact formats.

## 1 — What to show the user (their conclusions)

Present the conclusions so they can finalize their template. The `← why` trace is what teaches the
habit of grounding a frame in something other than assertion.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR DECISION FRAME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision:     Should we [option A] or [option B]?
              ← why: [what the ask or problem turned out to be]

Owner:        [name or role, the person who signs]
              ← why: [how you established they're the decider]

Trigger:      [what forces it] by [date]
              ← why: [budget cycle / renewal / board meeting / escalation]

Changes it:   [the evidence that would move the owner off their prior]
              ← why: [what they said when asked directly]

Good enough:  [the tolerance — "within 15%", "more than 20 or fewer than 10"]
              ← why: [what the decision is actually sensitive to]

Constraints:  data — [what's available / what isn't]
              time — [hours available before the deadline]
              sensitivity — [privacy, policy, or political limits]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 2 — The derived deliverable file (written quietly)

Write to `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md`. Silently; don't announce the
path.

```markdown
---
type: decision-frame
session: L1.2-Decision-Frame
date: <today>
---

# Decision Frame

**Decision:** Should we [option A] or [option B]?

**Owner:** [name or role]
**Trigger:** [what forces it] — [date]

## What would change the owner's mind

[The specific evidence. This is what the analysis has to produce.]

## Good enough to act on

[The tolerance. What precision the decision actually needs, and why.]

## Options on the table

1. [Option A] — owner: [who approves]
2. [Option B] — owner: [who approves]
3. [Do nothing] — cost of doing nothing: [what happens]

## Constraints

| Constraint | Status |
|---|---|
| Data | [what exists, what's reachable, what isn't] |
| Time | [hours available before the decision] |
| Authority | [in the room / supplying someone in the room] |
| Sensitivity | [privacy, policy, political limits] |

## Recommended use case

**[skill name]** — [one sentence on why this fits].

Runner-up: **[skill name]** — [why it's second].

## Open questions

- [Anything unresolved that could change the frame]
```

## 3 — The essence folded into ground truth

Two calls to `util_get_org_info`, each under a stable header so repeat runs update in place.

`set(02_Decisions, …)`:

```markdown
## Current Decision

Should we [option A] or [option B]? Owned by [role], forced by [trigger] on [date].
Moves on: [what would change their mind]. Tolerance: [good enough].
```

`set(05_Stakeholders, …)`:

```markdown
## Decision Audience

[Name or role] — decides [what]. Cares about [what they actually optimize for].
Wants [level of detail]. [Anything known about how they read analysis.]
```

## 4 — Use-case routing

Recommend from the frame, not from what the user asked for at the start. One primary, one
runner-up, one sentence each.

| If the decision hinges on… | Route to |
|---|---|
| Knowing where you currently stand across several measures | `kpi-dashboard` |
| Choosing between options whose outcomes depend on assumptions | `scenario-calculator` |
| What a number will be in a future period | `forecast` |
| Which accounts, customers, or cases to act on first | `risk-scorer` |
| Whether a change that was already tried actually worked | `ab-test-readout` |
| What a large volume of people said, in their own words | `feedback-synthesizer` |
| Whether the data can be trusted at all | `data-audit` (it may be the whole project) |
| Getting a group to commit to owners and dates | `meeting-to-actions` |
| People repeatedly asking what a document already answers | `knowledge-assistant` |
| Persuading a specific person of a conclusion you already have | `decision-memo` |

**Two routing notes worth stating out loud:**

- If the audit in L1.3 hasn't run yet and the data is unfamiliar, `data-audit` comes first
  regardless of which use case fits. Building a forecast on an unaudited extract is how people end
  up presenting a duplicate-row artifact as a growth trend.
- If the frame's tolerance is wide ("more than 20 or fewer than 10"), say so — it often means the
  simplest of the candidate use cases is sufficient, and the user can stop earlier than they
  expected. That's a good outcome, not a small one.
