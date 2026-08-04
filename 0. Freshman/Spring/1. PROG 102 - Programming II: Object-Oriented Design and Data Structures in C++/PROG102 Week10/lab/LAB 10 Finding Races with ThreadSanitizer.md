# PROG 102 · Lab 10
## Finding Races with ThreadSanitizer

**Week 10 · 2-hour lab session · 40 points**
**Deliverable:** `tracker.cpp` (repaired), `RESULTS.md`. In-lab checkoff.

> **Midterm 2 is this week.** This lab is short. **Finish it in the session.**

---

## Before You Start — Make TSan Run

```
g++ -std=c++17 -O1 -g -pthread -fsanitize=thread prog.cpp -o prog
./prog
```

If it dies at startup with

```
FATAL: ThreadSanitizer: unexpected memory mapping
```

that is an ASLR problem on some Linux kernels, **not your code**:

```
setarch $(uname -m) -R ./prog
```

**Lab 0 asked you to confirm this in Week 0.** If you did not, do it in the first five minutes and tell
your TA if it still fails.

---

## Purpose

You are given `tracker.cpp`. **It compiles clean under `-Wall -Wextra -pedantic`, it runs, it
terminates, and its output looks plausible.**

It contains **five concurrency faults**, and the reason this lab exists is that you cannot find them by
reading the output — the number that is most obviously wrong is not the one you would check, and the
number you *would* check looks fine.

---

## The Code

```cpp
struct Stats {
    long   hits  = 0;
    double total = 0.0;
    std::map<std::string,int> by_page;
    std::mutex m;                          // declared. Never used.
    bool  ready = false;

    void record(const std::string& page, double ms){
        ++hits;
        total += ms;
        by_page[page]++;
    }
    double mean() const { return hits ? total/hits : 0.0; }
};
```

Four writer threads call `record` 20,000 times each; a reporter thread samples `mean()` while they do.

---

## Part A — Observe (12 pts)

**A1.** *(3)* Build and run it **three times** at `-O2`. Report all three outputs.

**Expected hits is 80,000.** Report what you got.

**A2.** *(4)* One reported number looks approximately **right** and another is catastrophically wrong.

**Identify both, and explain why the plausible one is plausible.** This is the most important question
in Part A.

**A3.** *(5)* Now run it under ThreadSanitizer. Report:

- the number of distinct race reports;
- the **line numbers** implicated;
- one full report, including both stack traces.

**Compare with your answer to A2.** Did TSan implicate anything you had not suspected?

---

## Part B — Diagnose (10 pts)

**B1.** *(6)* Identify all **five** faults. For each: the line, one sentence on what is wrong, and
**what a user would observe** — which may be nothing.

*(One of them is not a data race in the strict sense. Finding it is worth the extra look.)*

**B2.** *(4)* The struct declares a `std::mutex m` that is never used.

- **(a)** *(2)* Does its presence make anything safe?
- **(b)** *(2)* What does its presence suggest about how this code was written?

---

## Part C — Repair (14 pts)

**C1.** *(8)* Fix all five. **Your repaired version must:**

- produce `hits = 80000` on every run;
- run **TSan-clean**;
- still terminate.

**Use the cheapest correct mechanism for each fault** — do not put one big mutex around everything and
call it done. Some of these want an atomic; at least one wants a mutex.

**In `RESULTS.md`, justify your choice for each.**

**C2.** *(6)* Measure the cost. Report the runtime of the original and of your repair, three runs each.

Then answer: **your version is slower. Is that acceptable?** Three sentences, referring to your numbers
and to what the original actually computed.

---

## Part D — What the Tool Cannot Do (4 pts)

**D1.** *(2)* Time your repaired program **with and without** `-fsanitize=thread`. Report the slowdown
factor.

**D2.** *(2)* Your repaired program runs TSan-clean.

**Does that prove it has no races?** Answer in two sentences. **"Yes" earns nothing.**

---

## Submission

- `tracker.cpp` — repaired, warning-free, TSan-clean.
- `RESULTS.md` — all transcripts, the five faults, the justifications, and Parts C2 and D.
- Machine, OS, compiler version, **and the exact TSan command that worked** at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 12 | Observing, and noticing which number lied |
| B | 10 | Five faults, including the one that is not a race |
| C | 14 | Cheapest correct fix per fault, and its cost |
| D | 4 | The limits of the tool |
| **Total** | **40** | |

---

## Reference Results

g++ 13.3.0, x86-64 Linux.

**A1 — three runs at `-O2`:**

```
hits=26079 total=25889 mean=0.9927 pages=2 (expected hits=80000)
hits=31942 total=30743 mean=0.9625 pages=2 (expected hits=80000)
hits=25279 total=23570 mean=0.9324 pages=2 (expected hits=80000)
```

**A3 — under TSan:** **10** race reports, implicating lines **17, 18, 19** and **30**.

---

## What This Lab Is Really Showing

**Part A2 is the point of the session.**

Look at the reference output. `mean` is 0.93–0.99, and the true mean is exactly 1.0 — **every recorded
value is 1.0 ms, so the mean looks essentially correct.** Meanwhile `hits` is 26,079 out of 80,000:
**two-thirds of the data is gone.**

If this were a real analytics dashboard, the graph everyone looks at would be the average response
time, and it would look **fine**. The traffic count would be wrong by a factor of three, and somebody
would eventually notice and blame the load balancer.

> **The corrupted statistic looked healthy because it is a ratio of two equally-corrupted numbers.**
> Both `hits` and `total` lost roughly the same proportion of updates, so their quotient survived.

That is what makes concurrency bugs different from every other kind you have met in this course. A
memory error crashes. A wrong algorithm gives visibly wrong answers. **A race quietly produces a
plausible number**, and the only reason you know is that a tool told you.

**Which is why Part D2's answer is "no".** TSan sees the interleavings that actually happened on the
runs you did. A clean run is evidence, not proof — and it is still the best evidence available, which
is why the answer is to run it always rather than to distrust it.

---

*PROG 102 · Week 10 · Lab 10 · © CSE Department*
