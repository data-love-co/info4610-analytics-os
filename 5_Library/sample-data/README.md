# sample-data — Practice Datasets

Deliberately messy, deliberately fictional. Use these when your real work data can't leave your
employer's systems, when you want to try a use case before committing your own data to it, or when
you want to see whether the agent catches a defect you already know is there.

Nothing here describes a real company. Regenerate any time:

```bash
python 0_System/scripts/make-sample-data.py
```

Fixed seed, so everyone gets the same numbers and the same mess. `--clean` removes them.

## What's here

| File | Rows | Built for |
|---|---|---|
| `regional_sales_monthly.csv` | ~195 | `kpi-dashboard`, `forecast`, `data-audit` |
| `customer_accounts.csv` | ~1,200 | `risk-scorer`, `data-audit` |
| `ab_test_results.csv` | 17,200 | `ab-test-readout` |
| `survey_responses.csv` | 240 | `feedback-synthesizer` |
| `staffing_model_inputs.csv` | 5 | `scenario-calculator` |
| `meeting-notes-q3-planning.md` | — | `meeting-to-actions` |
| `policy-handbook-excerpt.md` | — | `knowledge-assistant` |

## The defects, on purpose

Every CSV carries a realistic subset of these. Run `data-audit` before you trust any of them —
that's the exercise.

- **Four date formats in one column** (`2022-01-01`, `01/01/2022`, `01-Jan-2022`, `Jan 2022`),
  plus one date that doesn't exist
- **Six ways of writing "nothing"** — empty, `N/A`, `n/a`, `-`, `null`, a single space
- **Currency and percent as text** — `$1,234.00`, `18%` — in columns you'd expect to be numeric
- **Casing and whitespace drift** — `West`, `WEST`, `west`, `West ` are four values to a computer
- **Exact duplicate rows** — the double-paste that happens during every month-end close
- **Genuine outliers** — one bulk order, one outage month. These are real events, not errors;
  deleting them is a decision you have to defend
- **Impossible values** — negative units sold, a 40-year tenure on a 6-year-old product
- **`1.2M`** sitting in a numeric revenue column

## Two traps worth knowing about

**`customer_accounts.csv` has a leakage column.** `cancellation_reason` is only filled in for
accounts that already churned — it's recorded *after* the outcome. Any model that includes it will
look spectacular in testing and be useless in production, because you'd never have that field for
an account that hasn't churned yet. Target leakage is the single most common way a churn model
fails in the real world. The dataset is built so you can walk into it.

**`nps_score` is missing 18% of the time, and not at random.** Survey non-response correlates with
disengagement, which correlates with churn. Filling those blanks with the column average quietly
erases signal. Deciding what to do about it — impute, flag, or exclude — is the actual analytical
judgment, and it belongs in your cleaning log.

## What's in the data, if you want to check your work

Facilitator notes. Skip this section if you'd rather find it yourself.

- **Sales:** roughly 9% annual growth with a Q4 peak and a summer trough. Four regions at different
  scale. Two single-month anomalies with explanations in the `notes` column.
- **Accounts:** about 23% churn (271 of 1,201). It's driven by low logins, days since last login,
  support ticket volume, low NPS, short tenure, and the Basic plan. Real but noisy — a good model
  lands somewhere around 0.75–0.82 AUC, not 0.99. If you get 0.99, you left `cancellation_reason` in.
- **A/B test:** control converts at 4.03% (347 of 8,600), variant at 4.69% (403 of 8,600). A 0.65
  percentage point lift, 16.1% relative, z = 2.09, p = 0.037. **The 95% confidence interval on the
  difference is [+0.04pp, +1.26pp]** — significant at the 0.05 level, but the pessimistic end is
  almost nothing. This one is built so it cannot be read off the p-value. Whether to ship depends
  entirely on what the change costs, which is the conversation the exercise is for.
- **Survey:** five themes at different volumes — pricing and reporting dominate, reliability is
  small but sharp. Sentiment loosely tracks the rating, with enough noise that rating alone won't
  reproduce the themes.
