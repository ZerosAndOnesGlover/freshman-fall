# CS 211 · Problem Set 6 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** All counts verified against the Week 6 lab code on Python 3.14.2 / OpenJDK 25.0.3.

---

## Part A — Reachability and the Root Set (18)

**A1.** *(4 — one mark per correct group, one for the odd one out)*

| opcode | slots that can hold a pointer | same as `SLOTS` uses? |
|---|---|---|
| `copy` | `dst`, `a` | `a` is a use; `dst` is a **def** |
| `load` | `dst`, `a` | `a` is a use, `b` is an index (int) — a use, but never a pointer |
| `store` | `dst`, `b` | both uses; `a` is an index |
| `getfield` | `dst`, `a` | `a` is a use; `b` is a field **name** |
| `setfield` | `dst`, `b` | both uses; `a` is a field **name** |
| `alloc` | `dst` | no uses; `a` is a type **name** |
| `newarr` | `dst` | no uses; `a` is a **length** |
| `call` | `dst`, every element of `b` | `b*` are uses; `a` is the callee **name** |

**The odd one out is `load`/`store`'s index operand.** It *is* a use — liveness must keep it alive — but it can never hold a pointer, so a collector need not follow it. **The two sets are not the same set, and the difference is types, not liveness.**

*Full marks require noticing that "is a use" and "may be a pointer" are different questions. The best answers observe that a precise collector wants a **type-aware** map and that ours gets away with `isinstance` because the interpreter keeps `Ref` distinct — L14 §5.*

**A2.** *(5 — 2 instruction, 2 live sets, 1 the `SLOTS` entry)*

- **Instruction:** `t14 = call alloc1()`. It is the last instruction before `row[t14] = t13`, and it is the only one in `victim` that can allocate.
- **Live-after under `live`:** `{row, t13, t14}`. Under `week4`: `{t13, t14}` — **`row` is missing**.
- **The entry:** `'store': ((), ('dst', 'a', 'b'))`. `dst` belongs in the **uses** tuple. Week 4's model never inspected `dst` for any opcode.

Freed object is `#2`, the array originally at `m[0]`.

*A common wrong answer puts `dst` in defs "because it's called dst". Mark it down — `store` **defines nothing**; that is the whole point.*

**A3.** *(4 — 2 explanation, 2 demonstration)*

`SLOTS.get(ins.op, ((), ()))` returns **empty defs and empty uses**. Empty uses means the instruction appears to read nothing, so liveness *under-approximates*: variables that are live are reported dead.

For DCE that is unsound in the way Week 5 showed. **For a collector it is worse**, because the under-approximated set is the root set: an object whose only pointer is in a variable the analysis dropped is unreachable *according to the collector* and reachable *according to the program*. That is a use-after-free rather than a deleted instruction.

Removing the `check_coverage` call produces no error at all — the compiler runs, the collector runs, and the program either works or corrupts memory depending on where collections land.

*Accept any new opcode. The demonstration must show **both** the exception and the silent case; half marks for one.*

**A4.** *(5 — 2 table, 2 peak, 1 RSS)*

| | residency | collections | scanned |
|---|---|---|---|
| `live` | 16 B | 17 | 17 |
| `scope` | 216 B | 22 | 132 |

**Peak live is 504 B in both**, because a collection is triggered by object *count* reaching the threshold. Peak is therefore pinned at the threshold regardless of how much of what is retained is garbage. Retention shows up as *more frequent* collections and *more marking*, never as a higher peak.

A colleague benchmarking peak RSS will detect **nothing**: not root-set imprecision, not a retention bug, not a loitering object. They are measuring their own heap-sizing policy.

---

## Part B — Mark and Sweep (28)

**B1.** *(6 — 3 implementation, 3 the argument)*

Clearing marks **during the sweep** is the better answer, and the argument is that the sweep already visits every object, so clearing is free, whereas a separate pre-pass is a second full traversal.

Clearing **before marking** is also correct and has one real advantage: it makes an unmarked-but-live object impossible **if the program crashes mid-collection**, because the marks are never stale between collections. The sweep-clearing version leaves every live object marked between collections, so a bug that starts marking without clearing silently marks nothing new.

*Both answers score full marks with the argument. The question is which invariant they chose, not which line they wrote. Reject "it doesn't matter."*

Must still print 20096 and 15.

**B2.** *(6 — 3 construction, 3 argument)*

A root can name a freed address only after the collector has already made a mistake — `--roots=week4` in Part A is exactly the construction, and `--no-fixup` in Part D is another.

