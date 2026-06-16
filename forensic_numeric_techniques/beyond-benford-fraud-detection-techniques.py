#!/usr/bin/env python3
"""Runnable script companion for the forensic numeric techniques notebook.

The notebook remains the narrated teaching surface. This script executes the same
code cells in order so the DD Tech Lab companion folder has a runnable Python
artifact and a paired notebook. Synthetic examples only.
"""


# Cell 3
import math
from collections import Counter

# Inline expense amounts. Note the heavy clustering on leading digit 5.
amounts = [512, 5230, 58, 540, 5102, 5900, 53, 5001, 587, 5400, 512, 59, 7321, 980, 134, 521]

def benford_first_digit(values):
    expected = {d: math.log10(1 + 1.0 / d) for d in range(1, 10)}
    digits = [int(str(abs(v)).lstrip("0")[0]) for v in values if abs(v) >= 1]
    n = len(digits)
    counts = Counter(digits)
    worst_digit, worst_gap = None, 0.0
    for d in range(1, 10):
        obs = counts.get(d, 0) / n
        exp = expected[d]
        gap = obs - exp
        print("digit %d: observed %5.1f%%  expected %5.1f%%  gap %+5.1f%%" % (d, obs * 100, exp * 100, gap * 100))
        if gap > worst_gap:
            worst_gap, worst_digit = gap, d
    return worst_digit, worst_gap

wd, wg = benford_first_digit(amounts)
if wg > 0.10:
    print("-> REVIEW: leading digit %d is %.1f%% over the Benford expectation, pull those records" % (wd, wg * 100))
else:
    print("-> looks clean")

# Cell 5
from collections import Counter

# Many charges begin "49" (sitting just under a 5000 approval limit) and end in "00".
amounts = [4900, 4950, 4900, 4988, 4925, 4900, 1340, 4975, 2200, 4900, 8731, 4950, 4900, 612, 4900, 5310]

def two_digit_tests(values):
    firsts = Counter(int(str(abs(v))[:2]) for v in values if abs(v) >= 10)
    lasts = Counter(abs(v) % 100 for v in values if abs(v) >= 10)
    n = sum(firsts.values())
    top_first, top_first_n = firsts.most_common(1)[0]
    top_last, top_last_n = lasts.most_common(1)[0]
    print("most common first-two digits: %02d appears %d of %d (%.0f%%)" % (top_first, top_first_n, n, 100 * top_first_n / n))
    print("most common last-two digits:  %02d appears %d of %d (%.0f%%)" % (top_last, top_last_n, n, 100 * top_last_n / n))
    return top_first, top_first_n / n, top_last, top_last_n / n

tf, tf_share, tl, tl_share = two_digit_tests(amounts)
if tf_share > 0.20 or tl_share > 0.20:
    print("-> REVIEW: clustering on first-two %02d and last-two %02d suggests limit-skirting or rounding" % (tf, tl))
else:
    print("-> looks clean")

# Cell 7
# A ledger stuffed with suspiciously tidy totals.
amounts = [5000, 1000, 250.75, 2000, 500, 10000, 3000, 487.12, 1500, 2500, 7000, 642.38, 4000, 500, 6000, 1000]

def round_number_bias(values, base=500):
    n = len(values)
    round_hits = [v for v in values if float(v) % base == 0]
    share = len(round_hits) / n
    print("total amounts: %d" % n)
    print("amounts that are exact multiples of %d: %d (%.0f%%)" % (base, len(round_hits), share * 100))
    print("sample round values: %s" % sorted(set(round_hits))[:5])
    return share

share = round_number_bias(amounts)
# A clean transactional ledger rarely exceeds roughly 20 percent perfectly round amounts.
if share > 0.30:
    print("-> REVIEW: %.0f%% of entries are perfectly round, far above a normal ledger" % (share * 100))
else:
    print("-> looks clean")

# Cell 9
# Vendor groups: one has a single payment that towers over the rest.
groups = {
    "Vendor A": [820, 790, 805, 12500, 815],
    "Vendor B": [4200, 4350, 4100, 4400, 4250],
    "Vendor C": [60, 75, 68, 72, 70],
}

