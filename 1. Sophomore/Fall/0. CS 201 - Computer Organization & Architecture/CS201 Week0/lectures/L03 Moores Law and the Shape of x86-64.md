# CS 201 · Computer Organization & Architecture
## Week 0 · Lecture 3 of 3
### Moore's Law, Its End, and the Shape of x86-64

*“The complexity for minimum component costs has increased at a rate of roughly a factor of two per year. Certainly over the short term this rate can be expected to continue, if not to increase.”* — Gordon Moore, "Cramming more components onto integrated circuits", *Electronics* (1965)

---

**Reading:** CS:APP §1.9, §3.2 · **Previous:** L02, the von Neumann machine

**Coursework:** 📝 **PS 0** released Wed this week, due Fri this week 17:00 · 🔬 **Lab 0** Fri this week 15:00–16:50

---

## 1. The Observation, and What It Was Not

In 1965 Gordon Moore observed that the number of transistors on an economically optimal chip had been doubling roughly every year, and guessed it would continue. He revised it to two years in 1975. It held, near enough, for about four decades.

**Moore's Law was never a law of physics and never a promise about speed.** It was an observation about *transistor count*, sustained by an industry that decided to treat it as a target. Everything else — clock speed, performance per watt — came from a second, separate effect.

**That second effect was Dennard scaling.** Shrink a transistor's dimensions by a factor $k$ and you can also reduce its voltage and current by $k$, which means power density stays constant. Smaller transistors, more of them, *and* you can clock them faster for free. Between roughly 1975 and 2005, that is why computers got faster every year without programmers doing anything.

---

## 2. Dennard Scaling Ended; Moore's Law Outlived It by a Decade

Around 2005 the voltage could not be reduced any further. Below roughly 1 volt, leakage current — transistors conducting slightly even when off — starts to dominate, and it gets worse as the device gets smaller. Power density stopped being constant and started rising.

**The consequence is the power wall.** A chip can only dissipate so much heat. Once clock increases cost more power than the package can shed, clocks stop rising.

| | ~1995 | ~2005 | Today |
|---|---|---|---|
| Single-core clock | 100 MHz → 1 GHz | ~3 GHz | ~3–5 GHz |
| Cores | 1 | 1–2 | 4–128 |

**Clock speed has moved by less than a factor of two in twenty years.** Transistor budgets kept growing for another decade after Dennard scaling stopped — so the industry spent them on *more cores* rather than faster ones, because that is what the power budget allowed.

> **This is the single most important fact about your career as a programmer.** Until 2005, code got
> faster while you slept. It does not any more. Performance now comes from using the parallelism and
> the memory hierarchy deliberately — which is why Weeks 4, 5, 10 and 11 exist, and why they are the
> four hardest weeks of this course.

**The lab machine, as an illustration.** An Intel Core i5-8250U:

```
$ lscpu
Model name:  Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz
CPU(s):      8          Core(s) per socket: 4      Thread(s) per core: 2
CPU max MHz: 3400.0     CPU min MHz: 400.0
```

*(Measured on the lab hardware.)* **Four physical cores, eight hardware threads, and a nominal clock lower than a 2004 Pentium 4's.** Its performance advantage over that Pentium is almost entirely architectural: wider issue, better prediction, deeper cache, more cores. Not clock.

---

## 3. The Memory Hierarchy on Real Hardware

Since you will spend Weeks 4 and 6 here, look at the actual numbers now:

```
$ lscpu -C
NAME ONE-SIZE ALL-SIZE WAYS TYPE         LEVEL SETS COHERENCY-SIZE
L1d       32K     128K    8 Data             1   64             64
L1i       32K     128K    8 Instruction      1   64             64
L2       256K       1M    4 Unified          2 1024             64
L3         6M       6M   12 Unified          3 8192             64
```

*(Measured.)* Three things to notice, all of which are Week 4's subject:

**The split L1 from L02 §6 is right there** — 32 KB of instruction cache and 32 KB of data cache, separately, per core.

**The arithmetic closes exactly:**
$$64 \text{ sets} \times 8 \text{ ways} \times 64 \text{ bytes} = 32\,768 = 32\text{ KB} \quad \checkmark$$
A cache is fully described by three numbers, and those three are all of them.

**The coherency size is 64 bytes on every level.** That is the cache line — the smallest unit that ever moves between levels. **You never load a byte from DRAM; you load 64 of them.** Reading one `int` you need brings in fifteen you did not ask for, which is a gift when you are walking an array and a disaster when you are chasing pointers. Week 4 measures both.

---

## 4. x86-64: The Register File

The state the ISA promises you. Sixteen general-purpose 64-bit registers:

| Register | Conventional role *(Week 3 makes this precise)* |
|---|---|
| `rax` | Return value; accumulator |
| `rbx` | Callee-saved |
| `rcx` | 4th argument |
| `rdx` | 3rd argument |
| `rsi` | 2nd argument |
| `rdi` | **1st argument** |
| `rbp` | Frame pointer (callee-saved) |
| `rsp` | **Stack pointer** |
| `r8`–`r9` | 5th and 6th arguments |
| `r10`–`r11` | Caller-saved scratch |
| `r12`–`r15` | Callee-saved |

