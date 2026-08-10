# CS 201 · Computer Organization & Architecture
## Week 4 · Lecture 3 of 3
### Locality as Leverage — Blocking a Real Kernel

---

**Reading:** CS:APP §6.5–6.6 · **Previous:** L14, cache organisation

---

## 1. The Kernel

Matrix transpose. Four lines, no arithmetic, nothing to optimise algorithmically:

```c
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        B[j*N + i] = A[i*N + j];
```

**It is the perfect cache exercise because it has no other content.** $N^2$ loads, $N^2$ stores, zero flops. Whatever the runtime is, it is memory behaviour.

**And it cannot be made to have good locality on both sides.** Read `A` sequentially and you write `B` by column; read `A` by column and you write `B` sequentially. **One of the two access patterns must stride.**

---

## 2. What It Costs

$N = 2048$, `double`, so each matrix is 32 MiB — five times the 6 MiB L3.

```
naive            0.0608 s   (1.00x)
blocked b=8      0.0250 s   (2.43x)
blocked b=16     0.0230 s   (2.65x)
blocked b=32     0.0185 s   (3.29x)
blocked b=64     0.0170 s   (3.58x)
```

*(Measured.)*

---

## 3. The Fix: Work in Tiles

Instead of completing whole rows, transpose one small square block at a time:

```c
for (int ii = 0; ii < N; ii += b)
    for (int jj = 0; jj < N; jj += b)
        for (int i = ii; i < ii+b && i < N; i++)
            for (int j = jj; j < jj+b && j < N; j++)
                B[j*N + i] = A[i*N + j];
```

**The same $N^2$ assignments in a different order.** No arithmetic changed, no memory saved.

**Why it works.** In the naive version, by the time the loop returns to the row of `B` it touched at the start, that line was evicted long ago — the intervening work touched 32 MiB. In the blocked version, a $b \times b$ tile touches $b$ lines of `A` and $b$ lines of `B`. For $b = 32$ that is $64 \times 64 = 4$ KiB, comfortably inside the 32 KiB L1d. **Every line fetched is fully used before it is evicted.**

**Choosing $b$:** big enough that whole 64-byte lines are used ($b \ge 8$ for `double`), small enough that $2b$ lines fit in L1. The measurements bear this out — $b=8$ already gets 2.43×, and the curve flattens by 64.

---

## 4. Where the Speedup Actually Comes From

The obvious guess is "fewer L1 misses". **The obvious guess is wrong**, and this is the most instructive measurement of the week.

`valgrind --tool=cachegrind` on the $N = 2048$ transpose:

| | D refs | D1 miss rate | **LLd miss rate** |
|---|---:|---:|---:|
| naive | 12 636 013 | 41.5% | **41.5%** |
| blocked $b=32$ | 12 636 160 | **42.5%** | **13.5%** |

*(Measured.)*

**Blocking made the L1 miss rate slightly *worse* — 42.5% against 41.5%.**

**What collapsed is the last-level miss rate: 41.5% → 13.5%**, from 5 244 472 misses to 1 705 595. A **3.07× reduction in accesses that reach DRAM.**

And the wall clock improved **3.29×**. *(Measured.)*

$$\text{3.07× fewer DRAM trips} \;\longrightarrow\; \text{3.29× faster}$$

> **In the naive version, LLd misses equal D1 misses almost exactly** — 5 244 472 against 5 244 694.
> **Every single L1 miss went all the way to DRAM.** The L2 and L3 caught nothing at all, because the
> stride was larger than any of them could span. Blocking is what let the lower levels start working.
>
> **The lesson: optimise for the level that is actually missing.** An L1 miss served by L2 costs ~12
> cycles. An L1 miss served by DRAM costs ~438. **They appear identically in the D1 miss rate**, and
> one is 36× worse than the other.

---

## 5. The Control That Proves It

Repeat everything at $N = 512$, where both matrices are 2 MiB and **both fit in the 6 MiB L3**:

| | wall clock | LLd misses |
|---|---:|---:|
| naive | 0.0035 s | 66 989 |
| blocked $b=32$ | 0.0026 s | 66 993 |

*(Measured.)*

**Only 1.35× faster, and the last-level miss counts are identical to four significant figures** — 66 989 against 66 993. Those are compulsory misses: the data must be read from memory once, and no reordering avoids that.

**Blocking did nothing at the last level because there was nothing to do.** The whole working set already fit. The residual 1.35× is L1 and L2 behaviour.

> **This is what a controlled experiment looks like**, and it is why the $N=2048$ result is
> believable. The intervention helps exactly when the theory says it should — when the working set
> exceeds the cache — and does nothing when it says it should not.

---

## 6. The General Technique

Blocking is not a matrix trick. It is one instance of a general move:

> **Restructure a computation so that its inner loop's working set fits in a fast level of the
> hierarchy, then reuse everything in that level before moving on.**

| Domain | The blocked version |
|---|---|
| Matrix multiply | Tiled multiply — the standard, worth 5–10× |
| Image processing | Tile the image, run the whole filter chain per tile |
| Databases | Blocked nested-loop join; sort-merge over runs sized to memory |
| Sorting | Merge sort with runs sized to L2, then merge |
| **Out-of-core work** | The same idea with disk as the slow level — Week 7 |

**The hierarchy repeats at every scale**, which is why this technique transfers: registers over L1, L1 over L3, DRAM over SSD, SSD over network. The constants change; the shape does not.

---

## 7. What Not to Do

**Do not block by default.** The naive transpose at $N=512$ is 1.35× off optimal and vastly clearer. Blocking adds two loop levels, a tunable parameter, and edge cases at the boundaries.

**Do not tune $b$ by guessing.** The measurements above took two minutes. Guessing takes longer and is usually wrong.

**Do not assume it transfers.** The best $b$ depends on cache size, line size, element size and the access pattern. A value tuned on one machine can be worse than naive on another.

**Measure first.** If your working set already fits, blocking buys you nothing and costs you clarity — §5 is the proof.

---

## 8. What to Take Away

1. **Transpose has no arithmetic**, so its runtime is pure memory behaviour.
2. **Blocking reorders the same work** so each fetched line is fully used before eviction.
3. **The speedup was 3.29×**, from tiling alone.
4. **It came from last-level misses (41.5% → 13.5%), not L1** — L1 got marginally *worse*.
5. **In the naive version every L1 miss reached DRAM.** L2 and L3 caught nothing.
6. **At $N=512$ everything fits, and blocking does nothing** — the control that makes the result credible.
7. **Fit the inner loop's working set into a fast level.** That is the whole technique, at every scale.

---

## Exercises

1. For `double` and a 32 KiB L1d, derive the largest $b$ for which two $b \times b$ tiles fit. Compare with the measured optimum.
2. Blocking made D1 misses *worse* but the program 3.29× faster. Explain how both can be true.
3. At $N=512$ the LLd miss counts differed by 4 out of 66 989. What kind of miss are those, and why can no reordering remove them?
4. Write the blocked loop for **matrix multiply** rather than transpose. How many arrays are live in the inner loop, and how does that change the tile-size calculation?
5. §7 warns that a tuned $b$ may not transfer. Given the L1 sizes 32 KiB and 48 KiB, compute the best $b$ for each and say how badly the wrong one performs.
6. The transpose reads `A` sequentially and writes `B` strided. Would swapping that — strided reads, sequential writes — be better, worse, or the same? Consider write-allocate from L14 §6 before answering.

---

*Next week: pipelining — and Midterm 1, covering Weeks 0–4.*
