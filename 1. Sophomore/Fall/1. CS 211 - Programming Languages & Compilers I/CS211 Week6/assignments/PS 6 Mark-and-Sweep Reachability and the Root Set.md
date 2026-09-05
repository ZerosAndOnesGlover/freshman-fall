# CS 211 · Problem Set 6
## Mark-and-Sweep, Reachability, and the Root Set

---

**Released:** Week 6, Wednesday · **Due:** Week 7, Friday 17:00
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `collect.py` (your version, runnable end to end), any new modules you write, and `ps6.md` (written answers, tables, traces). Written answers inside code comments will not be marked.

Start from the Week 6 lab folder. `heap.py` and `runtime.py` are given to you complete — **you may not change `live.py`'s `SLOTS` table**, for the same reason as last week, and you should not need to change `runtime.py` at all. If you think you do, say so in `ps6.md` and explain why; that is a legitimate answer and occasionally the right one.

> **Project 1 is assigned this week and is due Week 11.** Part B's collector is a component of it.
> The mini-compiler is expected to run its output, and running it means having this.

---

## Part A — Reachability and the Root Set (18 points)

**A1.** *(4)* For each opcode below, say which slots can hold a **pointer** at run time, and therefore which slots a collector must follow. Then say whether that set is the same as the slots `live.py`'s `SLOTS` table marks as *uses*.

`copy` · `load` · `store` · `getfield` · `setfield` · `alloc` · `newarr` · `call`

Where the two sets differ, explain the difference. **One of them differs for a reason that has nothing to do with pointers** — find it and name it.

**A2.** *(5)* Reproduce the `victim.cy` result from L14 §3:

```
$ python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=live
$ python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=week4
```

Then explain it exactly:

- Give the **instruction** at which the collection happens, quoting it from `python3 tac.py victim.cy victim`.
- Give the **live set at that instruction under each model**. Compute both by hand; check with `runtime.live_after_map`.
- Name the single missing `SLOTS` entry responsible, and state which of `defs`/`uses` it belongs in.

**A3.** *(4)* `live.py`'s `check_coverage` raises when the code contains an opcode the table does not mention.

- Explain what an unknown opcode's def and use sets default to, and why that is *unsound for a collector* specifically — not merely imprecise.
- Add an opcode to `tac.py` that `SLOTS` does not know about, deliberately, and show the exception. Then **delete the `check_coverage` call** and show what happens instead. Report both.

**A4.** *(5)* Reproduce the `loiter.cy` table from L14 §4 for `--roots=live` and `--roots=scope`.

- Report residency, collections, and objects scanned.
- **Peak live is identical in both runs. Explain why**, in terms of what triggers a collection.
- A colleague benchmarks a collector by measuring peak RSS. In two sentences, say what they will fail to detect.

---

## Part B — Mark and Sweep (28 points)

**B1.** *(6)* `MarkSweep.collect` tracks the black set in a Python `set` of addresses. Real collectors use a **mark bit in the object header** — `Obj` already carries a `marked` slot for you.

- Rewrite the mark phase to use `o.marked` instead of the set.
- **You must now clear the marks somewhere.** Say where you chose to do it — before marking, or during the sweep — and give the argument for your choice. One of them makes an unmarked-but-live object impossible; say which.
- Confirm the collector still returns 20096 on `churn.cy churn 200` and 15 on `cycle.cy leak 5`.

**B2.** *(6)* The mark loop contains this line:

```python
obj = self.heap.objs.get(a)
if obj is None:
    continue                    # a root into freed memory
```

- Under what circumstances can a root name an address that is not in the heap? Construct one, and show it. *(Hint: Part A already made one happen.)*
- **Argue for or against removing the line** so that this situation raises instead. Whichever you choose, say what it costs.

**B3.** *(6)* Reproduce L13 §10's cycle result — `cycle.cy leak 5` under `--gc=rc` and `--gc=mark`.

- Report allocated / freed / still-live for both.
- `--gc=mark` leaves **5 objects live at exit**, and they are not reachable. Explain why they were not collected. Is this a bug? Answer in one sentence and defend it.
- Predict the leaked-object count for `leak 50` under `--gc=rc` **before running it**, then run it. If your prediction was wrong, say what you had not accounted for.

