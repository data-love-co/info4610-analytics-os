# OS detection & CLAUDE.md link (Step 0 detail)

## CLAUDE.md → AGENTS.md

The repo root needs a `CLAUDE.md` so Claude Code reads the workspace conventions. It's a **link to
`AGENTS.md`** — one source of truth, no drift. `0_System/bootstrap/setup.mjs` creates it per-OS
(true symlink on Mac/Linux; a generated copy on Windows, where symlinks need elevated privileges or
Developer Mode) and it's gitignored, since it's generated plumbing rather than content.

If Node isn't available, create it directly:

- **Mac/Linux:** `ln -sf AGENTS.md CLAUDE.md`
- **Windows (PowerShell, as admin):** `New-Item -ItemType SymbolicLink -Name CLAUDE.md -Target AGENTS.md`
- **Windows (no admin rights — common on a work laptop):** just copy it —
  `Copy-Item AGENTS.md CLAUDE.md`. The copy works identically; it only means you re-copy after
  editing `AGENTS.md`, which almost nobody does mid-session.

## Detect OS

- **Mac:** `uname -s` returns `Darwin`
- **Linux:** `uname -s` returns `Linux`
- **Windows:** `$env:OS` returns `Windows_NT` (PowerShell), or `ver` shows a Windows version.
  **Do not assume WSL or Git Bash** — a work-issued Windows laptop is usually plain PowerShell, or
  the Claude Code desktop app with no Unix shell at all.

State what you detected and confirm before proceeding. Every OS-specific command branches on this.

## If the machine is locked down

Managed corporate laptops sometimes block installs, PowerShell scripts, or symlink creation
entirely. None of that stops the workspace from working — it's plain markdown and CSV.

If they hit a wall:
- Copy `AGENTS.md` to `CLAUDE.md` by hand and move on.
- Skip Node entirely; nothing in the chain requires it after setup.
- Skip Python; it only powers the file converter and the sample-data generator, and the sample CSVs
  are already committed to the repo.

Say this plainly rather than troubleshooting IT policy. The point of the session is the analysis,
not the toolchain.