def relative_size_factor(group_map, threshold=5.0):
    flagged = []
    for name, vals in group_map.items():
        s = sorted((abs(v) for v in vals), reverse=True)
        largest, second = s[0], s[1]
        rsf = largest / second if second else float("inf")
        print("%s: largest %.0f, second %.0f, RSF %.1f" % (name, largest, second, rsf))
        if rsf > threshold:
            flagged.append((name, rsf))
    return flagged

flags = relative_size_factor(groups)
if flags:
    for name, rsf in flags:
        print("-> REVIEW: %s has an RSF of %.1f, top payment dwarfs its peers" % (name, rsf))
else:
    print("-> looks clean")

# Cell 11
from collections import Counter

# Reported headcounts that were clearly rounded to 0 and 5.
values = [200, 145, 130, 250, 175, 90, 305, 60, 415, 120, 185, 240, 95, 350, 110, 205]

def terminal_digit_heaping(nums):
    last = [abs(v) % 10 for v in nums]
    n = len(last)
    counts = Counter(last)
    expected = n / 10.0
    # Excess concentration on the favored 0 and 5 endings.
    favored = counts.get(0, 0) + counts.get(5, 0)
    favored_share = favored / n
    for d in range(10):
        print("ends in %d: %d (expected %.1f)" % (d, counts.get(d, 0), expected))
    print("share ending in 0 or 5: %.0f%% (random would be about 20%%)" % (favored_share * 100))
    return favored_share

share = terminal_digit_heaping(values)
if share > 0.40:
    print("-> REVIEW: %.0f%% of values end in 0 or 5, strong terminal-digit heaping" % (share * 100))
else:
    print("-> looks clean")

# Cell 14
from collections import defaultdict
from datetime import date

# Each tuple: (vendor, amount, invoice_no, pay_date)
payments = [
    ("Acme Supply", 4200.00, "INV-1001", date(2025, 3, 1)),
    ("Acme Supply", 4200.00, "INV-1002", date(2025, 3, 3)),   # near-duplicate pay
    ("Globex Parts", 3000.00, "INV-2001", date(2025, 3, 5)),
    ("Globex Parts", 3000.00, "INV-2002", date(2025, 3, 5)),   # same-day split
    ("Globex Parts", 3500.00, "INV-2003", date(2025, 3, 5)),   # together > 9000
    ("Initech LLC", 1200.00, "INV-3001", date(2025, 3, 6)),
]

def scan_payments(rows, dup_window_days=3, split_threshold=9000.0):
    flags = []
    by_vendor_amt = defaultdict(list)
    by_vendor_day = defaultdict(list)
    for v, amt, inv, d in rows:
        by_vendor_amt[(v, amt)].append((inv, d))
        by_vendor_day[(v, d)].append((inv, amt))
    for (v, amt), items in by_vendor_amt.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if abs((items[i][1] - items[j][1]).days) <= dup_window_days:
                    flags.append("duplicate pay " + v + " " + format(amt, ".2f") + " " + items[i][0] + "/" + items[j][0])
    for (v, d), items in by_vendor_day.items():
        if len(items) > 1 and sum(a for _, a in items) > split_threshold:
            flags.append("possible split " + v + " on " + str(d) + " total " + format(sum(a for _, a in items), ".2f"))
    return flags

found = scan_payments(payments)
if found:
    print("Payment scan -> REVIEW: " + "; ".join(found))
else:
    print("Payment scan -> looks clean")

# Cell 16
# Amounts submitted for approval; control limit is 10000 (second signoff above it)
amounts = [10000.0 * x for x in [0.12, 0.30, 0.55, 0.98, 0.99, 0.985, 0.97, 0.40, 0.99, 0.96]]

def threshold_bunching(values, limit=10000.0, band=0.05, alert_share=0.40):
    low = limit * (1.0 - band)
    just_under = [v for v in values if low <= v < limit]
    share = len(just_under) / len(values) if values else 0.0
    return share, len(just_under), len(values)

