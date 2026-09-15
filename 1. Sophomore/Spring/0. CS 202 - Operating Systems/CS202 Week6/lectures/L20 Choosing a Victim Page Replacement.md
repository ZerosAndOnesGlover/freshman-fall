# CS 202 · Operating Systems
## Week 6 · Lecture 2 of 3
### Choosing a Victim: Page Replacement

---

**Sat:** Wednesday of Week 6, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 22; Silberschatz §10.4 · **Next:** L21, working sets, thrashing and the OOM killer

---

## 1. The Question

L19 left the kernel with every frame full and a page to bring in. **Some page must go.** If it is used again soon, it comes back through a **major fault** — L19 §3's disk read, hundreds of times slower than any memory access. **The policy that picks the victim therefore decides how many major faults a program takes**, and this lecture measures that number for five policies.

**The tool is `pagesim.c`**: it reads a **reference string** — one page number per access — and counts faults for a given number of frames. **Loading a page into an empty frame counts as a fault**, as it would at program start. The policies are the classic ones, and each is a few dozen lines.

**The standard string** — Silberschatz §10.4, twenty references to six pages:

```
7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
```

```
$ ./pagesim all 1 2 3 4 5 6 7 8 < textbook.txt
20 references, 6 distinct pages
  frames     fifo      lru    clock    aging   aging2      opt
       1       20       20       20       20       20       20
       2       15       17       15       14       17       13
       3       15       12       14       10       13        9
       4       10        8        9        8        8        8
       5        9        7        9        7        7        7
       6        6        6        6        6        6        6
```

**Six faults is the floor** — each page must be loaded once. **The book's numbers for three frames — FIFO 15, LRU 12, OPT 9 — are reproduced.** The rest of the lecture is why the columns differ, and which differences survive on real programs.

---

## 2. FIFO, and Belady's Anomaly

**First in, first out**: evict the page that has been in memory longest. It needs a queue and nothing else — no information about use at all.

**It evicts pages that are old, not pages that are unused.** A page loaded at start-up and used on every access is evicted as soon as its turn comes, and faults straight back in.

**Worse, more memory can make it worse.** Belady, Nelson and Shedler's string from 1969:

```
$ ./pagesim all 3 4 < belady.txt           # 1 2 3 4 1 2 5 1 2 3 4 5
  frames     fifo      lru    clock    aging   aging2      opt
       3        9       10        9        9        9        7
       4       10        8       10        7        7        6
```

**FIFO with four frames takes 10 faults; with three, 9.** Adding a frame changes *which* pages are in memory, not just how many, and here it keeps the wrong ones. **Clock, measured, does the same.**

**LRU and OPT cannot.** Both are **stack algorithms**: the set of pages they hold with *n* frames is always a subset of the set with *n* + 1. A reference that hits with *n* frames therefore hits with *n* + 1, and faults can only fall as memory grows. FIFO's set with four frames is not a superset of its set with three, and the table shows the consequence.

---

## 3. OPT: The Unreachable Bound

**Evict the page whose next use is furthest in the future.** Belady proved no policy does better, and the table agrees: **9 faults for the textbook string with three frames, against LRU's 12 and FIFO's 15.**

**No kernel can run it**: it needs the future. `pagesim` can, because it has the whole string before it starts — it computes each reference's next use in one backwards pass. **OPT's value is as a yardstick**: a policy within a few percent of it has nothing left to gain.

---

## 4. LRU, and Why No Kernel Does It

**Least recently used**: evict the page whose last use is oldest — **the past as a predictor of the future**, which works exactly when programs have locality. **12 faults** on the textbook string; **LRU is a stack algorithm**, so no anomaly.

`pagesim` implements it with a timestamp per frame, updated on every reference. **A kernel cannot.** Most references do not enter the kernel at all: the TLB (L17) translates them in hardware, and the kernel learns nothing. **The only record of use is the accessed bit** the CPU sets in the page-table entry (L16 §3). A kernel that wanted timestamps would have to take a fault on every access — L18 §1's 1.9 µs, on every 10 ns load.

