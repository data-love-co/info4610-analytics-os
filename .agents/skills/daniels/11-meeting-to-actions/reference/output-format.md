# Output Format

## 1 — What to show in chat

Lead with the gaps. They're what the user can still fix.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<Meeting> — <date>   ·   <n> attendees
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEEDS RESOLUTION BEFORE THIS GOES OUT
  ⚠ Writer conflict — Tom needs them for the help center in August,
    Aisha needs them for onboarding docs in August. Not resolved.
  ⚠ Overtime model — Dana offered to build it. Nobody confirmed she owns it.
  ⚠ Implementation writeup — Aisha agreed to do it. No date set.
  ⚠ Assumed decided, wasn't — the room proceeded as if help center ships
    in August, but that depends on the writer conflict above.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DECIDED
  • SSO maintenance window moved to Sat Aug 15 (Aug 8 conflicts with close)
  • Clean backlog number due Jul 22, ahead of the board deck on the 24th
  • Ship the help center rewrite — downside is small even if deflection
    lands below the estimate

ACTIONS
  Owner      What                                        By
  Marcus     Clean triaged backlog count                 Jul 22
  Dana       Model overtime vs. contractor bridge        [NO DATE]
  Rachel     Post the 5 approved reqs                    [NO DATE]
  Ken        Send SSO calendar invite + customer notice  Aug 1
  Aisha      Write up implementation changes             [NO DATE]
  Tom        Check platform team re: manual report       [NO DATE]
  [UNASSIGNED] Resolve the writer conflict               before Aug

OPEN
  • Which two of the four backlog levers to pull — deferred pending
    the clean number
  • Whether reqs filling in August changes the Q4 forecast (Dana to
    revisit in September)
  • Vendor consolidation — pushed to next week

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DRAFT FOLLOW-UP  (review before sending — 3 inferred owners marked *)
<the email>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 2 — The deliverable → `2_Outputs/.agents/Use-Case/Meeting-Actions.md`

```markdown
---
type: meeting-actions
session: L2.1
meeting: <name>
meeting_date: <date>
attendees: <n>
date: <today>
---

# <Meeting> — <date>

## Needs resolution

| # | Issue | Why it matters | Who can settle it |
|---|---|---|---|

## Decisions

| # | Decision | Decided by | Conditions | Source |
|---|---|---|---|---|
| 1 | SSO window moved to Sat Aug 15 | Ken, agreed by room | none | "the following Saturday works, August 15th" |

## Actions

| # | Owner | Action | Due | Source wording |
|---|---|---|---|---|
| 1 | Marcus | Produce triaged backlog count | Jul 22 | "so Marcus said fine, the 22nd" |
| 2 | Dana* | Model overtime vs. contractor bridge | [NO DATE] | "Dana said she'd model it" |

\* inferred — confirm with the owner.

## Open questions

| # | Question | Raised by | Blocking |
|---|---|---|---|

## Discussion (context, no action)

- <brief>

## Not captured

<Anything in the notes too ambiguous to categorize. Say so rather than forcing it.>
```

## 3 — The email

Structure. Adapt the voice to `03_Preferences` in `0_User/`.

```
Subject: <Meeting> — decisions and next steps

<One line of context.>

Decided
• <decision>
• <decision>

Actions
  Owner     What                              By
  Marcus    Clean backlog count               Jul 22
  Ken       SSO invite + customer notice      Aug 1
  Dana      Overtime vs. contractor model     <need a date>

Still open — flagging these because I don't think we closed them:
• <Person> and <Person> both need <resource> in August. Can we sort
  this before the reqs get posted?
• Dana — confirming you're taking the overtime model?
• Aisha — what's a realistic date for the implementation writeup?

<One closing line: what happens next and when.>
```

**Rules for the draft:**

- Under 200 words. Longer follow-ups get skimmed and the actions get lost.
- Actions in a table. Prose action items are invisible.
- Gaps phrased as questions to named people. That's what gets them answered.
- No commitment appears that wasn't made in the room. Where a date is missing, the email asks.
- Mark every inferred owner so the user can check it before sending.

## 4 — The essence into ground truth

Only if the meeting moved something already tracked. `util_get_org_info` `set(02_Decisions, …)`:

```markdown
## Current Decision

<Update the tracked decision with what the meeting settled, what it left open, and the new date.>
```