Plus `rip`, the instruction pointer, and `RFLAGS`, the condition codes.

**You have already seen two of these do their job.** In L02, `sum_to` began with `mov DWORD PTR [rbp-0x14],edi` — the first argument arriving in `rdi`. And `push rbp` / `mov rbp,rsp` set up the frame pointer. Neither was arbitrary; both are the calling convention, and Week 3 is entirely about it.

**Each register is addressable at four widths**, a direct inheritance from the 16-bit 8086:

| 64-bit | 32-bit | 16-bit | 8-bit |
|---|---|---|---|
| `rax` | `eax` | `ax` | `al` |
| `rdi` | `edi` | `di` | `dil` |

**One trap, now, because it catches everyone.** Writing to a 32-bit register **zeroes the upper 32 bits**; writing to a 16- or 8-bit register **leaves the upper bits alone**. So `mov eax, 5` sets `rax` to 5, but `mov ax, 5` does not. This is why compilers emit `xor eax,eax` rather than `xor rax,rax` to zero a register — same effect, shorter encoding.

---

## 5. The Four Condition Flags

x86-64 comparison works in two steps, and this surprises people coming from higher-level languages: **the comparison and the branch are separate instructions communicating through hidden state.**

| Flag | Set when |
|---|---|
| **ZF** | Result was zero |
| **SF** | Result was negative (top bit set) |
| **CF** | Unsigned overflow — a carry out |
| **OF** | Signed overflow |

In L02's loop:

```
1171:  cmp  eax,DWORD PTR [rbp-0x14]     ; computes eax - n, discards it, sets flags
1174:  jle  1164                          ; branches on ZF, SF and OF
```

`cmp` performs a subtraction and throws the answer away, keeping only the flags. `jle` then reads them.

> **CF and OF are independent, and both can happen, neither, or either.** You proved this in
> ECE 110 when you built the adder and found that carry-out and signed overflow are different
> conditions. Week 1 picks it up again as the reason C's signed overflow is undefined behaviour
> while unsigned overflow is defined to wrap.

---

## 6. CISC on the Outside, RISC on the Inside

x86-64 is a CISC design: many instructions, variable length, operands that may live in memory. `add DWORD PTR [rbp-0x8],eax` reads memory, adds, and writes memory back — one instruction doing three things.

**Modern x86 chips do not execute those instructions.** The decoder translates each one into a sequence of fixed-width internal operations — micro-ops — and the out-of-order core executes *those*. That `add` becomes roughly a load, an add, and a store.

**So the ISA is now a compatibility layer over a RISC-like engine**, which is exactly L01's point about the ISA being a contract that says nothing about implementation. The decoder is the price of the contract: real silicon, real power, spent translating a 1978 instruction format into something a 2017 core can schedule.

Whether that price is worth paying is the live argument in computer architecture, and Week 12 returns to it with RISC-V and ARM64 as the counter-examples.

**The lab machine's vector support**, since Week 5 will use it:

```
$ grep -o -E "avx2|avx|sse4_2" /proc/cpuinfo | sort -u
avx
avx2
sse4_2
```

*(Measured — AVX2, so 256-bit vectors. No AVX-512 on this part.)*

---

## 7. Where the Course Goes From Here

| Weeks | What you gain |
|---|---|
| **1–3** | Fluency: floating point, the instruction set, the stack. You will read assembly without help. |
| **4–6** | The memory hierarchy. This is where "why is it slow" starts having answers. |
| **7–9** | The world outside the CPU: storage, networks, and what an attacker does with all of it. |
| **10–12** | Parallelism, deliberate optimisation, and what comes after Moore's Law. |

---

## 8. What to Take Away

1. **Moore's Law is about transistor count. Dennard scaling was about speed, and it ended in 2005.**
2. **The power wall is why you have four cores instead of one fast one.** Free performance is over.
3. **Sixteen registers, four widths each; 32-bit writes zero the top half and narrower writes do not.**
4. **`cmp` sets flags, `jle` reads them** — comparison and branch are separate.
5. **CISC outside, micro-ops inside.** The ISA is a contract, not a description of the hardware.
6. **A cache line is 64 bytes.** You will not stop hearing this.

---

## Exercises

1. Dennard scaling ended but Moore's Law continued for roughly another decade. What did the extra transistors get spent on, and why was that the only available choice?
2. Verify the L2 geometry the way §3 verified L1: 1024 sets, 4 ways, 64-byte lines. Does it come to 256 KB?
3. Why does `xor eax,eax` zero all of `rax`, and why do compilers prefer it to `mov rax,0`? Give both reasons.
4. `cmp` throws away its result. What would be lost if x86-64 had no flags register and every conditional branch took two register operands directly, the way RISC-V does?
5. A 64-byte cache line means an array walk gets fifteen free elements per miss. Construct a data structure access pattern for which the 64-byte line is actively harmful, and estimate how much memory bandwidth it wastes.

---

*Next week: Data representation — two's complement revisited, and why IEEE 754 addition is not associative.*