**For removal / raising:** the line converts a detected inconsistency into silence. Every time it fires, the collector has proof that its root set disagrees with its heap, and that is precisely the bug this week is about. Raising turns an invisible corruption into a stack trace.

**For keeping it:** a production collector cannot abort the program because one root looks stale; conservative roots (L14 §5) name non-heap words routinely, and a collector for C would fire this constantly and legitimately.

**The resolution most students miss and should be credited generously for reaching:** it depends on whether the collector is *precise*. Ours is, so the line is masking a bug and should raise. Boehm's is not, so the equivalent line is load-bearing.

**B3.** *(6 — 2 table, 2 the five, 2 the prediction)*

| | allocated | freed | still live |
|---|---|---|---|
| `--gc=rc` | 25 | 5 | **20** |
| `--gc=mark --threshold=8` | 25 | 20 | 5 |

The 5 left under `mark` are the **last batch**, allocated after the final collection. They are unreachable and were never collected because **nothing triggered a collection after they died** — the program ended first. **Not a bug**: a tracing collector reclaims at times of its choosing, and "at exit" is not one of them unless you ask.

Prediction for `leak 50`: 4 objects leak per call — `a`, `b`, and the two one-element arrays — so **200**. Verified: 250 allocated, 50 freed, 200 leaked.

*The common wrong prediction is 5 per call, counting `none`. `none` is freed: its count drops to zero at frame exit because `a.link` and `b.link` were overwritten. Students who predict 250 and then find 200 and* explain *the difference get full marks — that is exactly the reasoning the question wants.*

**B4.** *(10 — 5 working, 3 the comparison, 2 the two sentences)*

Reference implementation: evacuate each root via `each_root_slot`, writing `frame.env[name] = Ref(new)`; then a Cheney queue over the copies, evacuating children in place; then drop everything not forwarded.

Must produce **20096** and **15**.

**The comparison is the marked part, and the expected answer is that `scanned` is essentially identical to mark-sweep's** — both visit exactly the live objects. On `churn 200` both report 101. **Copying is not fewer objects; it is that the dead ones cost literally nothing**, because there is no sweep phase walking the whole heap. Mark-sweep's cost is O(live) to mark plus O(heap) to sweep; copying is O(live), full stop.

*Students who expected copying to scan less and report that it does not, with the explanation, get full marks. Students who report a smaller number have almost certainly failed to evacuate transitively — check their `cycle.cy` result.*

The two sentences: a copying collector **compacts**, so allocation becomes a pointer bump and fragmentation disappears. In exchange it needs the compiler to identify **where every root is stored**, not merely what it points at, because it must write the new address back.

---

## Part C — Reference Counting (18)

**C1.** *(5 — 3 the program, 2 the explanation)*

Swap the lines and any self-assignment through the last reference fails. Shortest form is an assignment of a variable to itself where the count is 1.

The explanation: the bug needs `old is new` *and* a count of exactly 1. A test suite that never self-assigns — which is nearly all of them, since self-assignment looks pointless — cannot produce the state. **The pointlessness of the operation is what protects it from being tested.**

*Accept any program that triggers it. Full marks require naming the count-of-one condition, not just "self assignment is bad".*

**C2.** *(5 — 1 program, 3 the two numbers, 1 CPython)*

`chain.cy chain 300` builds 602 objects in one chain.

| | value |
|---|---|
| max worklist **length** | **1** |
| max **iterations** in one `decref` | **601** |

**This is the marked part, and the trap is deliberate.** A chain is freed head-first: freeing a node pushes its single child, which is immediately popped, which pushes its single child. The worklist never holds more than one address — so a student who instruments `len(work)` and reports "1" has measured something true and irrelevant.

**The recursion depth avoided is the iteration count, 601** — that is how many nested calls the recursive version would have made. The general relation on a chain of `n` nodes plus `n` arrays is `2n + 1`; verified at n = 60 → 121, n = 120 → 241, n = 300 → 601.

*Full marks require both numbers and the explanation of why the length stays at 1. A student reporting only 601 has the right answer; a student reporting only 1 has measured the wrong quantity and should be shown the other.*

"Increase the recursion limit" is not a fix because (a) the depth is proportional to a *data structure the user controls*, so no limit is large enough for all inputs, and (b) in CPython the recursion was in **C**, where the limit is the OS thread stack and overflowing it is a segfault, not a Python exception.

**C3.** *(8 — 4 implementation and agreement, 2 leak rate, 2 the final question)*

`unreachable()` traces from `self.m.roots()` and reports counted objects not reached. Must agree exactly with `--gc=mark`.

