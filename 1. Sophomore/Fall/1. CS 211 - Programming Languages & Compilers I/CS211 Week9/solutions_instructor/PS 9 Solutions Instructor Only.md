# CS 211 · Problem Set 9 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** Measured on the reference machine (Intel i5-8250U, 4 cores / 8 threads, gcc 13.3.0, OpenJDK 25.0.3, CPython 3.14.2 with the GIL).

> **Concurrency figures are probabilistic.** Mark on order of magnitude and reasoning, never on
> exact counts. A student reporting 8 forbidden outcomes where the reference says 44 has done the
> experiment correctly.

---

## Part A — Reproducing the Impossible (18)

**A1.** *(5 — 2 counts, 2 the SC argument, 1 the fence)*

Reference: 44 per 200,000 (0.0220%); 73 / 50 / 26 per 500,000. With `fence`: **0 across all runs**.

The SC argument: some thread's store is first in the global order, so it precedes the other thread's load, so that load reads 1. **Full marks require the argument to be about the global order**, not an enumeration with a hand-wave.

**A2.** *(5 — 1 prediction recorded, 2 counts, 2 mechanism)*

| | per 500,000 |
|---|---|
| padded | 73 / 50 / 26 |
| unpadded | **4574 / 8315 / 3258** |

**~100× MORE, not fewer.** Mechanism: the shared line ping-pongs between cores; each store invalidates the other core's copy; the following **load misses** and takes much longer; the window in which the store is still buffered is correspondingly wider.

**Award the prediction mark for having written one down, right or wrong.** The lecture records its own wrong prediction for this reason. Quote the padded figure as "how often this happens" — it is the conservative one, for data laid out sensibly.

**A3.** *(4)*

Old: >120 s / 20,000 = **>6 ms per iteration**, essentially all `pthread_create` + `join`. New: 0.28 s / 500,000 ≈ **0.6 µs**. Four orders of magnitude.

The barrier exists because **both threads must be inside the same iteration** for a window to exist. Without it they drift apart and one finishes its pair before the other starts; the forbidden rate collapses toward zero. *Require that they tested it.*

**A4.** *(4)*

`mfence` (gcc may emit `lock orq $0, (%rsp)` instead). It prevents the load from issuing until the store buffer has drained.

**Why a locked instruction may be preferred:** on many Intel parts `lock`-prefixed RMW on an already-hot stack line is **cheaper than `mfence`**, which is a heavier serialising operation. *Accept the argument without a measurement; credit any student who measures it.*

---

## Part B — The Compiler Is the Problem (22)

**B1.** *(6)* `-O0` terminates, `-O2` **hangs**, `-O2 -DATOMIC` terminates. The two instructions: **`.L6:` / `jmp .L6`**. With `_Atomic`, the `movl` moves **inside** the loop at `.L5`.

**Loop-invariant code motion**, Week 5. **Not a bug**: LICM's precondition holds, and the compiler may additionally assume no other thread writes `ready`, because that would be a data race and a racy program has no defined behaviour.

**B2.** *(6)*

`-O2`: the loop became `addq %rax, plain_counter(%rip)` — correct answer, 0.000 s.
`-O0`: 2251561 (43.7% lost) / 1465090 (63.4% lost).

**What licensed it:** the source has a data race, therefore **undefined behaviour** — the standard makes *no requirement whatsoever* on such a program, so the compiler may assume the race does not occur. **Reject "the result is unpredictable"**: that is precisely what the standard does *not* say, and the distinction is the marked point.

Why `-O2` working is worse: it hides the defect while leaving it in the source, so it returns with a compiler upgrade, a different inlining decision or a new call site — and the evidence is gone.

**B3.** *(5 — 2 volatile, 1 barrier, 2 the standard)*

C `volatile` at `-O2`: **terminates**. **It does not make the program correct.** C's `volatile` constrains only the compiler's treatment of volatile accesses relative to one another; it creates **no happens-before edge** and says nothing about other threads. The `payload` read remains racy, and on ARM the reader can see `ready == 1` with a stale `payload`.

A `printf` or `asm volatile("" ::: "memory")` also stops the hoist — a compiler barrier, not a memory barrier, so the same objection applies.

*The two questions have different answers. Full marks need both.*

**B4.** *(5)*

`plain`: still spinning after 3 s. `volatile`: done. At `sleep(5)` the plain version **terminates**, because the loop is still interpreted and C2 has not compiled it.

**Implication:** the failure requires the code to be *hot*, which is exactly the code that matters and exactly what a fast test suite does not produce.

Java's `volatile`: a memory-model construct giving release/acquire plus a total order. C's `volatile`: a compiler directive about elision and reordering of volatile accesses, with **no** inter-thread guarantee.

---

## Part C — Build the Actor System (36)

Mark behaviour, not architecture.

**C1.** *(8)* A correlation id (or a per-`ask` reply mailbox) is required; a shared reply queue is the wrong answer and must be caught by their own four-concurrent-`ask` test. Timeout: raising, or returning a sentinel, are both defensible — **require a justification**, and require that a late reply does not corrupt a subsequent `ask`.

