# Demo Prep

Load at Phase 4.

---

## The five-minute structure

Time it. Five minutes is shorter than it feels, and the most common failure is spending three of
them on the interface before anyone knows what the tool concluded.

### Beat 1 — The decision (30 seconds)

Open with the question, not the artifact.

> "Our support backlog grew 46% in eleven days. We have to choose between filling five open reqs
> and bridging with contractors, and the decision goes to the VP on August 15th."

Not: "I built a staffing model in Claude Code with an interactive front end."

Nobody cares what you built until they know what it's for. Thirty seconds of stakes buys you the
next four minutes of attention.

### Beat 2 — The answer (60 seconds)

The recommendation, with the number, before the tour.

> "The contractor bridge wins under every scenario we tested, and it's not close — the ramp time on
> new hires means we don't feel the headcount until October, which is after the peak we're trying
> to cover. The gap is between $180K and $400K depending on how volume lands."

Leading with the answer is counterintuitive and correct. If the demo fails at minute three, the
room already has what it needs.

### Beat 3 — The show (2 minutes)

Two or three interactions. Rehearsed, in order, chosen because each proves something.

- **The one that shows the range.** Move the assumption that drives the answer; show the output move.
- **The one that shows robustness.** Push it to an extreme and show the conclusion holds.
- **The one that shows it's real.** Point at actual data — the source, the row count, the date.

**Not a tour of the features.** Nobody needs to see every filter. Three deliberate moves that make
an argument.

### Beat 4 — The honest part (60 seconds)

What it can't do, and what you'd do next.

> "This assumes contractor productivity at 70% of a full-time rep, which is a judgment call, not a
> measurement — it's the number I'd want to firm up before anyone signs anything. And it doesn't
> model attrition risk from running the current team hot for another quarter, which is real and
> which I couldn't quantify with what we have."

This beat is what separates someone presenting analysis from someone presenting a demo. It is also,
reliably, the part that earns the most credibility in the room.

---

## The four questions you will get

Prepare a one-sentence answer to each. Have the backup number ready.

**"Where did the data come from?"**
Source system, extract date, row count, and what you changed. *"The ticket export from Zendesk,
pulled August 3rd, 8,400 rows. I dropped three duplicate rows and normalized four date formats —
it's all in the cleaning log."* Having a cleaning log to point at ends this line of questioning
immediately.

**"How confident are you?"**
The interval, the backtest, or the validation, in one sentence. *"The forecast method missed by
about 7% on average over the last year of held-out data, so treat the three-month number as roughly
±14%."* Never answer this with "very."

**"What if <assumption> is wrong?"**
The sensitivity analysis. *"If contractor productivity is 50% instead of 70%, the gap narrows to
about $90K but the recommendation doesn't flip. It would flip below 40%."* Know your break-even.

**"Can we also see <adjacent thing>?"**
Know in advance whether the data supports it. Three good answers: yes and here it is; not with this
data, and here's what we'd need; that's a different question and here's how I'd approach it. The
bad answer is improvising a number.

---

## The hostile question

Someone will ask the question that undermines the whole thing. Find it before the room does.

Ask yourself: *what's the single strongest reason not to believe this?* Then prepare a real answer,
not a deflection. If the honest answer is "that's a real limitation and it's why I'm recommending we
revisit in 60 days," say that. Analysts who acknowledge a good objection gain credibility; analysts
who defend against one lose it.

**In the dry run, actually ask it.** Play the skeptical VP and go after the weakest point. It is a
much better place to discover a hole than the meeting.

---

## Fallback plan

Live demos fail. Prepare for it and it costs fifteen seconds instead of the room.

- **Screenshots of every state you plan to show**, in order, in one file. Not a folder — one file
  you can open and page through.
- **The numbers written down** so you can say them if nothing renders.
- **Know the one thing to show** if you have thirty seconds instead of five minutes. Usually the
  chart with the range on it.
- **Test on the actual setup** if you can — projector, screen share, someone else's laptop. Fonts,
  resolution, and dark mode all break things that worked locally.

If the demo does fail, say "let me show you the screenshots" and keep going. Do not debug in front
of the room. The analysis is the point; the tool is evidence.

---

## The demo notes file → `2_Outputs/.agents/L2.3-Demo/Demo-Notes.md`

```markdown
---
type: demo-notes
session: L2.3-Demo
artifact: <path or link>
duration: 5 min
date: <today>
---

# Demo — <what you built>

## Script

**Beat 1 — Decision (0:00–0:30)**
> <what you say>

**Beat 2 — Answer (0:30–1:30)**
> <what you say, with the number>

**Beat 3 — Show (1:30–3:30)**
1. <interaction> — proves <what>
2. <interaction> — proves <what>
3. <interaction> — proves <what>

**Beat 4 — Honest part (3:30–4:30)**
> <limitations and next step>

## Anticipated questions

| Question | Answer | Backup number |
|---|---|---|
| Where's the data from? | | |
| How confident? | | |
| What if <assumption> is wrong? | | |
| Can we see <adjacent>? | | |

## The hostile question

**Q:** <the strongest objection>
**A:** <the real answer, not a deflection>

## Fallback

- Screenshots: `<path>`
- Key numbers if nothing renders: <list>
- The one thing to show in 30 seconds: <which view>

## After the demo

**Leave-behind:** <the memo, the artifact link, or both>
**Follow-up owed:** <to whom, what, by when>
```
