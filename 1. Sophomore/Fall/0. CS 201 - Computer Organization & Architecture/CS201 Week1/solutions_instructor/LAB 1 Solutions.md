# CS 201 · Lab 1 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** These notes exist for the four checkpoints. Every figure was measured on the lab image
> (Ubuntu 24.04, GCC 13.3.0, Intel Core i5-8250U).

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — minimal case | 15 min | 10 min. Do not let it run long; Part 2 is the substance |
| 2 — absorption at scale | 30 min | 30 min, and 2.1 is the best question in the lab |
| 3 — `-ffast-math` | 20 min | 15 min. Dramatic, and fast once they run it |
| 4 — denormals | 25 min | 25 min. 4.1 is the one they should remember |

**If short of time, cut Part 1.1 and Part 5.** Never cut 2.1 or 4.1 — those are the two that teach measurement rather than floating point.

---

## Part 1 — The Minimal Case

```
(a+b)+c = 1.0
a+(b+c) = 0.0
```

*(Verified.)*

**Left:** $10^{16} - 10^{16} = 0$ exactly, then $0 + 1 = 1$ exactly. **Right:** $-10^{16} + 1$ needs $-9999999999999999$, which is not representable — near $10^{16}$ a `double`'s spacing is 2 — so it rounds back to $-10^{16}$, and the sum is 0. **The 1 was absorbed by the second operand before `a` was ever involved.**

### 1.1 — the boundary

`double` has 53 bits, so spacing near $2^k$ is $2^{k-52}$. Adding 1 stops working when spacing $> 2$, i.e. $k > 53$, i.e. around $9 \times 10^{15}$.

Students working in powers of ten will find both groupings still agree at `1e15` and diverge at `1e16`. **Accept that.** Push the strong ones to find the exact crossover at $2^{53} = 9\,007\,199\,254\,740\,992$ — where `x + 1 == x` becomes true for the first time.

**✅ CHECKPOINT 1** — both outputs, a boundary, and a theoretical prediction that matches.

---

## Part 2 — Absorption at Scale

```
exact (double, backward) : 16.695311366
float, forward           : 15.403682709   err -1.292e+00
float, backward          : 16.686031342   err -9.280e-03
float, Kahan             : 16.695310593   err -7.732e-07
```

*(Verified.)*

Say the ratios out loud, because the table understates them: **backward is 139× better than forward. Kahan is 1.7 million× better.**

### 2.1 — where it stops adding

Measured: **7 902 849 of 10 000 000 terms — 79.0% — change nothing. First absorbed index $i = 2\,097\,152$.**

Derivation:

$$\text{spacing near }16 = 16 \times 2^{-24} = 9.5367\times10^{-7}$$
$$\frac{1}{i} \le \frac{9.5367\times10^{-7}}{2} \;\Longrightarrow\; i \ge 2\,097\,152 = 2^{21}$$

**And $1/2^{21} = 4.76837\times10^{-7}$ is exactly half the spacing.** *(Verified.)* The agreement is exact, not approximate — worth pointing at, because students expect numerical arguments to be hand-wavy.

> **The factor of two is the whole question.** Everyone finds the ULP; roughly half forget that
> round-to-nearest needs the addend to exceed *half* an ULP before it moves the result. They will get
> $2^{22}$ and think they are within rounding error of correct. They are off by exactly 2×, and the
> measurement says so.

### 2.2 — is backward always better?

**No.** The technique is **ascending magnitude**, not reversal. The harmonic series happens to be descending, so reversing it sorts it. For $1, 2, 3, \ldots, n$, reversing makes it worse. For randomly ordered magnitudes, reversal does nothing systematic.

> Expect "always sum backwards" from most of the room. It is the single most important thing to
> correct in this lab, because it is a rule they will carry into real code and it is wrong.

**✅ CHECKPOINT 2** — the four sums, dead count, first index, and a correct answer on 2.2.

---

## Part 3 — `-ffast-math` Deletes the Correction

