---
title: "Hand it to the BI team"
level: "Any"
best_for: "Organizations that already run Tableau, Power BI, or Looker"
---

# Hand It to the BI Team

If your organization runs a BI platform with a team behind it, don't rebuild their platform in a
two-hour session. A parallel dashboard competes with the official one, confuses people about which
number is real, and dies the moment you stop maintaining it.

**What to build instead:** the logic, the definitions, and a worked example. Then hand over a spec.

## What a good spec contains

1. **The decision it serves** — one line. This is what gets it prioritized above the other forty
   requests in their queue
2. **The metrics, with full definitions** — numerator, denominator, filters, window, source system.
   This is the part they can't write for you and the part that takes them longest to extract
3. **A worked example** — one period computed by hand or in a spreadsheet, so they can validate their
   implementation against a known answer
4. **The layout** — what's prominent, what's secondary, what's a footnote
5. **The refresh cadence and the owner**
6. **The caveats** — anything the audit found that changes how a number should be read

## Why this beats handing over a dashboard

You're giving them the part that requires knowing the business and letting them do the part that
requires knowing the platform. A well-specified metric definition typically saves a BI team more time
than a mockup does — and it's the piece that almost never gets written down anywhere.

It also survives you changing roles, which a personal dashboard does not.

## Where the spec comes from

The build spec section of your use-case output in `2_Outputs/.agents/Use-Case/`, plus the definitions
in `0_Org/03_Metrics.md`. Both are already written by the time you get here.
