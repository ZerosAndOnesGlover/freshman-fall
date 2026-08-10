# CS 201 · Midterm 1 — Solutions and Mark Scheme
## Instructor Only

---

> **Not for distribution before the paper is returned.** All quoted measurements are from the lab
> machine and appear in the Weeks 0–4 lectures.
>
> **Marking principle: method over answer.** A correct approach with an arithmetic slip keeps most of
> the marks. A correct number with no working, on a question that says "show your working", keeps
> none.

---

## Q1 — Representation (20)

### (a) [4]

**[2]** `10000000` = $-128$. Negating: invert → `01111111`, add 1 → `10000000` = **$-128$**, unchanged.

**[2]** There is exactly **one** zero, so of 256 patterns one is spent on 0 and the remaining 255 split 127 positive / 128 negative. $+128$ has no representation.

### (b) [6] — 3 each

**`f`:** signed overflow is **undefined**, so the compiler may assume it never occurs. Under that assumption `x + 1 > x` is always true and the expression is a constant.

**`g`:** unsigned overflow is **defined** as modulo $2^{32}$, so `UINT_MAX + 1 == 0` and the comparison is genuinely false for exactly one input. It must be tested.

> **Require "may assume it never happens" or equivalent.** "Anything can happen with UB" does not
> explain the specific code and scores 3 of 6.

### (c) [4]

`1.5 = 1.1₂ × 2⁰` → $s = 0$, stored exponent $= 127$, unbiased $= 0$, mantissa $=$ `100…0`.

**Binary:** `0 01111111 10000000000000000000000` · **Hex:** `0x3fc00000`

*(1 for each of binary, hex, exponent pair, mantissa.)*

### (d) [3]

**[2]** The leading 1 of a normalised binary number is **implicit** — every normalised value starts with 1, so storing it would waste a bit. 23 stored + 1 implied = 24.

**[1]** **$2^{24} = 16\,777\,216$.** Adding 1 there rounds back to itself.

### (e) [3]

**[2]** The **inner** addition, $b + c$. $-10^{16} + 1$ needs $-9999999999999999$, not representable — near $10^{16}$ a `double`'s spacing is 2 — so it rounds back to $-10^{16}$.

**[1]** The 1 was **absorbed before `a` was ever involved**; then $a + (-10^{16}) = 0$.

> Award 1 if they identify absorption but pick the wrong addition.

---

## Q2 — Assembly (22)

### (a) [4]

**[2]** `[base + index × scale + displacement]`; scale ∈ **{1, 2, 4, 8}**.
**[2]** `QWORD PTR [rdi + rcx*8]`.

### (b) [4]

**[2]** `rax = rdi × 5`, and **zero** memory accesses — `lea` computes the address expression and stores the value.
**[2]** `lea rax, [rdi+rdi*8]`.

### (c) [5]

**[2]** $\texttt{0x80000000} - 1 = \texttt{0x7FFFFFFF}$: **ZF = 0, SF = 0, CF = 0, OF = 1.**

**[2]** `jl` **branches** (SF ≠ OF). `jb` **does not** (CF = 0).

**[1]** The same bits are $-2^{31}$ signed and $+2^{31}$ unsigned. `jl` reads SF/OF, `jb` reads CF — **the jump chooses the interpretation.**

> The most common error is CF and OF swapped. Award the [2] for the jumps if they follow correctly
> from the student's own (wrong) flags.

### (d) [5]

**[3]** `sar` rounds toward $-\infty$; C's `/` truncates toward zero. They differ only for negatives: $-17 \gg 3 = -3$ but $-17/8 = -2$. Adding $2^3 - 1 = 7$ before the shift converts floor to truncation. The `test`/`cmovns` applies the bias **only when `x` is negative**.

**[2]** `unsigned x / 8` → **`shr eax, 0x3`**, a single instruction: unsigned division has no negative case, so no correction is needed.

### (e) [4]

**[2]** `ja` is an **unsigned** comparison. A negative `x` reinterpreted as unsigned is $\ge 2^{31}$, hence above 6, so the branch is taken. **One comparison bounds both sides**, the lower folding into the upper.

**[2]** **Signed/unsigned conversion** — the same rule that makes `strlen(s) - 1` enormous on an empty string, used deliberately.

---

## Q3 — Procedures and the Stack (20)

### (a) [4]

| Offset | Contents |
|---|---|
| `rbp+8` | return address |
| `rbp+0` | saved `rbp` |
| `rbp-8` | saved `rbx` |
| `rbp-0x10` | padding / unused |
| `rbp-0x18` | `n` |

$8 + 8 + 8 + 24 = 48$ ✓ *(the `sub rsp,0x18` reserves 24 for one 8-byte local; the rest is alignment padding).*

### (b) [5]

**[3]** `fib(n-1)` returns in `rax`, which is **caller-saved**, so instruction `36`'s `call` may destroy it. The value must survive that call, so it moves to `rbx`, which is **callee-saved** and therefore restored by any callee.

**[2]** With `r10`: it **assembles and links cleanly** — `r10` is also caller-saved, so nothing preserves it. **It is wrong**, and *(measured)* first fails at $n = 4$, returning 2 instead of 3.

> Full credit for "it would compile but give wrong answers" without the specific $n$.

### (c) [4]

**[2]** `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`.
**[1]** Argument 7 is at **`[rsp+8]`** on entry — `[rsp]` holds the return address.
**[1]** **The caller** removes it.

### (d) [4]