| Build | Kahan result | Error |
|---|---|---:|
| `-O2` | 16.695310593 | $-7.7\times10^{-7}$ |
| `-O2 -ffast-math` | **15.403682709** | $-1.292$ |

*(Verified.)* **The `-ffast-math` Kahan result is bit-identical to the naive forward sum.** Show them that line twice — it is not "less accurate", it is *exactly* the algorithm they were trying not to write.

**The assumption:** `-ffast-math` permits treating FP addition as associative. Then `c = (t - s) - y` with `t = s + y` is provably $(s + y - s) - y = 0$, so `y = 1.0f/i - c` is just `1.0f/i`, and the compensation is dead code.

**If a student asks how to protect it:** `volatile float c;`, or a separate translation unit without the flag, or `#pragma GCC optimize("no-fast-math")`. All three work; the first is the usual answer and costs a memory round-trip per iteration.

**✅ CHECKPOINT 3** — the two Kahan values and a correct statement of the assumption.

---

## Part 4 — Denormals

```
rep0 normal 0.00348 s | denormal 0.11876 s | ratio 34.15x
rep1 normal 0.00358 s | denormal 0.12053 s | ratio 33.70x
rep2 normal 0.00389 s | denormal 0.11906 s | ratio 30.63x
```

*(Verified.)* **Same instructions, same count, ~34× the time.** The only difference is the bit patterns in the array.

`-fno-tree-vectorize` is in the build line deliberately — without it, vectorisation changes both loops and muddies the comparison. If a student drops it, the ratio moves; have them put it back and explain why it is there.

### 4.1 — the benchmark that measured nothing

The failed version:

```c
float x = FLT_MIN, s = 0;
for (long i = 0; i < n; i++) { x *= 0.999f; s += x; }
```

reported **1.00×** — no effect. *(This really was the first attempt, and it really did measure nothing.)*

**Why:** starting at `FLT_MIN` and multiplying by 0.999 walks *down* through the denormal range and reaches zero within a few thousand iterations. The remaining ~20 million iterations multiply and add **zeros**, which take the fast path. The denormal region is a vanishing fraction of the runtime, so it disappears into the noise.

**The general rule, which is the point of 4.1:** *a benchmark that shows no effect is usually measuring the wrong thing, not disproving the effect.* Before believing a null result, confirm the code spent its time where you think it did.

> Ask the room: **how would you have caught this without already knowing the answer?** Good answers:
> print the values partway through; count how many iterations are actually denormal; check the sum is
> not zero. All three would have exposed it in seconds.

### 4.2 — flush-to-zero

```
rep0 normal 0.00513 s | denormal 0.00448 s | ratio 0.87x   (denormal sum = 0)
rep1 normal 0.00413 s | denormal 0.00413 s | ratio 1.00x   (denormal sum = 0)
rep2 normal 0.00445 s | denormal 0.00420 s | ratio 0.94x   (denormal sum = 0)
```

*(Verified.)* **The penalty is gone — and so is the answer.** The denormal sum was $1.4\times10^{-36}$ without the flag and is **exactly 0** with it.

**What was given up: gradual underflow.** With FTZ, `a != b` no longer implies `a - b != 0`, so a guarded division can divide by zero. That is precisely the failure denormals were introduced to prevent. **The 34× is real and so is the cost** — this is the trade, stated plainly, and it is the right note to end the lab on.

**✅ CHECKPOINT 4** — three ratios, the 4.1 explanation, and the FTZ result *including* noticing that the sum became zero.

---

## What Success Looks Like

By the end, a student should be able to say:

1. Which addition in `a+(b+c)` destroyed the information, and why.
2. That 79% of a ten-million-term sum can contribute nothing, and predict where that starts.
3. That a compiler flag can delete a numerical algorithm without warning.
4. That a null benchmark result is a claim requiring evidence, not evidence itself.

**Item 4 is the transferable one.** The floating-point specifics get retaught in every numerical course they will take; the measurement discipline does not.

---

*CS 201 · Week 1 · Lab 1 Solutions · Instructor Only*
