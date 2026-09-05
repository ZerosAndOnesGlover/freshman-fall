# CS 211 · Lab 6 — Solutions
## Instructor Only

**Do not distribute.** Timings vary by machine; object counts, allocation counts and reclaimed fractions do not.

---

## Running the Lab

**Budget:** A 25, B 30, C 25, D 25 = 105 minutes against a 110-minute session. **Part B is the one to protect.** If the room is behind at 15:05, cut Q9's three-times repetition to a single run and skip Q12's discussion — everything else in B and D lands somewhere in the course again.

**Two predictable stalls.**

**Q5 takes longer than it looks** because each Java run is ~0.5 s of work and ~4 s of JVM startup, four collectors, and students will run it repeatedly. Tell them at the start that the whole loop is one command and takes under a minute.

**Q7 is the moment of the lab.** Students will have written down a table in Q5 that says ZGC is the worst collector, and Q7 shows it is the best by 14×. Let them sit with that for a moment before explaining it. **Do not pre-empt it in Q5** — if a student asks in Q5 whether ZGC is really that bad, say "write down what you measured" and move on.

**A machine check before the session:** `java -XX:+UseZGC -Xlog:safepoint -version` must produce safepoint lines. If BH 220's JDK is older than 15, ZGC is not available and Q7 must be run with `-XX:+UseShenandoahGC` or dropped. It is 25.0.3 as of this writing.

---

## Part A — Your Own Runtime

**Q1.**

| `--gc` | allocated | freed | peak live |
|---|---|---|---|
| `none` | 202 | 0 | 202 · 3256 B |
| `rc` | 202 | 202 | **8 · 152 B** |
| `mark` | 202 | 187 | 16 · 280 B |
| `gen` | 202 | 195 | 31 · 520 B |

All four return **20096**. That matters because **a collector is not allowed to be an optimisation with a visible effect.** If one returned a different number, it freed something reachable — the answer is the only end-to-end correctness check available without instrumenting every dereference.

*Accept "so we know it's correct". Push for* which *kind of incorrectness: a collector cannot make a program leak into a wrong answer, only into a crash or a wrong* value*, and a differing value means a live object was reused.*

**Q2.** **`rc` peaks at 8; `gen` at 31.**

- Reference counting frees an object **at the instruction where the last pointer to it dies**, so the heap never holds more than what is genuinely live.
- The generational collector only collects when the *young* generation hits the threshold, and promoted objects sit in the old generation until a major collection. Its peak is threshold plus survivors plus whatever the old generation is holding.

*Reject "rc is better". The question is what produces the number. The follow-up if a student says it anyway: ask what happens to `cycle.cy` — §Q13 and L13 §8.*

**Q3.** Medians **1** (`rc`) and **33** (`mark`, threshold 64).

- **`rc` describes the program.** It frees at the moment of death, so age-at-death is the real age.
- **33 is about half of 64**, the threshold. A tracing collector notices a death at the next collection, so on a steady allocation stream an object's recorded age is uniform on `[0, threshold)` and the median is half of it. **The histogram is measuring the collector.**
- Bug-report sentence, roughly: *"These lifetimes were gathered under a tracing collector, which cannot observe the moment an object becomes garbage; the distribution reflects the collection threshold rather than the program."*

**Q4.** The 284 objects aged 16–32 are the `Cell`s stored into `keep`.

`keep` has **4** slots and a `Cell` is stored on every **7th** iteration, so a stored `Cell` is displaced after 4 × 7 = **28** further allocations. 28 falls in the [16, 32) bucket. 2000 / 7 ≈ 285 stores, and 284 of them are displaced before the program ends.

*This is the question that shows the histogram is reading the source code back. Worth putting on the board if the room is quiet.*

---

## Part B — Four Real Collectors

**Q5.** From the reference machine (OpenJDK 25.0.3, `-Xmx256m`, `Churn 40000000 7`):

| collector | events | total | mean | p99 | max | throughput |
|---|---|---|---|---|---|---|
| Serial | 65 | 35.1 ms | 0.540 ms | 1.076 | 1.106 ms | 101.9 Mobj/s |
| Parallel | 27 | 15.9 ms | 0.589 ms | 0.940 | 0.940 ms | 96.7 Mobj/s |
| G1 | 29 | 24.4 ms | 0.840 ms | 1.428 | 1.428 ms | 97.4 Mobj/s |
| ZGC | 17 | 67.0 ms | 3.941 ms | 8.000 | 8.000 ms | 80.2 Mobj/s |

**Event counts will vary by machine and by run** — heap sizing is adaptive. The *ordering* and the ~100× ratio between ZGC's apparent and actual pause are stable.

