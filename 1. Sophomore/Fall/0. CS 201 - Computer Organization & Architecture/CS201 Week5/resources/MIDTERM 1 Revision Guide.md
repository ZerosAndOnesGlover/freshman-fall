# CS 201 · Midterm 1 Revision Guide
## Weeks 0–4 · 75 minutes · 100 points · 12.5%

---

**Week 5, Monday, 18:00–19:15, VNC 100.**
**One handwritten A4 sheet, one side.** No calculator, no devices.

---

## What Is Actually Examined

Five questions, and the shape is stable:

| | Topic | Marks | Source |
|---|---|---:|---|
| Q1 | Representation | 20 | Week 1 |
| Q2 | Assembly | 22 | Week 2 |
| Q3 | Procedures and the stack | 20 | Week 3 |
| Q4 | The memory hierarchy | 24 | Week 4 |
| Q5 | Synthesis | 14 | All weeks |

**Week 0 is not a section of its own** — it appears inside Q5 and as the vocabulary the other questions assume.

**Roughly 40 of the 100 marks are "explain why".** Not recall. If you can state a fact but not say what it is *for*, you will lose those marks. Practise saying things out loud.

---

## What to Put on Your Sheet

You get one side of A4. **Spend it on things you would otherwise derive wrongly under time pressure**, not on things you understand.

**Worth the space:**

- The **register table** — six argument registers in order, and the caller/callee-saved split.
- The **alignment parity rule**: `rsp ≡ 0 (mod 16)` before `call`, `≡ 8` on entry, **each push flips it**.
- The **cache formulas**: capacity $= S \times E \times B$; offset bits $= \log_2 B$; index bits $= \log_2 S$; same-set stride $= S \times B$.
- **IEEE 754 layout**: 1 / 8 / 23, bias 127, implicit leading 1, and what $e = 0$ and $e = 255$ mean.
- The **latency ladder**: 4 / 12 / 41 / 438 cycles.
- The **signed/unsigned jump pairs**: `jl`/`jb`, `jg`/`ja`.

**Not worth the space:** anything you can reconstruct in ten seconds, and anything you have never once used.

---

## The Six Things Most Likely to Cost You Marks

These are the errors that recurred across four weeks of problem sets. **Each is worth checking you can do cold.**

### 1. Branch displacement measured from the wrong instruction

`rip` advances **during fetch**, so a relative branch is measured from the address of the **next** instruction.

`7e ee` at `0x1174` is two bytes → `rip = 0x1176`; `0xee` = $-18$; target `0x1164`. **Not `0x1166`.**

### 2. Believing `cmp` writes a register

**It does not.** `cmp` and `test` compute, discard the result, and keep only the flags. Nothing lands in `eax`.

### 3. Stack alignment parity

On entry `rsp ≡ 8 (mod 16)`. **Each push flips the parity.** So:

- **Odd** number of pushes → aligned, `sub` nothing.
- **Even** number of pushes → still misaligned, `sub rsp, 8`.

Almost everyone gets this backwards the first time. Two pushes need a `sub`.

### 4. "Undefined behaviour means it wraps"

It does not. **It means the compiler may assume it never happens.** `x + 1 > x` on a signed `int` became `mov eax,0x1` — the comparison is *not in the binary*. The risk is deleted checks, not wrapped values.

### 5. Optimising the D1 miss rate

An L1 miss served by L2 costs ~12 cycles; one served by DRAM costs ~438. **Both appear identically in "D1 miss rate".** Blocking the transpose made D1 *worse* and the program 3.29× faster. **Ask which level is missing.**

### 6. Forgetting the exit test

A loop that runs $k$ times evaluates its condition $k+1$ times. `fib(3)`'s backward branch executes four times: three taken, one not.

---

## Things You Should Be Able to Do Without Notes

Time yourself. Each should take under three minutes.

1. Decode a two-byte relative branch and give its target.
2. Give the IEEE 754 bit pattern of a small value like 1.5, −0.75 or 40.0.
3. Draw a stack frame with return address, saved `rbp`, saved registers and locals at correct offsets.
4. Place the arguments of a mixed `int`/`double` signature.
5. Compute cache capacity from $S$, $E$, $B$, and the same-set stride.
6. Classify a described miss as compulsory, capacity or conflict.
7. State why one loop order is 30× slower than another.
8. Explain what `cdq` is for.

---

## Worked Example — the shape of a full-mark answer

> **Q. `int div8(int x){ return x/8; }` compiles to four instructions but `x >> 3` to one. Why?**

**A bare answer** *(≈1 of 5)*: "Because division is more complicated than shifting."

**A full-mark answer** *(5 of 5)*:

> `sar` rounds toward $-\infty$, but C's `/` must truncate toward zero. They agree for non-negative
> values and differ for negatives: $-17 \gg 3 = -3$ while $-17/8 = -2$. So the compiler adds a bias of
> $2^3 - 1 = 7$ before shifting, which converts floor to truncation — but only for negatives, hence
> the `test`/`cmovns` selecting between the biased and unbiased value. `unsigned x / 8` compiles to a
> single `shr`, because unsigned division has no negative case and therefore needs no correction.

**Notice what makes the difference:** a concrete example with numbers, the *reason* for the bias, and the contrasting case. That is roughly four sentences and it is the standard the marks are set to.

---

## A Realistic Revision Plan

**If you have a week.**

| Day | Do |
|---|---|
| 1 | Re-read the four [[CS201 Week5/summary\|summary]] files. Write your sheet from memory, then check it |
| 2 | Redo PS 1 Q2 and PS 2 Q1–Q2 **without notes**, timed |
| 3 | Redo PS 3 Q1 and Q4. Draw three stack frames from scratch |
| 4 | Redo PS 4 Q1 and Q3(d). Re-derive the cache formulas |
| 5 | The four quizzes, closed-book, in ten minutes each |
| 6 | The eight tasks in "without notes" above, timed |
| 7 | Light. Re-read your sheet. Sleep |

**If you have two days.** The four quizzes closed-book; the six error patterns above; PS 3 Q1(a) and PS 4 Q3(d). **Those two questions between them touch most of the paper.**

---

## During the Exam

**Read all five questions first.** Two minutes, and it stops you spending twenty on Q1 while Q4 is worth more.

**Q4 is the largest section at 24 marks**, and Q4(e) — the 3.29× question — is where the most marks are lost. **Do it while you are fresh.**

**Show working.** A correct method with an arithmetic slip earns most of the marks. A bare number earns none, and a bare *wrong* number earns nothing at all.

**"Explain in one sentence" means one sentence.** Padding does not earn marks and costs you time.

**If you are stuck, write what you do know.** "This is a conflict miss because the stride is a multiple of $S \times B$" earns marks even if the arithmetic that follows goes wrong.

---

## What the Exam Is Really Testing

Not whether you memorised the instruction set. **Whether you can look at a machine-level fact and say what it means for the code you write.**

Every question on the paper started life as a measurement in a lecture or a lab. If you did the labs and understood *why* the numbers came out as they did, you have already done most of the revision.

---

*CS 201 · Midterm 1 Revision Guide · Weeks 0–4*
