# CS 201 · Lab 4 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints. All figures measured on the lab image.

---

## Before the Session: the `perf` Problem

**`perf` does not work for unprivileged users on the lab image.**

```
$ cat /proc/sys/kernel/perf_event_paranoid
4
```

At paranoid level 4, `perf stat -e cache-misses` returns a permissions message, not data. Fixing it needs root:

```bash
sudo sysctl kernel.perf_event_paranoid=1
```

**Raise this with the lab administrator before the session if you want `perf` available** — it is genuinely better than cachegrind for Part 5, because it counts real events including prefetcher behaviour. **The lab as written does not depend on it**, and cachegrind is arguably the better teaching tool here anyway: it is deterministic, so every student gets the same numbers.

**Say all of this to the room.** "The tool the curriculum names is unavailable and here is why, here is the substitute, and here is what the substitute cannot see" is a more useful lesson than a working `perf` would have been.

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — geometry | 10 min | 10 min |
| 2 — find the cliffs | 30 min | 30 min. **The best part of the lab** |
| 3 — the line | 20 min | 15 min |
| 4 — 30× | 15 min | 10 min |
| 5 — where the speedup comes from | 35 min | **Protect this.** The surprise is the point |

**Cut Part 3 if short**, not Part 5.

---

## Part 1

$64 \times 8 \times 64 = 32$ KiB · $1024 \times 4 \times 64 = 256$ KiB · $8192 \times 12 \times 64 = 6$ MiB. All ✓.

1. **6 bits offset, 6 bits set index** (L1d).
2. $S \times B = 64 \times 64 = \mathbf{4096}$ bytes.
3. **`ONE-SIZE` is per core**, and a single-threaded program runs on one core. `ALL-SIZE` (128K) is four private 32 KiB caches, not a shared 128 KiB one — the distinction matters again in Week 10.

**✅ CHECKPOINT 1**

---

## Part 2

| KiB | ns | KiB | ns |
|---:|---:|---:|---:|
| 4 | 1.22 | 512 | 9.27 |
| 8 | 1.22 | 1024 | 12.12 |
| 16 | 1.19 | 2048 | 14.83 |
| **32** | **1.22** | 4096 | 30.39 |
| 64 | 2.50 | **8192** | **81.81** |
| 128 | 3.40 | 16384 | 113.54 |
| 256 | 5.67 | 32768 | 128.94 |

*(Verified.)*

### 2.1 / 2.2

Cliffs at **32 KiB, ~256 KiB, ~6 MiB** — all three matching Part 1. Cycles at 3.4 GHz: **4.1 / 11.6 / 41.2 / 438**, against canonical 4 / 12 / 40 / 200+.

> **Point out how good the agreement is.** Students expect textbook constants to be rough. These are
> not — and finding them with nothing but a stopwatch is the most satisfying thing in the course so
> far. Let it land.

### 2.3 — the sequential cycle

| KiB | random | sequential |
|---:|---:|---:|
| 4 | 1.22 | 1.39 |
| 32 | 1.22 | 1.19 |
| 256 | 5.67 | 1.21 |
| 2048 | 14.83 | 1.33 |
| 8192 | 81.81 | 1.52 |
| 32768 | 128.94 | **1.55** |

*(Verified.)* **The staircase is gone. 83× faster at 32 MiB on the identical working set.**

**Mechanism:** the hardware prefetcher recognises the constant stride and fetches ahead, so lines are resident before they are demanded. Latency is entirely hidden.

**The question to put to the room:** *if the hardware can do that, why does the rest of the lab matter?* Good answers: prefetching hides latency but not bandwidth; only regular patterns are predictable, and lists, trees and hash tables are not; and a prefetcher that correctly predicts a wasteful pattern still wastes the bandwidth.

**✅ CHECKPOINT 2**

---

## Part 3

Cost per access rises to stride 16 (= 64 bytes) and flattens: 0.85 → 11.06 → 18.32 → 19.42 ns. *(Verified.)*

**The plateau:** below stride 16 every stride touches **the same number of lines** — you fetch the whole 64-byte line whether you use 16 `int`s of it or one. Past stride 16 you begin skipping lines entirely, so the count of lines finally falls and the per-access cost stops rising.

**At stride 4 you use 1/4 of each line; at stride 8, 1/8. You paid identically for both.**

**✅ CHECKPOINT 3**

---

## Part 4

```
row-major   0.0086 s    col-major   0.3099 s    ratio 35.98x
```

*(Verified; a repeat run gave 28.71×. Tell them the variance is expected and the effect is not.)*

**In the assembly the two loops are nearly identical** — same instructions, same count, differing only in which register indexes which. **Nothing about the code explains a 30× gap.** That is the whole point of the exercise, and it is the moment Week 4 justifies itself.

**✅ CHECKPOINT 4**

---

## Part 5 — the important one

### 5.1

```
naive 0.0608 s | b=8 2.43x | b=16 2.65x | b=32 3.29x | b=64 3.58x
```

### 5.2

| | D1 miss rate | LLd miss rate |
|---|---:|---:|
| naive | 41.5% | **41.5%** |
| blocked $b=32$ | **42.5%** | **13.5%** |

*(Verified.)*

**Let them sit with "blocking made D1 worse" before explaining.** Most of the room will have predicted the opposite, confidently.

**Answers:**

1. **From the last level.** LLd misses fell 5 244 472 → 1 705 595, a **3.07× reduction in DRAM trips**, which produced the 3.29× wall-clock gain. The extra L1 misses are served by L2/L3 at ~12–41 cycles and are nearly free by comparison.
2. **LLd ≈ D1 in the naive run means every L1 miss went all the way to DRAM.** L2 and L3 contributed nothing at all — the stride outran all of them.
3. **D1 miss rate is a bad optimisation target on its own.** It counts a 12-cycle L2 hit and a 438-cycle DRAM trip identically. **Ask which level is missing, not how many misses there are.**

### 5.3 — the control

```
N=512:  naive 0.0035 s (LLd 66,989)   blocked 0.0026 s (LLd 66,993)
```

*(Verified.)*

Those ~67 000 are **compulsory** misses — each matrix must be read once, and no loop reordering removes a first touch.

**Why this makes the N=2048 result stronger:** blocking removes *capacity* misses. At $N=512$ everything fits in L3, so there were none to remove, and it did nothing. **An intervention that helps exactly when its mechanism applies, and not otherwise, is evidence the mechanism is real.** One that helped everywhere would be suspicious.

> **Do not let them leave without this.** It is the difference between "blocking is a trick that makes
> things faster" and "blocking removes capacity misses, so establish you have capacity misses first."
> Midterm 1 asks a version of it.

**✅ CHECKPOINT 5**

---

## What Success Looks Like

1. Derive a cache's capacity from $S \times E \times B$ and locate the cliffs by timing.
2. Explain the 64-byte line from a stride curve.
3. Say why loop order alone is worth 30×.
4. **Read D1 and LLd miss rates and say which level is the problem.**
5. **Recognise a null result as evidence.**

Items 4 and 5 are what separates this from a lab about caches. They are about diagnosis, and Week 11 assumes both.

---

*CS 201 · Week 4 · Lab 4 Solutions · Instructor Only*