**B4.** *(10)* **Implement a copying collector** (Cheney's algorithm) as a new class in `collect.py`.

Evacuate every live object to a fresh address; do not touch the dead ones at all. `runtime.Machine.each_root_slot()` yields `(frame, name, address)` so that you can write the new address back.

- Report `churn.cy churn 200` and `cycle.cy leak 5` — both must give the same answers as mark-sweep.
- **Compare `scanned` against `MarkSweep` on the same workload and explain the relationship you find.** Do not assume it will be smaller.
- State, in two sentences, what a copying collector can do that mark-sweep cannot, and what it requires from the compiler in exchange. L14 §5 is the argument; say it in your own words.

---

## Part C — Reference Counting (18 points)

**C1.** *(5)* `on_var_write` increments before it decrements.

- Swap the two lines. Write the shortest Cyan function that then **frees a live object**, and show the crash.
- Explain why no amount of testing on programs without self-assignment would find this.

**C2.** *(5)* `decref` uses an explicit worklist rather than recursion.

- Write a Cyan function that would recurse at least 100 deep under the recursive version. *(`chain.cy` is a start.)*
- Instrument `decref` and report, for `chain.cy chain 300`, **both** the maximum *length* the worklist ever reaches **and** the maximum number of *iterations* a single call to `decref` performs.
- **The two numbers are wildly different, and only one of them is the recursion depth you avoided.** Say which, and why the other one is what it is.
- CPython hit this as a real bug. In two sentences, say why "just increase the recursion limit" is not a fix.

**C3.** *(8)* **Implement `RefCount.unreachable()`**: at the end of a run, report the objects that are still counted but not reachable from the roots — that is, the leak.

- It must agree exactly with what `--gc=mark` would have freed. Verify on `cycle.cy leak 5` and on `chain.cy chain 60`.
- Use it to report the **leak rate** of `cycle.cy` at `leak 5`, `leak 50`, and `leak 500`, as objects leaked per call.
- Then answer: you have just written a tracing collector in order to find reference counting's mistakes. **What have you actually saved by keeping the reference counts?** There is a real answer; L13 §6 measured it.

---

## Part D — Generations, Barriers, and Growth (26 points)

**D1.** *(6)* Reproduce the promotion result of L14 §8 with and without `--no-fixup`, on both `chain` and `walk`.

- Report all four runs.
- Explain in terms of the tri-colour invariant **why no write barrier could have caught this**. Your answer must identify the moment the old-to-young pointer comes into existence.
- `promote_after` defaults to 2. Find the smallest value of `n` for which `chain.cy chain n --no-fixup` frees a live object, and explain what that number is measuring.

**D2.** *(6)* Measure the write barrier on `churn.cy`, `chain.cy`, and `loiter.cy`: report `barrier_hits`, `barrier_records`, and the ratio. **Quote the `--threshold` you used** — one of the three numbers depends on it, and you should be able to say which before you run anything.

- **Two of the three record zero.** Explain each from the program's source, not from the numbers, and say whether the two zeros have the same cause.
- The barrier costs a few instructions per pointer write and saves a scan of the old generation per minor collection. Write down the inequality that decides whether it pays, in terms of quantities you can measure, and evaluate it for `churn 2000`.

**D3.** *(8)* **Implement a heap-growth policy.** L14 §9 showed 538 collections reclaiming zero objects.

- After each collection, if the fraction reclaimed is below some threshold, grow the trigger point. Choose the fraction and the growth factor, and **justify both choices** rather than tuning until the number looks good.
- Report collections, total pause, and objects scanned for `chain.cy chain 300` before and after.
- Report the same three for `churn.cy churn 2000` before and after. **If your policy changes the numbers on `churn`, that is a finding you must explain** — say whether it is an improvement, a regression, or noise, and how you decided.
- The JVM throws `OutOfMemoryError: GC overhead limit exceeded` at 98% time in GC with under 2% recovered. In two sentences, relate that rule to what you implemented.

**D4.** *(6)* Sweep `--threshold` over at least six values for `churn.cy churn 2000` under `--gc=gen`. Report collections, total pause, residency, and objects scanned.

- Identify the value that minimises total pause, and the value that minimises residency. **They are not the same. Say which you would ship and why.**
- L14 §11 found that a 1 GB JVM heap ran 12% **slower** than a 128 MB one while doing 40% less collection. Your sweep will not reproduce that. **Explain why not** — what does the real measurement include that ours cannot?

---

## Part E — Written (10 points)

**E1.** *(5)* L13 §9 showed that Cyan could not express a heap cycle, for three unrelated reasons.

- State all three precisely.
- L13 §10 relaxed exactly one of them and got a cycle. **Was relaxing that one *necessary*?** That is: with the empty-array rule left alone, can a cycle be built by relaxing either of the other two instead? Answer for each, with either a program or an argument.
- In two sentences: what does this say about reasoning from "our language guarantees X"?

**E2.** *(5)* You are asked to add `weak` references to Cyan — a pointer that does not keep its target alive — so that reference counting can handle cyclic structures the way Swift and Rust's `Weak` do.

- Say what changes in `RefCount`, in one paragraph.
- Say what changes in `MarkSweep`, in one paragraph.
- **One of the two is substantially harder, and it is not the one most people guess.** Say which and why. *(Consider what must happen to every weak reference to an object at the moment that object is determined to be dead, and when a tracing collector knows that.)*

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14.2, OpenJDK 25.0.3, x86-64 Linux). **Counts are deterministic; timings are not.** If a count differs, you have found something — report it rather than adjusting it.

