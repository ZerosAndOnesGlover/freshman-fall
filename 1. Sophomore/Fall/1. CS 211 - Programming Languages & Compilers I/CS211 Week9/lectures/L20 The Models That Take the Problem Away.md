# CS 211 · Programming Languages & Compilers I
## Week 9 · Lecture 2 of 2
### The Models That Take the Problem Away

*“There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. The first method is far more difficult.”* — C. A. R. Hoare, "The Emperor's Old Clothes" (Turing Award lecture, 1980)

---

**Reading:** Manson, Pugh & Adve, "The Java Memory Model" (2005) · Batty et al. (2011) · Armstrong, "Making Reliable Distributed Systems" ch. 2 · **Next:** L21, domain-specific languages

**Coursework:** 📝 **PS 8** due Fri this week 17:00 · 🔬 **Lab 9** Fri this week 14:00–15:50 · 📊 **Quiz 10** Tue of Week 10 · 📝 **PS 10** released Wed of Week 10, due Fri of Week 11 17:00

---

## 1. A Memory Model Is a Contract

L19 left a mess: the hardware reorders, the compiler reorders more, and a data race means the specification stops making promises. A **memory model** is the document that says who owes what.

It has two readers and it binds both.

- **To the programmer** it says: *if you synchronise like this, you will observe that.*
- **To the compiler and the hardware** it says: *you may reorder anything the programmer cannot detect under those rules.*

That second clause is why memory models exist at all. Without one, every optimisation in Weeks 4 and 5 would be illegal on a multi-threaded program — because *some* thread might be watching. The model exists to say **which observers are entitled to complain.**

Everything below is a point on one axis: **how much ordering is guaranteed by default, and how much you must ask for.**

---

## 2. C11 and C++11: Ordering as a Parameter

C11 makes ordering an argument you pass:

```c
atomic_fetch_add_explicit(&counter, 1, memory_order_relaxed);
atomic_fetch_add_explicit(&counter, 1, memory_order_acq_rel);
atomic_fetch_add_explicit(&counter, 1, memory_order_seq_cst);   /* default */
```

| order | what it guarantees |
|---|---|
| `relaxed` | **atomicity only.** No happens-before edge at all. The operation will not tear; nothing else. |
| `acquire` (loads) | nothing after it in program order moves before it |
| `release` (stores) | nothing before it in program order moves after it |
| `acq_rel` | both, for read-modify-write |
| `seq_cst` | acq_rel **plus** a single global total order over all `seq_cst` operations |

The pairing that matters is **release/acquire**: a release store and the acquire load that *reads that value* create a happens-before edge, so everything the writer did before its release is visible to the reader after its acquire. That is the mechanism behind every correct flag-and-payload handoff, including the one `hoist.c` got wrong.

Measured, four threads incrementing one counter a million times each:

| mode | answer | time |
|---|---|---|
| `plain` (racy, `-O0`) | 1465090 of 4000000 | 0.032 s |
| `relaxed` | 4000000 | 0.126 s |
| `acq_rel` | 4000000 | 0.124 s |
| `seq_cst` | 4000000 | 0.141 s |
| `mutex` | 4000000 | 0.412 s |

Three things to read off that.

**`seq_cst` costs about 12% over `relaxed`** on this workload. That is the price of the global total order, and on x86 it is small because the hardware is already TSO — the same code on ARM would show a much larger gap, because more barriers have to be emitted to simulate the ordering x86 gives away.

**A mutex costs roughly 3.3× a `seq_cst` atomic.** For one increment, an atomic is strictly better. For a five-line critical section it is usually the other way, because the atomic version needs a retry loop and the mutex does not.

**The racy version is the fastest and it is the only wrong one.** Which is the honest summary of this entire week.

> **`relaxed` is the one to be careful with.** It is not "slightly weaker"; it provides *no
> ordering whatsoever*, and code using it is correct only if you have proved you need none. A
> counter that is read once at the end is the standard legitimate use. A flag that guards a
> payload is not, and that mistake is `hoist.c` with an `_Atomic` on it.

---

## 3. The Java Memory Model

Java made a different choice: **no ordering parameters.** You get a small set of constructs, each with a fixed meaning.

| construct | edge it creates |
|---|---|
| `volatile` write → read | release/acquire pair, plus participation in a total order |
| `synchronized` unlock → lock | release/acquire on the same monitor |
| `Thread.start()` | before everything in the new thread |
| thread end → `join()` returns | everything in the thread, before the join |
| `final` field, set in a constructor | visible to any thread that sees the reference, **without synchronisation** |

`volatile` is the one to understand, and its name is misleading — it is nothing like C's `volatile`, which promises only that the compiler will not elide the access and says **nothing** about other threads. Java's `volatile` is a full memory-model construct: it fixed `Hoist.java`, and C's `volatile` would not have fixed `hoist.c` in any portable way.

