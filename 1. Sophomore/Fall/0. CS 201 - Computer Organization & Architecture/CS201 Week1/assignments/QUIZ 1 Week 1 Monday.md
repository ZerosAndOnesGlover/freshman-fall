# CS 201 · Quiz 1
## Administered: Monday, Week 1 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 0** — the abstraction hierarchy, the von Neumann machine, the fetch-decode-execute cycle, and the shape of x86-64.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is that you find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** Name the five stages an instruction passes through, in order.

&nbsp;

&nbsp;

---

**Q2.** The instruction at `0x1174` is `7e ee`, a two-byte `jle`. Compute its target.

&nbsp;

&nbsp;

---

**Q3.** What value does `rip` hold at the moment a relative branch applies its displacement, and why is it that value?

&nbsp;

&nbsp;

---

**Q4.** x86-64 instructions are 1 to 15 bytes long; ARM64's are always 4. Give one advantage of each choice.

&nbsp;

&nbsp;

---

**Q5.** `mov eax, 5` and `mov ax, 5` both write to a sub-register of `rax`. What is the difference in effect on the upper bits of `rax`?

&nbsp;

&nbsp;

---

**Q6.** Distinguish Moore's Law from Dennard scaling in one sentence each. Which ended in 2005?

&nbsp;

&nbsp;

---

**Q7.** `cmp eax, edx` is followed by `jle`. Where does the result of the `cmp` go?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **Fetch, Decode, Execute, Memory, Writeback.**

*Order matters; "execute" before "decode" is the common slip.*

---

**Q2.** **`0x1164`.**

`0xee` is a signed 8-bit displacement: $238 - 256 = -18$. The instruction is at `0x1174` and is two bytes, so `rip` is `0x1176`, and $\texttt{0x1176} - 18 = \texttt{0x1164}$.

*If you got `0x1166`, you added to `0x1174` instead of to the next instruction — see Q3, which is the same point.*

---

**Q3.** **`rip` holds the address of the *next* instruction** — here `0x1176`, not `0x1174`.

Because **`rip` is advanced during the fetch stage**, before the instruction executes. By the time the displacement is applied, the pointer has already moved past the branch itself.

---

**Q4.** **Variable-length (x86-64): code density.** One-byte `push` and `ret` mean smaller binaries and more instructions resident in the instruction cache.

**Fixed-length (ARM64): trivial decode.** Instruction *N+1*'s address is known without decoding instruction *N*, so boundaries can be found in parallel — which is what matters at wide issue rates.

---

**Q5.** **`mov eax, 5` zeroes the upper 32 bits of `rax`. `mov ax, 5` leaves them alone.**

A 32-bit write zero-extends; 16- and 8-bit writes merge into the existing value. This is why compilers emit `xor eax,eax` to zero a full 64-bit register.

---

**Q6.** **Moore's Law:** transistor count per chip doubles roughly every two years — an observation about *count*.

**Dennard scaling:** as transistors shrink by a factor $k$, voltage and current shrink by $k$ too, so power density stays constant — which is what allowed *clock speed* to rise for free.

**Dennard scaling ended** around 2005. Moore's Law continued for roughly another decade.

*Getting these the wrong way round is the single most common error on this quiz.*

---

**Q7.** **Into the flags register** — ZF, SF, CF, OF.

`cmp` performs the subtraction and **discards the numeric result**, keeping only the condition codes. `jle` then reads them. Nothing is written to `eax` or any other general-purpose register.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q3, Q7 | L02 §2 and §5 — the cycle and how `rip` moves |
| Q2 | L02 §5, then do it again on the `eb 0a` at `0x1162` |
| Q4 | L02 §4 |
| Q5, Q6 | L03 §2 and §4 |

**Q2, Q3 and Q7 are the ones that recur.** Week 2 assumes all three without restating them, and Week 3's stack frames depend on Q3 being automatic.

---

*CS 201 · Week 1 · Quiz 1 · covers Week 0 · ungraded*
