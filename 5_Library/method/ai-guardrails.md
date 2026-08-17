# AI Guardrails

You're using an AI agent to do analysis you'll put your name on. This is what to check before you
do.

---

## What these tools are reliably good at

- **Structuring work.** Turning a vague ask into a framed question, organizing an analysis, choosing
  a defensible method.
- **Mechanical transformation.** Parsing four date formats, stripping currency symbols, reshaping a
  table. Fast and accurate.
- **Reading a lot of text.** Coding 400 survey responses is genuinely tedious for a person and
  genuinely well-suited to this.
- **Writing code you can inspect.** The code is checkable in a way an answer isn't.
- **First drafts.** Memos, summaries, documentation. You edit; it doesn't ship as-is.

## What they are unreliable at

- **Arithmetic in prose.** A model reasoning through a calculation in text makes errors. **Make it
  write and run code for anything numeric**, then check the code. This is the single highest-value
  habit in this document.
- **Knowing your business.** It doesn't know that the West region was reorganized in 2024, or that
  "active customer" means something specific at your company. It will produce a fluent, confident
  answer built on the wrong assumption.
- **Knowing what it doesn't know.** It will answer rather than decline, unless instructed otherwise
  and sometimes even then.
- **Consistency across a long session.** A definition established early can drift. Re-state the
  important ones.

---

## The five checks

Before any AI-produced number reaches a document with your name on it:

**1. Does the number reproduce?** Ask it to show the calculation, then check it — recompute one
value by hand, or in Excel, or ask a second time in a fresh session. If two runs disagree, neither
is trustworthy yet.

**2. Does it match the source?** Pick three numbers at random and trace them back to the raw data.
Not the cleaned file — the original. This catches transformation errors, which are the most common
and hardest to see.

**3. Is the method appropriate?** You don't need to be able to derive it, but you do need to be able
to say why it was chosen. "Welch's t-test because the group variances differ" is an answer. "It
recommended it" is not, and it will not survive a follow-up question.

**4. Are the caveats still attached?** Uncertainty gets stripped as work moves from analysis to
artifact to slide. Check that the ranges, the sample sizes, and the limitations made it through.

**5. Could you defend every line?** If someone asks "why did you exclude those rows," is there an
answer you can give? If not, go back — the answer exists in the cleaning log or it doesn't exist at
all.

---

## The specific failure to watch for

**Fluent wrongness.** The output of these tools is well-organized, confidently phrased, and
formatted like something that was checked. That presentation is not evidence of correctness, and it
disarms the skepticism you'd apply to a colleague's rough draft.

The practical countermeasure: **read AI output as if a smart intern produced it under time
pressure.** Plausible structure, right general shape, and possibly a wrong number in the middle that
nothing about the presentation will flag for you.

---

## Grounding

These tools work far better when they're working from your files than from their own knowledge.
That's the entire design of this workspace:

- `0_Org/` holds your metric definitions, so the agent uses yours instead of the generic ones
- `5_Library/sources/processed/` holds your actual data
- The audit and cleaning log record what was changed and why
- Each skill writes its output to a known place, so the next one reads facts rather than
  remembering them

**When an answer seems off, the first question is what it was reading.** Most bad output traces to
missing context, not to bad reasoning.

---

## Confidentiality — the one with real consequences

Everyone here has a job and an obligation to an employer.

- **`5_Library/sources/raw/` is gitignored.** Nothing there gets committed.
- **`5_Library/sources/processed/` is tracked.** Ingestion is what moves data across that line.
- **Personal identifiers** — names, emails, employee or customer IDs, salary or health detail — do
  not belong in a tracked file. Aggregate, mask, or drop them.
- **When you're unsure whether data can be here, it can't.** Use `5_Library/sample-data/` and
  re-point the method at real data inside your own systems later. You lose nothing pedagogically.
- **Check your employer's policy on AI tools** before putting work data into any of them, including
  this one. That policy exists, most people haven't read it, and "I didn't know" is not a defense
  anyone enjoys giving.

---

## Attribution

If AI helped produce an analysis you're presenting, whether to say so depends on your organization's
norms — some expect disclosure, some treat it like using Excel.

What isn't optional: **you are accountable for the output.** "The AI produced it" is not a defense
for a wrong number in a board deck, and it will not be received as one. The checks above are how you
earn the right to put your name on it.
