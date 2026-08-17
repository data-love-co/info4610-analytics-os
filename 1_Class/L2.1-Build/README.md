# L2.1 — Build Your Use Case

**Lesson 2 (6:00–7:50 PM), first block.** About 60 minutes. Build the thing.

You arrive with a framed decision and audited data. That's what makes an hour enough.

## What you do

1. **Open `L2.1-Build-Spec-Template.md` and fill the top half first.** Fifteen minutes. It's the
   difference between building the right thing and building something well.
2. **Run your use-case skill.** The one your L1.2 frame pointed at. Say what you want — "score my
   accounts", "forecast next quarter", "synthesize this survey" — and the skill takes it from there.
3. **Then run `build-and-ship`** to get it into a form someone else can use.

## The ten use cases

Pick one. Two if the first one lands fast.

| Skill | Say this | You end up with |
|---|---|---|
| `kpi-dashboard` | "build me a dashboard" | Clean metrics from a messy spreadsheet, plus a "so what" |
| `scenario-calculator` | "what if we raise prices" | A simulator with ranges, not single-point guesses |
| `forecast` | "forecast next quarter" | Trend + seasonality with honest uncertainty bands |
| `risk-scorer` | "which customers will churn" | Scored accounts with the top drivers exposed |
| `ab-test-readout` | "did this test work" | A hypothesis-test readout ending in ship / iterate / hold |
| `feedback-synthesizer` | "what are people saying" | Themes, sentiment, and verbatim quotes |
| `data-audit` | "is this data any good" | An audit and a cleaning log — sometimes the whole project |
| `meeting-to-actions` | "who owns what from this meeting" | Decisions, owners, deadlines, a draft email |
| `knowledge-assistant` | "answer questions from these docs" | Grounded Q&A that cites and refuses |
| `decision-memo` | "write this up for my VP" | That's L2.2 — but you can start early |

Not sure which? Ask: *"which skill should I use?"* The `find-skills` skill routes on the shape of
your problem, not on what you called it.

## Where to build it

Four questions decide this, in order:

1. Who uses it after today?
2. Does it need to refresh with new data, or is it a one-time answer?
3. **Can they maintain it without you?**
4. What's allowed on their machines?

`5_Library/build-surfaces/Choosing-Your-Surface.md` has the full comparison — Claude Code, Claude
Design, Cowork, artifacts, Excel, and handing a spec to a BI team.

**The tradeoff worth saying out loud:** the interactive artifact will look better in your demo. The
Excel version is what your team will still be using in March. Both are legitimate; pick
deliberately rather than by default.

## Three things that get dropped under time pressure

Check them before you call it done:

- **The uncertainty survived into the artifact.** If your analysis had a range, the built thing shows
  a range. This is exactly where intervals get quietly dropped, and dropping them turns a model into
  a promise.
- **The definitions travel with the numbers.** A metric without its definition gets misread by the
  second person who sees it.
- **The source and date are on the artifact.** In eight months someone will find this file and need
  to know what it was built from.

## Number check before you stop

Pick three numbers from your artifact at random and confirm they match the analysis document.
Mismatches between the built thing and the analysis are common, and they are fatal in a demo.

## Where work goes

- **You fill** `L2.1-Build-Spec-Template.md` by hand.
- The skill writes `2_Outputs/.agents/Use-Case/<Name>.md`.
- The built artifact goes in `4_Build_Projects/YYYY.MM Short Name/`.
