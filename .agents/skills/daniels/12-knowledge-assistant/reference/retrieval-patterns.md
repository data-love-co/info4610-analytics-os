# Corpus Preparation, Retrieval, and Output

Load at Phase 2 and Closing.

---

## Preparing the corpus

### Chunk on meaning, not character count

The default advice — split every 1,000 characters with a 200-character overlap — is fine for prose
and bad for policy documents. A policy split mid-clause retrieves as two half-answers and cites as
neither.

**Split on the document's own structure:** section, subsection, or heading. In the practice
handbook that means one chunk per numbered subsection (4.1, 4.2, …). Each chunk is a complete
thought with an addressable name.

If a section is very long, split it at the next heading level down and repeat the parent heading in
both halves, so each chunk stands alone.

### Keep the metadata on every chunk

```yaml
document: Employee Handbook
version: "4.2"
effective: 2026-01-01
section: "7.4"
section_title: Equipment and Home Office
supersedes: "4.1 (stipend was $500)"
```

The citation is only useful if it's checkable. "Handbook 4.2, §7.4" lets someone open the document
and verify. "The handbook says" does not.

### Audit the corpus before building on it

Four checks. Run all of them and report the findings — they're often more valuable than the
assistant.

| Check | What you're looking for |
|---|---|
| **Contradictions** | The same fact stated two ways. The practice handbook has one ($750 vs. $500 stipend) planted deliberately, with the resolution noted. Real corpora have several, unnoted |
| **Staleness** | Effective dates, "under review" language, references to systems or roles that no longer exist |
| **Coverage gaps** | What the documents don't cover. The practice excerpt is Sections 4 and 7 only — anything about expenses or benefits is simply absent |
| **Ambiguity** | Rules stated so vaguely they can't be applied. "Approval criteria are under review" is honest and unhelpful; the assistant must pass that through, not smooth it over |

**Report every conflict to the user and ask which version governs.** Do not pick one silently. This
audit frequently turns up things nobody knew were inconsistent, and fixing the document is a better
outcome than working around it.

---

## Retrieval

### The simplest thing that works

For a small corpus — anything under roughly fifty pages — **just put the documents in the context.**
A Claude Project with the files attached and the answering rules as project instructions
outperforms a hand-rolled retrieval pipeline on accuracy, takes fifteen minutes, and has no
infrastructure to maintain.

Reach for retrieval when the corpus genuinely exceeds what fits, or when it changes often enough
that re-uploading is a burden.

### When you do need retrieval

**Keyword search (BM25 or similar)** — surprisingly strong for policy documents, because people ask
using the document's own vocabulary ("PTO carryover", "parental leave"). No embeddings, no
dependencies, easy to debug when it retrieves the wrong thing.

**Embedding search** — better for questions phrased differently from the document ("can I take time
off for my dad's surgery" → the sick-leave section, which never says "dad"). Needs an embedding
model and a vector store.

**Hybrid — run both, merge, take the top few by combined rank.** This is the practical default when
retrieval is warranted. Keyword catches exact policy terms; embeddings catch paraphrase.

**Always retrieve more chunks than you think you need** — five to eight rather than two. Policy
answers frequently span sections (parental leave in 4.5 interacts with FMLA; remote work in 7.1
interacts with 7.2), and a narrow retrieval produces a confidently incomplete answer.

### Debugging bad answers

When the assistant answers wrong, diagnose in this order:

1. **Was the right chunk retrieved?** Print what came back. Most bad answers are retrieval failures,
   not generation failures.
2. **If not** — chunking or query problem. Try hybrid retrieval, or re-chunk on better boundaries.
3. **If yes but the answer is still wrong** — the answering rules aren't strict enough. Usually the
   model is filling a gap from general knowledge, which means rule 1 needs to be more forceful and
   the "not covered" path needs to be more explicit.

---

## The answering rules, as a prompt

Whatever the surface, these instructions define the behavior. Adapt the specifics; keep the shape.

```
You answer questions about <organization>'s <document set> using ONLY the
provided documents.

Rules:
1. Answer only from the documents. Never from general knowledge or from what
   is typical at other organizations.
2. Cite the document, version, and section for every claim, inline.
3. Quote exactly for amounts, deadlines, and eligibility rules. Do not
   paraphrase these.
4. If the documents do not answer the question, say exactly:
   "That isn't covered in <document set>. For this, contact <fallback>."
   Do not approximate from a related section.
5. If the documents contradict each other, show both and identify which
   version is current. Do not resolve it yourself.
6. If a policy is marked under review, pending, or dated, say so in the answer.
7. Never advise an individual on their situation. State what the policy says
   and stop.
8. For anything involving medical leave, accommodation, harassment,
   termination, or a compensation dispute, do not answer. Respond:
   "This needs a person. Please contact <HR contact>."

Corpus: <document list with versions and effective dates>
Coverage: <what is included>
NOT covered: <what is absent — be specific>
Fallback contact: <name or alias>
```

Rule 4's exact wording matters. A vague "I'm not sure" invites the model to try anyway; a scripted
sentence with a named fallback does not.

---

## Output — what to write

### The deliverable → `2_Outputs/.agents/Use-Case/Knowledge-Assistant.md`

```markdown
---
type: knowledge-assistant
session: L2.1
corpus_docs: <n>
date: <today>
---

# <Name> — Knowledge Assistant

## Purpose and audience

<What it answers, for whom, and what it deliberately does not do.>

## Corpus manifest

| Document | Version | Effective | Sections | Chunks |
|---|---|---|---|---|

**Coverage:** <what's included>
**Not covered:** <what's absent — specific, because this drives the "not covered" answers>

## Corpus audit

### Contradictions found
| Item | Version A | Version B | Governs | Resolved by |
|---|---|---|---|---|

### Stale or pending
| Section | Issue |
|---|---|

### Gaps
<Questions people will ask that these documents cannot answer.>

## Answering rules

<The full prompt above, as deployed.>

## Test results

| # | Question | Category | Response | Correct? |
|---|---|---|---|---|
| 1 | How much PTO do I accrue after 4 years? | direct | 20 days (§4.1) | yes |
| 5 | How do I submit an expense report? | not covered | declined + routed | yes |
| 7 | I need accommodation for a medical issue | sensitive | routed to HR | yes |

**Not-covered tests:** <n> run, <n> correctly declined. This is the number that matters.

## Build

**Surface:** <Claude Project / retrieval pipeline / FAQ page>
**Retrieval:** <none — full context / keyword / hybrid>
**Access:** <who can use it>

## Maintenance — the part with no technical answer

**Owner:** <who updates this>
**Review:** <when — at minimum, whenever a source document changes version>
**Risk if stale:** an assistant confidently serving last year's policy is worse than no assistant.
```

### What to show in chat

The corpus inventory, every contradiction found, the coverage gaps, and ten sample exchanges —
**including the refusals.** Show the refusals prominently. They are the proof that it works.
