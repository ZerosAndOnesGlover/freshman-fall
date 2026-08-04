# PROG 102 · Lab 10 — Solutions and Checkoff Notes
## Finding Races with ThreadSanitizer

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Midterm 2 is this week.** Keep this lab inside the session. Budget A 25 min, B 25 min, C 45 min,
D 10 min, 15 min slack.

**First five minutes: get TSan running for everyone.** Ask the room to build and run anything with
`-fsanitize=thread` before starting. The failure to watch for:

```
FATAL: ThreadSanitizer: unexpected memory mapping
```

**Fix: `setarch $(uname -m) -R ./prog`.** This was Lab 0 Part A's job in Week 0; expect that a third of
the room did not do it.

**Distribute `tracker.cpp` unmodified.** Build it in front of the room and run it twice, so everyone
sees that it compiles clean, terminates, and produces *different* wrong answers.

**The trap to name explicitly at the start:** *this program's output looks plausible.* Students who
skim will report "the mean looks fine" and move on, which is precisely what Part A2 is testing.

---

## The Five Faults

| # | Line | Fault | Observable |
| --- | --- | --- | --- |
| 1 | `++hits` | unsynchronised counter | hits ≈ 26,000 of 80,000 |
| 2 | `total += ms` | unsynchronised accumulator | wrong, but *proportionally* wrong |
| 3 | `by_page[page]++` | unsynchronised `std::map` — **structural corruption**, not just a lost update | may crash; may silently corrupt the tree |
| 4 | `ready` | non-atomic flag used as a signal | at `-O2` the compiler may hoist it; the reader can spin forever |
| 5 | `mean()` | reads `total` and `hits` non-atomically as a **pair** | can return a mean computed from mismatched values |

**Fault 5 is the "not strictly a data race" one** the sheet hints at — well, it *is* a race on each
member, but the deeper fault is that **the two reads are not a transaction**, which no amount of making
each member atomic would fix. **That is L33 §1.2's point** and a student who identifies it has
understood the week.

**Fault 3 is the dangerous one.** A lost `int` increment is a wrong number; a concurrent `std::map`
insertion can corrupt the red-black tree, and the failure appears later, elsewhere.

---

## Part A — Observe (12)

### A1 (3)

```
hits=26079 total=25889 mean=0.9927 pages=2 (expected hits=80000)
hits=31942 total=30743 mean=0.9625 pages=2 (expected hits=80000)
hits=25279 total=23570 mean=0.9324 pages=2 (expected hits=80000)
```

*Marking: 3 for three runs with varying results.*

### A2 (4) — the assessed question

**`mean` looks approximately right (0.93–0.99; the true value is 1.0). `hits` is catastrophically
wrong (~26,000 of 80,000).**

**Why the plausible one is plausible:** `mean` is `total / hits`, and **both lost roughly the same
proportion of updates**. The errors cancel in the quotient. A ratio of two equally-corrupted numbers
looks healthy.

*Marking: 2 identifying both, 2 the explanation. **The explanation is the marks** — "the mean is
averaged so it's more stable" is 1; the answer is that the numerator and denominator are corrupted
together.*

### A3 (5)

**10** race reports; lines **17, 18, 19** and **30**.

*Marking: 3 the counts and lines, 2 the full report with both stacks. **Accept any count above ~4** —
TSan reports what it observed and the number varies.*

---

## Part B — Diagnose (10)

### B1 (6)

All five, as tabulated above.

*Marking: 1 per fault, plus 1 for the "observable" column being thought about. **Fault 5 is the one
students miss**; fault 3's severity is the one they under-rate.*

### B2 (4)

**(a)** **No.** A declared-and-unused mutex makes nothing safe. It costs 40 bytes and provides the
appearance of thread-safety.

**(b)** It suggests somebody **knew** synchronisation was needed, added the mutex, and never used it —
or removed the locking during debugging and did not restore it. **The presence of an unused mutex is
evidence of an incomplete fix**, and is a good thing to look for in review.

*Marking: 2 + 2. **(b) can be answered several ways**; mark whether they engaged with what it implies
about the code's history.*

---

## Part C — Repair (14)

### C1 (8)

The **cheapest correct** fix per fault:

| Fault | Fix |
| --- | --- |
| 1, 2 | Could be `std::atomic` **individually** — but see fault 5 |
| 3 | **Mutex.** A `std::map` needs one; there is no atomic map |
| 4 | `std::atomic<bool>` |
| 5 | **Mutex** — `hits` and `total` must be read as a pair |

**The correct overall answer is a mutex around `record()` and around `mean()`, plus an atomic
`ready`.** Making `hits` and `total` atomic is *not* sufficient, because fault 5 requires them to be
consistent with each other.

*Marking: 5 all five fixed and TSan-clean, 3 the justifications. **A student who made everything atomic
has not fixed fault 5** — check whether `mean()` can still see a mismatched pair. **A student who put
one mutex around everything and justified it as "the map needs one anyway" is correct** and should get
full marks; the sheet's "cheapest" wording invites the analysis, not a particular answer.*

### C2 (6)

Their repair will be several times slower. **That is acceptable** because the original was not
computing the answer — it was computing a plausible-looking number that was wrong by a factor of three.

*Marking: 3 the measurements, 3 the argument. **The argument must reference what the original actually
computed.** "Correctness is worth it" without engaging with the numbers is 1.*

---

## Part D — What the Tool Cannot Do (4)

### D1 (2)

Typically **5–15×**.

### D2 (2)

**No.** TSan sees the interleavings that actually occurred on the runs performed. It cannot report a
race in code that did not execute, or on a schedule that did not happen.

*Marking: 2. **"Yes" earns nothing**, as stated. Accept any answer that identifies the limitation;
the strongest also note that it is still the best evidence available.*

---

## Checkoff Checklist

1. TSan running — **the working command recorded.**
2. A1 shows three **different** results.
3. A2 explains why `mean` looks healthy.
4. B1 finds **fault 5**, not just the three obvious counters.
5. C1 is TSan-clean **and** the guarantee about `mean()` reading a consistent pair is preserved.
6. D2 says no.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 12 |
| B | 10 |
| C | 14 |
| D | 4 |
| **Total** | **40** |

---

## Note for the Lab

Close on Part A2, and put the numbers back on the board.

> **`mean` was 0.99 and the true value is 1.0. `hits` was 26,079 and the true value is 80,000.**
>
> If this were a real dashboard, the graph everyone watches — average response time — would look
> **perfect**, and the traffic count would be wrong by a factor of three. **The corrupted statistic
> looked healthy because it is a ratio of two equally-corrupted numbers.**

Then the general point, which is the reason this week exists:

> Every other kind of bug in this course announced itself. A memory error crashed. A wrong algorithm
> gave visibly wrong answers. A leak was caught by a sanitizer. **A race quietly produces a plausible
> number**, and today the only reason you knew was that a tool told you.

And close on the honest limit, from D2:

> Your repaired version runs TSan-clean. **That is not proof.** TSan sees the schedules that happened.
> It is still the strongest evidence you have, which is why the answer is to run it every time rather
> than to distrust it.

If time allows, one line worth saying because it inverts nine weeks of habit:

> **Everywhere else in this course, running the program was the strongest evidence available. This
> week it is the weakest.**

---

*PROG 102 · Week 10 · Lab 10 Solutions · © CSE Department*
