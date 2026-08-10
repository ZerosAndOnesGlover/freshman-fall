# CS 201 · Week 1 · Lab 1
## Demonstrating Floating-Point Non-Associativity

---

**When:** **Tuesday of Week 2**, 15:00–16:50, BH 210 — *after* Week 1's three lectures
**Covers:** Week 1 · **Assessment:** unmarked, checked off by the TA
**Prerequisite:** Lab 0's toolchain. You will need `gcc`, `objdump` and `python3`.

---

## What This Lab Is For

Lecture 6 asserted that floating-point addition is not associative, that summation order changes the answer by percent-level amounts, and that denormals are slow. **You are going to measure all three yourself**, and then find the case where the compiler quietly changes your answer.

**No report.** Show the TA at each **✅ CHECKPOINT**.

---

## Part 1 — The Minimal Case (15 min)

```c
#include <stdio.h>

int main(void) {
    double a = 1e16, b = -1e16, c = 1.0;
    printf("(a+b)+c = %.1f\n", (a + b) + c);
    printf("a+(b+c) = %.1f\n", a + (b + c));
    return 0;
}
```

```bash
gcc -O0 -o assoc assoc.c && ./assoc
```

Expected:

```
(a+b)+c = 1.0
a+(b+c) = 0.0
```

*(Verified.)*

**Before moving on, explain it out loud to the person next to you.** Which grouping loses the 1, and at what step? If you cannot say which single addition destroyed the information, reread L06 §2 — the rest of this lab builds on it.

### 1.1 Find the boundary

Replace `1e16` with smaller values — `1e15`, `1e14`, and so on — and find the largest magnitude at which both groupings still agree.

**Then predict it from theory** before you look: `double` has 53 bits of mantissa, so the spacing of representable values near $2^k$ is $2^{k-52}$. Adding 1 does nothing once that spacing exceeds 2.

**✅ CHECKPOINT 1** — both outputs, the boundary you found, and the value theory predicts.

---

## Part 2 — Absorption at Scale (30 min)

Now the version that matters. Sum $\sum_{i=1}^{10^7} 1/i$ four ways:

```c
#include <stdio.h>
#define N 10000000

int main(void) {
    float naive = 0;
    for (long i = 1; i <= N; i++) naive += 1.0f / i;

    float back = 0;
    for (long i = N; i >= 1; i--) back += 1.0f / i;

    float s = 0, c = 0;
    for (long i = 1; i <= N; i++) {
        float y = 1.0f / i - c;
        float t = s + y;
        c = (t - s) - y;
        s = t;
    }

    double exact = 0;
    for (long i = N; i >= 1; i--) exact += 1.0 / i;

    printf("exact (double, backward) : %.9f\n", exact);
    printf("float, forward           : %.9f   err %.3e\n", (double)naive, naive - exact);
    printf("float, backward          : %.9f   err %.3e\n", (double)back,  back  - exact);
    printf("float, Kahan             : %.9f   err %.3e\n", (double)s,     s     - exact);
    return 0;
}
```

```bash
gcc -O2 -o sums sums.c && ./sums
```

Measured on the lab machine:

```
exact (double, backward) : 16.695311366
float, forward           : 15.403682709   err -1.292e+00
float, backward          : 16.686031342   err -9.280e-03
float, Kahan             : 16.695310593   err -7.732e-07
```

*(Verified.)*

**The forward float sum is wrong by 7.7%** — in the second digit, not the last.

### 2.1 Find where it stops adding

Instrument the forward loop: count how many iterations leave the accumulator **completely unchanged**.

```c
float s = 0; long dead = 0;
for (long i = 1; i <= N; i++) {
    float before = s;
    s += 1.0f / i;
    if (s == before) dead++;
}
printf("%ld of %d terms changed nothing (%.1f%%)\n", dead, N, 100.0 * dead / N);
```

Find the **first** $i$ at which the term is absorbed, and compare it with theory: the spacing of floats near 16 is $16 \times 2^{-24} \approx 9.5 \times 10^{-7}$, and a term smaller than half that rounds away.

### 2.2 Why backward is better, and why it is not enough

Backward summation is **139× more accurate here for zero cost**. Explain why in one sentence.

Then answer the harder question: **is backward summation always better?** Construct — or argue for — a sequence where it is not.

**✅ CHECKPOINT 2** — the four sums, your dead-term count and first absorbed index, and your answer on backward summation.

---

