# CS 211 · Lab 6
## Profiling Garbage Collection Pauses

**Friday of Week 6 · 14:00–15:50 · BH 220 · covers Week 6**
**Unmarked and mandatory.** The TA checks you off in the session. [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.

**Bring:** a terminal. Everything is in this folder.

> **Lab 6 covers Week 6.** Both of this week's lectures have already happened. Part C assumes
> you know what a root set is, and Part D assumes you know what promotion is.

---

## Setup

```bash
cd "CS211 Week6/lab"
python3 runtime.py churn.cy churn 20 --gc=none    # should print a heap report
java -version                                     # 25.0.3 in BH 220
javac Churn.java
```

If any of those fail, get the TA now rather than at 15:30.

---

## Part A — Your Own Runtime (25 min)

**Q1.** Run the same program under all four collectors:

```bash
for g in none rc mark gen; do python3 runtime.py churn.cy churn 200 --gc=$g --threshold=16; done
```

Record **allocated / freed / peak live** for each in a table.

All four return 20096. **Say why that matters** — what would it mean if one of them did not?

**Q2.** One collector has a peak footprint of 8 objects; another has 31. Both are correct.

**Name them, and explain the difference in one sentence each.** If your explanation for the 8 is "it is better", you have not answered the question — say *what it does* that produces that number.

**Q3.** Now measure lifetimes, twice:

```bash
python3 runtime.py churn.cy churn 2000 --gc=rc --lifetimes | tail -12
python3 runtime.py churn.cy churn 2000 --gc=mark --threshold=64 --lifetimes | tail -12
```

The medians are **1** and **33**.

- Which one describes the program?
- The other number is close to half of something. **Half of what, and why?**
- Write one sentence you could put in a bug report to explain why the second measurement is not wrong, merely useless.

**Q4.** In the reference-counted histogram, 284 objects die with an age between 16 and 32.

**Find them in `churn.cy`.** Which allocation site produces them, and why is their age in that range? The source has the answer; the arithmetic is one line.

---

## Part B — Four Real Collectors (30 min)

**Q5.** Run the Java workload under each collector, piping through the summariser:

```bash
for gc in SerialGC ParallelGC G1GC ZGC; do
  java -XX:+Use$gc -Xlog:gc -Xmx256m Churn 40000000 7 2>&1 | python3 pauses.py $gc
done
```

Build a table: **events, total, mean, p99, max**, and the throughput from the last line of each run.

**Q6.** Look at a single Serial GC line:

```
[0.410s][info][gc] GC(64) Pause Young (Allocation Failure) 33M->1M(117M) 0.342ms
```

- What are the three numbers `33M->1M(117M)`?
- Compute the fraction of the occupied heap reclaimed. `pauses.py` reports it too — check yourself against it.
- **That single number is the entire justification for generational collection.** Say it in one sentence.

**Q7.** From your Q5 table, ZGC looks like the worst of the four — roughly six times the pause of G1.

**It is not.** Run this instead:

```bash
java -XX:+UseZGC -Xlog:safepoint -Xmx256m Churn 40000000 7 2>&1 \
  | grep -o "Total: [0-9]* ns" \
  | awk '{s+=$2; if($2>m)m=$2; n++} END {printf "%d safepoints, total %.2f ms, mean %.1f us, max %.1f us\n", n, s/1e6, s/n/1000, m/1000}'
```

and the same for `-XX:+UseG1GC`.

- Report both.
- **How large is the discrepancy for ZGC between the two measurements, as a factor?**
- Explain what `-Xlog:gc` was actually reporting for ZGC and why it is not a pause. One sentence.

**Q8.** You now have two tables that rank the same four collectors differently, from the same JVM, on the same program.

**Write down, in one sentence, the general rule you would give a colleague** so that they do not make this mistake. It should not mention ZGC.

**Q9.** Sweep the heap size on G1:

```bash
for hs in 32m 64m 128m 256m 512m 1g; do
  printf "%-5s " $hs
  java -XX:+UseG1GC -Xlog:gc -Xmx$hs Churn 40000000 7 2>&1 | tail -1
done
```

- Plot or tabulate throughput against heap size.
- **The largest heap is not the fastest.** Find the peak, and report how much slower `1g` is.
- Run the two ends three times each. Is the difference larger than the run-to-run spread?
- Give the explanation. *(CS 201's `L15 Locality as Leverage` is the argument; this is that lecture arriving through a JVM flag.)*

---

## Part C — Root Sets (25 min)

**Q10.** Reproduce the use-after-free:

```bash
python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=live
python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=week4
```

- Which object is freed, and at which instruction? Get the instruction from `python3 tac.py victim.cy victim`.
- `--roots=week4` scanned **0** objects and `--roots=live` scanned **1**. The buggy one did less work. **Say precisely what work it skipped.**

**Q11.** Now the other direction:

```bash
python3 runtime.py loiter.cy loiter 400 --gc=mark --threshold=24 --roots=live
python3 runtime.py loiter.cy loiter 400 --gc=mark --threshold=24 --roots=scope
```

- Record **residency, collections, objects scanned** for both.
- **Peak live is 504 bytes in both.** Why does the difference not appear there?
- `big` is dead from line 3 of `loiter`, and in scope until the function returns. **Cyan has no
  nested block statement** — check, with `{ let x = 1; }` inside a function — so you cannot shrink
  its scope even if you want to. Given that, what is the *only* thing a Cyan programmer could do
  to help a `scope`-rooted collector here? What would the equivalent line be in Java?

**Q12.** *(Discussion — do this one out loud with your neighbour.)*

L14 §2 claims that the root set is a **compiler output**, and that the collector has no way to check it.

Take that seriously for two minutes. If the compiler emits a stack map with one wrong entry, in one method, on one line:

- Which test would catch it?
- What would the failure look like in production?
- Would it be reproducible?

---

## Part D — Cycles and Promotion (25 min)

**Q13.** CPython is reference counted, and has exactly L13 §8's problem:

```bash
python3 pycycle.py
```

- With `gc` disabled: how many nodes does the acyclic case leak? The cyclic case?
- With `gc` enabled: 10,000 cycles are built, and thousands of nodes are still alive before an explicit `gc.collect()`. **Why?** `gc.get_threshold()` is printed for you.
- Comment out the `b.link = a` line in `make_cycle` and re-run. Report what changes.

**Q14.** Reproduce the promotion hole from L14 §8:

```bash
python3 runtime.py chain.cy chain 120 --gc=gen --threshold=32
python3 runtime.py chain.cy chain 120 --gc=gen --threshold=32 --no-fixup
python3 runtime.py chain.cy walk  120 --gc=gen --threshold=32
python3 runtime.py chain.cy walk  120 --gc=gen --threshold=32 --no-fixup
```

- Four runs, four results. Tabulate them.
- **`chain` with `--no-fixup` returns the correct answer and frees 97 reachable objects.** Explain how both of those can be true.
- `walk` crashes. What is different about `walk`?

**Q15.** Find the smallest `n` for which `chain.cy walk n --gc=gen --threshold=32 --no-fixup` crashes. Then explain what that value of `n` is measuring — it is a function of `threshold` and `promote_after`.

**Q16.** Watch the bet lose:

```bash
python3 runtime.py chain.cy chain 300 --gc=mark --threshold=64
python3 runtime.py chain.cy chain 300 --gc=gen  --threshold=64
```

- How many collections? How many objects freed?
- **The generational collector is slower here despite scanning fewer objects.** Look at its minor/major split and explain.
- What should a collector do when a collection reclaims nothing? *(This is PS 6 Part D3 — starting it here is encouraged.)*

---

## If You Finish Early

**Q17.** Run Q10's `victim.cy` under all three root policies and record **objects freed** and **objects scanned** for each. `--roots=scope` does not crash — it is safe, as advertised. It also frees **nothing at all**, while scanning four times as much as the precise policy. Explain both halves from the source of `victim`.

**Q18.** Find a Cyan program whose peak footprint under `--gc=rc` is *worse* than under `--gc=mark`. There is one in this folder already. Then find one where `rc` is worse and **no cycle is involved** — or argue that none exists, naming the property of `RefCount` you are relying on.

**Q19.** Add `-XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC` to the Java run. Epsilon allocates and never collects — it is `--gc=none`, in a production JVM. Predict what happens at `-Xmx256m` before you run it, then run it. Then work out roughly how large `-Xmx` would have to be for it to finish, and say why anyone ships a collector that does nothing.

---

## Before You Leave

Show the TA:

1. Your Q1 table, four collectors, and your Q3 answer about the two medians.
2. Your Q7 numbers — ZGC and G1 safepoints — and the factor in Q7.
3. Your Q10 answer: which object, which instruction.
4. Your Q14 table, all four runs, with the explanation of how a wrong collector printed a right answer.

---

*CS 211 · Week 6 · Lab 6 · © CSE Department*
