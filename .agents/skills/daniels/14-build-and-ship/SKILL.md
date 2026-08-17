---
name: build-and-ship
description: >
  Picks the right surface to build an analysis tool in — Claude Code, Claude Design, Cowork, an
  artifact, Excel, or a BI tool — builds it, then preps the demo. Use when: "where should I build
  this", "make this interactive", "turn this into a tool", "build the dashboard", "prep my demo",
  "how do I present this", "make it shareable". Sessions L2.1 and L2.3. Make sure to use this skill
  whenever someone has an analysis and needs it to become something other people can use or see.
---

# build-and-ship — Build It, Then Demo It

Two jobs. **Build:** get the analysis into a form someone else can use. **Ship:** get it in front
of the room without the demo eating the message.

The most common mistake here is building in the most impressive surface rather than the right one.
A finance director who will hand this to two colleagues who live in Excel should build it in Excel,
even though a React dashboard would look better in a demo. Optimize for who uses it on Tuesday.

## Phase 0 — Resolve and load inputs

Call **`util_get_inputs`** (`get("build-and-ship")`), then pull:

- **The use-case output** *(primary)* — from `2_Outputs/.agents/Use-Case/`, including its build spec
- **User profile** *(primary)* — via `util_get_user_info`. `02_Expertise` decides what they can
  maintain after the session ends, which is the constraint that matters most
- **The session template** *(primary)* — `1_Class/L2.1-Build/`
- **Constraints** *(supplementary)* — via `util_get_org_info` (`06_Constraints`). A locked-down
  laptop or a policy against uploading data rules out surfaces before anything else does

## Phase 1 — Choose the surface

**Load `5_Library/build-surfaces/Choosing-Your-Surface.md`** for the full comparison. Ask four
questions, in this order:

1. **Who uses it after this session?** Just the user, their team, or an executive who opens it once?
2. **Does it need to update with new data, or is it a one-time answer?** This is the biggest fork.
3. **What can they maintain?** Building something they can't modify next month is building a
   dependency, not a tool. Be honest about this even when the fancier option is available.
4. **What's allowed?** Corporate policy on uploads, installs, and where data can live.

Then recommend one, with the reason:

| Situation | Surface |
|---|---|
| Recipients live in spreadsheets; needs to be edited by them | **Excel / Sheets** — formulas visible, no black box |
| Show it once, in a meeting; wow matters; no maintenance | **An artifact or single HTML file** — interactive, self-contained, sendable as a link |
| Recurring, needs to refresh with new data | **Claude Code** — a script plus a rendered output, re-runnable |
| Exploring, iterating, one person working through a problem | **Claude Code**, or the analysis surface they already use |
| Needs a designed interface, multiple screens, real polish | **Claude Design**, then hand off or build from it |
| Team collaboration on documents and shared context | **Cowork** — shared workspace, multiple people, files in one place |
| The org has Tableau / Power BI and a team that maintains it | **Build the logic and the definitions here; hand over the spec.** Don't rebuild their platform |

**Say the tradeoff out loud.** "The artifact will look better in your demo. The Excel version is
what your team will actually still be using in March." Then let them choose — they know their
organization.

## Phase 2 — Build the smallest thing that answers the question

Build the version that answers the decision, then stop and show it. Do not build the complete
version before the user has seen anything.

Order of work:

1. **The number or the answer** — get it right first, in whatever form
2. **The primary view** — the one chart or table that carries the message
3. **Interaction, only if it earns its place** — a slider on the assumption that actually drives
   the answer, not sliders on everything
4. **Polish** — last, and only after the content is settled

For anything with charts, follow `5_Library/method/chart-choices.md`. The rules there are not
decoration; they're what makes a dashboard readable in ninety seconds and a comparison honest.

**Three things to get right regardless of surface:**

- **The uncertainty is visible.** Ranges, intervals, and caveats survive into the built artifact.
  This is exactly where they get dropped, and dropping them is how a model becomes a promise.
- **The definitions travel with the numbers.** A metric without its definition will be
  misinterpreted by the second person who sees it.
- **The data source and date are on the artifact.** Someone will find this file in eight months and
  need to know what it was built from.

## Phase 3 — Test it like a stranger

Before the demo, run through it as someone who wasn't in the room:

- Open it cold. Is it obvious what it shows and what to do with it?
- Are the axis labels, units, and time windows stated?
- Do the numbers match the analysis document? Check three at random. **Mismatches here are common
  and fatal in a demo.**
- Does it break on edge cases — an empty filter, an extreme slider value, a missing month?
- On someone else's screen: does it render? Does it need a login, a file they don't have, a font
  they don't have?

## Phase 4 — Prep the demo

**Load `reference/demo-prep.md`** for the full structure. The core:

**Five minutes, four beats.**

1. **The decision** (30 seconds) — what question this answers and who has to decide. Not "I built a
   dashboard." *"Our team has to choose between hiring and a contractor bridge by August 15th."*
2. **The answer** (60 seconds) — the recommendation, with the number. Lead with it. Never make the
   room wait through a tour of the interface to find out what you concluded.
3. **The show** (2 minutes) — the two or three interactions that prove it. Rehearsed. Not a tour.
4. **The honest part** (60 seconds) — what it can't do, what you'd do next. This is what separates a
   professional from a demo.

**Then prepare for the four questions you will get:**

- *"Where did the data come from?"* — source, date, row count, and what you cleaned. The cleaning
  log exists for this moment.
- *"How confident are you?"* — the interval, the backtest, or the validation. In one sentence.
- *"What if <assumption> is wrong?"* — the sensitivity analysis. Have the number.
- *"Could we also see <adjacent thing>?"* — know whether the data supports it. "Not with this data,
  and here's what we'd need" is a strong answer.

**Have a fallback.** Screenshots of the working tool, in order. Live demos fail — a file path, a
missing dependency, a laptop that won't project. A prepared fallback turns a disaster into a
fifteen-second detour.

## Closing

1. Show the built artifact and the demo script.
2. Do a dry run: *"Give me the five minutes. I'll play the skeptical VP."* Then actually be
   skeptical — ask the hard question they haven't prepared for. Better here than in the room.
3. Quietly write `2_Outputs/.agents/L2.3-Demo/Demo-Notes.md` with the script, the anticipated
   questions and answers, and the fallback plan.
4. Note where the built artifact lives — `4_Build_Projects/YYYY.MM Short Name/`.

## Guardrails

- **Never recommend a surface the user can't maintain**, unless they explicitly want a one-time
  artifact and understand that's what they're getting.
- **Never let uncertainty get dropped in the build.** If the analysis had a range, the artifact
  shows a range.
- **Never ship a chart that misleads** — truncated axes without a marked break, dual axes implying
  a relationship, pie charts with eight slices, 3D anything. See
  `5_Library/method/chart-choices.md`.
- Never demo without checking the numbers against the analysis document.
- Never build the impressive version when the useful version is different. Say which is which.
- Never upload data to an external service without the user's explicit say-so, and check
  `06_Constraints` first.
- The demo is theirs. Coach it, run the dry run, ask the hard question — but they present it.
