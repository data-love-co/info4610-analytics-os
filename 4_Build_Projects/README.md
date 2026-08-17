# 4_Build_Projects — Things You Build

Dashboards, calculators, scripts, apps — anything with its own files that someone runs or opens.

Empty until you build something. One folder per project, named `YYYY.MM Short Name`
(e.g. `2026.09 Regional Staffing Model`).

## What goes in a build folder

Whatever the thing needs, plus these three, which are what make it survivable:

**A README.** What it does, what decision it serves, who uses it, how to run it, and who owns it.
Three paragraphs. The version of this you write while you still remember is worth ten times the one
you write in March.

**The inputs, or a pointer to them.** If it reads a file, say which file and where it comes from. If
the data can't live in this repo, say where it does live and how to get an extract.

**The caveats.** Whatever the audit found, whatever the model can't do, whatever assumption it rests
on. These get separated from the analysis the moment the tool leaves your hands, and then somebody
uses it without them.

## Confidentiality

This folder is tracked in git. If your build reads real work data, keep the data out — point at it,
don't commit it. Add a pattern to `.gitignore` if you need to (`*.private.csv` and `**/private/` are
already there).

## Handing one over

If someone else will maintain it, the README needs one more section: **what would break it.** A
column rename upstream, a system migration, a definition change, a hardcoded date. The person who
built it always knows; the person who inherits it never does.
