# templates/ — No-AI Fallbacks

Every exercise has a fillable markdown template here, for working a stage by hand without running
the skill. The working copy already lives in the matching `1_Class/<session>/` folder — you fill
that one. These masters stay unchanged so you can start over.

## Files

| Stage | Session | Template | Skill output |
|---|---|---|---|
| Decision frame | `L1.2-Decision-Frame` | `L1.2-Decision-Frame-Template.md` | `2_Outputs/.agents/L1.2-Decision-Frame/Decision-Frame.md` |
| Data audit | `L1.3-Data-Audit` | `L1.3-Data-Audit-Template.md` | `2_Outputs/.agents/L1.3-Data-Audit/Data-Audit.md` · `Cleaning-Log.md` |
| Build spec | `L2.1-Build` | `L2.1-Build-Spec-Template.md` | `2_Outputs/.agents/Use-Case/<Name>.md` |
| Decision memo | `L2.2-Decision-Memo` | `L2.2-Decision-Memo-Template.md` | `2_Outputs/.agents/L2.2-Decision-Memo/Decision-Memo.md` |
| Demo notes | `L2.3-Demo` | `L2.3-Demo-Notes-Template.md` | `2_Outputs/.agents/L2.3-Demo/Demo-Notes.md` |

## Notes

- **Two copies, same content.** The master here is the source of truth; the copy in
  `1_Class/<session>/` is your working surface. Fill the copy.
- **Field names match the skill's closing block.** The templates are derived from each skill's
  `reference/output-format.md` — you transcribe from the skill's output into the matching field.
  Renaming a field breaks that copy step, so don't paraphrase the labels.
- **The template and the skill's output file are two different artifacts** with two different jobs.
  The template is yours: it holds your judgment calls and your reasoning. The output file is the
  chain's machine-readable reference, and the next skill reads it. Don't collapse them.
- **You can work any stage entirely by hand.** The next skill picks up your completed template
  exactly as if you'd run the previous one conversationally. That's a legitimate way to do this —
  and for the decision frame in particular, doing it on paper first is often better.
