# CS 202 · Problem Set 4 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 4.** Q1 and Q2 are algorithms with exact output; students who match have implemented them. **Q3 and Q5 are about explaining measurements that do not do what intuition predicts** — the naive policy's deadlock rate is not monotonic in the supply, and a fixed back-off does not re-collide. **Mark the explanation against the student's own table**, not against the reference numbers.

**Reference programs**, all in `solutions_instructor/`: `banker reference`, `detect reference`, `banksim reference` and `livelock PS 4 Q5 reference (do not distribute).c`, and `bankbench.c` for Q4. The student skeletons in `assignments/ps4/` compile warning-clean.

**Measured figures are from the reference machine**: i5-8250U, Ubuntu 24.04.4, kernel **7.0.0-31**.

---

## Q1: The Banker's Algorithm (30 points)

### Reference `safe` and `request`

```c
static int safe(int *seq)
{
    int work[MAXR], finish[MAXP] = {0}, count = 0;
    memcpy(work, avail, sizeof(int) * m);
    for (int pass = 0; pass < n && count < n; pass++) {
        int progressed = 0;
        for (int i = 0; i < n; i++) {
            if (finish[i]) continue;
            int ok = 1;
            for (int j = 0; j < m && ok; j++)
                if (need(i, j) > work[j]) ok = 0;
            if (ok) {
                for (int j = 0; j < m; j++) work[j] += alloc[i][j];
                finish[i] = 1;
                if (seq) seq[count] = i;
                count++;
                progressed = 1;
            }
        }
        if (!progressed) break;
    }
    return count == n;
}

static int request(int i, const int *req)
{
    for (int j = 0; j < m; j++) if (req[j] > need(i, j)) return -2;
    for (int j = 0; j < m; j++) if (req[j] > avail[j]) return 0;
    for (int j = 0; j < m; j++) { avail[j] -= req[j]; alloc[i][j] += req[j]; }
    if (safe(0)) return 1;
    for (int j = 0; j < m; j++) { avail[j] += req[j]; alloc[i][j] -= req[j]; }   /* roll back */
    return -1;
}
```

**The scan order matters for matching output.** Scanning in index order *within* a pass, and continuing the pass after each success, gives ⟨P1, P3, P4, P0, P2⟩ on the textbook state. **A student whose scan restarts from P0 after every success gets ⟨P1, P3, P0, P2, P4⟩** — equally correct, and a different string. **Full marks for (a) require the exact line; give 10 of 12 for a different valid safe sequence with everything else right**, and say why in feedback.

### (a) [12]

Reproduced exactly, as in the handout.

### (b) [10]

```
$ ./banker < states/ps4_state.txt
state is SAFE; one safe sequence: <P1, P2, P3, P0>
request P1 (1,0,1): GRANTED
  available now (0,1,1)  state is SAFE; one safe sequence: <P1, P2, P3, P0>
request P2 (0,0,1): DENIED: would be unsafe
request P3 (1,0,0): WAIT: not available
request P0 (3,0,0): ERROR: exceeds maximum claim
request P1 (0,0,1): GRANTED
  available now (0,1,0)  state is SAFE; one safe sequence: <P1, P2, P3, P0>
```

**GRANTED occurs twice.** **[3]** for the output.

**The denial, by hand [5].** After P1's first grant, Available = (0, 1, 1). **Pretend to grant P2 (0, 0, 1)**: Available = (0, 1, 0); P2's allocation becomes (2, 1, 2).

| | Allocation | Max | **Need** | Fits in Work = (0, 1, 0)? |
|---|---|---|---|---|
| P0 | 1 0 0 | 3 2 2 | 2 2 2 | no |
| P1 | 6 1 2 | 6 1 3 | **0 0 1** | **no — needs 1 of C, 0 free** |
| P2 | 2 1 2 | 3 1 4 | 1 0 2 | no |
| P3 | 0 0 2 | 4 2 2 | 4 2 0 | no |

**No process can finish on the first step, so the state is unsafe.** The one unit of C was the unit P1 needed to finish and release its six units of A; **giving it to P2 leaves nobody able to start the chain.**

**The error [2].** P0's claim is Max (3, 2, 2) with Allocation (1, 0, 0): **Need (2, 2, 2)**. The request **(3, 0, 0) exceeds its need for A by one.**

### (c) [8]

**The bug [4]:** a denied request's pretend-grant stays in place — **Available is reduced and the process's Allocation increased by units it never received.** Later safety checks and availability checks see resources as held that are in fact free, **and the state drifts permanently away from reality.**

**A visible example [4]**, verified with the reference program and a copy with the rollback removed. After `textbook.txt`'s three requests, add `request 1 0 2 0`:

