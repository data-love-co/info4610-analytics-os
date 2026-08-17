# The Question Ladder

Load this after mode routing. Two entry points, one destination: a decision specific enough to be
wrong.

---

## Mode A — Excavate (they were handed an ask)

Someone asked for a thing. The thing is a proxy for a decision, and the proxy is usually wrong in
an interesting way. Climb down from the request to the decision underneath it.

**Rung 1 — Get the ask verbatim.**
*"What exactly did they ask you for? Their words, not your translation."*
Write it down as stated. "Can you pull the numbers on churn" is different from "why are we losing
customers," and the difference matters.

**Rung 2 — What would they do with it?**
*"Say I hand you a perfect version of that tomorrow morning. What happens next?"*
If the honest answer is "it goes in a deck," ask what the deck is for. Keep going until you reach
something someone does.

**Rung 3 — What's the choice underneath?**
*"So the real question is whether to [X] or [Y]?"*
Offer your read and let them correct it. People are much better at fixing a wrong frame than
producing one from scratch — a specific wrong guess is more useful here than an open question.

**Rung 4 — Why now?**
*"This has probably been true for a while. Why is it on your desk this week?"*
The answer names the trigger and usually the deadline. It also occasionally reveals that the
request came from a different conversation than the user thinks.

**Rung 5 — Who actually decides?**
*"Who has to say yes for anything to change?"*
Sometimes the person who asked and the person who decides are different people. That changes what
the analysis has to look like.

**Common excavation results:**

| The ask | What it usually turns out to be |
|---|---|
| "Build me a dashboard" | "I don't trust the number I'm reporting upward" or "I'm being asked the same question weekly and I want to stop" |
| "Pull the churn numbers" | "Should we fund a retention program, and at what size?" |
| "How did the campaign do?" | "Do we run it again, and with what budget?" |
| "I need a forecast" | "Do we commit to a number I'll be held to?" |
| "Analyze the survey" | "What do we fix first, given we can fix two things?" |
| "Can you look at this spreadsheet" | "Someone challenged a number and I need to know if they're right" |

---

## Mode B — Construct (they have a problem, no ask)

They know something's wrong. Turn it into a question with an answer.

**Rung 1 — Name the gap.**
*"What's happening that shouldn't be — or not happening that should?"*
Push for something observable. "Morale is bad" becomes "three of eight people on the team have left
in six months."

**Rung 2 — Size it.**
*"How big is it? Roughly is fine — an order of magnitude."*
This is a filter. If nobody can estimate the size within a factor of ten, that's the first finding,
and it may be the whole project.

**Rung 3 — What could be done about it?**
*"If you could wave a wand, what are the two or three things anyone could actually do here?"*
The options ARE the decision. No options means no decision — it means a report.

**Rung 4 — Who'd have to approve each one?**
Different options often have different owners. If the only viable option needs an approver the user
has no access to, that's worth knowing now.

**Rung 5 — What's the cost of doing nothing?**
*"What happens if this stays exactly as it is for another two quarters?"*
This is what makes the memo land later. An analysis that can't answer this reads as optional.

---

## Constraint pass

Run all four before closing. Each one either confirms the frame or narrows it.

### Data
*"What data would settle this, and can you actually get it?"*

- Exists and they have it → proceed.
- Exists and they can't get it → who owns it, and how long to request? If longer than the deadline,
  narrow the question.
- Doesn't exist → what's the nearest question the available data *can* answer? Say plainly that
  it's a proxy, and note what it misses.
- **They have it but can't put it on this machine** → build the method on
  `5_Library/sample-data/` and re-point it at real data inside their environment later. Offer this
  early; for a lot of people it's the whole answer.

### Time
*"When's the decision, and how much of your time is real between now and then?"*

Working professionals are doing this alongside a full week. If the frame needs 20 hours and they
have 4, narrow it now. A smaller question answered well beats a big one abandoned.

### Authority
*"Are you in the room where this gets decided, or are you supplying someone who is?"*

Both are fine, but they produce different artifacts. Supplying someone else means the memo does
more work and the analysis has to survive being explained secondhand.

### Sensitivity
*"Is there anything about this that's politically or legally delicate?"*

Headcount, compensation, performance, anything touching a protected class, anything under a
confidentiality obligation. Not a reason to stop — a reason to know before you build. It shapes
what can be shown, at what grain, and to whom.

---

## When the frame won't hold

Three failure modes and what to do:

**"Nothing would change their mind."** The decision is made and the analysis is for cover. Say it
once, plainly and without cynicism: *"It sounds like this one's decided. Do you want to analyze it
anyway, aim at a different question, or aim at a different audience?"* All three are legitimate. It
is their workplace, not yours.

**The scope keeps growing.** Every question adds a dimension. Stop and ask: *"If you could only
answer one of these by Friday, which one?"* Then frame that one and note the others as follow-ons.

**No real decision exists.** Sometimes an ask is genuine curiosity, and curiosity is allowed. Say
so and reframe the goal: the artifact becomes something reusable — a dashboard someone maintains, a
model someone re-runs — rather than a one-time recommendation. That's a legitimate project with a
different success test.
