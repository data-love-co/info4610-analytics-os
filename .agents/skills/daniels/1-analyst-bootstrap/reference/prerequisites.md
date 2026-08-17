# Prerequisites — install commands by OS (Step 2 detail)

Confirm each. If one is missing, give the install command for their OS — then continue either way.
**None of these blocks the session.**

| Prerequisite | Check | Mac | Windows | Linux | Needed for |
|---|---|---|---|---|---|
| **git** | `git --version` | `brew install git` | `winget install Git.Git` | `apt install git` | Cloning and versioning this repo |
| **Node.js 18+** | `node --version` | `brew install node` | `winget install OpenJS.NodeJS.LTS` | nodejs.org (LTS) | `setup.mjs` only |
| **Python 3** | `python --version` | `brew install python` | `winget install Python.Python.3.12` | `apt install python3` | File converter, sample-data generator |

**After any `winget install`:** open a **new** terminal so `PATH` refreshes before re-checking.

**On Windows,** `python` and `python3` may both work, or only one may. Try both before concluding
it isn't installed. If the Microsoft Store stub opens instead of Python, that means it isn't really
installed.

## What breaks without each one

Be specific rather than insisting on a clean environment:

- **No git** — the workspace still works; they just can't version or share it. Fine for two sessions.
- **No Node** — create `CLAUDE.md` by hand (see `os-setup.md`). Nothing else needs Node.
- **No Python** — the sample CSVs are already committed, so practice data still works. What they
  lose is `parse-sources.py` (converting PDFs and Office docs) and regenerating sample data. If
  they need a PDF converted and have no Python, the agent can often read the file directly — try
  that before sending anyone to IT.

If a work laptop blocks all three, say so plainly and proceed. The chain is markdown; the analysis
is the point.
