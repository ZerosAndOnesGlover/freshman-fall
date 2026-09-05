# CS 211 · Lab 9 — Solutions
## Instructor Only

**Do not distribute.** Every figure below was measured on the reference machine (Intel i5-8250U, 4 cores / 8 threads, gcc 13.3.0, OpenJDK 25.0.3). **Concurrency counts are probabilistic — orders of magnitude reproduce, exact numbers do not.** Mark on the order of magnitude and the reasoning.

---

## Running the Lab

**Budget:** A 25, B 30, C 25, D 20 = 100 minutes against 110.

**Check before the session:** `setarch $(uname -m) -R ./anything` must work, and TSan must run. Without `setarch` TSan aborts with `FATAL: ThreadSanitizer: unexpected memory mapping` on every machine in BH 220. **If students hit that cold in Q17 they will assume they broke something.** Say it at the front at the start of Part D.

**Three predictable stalls.**

**Q2 is anticlimactic if they run 20,000 iterations** and see zero. Tell them to use at least 200,000.

**Q5 is the one to protect.** Insist they write the prediction down *before* running. Most predict "fewer" — the answer is ~100× **more**, and the value of the question is entirely in having committed first. **The lecture made the same wrong prediction and says so**; if a student notices, that is the right response and worth saying aloud.

**Q6's `-O2` build hangs.** Some students will not use `timeout` and will sit staring at a terminal. Put the `timeout 5` on the board.

---

## Part A — The Impossible Outcome

**Q1.** Some thread's store executes first in the global order; that store precedes the other thread's load, so that load reads 1. No interleaving of the four operations has both loads reading 0.

**Q2.** Eight reference runs of 200,000: **71, 16, 20, 15, 31, 25, 11, 19.** One run on a loaded machine gave **378**.

**Not stable, and the spread is wide** — roughly 1 in 3,000 to 1 in 18,000, with outliers under load.

*Accept anything from single digits to a few hundred per 200,000. **Zero** means too few iterations or an idle-but-throttled machine; have them re-run at 500,000. Do not mark down a student whose numbers differ from the lecture's 44 — that is the point of the question.*

**Q3.** Order 0.01%, so roughly **1 run in 10,000** (range 3,000–18,000). A test suite exercising the case a hundred times a day sees it about **once every three months** — and when it does, it will not reproduce.

*The intended conclusion is not the exact number. It is that no amount of running the test changes the situation qualitatively, which is what sets up Q17.*

**The intended conclusion:** this class of defect is not reachable by testing. That sets up Q17.

**Q4.** **0 / 0 / 0** across three runs of 500,000 — 1.5 million iterations, never. The fence compiles to **`mfence`** (or a `lock`-prefixed instruction). It drains the store buffer: the store must be globally visible before the load may issue.

**Q5.** **Prediction almost always wrong.** Measured:

| | forbidden per 500,000 |
|---|---|
| padded | 73 / 50 / 26 |
| **unpadded** | **4574 / 8315 / 3258** |

About **100× more**, not fewer.

**Mechanism:** sharing a line makes it ping-pong between cores. Each store invalidates the other core's copy, so the following **load misses** and takes far longer — which *widens* the window during which the store is still in the buffer. **False sharing amplifies the reordering rather than hiding it.**

*The padded figure is the honest one to quote: a conservative rate for sensibly laid-out data. Full marks require the mechanism, not just the direction.*

---

## Part B — The Compiler Did It

**Q6.** `-O0` terminates. **`-O2` hangs.** `-O2 -DATOMIC` terminates.

**Q7.** Non-atomic at `-O2`:

```
        movl    ready(%rip), %eax     # load ONCE, before the loop
        testl   %eax, %eax
        jne     .L5
.L6:
        jmp     .L6
```

The two instructions are **`.L6:` and `jmp .L6`** — an unconditional infinite loop.

With `_Atomic`:

```
.L5:
        movl    ready(%rip), %eax     # load INSIDE the loop
        testl   %eax, %eax
        je      .L5
```

**The single difference is where the load is** — outside the loop against inside it.

**Q8.** **Loop-invariant code motion**, from Week 5.

**Not a bug in it.** LICM's precondition is that nothing in the loop modifies the value, which is true. The compiler is additionally entitled to assume no *other thread* modifies it, because a concurrent unsynchronised write would be a data race, and a racy program has no defined behaviour. **The optimisation is correct; the program was already broken before it ran.**

*Credit either conclusion if argued. Reject "the compiler should just not do that" with no engagement — L20 §1 is why that would forbid nearly every optimisation in Weeks 4–5.*

**Q9.** `-O2`: **4000000, 0.000 s.** `-O0`: 2251561 (43.7% lost) and 1465090 (63.4% lost).

The whole loop became:

```
        addq    %rax, plain_counter(%rip)
```

**What licensed it:** the source contains a data race, so it has **undefined behaviour**; the compiler may assume the race does not occur, and under that assumption the loop is a single addition.

**Q10.** *(Discussion.)* Draw out:

- **Both have the bug.** It is in the source, not in either build.
- `-O2` "working" is worse than `-O0` failing, because it removes the evidence while leaving the defect. A future compiler version, a different inlining decision, or a slightly different loop body brings it straight back.
- **What to do next:** stop bisecting optimisation levels and run TSan. The question is not which build is right but whether the program is race-free, and that is a different kind of question.

---

## Part C — Java, and the Actor Alternative

**Q11.** `plain`: still spinning after 3 s. `volatile`: done.

