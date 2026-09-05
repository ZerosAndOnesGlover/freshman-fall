# CS 211 · Reading Guide · Week 9
## Concurrency in Programming Languages

**Read one paper properly this week rather than four chapters badly.** The concurrency literature is unusual in that the primary sources are better than the textbooks — shorter, sharper, and written by people who had just found the problem.

---

## Before Tuesday (L19 — what concurrent code means)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Adve & Boehm (2010)** | all | "Memory Models: A Case for Rethinking Parallel Languages and Hardware." *CACM.* **The single best entry point.** Says why sequential consistency was abandoned and what replaced it. | 8 |
| **Boehm (2005)** | §1–4 | "Threads Cannot Be Implemented as a Library." The argument that a compiler which does not know about threads will break them — which is `hoist.c`. | 8 |
| **Dragon** | **§11.4** | Data dependence and legal reorderings. Thin on concurrency, but it is the compiler-side vocabulary. | 6 |

---

## Before Thursday (L20 — the models)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Sewell et al. (2010)** | §1–3 | "x86-TSO: A Rigorous and Usable Programmer's Model." **§2 is the store buffer, formally, and it is exactly `litmus.c`.** | 10 |
| **Manson, Pugh & Adve (2005)** | §1–2, §5 | "The Java Memory Model." Why the 1995 model was broken and what JSR-133 replaced it with. | 12 |
| **Armstrong (2003)** | ch. 2 | Erlang's thesis: concurrency-oriented programming, and why processes share nothing. Readable, opinionated, and the origin of "let it crash". | 14 |
| **cppreference** | `memory_order` | Not a paper, but the clearest per-order statement in existence. **Read the release/acquire section twice.** | 4 |

---

## Papers, If You Want Them

- **Lamport (1979)**, "How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs." Two pages, and it is where sequential consistency is defined.
- **Batty et al. (2011)**, "Mathematizing C++ Concurrency." The formalisation that found real bugs *in the standard*.
- **Harris, Marlow, Peyton Jones & Herlihy (2005)**, "Composable Memory Transactions." STM, and the composability argument in L20 §7.
- **Dijkstra (1965)** on the mutual exclusion problem, if you want to see the algorithm `litmus.c` breaks in its original form.

---

## Tools

- **`herd7` and `litmus7`** (`diy.inria.fr`) — the Cambridge/INRIA tools that *simulate* ARM and POWER memory models. **This is how you answer PS 9 Part D without ARM hardware**, and it is what the model papers were written to support.
- **ThreadSanitizer**: `clang.llvm.org/docs/ThreadSanitizer.html`. Note the ASLR caveat — on these machines you need `setarch $(uname -m) -R`.
- **`jcstress`** — the JDK's concurrency stress harness. Overkill for this course, but it is what the JMM people actually use, and its test catalogue is an education by itself.

---

## The One Thing Worth Reading Twice

**Adve & Boehm §3, on why data races must be undefined behaviour.**

Read it, then run:

```bash
gcc -O2 -pthread -o orders orders.c && ./orders 4 1000000     # plain: correct, 0.000 s
gcc -O0 -pthread -o o0 orders.c     && ./o0 4 1000000          # plain: 63% lost
```

The paper argues that defining race behaviour would forbid nearly every optimisation, because the compiler would have to assume any thread might observe any intermediate state. **The experiment shows what the alternative buys and costs in one pair of runs:** at `-O2` the entire loop became a single `addq` and the answer came out right; at `-O0` two thirds of the increments vanished.

Most treatments present undefined behaviour as a wart. It is a deliberate trade, the paper says what was bought with it, and seeing the traded-away optimisation *actually happen* is the difference between having read §3 and having understood it.

---

## A Note on What Is Different About This Week

Every previous week had a property you could check. A grammar is ambiguous or it is not; a type checks or it does not; an object is reachable or it is not. You wrote the checker and ran it.

**This week the property is about executions that did not happen.** A program is race-free if *no* execution has two conflicting concurrent accesses — over all schedules, all thread interleavings, all optimisation levels, and all architectures. You cannot enumerate those, and testing samples them at a rate L19 §3 measures as one in five thousand.

That is why the tooling looks different. ThreadSanitizer does not run your program many times hoping to hit the bad schedule; it watches **one** execution and checks the *happens-before relation*. Same move as Week 5 replacing a guess about operand shape with a table of what each opcode means, and Week 6 replacing peak-RSS with residency: **check the property, not a sample of the outcomes.**

If you take one habit from this week, that is the one.

---

*CS 211 · Week 9 · Reading Guide · © CSE Department*
