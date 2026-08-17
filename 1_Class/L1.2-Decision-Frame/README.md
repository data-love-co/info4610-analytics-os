# L1.2 — Frame the Decision

**Lesson 1, second block.** About 30 minutes. The most important thirty minutes of the two sessions,
and the ones that feel least like progress while you're in them.

## The idea

**An analysis with no decision attached is a hobby.**

The most common failure in corporate analytics is not bad math. It is a technically flawless answer
to a question nobody was asking — usually because the analyst started from the data that was
available instead of the choice that was pending.

Five fields make a frame. Each has to be specific enough to be wrong:

1. **The decision** — not the topic. A verb and at least two options. "Should we extend the
   contractor bridge or fill the reqs" is a decision. "Understand our staffing situation" is a
   topic.
2. **The owner** — a named person or role who can actually make the call. Not "leadership."
3. **The trigger and deadline** — what forces this, and when. If nothing forces it, the decision may
   not be real, and it's better to find that out now.
4. **What would change their mind** — the hardest question in the exercise and the one that defines
   what your analysis has to produce. If nothing would change the owner's mind, the decision is
   already made and you're being asked for cover. Worth knowing.
5. **Good enough to act on** — how wrong could this be and still lead to the same choice? This is
   what makes a two-hour build possible instead of a two-week one.

## What you do

Open `L1.2-Decision-Frame-Template.md` and start the `frame-the-decision` skill: *"help me frame my
decision."*

The skill asks two things up front — do you have a specific ask from someone, or a problem with no
ask? — then routes accordingly. It works one field at a time, and it will not let you move on from a
vague answer. **You write the fields; the skill will not write them for you.**

At the end it recommends which use-case skill fits your frame, and which is the runner-up.

## Don't skip to the data

You will want to. Everybody wants to — opening the spreadsheet feels like starting, and this feels
like talking about starting.

Fifteen minutes here typically halves the amount of analysis you end up doing, because most of what
people build turns out not to bear on the decision. That's the trade.

## Where work goes

- **You fill** `L1.2-Decision-Frame-Template.md` by hand. It stays in this folder.
- The agent's derived deliverable lands in `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md`.
- The decision statement and the audience fold into `0_Org/` for the next skill to read.

## If the frame won't hold

Three things happen often enough to name:

- **Nothing would change the owner's mind.** The decision is made. Analyze it anyway, aim at a
  different question, or aim at a different audience — all three are legitimate.
- **The scope keeps growing.** Answer one question by Friday. Note the rest as follow-ons.
- **There's no real decision, just curiosity.** That's allowed. The goal shifts from a
  recommendation to something reusable — a dashboard someone maintains, a model someone re-runs.

Bring any of these to the room. They're more interesting than a clean frame.
