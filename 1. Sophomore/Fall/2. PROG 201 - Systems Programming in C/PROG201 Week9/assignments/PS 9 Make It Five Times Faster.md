# PROG 201 · Problem Set 9
## Make It Five Times Faster

---

**Released:** Week 9, Wednesday · **Due:** Week 10, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS9_{LastName}_{StudentID}.pdf`, and your code as `PS9_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **The requirement is 5× by analysis, not by guessing.** A submission that reaches 5× with no
> profile loses most of Q1 and Q3, and a submission that reaches 3× with a correct analysis and an
> honest account of what did not work scores better than you might expect. **The marks are for the
> method.**
>
> **Every number is on your own machine.** State your `gcc --version`, `uname -r`, `lscpu | grep -i
> "model name"`, and whether you are on BH 215 or your own hardware.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.

---

### The Program

`slow.c` reads a word list, counts occurrences, scores each distinct word, and prints a summary. **It is correct.** It is also much slower than it needs to be, and every reason is findable.

```bash
cd ps9
gcc -O2 -o gen gen.c
./gen 400000 > words.txt
gcc -O2 -g -o slow slow.c
./slow words.txt
```

```
400000 words, 5988 distinct
most distinctive: of  (count 18159, score 0.689853)
read+count 2.296 s, score 0.055 s, total 2.351 s
```

`check.sh` verifies that your version prints **byte-identical** output and reports the speedup:

```bash
./check.sh ./slow ./fast words.txt
```

**Identical output is not negotiable.** A faster program that computes something else has not been optimised.

---

### Q1: Find Out Where the Time Is — Before Changing Anything (24 points)

**(a) [6]** Before you profile: **write down your prediction.** Which part of the program do you think dominates, and why? Two or three sentences.

You will be marked on having written it, not on being right. *(Most people are wrong, and the value of the exercise is finding that out about yourself once.)*

**(b) [10]** Profile it with **Callgrind**:

```bash
head -c 400000 words.txt > words_small.txt        # it runs ~50x slower under valgrind
valgrind --tool=callgrind --callgrind-out-file=cg.out ./slow words_small.txt
callgrind_annotate cg.out
```

Report the top four entries with their percentages, and the annotated source lines that go with them.

**(c) [8]** Profile it again with a **sampling** profiler — the one from L28 §5, which is in your Lab 9 directory as `sprof.c`. Link it in, call `sprof_start(1000)` at the top of `main` and `sprof_report(8)` at the end, and **build with `-rdynamic`**.

Report its output. Then compare the two profiles and answer: **where do they disagree, and which one is more useful here?** *(One of them will attribute most of the time to a library without saying which function. Say why.)*

---

### Q2: Make It Faster (30 points)

**5× is the requirement.** Byte-identical output is the constraint.

**(a) [20]** The optimised program, and `check.sh` output showing both.

**(b) [10]** **A list of every change you made, in the order you made it, with the measurement after each one.** A table:

| # | change | seconds | cumulative speedup |
| --- | --- | --- | --- |
| 0 | (baseline) | 2.351 | 1.00× |
| 1 | | | |

**Include the changes that did not help**, with their numbers. A change that bought 0% is a result, and leaving it out makes your write-up a story rather than a record.

---

### Q3: Account For It (20 points)

**(a) [8]** For your **largest** win: name the operation that was hot, say how many times it was being executed and why, and say what your change did to that count.

"I used a hash table" is [2]. "The linear scan called `strcmp` about *N* × *D* times — 400,000 words against up to 5,988 distinct entries, which Callgrind measured at 2.45 billion instructions or 61.59% of the program — and a hash table makes that a constant number of comparisons per word" is [8].

**(b) [6]** Re-profile the optimised program. **The top entry will have changed.** Report the new profile and say what the program is now bounded by.

**(c) [6]** One of your changes was probably to `normalise()`. It has two separate problems, one obvious and one that only matters because of where it is written.

Name both. For the second, say what it costs asymptotically and why it is easy to miss when reading the code. *(Look at the loop condition.)*

---

### Q4: The Ceiling (14 points)

**(a) [6]** How fast could this program possibly be? Work out a floor for the runtime from first principles: the input is 2.1 MB, and it must be read and every word must be looked at once.

Use your Lab 9 bandwidth ceiling and a plausible per-word cost. Compare with what you achieved, and say how much room is left.

**(b) [4]** Try `-O3`, `-Os` and `-march=native` on **both** the original and your optimised version — four numbers.

Report them, and say what the comparison tells you about compiler flags relative to what you did by hand.

**(c) [4]** Apply **PGO** to your optimised version:

```bash
gcc -O2 -fprofile-generate -o p prog.c && ./p words.txt >/dev/null
gcc -O2 -fprofile-use -fprofile-correction -o p_pgo prog.c
```

Report the result. **If it is zero, say so and explain why** — a technique that does nothing for this program is a fact about the program.

---

### Q5: Method (12 points)

**(a) [4]** Your timings vary from run to run. Report the spread over ten runs of your optimised version, and say which statistic you used in Q2(b) and why.

If your program is now fast enough that `/usr/bin/time`'s resolution is a problem, **say so and fix it** — that is L30 §5's third pitfall and worth the marks.

**(b) [4]** Somewhere in this problem set you will have made a measurement that turned out to be wrong or meaningless. **Describe it**, say how you noticed, and say what the general form of the mistake is.

*(If you genuinely did not make one, say so — and then say which of L30 §5's five you think you are most at risk of, and why.)*

**(c) [4]** In one paragraph: you have a 5×-faster program. **Should it be merged?** Consider readability, the size of the diff, what a future maintainer needs to know, and whether 2.3 s was actually a problem. Argue a position.

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 9 · PS 9 · © CSE Department*
