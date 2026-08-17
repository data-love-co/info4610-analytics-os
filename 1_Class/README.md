# 1_Class — The Two Sessions

One self-contained subfolder per block. This is where the work *happens* during class — not where
outputs land.

Each session subfolder holds:
- `README.md` — what happens in that block and what you do
- the working **template** for the exercise (master copy in `5_Library/templates/`) — **you complete
  it by hand, and your completed version stays in this folder**

## The map

| Folder | Block | Exercise | Skill |
|---|---|---|---|
| `Slides/` | both | The session decks | — |
| `L1.1-Setup/` | Lesson 1 | Set up the workspace, load data | `analyst-bootstrap`, `ingest-data` |
| `L1.2-Decision-Frame/` | Lesson 1 | Frame the decision | `frame-the-decision` |
| `L1.3-Data-Audit/` | Lesson 1 | Audit the data, log the cleaning | `data-audit` |
| `L2.1-Build/` | Lesson 2 | Build your chosen use case | one of skills 5–12, then `build-and-ship` |
| `L2.2-Decision-Memo/` | Lesson 2 | Write the memo | `decision-memo` |
| `L2.3-Demo/` | Lesson 2 | Present it | `build-and-ship` |

## Why the first session doesn't build anything

Lesson 2 is a two-hour build. That's only possible if you arrive knowing what you're building and
whether the data supports it. Lesson 1 buys that.

The two most common ways this kind of project fails have nothing to do with the tool: you build a
beautiful answer to a question nobody asked, or you build on data that can't hold the weight. L1.2
and L1.3 exist to catch both, at a cost of about ninety minutes.

## The rule

You complete the templates **by hand**. The agent never fills them in.

That isn't ceremony. Writing the decision statement yourself is what makes you able to defend it in
a room, and the difference between a frame you wrote and one that was written for you shows up the
first time someone pushes back on it.

Where things go:
- `1_Class/<session>/` — your hand-completed template. **Human-owned.**
- `2_Outputs/.agents/<session>/` — the agent's derived deliverable. **Agent-owned, don't hand-edit.**
- `0_Org/` — the distilled essence the next skill reads.

Each session is self-contained: opening any one folder gives you everything you need for that block.