**The `final` row is the interesting one.** It exists so that immutable objects can be published safely without the publisher and the reader synchronising — which is what makes `String` and the `java.time` classes safe to share. **Immutability is a synchronisation strategy**, and §6 is that idea taken to its conclusion.

Two pieces of history worth knowing. The **original 1995 JMM was broken** — it made `final` fields mutable-looking and permitted optimisations that broke `String` — and was replaced by JSR-133 in Java 5. And the "double-checked locking" idiom that every Java textbook of the era recommended was **unfixably wrong** under the old model. That is what a bad memory model costs: not slow programs, but a decade of published advice that did not work.

---

## 4. Why We Cannot Show You the Interesting Case

The syllabus asks you to demonstrate memory-ordering bugs **on a weakly-ordered processor**. BH 220 has none. Every machine in this course is x86-64.

That is worth stating plainly rather than working around, because the gap is the lesson:

| | LoadLoad | LoadStore | StoreStore | **StoreLoad** |
|---|---|---|---|---|
| **x86-TSO** | no | no | no | **yes** |
| **ARM, POWER, RISC-V** | **yes** | **yes** | **yes** | **yes** |

L19 §3 measured the one x86 permits, and it was enough to break Dekker's algorithm. **The other three are the ones that make code fail when it moves.**

Concretely: the flag-and-payload handoff

```c
payload = 42;      /* StoreStore reordering would let these swap */
ready = 1;
```

is broken on ARM and *works by accident* on x86, because x86 forbids StoreStore. So a program written and tested exclusively on x86 can contain a real bug that no amount of x86 testing will ever reveal — and it appears the day it is built for an Apple M-series laptop or a Graviton server.

> **"It works on my machine" has a precise technical meaning here**, and it is the difference
> between two rows of that table. This is not a hypothetical: it is the single most common source
> of genuine bugs found during x86-to-ARM ports, and every large codebase that made that move in
> the last five years hit it.

*(PS 9 Part D asks you to reason about the ARM case without hardware, which is what the formal models are for — and `herd7`/`litmus7` from the Cambridge group will simulate it if you want to see the outcomes.)*

---

## 5. Locks, and What They Actually Give You

A mutex is usually taught as *mutual exclusion*: one thread in the critical section at a time. That is half of it, and the half that gets people into trouble.

The other half: **unlocking is a release and locking is an acquire.** A lock does not merely serialise access — it *publishes* everything the previous holder did. Take that away and mutual exclusion alone would not help, because the next thread could still be reading stale values.

Which explains a common bug shape. Protecting *writes* with a lock but reading without one gives you mutual exclusion among writers and **no happens-before edge to the readers at all**. The reads are still racy, and `hoist.c` is what happens next.

Costs, from §2: a mutex is ~3.3× a `seq_cst` atomic for one increment. Two further properties matter more than that ratio:

- **Locks do not compose.** Two individually correct locked operations combined are not automatically correct, and combining two lock orders is how deadlocks are built.
- **A lock is a claim about a *program*, not about *data*.** Nothing in the language ties a mutex to the data it protects — that association lives in comments and in your head. **Rust is the mainstream exception**: `Mutex<T>` *contains* the data, so accessing it without locking is a type error rather than a code review finding.

---

## 6. Take the Shared State Away

Every bug in L19 needed one precondition: **two threads reaching the same memory.**

So remove it. In the **actor model**, an actor owns its state, nothing else may touch it, and actors communicate by sending immutable messages to each other's mailboxes.

```python
class Counter(Actor):
    def on(self, msg):
        if msg.tag == 'inc':
            self.count += 1
```

**There is no lock in that class and there cannot be a race on `self.count`**, because exactly one thread ever executes `on`. No barrier to place, no memory order to choose, no happens-before to reason about.

Measured against the alternatives — 4 senders, 20,000 increments each:

| model | answer | time | throughput |
|---|---|---|---|
| actor (no shared state) | 80000 | 0.317 s | 252,000/s |
| shared + lock | 80000 | 0.025 s | 3,236,000/s |
| shared, no lock | 80000 | 0.008 s | 10,224,000/s |

**The actor model is about 13× slower than a lock here**, and the argument for it is not speed. It is that the counter class cannot be misused — not by you, not by a colleague, not in six months.

Two honesty notes on that table.

**The locking did not disappear; it moved.** `actors.py` uses a `queue.Queue`, which locks internally. What changed is that the lock is written once, by someone whose job it was, inside a mailbox — instead of appearing at every call site written by everyone. **That relocation is the whole engineering argument**, and it is a relocation, not an elimination.

