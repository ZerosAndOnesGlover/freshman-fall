# CS 202 · Problem Set 2
## Simulating MLFQ and a Fair Scheduler

---

**Released:** Week 2, Wednesday · **Due:** Week 3, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS2_{LastName}_{StudentID}.pdf`, plus your `schedsim.c` in a tarball `PS2_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Q1 and Q2 have exact expected output.** The lines below were produced by the reference
> simulator from the same skeleton you are given. If yours differs, **find out why before you
> submit** — a difference of one millisecond is a real difference in the rule you implemented.
>
> Your `schedsim.c` must compile clean under `gcc -O2 -Wall -Wextra`.

**Files provided** in `assignments/ps2/`:

| File | What it is |
|---|---|
| `schedsim.c` | The simulator. **FCFS, SJF, SRTF and round robin are complete and correct.** MLFQ and the fair scheduler are yours: eleven places marked `TODO`, each with a comment saying what goes there |
| `workloads/*.txt` | `convoy`, `late`, `mixed`, `gamer`, `starve`, `nices` — the workloads from L07 and L08 |

Read the comment at the top of `schedsim.c` for the workload format and the policy syntax. **Read the whole of `main` before writing anything**: the order of the steps inside each simulated millisecond is what makes the expected output exact.

---

### Q1: MLFQ (30 points)

Implement the MLFQ `TODO`s — the preemption rule, the ordering in `better()`, the boost, and demotion — so that `mlfq:N:Q:A:S` follows OSTEP's final rules (L08 §1), and `mlfq:N:Q:A:S:naive` follows the gameable version (L08 §2).

**Your output must reproduce these lines exactly:**

```
$ ./schedsim mlfq:3:10:20:0 < workloads/mixed.txt
edit           0    30     302        302       10      11      0.4
average turnaround 316.0 ms, average response 5.0 ms, 60 context switches, CPU busy 330 of 330 ms

$ ./schedsim mlfq:3:10:20:0:naive < workloads/gamer.txt
average turnaround 320.5 ms, average response 5.0 ms, 46 context switches, CPU busy 400 of 400 ms

$ ./schedsim mlfq:3:10:20:0 < workloads/gamer.txt
average turnaround 339.0 ms, average response 5.0 ms, 19 context switches, CPU busy 400 of 415 ms

$ ./schedsim mlfq:3:10:20:0:naive < workloads/starve.txt
average turnaround 846.3 ms, average response 7.0 ms, 802 context switches, CPU busy 900 of 900 ms

$ ./schedsim mlfq:3:10:20:100:naive < workloads/starve.txt
average turnaround 740.3 ms, average response 7.0 ms, 809 context switches, CPU busy 900 of 900 ms
```

**Submit:** the output of all five commands, in full.

**Marking:** 6 per matching run. **A run that differs earns half its marks if your write-up identifies which rule causes the difference.**

---

### Q2: A Fair Scheduler (25 points)

Implement the fair `TODO`s: `vruntime` charging by weight, ordering by `vruntime`, placement of arriving and waking jobs, and both kinds of preemption (L08 §4).

**Your output must reproduce these lines exactly:**

```
$ ./schedsim fair:20:1 < workloads/nices.txt
n0             0   300     432        432        0     132    132.0
n5             0   300     697        697       14     397    397.0
n10            0   300     900        900       19     600    600.0
average turnaround 676.3 ms, average response 11.0 ms, 84 context switches, CPU busy 900 of 900 ms

$ ./schedsim fair:20:1 < workloads/mixed.txt
edit           0    30     301        301       10      10      0.3
average turnaround 315.5 ms, average response 5.0 ms, 60 context switches, CPU busy 330 of 330 ms
```

**(a) [15]** The two runs above.

**(b) [5]** Remove the **wake-up preemption** — keep only the slice-expiry rule — and run `mixed.txt` again. Report the editor's wait per keystroke. **Which policy from L07 is it now identical to, and why exactly that one?** *(Compute the fair slice for two jobs of equal weight.)*

**(c) [5]** Remove the **sleeper placement** — let a waking job keep whatever `vruntime` it had — and run **both `mixed.txt` and `burst.txt`** again, comparing each with the full version. **One changes and one does not. Explain both** — why the editor in `mixed.txt` never benefits from the missing floor, and what the napping job in `burst.txt` does with it — and say what it would mean on a real machine for a process that had slept for an hour.

---

### Q3: Choosing the Allotment (15 points)

Run `mlfq:3:10:A:0` on `gamer.txt` for **A = 5, 10, 20, 50, 100 and 1000**.

**(a) [6]** Tabulate both jobs' turnaround for each *A*. **Does the gamer ever finish first?** Describe how the gap between the two jobs changes as *A* grows, and explain it: what does MLFQ turn into when *A* is larger than either job's total CPU time, and what does the gamer's 1 ms of self-inflicted I/O cost it then? Refer to the gamer's 9 ms bursts and the 10 ms top-level quantum.

**(b) [5]** Now run the same six values on `mixed.txt` and tabulate the editor's wait per keystroke and the batch job's turnaround. **Does a small allotment hurt the editor?** Explain from how much CPU the editor uses per keystroke.

**(c) [4]** Recommend an allotment for a machine that runs both kinds of workload, and justify it from your two tables in two sentences.

---

### Q4: The Voodoo Constant (15 points)

Run `mlfq:3:10:20:S:naive` on `starve.txt` for **S = 0, 25, 50, 100, 200 and 400**.

**(a) [7]** Tabulate the long job's turnaround and its total waiting time, and the interactive jobs' average wait per turn (`wait/rdy`), for each *S*. Plot the long job's turnaround against *S* — by hand is fine.

**(b) [4]** **What happens as *S* becomes very small?** Explain what MLFQ turns into, and why.

**(c) [4]** Now run the **non-naive** rules with *S* = 0 on `starve.txt`. **Does the long job still starve?** Explain why Rule 4's final form makes the boost less necessary for *this* workload, and give a workload for which the boost is still needed. *(L08 §3's second problem.)*

---

### Q5: The Model Against the Machine (15 points)

**(a) [5]** Run `share.c` from the Week 2 resources on your own machine. Compare Linux's shares for nice 1, 5, 10 and 19 with the shares your fair scheduler gives on a two-job version of `nices.txt` — write the workload. **Are they the same? Should they be?**

**(b) [5]** Run `slice.c` for 2, 3 and 4 hogs. Then work out the slice `fair:20:1` would give each job for 2, 3 and 4 equal jobs. **Where does the model disagree with the machine, and what did Linux change that explains it?** *(L08 §6.)*

**(c) [5]** Name **two things** a real CPU scheduler must deal with that `schedsim` does not model at all, and for each, say which of the results in Q1–Q4 you would expect it to change and in which direction. *(L07 §2's note on the model is a starting point; Week 1 supplies one, and your own machine has several CPUs.)*

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | MLFQ | 30 |
| 2 | A fair scheduler | 25 |
| 3 | Choosing the allotment | 15 |
| 4 | The voodoo constant | 15 |
| 5 | The model against the machine | 15 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 2 · PS 2 · © CSE Department*
