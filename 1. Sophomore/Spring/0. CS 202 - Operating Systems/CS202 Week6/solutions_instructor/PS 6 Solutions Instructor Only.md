# CS 202 · Problem Set 6 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 6.** Q1, Q2, Q3 and Q5 have exact answers — the reference produces them, and a correct implementation reproduces them. **Q4 is the student's own trace and cannot be checked against a table**; mark its arithmetic and its reasoning, and require the trace file in the tarball.

**Reference:** `solutions_instructor/pagesim reference (do not distribute).c`, which is the skeleton with `lru`, `clock_policy` and `aging_common` filled in. The skeleton compiles with no compiler output; so does the reference.

All figures from the reference machine: i5-8250U, Ubuntu 24.04.4, kernel 7.0.0-31, valgrind 3.22.0.

---

## Q1: LRU and Clock (25 points)

### Reference implementations

```c
static unsigned long lru(int nframes)
{
    unsigned long faults = 0;
    int used = 0;
    size_t *last = calloc((size_t)nframes, sizeof *last);
    for (size_t t = 0; t < nrefs; t++) {
        int f = hfind(refs[t]);
        if (f >= 0) { last[f] = t; continue; }
        faults++;
        if (used < nframes) f = used++;
        else {
            f = 0;
            for (int i = 1; i < nframes; i++) if (last[i] < last[f]) f = i;
            hdel(frame_page[f]);
        }
        frame_page[f] = refs[t];
        last[f] = t;
        hput(refs[t], f);
    }
    free(last);
    return faults;
}

static unsigned long clock_policy(int nframes)
{
    unsigned long faults = 0;
    int used = 0, hand = 0;
    unsigned char *ref = calloc((size_t)nframes, 1);
    for (size_t t = 0; t < nrefs; t++) {
        int f = hfind(refs[t]);
        if (f >= 0) { ref[f] = 1; continue; }
        faults++;
        if (used < nframes) f = used++;
        else {
            while (ref[hand]) { ref[hand] = 0; hand = (hand + 1) % nframes; }
            f = hand;
            hand = (hand + 1) % nframes;
            hdel(frame_page[f]);
        }
        frame_page[f] = refs[t];
        ref[f] = 1;
        hput(refs[t], f);
    }
    free(ref);
    return faults;
}
```

### (a) [15]

Exact match with both tables: **15**. **Two common deviations, and what they look like:**

| Bug | Symptom |
|---|---|
| hand left **on** the evicted frame instead of after it | Clock 3 frames: 15 instead of 14 |
| reference bit **not set** when a page is loaded | Clock 4 frames: 10 instead of 9 |
| LRU updating `last` only on faults | LRU = FIFO exactly |

**[7] per correct table**, +1 for both.

### (b) [5]

**FIFO 15, LRU 17 — LRU is worse.** The frame contents, two frames, first twelve references:

| *t* | ref | FIFO | | LRU | |
|---:|---:|---|---|---|---|
| 0 | 7 | FAULT | [7] | FAULT | [7] |
| 1 | 0 | FAULT | [7, 0] | FAULT | [7, 0] |
| 2 | 1 | FAULT | [1, 0] | FAULT | [1, 0] |
| 3 | 2 | FAULT | [1, 2] | FAULT | [1, 2] |
| 4 | 0 | FAULT | [0, 2] | FAULT | [0, 2] |
| 5 | 3 | FAULT | [0, 3] | FAULT | [0, 3] |
| 6 | 0 | hit | [0, 3] | hit | [0, 3] |
| **7** | **4** | **FAULT** | **[4, 3]** | **FAULT** | **[0, 4]** |
| 8 | 2 | FAULT | [4, 2] | FAULT | [2, 4] |
| 9 | 3 | FAULT | [3, 2] | FAULT | [2, 3] |
| 10 | 0 | FAULT | [3, 0] | FAULT | [0, 3] |
| 11 | 3 | hit | [3, 0] | hit | [0, 3] |

**They first differ at *t* = 7** (the eighth reference, page 4): **FIFO evicts 0** — in memory longest — **while LRU evicts 3** and keeps 0, which was used one reference earlier. **[3]**

**Is LRU doing anything wrong? No [2].** Keeping the more recently used page is the right bet; **this string punishes it** — page 0 is not referenced again until *t* = 10, while 3 returns at *t* = 9. **With two frames almost nothing fits, and the outcome is close to luck.** Accept any answer that says LRU's rule is sound and this string is adversarial; **do not accept** "LRU is worse than FIFO in general".

### (c) [5]

**Clock takes 9 faults with four frames and 9 with five.** With five frames the faults fall at *t* = 0, 1, 2, 3, 5, 7, 17, 18, 19 — **the fifth frame removes the two mid-string faults (13, 14) and adds two at the end (18, 19).**

