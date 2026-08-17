# 0_User — Your Profile

Who runs this workspace — personal and professional context the agent reads at the start of every
session so it adapts to you. Personal only; organizational facts live in `0_Org/`.

Numbered topic files, read and written only through the `util_get_user_info` skill. The
`analyst-bootstrap` interview seeds them; you can update any topic any time by saying so.

```
0_User/
├── 01_Overview.md      # name, role, function, organization
├── 02_Expertise.md     # background, analytics comfort, tools you actually use
├── 03_Preferences.md   # working style: tone, depth, pace, how you want recommendations framed
├── 04_Goals.md         # what you want from these sessions and from the work
└── Z_Library.md        # fuller background
```

The folder starts empty. Say **"get me started"** and the bootstrap fills it in.

## The field that matters most

**`02_Expertise` — your analytics comfort.** Answer it accurately.

This workspace serves people whose day jobs are finance, operations, marketing, and general
management, not data science. Every skill reads this field to decide whether to build in a
spreadsheet, a no-code surface, or Python — and whether to explain a method or just apply it.

"I haven't done statistics since undergrad and I live in Excel" is useful, specific, and extremely
common in this room. Inflating it makes everything downstream harder for you, and nobody sees this
file but you.

## Changing it

Just say so: *"I'd rather you gave me the recommendation first and the options after,"* or *"stop
explaining the statistics, I've got it."* The agent updates `03_Preferences` and everything after
that adapts.