| Measurement | Value |
| --- | --- |
| `churn.cy churn 200`, all four collectors | returns 20096 |
| `--gc=none` peak live | 202 objects · 3256 B |
| `--gc=rc` peak live | **8 objects · 152 B** |
| `--gc=mark --threshold=16` peak live | 16 objects · 280 B |
| `--gc=gen --threshold=16` peak live | 31 objects · 520 B |
| `--gc=gen` barrier on `churn 200` | 234 writes, 25 recorded |
| `cycle.cy leak 5 --gc=rc` | 25 allocated, 5 freed, **20 leaked** |
| `cycle.cy leak 5 --gc=mark --threshold=8` | 25 allocated, 20 freed |
| `victim.cy --roots=live` | exit 0, 1 object scanned |
| `victim.cy --roots=week4` | **use-after-free on `#2`**, exit 3 |
| `loiter 400 --roots=live` | residency 16 B · 17 collections · 17 scanned |
| `loiter 400 --roots=scope` | residency 216 B · 22 collections · 132 scanned |
| `chain.cy walk 120 --gc=gen --no-fixup` | **use-after-free on `#98`** |
| `chain.cy chain 300 --gc=mark --threshold=64` | 538 collections, 0 freed |

Lifetime distribution, `churn 2000`:

| collector | median age at death | interpretation |
| --- | --- | --- |
| `--gc=rc` | **1** | the program's actual behaviour |
| `--gc=mark --threshold=64` | 33 | half the threshold — **the collector measuring itself** |

---

## A Note on Parts B2, D3 and E1

Each of these asks you to make a judgement rather than to compute an answer, and each has a defensible case on both sides.

B2 asks whether a defensive `continue` should stay or become an exception. D3 asks you to choose two constants and defend them. E1 asks whether a change was necessary, which requires you to look for something that may not exist.

**A well-argued answer that reaches the opposite conclusion from the model solution gets full marks. A correct conclusion with no argument does not.** These are the questions on which a compiler engineer is actually paid, and the reasoning is the deliverable.

**One thing that will not get marks: a policy tuned until the benchmark improved, presented as a design.** D3 says *justify both choices* for that reason. If you tried six factors and picked the best, say so and report all six — that is an honest empirical answer and it scores full marks. Reporting only the winner, as though it were reasoned, does not.

---

*CS 211 · Week 6 · Problem Set 6 · © CSE Department*
