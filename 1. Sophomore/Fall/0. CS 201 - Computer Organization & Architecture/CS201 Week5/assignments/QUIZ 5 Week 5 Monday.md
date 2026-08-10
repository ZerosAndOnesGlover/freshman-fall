# CS 201 · Quiz 5
## Administered: Monday, Week 5 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 4** — the memory hierarchy, cache organisation, and locality.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first.
>
> **Midterm 1 is this evening, 18:00, VNC 100.** This quiz is deliberately drawn from the section of
> the paper worth the most marks.

---

**Q1.** A cache has $S = 64$, $E = 8$, $B = 64$. Give its capacity and the number of set-index bits.

&nbsp;

&nbsp;

---

**Q2.** What byte stride makes every access land in the same set of that cache?

&nbsp;

&nbsp;

---

**Q3.** Two loops sum the same matrix; one is 30× slower. Both compile to nearly identical instructions. Why?

&nbsp;

&nbsp;

---

**Q4.** Classify: repeatedly traversing a 20 MiB linked list in random order, on a machine with a 6 MiB L3.

&nbsp;

&nbsp;

---

**Q5.** Blocking a transpose made the D1 miss rate go **up** (41.5% → 42.5%) and the program 3.29× **faster**. How?

&nbsp;

&nbsp;

---

**Q6.** Why does writing to an array you never read still cause it to be read?

&nbsp;

&nbsp;

---

**Q7.** At $N = 512$ blocking gave only 1.35×, and the last-level miss counts were identical. Why is that *good* evidence rather than a disappointing result?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** $64 \times 8 \times 64 = 32\,768 =$ **32 KiB**. Set-index bits $= \log_2 64 =$ **6**.

*(Offset bits are also 6. Tag is the remaining 52.)*

---

**Q2.** $S \times B = 64 \times 64 =$ **4096 bytes**.

In `double`s that is a row length of 512 — which is why `double A[512][512]` is the standard pathological case.

---

**Q3.** **C is row-major**, so the first loop walks memory sequentially and the second strides by a full row.

A 64-byte line holds 16 `int`s. **The row-major loop uses all 16; the column-major loop uses one and abandons the rest**, and the line is evicted long before it returns. Same lines fetched, 1/16 of the value extracted.

*(Measured: 0.0086 s against 0.3099 s — ~30×, identical work and identical result.)*

---

**Q4.** **Capacity.** 20 MiB exceeds the 6 MiB L3, and the random order defeats any reuse.

*Not conflict — the problem is not where lines map, it is that there are too many of them. Not compulsory — the traversal is repeated, so reuse was possible in principle.*

---

**Q5.** **The extra L1 misses were cheap and the avoided DRAM trips were expensive.**

An L1 miss served by L2 costs ~12 cycles; one served by DRAM costs ~438 — **36× more** — and both are counted identically in "D1 miss rate". The **last-level** rate collapsed 41.5% → 13.5%, a 3.07× reduction in DRAM trips, and that is where the 3.29× came from.

**Ask which level is missing, not how many misses there are.**

---

**Q6.** **Write-allocate.** On a write miss the line is fetched into the cache first, then written into.

This is why initialising a large buffer costs a full read of it, and why non-temporal stores (`movnt*`) exist — they bypass the cache to avoid exactly this.

---

**Q7.** **Blocking removes capacity misses. At $N = 512$ both matrices fit in the 6 MiB L3, so there were none to remove** — the ~67 000 last-level misses are compulsory, and no reordering avoids a first touch.

**An intervention that helps exactly when its stated mechanism applies, and does nothing when it does not, is evidence the mechanism is real.** One that helped under all conditions would suggest the measurement, not the mechanism, was doing the work.

---

### Before Tonight

| If you missed | Reread, then check the revision guide |
|---|---|
| Q1, Q2 | L14 §1–§2 |
| Q3, Q6 | L13 §6, L14 §6 |
| Q4 | L14 §4 |
| **Q5, Q7** | **L15 §4–§5 — worth 6 of the paper's 24 memory marks** |

**Q5 and Q7 are Midterm Q4(e).** If either was shaky, spend twenty minutes on L15 §4–§5 this afternoon and nothing else.

---

*CS 201 · Week 5 · Quiz 5 · covers Week 4 · ungraded*