Leak rate for `cycle.cy`: **4 objects per call**, at every `n`. `leak 5` → 20, `leak 50` → 200, `leak 500` → 2000. **Linear in the work done.**

**The final question is the one to mark hard.** Having written a tracer to find refcounting's mistakes, what did the counts buy?

The answer is **promptness**, and L13 §6 measured it: peak live of 8 objects against mark-sweep's 16 and generational's 31. Reference counting freed every acyclic object at the instruction where it died. A tracer that runs only when you call it gives you the right answer at a time you did not choose; the counts give you almost all of the reclamation immediately, and the tracer is then a *backstop* rather than the mechanism.

**That is exactly CPython's architecture**, and a student who says so has answered the question. *(Reject "nothing" — it is a defensible-sounding answer and it is contradicted by a measurement in the lecture.)*

---

## Part D — Generations, Barriers, and Growth (26)

**D1.** *(6 — 2 table, 2 invariant, 2 the smallest n)*

| | fix-up | `--no-fixup` |
|---|---|---|
| `chain 120` | 0 freed, = 119 | **97 freed**, = 119 |
| `walk 120` | 0 freed, = 120 | **crash on `#98`** |

**Why no barrier could catch it:** the old-to-young pointer is not created by a write. It is created by **promotion** — the pointer already existed, young-to-young, and was correctly not recorded. Changing the parent's generation changes the pointer's classification **without any store executing**. A write barrier fires on writes; nothing wrote.

Smallest `n` at `--threshold=32`: **33**. It measures the point at which enough allocation has happened for a first minor collection (32 young objects) *and* for something to survive `promote_after = 2` of them. Below it, nothing is ever promoted and the hole cannot exist.

**D2.** *(6 — 3 measurement, 1 the zero, 2 the inequality)*

At `--threshold=32`:

| program | barrier hits | recorded |
|---|---|---|
| `churn 200` | 234 | **21** (9.0%) |
| `chain 300` | 902 | **0** |
| `loiter 400` | 420 | **0** |

*The record count for `churn` depends on the threshold — it is 25 at `--threshold=16` and 21 at 32, because the threshold determines how much gets promoted. **Accept any figure the student's stated threshold produces**; reject a figure with no threshold quoted. The hit counts do not vary.*

**Both zeros, and they do not have the same cause.**

- **`chain`** writes plenty of pointers, but every one is a field initialiser on a *brand-new* object — `new Node { link: [head] }` — and the list only ever grows at the head, so **no old object is ever written to**. Its old-to-young pointers all arise from *promotion*, which is exactly D1's hole.
- **`loiter`** writes pointers only while building `big`, in the first statement, **before anything has been promoted at all**. There is no old generation yet. Its 420 hits are the array-literal stores and they are all young-to-young.

*A student who says "both are young-to-young" has the surface answer. Full marks require noticing that `chain`'s zero is a claim about the shape of the data structure and `loiter`'s is a claim about timing.*

The inequality: the barrier pays when

$$c_b \times W \;<\; c_s \times |\text{old}| \times M$$

where `W` is pointer writes, `M` minor collections, `|old|` the old-generation size, and `c_b`, `c_s` the per-write and per-object-scanned costs. For `churn 2000` the right side dominates by orders of magnitude; for `chain` the left side is all cost and the right side is zero, because a minor collection there reclaims nothing regardless.

**D3.** *(8 — 3 policy and justification, 3 the two before/after tables, 2 the JVM rule)*

Reference implementation: after a collection, if `freed / live_before < 0.25`, set the threshold to `max(threshold, 2 × live)`.

**Justification expected for both constants**, not just numbers: the *yield fraction* is asking "did collecting pay for itself", so it should be well above zero and well below one — a quarter is arbitrary within a broad safe range and should be stated as such. The *factor* must be > 1 to terminate and is usually 2 because it makes the amortised collection cost per allocated byte constant, the same argument as dynamic-array growth.

| `chain 300` | collections | pause | scanned |
|---|---|---|---|
| plain | 538 | 103.89 ms | 178,885 |
| with growth | **4** | **0.73 ms** | **960** |

Final threshold 1024, after 4 growths. **A 142× reduction in pause time.**

| `churn 2000` | collections | pause | scanned |
|---|---|---|---|
| plain | 34 | 1.17 ms | 193 |
| with growth | 34 | 1.22 ms | 193 |

**Identical — the threshold never grows, because every collection on `churn` reclaims nearly everything.** That is the result to insist on: *a good policy is invisible when it is not needed.* A student whose policy changes `churn`'s numbers has one that fires spuriously, and must say so.