**C2.** *(8)* Restart must give **fresh state** — a supervisor that catches and continues with the corrupted actor has missed the point. Expect ~33 failures and ~33 restarts over 100 messages, with the failing message lost each time.

"Let it crash" is reasonable **because the actor's state is private**: discarding and rebuilding it cannot corrupt anything else. In a shared-memory design a thread dying mid-update leaves shared invariants broken and locks held, so crashing is not recoverable.

**C3.** *(10)* **There may be no crossover in CPython, and saying so with numbers is full marks.** With the GIL, CPU-bound stages do not run in parallel, so the pipeline adds message overhead without adding throughput. The crossover appears if the work is I/O-bound or releases the GIL. **Reject any claimed crossover unsupported by a table.**

**C4.** *(6)* With the GIL, list `append` is effectively atomic and the corruption is hard to show; a `read-modify-write` on an element (`lst[0] += 1`) can be made to fail. **A precise account of why it cannot be demonstrated, plus what a free-threaded build would do, is full marks.**

The invariant is **immutability of messages** (equivalently: no shared mutable state). Erlang enforces it by copying every message between processes; Rust enforces it in the type system, with `Send`/`Sync` and ownership transfer. Either answer.

**C5.** *(4)* The lock is inside **`queue.Queue`**. **Accept either verdict, argued.** For: written once, in one place, by someone whose job it was, instead of at every call site. Against: "no shared mutable state" is overstated when the mailbox has some, and the guarantee is really about *user* code.

---

## Part D — Weak Memory Without the Hardware (12)

**D1.** *(6 — 2 table, 3 the three programs, 1 the handoff)*

| | LoadLoad | LoadStore | StoreStore | StoreLoad |
|---|---|---|---|---|
| x86-TSO | no | no | no | **yes** |
| ARM/POWER | yes | yes | yes | yes |

The handoff is broken by **StoreStore**: `ready = 1` becomes visible before `payload = 42`, so the reader sees the flag with a stale payload. The missing edge is a **release** on the store to `ready` paired with an **acquire** on the load.

**D2.** *(6)*

Testing on x86 can establish that the program does not exhibit x86-permitted reorderings; it **cannot** establish anything about the three x86 forbids, because the hardware never produces them regardless of how long you run.

Two techniques: **(a)** a race detector such as TSan, which checks happens-before rather than outcomes, at ~9× runtime; **(b)** a memory-model simulator such as `herd7`/`litmus7`, which explores the ARM model exhaustively for small tests, at the cost of only handling small tests. *(Accept "use the language's atomics and rely on the compiler to emit the right barriers per target" as a third.)*

The colleague's proposal: **load and core count change the probability of x86-permitted interleavings and do nothing whatever about reorderings x86 does not perform.** No amount of x86 stress testing samples an outcome the hardware cannot produce. It is a reasonable way to find *other* races and no evidence at all about portability.

---

## Part E — Written (12)

**E1.** *(6)*

Guarantees, weakest to strongest: relaxed atomics → locks → STM ≈ actors *(accept variations, argued)*. Cost, cheapest to dearest: atomics (0.126–0.141 s) → locks (0.412 s) → actors (~13× locks) → STM.

**They differ** because actors and STM buy *composability and isolation*, which is a property of the program's structure rather than of an individual operation.

**Compose:** two locked operations combined are not automatically atomic. Transferring between accounts: `withdraw(a)` and `deposit(b)` are each correct under locks, and the pair is not — another thread can observe the money in neither account. Under STM, `atomically $ withdraw a >> deposit b` is atomic by construction.

**Haskell's property: purity, enforced by the type system.** STM requires that a rolled-back transaction leaves no trace, which requires the block be free of irrevocable side effects — and `STM` being a distinct monad from `IO` is what makes that checkable rather than a convention.

**E2.** *(6)*

**What is different in kind:** Weeks 4–7's defects were deterministic — same input, same wrong answer, every time. This one's *visibility* depends on the optimisation level, so the ordinary debugging move (turn optimisation down, get better information) **changes whether the bug exists at all**. Bisection on `-O` levels finds nothing, because both builds are consequences of the same broken source.

**Two earlier instances of checking the property rather than the outcomes:** Week 5's `SLOTS` table replacing a guess about operand shape; Week 6's residency replacing peak RSS. *(Week 8's type checker is a third.)*

**In CI:** a TSan build of the test suite (~9×, so a separate job); and atomics/locks used correctly rather than relied upon by observation. **Running the tests more times is not on the list** because the failure rate is ~1 in 5,000 and non-reproducible: multiplying the runs multiplies the cost linearly and the confidence hardly at all.

---

## Overall

**Expected distribution:** A and B should be high — they are reproduction with careful reading. **Part C is the assessment**, and C3 and C4 are where honest negative results separate students who ran the experiment from students who described one.

**Two failure modes:**

1. **Fabricated positives in C3/C4.** A claimed crossover with no table, or a claimed race demonstration under the GIL. Ask to see the numbers.
2. **B2 answered as "unpredictable".** The standard says the program has *no* behaviour, which is a stronger and different claim, and it is what licensed deleting the loop.

---

*CS 211 · Week 9 · PS 9 Solutions · © CSE Department*