| | After P0's denied (0,2,0), Available is | `request P1 (0,2,0)` |
|---|---|---|
| **correct** | (2, 3, 0) | **GRANTED** — P1's need becomes 0, so it can finish |
| **no rollback** | **(2, 1, 0)** — two phantom units of B "held" by P0 | **WAIT: not available** |

**Accept** any sequence that produces a visibly wrong later answer, with the wrong state shown.

---

## Q2: Deadlock Detection (20 points)

### (a) [8]

Reference loop:

```c
int work[MAXR], finish[MAXP], order[MAXP], k = 0;
memcpy(work, avail, sizeof(int) * m);
for (int i = 0; i < n; i++) {
    int holds = 0;
    for (int j = 0; j < m; j++) holds |= alloc[i][j];
    finish[i] = !holds;
}
for (int progress = 1; progress; ) {
    progress = 0;
    for (int i = 0; i < n; i++) {
        if (finish[i]) continue;
        int ok = 1;
        for (int j = 0; j < m; j++) if (req[i][j] > work[j]) ok = 0;
        if (ok) { for (int j = 0; j < m; j++) work[j] += alloc[i][j];
                  finish[i] = 1; order[k++] = i; progress = 1; }
    }
}
```

Output reproduced exactly. **[4 + 4]**

### (b) [6]

```
$ ./detect < states/ps4_detect_a.txt
no deadlock; the processes can finish in the order <P2, P1, P0>
$ ./detect < states/ps4_detect_b.txt
DEADLOCKED: P0 P1
```

**Resource-allocation graph for `ps4_detect_b` [2]:** P0 holds one A and requests B; P1 holds B and requests A; P2 holds C and requests nothing; P3 holds nothing and requests C. **Cycle: P0 → B → P1 → A → P0.**

**P3 [2]:** it **holds nothing**, so the detector marks it finished from the start — it cannot be part of a cycle. *(Even without that rule it would finish in both files, once P2 releases the C it requests.)*

**P2 [2]:** it **requests nothing**, so its request (0, 0, 0) fits in *Work* even when nothing is available; it finishes first and releases C.

### (c) [6]

With P3 requesting (1, 0, 0), reference:

```
with the rule:     DEADLOCKED: P0 P1
without the rule:  DEADLOCKED: P0 P1 P3
```

**Which is right about P3 [3]:** **P3 is waiting forever** — the only unit of A is held by P0, which is deadlocked — **but P3 is not *part of* the deadlock**: it holds nothing, so no cycle passes through it, and **it would proceed at once if the deadlock were broken.** The rule's answer — P0 and P1 — is the set whose members must be dealt with.

**Why it matters [3]:** recovery by **killing deadlocked processes** would, without the rule, **kill P3 as well** — losing its work for nothing, since killing P0 or P1 alone releases what P3 needs. **The distinction is between the processes that cause the deadlock and those that are merely blocked by it.**

---

## Q3: How Conservative Is the Banker? (20 points)

### (a) [8]

Reference, 10,000 runs per policy, seed 202:

| `UNITS` | Largest claim `UNITS/2` | Naive: deadlocked | Banker: deadlocked | Banker: refused-but-free per run |
|---:|---:|---:|---:|---:|
| 4 | 2 | **24.5%** | 0 | 2.3 |
| 6 | 3 | **42.3%** | 0 | 6.5 |
| 9 | 4 | **33.5%** | 0 | 5.5 |
| 12 | 6 | **67.0%** | 0 | 23.3 |

**[2 per row.]** Student rates will differ somewhat with their `rand()`; **the non-monotonic shape should not.**

### (b) [6]

**Not monotonic** — both columns rise from 4 to 6, **fall from 6 to 9**, and rise steeply to 12. The explanation is in the claim distribution, `rand() % (UNITS/2 + 1)`:

| `UNITS` | Claims drawn from | Largest claim ÷ supply | Chance a claim is 0 | Units a run requests (six processes × three types, on average) |
|---:|---|---:|---:|---:|
| 4 | 0–2 | 0.50 | 1/3 | 18 × 1.0 = **18** |
| 6 | 0–3 | 0.50 | 1/4 | 18 × 1.5 = **27** |
| **9** | **0–4** | **0.44** | 1/5 | 18 × 2.0 = **36** |
| 12 | 0–6 | 0.50 | 1/7 | 18 × 3.0 = **54** |

- **More units per run means more steps at which processes can each hold part of what the others need** — which pushes both columns up as `UNITS` grows (4 → 6 → 12).
- **Integer division makes `UNITS` = 9 relatively generous**: the largest claim is 4 of 9, not half, so total demand is smaller relative to supply — **which is why 9 falls below 6.**
- **Small supplies have many zero claims** (a third of all claims at `UNITS` = 4), and a process that claims nothing of a resource cannot contend for it.

**Marking:** 2 for describing the non-monotonic trend correctly, 4 for an explanation using at least two of the three factors. **A student who asserts a monotonic trend their own table contradicts earns 0 for this part.**

