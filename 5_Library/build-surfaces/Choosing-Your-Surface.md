# Choosing Your Build Surface

Where to build the thing. This decision gets made badly more often than any other in the session,
almost always in the direction of building something impressive that nobody can maintain.

---

## Four questions, in order

**1. Who uses it after today?** Just you, your team, or an executive who opens it once?

**2. Does it need to refresh with new data, or is it a one-time answer?** This is the biggest fork in
the road. A one-time answer and a maintained tool are different products.

**3. Can they maintain it without you?** Building something you can't modify next month is building
a dependency, not a tool. Be honest here even when the better-looking option is available.

**4. What's allowed?** Corporate policy on installs, uploads, and where data can live. Check
`0_Org/06_Constraints.md` — this rules out surfaces before anything else does.

---

## The routing table

| Your situation | Build in | Why |
|---|---|---|
| Recipients live in spreadsheets and need to edit it | **Excel / Google Sheets** | Formulas are visible. No black box. They can change it without you |
| Show it once, in a meeting, polish matters, no maintenance | **A Claude artifact** | Interactive, self-contained, shareable as a link. Built in minutes |
| Recurring, refreshes with new data | **Claude Code** | A script plus a rendered output. Re-runnable, versionable, real |
| Exploring — one person working a problem | **Claude Code**, or Claude with the file attached | Iteration speed matters more than polish |
| Needs a designed interface, several screens, real visual quality | **Claude Design** | Purpose-built for interface design; hand off or build from it |
| Several people working the same documents and context | **Claude Cowork** | Shared workspace, shared files, multiple people |
| Answering questions from a fixed document set | **A Claude Project** with the docs attached | Fastest path to a grounded assistant. Often sufficient |
| Your org runs Tableau / Power BI with a team behind it | **Build the logic and definitions here; hand over the spec** | Don't rebuild their platform. Give them a spec they can implement in a day |

---

## The surfaces

### Claude Code

The agent in your terminal, desktop app, or VS Code. Reads your whole folder, writes and runs code,
edits files.

**Best for:** anything that has to be re-run, anything touching files on disk, anything you want
under version control. This entire workspace is designed around it.

**Cost:** a Claude subscription.

**The honest caveat:** if you've never used a terminal, budget twenty minutes of discomfort. It is
genuinely learnable in one session and it is the surface that pays off longest.

### Claude artifacts

Interactive pages Claude builds and hosts. HTML, charts, calculators, dashboards. Shareable as a
link.

**Best for:** a scenario calculator with sliders, a dashboard for one meeting, anything where
interactivity makes the argument.

**The tradeoff:** it's a snapshot. Refreshing with new data means rebuilding. Perfect for a one-time
answer, wrong for a monthly report.

### Claude Design

For interfaces — layout, visual design, multiple screens, real polish.

**Best for:** when what you're building is genuinely a *product* someone will use repeatedly, and it
needs to look like one. Also good for producing something a design or engineering team can build
from.

**Not for:** a chart and three numbers. That's an artifact or a spreadsheet.

### Claude Cowork

Shared workspace. Multiple people, shared files, shared context.

**Best for:** when the analysis is a team effort, when a colleague continues the work, or when the
output is a living document rather than a one-time artifact.

### Excel / Google Sheets

Not a lesser option. For a large share of the people in this room it is the correct one.

**Best for:** recipients who live in spreadsheets, anything they need to change themselves, anything
that has to survive you being on vacation.

**The rule if you build here:** formulas visible, no hidden sheets, definitions written in the sheet
itself. The reason spreadsheets endure is transparency — a spreadsheet with a hardcoded number
buried in a formula is worse than a script.

### Hand it to the BI team

If your organization runs Tableau, Power BI, Looker, or similar with a team behind it, **do not
rebuild their platform in a two-hour session.**

Build the logic, the metric definitions, and a worked example here. Hand them a spec. That's a
better contribution than a parallel dashboard that competes with the official one and dies when you
stop maintaining it.

---

## The tradeoff to say out loud

> "The interactive artifact will look better in your demo. The Excel version is what your team will
> still be using in March."

Both are legitimate. What's not legitimate is picking by default, or picking the impressive one and
discovering in six weeks that nobody can change it.

**If you want both:** build the artifact for the demo and the spreadsheet for the team. It's less
work than it sounds, because the analysis underneath is the same and it's already done.

---

## Three things that must survive into the built artifact

Regardless of surface. These are exactly what gets dropped under time pressure:

1. **The uncertainty is visible.** If the analysis had a range, the artifact shows a range. Dropping
   it is how a model turns into a promise.
2. **The definitions travel with the numbers.** A metric without its definition gets misread by the
   second person who sees it.
3. **The source and the date are on the artifact.** Someone finds this file in eight months and needs
   to know what it was built from.