**Q6.** `33M->1M(117M)`: **occupied before**, **occupied after**, **current heap capacity**.

Reclaimed = (33 − 1) / 33 = **97.0%**. `pauses.py` reports 97.0% mean for Serial, 98.6% for Parallel and G1.

The sentence: **"Ninety-seven per cent of everything in the young generation was garbage, so a collector that looks only there finds almost all of the garbage for almost none of the work."**

**Q7.**

| | safepoints | total | mean | max |
|---|---|---|---|---|
| ZGC | 56 | 4.67 ms | 83.4 µs | **114.9 µs** |
| G1 | 29 | 25.15 ms | 867.2 µs | **1637.1 µs** |

- Discrepancy for ZGC: `-Xlog:gc` reported a max of **8.000 ms**; the true max pause is **114.9 µs**. A factor of about **70**.
- `-Xlog:gc` reports the duration of a **collection cycle**. ZGC's cycle runs concurrently with the program; the stop-the-world portions are the safepoints inside it. For Serial and Parallel the cycle *is* the pause, which is why the same flag is honest for them and misleading for ZGC.

*The trap is that the misleading number is plausible. Nothing warns.*

**Q8.** Something close to: **"Measure the quantity you care about, not the one the tool defaults to printing — and when comparing tools, check that the default means the same thing for each."**

*Accept anything that generalises. Reject answers that are about ZGC, or about reading documentation more carefully; the point is that both tables were correct.*

**Q9.**

| `-Xmx` | collections | GC total | throughput |
|---|---|---|---|
| 32m | 119 | 83.2 ms | 93.0 Mobj/s |
| 64m | 58 | 55.2 ms | 97.0 Mobj/s |
| 128m | 30 | 24.0 ms | **98.1 Mobj/s** |
| 256m | 29 | 24.2 ms | 97.9 Mobj/s |
| 512m | 24 | 21.4 ms | 94.0 Mobj/s |
| 1g | 18 | 18.5 ms | 80.0 Mobj/s |

Peak at **128m**; `1g` is the slowest of all six while doing the least collection.

**Insist on the repetitions before accepting any percentage.** On the reference machine 128m gave 98.4 / 97.2 / 99.3 (mean 98.3) and 1g gave 87.4 / 83.7 / 87.9 (mean 86.3) — a **12%** loss, against a within-configuration spread of about 2%. The single-run 80.0 in the sweep is the low end of 1g's own spread, so a student quoting 18% from one run has over-claimed from one sample; that is worth a word. **What must reproduce is the direction**, and students getting 84–88 for 1g have done nothing wrong.

**Explanation:** the collector is not the only thing touching memory. A larger young generation means allocation sweeps a larger region before wrapping, and by the time it returns, none of it is in cache. Roughly 5.5 ms of saved collector time is paid for with tens of milliseconds of mutator cache misses. Bump allocation is fast **because it is sequential**, and that is a memory-hierarchy property, not a bookkeeping one — CS 201 L15.

---

## Part C — Root Sets

**Q10.** `#2` is freed. The collection happens at `t14 = call alloc1()`, the last instruction before `row[t14] = t13`.

`--roots=week4` skipped **marking from `row`**. Under Week 4's model `store` reads only `a` and `b`, so `row` — which lives in the `dst` slot — is not live at the call, is not a root, and the array it points at is white. `--roots=live` scanned 1 object: `row`'s array, and nothing else is live there.

**Q11.**

| | residency | collections | scanned |
|---|---|---|---|
| `--roots=live` | 16 B | 17 | 17 |
| `--roots=scope` | 216 B | 22 | 132 |

**Peak live is 504 B in both** because peak is set by the collection *trigger* — 24 objects — not by how much of the heap is garbage. A retaining collector runs more often and marks more; it does not exceed the threshold, so peak cannot show it.

`{ let x = 1; }` is a parse error: **Cyan has no nested block statement.** So a Cyan programmer cannot shrink `big`'s scope at all; the only thing available is to **reuse the variable** — assign something small to `big` after its last real use. In Java that line is `big = null;`.

*This is the honest answer and students often try to write the block first. Let them hit the parse error; it is one line of evidence that scoping is a language feature with a runtime cost.*

**Q12.** *(Discussion.)* Points to draw out:

- **No unit test catches it.** The stack map is only consulted when a collection lands at that exact instruction, on a path where the affected slot holds the only pointer to an object.
- **In production it looks like data corruption**, not a crash: an object is reused, a field reads back as something else, and the failure surfaces arbitrarily far away.
- **It is not reproducible**, because whether the collection lands there depends on total allocation, which depends on load.
- The useful closing remark: **this is why JIT compilers are tested with a "stress GC" mode that collects at every safepoint.** If a student gets there on their own, that is the best answer in the room.

