#!/usr/bin/env python3
"""
make-sample-data.py — generate deliberately messy practice datasets.

Run from the repo root:
    python 0_System/scripts/make-sample-data.py

Writes CSVs into 5_Library/sample-data/. Deterministic (fixed seed), so everyone
in the room gets the same numbers and the same mess. Standard library only — no
pandas, no numpy, nothing to install.

The mess is on purpose. Every file carries a realistic subset of:
  - inconsistent date formats            - currency and percent as text
  - blanks, "N/A", "n/a", "-", "null"    - stray whitespace and casing drift
  - exact duplicate rows                 - genuine outliers
  - impossible values (negatives)        - a column that is numeric in name only

Re-run any time; files are overwritten. --clean removes them instead.
"""

import argparse
import csv
import math
import os
import random
from datetime import date, timedelta

SEED = 4610
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(REPO_ROOT, "5_Library", "sample-data")

FILES = [
    "regional_sales_monthly.csv",
    "customer_accounts.csv",
    "ab_test_results.csv",
    "survey_responses.csv",
    "staffing_model_inputs.csv",
]


# --- mess helpers ------------------------------------------------------------

def maybe_blank(rng, value, p=0.03):
    """Occasionally replace a value with one of the many ways people write 'nothing'."""
    if rng.random() < p:
        return rng.choice(["", "N/A", "n/a", "-", "null", " "])
    return value


def messy_case(rng, value, p=0.12):
    """Casing and whitespace drift, the way real exports arrive."""
    if rng.random() < p:
        return rng.choice([value.upper(), value.lower(), f" {value}", f"{value} "])
    return value


def messy_date(rng, d):
    """One column, four date formats. This is the most common real-world defect."""
    fmt = rng.choice(["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y", "%b %Y"])
    return d.strftime(fmt)


def as_money(rng, amount, p=0.35):
    """Sometimes a number, sometimes a string that looks like money."""
    if rng.random() < p:
        return f"${amount:,.2f}"
    return f"{amount:.2f}"


# --- 1. regional sales: trend + seasonality + mess ---------------------------