### (c) [6]

**No [2].** A refusal means the state *after* the grant would be **unsafe**, and **unsafe is not deadlocked** (L14 §3): the processes might never ask for their full claims in an order that realises the deadlock. **Some refusals prevented deadlocks; others refused grants that would have been harmless.**

**Counting them [4]** — accept any sound design, for example: **at each refusal, fork the simulation** — copy the whole state, make the refused grant in the copy, **continue the copy under the naive policy with the same future random choices**, and record whether it deadlocks. The fraction of copies that deadlock is the fraction of refusals that prevented a deadlock *on that future*. A careful answer notes that one future is one sample, and repeats with several.

---

## Q4: What the Safety Check Costs (15 points)

### (a) [9]

Reference (`bankbench.c`): every resource but the last plentiful; need of the last increasing with index; scanned in reverse so each pass finds one process.

| *n* | *m* = 4 | *m* = 32 |
|---:|---:|---:|
| 100 | 0.018 ms | 0.066 ms |
| 200 | 0.071 ms | 0.257 ms |
| 400 | 0.278 ms | 1.102 ms |
| 800 | 1.093 ms | 4.356 ms |
| 1,600 | 4.615 ms | 17.398 ms |
| 3,200 | 20.590 ms | 74.690 ms |

**[5]** for a table from a construction that genuinely forces one process per pass, **[4]** for describing the construction. **Deduct 3** if every comparison fails at the first resource — then *m* has no effect and the student cannot answer (b).

### (b) [6]

**Exponent of *n* [3]:** successive ratios 3.9, 3.9, 3.9, 4.2, 4.5 at *m* = 4 → **about 4 per doubling, *n*²**, rising slightly at large *n* as the arrays leave the cache.

**Proportional to *m*? [3]** No: ×8 in *m* gives **×3.6** at *n* = 3,200 and ×3.7 at *n* = 100. **Each process visited costs a `finish[i]` test and loop overhead that does not grow with *m*; only the inner comparison does.** The measured cost is *a*·*n*² + *b*·*n*²*m* with a substantial *a*. **Accept** any explanation that separates per-process from per-resource work.

---

## Q5: Livelock and Back-Off (15 points)

### (a) [7]

Reference, 3 s each:

| Strategy | Two CPUs: rounds/s | failures/round | One CPU: rounds/s | failures/round |
|---|---:|---:|---:|---:|
| `backoff` (random 0–99 µs) | 1,323,645 | 0.01 | 1,342,831 | 0.01 |
| `fixed` (50 µs) | 1,294,034 | 0.01 | 1,345,755 | 0.00 |
| `expo` (1 µs doubling to 1 ms) | 1,277,357 | 0.01 | **1,412,072** | **0.00** (5,324 failures in 3 s) |

*(For comparison, L15 §4's `polite` retry: 128,579 per second and 32 failures per round on two CPUs.)*

### (b) [5]

**`fixed` did not re-collide**: it performs almost exactly like random back-off. **[1]**

**Why [3]:** **a 50 µs sleep is not 50 µs.** Timer slack (`/proc/self/timerslack_ns` = 50,000, L09 §6) lets the kernel fire each wake-up anywhere up to 50 µs late, and the wake-ups of the two threads are also subject to scheduling delay and, on an idle CPU, idle-state exit latency. **Each thread's actual sleep is already randomised by tens of microseconds**, which breaks the symmetry just as `rand_r` does. **Also accept**: collisions are rare to begin with (0.01 per round), because a failed thread sleeps while the other finishes its round — so even a repeated collision has little effect on throughput.

**Making it collide [1]:** remove the jitter — **`prctl(PR_SET_TIMERSLACK, 1)`** and busy-wait on `clock_gettime` for exactly 50 µs, or sleep with `clock_nanosleep` to an **absolute** deadline shared by both threads. **Accept** either, or "use a spin loop of a fixed iteration count".

### (c) [3]

**Heavy contention [1]:** doubling the window after each consecutive failure **spreads retries over a wider range the more often they collide**, so the expected number of collisions stays bounded however many contenders there are; a fixed range saturates.

**Light contention [1]:** a success **resets the window to its smallest**, so an uncontended retry waits only microseconds — **but a single unlucky collision can still cost up to the current window**, and the first few retries collide more often than with a wider fixed range.

**Here [1]:** `expo` did best on **one CPU** (1.41M rounds per second, 5,324 failures), where a thread that retries almost immediately after the other has released usually succeeds; on **two** it is slightly behind, since short early windows collide more with a thread genuinely running at the same time. **The differences are a few percent** because, with only two threads, contention is never heavy enough for the window to matter. **Accept** any argument consistent with the student's own numbers.

---

*CS 202 · Week 4 · PS 4 Solutions · Instructor Only*
