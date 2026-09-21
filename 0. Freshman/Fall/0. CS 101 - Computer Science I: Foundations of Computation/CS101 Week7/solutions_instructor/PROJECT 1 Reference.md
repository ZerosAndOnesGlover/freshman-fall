# CS 101 · Project 1 · Reference Numbers (INSTRUCTOR ONLY)

> Computed by a reference solution run on `ROWS` (the 121 records in `project1_starter.py`, identical to
> `resources/weather_data.csv`). Use these to check a student's printed report. Keeping the **first** of
> the duplicated 2024-01-16 rows (stable merge sort, then compare neighbours) is what gives these figures;
> a student who keeps the second may differ in the second decimal place — accept if the choice is stated.

## Data quality

121 rows read · **110 kept** · 11 rejected:

| Line | Reason |
|---|---|
| `2024-01-11,41.8,33.3,0.07,` | missing value |
| `2024-01-23,36.2,27.7,,73` | missing value |
| `2024-02-03,N/A,35.1,0.2,68` | not a number |
| `2024-02-15,54.4,39.7,0.12,` | missing value |
| `2024-02-20,60.0,42.7,0.1,130` | implausible (humidity) |
| `2024-03-01,54.7,40.9,,55` | missing value |
| `2024-03-11,63.0,73.0,0.0,51` | implausible (low > high) |
| `2024-03-19,58.3,49.3,0.11,` | missing value |
| `2024-04-01,65.0,error,0.04,83` | not a number |
| `2024-04-10,69.1,58.9,0.0` | wrong number of fields |
| `2024-01-16` (second copy) | duplicate date |

## Statistics (population standard deviation)

| | mean | median | min | max | sd |
|---|---|---|---|---|---|
| high | 56.19 | 54.95 | 28.5 | 80.1 | 13.41 |
| low | 43.17 | 42.05 | 18.0 | 70.6 | 13.78 |

Highest high **2024-04-21, 80.1**. Lowest low **2024-01-05, 18.0**.
Monthly average high: Jan **41.13** (29 days) · Feb **49.30** (26) · Mar **62.31** (28) · Apr **72.64** (27).
(Sample standard deviation, dividing by n − 1, is also acceptable if labelled.)

## Search, sort, streak

Five hottest: 04-21 80.1 · 04-22 79.5 · 04-27 79.3 · 04-24 79.2 · 04-29 78.0.
Days with 60 ≤ high ≤ 65: **10** (two binary searches, no scan).
Longest run with high > 70: **5 days, 2024-04-20 to 2024-04-24**.

## Reference code

```python
# ROWS as in project1_starter.py
from collections import deque

def parse_row(line):
    """(date, high, low, precip, humidity) or a reason string."""
    fields = line.split(",")
    if len(fields) != 5:
        return "wrong number of fields"
    if "" in fields:
        return "missing value"
    try:
        high = float(fields[1]); low = float(fields[2]); precip = float(fields[3]); hum = float(fields[4])
    except ValueError:
        return "not a number"
    if not (0 <= hum <= 100) or low > high or precip < 0:
        return "implausible"
    return (fields[0], high, low, precip, hum)

def merge_sort(items, key):
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left = merge_sort(items[:mid], key); right = merge_sort(items[mid:], key)
    out = []; i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

records = []; rejected = []
for line in ROWS[1:]:
    r = parse_row(line)
    if isinstance(r, str):
        rejected.append((r, line))
    else:
        records.append(r)
by_date = merge_sort(records, lambda r: r[0])
unique = []
for r in by_date:
    if unique and unique[-1][0] == r[0]:
        rejected.append(("duplicate date", r[0])); continue
    unique.append(r)
print("rows", len(ROWS) - 1, "valid", len(unique), "rejected", len(rejected))
for why, line in rejected: print("  ", why, line)

def stats(values):
    n = len(values); s = merge_sort(values, lambda v: v)
    mean = sum(values) / n
    med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    sd = (sum((v - mean) ** 2 for v in values) / n) ** 0.5
    return mean, med, s[0], s[-1], sd
for idx, name in [(1, "high"), (2, "low")]:
    m, med, lo, hi, sd = stats([r[idx] for r in unique])
    print(f"{name}: mean {m:.2f} median {med:.2f} min {lo} max {hi} sd {sd:.2f}")
hottest = merge_sort(unique, lambda r: r[1])[::-1][:5]
print("hottest", [(r[0], r[1]) for r in hottest])
coldest = merge_sort(unique, lambda r: r[2])[0]; print("coldest low", coldest[0], coldest[2])
months = [[0, 0] for _ in range(13)]
for r in unique:
    m = int(r[0][5:7]); months[m][0] += r[1]; months[m][1] += 1
for m in range(1, 5): print("month", m, f"{months[m][0] / months[m][1]:.2f}", months[m][1])
# range query 60..65 inclusive on high via binary search
sh = merge_sort(unique, lambda r: r[1])
def first_at_least(lst, x):
    lo, hi = 0, len(lst)
    while lo < hi:
        mid = (lo + hi) // 2
        if lst[mid][1] < x: lo = mid + 1
        else: hi = mid
    return lo
a = first_at_least(sh, 60.0); b = first_at_least(sh, 65.0000001)
print("days with 60<=high<=65:", b - a)
# streak above 70 using a stack of the current run
best = []; run = []
for r in unique:
    if r[1] > 70:
        run.append(r)
    else:
        if len(run) > len(best): best = run
        run = []
if len(run) > len(best): best = run
print("longest >70 streak", len(best), best[0][0] if best else None, best[-1][0] if best else None)
```
