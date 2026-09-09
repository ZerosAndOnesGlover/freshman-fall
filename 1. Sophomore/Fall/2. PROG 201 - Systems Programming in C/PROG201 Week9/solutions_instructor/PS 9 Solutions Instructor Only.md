# PROG 201 · PS 9 Solutions
## Make It Five Times Faster — Instructor Only

---

**Do not distribute.** Q1(a) asks for a prediction before profiling; a student who has seen the answer cannot make one.

**Machine these numbers came from:** Intel i5-8250U, gcc 13.3.0, Linux 7.0.0-30-generic. `words.txt` from `./gen 400000`, which is deterministic — **every student's input is identical**, so the *ratios* are directly comparable even though the absolute times are not.

The reference optimised version is alongside this file as `fast reference (do not distribute).c`.

---

## The Three Defects, and What Each Is Worth

Measured with `check.sh`'s best-of-5, output verified identical at every stage:

| stage | seconds | cumulative | what it bought |
| --- | --- | --- | --- |
| baseline | **2.31** | 1.0× | |
| + hash-table `lookup` | **0.10** | **23×** | the whole game |
| + `normalise` without `malloc` and without `strlen` in the condition | 0.09 | 26× | ~10% |
| + `compute_scores` bucketed by first letter | **0.03** | **77×** | **3× of what was left** |

**Read the last two rows together.** In the original profile `compute_scores` was 0.055 s of 2.351 — **2.3%, invisible, correctly ignored**. After the first fix it is a third of the remaining runtime. That is Amdahl's law working in the direction people forget, and it is L28 §7's "the new top item is rarely the old second place." **Reward a student who noticed it by re-profiling; most will find it by re-profiling and not remark on it.**

**The 5× requirement is met by the first change alone.** That is deliberate: it means a student who profiles correctly and makes one change passes, and everything above that is Q3 and Q4.

### The defects, stated

**1. `lookup` is a linear scan.** *O(D)* per word, *N* × *D* overall — 400,000 words against up to 5,988 distinct entries. Callgrind attributes **61.59% of all instructions to `__strcmp_avx2`** and 2.45 billion instruction reads. A hash table makes it *O(1)* expected.

**2. `normalise` has two problems**, and Q3(c) is about the second:

```c
char *out = malloc(MAXLEN);                              /* (a) */
for (int i = 0; i < (int) strlen(w) && j < MAXLEN - 1; i++)   /* (b) */
```

(a) is a `malloc`/`free` pair per word — 400,000 of each. (b) is **`strlen` in the loop condition**, so it is re-evaluated every iteration: *O(len²)* per word. With words of 3–9 characters that is small, which is exactly why it is easy to miss and why it is worth only ~10% here. **Say to students who found only (a) that (b) is the one CS:APP §5.1 opens with.**

**3. `compute_scores` is *O(D²)*** — for each distinct word it re-sums every other word with the same first letter. One pass into a 256-entry array of totals makes it *O(D)*.

---

## Q1 — Find Out Where the Time Is (24)

**(a) [6]** Any written prediction earns the marks. **Do not mark the content.**

Typical predictions, for calibration: "the file reading", "the `printf`", "`fscanf` is slow". The commonest correct-ish one is "the nested loop in `compute_scores`" — which is wrong for a good reason, since it *is* the only obvious *O(n²)* in the file and it is 2.3% of the runtime.

**(b) [10]** The four entries **[6]**, the annotated lines **[4]**:

```
3,984,355,595 (100.0%)  PROGRAM TOTALS
  2,453,885,767 (61.59%)  strcmp-avx2.S:__strcmp_avx2 [libc.so.6]
  1,247,789,129 (31.32%)  slow.c:main [./slow]
    227,382,882 ( 5.71%)  ???:0x0000000000109190
     30,305,117 ( 0.76%)  vfscanf-internal.c:__vfscanf_internal
```

**`main` at 31.32% is inlining**, not a mistake — `lookup`, `add_word` and `normalise` are all static and got folded in. A student who reports "the profile says `main`" and is puzzled has spotted something real; the annotated source resolves it.

**(c) [8]** The sampler's output **[4]**, the comparison **[4]**:

```
[sprof]    1955   74.88%  /lib/x86_64-linux-gnu/libc.so.6
[sprof]     465   17.81%  main
[sprof]     179    6.86%  ./slow_p
```

**They agree on the shape and the sampler cannot name the function.** ~75% "somewhere in libc" against Callgrind's precise `__strcmp_avx2`. The reason is L28 §6: `dladdr` reads the **dynamic** symbol table, and glibc resolves `strcmp` through an **IFUNC** to a variant whose symbol is not there.

Full marks require naming *why* the sampler is vague, not just that it is. **Callgrind is more useful here**; the sampler would be more useful on a long-running program where 50× slowdown is unaffordable.

