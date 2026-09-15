# CS 202 · Problem Set 4
## The Banker's Algorithm, and Deadlock Detection

---

**Released:** Week 4, Wednesday · **Due:** Week 5, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS4_{LastName}_{StudentID}.pdf`, plus your `.c` files in a tarball `PS4_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Every measured answer requires output from your own machine.** State your CPU model, `uname -r`
> and `gcc --version` at the top.
>
> Every file you submit compiles clean under `gcc -O2 -Wall -Wextra`.

**Files provided** in `assignments/ps4/`:

| File | Yours to write | Provided |
|---|---|---|
| `banker.c` | `safe` and `request` | input parsing, output, the request loop |
| `detect.c` | the detection loop | input parsing, output |
| `banksim.c` | `safe` | the random-workload harness and both policies |
| `states/*.txt` | — | the textbook states, and three new ones |

---

### Q1: The Banker's Algorithm (30 points)

Implement `safe` and `request` in `banker.c` (L14 §4). **Scan processes in index order, repeatedly**, and check a request's claim, then its availability, then safety, in that order — so that your output matches exactly.

**(a) [12]** Your program must reproduce the textbook, line for line:

```
$ ./banker < states/textbook.txt
state is SAFE; one safe sequence: <P1, P3, P4, P0, P2>
request P1 (1,0,2): GRANTED
  available now (2,3,0)  state is SAFE; one safe sequence: <P1, P3, P4, P0, P2>
request P4 (3,3,0): WAIT: not available
request P0 (0,2,0): DENIED: would be unsafe
```

**(b) [10]** Run `./banker < states/ps4_state.txt`, which has four processes, three resource types and five requests, **and report the output.** **One request of each of the four kinds occurs**, and one kind occurs twice. Then:

- **For the request that is denied**, show by hand — a table of *Need* against *Work* — the point at which no process can finish.
- **For the request that exceeds its claim**, give the claim it exceeds.

**(c) [8]** A request that is denied must leave the state **exactly** as it was. **Describe the bug** that results if `request` forgets to roll back, and give a sequence of requests from `textbook.txt` in which the bug produces a visibly wrong later answer.

---

### Q2: Deadlock Detection (20 points)

Implement the detection loop in `detect.c` (L15 §1). A process that holds nothing is finished from the start; then scan in index order, finishing any process whose **request** fits in *Work*.

**(a) [8]** Your program must reproduce:

```
$ ./detect < states/textbook_detect.txt
no deadlock; the processes can finish in the order <P0, P2, P3, P4, P1>
$ ./detect < states/textbook_detect_more.txt
DEADLOCKED: P1 P2 P3 P4
```

**(b) [6]** Run `ps4_detect_a.txt` and `ps4_detect_b.txt`, which differ in **one** process's request. Report both. **Draw the resource-allocation graph for `ps4_detect_b`** and find its cycle. **Why is P3 not listed as deadlocked in either**, and **why is P2 never deadlocked** although nothing is available at the start?

**(c) [6]** Make a copy of `ps4_detect_b.txt` in which **P3, still holding nothing, requests one unit of the first resource**. Run it. Then remove the "holding nothing is finished" step from your detector and run it again. **Report both, and argue which answer is right about P3.** Is P3 waiting forever? Is it *part of* the deadlock? Why does the distinction matter to a system that will kill deadlocked processes to recover?

---

### Q3: How Conservative Is the Banker? (20 points)

Put your safety check into `banksim.c` (adapting it: processes already done are finished from the start, and need is `maxc − alloc`). The harness runs 10,000 random workloads under each policy.

**(a) [8]** Report the output for `UNITS` = 4, 6, 9 and 12 (change the `#define` and rebuild). **Tabulate the naive policy's deadlock rate and the Banker's refusals per run** against `UNITS`.

**(b) [6]** **Describe what happens to both columns as `UNITS` grows — the trend is not simple.** Explain it from how the harness draws each maximum claim, `rand() % (UNITS/2 + 1)`: for each value of `UNITS`, what is the largest claim relative to the supply, how many processes can claim nothing at all, and how many single-unit requests does a run make?

**(c) [6]** The harness refuses a grant only if the state after it would be unsafe. **Is every refusal a deadlock prevented?** Argue from L14 §3's distinction between unsafe and deadlocked, and describe how you would modify the harness to *count* how many refusals actually prevented a deadlock. *(You need not implement it.)*

---

### Q4: What the Safety Check Costs (15 points)

**(a) [9]** Write a program that builds a **worst-case** state for your safety check — one in which every pass finishes exactly one process and every comparison scans all *m* resources — for *n* = 100, 200, 400, 800, 1,600 and 3,200, with *m* = 4 and *m* = 32, and times one call to your `safe`. Report the table. *(L14 §5 describes one such construction; yours may differ.)*

**(b) [6]** Estimate the exponent of *n* from your table (the ratio between successive doublings). **Does the cost grow in proportion to *m*?** Explain any departure from O(*n*²*m*) in terms of what your implementation does per process that does not depend on *m*.

---

### Q5: Livelock and Back-Off (15 points)

Copy `resources/livelock.c` and **add two retry strategies** to it:

- `fixed`: after a failed `trylock`, sleep **exactly 50 µs**;
- `expo`: sleep a random time below a limit that **starts at 1 µs, doubles after each consecutive failure up to 1 ms**, and **resets to 1 µs after a success**.

**(a) [7]** Measure `backoff`, `fixed` and `expo` for 3 seconds each, pinned to **two** CPUs (`taskset -c 2,3`) and to **one** (`taskset -c 2`). Report rounds per second and failures per round.

**(b) [5] Predict first:** two threads that fail together and both sleep *exactly* 50 µs should wake together and fail together again. **Did `fixed` behave like that?** If not, explain why a request to sleep 50 µs does not produce a sleep of exactly 50 µs on this machine. *(L09 §6.)* What would you have to change to make `fixed` collide repeatedly?

**(c) [3]** Ethernet used exponential back-off for collisions. **What does it buy over a fixed random range when contention is heavy, and what does it cost when contention is light?** Say whether your `expo` measurements on one CPU and on two support that argument, and why the difference is small here.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The Banker's algorithm | 30 |
| 2 | Deadlock detection | 20 |
| 3 | How conservative is the Banker? | 20 |
| 4 | What the safety check costs | 15 |
| 5 | Livelock and back-off | 15 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 4 · PS 4 · © CSE Department*
