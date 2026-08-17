---
title: "Claude Code"
level: "Intermediate"
best_for: "Anything re-runnable, anything touching files, anything you want versioned"
---

# Claude Code

Anthropic's agent in your terminal, desktop app, or VS Code extension. It reads your whole folder,
writes and runs code, and edits files. This workspace is built around it.

**What it's for here:** the use case that has to refresh with new data, the analysis that touches
files on disk, the thing you want under version control. Also the fastest way to explore a dataset
if you're comfortable in a terminal.

**Cost:** a Claude subscription (Pro or higher), or API credits.

**Quickstart**

1. Install: `npm install -g @anthropic-ai/claude-code` — or use the desktop app, which needs no
   terminal setup at all
2. Open this repo's folder in it. It reads `CLAUDE.md` automatically
3. Say "get me started"
4. Review what it changes before accepting. In a git repo, `git diff` shows you everything

**If you've never used a terminal:** budget twenty minutes of discomfort. It's genuinely learnable in
one session, and it's the surface that pays off longest. The desktop app is a gentler entry point —
same agent, no command line.

**Watch out for:** it runs commands. Read what it proposes on anything that deletes, moves, or
overwrites. It asks first; don't approve on autopilot.