---

## Q2 — Make It Faster (30)

**(a) [20]** 5× and identical output **[14]**; `check.sh` output pasted **[6]**.

**Identical output is a hard gate.** A submission that is 100× faster and prints a different score has not optimised anything; mark Q2(a) at 0 and mark the rest normally, and say why.

**(b) [10]** The table **[6]**, **the failed changes included [4]**.

Award the last four marks generously and visibly. A table containing "tried `-O3`: 2.38 s, slower than `-O2`" or "tried `restrict`: no change" is better work than one showing only wins, and if the rubric does not reward it, next year's tables will all be monotonic.

---

## Q3 — Account For It (20)

**(a) [8]** As the "Defects" section above. The marks are for **the count** — *N* × *D*, with numbers — not for naming the data structure.

**(b) [6]** The new profile **[3]**, the new bottleneck **[3]**.

After the hash fix, `compute_scores` dominates; after all three, the program is bounded by **`fscanf` and the file read** — `__vfscanf_internal` and the kernel. A student who reports "it is now I/O bound" and stops there has it; one who adds "so the remaining wins are in the parsing, not the counting" has it properly.

**(c) [6]** Both problems **[4]**, the asymptotic answer **[2]**.

`strlen` in the condition is *O(len)* per iteration, so *O(len²)* per word. Easy to miss because **it reads as a bound rather than as a call**, and because C's `for` re-evaluates the condition every time — which people know and do not apply.

---

## Q4 — The Ceiling (14)

**(a) [6]** Any defensible floor with arithmetic shown.

Reference: the input is 2.1 MB. At the Lab 9 bandwidth ceiling of ~13.7 GB/s that is **0.15 ms** to read; 400,000 words at even 20 ns of parsing each is **8 ms**. So a floor of roughly **10 ms against the 30 ms achieved** — about 3× of headroom, essentially all of it in `fscanf`.

Marks for the method, not the number. A student who concludes "we are within 3× of the floor and the remaining work is parsing" has answered it.

**(b) [4]** Four numbers. Reference, on the original: `-O0` 2.78, `-O2` 2.35, `-O3` 2.38, `-Os` 2.78, `-Ofast` 2.33. On the optimised version: 0.05 / 0.04 / 0.04 / 0.04.

**The conclusion wanted:** flags bought **19%** and the source changes bought **77×**, and once the algorithm was right the flags bought nothing at all. **`-O3` was slower than `-O2`** on the original — worth a sentence about code size.

**(c) [4]** Reference: **0.0380 s with and without PGO — no change.**

The explanation: the program is bounded by hash lookups and `fscanf`, not by branch misprediction or code layout, so there is nothing for PGO to improve. **"It did nothing" is the correct answer and earns full marks with the reasoning**; a student who reports a 20% PGO win should be asked to show the two timings, because it is more likely to be noise than PGO.

---

## Q5 — Method (12)

**(a) [4]** The spread **[2]**, the statistic and the resolution problem **[2]**.

Reference: ten runs of the optimised version through `/usr/bin/time` give `0.03 0.03 0.04 0.04 0.03 0.04 0.03 0.03 0.04 0.03` — **every measurement is right and the resolution is 10 ms**, which on a 30 ms program is ±33%. The correct response is to switch to `clock_gettime` or to time a loop of runs. **A student who notices this unprompted has found L30 §5's third pitfall in their own data**; say so.

The statistic: **the minimum**, for a microbenchmark, because the distribution has a hard floor and a long tail.

**(b) [4]** Any honest account.

Most likely candidates, all real: timing at 10 ms resolution (above); comparing a cold first run against a warm one; forgetting that Callgrind's percentages are of *instructions*, not time, and being surprised the speedup did not match; measuring with `-O0` because that is what the debugger build was.

**"I did not make one" plus a stated risk** is worth the full 4 if the risk is specific.

**(c) [4]** Any defended position. There is no expected answer, and the marks are for engaging with the trade.

**For merging:** 77×, output identical, and the hash table is thirty lines of standard code. **Against:** the original is obviously correct and the new one has a hash table a reader must verify; the `static char` buffer in `normalise` is not reentrant and would be a bug the day someone threads this; and if 2.3 s was never a problem, the whole diff is risk with no return.

**The best answers separate the three changes** and merge only the first — 23× for thirty readable lines — while noting that the other two bought 3× more on top of a program nobody was complaining about.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Find out where the time is | 24 |
| 2 | Make it faster | 30 |
| 3 | Account for it | 20 |
| 4 | The ceiling | 14 |
| 5 | Method | 12 |
| | **Total** | **100** |

---

*PROG 201 · Week 9 · PS 9 Solutions · Instructor Only · © CSE Department*