def regional_sales(path):
    """48 months x 4 regions. Feeds: kpi-dashboard, forecast, data-audit."""
    rng = random.Random(SEED)
    regions = {"West": 1.00, "Midwest": 0.72, "Northeast": 0.88, "South": 0.64}
    channels = ["Direct", "Partner", "Online"]
    start = date(2022, 1, 1)

    rows = []
    for i in range(48):
        d = date(start.year + (start.month - 1 + i) // 12, (start.month - 1 + i) % 12 + 1, 1)
        # Trend: ~9% annual growth. Seasonality: Q4 peak, summer trough.
        trend = 100_000 * (1.0072 ** i)
        seasonal = 1 + 0.22 * math.sin((d.month - 4) / 12 * 2 * math.pi)
        for region, weight in regions.items():
            base = trend * weight * seasonal
            noise = rng.gauss(1.0, 0.07)
            revenue = base * noise
            # Two genuine outliers: a bulk order and a systems outage.
            if i == 29 and region == "West":
                revenue *= 3.4
            if i == 38 and region == "South":
                revenue *= 0.18
            units = max(1, int(revenue / rng.uniform(380, 520)))
            rows.append({
                "month": messy_date(rng, d),
                "region": messy_case(rng, region),
                "channel": rng.choice(channels),
                "units_sold": maybe_blank(rng, units, p=0.02),
                "revenue_usd": maybe_blank(rng, as_money(rng, revenue), p=0.04),
                "returns_usd": as_money(rng, revenue * rng.uniform(0.005, 0.04), p=0.15),
                "notes": rng.choice(["", "", "", "", "bulk order", "partial month", "restated"]),
            })

    # Impossible values someone will have to catch.
    rows[61]["units_sold"] = -14
    rows[102]["revenue_usd"] = "0"
    rows[145]["revenue_usd"] = "1.2M"          # numeric column, text value
    rows[7]["month"] = "2022-13-01"            # invalid date
    # Exact duplicates — a double-paste during a month-end close.
    rows.insert(80, dict(rows[79]))
    rows.insert(81, dict(rows[79]))
    rows.insert(150, dict(rows[149]))

    write_csv(path, rows)


# --- 2. customer accounts: churn + drivers -----------------------------------

def customer_accounts(path):
    """1,200 accounts with a churn flag. Feeds: risk-scorer, data-audit."""
    rng = random.Random(SEED + 1)
    plans = ["Basic", "Standard", "Premium", "Enterprise"]
    segments = ["SMB", "Mid-Market", "Enterprise"]
    rows = []

    for i in range(1200):
        tenure = max(1, int(rng.gauss(26, 16)))
        plan = rng.choices(plans, weights=[35, 33, 22, 10])[0]
        seat_count = max(1, int(rng.lognormvariate(2.4, 0.9)))
        mrr = {"Basic": 49, "Standard": 149, "Premium": 399, "Enterprise": 1200}[plan]
        mrr = mrr * (1 + seat_count / 40) * rng.uniform(0.85, 1.2)
        logins_90d = max(0, int(rng.gauss(38, 22) * (0.4 if plan == "Basic" else 1.0)))
        tickets_90d = max(0, int(rng.expovariate(1 / 2.2)))
        nps = min(10, max(0, int(rng.gauss(7.4, 2.4))))
        days_since_login = max(0, int(rng.expovariate(1 / 18)))

        # Churn is driven by low usage, recent silence, ticket load, and low NPS.
        # Deliberately learnable, deliberately not perfectly separable.
        score = (
            -0.045 * logins_90d
            + 0.055 * days_since_login
            + 0.26 * tickets_90d
            - 0.21 * nps
            - 0.021 * tenure
            + (0.9 if plan == "Basic" else 0.0)
            - 0.25
        )
        churned = 1 if (1 / (1 + math.exp(-score))) > rng.random() else 0

        rows.append({
            "account_id": f"ACC-{10000 + i}",
            "segment": messy_case(rng, rng.choices(segments, weights=[55, 32, 13])[0]),
            "plan": messy_case(rng, plan),
            "tenure_months": tenure,
            "seats": seat_count,
            "mrr_usd": maybe_blank(rng, as_money(rng, mrr), p=0.02),
            "logins_last_90d": maybe_blank(rng, logins_90d, p=0.05),
            "support_tickets_90d": tickets_90d,
            "days_since_last_login": days_since_login,
            "nps_score": maybe_blank(rng, nps, p=0.18),   # survey non-response, not random
            "renewal_date": messy_date(rng, date(2026, 1, 1) + timedelta(days=rng.randint(0, 540))),
            "churned": churned,
        })

    # Leakage trap: a column that "predicts" churn because it is filled in AFTER churn.
    for r in rows:
        r["cancellation_reason"] = (
            rng.choice(["price", "missing feature", "switched vendor", "budget cut", ""])
            if r["churned"] == 1 else ""
        )

    rows.insert(410, dict(rows[409]))   # duplicate account row
    rows[55]["tenure_months"] = 480     # 40-year tenure on a 6-year-old product
    write_csv(path, rows)


# --- 3. A/B test results -----------------------------------------------------

def ab_test(path):
    """Checkout redesign test. Feeds: ab-test-readout."""
    rng = random.Random(SEED + 2)
    # Separate stream for order values: rejection sampling inside lognormvariate
    # consumes a variable number of draws, which would perturb the conversion stream.
    rng_val = random.Random(SEED + 22)
    rows = []
    # True effect: 4.15% -> 4.68% conversion. Realized 4.03% vs 4.69% (z about 2.1).
    # Significant at 0.05, but the 95% CI runs [+0.04pp, +1.26pp] -- the pessimistic end
    # is nearly zero. Deliberate: you cannot read this one off the p-value alone.
    arms = {"control": 0.0415, "variant": 0.0468}
    n_per_arm = 8600
    start = date(2026, 5, 4)

    for arm, rate in arms.items():
        for i in range(n_per_arm):
            day = start + timedelta(days=rng.randint(0, 13))
            converted = 1 if rng.random() < rate else 0
            order_value = round(rng_val.lognormvariate(4.3, 0.55), 2) if converted else 0.0
            rows.append({
                "visitor_id": f"V{rng.randint(100000, 999999)}-{i}",
                "assigned_arm": arm,
                "assigned_date": day.isoformat(),
                "device": rng.choices(["desktop", "mobile", "tablet"], weights=[42, 51, 7])[0],
                "new_visitor": rng.choices([1, 0], weights=[62, 38])[0],
                "converted": converted,
                "order_value_usd": order_value if converted else "",
            })

    rng.shuffle(rows)
    write_csv(path, rows)


# --- 4. survey responses -----------------------------------------------------

def survey(path):
    """Open-ended text plus a rating. Feeds: feedback-synthesizer."""
    rng = random.Random(SEED + 3)
    themes = {
        "onboarding": [
            "Setup took three weeks longer than we were told it would.",
            "Onboarding was smooth once we got assigned a real implementation contact.",
            "Nobody told us we needed IT approval before the kickoff call.",
            "The first two weeks were confusing. Documentation assumed we already knew the product.",
        ],
        "pricing": [
            "The per-seat price is hard to justify when half our seats are read-only.",
            "Renewal came in 18% higher with no explanation. That is what started the conversation.",
            "Value is fine. The problem is the annual commitment.",
            "We are paying for tiers we do not use.",
        ],
        "support": [
            "Support responds fast but escalations disappear for days.",
            "Our CSM is genuinely excellent and has saved this relationship twice.",
            "Tickets get closed before the issue is actually resolved.",
            "First-line support reads from a script. Second-line is great.",
        ],
        "reporting": [
            "Reporting is the weakest part. I export to Excel to do anything real.",
            "Cannot schedule a recurring report to my leadership team, which is the whole job.",
            "Dashboards look nice but I cannot drill into anything.",
            "I would pay more for better reporting alone.",
        ],
        "reliability": [
            "Two outages last quarter during month-end close. That is unacceptable timing.",
            "Rock solid for us. No complaints on uptime.",
            "Performance degrades badly when we pull more than a year of history.",
        ],
    }
    rows = []
    for i in range(240):
        theme = rng.choices(list(themes), weights=[22, 26, 18, 24, 10])[0]
        text = rng.choice(themes[theme])
        # Rating loosely tracks sentiment, with real noise.
        positive = any(w in text.lower() for w in ["smooth", "excellent", "rock solid", "fine", "great"])
        rating = rng.randint(7, 10) if positive else rng.randint(2, 7)
        rows.append({
            "response_id": f"R-{2000 + i}",
            "submitted": messy_date(rng, date(2026, 6, 1) + timedelta(days=rng.randint(0, 45))),
            "role": messy_case(rng, rng.choice(["Analyst", "Manager", "Director", "VP", "Individual Contributor"])),
            "tenure_bucket": rng.choice(["<6 months", "6-12 months", "1-2 years", "2+ years"]),
            "satisfaction_1_10": maybe_blank(rng, rating, p=0.04),
            "would_recommend": rng.choice(["Yes", "yes", "No", "no", "Maybe", ""]),
            "what_would_you_change": maybe_blank(rng, text, p=0.09),
        })
    write_csv(path, rows)


# --- 5. staffing model inputs ------------------------------------------------

def staffing(path):
    """Role-level cost and capacity assumptions. Feeds: scenario-calculator."""
    rng = random.Random(SEED + 4)
    roles = [
        ("Support Rep",        58_000, 14, 0.18),
        ("Senior Support Rep", 78_000, 19, 0.11),
        ("Team Lead",          96_000, 8,  0.07),
        ("Implementation Eng", 118_000, 5, 0.13),
        ("Account Manager",    89_000, 11, 0.15),
    ]
    rows = []
    for name, salary, headcount, attrition in roles:
        rows.append({
            "role": name,
            "current_headcount": headcount,
            "fully_loaded_salary_usd": as_money(rng, salary * 1.28, p=0.5),
            "annual_attrition_rate": f"{attrition:.0%}",       # percent as text, on purpose
            "tickets_per_fte_per_week": round(rng.uniform(38, 74), 1),
            "ramp_time_weeks": rng.choice([4, 6, 8, 12]),
            "cost_to_hire_usd": as_money(rng, rng.uniform(4000, 16000)),
            "overtime_multiplier": 1.5,
        })
    write_csv(path, rows)


# --- io ----------------------------------------------------------------------

def write_csv(path, rows):
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  ok  {os.path.basename(path):<32} {len(rows):>6} rows")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--clean", action="store_true", help="delete the generated CSVs instead")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    if args.clean:
        for name in FILES:
            p = os.path.join(OUT_DIR, name)
            if os.path.exists(p):
                os.remove(p)
                print(f"  removed {name}")
        return

    print(f"\nWriting sample data to 5_Library/sample-data/  (seed {SEED})\n")
    regional_sales(os.path.join(OUT_DIR, "regional_sales_monthly.csv"))
    customer_accounts(os.path.join(OUT_DIR, "customer_accounts.csv"))
    ab_test(os.path.join(OUT_DIR, "ab_test_results.csv"))
    survey(os.path.join(OUT_DIR, "survey_responses.csv"))
    staffing(os.path.join(OUT_DIR, "staffing_model_inputs.csv"))
    print("\nThe mess is intentional. Run the data-audit skill on any of these before you trust them.\n")


if __name__ == "__main__":
    main()
