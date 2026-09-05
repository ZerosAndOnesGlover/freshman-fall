# CS 211 · Problem Set 9
## A Mini Actor System

---

**Released:** Week 9, Wednesday · **Due:** Week 10, Friday 17:00
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `actors.py` and any new modules (runnable end to end), your modified `.c` files, and `ps9.md` (written answers, tables, traces). Written answers inside code comments will not be marked.

> **Project 1 is due Week 11, the Friday after this problem set.** If you are not yet running under
> `--gc=none`, deal with that first — this problem set is worth 100 marks and the project is worth
> 12.5% of the course.

Start from the Week 9 lab folder. `litmus.c`, `orders.c`, `hoist.c`, `Hoist.java` and `actors.py` are given to you complete.

---

## Part A — Reproducing the Impossible (18 points)

**A1.** *(5)* Build and run the store-buffer litmus test.

- Report the four outcome counts and the percentage of forbidden outcomes, over at least **three runs of 500,000 iterations**.
- **Write the sequential-consistency argument out**, in your own words: enumerate enough interleavings to show `r1 == 0 && r2 == 0` cannot occur under SC.
- Now run with `fence` and report. How many forbidden outcomes across all your runs?

**A2.** *(5)* `litmus.c` pads `x` and `y` onto separate cache lines.

- **Predict, before running:** does removing the padding make the forbidden outcome more or less frequent? Write your prediction and your reasoning down first.
- **Remove the padding**, rebuild, and report the counts over three runs of 500,000.
- The change is about two orders of magnitude. **Explain the mechanism at the hardware level** — what happens to the shared line, and what that does to the duration of the load.
- Which of the two configurations should be quoted as "how often this happens", and why? In two sentences, say what this implies about performance numbers that were produced without checking the data layout.

**A3.** *(4)* The first version of `litmus.c` created two threads per iteration and took over two minutes for 20,000 iterations; the shipped version does 500,000 in under half a second.

- Estimate the per-iteration cost of `pthread_create` from those figures.
- Explain why the shipped version needs a **barrier** at all, and what would happen to the forbidden-outcome rate without one. Test your prediction.

**A4.** *(4)* Disassemble the fenced and unfenced versions:

```
gcc -O2 -pthread -S -o - litmus.c | less
```

- Find the instruction the `seq_cst` fence compiled to. Name it.
- Explain what it does to the store buffer.
- x86 also gives that ordering as a side effect of any `lock`-prefixed instruction. **Why might a compiler prefer `lock addq $0, (%rsp)` to `mfence`?** *(Measure if you can; a defensible argument scores full marks without a measurement.)*

---

## Part B — The Compiler Is the Problem (22 points)

**B1.** *(6)* Reproduce the three `hoist.c` results (`-O0`, `-O2`, `-O2 -DATOMIC`) and give the outcome of each.

- Disassemble the `-O2` reader and quote the two instructions that make it an infinite loop.
- Quote the corresponding `-O2 -DATOMIC` assembly and say precisely what changed.
- **Name the Week 5 optimisation responsible**, and explain why it is not a bug in that optimisation.

**B2.** *(6)* `orders.c` at `-O2` reports the racy version as **correct, in 0.000 s**.

- Disassemble `w_plain` at `-O2` and quote what the loop became.
- Run the same binary built at `-O0`, three times, and report the losses.
- **Explain what licensed the `-O2` transformation.** Your answer must use the phrase *undefined behaviour* correctly, and must say what the standard actually claims — not "the result is unpredictable".
- In two sentences: why is "it works at `-O2`" a worse situation than "it fails at `-O0`"?

**B3.** *(5)* Try to fix `hoist.c` **without** `_Atomic`:

- Attempt 1: declare `ready` as C `volatile`. Does it terminate at `-O2`? Does that make the program correct? *(Careful: these are different questions, and the honest answer to the second is not the same as the first.)*
- Attempt 2: put a `printf` or an empty inline-asm barrier in the loop body. Report what happens.
- **Neither is a portable fix.** Explain why, referring to what the C standard says `volatile` guarantees about *other threads*.

**B4.** *(5)* Run `Hoist.java` both ways.

- Report both outcomes.
- The plain version terminates if you set `Thread.sleep` to 5 ms instead of 300 ms. **Explain why**, and say what that implies about testing.
- Java's `volatile` fixed it and C's would not. **State the difference between the two keywords in one sentence each.**

---

## Part C — Build the Actor System (36 points)

`actors.py` gives you `Actor`, `Message`, a `Counter` and a benchmark. Extend it.

**C1.** *(8)* **Request/reply with correlation.**

- Add an `ask(actor, msg, timeout)` helper that sends a message and blocks until a reply arrives, returning it.
- Replies must be **correlated**: two concurrent `ask`s to the same actor must not receive each other's answers. Say how you did it.
- Show it working with at least four concurrent `ask`s.
- **What happens on timeout?** Implement something defensible and justify it.

**C2.** *(8)* **Supervision.**

- Make an actor that raises an exception in `on` restart with fresh state rather than killing the process.
- Add a `Supervisor` actor that owns children, restarts them on failure, and gives up after *N* restarts in a window.
- Demonstrate: an actor that fails every third message, supervised, processing 100 messages. Report how many were lost and how many restarts occurred.
- **Erlang's slogan is "let it crash".** Explain in two sentences what makes that reasonable *here* and unreasonable in a shared-memory design.