**Real policies approximate LRU using that one bit.**

---

## 5. Clock: Second Chance with One Bit

**Arrange the frames in a circle with a hand.** Every reference sets the frame's reference bit — the accessed bit. **On a fault the hand sweeps**: a frame with its bit set has the bit **cleared** and is passed over — a second chance; **the first frame found with its bit clear is evicted**.

- **A page used since the hand last passed survives.** A page not used for a full sweep does not.
- **If every bit is set, the hand goes all the way round, clearing them, and evicts where it started** — Clock degenerates to FIFO, which is why it shows Belady's anomaly in §2.
- **The cost is one bit per page and a sweep per fault** — nothing per access.

**14 faults on the textbook string with three frames and 9 with four**, between FIFO and LRU. **§7 shows how close to LRU it comes on real programs.**

**Aging** keeps more history: an 8-bit counter per frame, shifted right at every clock tick with the reference bit copied into its top bit, and the frame with the smallest counter evicted. **A page used in the last tick outranks one used only earlier; a page used in several recent ticks outranks one used in one.** `aging2` in the tables differs in one detail — it compares the reference bit before the counter — and **PS 6 Q5 is about why that detail matters.**

---

## 6. Locality, Made to Order

**Policies differ only when programs have structure.** `gentrace.c` makes a string with known structure: **1,000 pages; ten phases of 10,000 references; in each phase a working set of 50 pages receives 90% of references** and the other 10% go anywhere:

```
$ ./gentrace 1000 50 90 10 10000 1 | ./pagesim -t 100 all 10 25 40 50 60 80 100 200
100000 references, 1000 distinct pages
```

| Frames | FIFO | LRU | Clock | OPT |
|---:|---:|---:|---:|---:|
| 10 | 83,864 | 83,700 | 83,819 | 55,564 |
| 25 | 61,728 | 60,405 | 61,072 | 29,836 |
| 40 | 43,209 | 38,515 | 40,379 | 15,857 |
| **50** | 34,197 | **25,908** | 28,654 | 10,352 |
| **60** | 27,747 | **16,518** | 19,906 | 8,933 |
| 80 | 20,327 | 10,155 | 11,571 | 7,909 |
| 100 | 16,696 | 9,558 | 9,969 | 7,236 |
| 200 | 10,801 | 8,538 | 8,561 | 5,271 |

- **Below the working set, every policy is bad**, and they are nearly equal: with 10 or 25 frames the working set does not fit, and no choice of victim helps.
- **Around 50–80 frames the policies separate.** LRU keeps the working set and FIFO does not: **at 60 frames FIFO faults 68% more than LRU.** Clock is within 21% of LRU.
- **Past the working set the curve flattens**: the remaining faults are the 10% of references to random pages, which no amount of memory short of 1,000 frames prevents — **and even OPT pays them.**

**That knee is the working set.** L21 measures one in a real process, and shows what happens to a machine when the frames sit to the left of it.

---

## 7. Real Programs

**`valgrind --tool=lackey --trace-mem=yes` records every memory access a program makes**; `lackey2pages.c` reduces the log to a reference string of data pages, removing consecutive repeats. Two programs, traced on the reference machine:

**`sort -n` of 2,000 numbers**: 2,121,880 data accesses → **1,031,795 references to 387 distinct pages**.

| Frames | FIFO | LRU | Clock | OPT |
|---:|---:|---:|---:|---:|
| 8 | 237,042 | 142,675 | 224,263 | 80,568 |
| 16 | 10,282 | 7,934 | 8,554 | 4,073 |
| **32** | 2,747 | **1,393** | 1,520 | 890 |
| 64 | 741 | 544 | 558 | 430 |
| 128 | 473 | 464 | 463 | **387** |
| 387 | 387 | 387 | 387 | 387 |

**`ls /usr/bin`**: 7,118,108 data accesses → **2,390,544 references to 302 distinct pages**.

