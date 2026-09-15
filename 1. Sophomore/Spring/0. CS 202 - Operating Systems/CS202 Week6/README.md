# CS 202 · Operating Systems
## Week 6: Page Replacement and Swapping

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 5 due **Friday**, PS 6 released **Wednesday**, **Quiz 6** at the start of **Monday's** lecture (covers Week 5).
**Lab 5 — last week's page map — is sat on the Tuesday of this week; Lab 6 covers this week and is sat on the Tuesday of Week 7.**

---

### Why This Week Exists

Because Week 5's promises come due. **A gigabyte mapped cost nothing; a gigabyte used costs a gigabyte** — and the machine has only so many frames.

**Three answers exist, and this week measures all three.** xv6 refuses: `sbrk` returns −1 and nothing dies. Linux **takes pages back**, writing them to swap and reading them in again at **90 µs each** — fifty times the cost of an ordinary fault, eleven thousand times the cost of a cache hit. And when reclaim cannot keep up, **something is killed**, chosen by a score you can read and partly set.

**In between lies the interesting part**: which page to take back. **The policy decides how often a program waits 90 µs**, and the difference between policies is measurable — on textbook strings, on generated ones, and on the memory trace of a real `sort`.

> ### ⚠️ Lab 6 and `thrash` run inside memory-limited scopes, always
>
> A program that eats memory on a shared machine makes the kernel reclaim from **everyone**, and
> `systemd-oomd` — active on these machines — may kill your whole session. **Every experiment this
> week runs under `systemd-run --user --scope -p MemoryMax=…`, and stays short.**

---

### Learning Objectives

By the end of Week 6, you should be able to:

1. Say what xv6 does when memory runs out, and **what that costs in memory it cannot reclaim**.
2. Name what Linux does with a **clean file page, a dirty file page, and an anonymous page**, and why they differ.
3. Explain **major and minor faults**, and **quote the measured cost of each** on this machine.
4. Read **pressure stall information**, and say why a thrashing machine shows more I/O pressure than memory pressure.
5. Explain **`kswapd`, watermarks and direct reclaim**, and when a cgroup reclaims at its own limit.
6. Simulate **FIFO, LRU, Clock, aging and OPT**, and reproduce the textbook fault counts.
7. Demonstrate **Belady's anomaly**, and prove that LRU cannot show it.
8. **Measure a real program's reference string** and its fault curve, and convert faults into runtime.
9. Define the **working set**, and **measure one** with `clear_refs` and `Referenced`.
10. Explain **thrashing** from measurements — and why locality matters more than capacity.
11. Explain **overcommit**: what the heuristic refuses, what `CommitLimit` means, and what `RLIMIT_AS` limits.
12. Explain the **OOM killer's score**, who sets `oom_score_adj` floors, and what `systemd-oomd` adds.

---

### This Week's Materials

| File | Purpose |
|---|---|
| [[L19 Swapping and the Cost of a Major Fault]] | **xv6 refusing** — `sbrk` −1, `fork` −1, nothing dies; what Linux reclaims and where it puts it; **a major fault at 90 µs**, beside 1.9 µs and 8 ns; **pressure: 6% memory, 18% I/O**; `kswapd`, watermarks, direct reclaim; what xv6 would need to swap |
| [[L20 Choosing a Victim Page Replacement]] | FIFO, OPT, LRU, Clock and aging, **reproducing the textbook's 15, 9, 12 and 14**; **Belady's anomaly — and Clock has it too**; a generated locality curve with a knee at the working set; **real `sort` and `ls` traces**, where Clock comes within 10% of LRU; Linux's lists and **multi-generational LRU, on in this kernel** |
| [[L21 Working Sets Thrashing and the OOM Killer]] | **A 257 MiB process with a 16 MiB working set**; **thrashing measured — 1,470× slower, and locality worth 11×**; `systemd-oomd` watching your session; **overcommit refusing 12 GiB but accepting 8 TB in pieces**; **the badness score, measured linear**; a kill observed, with `memory.events` |
| [[CS202 Week6/assignments/QUIZ 6 Week 6 Monday\|QUIZ 6 Week 6 Monday]] | Ten minutes, covers **Week 5**, answer key printed |
| [[PS 6 Page Replacement Simulated and Measured]] | Implement LRU, Clock and aging; Belady; a locality curve; **your own program's trace**. Due **Friday of Week 7** |
| `assignments/ps6/` | `pagesim.c` with `TODO`s, `gentrace.c`, `lackey2pages.c`, and the two classic strings |
| [[LAB 6 Out of Memory]] | Overcommit's refusals, `RLIMIT_AS`, **an OOM kill in a scope**, the badness score, and `systemd-oomd`. **Tuesday of Week 7** |
| `lab/hog.c`, `overcommit.c`, `oomscore.c` | Fill memory; probe what the heuristic refuses; watch your own score move |
| [[CS202 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | OSTEP 21–23, Silberschatz §10.4–§10.6, Denning (1968) |
| `resources/thrash.c`, `wss.c`, `memhog.c` | The thrashing curve, the working-set measurement, and xv6 running out |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A page fault that reaches the disk costs 90 µs, and everything else this week is about not taking one.**

The replacement policy tries to keep the pages you will ask for; **the working set is what that means in one number**; thrashing is what happens when the working set does not fit, and it is a cliff, not a slope — **1,470× at four times too little memory.** Overcommit is the promise, reclaim is the bill, and the OOM killer is what happens when the bill cannot be paid.

**And every one of those mechanisms is visible from an ordinary account**: `Referenced` for the working set, `memory.events` and pressure for the reclaim, `oom_score` for who dies next.

---

### Assessment Reminder

**PS 5 is due Friday at 17:00. PS 6 is released Wednesday.**

**Labs and quizzes carry no weight** and are still required. **Quiz 6 is at the start of Monday's lecture and covers Week 5.**

> **Two labs touch this week.** **Lab 5** — reading the page map — is sat on the **Tuesday of this
> week**. **Lab 6** covers this week and is sat on the **Tuesday of Week 7**.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 5's accessed and dirty bits** are the only information any of this week's policies has. **L18's demand paging** is why a program can ask for more than exists; **Lab 5's `MADV_PAGEOUT`** was reclaim by request, and its swapped pages are L19's. **Week 2's scheduler** had the same shape of problem — choose a victim with partial information — and MLFQ's boost was the same kind of fix as Clock's second chance.

**Sideways:** **MATH 251**'s expectation is behind Q3's estimate of how many random references must fault.

**Forward:** **Week 7's page cache** is the other half of reclaim: file pages, which this week only dropped. **Week 8's journaling** cares which dirty pages reach disk and when. **Project 2** adds lazy allocation to xv6, which is L19 §6's list. **Week 12** returns to cgroups as an isolation mechanism, not just an accounting one.

---

*CS 202 · Week 6 · © CSE Department*