**C3.** *(10)* **A pipeline, and a measurement.**

- Build a three-stage pipeline of actors: source → transform → sink.
- Measure throughput for messages of increasing work per message — say 0, 10, 100 and 1000 µs of computation.
- Compare against a single-threaded loop doing the same total work.
- **Find the crossover**: the work-per-message at which the actor pipeline beats the sequential loop. Report it and explain what determines it.
- **If there is no crossover on your machine, say so and explain why** — that is a real result and scores full marks.

**C4.** *(6)* **Break the model deliberately.**

- Pass a **mutable** object in a message — a list — and have both sender and receiver modify it.
- Show that the race is back. Demonstrate it, or explain precisely why CPython's GIL prevents you from demonstrating it and what would happen without it.
- **State the invariant the actor model relies on** that this violates, and say what a language would have to enforce to make the violation impossible. *(Rust and Erlang give different answers; either is fine.)*

**C5.** *(4)* `actors.py`'s docstring claims the locking "has not gone away — it has been moved into the mailbox".

- Find the lock. Where is it?
- **Is the claim fair?** Argue for or against, in a paragraph.

---

## Part D — Weak Memory Without the Hardware (12 points)

**D1.** *(6)* This machine is x86-64. The interesting reorderings are not available.

- Give the four reordering categories and say which x86 permits.
- For **each** of the three x86 forbids, write a short two-thread program whose behaviour would differ on ARM, and state the outcome that becomes possible.
- Take the flag-and-payload handoff from `hoist.c`. **On ARM it is broken even with `_Atomic` replaced by a plain store, for a reason x86 hides.** Name the reordering and say what edge is missing.

**D2.** *(6)* You are asked to certify that a codebase tested only on x86 is safe to ship on ARM.

- Say what testing can and cannot establish here.
- Name **two** techniques that address what testing cannot, and say what each one costs. *(One of them is in this week's lab.)*
- A colleague proposes running the x86 test suite under heavy load and on many cores instead. **Respond**, in three sentences.

---

## Part E — Written (12 points)

**E1.** *(6)* Four models were measured or described this week: locks, atomics, actors, and STM.

- Put them in order of **what they guarantee**, and separately in order of **what they cost**. The orders are not the same; say where they differ.
- **Locks do not compose and STM does.** Explain what "compose" means here with a concrete example of two operations that combine correctly under STM and incorrectly under locks.
- Name the property of Haskell that makes STM practical there and impractical in C.

**E2.** *(6)* L19 §6 showed a data race that the optimiser removed by deleting the loop.

- Weeks 4 through 7 each contained a silent failure. **This week's is different in kind.** Say how — what is different about a defect whose visibility depends on the optimisation level?
- ThreadSanitizer finds these by checking **happens-before** rather than by checking outcomes. Name two earlier places in this course where a similar move — checking the property rather than sampling the results — was the fix.
- In two sentences: what would you put in a CI pipeline for a concurrent C codebase, and why is running the tests more times not on your list?

---

## Reference Numbers

From the machine these notes were prepared on (Intel i5-8250U, 4 cores / 8 threads, x86-64, gcc 13.3.0, OpenJDK 25.0.3). **Counts vary between runs; orders of magnitude do not.**

| Measurement | Value |
| --- | --- |
| `litmus 200000` forbidden outcomes | **44** (0.0220%) |
| `litmus 500000`, three runs | 73 / 50 / 26 |
| `litmus 500000 fence`, three runs | **0 / 0 / 0** |
| `hoist.c` at `-O0` / `-O2` / `-O2 -DATOMIC` | terminates / **hangs** / terminates |
| `-O2` reader assembly | `.L6: jmp .L6` |
| `orders 4 1000000` plain at `-O2` | **4000000, 0.000 s** — the loop became one `addq` |
| `orders 4 1000000` plain at `-O0` | 2251561 (43.7% lost), 1465090 (63.4% lost) |
| `relaxed` / `acq_rel` / `seq_cst` / `mutex` | 0.126 / 0.124 / 0.141 / 0.412 s |
| `java Hoist plain` / `volatile` | still spinning after 3 s / done |
| TSan on `orders.c` | `data race orders.c:31 in w_plain` |
| TSan slowdown, whole program | 0.32–0.45 s → 2.86–3.22 s, **~9×** |
| `actors.py 4 20000` | actor 252k/s, lock 3.24M/s, racy 10.2M/s |

**ThreadSanitizer will not start on these machines without `setarch $(uname -m) -R`.** That is a prerequisite, not a footnote.

---

## A Note on Parts C3, C4 and D2

Each asks you to report something that may not be there.

C3 asks for a crossover that **may not exist on your machine** — Python's threading and the GIL may mean the actor pipeline never wins. Say so, with the numbers, and explain why.

C4 asks you to demonstrate a race that **CPython's GIL may hide**. `sys._is_gil_enabled()` will tell you which build you have. A careful account of why you *cannot* demonstrate it, plus what would happen on a free-threaded build, is worth full marks.

D2 asks you to give professional advice, and the honest advice includes admitting what cannot be established.

**As in every problem set this term: a careful negative result scores full marks and a fabricated positive one scores zero.** This week that rule matters more than usual, because concurrency bugs are probabilistic and it is genuinely tempting to run something until it gives the answer you wanted. **If you had to run it forty times to see it once, report that you ran it forty times.**

---

*CS 211 · Week 9 · Problem Set 9 · © CSE Department*
