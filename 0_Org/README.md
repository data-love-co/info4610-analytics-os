# 0_Org — Ground Truth

Facts about your organization and your work — the layer every skill reads before it runs. Short
topic files, no index, so the agent can read the whole folder before any exercise.

The `analyst-bootstrap` interview seeds these. Each stage of the chain distills its output back into
the relevant file, which is what makes the chain compound: L1.2 updates the ground truth, L2.1 reads
the updated version, and you stop re-explaining your situation every time you open a new chat.

```
0_Org/
├── 01_Overview.md       # the organization, your unit, what it's responsible for
├── 02_Decisions.md      # decisions in play, who owns each, cost of being wrong
├── 03_Metrics.md        # what you measure — and how each is DEFINED
├── 04_Data.md           # systems of record, what exists, access, sensitivity
├── 05_Stakeholders.md   # who the analysis is for, what each cares about
├── 06_Constraints.md    # policy, privacy, budget, timing, political limits
├── 07_Insights.md       # running takeaways, dated
└── Z_Library.md         # deeper detail, referenced by file name + section header
```

Read and written only through the `util_get_org_info` skill — no other skill touches the layout.

## The file that earns its keep

**`03_Metrics.md`** — and specifically the *definitions*, not the names.

"We track retention" is not a definition. Logo or revenue? Gross or net? What's in the denominator?
What's excluded — trials, internal accounts, the first 30 days? Two teams in the same company
routinely report different numbers for the same metric and neither knows why.

Writing the definitions down once, here, saves more rework than anything else in this workspace.

## Two rules

**Distilled essence only.** Full work products live in `2_Outputs/.agents/<session>/`. A one-line
decision statement lives here; the memo doesn't. Raw data lives in `5_Library/sources/`.

**This folder is tracked in git.** No customer names, employee names, account numbers, or salary
figures tied to a person. Capture the shape of a thing without the identifying detail. The agent is
instructed to flag close calls — you decide.