---

## Part D — Cycles and Promotion

**Q13.** With `gc` disabled: acyclic leaks **0**; cyclic leaks **200** out of 200 built, and `gc.collect()` then frees exactly 200.

With `gc` enabled, 10,000 cycles leave **9,998** nodes alive before an explicit collect, because `gc.get_threshold()` is `(2000, 10, 0)` — the tracing pass runs after a net 2,000 container allocations, **not when the garbage appears**. Automatic does not mean immediate.

Commenting out `b.link = a` makes the leak vanish entirely: one line, and reference counting becomes complete.

*Python 3.13 and later report `(2000, 10, 0)`; 3.12 and earlier report `(700, 10, 10)`. Either is fine — the point is that it is a count of allocations.*

**Q14.**

| | fix-up present | `--no-fixup` |
|---|---|---|
| `chain 120` | 242 alloc, **0 freed**, = 119 | 242 alloc, **97 freed**, = 119 |
| `walk 120` | 240 alloc, 0 freed, = 120 | **use-after-free on `#98`** |

**Both are true of `chain --no-fixup`** because `chain` only reads `head`. The 97 freed objects are the *tail* of the list — reachable, but never dereferenced again, so their reclamation is invisible. The collector was wrong and the program could not tell.

`walk` is different because it **traverses every node**. Same bug, same flag; the only change is that something reads the corrupted region.

*The intended lesson is Quiz 5's Q6 again in a new place: a crash tells you now, a wrong answer tells you later, and a right answer over a corrupted heap tells you never.*

**Q15.** **n = 33** at `--threshold=32`.

What it measures: the first minor collection cannot happen until 32 young objects exist, and promotion requires surviving `promote_after = 2` collections. Below that, nothing is ever promoted, so no unrecorded old-to-young pointer can exist and the hole cannot open. **The bug requires sustained allocation to appear at all**, which is why every small test passes.

*Expect 32 or 33 depending on how a student counts; both fine if the reasoning is right.*

**Q16.**

| | collections | pause | scanned | freed |
|---|---|---|---|---|
| `mark` | 538 | 106.16 ms | 178,885 | **0** |
| `gen` | 290 | 114.70 ms | 130,374 | **0** |

Generational is **slower in wall time despite scanning 27% fewer objects**: its 290 collections are **282 major and 8 minor**. With nothing dying young a minor collection reclaims nothing, so it degenerates into full collections *plus* the write-barrier overhead on every store, and the barrier buys nothing.

The right response to a collection that reclaims nothing is **to grow the heap**, not to collect again. That is PS 6 D3, and the reference implementation takes `chain 300` from 538 collections / 103.89 ms to **4 collections / 0.73 ms** — while leaving `churn 2000` at 34 collections either way.

---

## If You Finish Early

**Q17.**

| `--roots` | freed | scanned |
|---|---|---|
| `live` | 3 | 1 |
| `scope` | **0** | 4 |
| `week4` | 4, then **crash** | 0 |

`--roots=scope` is safe and reclaims **nothing**, because `m`, `row` and every temporary are still named in the frame at the point of collection — `victim` is four statements long, so nothing has left scope. It also scans four times as much as the precise policy to achieve that. **Safety and usefulness are different properties**, and the safe policy is useless on short functions, which is most functions.

**Q18.** **`cycle.cy` is the answer and it is sitting in the same folder** — `leak 5` peaks at **21 objects under `rc`** against **8 under `mark`**, and the gap grows without bound with `n`. Students who go looking for something clever have missed that L13 §10 already built it.

The second half: for a program with **no cycle**, no such function exists. Reference counting is complete on an acyclic heap and frees at the last pointer death, so its live set is exactly the reachable set at every instant, while a tracing collector's is the reachable set *plus* whatever has died since the last collection. The property being relied on is **promptness plus completeness**, and the second half is the one that fails in the cyclic case.

**Q19.** `-XX:+UseEpsilonGC` at `-Xmx256m` dies:

```
Terminating due to java.lang.OutOfMemoryError: Java heap space
```

`Churn 40000000 7` allocates roughly 40 M objects of ~48 bytes, so finishing without collection needs on the order of **2 GB**, and the number scales with `n` rather than with live data. Epsilon is shipped for exactly three uses: **measuring allocation cost with the collector removed**, testing that a program's live set really is bounded, and very short-lived jobs that will exit before the heap fills.

---

*CS 211 · Week 6 · Lab 6 Solutions · © CSE Department*
