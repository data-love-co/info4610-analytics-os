# L2.3 — Demo

**Lesson 2 (6:00–7:50 PM), final block, about 25 minutes.** Show what you built and what you
learned.

> **On timing.** The block holds roughly five full demos. With a larger group your instructor will
> run one of these instead: volunteers only, two-minute lightning rounds, or table groups where each
> table sends one. **Prepare the full five minutes regardless.** Building the four beats is the
> exercise, and a five-minute structure cuts down to two cleanly. A two-minute structure does not
> expand.

## The structure

Four beats. Time them — five minutes is shorter than it feels.

**1. The decision (30 seconds).** Open with the question and the stakes, not the artifact. *"Our
backlog grew 46% in eleven days and we have to choose between hiring and contractors by August
15th."* Not *"I built a staffing model in Claude Code."* Nobody cares what you built until they know
what it's for.

**2. The answer (60 seconds).** The recommendation, with the number, before the tour. This is
counterintuitive and correct — if the demo breaks at minute three, the room already has what it
needs.

**3. The show (2 minutes).** Two or three interactions, rehearsed, each chosen because it proves
something. One that shows the range. One that shows the conclusion holds under pressure. One that
shows it's built on real data. **Not a tour of the features.**

**4. The honest part (60 seconds).** What it can't do, and what you'd do next. This is the beat that
separates someone presenting analysis from someone presenting a demo, and it reliably earns the most
credibility in the room.

## What you do

Open `L2.3-Demo-Notes-Template.md` and write the words you'll actually say. Bullet points about what
you'll cover turn into rambling under pressure.

Then ask the agent for a dry run: *"give me the five minutes, and play the skeptical VP."* Have it
actually be skeptical — go after the weakest point. Much better to discover the hole here.

## Prepare for four questions

You will get some version of all four:

- **"Where did the data come from?"** — source, extract date, row count, and what you cleaned. Point
  at the cleaning log. That ends this line of questioning immediately.
- **"How confident are you?"** — the interval, the backtest, or the validation, in one sentence.
  Never answer this with "very."
- **"What if that assumption is wrong?"** — the sensitivity analysis. Know your break-even.
- **"Can we also see X?"** — know whether the data supports it. *"Not with this data, and here's
  what we'd need"* is a strong answer. Improvising a number is not.

## Have a fallback

Live demos fail — a file path, a missing dependency, a laptop that won't project. Screenshots of
every state you plan to show, in order, in one file. The key numbers written down. If it breaks, say
"let me show you the screenshots" and keep going. Do not debug in front of the room.

## What gets talked about afterward

Not the prettiest artifact. Usually one of these:

- Someone who found their data couldn't answer the question they framed, said so, and narrowed to
  what it *could* answer
- Someone whose model didn't beat the rule their team already uses, and reported that
- Someone who realized in L1.2 that nothing would change their decision-maker's mind

Those are the sessions people remember, and they're all findings.

## Where work goes

- **You fill** `L2.3-Demo-Notes-Template.md` by hand.
- The agent writes `2_Outputs/.agents/L2.3-Demo/Demo-Notes.md`.
