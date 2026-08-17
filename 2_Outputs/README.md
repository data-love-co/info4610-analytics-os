# 2_Outputs — Agent Work Products

The full record of what the **agent** produces — the markdown deliverable each skill writes, derived
from your hand-completed template plus the evidence. This is what you share, show to stakeholders,
and build on.

This top level is a pointer. The actual outputs live in a dotfile-prefixed `.agents/` layer —
agent-owned, **not hand-edited** — mirroring `1_Class/` session for session:

```
2_Outputs/
└── .agents/                        # agent-owned working layer (don't hand-edit)
    ├── L1.2-Decision-Frame/Decision-Frame.md
    ├── L1.3-Data-Audit/Data-Audit.md · Cleaning-Log.md
    ├── Use-Case/<Name>.md          # whichever use case you built, + any data it produced
    ├── L2.2-Decision-Memo/Decision-Memo.md
    └── L2.3-Demo/Demo-Notes.md
```

## Three homes, two owners

- **`1_Class/<session>/`** — your hand-completed template. **Human-owned.** You fill these; the agent
  never does.
- **`2_Outputs/.agents/<session>/`** — the agent's full work products. **Agent-owned, not
  hand-edited.** What you point stakeholders to.
- **`0_Org/`** — only the distilled essence the next skill reads.

All three grow together.

## Why the outputs are hidden in a dotfolder

So you don't confuse them with your own work. The template in `1_Class/` is where your thinking
lives, and it's the artifact that makes you able to defend the analysis. The generated file is a
reference document — accurate, complete, and not something you should be editing by hand, because
the next skill in the chain reads it.

If you want to change what's in a generated file, re-run the skill rather than editing it. Otherwise
the chain reads something you changed and the agent's reasoning silently diverges from the record.

## Before you share any of this

These files are tracked in git. Check them for anything that shouldn't leave your machine —
customer names, employee names, account numbers, salary detail. The agent is instructed to flag
these, but you're the one who signs off.