share, n_band, n_total = threshold_bunching(amounts)
print("Just-under-limit share = " + format(share, ".0%") + " (" + str(n_band) + " of " + str(n_total) + ")")
if share >= 0.40:
    print("Threshold check -> REVIEW: amounts bunched just under the 10,000 approval limit")
else:
    print("Threshold check -> looks clean")

# Cell 18
from datetime import date

# (invoice_no, invoice_date) expected to rise together over time
docs = [
    (1001, date(2025, 1, 2)),
    (1002, date(2025, 1, 3)),
    (1003, date(2025, 1, 5)),
    (1003, date(2025, 1, 6)),   # cloned number
    (1006, date(2025, 1, 7)),   # gap: 1004, 1005 missing
    (1004, date(2025, 1, 8)),   # out of order (backdated look)
]

def sequence_integrity(rows):
    flags = []
    ordered = sorted(rows, key=lambda r: r[1])
    seen = set()
    prev = None
    for num, d in ordered:
        if num in seen:
            flags.append("duplicate number " + str(num) + " on " + str(d))
        seen.add(num)
        if prev is not None and num < prev:
            flags.append("out-of-order number " + str(num) + " after " + str(prev))
        prev = max(prev, num) if prev is not None else num
    nums = sorted(n for n, _ in rows)
    full = set(range(nums[0], nums[-1] + 1))
    missing = sorted(full - set(nums))
    if missing:
        flags.append("missing numbers " + ",".join(str(m) for m in missing))
    return flags

found = sequence_integrity(docs)
if found:
    print("Sequence check -> REVIEW: " + "; ".join(found))
else:
    print("Sequence check -> looks clean")

# Cell 20
# Each dict is a journal entry
entries = [
    {"id": "JE-1", "txn_type": "payroll", "account": "expense", "created_by": "amy", "approved_by": "ben"},
    {"id": "JE-2", "txn_type": "sale",    "account": "revenue", "created_by": "cara", "approved_by": "dan"},
    {"id": "JE-3", "txn_type": "payroll", "account": "revenue", "created_by": "amy", "approved_by": "ben"},  # impossible cell
    {"id": "JE-4", "txn_type": "refund",  "account": "expense", "created_by": "eve", "approved_by": "eve"},  # self-approval
]

# Allowed account per transaction type
allowed = {"payroll": {"expense"}, "sale": {"revenue"}, "refund": {"expense", "revenue"}, "purchase": {"expense"}}

def impossible_cells(rows):
    flags = []
    for r in rows:
        ok = allowed.get(r["txn_type"], set())
        if r["account"] not in ok:
            flags.append(r["id"] + " " + r["txn_type"] + " posted to " + r["account"])
        if r["created_by"] == r["approved_by"]:
            flags.append(r["id"] + " self-approved by " + r["created_by"])
    return flags

found = impossible_cells(entries)
if found:
    print("Logic check -> REVIEW: " + "; ".join(found))
else:
    print("Logic check -> looks clean")

# Cell 23
import math
from collections import Counter

def zipf_slope(transactions):
    counts = sorted(Counter(transactions).values(), reverse=True)
    xs = [math.log(i + 1) for i in range(len(counts))]
    ys = [math.log(c) for c in counts]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else 0.0

# Inline ledger: volume spread far too evenly across vendors (tripwire).
ledger = (["V1"] * 12 + ["V2"] * 11 + ["V3"] * 11 + ["V4"] * 10 +
          ["V5"] * 10 + ["V6"] * 10 + ["V7"] * 9 + ["V8"] * 9)
slope = zipf_slope(ledger)
print("fitted log-log slope:", round(slope, 3))
if slope > -0.4:
    print("-> REVIEW: distribution is unnaturally flat (slope near 0), unlike a natural ledger")
else:
    print("-> looks clean")