At `sleep(5)` the plain version **terminates** — the loop is still being interpreted, so the field is re-read each time. C2 has not compiled it yet.

**Implication:** a fast test passes and a warm production process hangs. **The bug appears only after the code gets hot**, which is precisely the code that matters.

**Q12.** With C `volatile` at `-O2` it **terminates**.

**It does not make the program correct.** C's `volatile` promises only that the compiler will not elide or reorder *volatile* accesses relative to each other; it says **nothing** about visibility to other threads, and provides **no happens-before edge**. It happens to defeat this particular hoist on this compiler. The `payload` read is still racy, and on a weakly-ordered machine the reader can see `ready == 1` with a stale `payload`.

*This is the most commonly mis-answered question in the lab. The two questions — "does it terminate" and "is it correct" — have different answers, and full marks require both.*

**Q13.** actor 80000 / 0.317 s / 252k per s; lock 80000 / 0.025 s / 3.24M; racy 80000 / 0.008 s / 10.2M.

**What you buy:** `self.count += 1` in `Counter.on` is executed by exactly one thread, ever. No lock appears in that class and no race is possible in it — not through misuse, not by a colleague, not in six months.

**Why the racy Python was right:** `sys._is_gil_enabled()` is `True`. The GIL makes bytecode interleaving coarse enough to hide it. **The same algorithm in C lost 44–63%.** The correctness came from the interpreter, not from the code — and free-threaded CPython removes it.

**Q14.** The lock is inside **`queue.Queue`**, which is internally synchronised.

**The claim is fair**, and the argument is that the lock is now written **once, by someone whose job it was, in one place**, instead of at every call site by everyone. **Accept the opposing view if argued** — that "no shared mutable state" is overstated when the mailbox plainly has some, and that the model's guarantee is about *your* code rather than the runtime's.

---

## Part D — The Machines We Do Not Have

**Q15.**

| reordering | x86-TSO | ARM / POWER |
|---|---|---|
| LoadLoad | no | **yes** |
| LoadStore | no | **yes** |
| StoreStore | no | **yes** |
| StoreLoad | **yes** | **yes** |

**Q16.** **StoreStore** would let `ready = 1` become visible before `payload = 42`.

**Not possible on x86** (StoreStore forbidden). **Possible on ARM.**

What to do: the honest answers are **(a)** use the language's atomics rather than relying on the hardware — release/acquire gives the edge on every architecture; **(b)** run a race detector, which checks happens-before rather than outcomes; **(c)** simulate the weak model with `herd7`/`litmus7`. *Accept any two.*

**Q17.** Without `setarch`: `FATAL: ThreadSanitizer: unexpected memory mapping`. With it:

```
WARNING: ThreadSanitizer: data race
  Read of size 8 ... by thread T2:  #0 w_plain orders.c:31
  Previous write of size 8 ... by thread T1:  #0 w_plain orders.c:31
  Location is global 'plain_counter' of size 8
SUMMARY: ThreadSanitizer: data race orders.c:31 in w_plain
```

On `hoist.c`: `data race hoist.c:35 in setter`.

Slowdown, 4 threads × 300k, whole program: **0.32–0.45 s → 2.86–3.22 s, about 9×.**

**Q18.** *(Discussion.)*

- TSan tracks the **happens-before relation** during one execution. It does not need the bad interleaving to occur — it observes two accesses with no edge between them and reports that, whatever order they happened in this run.
- **Earlier instances of the same move:** Week 5 replaced a guess about operand *shape* with a table of what each opcode *means*; Week 6 replaced peak RSS (a sample of an outcome) with residency (the property). *Accept Week 8's type checker as a third.*
- **Limits:** it reports races on code paths it **actually executed**. It does not explore schedules and it does not reason about paths not taken. A race behind an untaken branch is invisible to it.

---

## If You Finish Early

**Q19.** One-sided fencing: the forbidden outcome **returns**. Measured, fence in thread 0 only, per 500,000:

| | forbidden |
|---|---|
| no fence | 73 / 50 / 26 |
| **fence in one thread only** | **12 / 15 / 5** |
| fence in both | 0 / 0 / 0 |

Reduced by roughly a factor of five and **definitively not eliminated** — the unfenced thread's store can still sit in its buffer while its load proceeds. **A barrier is a property of the pair, not of one participant**, which is why release must be matched with acquire.

*The partial reduction is the interesting part: a student who fences one side, sees the count drop, and concludes it is fixed has made exactly the mistake this question exists to catch.*

**Q20.** `relaxed` still gives 4000000. **It should**, and this is one of the few genuinely correct uses: nothing is ordered *relative to* the counter, and the value is read once after all threads join — where the `join` supplies the happens-before edge. Push back on students who conclude "relaxed is fine then": change it to a flag guarding a payload and it breaks immediately.

**Q21.** The flag/payload pattern. On x86 they will likely **not** reproduce it, because the reordering required is StoreStore, which x86 forbids. **Saying so, and naming ARM, is the full-marks answer.** Anyone who claims to have reproduced it on x86 has almost certainly observed a compiler reordering rather than a hardware one — worth checking their assembly with them.

**Q22.** Under load the rate typically **rises** — more preemption, longer windows. The implication is that a loaded CI machine is a *better* race detector than a quiet laptop, and that "could not reproduce locally" is weak evidence. **This is still not a substitute for TSan**, and a student who says so has the point.

---

*CS 211 · Week 9 · Lab 9 Solutions · © CSE Department*