## Part 3 — The Compiler Deletes Your Correction (20 min)

Kahan summation depends on `(t - s) - y` **not** being zero. Under real-number algebra it is zero. So:

```bash
gcc -O2              -o sums_safe sums.c && ./sums_safe
gcc -O2 -ffast-math  -o sums_fast sums.c && ./sums_fast
```

**Compare the Kahan line between the two builds.** Then look at why:

```bash
objdump -d --no-show-raw-insn -M intel sums_fast | sed -n '/<main>:/,/ret/p' | head -60
```

`-ffast-math` tells the compiler it may treat floating-point arithmetic as associative. Under that assumption `c` is provably always 0, the compensation is dead code, and it is removed. **Your careful algorithm becomes the naive one.**

> This is Week 0's lesson again in a more expensive form. In Week 0 the compiler deleted a loop and
> the answer stayed right. Here it deletes a correction and the answer goes wrong — **silently, with
> no warning, in a build flag someone else may have set in the project's makefile.**

**✅ CHECKPOINT 3** — the two Kahan results side by side, and a one-sentence statement of what `-ffast-math` assumed.

---

## Part 4 — Denormals Are Slow (25 min)

```c
#include <stdio.h>
#include <time.h>
#include <float.h>
#define N 2000000
static float A[N], B[N];
static double now(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}
int main(void) {
    for (long i = 0; i < N; i++) {
        A[i] = 1.0f + i * 1e-6f;                 /* normal   */
        B[i] = FLT_TRUE_MIN * (1 + (i % 1000));  /* denormal */
    }
    volatile float sink;
    for (int rep = 0; rep < 3; rep++) {
        double t0 = now(); float s = 0;
        for (long i = 0; i < N; i++) s += A[i] * 1.0000001f;
        double t1 = now(); sink = s;

        double t2 = now(); float d = 0;
        for (long i = 0; i < N; i++) d += B[i] * 1.0000001f;
        double t3 = now(); sink = d;

        printf("rep%d normal %.5f s | denormal %.5f s | ratio %.2fx\n",
               rep, t1 - t0, t3 - t2, (t3 - t2) / (t1 - t0));
    }
    (void)sink; return 0;
}
```

```bash
gcc -O2 -fno-tree-vectorize -o denorm denorm.c && ./denorm
```

Measured on the lab machine:

```
rep0 normal 0.00348 s | denormal 0.11876 s | ratio 34.15x
rep1 normal 0.00358 s | denormal 0.12053 s | ratio 33.70x
rep2 normal 0.00389 s | denormal 0.11906 s | ratio 30.63x
```

*(Verified.)* **Identical instructions, identical instruction count, 34× the time** — purely because of the *values* in the array.

### 4.1 A benchmark that measured nothing

The first attempt at this measurement used a decaying loop:

```c
float x = FLT_MIN, s = 0;
for (long i = 0; i < n; i++) { x *= 0.999f; s += x; }
```

and reported a ratio of **1.00×** — no effect at all.

**Work out why**, then say what general rule it illustrates. *(Hint: what is `x` after a few thousand iterations, and how fast is arithmetic on that?)*

> **This is the most useful thing in the lab.** A benchmark showing no effect is usually measuring the
> wrong thing, not disproving the effect. Week 11 is three hours of this.

### 4.2 The industry fix

```bash
gcc -O2 -fno-tree-vectorize -ffast-math -o denorm_ftz denorm.c && ./denorm_ftz
```

Among its many effects, `-ffast-math` enables flush-to-zero. **What happened to the ratio, and what did you give up to get it?**

**✅ CHECKPOINT 4** — your three ratios, your explanation of the failed benchmark, and the flush-to-zero result.

---

## Part 5 — Optional

Add `-fsanitize=undefined` to L04's `always_true(INT_MAX)` and watch it report the signed overflow at run time. It is the tool that finds this class of bug in code you did not write.

---

## Before You Leave

| Claim | You should now have measured |
|---|---|
| Addition is not associative | 1.0 vs 0.0 |
| Order changes accuracy | 7.7% error, and 139× from reversing a loop |
| Compensation recovers it | 1.7 million× |
| …unless the compiler removes it | `-ffast-math` |
| Denormals are slow | ~34× |
| Benchmarks lie | the 1.00× that was wrong |

**The habit:** when someone tells you a floating-point result is "close enough", ask how they know. The tools to find out are the ones you just used.

---

*CS 201 · Week 1 · Lab 1*
