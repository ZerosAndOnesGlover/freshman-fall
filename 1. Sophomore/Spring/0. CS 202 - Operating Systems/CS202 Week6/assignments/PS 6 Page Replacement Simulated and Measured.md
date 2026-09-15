# CS 202 · Problem Set 6
## Page Replacement, Simulated and Measured

---

**Released:** Week 6, Wednesday · **Due:** Week 7, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS6_{LastName}_{StudentID}.pdf`, plus your `pagesim.c` and the trace you record in Q4, gzipped, in `PS6_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Every measured answer requires output from your own machine.** State your CPU model, `uname -r`
> and `gcc --version` at the top. Your `pagesim.c` must compile clean under `gcc -O2 -Wall -Wextra`.

**Files provided** in `assignments/ps6/`:

| File | Yours to write | Provided |
|---|---|---|
| `pagesim.c` | `lru`, `clock_policy` (Q1), `aging_common` (Q5) | the page-to-frame table, `fifo`, `opt`, and the driver |
| `gentrace.c` | — | a reference string with locality, from a seed |
| `lackey2pages.c` | — | valgrind's memory trace → a page reference string |
| `traces/textbook.txt`, `traces/belady.txt` | — | the two classic strings |

**A reference string is one page number per line, in hexadecimal.** A fault is any reference to a page not in a frame, **including the first load into an empty frame**. Fill empty frames in order, frame 0 first.

---

### Q1: LRU and Clock (25 points)

Implement `lru` and `clock_policy` (L20 §4–§5), following the comments in `pagesim.c` exactly — in particular **what happens to the clock hand when it passes a frame, and where it stops.**

**(a) [15]** Reproduce, for `traces/textbook.txt`:

```
$ ./pagesim lru 1 2 3 4 5 6 7 8 < traces/textbook.txt
20 references, 6 distinct pages
  frames      lru
       1       20
       2       17
       3       12
       4        8
       5        7
       6        6
       7        6
       8        6
$ ./pagesim clock 1 2 3 4 5 6 7 8 < traces/textbook.txt
  frames    clock
       1       20
       2       15
       3       14
       4        9
       5        9
       6        6
       7        6
       8        6
```

**(b) [5]** **With two frames, LRU takes 17 faults and FIFO takes 15.** Show the two frame contents step by step for the first ten references and **name the reference at which they first differ.** Is LRU doing anything wrong?

**(c) [5]** Clock with **five** frames takes 9 faults — the same as with four — while LRU improves from 8 to 7. **Explain from the algorithm** what Clock is doing with the fifth frame.

---

### Q2: Belady's Anomaly (15 points)

**(a) [5]** Run all four policies on `traces/belady.txt` — the string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 — with **three** and **four** frames, and report the table.

**(b) [5]** **Which policies fault more with four frames than with three?** For **one** of them, show the frame contents at the reference where the extra fault happens, and explain what the extra frame changed.

**(c) [5]** **Prove that LRU cannot show the anomaly**: show that after any prefix of any string, the pages LRU holds with *n* frames are exactly the *n* most recently referenced distinct pages, and conclude. **Does your argument also cover OPT?** If not, say what a separate argument would need.

---

### Q3: Locality (20 points)

`./gentrace TOTAL WSS P PHASES LENGTH SEED` writes a string over `TOTAL` pages in `PHASES` phases; in each phase, `P` percent of references fall in a working set of `WSS` consecutive pages and the rest anywhere.

**(a) [8]** Run:

```bash
./gentrace 1000 50 90 10 10000 1 > loc.txt
./pagesim all 10 25 40 50 60 80 100 200 < loc.txt
```

and report the FIFO, LRU, Clock and OPT columns. *(Ignore the aging columns until Q5.)*

**(b) [6]** **Explain the shape of the curve**: why the policies are nearly equal at 10 and 25 frames, why they separate around 50–60, and why the curve flattens after 100. **Give LRU's advantage over FIFO as a percentage at 60 frames**, and Clock's gap to LRU.

**(c) [6]** **Why does OPT still take 5,271 faults with 200 frames**, when the working set of each phase is 50 pages? **Estimate that number from the generator's parameters** — and say what it tells you about the limit of any replacement policy on this workload.

---

### Q4: A Real Program (25 points)

Record your own trace. **Pick something small**: `valgrind` slows a program about fifty times, and the log grows by roughly 15 bytes per memory access.

```bash
seq 1 2000 | shuf > nums.txt
valgrind --tool=lackey --trace-mem=yes --log-file=t.log sort -n nums.txt -o /dev/null
./lackey2pages -d < t.log > mine.pages        # -d: data accesses only
rm t.log                                       # it is large
sort -u mine.pages | wc -l
```

**(a) [8]** Report the program you traced, the number of accesses and references `lackey2pages` reports, and the number of distinct pages. **Then give the fault table** for FIFO, LRU, Clock and OPT at several frame counts from 8 up to the number of distinct pages.

**(b) [7]** **At what number of frames does your program's fault count fall to under 1% of its references?** What does that number say about its working set, compared with the number of distinct pages it touches?

**(c) [6]** L19 §3 measured a major fault on this machine at about **90 µs**. Suppose every fault in your table were a major fault and the program's own work took **1 second**. **Tabulate the total runtime at each frame count**, and say which frame counts keep the slowdown under 10%.

**(d) [4]** `lackey2pages` **drops consecutive references to the same page.** For which of the four policies does that change the answer, and for which does it not? **Would keeping the repeats change your Q4(b) answer?**

---

### Q5: Aging (15 points)

Implement `aging_common` (L20 §5), exactly as its comment specifies: an 8-bit counter and a reference bit per frame; **before** reference *t*, if *t* > 0 and *t* is a multiple of the tick, every occupied frame's counter is shifted right with the reference bit copied into its top bit and the bit cleared; a loaded page's counter starts at 0; on a fault, evict the smallest counter, lowest frame number among equals. **`aging2` differs in one line**: it compares the reference bit and the counter together as a 9-bit number, the reference bit most significant.

**(a) [6]** With `loc.txt` from Q3, run **60 frames** at ticks **1, 8, 100, 1,000 and 10,000** (`-t`), and report `aging` and `aging2` at each, with LRU and FIFO for comparison.

**(b) [5]** **`aging` at tick 1,000 takes more faults than FIFO. Explain why**, from the rule for a newly loaded page's counter. **Why does `aging2` not have this problem**, and why does the fix not help at tick 1?

**(c) [4]** At tick 100, **`aging2` takes fewer faults than exact LRU** — 14,460 against 16,518. **LRU is supposed to be the better approximation of OPT. Explain how a coarser policy can beat it here**, using what `gentrace` puts in the string besides the working set.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | LRU and Clock | 25 |
| 2 | Belady's anomaly | 15 |
| 3 | Locality | 20 |
| 4 | A real program | 25 |
| 5 | Aging | 15 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 6 · PS 6 · © CSE Department*
