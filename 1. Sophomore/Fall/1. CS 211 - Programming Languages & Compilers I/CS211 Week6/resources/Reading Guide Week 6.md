# CS 211 · Reading Guide · Week 6
## Runtime Systems: Memory Management

**Read against a question.** This week has more good writing available than any other in the course — garbage collection is unusually well documented — and that is a trap, because you could read for a fortnight. Each entry below says what to get out of it and roughly what it costs.

---

## Before Tuesday (L13 — the heap, manual free, reference counting)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Dragon** | **§7.4** | Heap management, allocation strategies, fragmentation. The part the Dragon Book does best on this topic. | 8 |
| **Dragon** | **§7.5** | Introduction to garbage collection: reachability, the mutator/collector split, and the design criteria. **Read §7.5.2 on reachability twice** — it is the definition L13 §11 is built on. | 10 |
| **Appel** | **ch. 13.1–13.3** | Mark-and-sweep and reference counting, shorter and more concrete than the Dragon. If §7.5 does not land, come here first. | 12 |
| **GC Handbook** | **ch. 5** | Reference counting, properly: the cycle problem, deferred counting, and why it is not the naive option. | 20 |

**Skip for now:** the Dragon's §7.6.4 onwards on short-pause collection — L14 gets there, and it reads much better once you have seen a pause measured.

---

## Before Thursday (L14 — roots, generations, barriers)

| Source | Section | Why | Pages |
|---|---|---|---|
| **GC Handbook** | **ch. 9** | Generational collection. **The best single chapter on this week's material in any book.** Read it with `collect.py`'s `Generational` open beside you. | 22 |
| **GC Handbook** | **ch. 11** | The run-time interface: stack maps, safepoints, conservative vs precise, interior pointers. **This is L14 §2 and §5 in full.** | 25 |
| **Appel** | **ch. 13.4–13.7** | Generations, incremental collection, and the compiler interface, in a fraction of the pages. | 14 |
| **Dragon** | **§7.7** | Short-pause collection: incremental and concurrent. Read it for the tri-colour invariant argument in §7.7.1. | 8 |

---

## Papers, If You Want Them

None are required. All three are short, readable, and are the actual source of what you implemented.

- **Ungar, D. (1984), "Generation Scavenging."** *SIGPLAN Notices* 19(5). The paper that made generational collection standard. Twelve pages, and every idea in `collect.py`'s `Generational` is in it, including the remembered set.
- **Bacon, D. & Rajan, V. (2001), "Concurrent Cycle Collection in Reference Counted Systems."** The answer to L13 §8 — how to find cycles *without* a full tracing collector. Read it if PS 6 Part C3 annoyed you, which it should have.
- **Boehm, H. & Weiser, M. (1988), "Garbage Collection in an Uncooperative Environment."** Conservative collection for C. The paper behind L14 §5, and worth reading for the engineering honesty about what "uncooperative" costs.

**And one blog post, which is better than it sounds:** Boehm's *"Destructors, Finalizers, and Synchronization"* argument that finalizers are a design error. PS 6 E2 is standing next to this.

---

## Runtime Documentation

You will read real GC logs in Lab 6. Two pages worth having open:

- **`docs.oracle.com` — "HotSpot Virtual Machine Garbage Collection Tuning Guide."** Skim the collector descriptions; ignore the tuning advice for now.
- **The `-Xlog` unified logging reference.** Specifically, what `gc`, `gc+phases` and `safepoint` each report. **Read this after Lab 6 Q7, not before** — the point lands much harder once you have been misled by the default.

For CPython: **`docs.python.org/3/library/gc.html`**, and the "Design of CPython's Garbage Collector" page in the developer guide, which is unusually candid about the incremental collector introduced in 3.13.

---

## The One Thing Worth Reading Twice

**GC Handbook ch. 11 §11.1–11.2, on stack maps and safepoints.**

Read it, then run `python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=week4` and watch the collector free an object the next instruction writes through.

The chapter tells you the collector is *given* its root set by the compiler. **It does not dwell on the consequence, which is that the collector has no way to check it** — there is no assertion, no cross-validation, and no test that fails. A wrong stack map is a silent memory-safety bug in a memory-safe language, and noticing that is the difference between having read the chapter and having understood it.

---

## A Note on Where This Week Sits

Every previous week of this course was about a **representation**: a token stream, a tree, an IR, a graph. This week is the first that is about a **process** — something that happens while the program runs, that the program cannot see, and that has to be correct with respect to a state neither the compiler nor the collector has complete information about.

That is why the reading feels different. Chapters on parsing are about structures you can draw. Chapters on collection are about *invariants over time*, and the ones that matter here are two:

- **A count of zero implies unreachable** — reference counting's invariant, which is true and insufficient.
- **No black object points to a white object** — tracing's invariant, which is what every barrier in ch. 15 exists to preserve.

**If you keep those two sentences straight, the whole literature organises itself around them.** If you do not, chapter 9 reads as a list of tricks.

---

*CS 211 · Week 6 · Reading Guide · © CSE Department*
