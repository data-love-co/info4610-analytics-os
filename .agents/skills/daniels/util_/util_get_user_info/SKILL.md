---
name: util_get_user_info
description: >
  The single read/write path for who runs this workspace — personal and professional context about
  the user, never organizational data. Triggers when the user says "update my profile", "change my
  working preferences", "what do you know about me", "update my background", "I prefer short
  answers", "I don't write code", "add to my goals", or any correction to their name, role,
  function, tooling, or working style. Also invoked by analyst-bootstrap (to seed 0_User/ from the
  onboarding interview) and by chain skills that need to know how technical the user is before
  choosing an approach. All reads and writes go through this skill; no other skill touches 0_User/
  directly.
---

# util_get_user_info — Personal Profile

You are the sole gatekeeper for `0_User/`. Every skill that needs to know who the user is, how
technical they are, or how they like to work reads through you. Bootstrap seeds the files; the
user can update any topic at any time.

## Why the technical-comfort field matters more than the rest

This workspace serves people whose day jobs are finance, operations, marketing, and general
management — not data science. The same use case gets built very differently for someone who
lives in Excel than for someone who writes SQL every day. Skills read `02_Expertise` to decide
whether to reach for a spreadsheet, a no-code surface, or Python — and whether to explain the
method or just apply it. Get this field right and everything downstream gets easier.

## The folder contract

`0_User/` holds personal and professional context about the individual. Organizational facts never
go here; those belong in `0_Org/` via `util_get_org_info`.

```
0_User/
├── 01_Overview.md      # name, role, function, the organization they work in
├── 02_Expertise.md     # background, domain depth, analytics and technical comfort, tools they use
├── 03_Preferences.md   # working style: tone, depth, pace, how they want recommendations framed
├── 04_Goals.md         # what they want out of these sessions and out of the work itself
└── Z_Library.md        # fuller background, referenced by file name + section header
```

The folder starts empty. Bootstrap seeds it via `set()` during the onboarding interview.

## Interface

### get()

Read and return the whole folder in one pass — `01_Overview.md`, `02_Expertise.md`,
`03_Preferences.md`, `04_Goals.md`, `Z_Library.md`. Skip missing files silently.

### get(file)

Read and return the named topic file (e.g. `get(03_Preferences)`). If it doesn't exist yet, return
empty and note it hasn't been created.

### set(file, content)

1. If the file doesn't exist, create it with `content` as the full body.
2. If it exists, read it first. Locate the section matching `content`'s top-level `##` or `###`
   header and replace it in place, leaving other sections intact. If no matching header exists,
   append as a new section.
3. If the content runs long (more than ~40 lines) or is deeper background than a concise topic file
   should carry, route the detail into `Z_Library.md` under a `##` header, and write a short
   summary in the topic file with a note: `→ see Z_Library.md § <section>`.
4. After writing, read the file back and confirm the result looks correct before returning.

## Step-by-step: reading the profile

1. Read each topic file that exists in `0_User/`.
2. Return the contents cleanly, grouped by file heading. Do not editorialize.
3. If a topic file is missing or empty, note the gap so the caller can decide whether to ask.

## Step-by-step: updating the profile

1. Identify which topic file the content belongs to.
2. If the content spans topics, split it — write each piece to the correct file.
3. Call `set(file, content)`.
4. Read the file back. Confirm to the user in one short sentence.
5. Never overwrite sections the user hasn't asked to change.

## Topic guide

| File | What goes here |
|---|---|
| `01_Overview.md` | Name, current role and title, function (finance / ops / marketing / HR / product / general management), organization, one-sentence identity |
| `02_Expertise.md` | Professional background, domain depth, **analytics comfort** (never / spreadsheets / statistics coursework / SQL / writes code), **tools they actually use** (Excel, Sheets, Tableau, Power BI, SQL, Python, R, none) |
| `03_Preferences.md` | Tone (direct or explained), depth, pacing, whether they want the recommendation first or the options first, how much method detail they want shown |
| `04_Goals.md` | What they want out of these two sessions; what they want to be able to do at work afterward |
| `Z_Library.md` | Career history, extended background, anything too long for a topic file |

## Guardrails

- Personal context only — never write organizational facts, metric definitions, or data-system
  details into `0_User/`. Those belong in `0_Org/` via `util_get_org_info`.
- Record analytics comfort as the user states it, without flattery or inflation. "I have not done
  statistics since undergrad" is useful information and should be written down plainly.
- Never overwrite sections the user hasn't asked to change.
- Keep each topic file short and skimmable. Push length into `Z_Library.md`.
- Always read the file back after writing and confirm before returning.
- Never send the user's data to external services — all reads and writes are local.