**Why [5]:** the extra frame delays the first eviction, so **when the hand finally sweeps, every reference bit is set** — the sweep clears all of them and evicts where it started, **exactly FIFO's choice** (L20 §5). The pages it then throws away are 0 and 1, which the string's last three references ask for again. **Clock is not a stack algorithm**, so more frames can rearrange which pages survive. **Accept** "all bits set → degenerates to FIFO" with the fault positions as evidence.

---

## Q2: Belady's Anomaly (15 points)

### (a) [5]

```
12 references, 5 distinct pages
  frames     fifo      lru    clock    aging   aging2      opt
       3        9       10        9        9        9        7
       4       10        8       10        7        7        6
```

### (b) [5]

**FIFO and Clock fault more with four frames than with three [2].**

**FIFO, at the seventh reference (page 5) [3]:** with three frames the contents are [4, 1, 2] after *t* = 5, and 5 replaces 4 — leaving 1 and 2, which are the next two references, both hits. **With four frames** the contents are [1, 2, 3, 4] and 5 replaces **1**, so the next reference (1) faults, then 2 faults, and the cascade continues. **The extra frame kept pages 3 and 4 alive long enough to be the oldest at the wrong moment.**

### (c) [5]

**Claim:** after any prefix, LRU with *n* frames holds exactly the **n most recently referenced distinct pages** (or all of them, if fewer have been referenced).

**Proof [3]:** by induction on the references. It holds vacuously at the start. A reference to a page already held makes it the most recent, and the rest keep their order: still the *n* most recent. A reference to a page not held is a fault; if a frame is free the set grows by the new page — still the *n* most recent; otherwise LRU evicts the least recently used, which is the *n*-th most recent, and inserts the new page as the most recent: **again the *n* most recent.**

**Conclusion [1]:** the set for *n* frames is a **subset** of the set for *n* + 1, so any reference that hits with *n* frames hits with *n* + 1. **Faults cannot increase with more frames.**

**OPT [1]:** the argument does **not** carry over — OPT's set is not "the *n* most recent" anything. **A separate argument is needed**, and the standard one shows OPT's sets are also nested (it evicts the page with the furthest next use, which is the same page whatever *n* is, so the *n*-frame set is contained in the *n* + 1-frame set). **Accept** "needs its own proof, and it is also a stack algorithm".

---

## Q3: Locality (20 points)

### (a) [8]

```
100000 references, 1000 distinct pages
```

| Frames | FIFO | LRU | Clock | OPT |
|---:|---:|---:|---:|---:|
| 10 | 83,864 | 83,700 | 83,819 | 55,564 |
| 25 | 61,728 | 60,405 | 61,072 | 29,836 |
| 40 | 43,209 | 38,515 | 40,379 | 15,857 |
| 50 | 34,197 | 25,908 | 28,654 | 10,352 |
| 60 | 27,747 | 16,518 | 19,906 | 8,933 |
| 80 | 20,327 | 10,155 | 11,571 | 7,909 |
| 100 | 16,696 | 9,558 | 9,969 | 7,236 |
| 200 | 10,801 | 8,538 | 8,561 | 5,271 |

**[1 per row.]** Students' numbers are identical — the generator is seeded.

### (b) [6]

- **10 and 25 frames [2]:** the working set is 50 pages, so **no policy can hold it**. Every policy evicts pages that are about to be used; the choice of victim is nearly irrelevant, and all three real policies land within 0.2% of each other.
- **50–60 frames [2]:** the working set now fits, **and the policies differ in whether they keep it**. LRU does; FIFO evicts by age and throws working-set pages out in turn.
- **After 100 frames [2]:** what is left is the **10% of references to random pages**, which nothing can predict. The curve flattens at that floor.

**At 60 frames: FIFO/LRU = 27,747/16,518 = 1.68 — FIFO faults 68% more.** **Clock/LRU = 19,906/16,518 = 1.21 — Clock is 21% above LRU.**

### (c) [6]

**OPT still faults 5,271 times [2]** because **10% of every phase's references go to a uniformly random page of the 1,000**, and with 200 frames most of those pages are not resident. **No policy can do better: those references are unpredictable by construction.**

**Estimate [3]:** 100,000 references × 10% = **10,000 random references**; a random page is resident with probability of roughly frames/total = 200/1,000 = 0.2, so about **8,000 of them fault** — the same order as the measured 5,271, which is lower because OPT keeps the pages that are about to be used and because some random references hit the working set anyway.

**What it says [1]:** **a replacement policy can only exploit structure that exists.** Past the working set, the fault rate is a property of the workload, not of the policy — which is why L20 §7's real programs, whose references are almost all predictable, do so much better than this synthetic one.

---

## Q4: A Real Program (25 points)

**There is no expected table; mark the method.** The reference trace, for comparison:

