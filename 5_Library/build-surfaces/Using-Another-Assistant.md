# Using Another Assistant

This workspace is built for Claude Code, but almost none of it is Claude-specific. It is plain
markdown and CSV, and the instruction file at the root (`AGENTS.md`) is an open standard read
natively by most coding agents.

You can run these sessions on Copilot, Codex, Cursor, Gemini, or ChatGPT. What changes is **how
much of the chain is automated**, not whether you can do the work.

---

## The two layers

Understanding this split tells you exactly what any given tool can and cannot do here.

**Layer 1 is the method.** The decision frame, the seven audit checks, the choice of statistical
test, the memo structure, the templates. This is thinking, written down as markdown. **Every tool
can do this, and so can a legal pad.** It is also the part that matters for your career.

**Layer 2 is the automation.** Skills loading themselves when you describe a problem, outputs
writing to known paths, each stage reading the previous stage's file, the essence folding into
`0_Org/` so you stop re-explaining your situation. This needs a tool that can read and write files
on your machine.

Losing Layer 2 costs you convenience. It does not cost you the analysis.

---

## Three tiers of tool

### Tier A — Full agentic (everything works)

Reads and writes local files, runs code, and picks up `AGENTS.md` automatically.

| Tool | Notes |
|---|---|
| **Claude Code** | What this repo was built for. Reads `CLAUDE.md`, which setup generates from `AGENTS.md` |
| **GitHub Copilot** (agent mode, VS Code) | Reads `AGENTS.md` natively. **Free for verified students** with a .edu address through GitHub Education |
| **OpenAI Codex** | Reads `AGENTS.md` natively |
| **Cursor · Windsurf · Zed · Gemini CLI · Aider** | All read `AGENTS.md` natively |

**How to run it:** open the folder, say "get me started," and follow the chain. Everything in this
repo behaves as documented.

**One difference to expect:** the skills in `.agents/skills/` are auto-discovered by Claude Code. On
other tools you may need to point at them the first time. Say: *"Read `.agents/skills/find-skills/
SKILL.md` and follow it to find the right skill for my problem."* After that it will keep working.

### Tier B — Upload and analyze (no local files)

Can run code on files you upload, but cannot read your folder or write back to it.

| Tool | Notes |
|---|---|
| **ChatGPT Plus** (Advanced Data Analysis) | Uploads CSV and Excel, writes and runs Python, returns charts and downloadable files. The free tier allows a few uploads a day but not the analysis engine |
| **Claude** (web or desktop, no Claude Code) | Upload files, analyze, get results in chat |
| **Gemini** | Similar upload-and-analyze capability |

**How to run it:**

1. Download the repo as a ZIP from the green **Code** button on
   https://github.com/data-love-co/info4610-analytics-os
2. Upload the one data file you need. For practice data that is something from
   `5_Library/sample-data/`
3. Open the relevant prompt in [Portable-Prompts.md](Portable-Prompts.md), paste it in, and work
   through it
4. Fill your template in `1_Class/<session>/` by hand as you go

**What you lose:** the agent writing to `2_Outputs/` and each stage reading the last one
automatically. You carry the context between stages by pasting your filled template into the next
prompt. That is genuinely fine, and the templates were built for exactly this.

**All ten use cases work in Tier B.**

### Tier C — Chat only (no code execution)

A free chatbot with no ability to run Python.

**Works well:**

| Use case | Why it works |
|---|---|
| Frame the decision | Pure thinking. Arguably the best use of a chat tool in the whole chain |
| Meeting to action items | Text in, structure out |
| Feedback synthesis | Text in, themes out. Fine up to a few hundred responses pasted in batches |
| Decision memo | Writing and structure |
| Knowledge assistant | Paste the documents, ask questions against them |

**Does not work reliably:**

| Use case | Why not |
|---|---|
| Forecast | Needs real computation and a backtest |
| Risk scorer | Needs a fitted model and validation |
| A/B test readout | Needs an actual test statistic and interval |
| KPI dashboard | Needs aggregation over hundreds of rows |
| Data audit | Needs to count, profile, and detect duplicates across the file |

**The reason is worth knowing**, because it is one of the lessons of the course: language models do
arithmetic in prose badly. They are fluent and confident about it, which makes the errors hard to
spot. Any tool that cannot write and execute code should not be trusted with a number you will
present. See [ai-guardrails.md](../method/ai-guardrails.md).

**If you are in Tier C:** pick a use case from the top list. You will do real work and learn the
thing the session is teaching. Do not try to compute a forecast by chat.

---

## Which tool should you actually use?

| Your situation | Use |
|---|---|
| Willing to spend about $20 for the month | **Claude Code**, Pro plan. What the repo is built for |
| Want it free and have a .edu address | **GitHub Copilot** agent mode in VS Code, free student plan. Full Tier A |
| Already pay for ChatGPT Plus | **ChatGPT** with Advanced Data Analysis. Tier B, all ten use cases |
| Locked-down work laptop, browser only | Any web assistant. Tier B or C depending on the plan |
| Not paying for anything | Free chat tool, Tier C. Choose from the "works well" list above |

**Nobody in the room is blocked.** The tiers change which use cases are practical, not whether you
participate.

---

## Getting Copilot free as a student

Worth five minutes if the subscription cost is a barrier:

1. Apply for the GitHub Student Developer Pack at https://education.github.com/pack using your
   university email address
2. Once verified, the GitHub Copilot Student plan activates on your account
3. Install VS Code (https://code.visualstudio.com) and the GitHub Copilot extension
4. Switch the Copilot sidebar to **Agent** mode, not Chat mode. Agent mode is what reads and writes
   files
5. Open this workspace folder. Copilot reads `AGENTS.md` on its own

Verification is not instant, so start it before you need it.

---

## A note on why this repo travels well

`AGENTS.md` is an open standard stewarded by the Linux Foundation, read by more than twenty coding
agents. `CLAUDE.md` is generated from it rather than maintained separately, so there is one source
of truth and no drift.

That is a deliberate design choice you can copy. If you build an agentic workspace for your own
team, putting the instructions in `AGENTS.md` means it is not a bet on one vendor. Whatever your
organization standardizes on in two years will most likely read it.