**The racy row got the right answer, and that is an accident.** CPython 3.14 here is a GIL build (`sys._is_gil_enabled()` is `True`), so bytecode-level interleaving is coarse enough to hide the race. The *identical algorithm* in C lost 44–63% of its updates (L19 §6). **The same logic is safe in one language by accident of its interpreter and catastrophically wrong in another** — and the free-threaded builds arriving in CPython 3.13+ remove the accident.

This is what Go means by *"Do not communicate by sharing memory; share memory by communicating."* Go channels, Erlang and Elixir processes, and Akka actors are all this design; Erlang adds per-process heaps and supervision trees, which is why telecoms switches were written in it.

---

## 7. Two More Models, Briefly

**Software transactional memory.** Mark a block atomic and let the runtime handle it: read and write freely, and on conflict the transaction rolls back and retries.

```haskell
atomically $ do
  a <- readTVar from
  writeTVar from (a - n)
  ...
```

The property locks lack: **STM composes.** Two atomic blocks combined are still atomic. The costs are that every read and write is logged, rollback requires the block to be free of side effects — which is why STM works in Haskell, where the *type system* enforces that — and pathological contention causes livelock.

**async/await.** Not parallelism at all: one thread, many suspended computations, an event loop resuming whichever is ready. `await` marks a point where the function may be suspended.

**Because there is one thread, there are no data races** — Python's `asyncio`, JavaScript, and single-threaded Rust executors all get that for free. What you get instead is that *every* `await` is a place where other code runs, so an invariant broken across an `await` is visible to everyone. **The interleaving points became explicit and rare rather than implicit and everywhere**, which is a genuine improvement and not a solution: `async` buys concurrency, not parallelism, and a CPU-bound task still blocks the loop.

---

## 8. The Tooling, and Its Limits

You cannot test your way to race freedom — L19 §3's bug appeared 0.02% of the time. **ThreadSanitizer** is the tool that changes that, by tracking happens-before at run time rather than sampling outcomes.

```
$ setarch $(uname -m) -R ./orders_tsan 2 20000
WARNING: ThreadSanitizer: data race (pid=333015)
  Read of size 8 at 0x555555558050 by thread T2:
    #0 w_plain orders.c:31
  Previous write of size 8 at 0x555555558050 by thread T1:
    #0 w_plain orders.c:31
  Location is global 'plain_counter' of size 8
SUMMARY: ThreadSanitizer: data race orders.c:31 in w_plain
```

**The exact line, the exact variable, both stacks.** It found `hoist.c:35` the same way.

Three practical notes:

- **It costs about 9×** — 0.32–0.45 s became 2.86–3.22 s on the same workload. That is a CI configuration, not a development default.
- **On this machine it will not start** without disabling ASLR: `FATAL: ThreadSanitizer: unexpected memory mapping`. The fix is `setarch $(uname -m) -R`, and it is a real prerequisite rather than a footnote.
- **It reports races it observes**, not races that exist. It does not explore schedules. A race on a path you did not execute is a race it did not find.

> **It is still the single most effective tool in this week.** L19's bug is invisible to testing
> and obvious to TSan, because TSan is checking the *happens-before relation* rather than the
> *outcome* — the same move as Week 5's liveness table replacing a guess about operand shape.
> **Check the property, not a sample of the results.**

---

## 9. What to Take From This

1. **A memory model binds two parties.** It tells you what you may assume and tells the compiler what it may reorder — and without one, every Week 4–5 optimisation would be illegal.
2. **C11 makes ordering a parameter.** `relaxed` gives atomicity and *nothing else*; release/acquire is the pairing that publishes a payload.
3. **Measured: `seq_cst` costs ~12% over `relaxed`, a mutex ~3.3× a `seq_cst` atomic** — and the racy version is fastest and wrong.
4. **Java fixes the meanings instead of parameterising them.** Its `volatile` is a memory-model construct; C's is not, and confusing them is a real bug.
5. **A broken memory model cost Java a decade of wrong published advice** about double-checked locking.
6. **x86 forbids three of the four reorderings ARM allows**, so a genuine bug can be untestable on x86 and appear on the first ARM build.
7. **A lock publishes as well as excludes** — protecting writes but not reads gives mutual exclusion and no visibility.
8. **Actors remove the precondition rather than managing it**, at ~13× the cost here — and the locking moved into the mailbox rather than vanishing.
9. **The racy Python got the right answer because of the GIL**, while identical C logic lost 63%.
10. **TSan checks happens-before, not outcomes**, costs ~9×, needs `setarch -R` here, and finds in one run what testing will not find in a year.

**Next week the compiler becomes the subject again**, and concurrency's lesson carries: a domain-specific language is a way of making a class of mistake unwriteable, which is exactly what §6 did.

---

*CS 211 · Week 9 · Lecture 20 · © CSE Department*
