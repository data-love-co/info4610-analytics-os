# build-surfaces/ — Where to Build It

Two different questions live here.

**"Which assistant am I running?"** → **[Using-Another-Assistant.md](Using-Another-Assistant.md)**.
This workspace is built for Claude Code, but `AGENTS.md` is an open standard read by Copilot,
Codex, Cursor, Gemini CLI and twenty-odd other tools, so the whole chain runs on those too.
ChatGPT and other upload-and-analyze tools handle all ten use cases with a bit more manual
carrying, using **[Portable-Prompts.md](Portable-Prompts.md)**. Copilot is free for students.

**"Where do I build the thing I'm making?"** → **[Choosing-Your-Surface.md](Choosing-Your-Surface.md)**,
the four questions and the routing table.

The `tools/` folder has a one-page note on each surface: what it's for, what it costs, how to start,
and what to watch out for.

| Surface | Best for |
|---|---|
| [Claude Code](tools/claude-code.md) | Anything re-runnable, anything touching files, anything versioned |
| [Claude Artifacts](tools/claude-artifacts.md) | One interactive thing to show in one meeting |
| [Claude Design](tools/claude-design.md) | A real interface someone uses repeatedly |
| [Claude Cowork](tools/claude-cowork.md) | Several people working the same files |
| [Excel / Sheets](tools/excel-and-sheets.md) | Recipients who need to change it themselves |
| [Hand it to BI](tools/bi-handoff.md) | Organizations with a BI team and a platform already |

## The decision in one line

**Build in the surface whoever uses this on Tuesday can maintain** — not the one that demos best.

Those are sometimes the same thing. When they're not, say which is which out loud and choose on
purpose. Building the impressive version by default is how people end up owning a tool nobody else
can touch.