The JVM rule — 98% of time in GC with under 2% recovered — is **the same predicate with the opposite response**: both detect "collection is not paying", and where we grow the heap, the JVM has run out of room to grow and reports failure instead. Ours is what the JVM does *first*; `OutOfMemoryError` is what it does when it cannot.

**D4.** *(6 — 3 sweep, 2 the two optima, 1 the JVM contrast)*

Any sweep of six or more values. The shape: total pause falls as the threshold rises (fewer collections), residency rises (more garbage retained between collections). **The two optima are at opposite ends, so they cannot coincide.**

Which to ship is a legitimate judgement: pause matters for interactive work, residency for constrained memory. **Full marks for either with a stated context.** No marks for picking one without saying what the program is for.

**Why our sweep cannot reproduce L14 §11:** our "heap" is a Python dict and our objects are Python objects. There is no contiguous allocation region, no bump pointer, and no relationship between our threshold and any cache. The JVM result is a **memory-hierarchy** effect, and we have not modelled memory. *(The strongest answers note that this is exactly why the copying collector of B4 is the interesting one — it is the only design here where locality would even be expressible.)*

---

## Part E — Written (10)

**E1.** *(5 — 2 the three rules, 2 the necessity argument, 1 the closing)*

The three:

1. **`new` must initialise every field**, so a struct with a field of its own type is uninhabitable.
2. **No `null`, and an empty array literal has no inferable element type**, so there is no way to build an object that points at nothing yet.
3. **No infinite types**: a self-containing array needs `T = [T]`, which cannot be written.

**Was relaxing rule 2 necessary? No — and this is the marked part.** Each of the three is individually sufficient to prevent cycles, so none of them is necessary.

Relaxing rule 1 instead — allow partial initialisation, leaving `next` unset — gives a cycle immediately:

```cyan
struct Node { val: int; next: Node; }
let a = new Node { val: 1 };
let b = new Node { val: 2 };
a.next = b;  b.next = a;
```

**Verified:** with only the missing-field check removed, `leak(5)` allocates 10 objects; `--gc=rc` frees **0**, `--gc=mark` frees 8. *(Note this leaks 2 per call rather than 4, since there are no intermediate arrays — a student reporting that has actually run it.)*

Relaxing rule 3 — equirecursive types — permits `r[0] = r` and gives a one-object cycle.

The closing: **"our language guarantees X" is a claim about a conjunction of rules, and the guarantee dies when *any* term is relaxed.** You cannot predict which change ends it unless you can enumerate the terms — and nobody wrote these three down as a memory-safety argument, because none of them was designed as one.

*This is the best question on the paper. Full marks require a counterexample or argument for each of the other two, not a general remark.*

**E2.** *(5 — 1 refcount, 2 marksweep, 2 the comparison)*

**`RefCount`:** a weak reference does not increment. That is nearly all of it — plus a registry so that when an object hits zero, the weak references to it can be cleared before it is freed.

**`MarkSweep`:** do not follow weak edges during marking. Then, after marking and **before sweeping**, clear every weak reference whose target is white.

**The harder one is `MarkSweep`, and most students guess `RefCount`.** The reason is *timing*. Reference counting knows an object is dead **at a single point**, the decrement to zero, and can clear the weak references right there. A tracing collector does not know anything is dead until marking has finished — so there is a window in which a weak reference points at an object that is doomed but not yet freed, and reading it during that window must return "absent", not a pointer. That requires an ordered phase between mark and sweep, and it is why real runtimes have a documented ordering of weak references, soft references, finalizers and phantom references, in that order, each with its own pass.

*Credit any answer that identifies "when does the collector know" as the distinction. Reject answers that say marksweep is harder because there is more code.*

---

## Overall

**Expected distribution:** Parts A and C are recall-plus-a-step and should be high. **Part B4 and Part D3 separate the class.** Part E1 is the question that identifies students who are reading the course as an argument rather than a sequence of techniques.

**The two failure modes to watch for in marking:**

1. **Numbers with no run behind them.** Every count in this paper is deterministic and reproducible. A table with a wrong count is a student who did not run it; a table with a *right* count and a wrong explanation is a student who did. Mark those differently.
2. **D3 tuned rather than justified.** The paper warns about this explicitly. A student who reports six factors and picks one has done the assignment; a student who reports one factor and calls it a design has not, even if the factor is 2.

---

*CS 211 · Week 6 · PS 6 Solutions · © CSE Department*