| Frames | FIFO | LRU | Clock | OPT |
|---:|---:|---:|---:|---:|
| 8 | 367,658 | 313,113 | 328,962 | 156,793 |
| 16 | 72,350 | 35,870 | 50,057 | 18,887 |
| **32** | 17,171 | **10,191** | 10,508 | 5,827 |
| 64 | 6,063 | 4,314 | 4,530 | 2,146 |
| 128 | 1,104 | 918 | 937 | 469 |

- **Real programs have far sharper locality than the synthetic string.** `sort` touches 387 pages, but **with 16 frames it faults on only 1% of its references**, and with 32 frames on 0.13%.
- **Clock is within 10% of LRU from 32 frames up, on both programs** — one bit per page buys nearly all of LRU's benefit. At 8 and 16 frames, where every page's bit is set on each sweep, it slides towards FIFO.
- **With 128 frames, OPT loads each of `sort`'s pages exactly once**: its working set fits in a third of its pages.

**Caution:** these are single runs of two programs, and `lackey2pages` drops consecutive repeats, which changes the counts for policies with clocks. **PS 6 Q4 has you trace a program of your own.**

---

## 8. What Linux Does

**Linux uses the accessed bit, in lists rather than a circle.** Pages sit on an **active** and an **inactive** list, separately for **anonymous** memory (evicted to swap) and **file** memory (dropped, or written back if dirty). Reclaim scans the inactive list's tail; a page found with its accessed bit set is moved to the active list — a second chance — and one not referenced is evicted. **Pages move from active to inactive as the lists are balanced.** It is Clock's idea with two hands and a notion of which memory is cheaper to evict: `swappiness`, 60 here, weights anonymous against file pages.

**This kernel runs the newer multi-generational LRU instead**:

```
$ cat /sys/kernel/mm/lru_gen/enabled
0x0007
```

**MGLRU sorts pages into several generations by how recently their accessed bits were found set**, walking page tables to collect the bits in bulk rather than list by list, and evicts from the oldest generation. **It is aging (§5) with a handful of generations instead of an 8-bit counter** — and it was merged because, on Google's and others' fleets, it spent less CPU on reclaim and evicted better.

---

## 9. What to Take Away

1. **The victim decides the number of major faults.** On the textbook string: **FIFO 15, LRU 12, Clock 14, OPT 9** with three frames.
2. **FIFO can fault more with more frames** — 9 with three, 10 with four on Belady's string — **and so can Clock. Stack algorithms like LRU and OPT cannot.**
3. **OPT needs the future**; it is the bound, not a policy.
4. **Exact LRU needs a timestamp on every access, which the kernel never sees.** The accessed bit is all the hardware gives.
5. **Clock approximates LRU with one bit**: within 21% of LRU at the working set on a synthetic string, and **within 10% on real `sort` and `ls` from 32 frames up.**
6. **Below the working set every policy fails; above it every policy is fine.** The policies matter at the knee — which is exactly where a loaded machine lives.
7. **Linux keeps active and inactive lists, and this kernel uses multi-generational LRU**: aging, with generations.

---

## Exercises

1. By hand, run FIFO, LRU and OPT on the textbook string with **three** frames, and check the table. At which references do FIFO and LRU first choose different victims?
2. **Prove that LRU is a stack algorithm**: show that the pages LRU holds with *n* frames after any reference are the *n* most recently used distinct pages.
3. Construct a short string on which **Clock faults more than FIFO** with the same number of frames. *(Hint: what does Clock do when every bit is set?)*
4. In §6, **why does OPT still fault 5,271 times with 200 frames?** Estimate the number from the string's parameters.
5. `sort` with 8 frames: FIFO 237,042 faults, LRU 142,675, Clock 224,263. **Why is Clock so much closer to FIFO than to LRU at this size**, when it is close to LRU at 32 frames?

---

*CS 202 · Week 6 · L20 · © CSE Department*