**[2]** `rsp ≡ 0 (mod 16)` **immediately before `call`**; hence `≡ 8 (mod 16)` on entry.

**[2]** **`sub rsp, 8`.** Entry is `≡ 8`; each push flips the parity, so **two** pushes return it to `≡ 8` — still misaligned. Eight more bytes are needed.

> **This is the single most-failed part of the paper.** Award both marks only for the parity argument;
> a correct number with the reasoning "two pushes is 16 bytes so it's fine" gets 1.

### (e) [3]

**[2]** **Nothing.** `ret` is `pop rip` — no hardware check that the value is a legitimate return address.

**[1]** Any of: **stack canary**, **ASLR**, **NX / non-executable stack**, **shadow stack / CET**.

---

## Q4 — The Memory Hierarchy (24)

### (a) [4]

$64 \times 8 \times 64 = 32\,768 =$ **32 KiB**; **6** offset bits; **6** set-index bits.

### (b) [4]

**[2]** $S \times B = 64 \times 64 =$ **4096 bytes**.
**[2]** $4096 / 8 =$ **512 `double`s** per row.

### (c) [4] — 1, 1.5, 1.5

1. **Compulsory** — never referenced before.
2. **Capacity** — 20 MiB exceeds the 6 MiB L3, and random order defeats reuse.
3. **Conflict** — only 8 KiB of data in a 32 KiB cache, so capacity is ample, but the 32 KiB separation maps both arrays to identical sets and direct-mapped allows one line per set.

### (d) [6]

**[3]** C is **row-major**: `m[i][j]` and `m[i][j+1]` are adjacent. The first loop walks memory sequentially; the second strides by $N \times 4$ bytes.

**[3]** A 64-byte line holds **16 `int`s**. The row-major loop uses **all 16** of every line it fetches. The column-major loop uses **one** and abandons the rest, and by the time it returns to that row the line has long been evicted. **Same number of lines fetched; 1/16 of the value extracted.**

> Full marks require the line size and the fraction used. An answer that says only "poor locality"
> scores 3.

### (e) [6]

**1. [3]** An L1 miss caught by L2 costs ~12 cycles; one reaching DRAM costs ~438 — **36× more** — and **both are counted identically in the D1 miss rate.** Blocking traded a small number of extra cheap L1 misses for a **3.07× reduction in DRAM trips**, which is where the 3.29× came from.

**2. [3]** LLd ≈ D1 means **essentially every L1 miss also missed L2 and L3 and went to DRAM** — the lower levels contributed nothing, because the stride outran all of them. **Aim the optimisation at the level that is actually missing:** the naive version's problem was never L1.

> This is the highest-value pair on the paper and separates the class. Award generously for the
> distinction between *where a miss is served*; do not require the exact cycle figures.

---

## Q5 — Synthesis (14)

### (a) [5]

**[2]** $100\,000 \times 96 / 64 =$ **150 000 lines**, of which 4 bytes in every 96 are used.

**[2]** **Struct-of-arrays**: a contiguous array of the 4-byte field is $100\,000 \times 4 = 400\,000$ bytes $= $ **6250 lines**. **24× fewer.**

**[1]** Any: a single element is no longer one object; updates must touch several arrays consistently; poor locality for code that reads all fields of one element; the type system no longer groups the fields.

### (b) [5]

**Marks are for the order and the reasoning.** A defensible sequence:

1. **Time it, and time a part of it** — establish there is a problem and locate the fraction that matters. *(Amdahl: optimising 5% is worth at most 5.3%.)*
2. **Check the memory behaviour** — cachegrind, D1 **and** LL. Rules in or out the difference between compute-bound and memory-bound, which determines every subsequent decision.
3. **Look at what was compiled** — `objdump`. Rules in or out the possibility that the source and the machine code differ in the way that matters *(vectorised or not, branch or `cmov`, loop present at all)*.

> Accept any order that **measures before changing** and that separates *how much* from *where* from
> *why*. **Deduct heavily for starting with a code change**, and for any answer that begins by
> guessing the cause.

### (c) [4]

**[2]** `n` was a compile-time constant, so GCC **evaluated the entire loop during compilation** and emitted the result as a single immediate — `movabs rdx,0x11c3793adb7080`, which is 5000000050000000. The two clock readings ended up adjacent with nothing between them. The loop **is not in the program**.

**[2]** **A benchmark measures what the compiler left, not what you wrote.** Verify that the work still exists — by disassembling, or by making the input opaque to the optimiser — before believing any timing.

---

## Mark Summary and Expected Distribution

| | | Expected mean |
|---|---:|---:|
| Q1 Representation | 20 | ~14 |
| Q2 Assembly | 22 | ~15 |
| Q3 Procedures | 20 | ~13 |
| Q4 Memory Hierarchy | 24 | ~14 |
| Q5 Synthesis | 14 | ~8 |
| **Total** | **100** | **~64** |

**Where marks will be lost, in order:**

1. **Q3(d)** — the alignment parity. Expect over half the class to say two pushes need no `sub`.
2. **Q4(e)** — explaining the speedup without engaging that D1 went *up*.
3. **Q1(b)** — describing UB generally instead of explaining the two code generations.
4. **Q2(c)** — CF and OF interchanged.
5. **Q5(b)** — proposing a fix before proposing a measurement.

**Items 1 and 2 should be worked through in the Week 6 lecture**, since both recur: alignment in every hand-written assembly exercise, and miss-level diagnosis throughout Weeks 10 and 11.

---

*CS 201 · Midterm 1 Solutions · Instructor Only*