**`sort -n` of 2,000 numbers**: `2,121,880 accesses, 1,031,795 page references after removing repeats`, **387 distinct data pages**.

| Frames | FIFO | LRU | Clock | OPT |
|---:|---:|---:|---:|---:|
| 8 | 237,042 | 142,675 | 224,263 | 80,568 |
| 16 | 10,282 | 7,934 | 8,554 | 4,073 |
| 32 | 2,747 | 1,393 | 1,520 | 890 |
| 64 | 741 | 544 | 558 | 430 |
| 128 | 473 | 464 | 463 | 387 |
| 387 | 387 | 387 | 387 | 387 |

**(a) [8]** — **4** for a trace with its accesses/references/distinct-pages line, **4** for a table with at least five frame counts and all four policies. **Deduct 2** if the program is so large that the trace is unreadable (the log exceeds a few GiB); tell them to trace something smaller.

**(b) [7]** For the reference trace, **1% of 1,031,795 references is 10,318 faults**, reached at **16 frames** — 64 KiB of memory for a program that touches 387 pages (1.5 MiB). **The working set is a small fraction of the pages touched** — `sort` streams through its input and works on a small merge buffer. **Marks: [4]** for the frame count, **[3]** for the comparison with distinct pages.

**(c) [6]** With 90 µs per major fault and 1 s of work:

| Frames | LRU faults | fault time | total | slowdown |
|---:|---:|---:|---:|---:|
| 8 | 142,675 | 12.8 s | 13.8 s | 1,280% |
| 16 | 7,934 | 0.71 s | 1.71 s | 71% |
| 32 | 1,393 | 0.13 s | 1.13 s | 13% |
| **64** | **544** | **0.049 s** | **1.05 s** | **4.9%** |
| 128 | 464 | 0.042 s | 1.04 s | 4.2% |

**Under 10% from 64 frames up** — 256 KiB. **[4]** for the arithmetic, **[2]** for the answer to "which frame counts".

**(d) [4]** **Dropping consecutive repeats changes nothing for FIFO, LRU, OPT or the fault counts of any policy** — a repeated reference to the page just referenced is always a hit, and it changes no policy's state except by updating a timestamp that is already the newest. **It does change aging** (Q5), whose tick counts references: with repeats removed, a tick covers a different span of the program's execution. **[3]** for that distinction; **[1]** for "Q4(b) is unchanged, because faults are unchanged".

*(A student who says Clock is affected is wrong for the hit case — setting an already-set bit is idempotent — but give credit if they argue about the tick-based policies.)*

---

## Q5: Aging (15 points)

### (a) [6]

`loc.txt`, **60 frames** (FIFO 27,747 and LRU 16,518 at every tick, since they ignore it):

| Tick | `aging` | `aging2` |
|---:|---:|---:|
| 1 | 77,321 | 77,321 |
| 8 | 52,250 | 23,150 |
| 100 | 33,205 | **14,460** |
| 1,000 | 80,799 | 16,381 |
| 10,000 | 88,561 | 16,518 |

**[1 per row, +1 for including FIFO and LRU.]**

### (b) [5]

**Why `aging` collapses at long ticks [3]:** **a newly loaded page's counter is 0**, and between ticks nothing changes it. Once the frames are full, every fault therefore evicts **a page loaded since the last tick** — the lowest-numbered such frame — because pages present at the last tick have a 1 somewhere in their counters. **With a tick of 1,000 references and tens of faults between ticks, the policy spends its time evicting pages it has just fetched**, and does worse than FIFO.

**Why `aging2` avoids it [1]:** it compares **the reference bit first**, and a just-loaded page has that bit set, so it outranks anything not referenced since the last tick. The pages evicted are those that have been neither referenced recently nor used often.

**Why the fix does not help at tick 1 [1]:** at tick 1, **the shift happens before every reference**, so every reference bit is cleared immediately after it is set, and the two policies are identical — the counters hold only the last 8 references, almost all frames are 0, and the tie-break (lowest frame number) evicts frame 0 again and again.

### (c) [4]

**`aging2` at tick 100 beats exact LRU** — 14,460 against 16,518.

**Because 10% of the string's references are to uniformly random pages [2].** LRU is **pure recency**: a random reference makes that page the most recently used, and LRU will keep it over a working-set page that has not been touched in the last few hundred references. **Aging counts frequency as well as recency** — eight generations of reference bits — so a page touched once by a random reference has a single 1 in its counter, while a working-set page has several, and the working set survives.

**The general point [2]:** **LRU is optimal only if recency predicts the future exactly.** When a workload mixes a stable working set with noise, a policy with a little memory of frequency does better — which is why Linux's lists and its multi-generational LRU (L20 §8) are closer to aging than to LRU.

---

*CS 202 · Week 6 · PS 6 Solutions · Instructor Only*