# Cell 25
def novelty_by_quarter(stream):
    seen = set()
    n = len(stream)
    bounds = [n * (q + 1) // 4 for q in range(4)]
    rates = []
    start = 0
    for b in bounds:
        chunk = stream[start:b]
        new = sum(1 for name in chunk if name not in seen)
        for name in chunk:
            seen.add(name)
        rates.append(new / len(chunk) if chunk else 0.0)
        start = b
    return rates

# Ordered stream: after the early ramp the roster settles, then a late
# burst of brand-new vendors appears in the final quarter (tripwire).
stream = (["A", "B", "C", "A", "B", "C", "A", "B"] * 3 +
          ["A", "B", "C", "A", "B", "C", "A", "B"] * 3 +
          ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"])
rates = novelty_by_quarter(stream)
print("new-name rate by quarter:", [round(r, 2) for r in rates])
# Compare the final quarter against the settled middle quarters (Q2, Q3),
# not Q1, since Q1 is inflated by the unavoidable startup ramp.
settled = (rates[1] + rates[2]) / 2
if rates[-1] > 0.25 and rates[-1] > settled + 0.25:
    print("-> REVIEW: late burst of brand-new counterparties after novelty had settled")
else:
    print("-> looks clean")

# Cell 27
def circular_counterparties(payments_out, payments_in):
    paid_to = {p["to"] for p in payments_out}
    paid_by = {p["from"] for p in payments_in}
    return paid_to & paid_by

# Outflows and inflows; "Helio Trading" sits on both sides (tripwire).
payments_out = [{"to": "Acme Supply"}, {"to": "Helio Trading"}, {"to": "Birch Freight"}]
payments_in = [{"from": "North Retail"}, {"from": "Helio Trading"}, {"from": "East Mart"}]
overlap = circular_counterparties(payments_out, payments_in)
print("counterparties paid AND received from:", sorted(overlap))
if overlap:
    print("-> REVIEW: circular cash flow with", ", ".join(sorted(overlap)))
else:
    print("-> looks clean")

# Cell 29
def shared_bank_accounts(vendors, employees):
    emp_by_acct = {}
    for e in employees:
        emp_by_acct.setdefault(e["bank_account"], []).append(e["name"])
    hits = []
    for v in vendors:
        for emp_name in emp_by_acct.get(v["bank_account"], []):
            hits.append((v["name"], emp_name, v["bank_account"]))
    return hits

# Vendor "Crestline LLC" shares a bank account with employee "Dana Pyle" (tripwire).
vendors = [{"name": "Crestline LLC", "bank_account": "00471920"},
           {"name": "Orchard Parts", "bank_account": "88820017"}]
employees = [{"name": "Dana Pyle", "bank_account": "00471920"},
             {"name": "Sam Ortiz", "bank_account": "55510023"}]
hits = shared_bank_accounts(vendors, employees)
for vend, emp, acct in hits:
    print("shared account", acct, "->", "vendor", vend, "and employee", emp)
if hits:
    print("-> REVIEW: vendor and employee share a bank account")
else:
    print("-> looks clean")

# Cell 32
import datetime

# Inline daily revenue for a single quarter (Jan 1 to Mar 31).
# A big block is dumped into the last 3 days to hit the number.
entries = []
start = datetime.date(2025, 1, 1)
for i in range(90):
    d = start + datetime.timedelta(days=i)
    amt = 1000.0
    if i >= 87:           # last 3 days of the quarter
        amt = 40000.0
    entries.append((d, amt))

total = sum(a for _, a in entries)
last_days = 3
cutoff = entries[-1][0] - datetime.timedelta(days=last_days - 1)
tail = sum(a for d, a in entries if d >= cutoff)
tail_share = tail / total
even_share = last_days / len(entries)   # what an even spread would give

print("Total revenue: {:.0f}".format(total))
print("Last {} days share: {:.1%} (even baseline {:.1%})".format(last_days, tail_share, even_share))
if tail_share > 3 * even_share:
    print("-> REVIEW: revenue heavily concentrated at period end, check cutoff and shipping dates")
else:
    print("-> looks clean")

# Cell 34
import datetime

# (timestamp, amount) journal entries. Two land on a Saturday and late at night.
entries = [
    (datetime.datetime(2025, 3, 12, 10, 30), 1200.0),
    (datetime.datetime(2025, 3, 13, 14, 5), 800.0),
    (datetime.datetime(2025, 3, 15, 2, 15), 95000.0),   # Saturday, 2am
    (datetime.datetime(2025, 3, 14, 23, 50), 60000.0),  # Friday, near midnight
    (datetime.datetime(2025, 3, 17, 9, 45), 500.0),
]

def off_hours(ts):
    weekend = ts.weekday() >= 5          # 5=Sat, 6=Sun
    after_hours = ts.hour < 7 or ts.hour >= 19
    return weekend or after_hours

flagged = [(ts, amt) for ts, amt in entries if off_hours(ts)]
exposure = sum(amt for _, amt in flagged)
print("Entries: {}, off-hours entries: {}".format(len(entries), len(flagged)))
for ts, amt in flagged:
    print("  {} ({}) amount {:.0f}".format(ts, ts.strftime("%A"), amt))
if flagged:
    print("-> REVIEW: {:.0f} posted outside business hours or on a weekend".format(exposure))
else:
    print("-> looks clean")

# Cell 36
# Altman Z-score using the published coefficients.
# Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
# Realistic figures for a struggling firm (all in thousands).
working_capital = -200.0
total_assets = 1000.0
retained_earnings = -150.0
ebit = 40.0
market_value_equity = 120.0
total_liabilities = 900.0
sales = 600.0

X1 = working_capital / total_assets
X2 = retained_earnings / total_assets
X3 = ebit / total_assets
X4 = market_value_equity / total_liabilities
X5 = sales / total_assets

Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
print("Altman Z-score: {:.2f}".format(Z))
if Z < 1.81:
    print("-> REVIEW: distress zone (Z < 1.81), high financial-distress risk")
elif Z > 2.99:
    print("-> looks clean (safe zone, Z > 2.99)")
else:
    print("-> REVIEW: grey zone (1.81 to 2.99), inconclusive")

# Cell 38
import statistics

# Each row: (id, amount, postings_that_day, hour_of_day). Row 3 is jointly extreme.
rows = [
    ("E1", 1200.0, 12, 10),
    ("E2", 1500.0, 14, 11),
    ("E3", 98000.0, 1, 2),     # huge, lonely, middle of the night
    ("E4", 1100.0, 13, 14),
    ("E5", 1300.0, 15, 9),
]

def zscores(vals):
    mu = statistics.mean(vals)
    sd = statistics.pstdev(vals)
    if sd == 0:
        return [0.0 for _ in vals]
    return [(v - mu) / sd for v in vals]

amts = zscores([r[1] for r in rows])
freq = zscores([r[2] for r in rows])
hour = zscores([r[3] for r in rows])

combined = []
for i, r in enumerate(rows):
    score = abs(amts[i]) + abs(freq[i]) + abs(hour[i])
    combined.append((r[0], score))

worst = max(combined, key=lambda x: x[1])
for name, score in combined:
    print("{}: combined deviation {:.2f}".format(name, score))
if worst[1] > 3.0:
    print("-> REVIEW: {} is a joint outlier on size, frequency, and timing".format(worst[0]))
else:
    print("-> looks clean")

# Cell 40
from collections import Counter

# (memo_text, amount)
entries = [
    ("Reclass to hit target", 50000.0),
    ("Standard monthly accrual", 1200.0),
    ("Standard monthly accrual", 1200.0),
    ("Standard monthly accrual", 1200.0),
    ("", 75000.0),                       # large entry, blank memo
    ("Customer invoice 4471", 900.0),
]

risk_words = ["reclass", "plug", "adjust", "manual", "reverse", "to hit"]
large_threshold = 20000.0
template_threshold = 3

risk_hits = []
for memo, amt in entries:
    low = memo.lower()
    if any(w in low for w in risk_words):
        risk_hits.append((memo, amt))

memo_counts = Counter(m for m, _ in entries if m.strip())
templated = [(m, c) for m, c in memo_counts.items() if c >= template_threshold]
blank_large = [(m, amt) for m, amt in entries if not m.strip() and amt >= large_threshold]

print("Risk-keyword hits: {}".format(risk_hits))
print("Templated memos (>= {} uses): {}".format(template_threshold, templated))
print("Blank memo on large entry: {}".format(blank_large))
if risk_hits or templated or blank_large:
    print("-> REVIEW: memo patterns suggest thin documentation on material entries")
else:
    print("-> looks clean")
