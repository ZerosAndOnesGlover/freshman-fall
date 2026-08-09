# CS 201 · Problem Set 0
## Tracing the Machine — Layers, Encoding, and the Cycle

---

**Released:** Week 0, Wednesday · **Due:** Week 0, Friday 17:00 *(the second Friday — Week 0 is ten days)*
**Total: 100 points** · Submit one PDF, `PS0_{LastName}_{StudentID}.pdf`

> Collaboration: discussing approaches is fine and encouraged. The write-up must be yours. State at
> the top: *"I worked on this problem set independently"* or name who you discussed which question
> with.
>
> **Q2 and Q3 must be done by hand.** You may check your answers with `objdump` and `gdb` afterwards
> — you should — but show the working, not the tool output.

---

### Q1: The Layers (18 points)

**(a) [6]** The table below lists five layers. For each, give **one thing it hides** from the layer above and **one thing that hiding costs you**.

| Layer | Hides… | Costs… |
|---|---|---|
| Gates over transistors | | |
| ISA over microarchitecture | | |
| C over assembly | | |
| Python over C | | |
| Virtual memory over physical memory | | |

*(The last row is Week 6 material. Answer it from what you can reason out; you will not be marked down for an incomplete answer, only for a confused one.)*

**(b) [6]** The ISA is described in lecture as "the only layer that is a promise". Explain what is meant, and give a concrete consequence that would not hold if the ISA were merely a convention.

**(c) [6]** In Lecture 1, the same loop ran in 12.06 s under Python and 0.258 s compiled with `gcc -O0` — a factor of about 46.

State **three** distinct per-iteration costs Python pays that the C version does not. For each, say whether you would expect it to scale with the *number* of iterations, the *size* of the numbers involved, or neither.

---

### Q2: Decoding by Hand (26 points)

Here is the `-O0` disassembly of `sum_to` from Lecture 2:

```
    1149:  f3 0f 1e fa           endbr64
    114d:  55                    push   rbp
    114e:  48 89 e5              mov    rbp,rsp
    1151:  89 7d ec              mov    DWORD PTR [rbp-0x14],edi
    1154:  c7 45 f8 00 00 00 00  mov    DWORD PTR [rbp-0x8],0x0
    115b:  c7 45 fc 01 00 00 00  mov    DWORD PTR [rbp-0x4],0x1
    1162:  eb 0a                 jmp    116e
    1164:  8b 45 fc              mov    eax,DWORD PTR [rbp-0x4]
    1167:  01 45 f8              add    DWORD PTR [rbp-0x8],eax
    116a:  83 45 fc 01           add    DWORD PTR [rbp-0x4],0x1
    116e:  8b 45 fc              mov    eax,DWORD PTR [rbp-0x4]
    1171:  3b 45 ec              cmp    eax,DWORD PTR [rbp-0x14]
    1174:  7e ee                 jle    1164
    1176:  8b 45 f8              mov    eax,DWORD PTR [rbp-0x8]
    1179:  5d                    pop    rbp
    117a:  c3                    ret
```

**(a) [6]** Compute the target of the forward jump at `0x1162` (`eb 0a`) **by hand**, showing the arithmetic. State explicitly what value `rip` holds at the moment the displacement is applied, and why it is that value and not `0x1162`.

**(b) [6]** Do the same for the backward branch at `0x1174` (`7e ee`). `0xee` is a *signed* 8-bit displacement — convert it first.

**(c) [6]** The instruction at `0x1154` is seven bytes: `c7 45 f8 00 00 00 00`. Account for every byte. Which byte or bytes encode the operation, which encode the destination, and which encode the immediate value? *(You are not expected to have memorised x86-64 encoding. Reason it out by comparing against `0x115b`, which differs in exactly two places, and say what that comparison tells you.)*

**(d) [8]** Instructions in this listing range from 1 byte (`ret`) to 7 bytes. Across the whole binary the distribution is:

| Length | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Count | 18 | 16 | 22 | 19 | 10 | 8 | 20 |

RISC-V and ARM64 use a **fixed** 4-byte instruction length instead.

State **one advantage** of x86-64's variable-length encoding and **one advantage** of the fixed-length alternative. Then say which you would choose for a processor that must decode eight instructions per cycle, and defend it in two or three sentences.

---

### Q3: Trace the Cycle (26 points)

Call `sum_to(3)`. Execution reaches `0x1164` for the **first** time with the stack slots holding `total = 0` and `i = 1`.

**(a) [14]** Trace execution from `0x1164` up to and including the branch at `0x1174`, for this **first** pass. Fill in one row per instruction:

| # | Address | Instruction | Fetch: bytes read, new `rip` | Execute: what happens | `eax` | `total` | `i` | Branch taken? |
|---|---|---|---|---|---|---|---|---|
| 1 | `0x1164` | | | | | | | — |

Six rows. Show `rip` after each fetch, and note for every instruction whether it reads memory, writes memory, or neither.

**(b) [6]** How many times is the branch at `0x1174` **taken** during the whole of `sum_to(3)`, and how many times is it **not taken**? Explain the difference in one sentence.

**(c) [6]** Count, for the whole call `sum_to(3)`:

1. total instructions executed;
2. total **data** memory reads;
3. total **data** memory writes.

Do not count instruction fetches. Then answer: at `-O2` the compiler keeps `total` and `i` in registers instead of on the stack. Using your counts, state how many of the reads and writes that removes.

---

### Q4: Cache Geometry (16 points)

`lscpu -C` on the lab machine reports:

```
NAME ONE-SIZE  WAYS  TYPE         LEVEL  SETS  COHERENCY-SIZE
L1d       32K     8  Data             1    64              64
L2       256K     4  Unified          2  1024              64
L3         6M    12  Unified          3  8192              64
```

**(a) [4]** Verify all three sizes from sets × ways × line size. Show the arithmetic for each.

**(b) [4]** The coherency size — the cache line — is 64 bytes at every level. An `int` is 4 bytes. When a program reads one `int` that is not in cache, how many `int`s are actually brought in, and how many of them were asked for?

**(c) [4]** Program A walks a 1-million-element `int` array in index order. Program B visits the same million elements in a random permutation. Both perform exactly one million reads.

Using only the 64-byte line, estimate how many cache lines each program must fetch. State any assumption you make.

**(d) [4]** L1d is 32 KB and there are four cores, giving 128 KB of L1d in the machine — but L3 is 6 MB and shared. Why is the *fast* cache the small one? Answer in terms of a cost that grows with size.

---

### Q5: After Moore's Law (14 points)

**(a) [5]** Distinguish **Moore's Law** from **Dennard scaling** in one sentence each. Which one ended around 2005, and which continued for roughly another decade?

**(b) [5]** The lab machine is an i5-8250U: 4 cores, 8 threads, 1.6 GHz base and 3.4 GHz turbo. A 2004 Pentium 4 reached 3.8 GHz on a single core.

The i5 is nonetheless far faster on essentially every real workload. Give **three** architectural reasons, none of which is clock speed.

**(c) [4]** "Free performance is over" — the claim that code no longer gets faster just by waiting for new hardware.

Name one category of program for which this is **still not really true**, and explain what property of that program lets it keep benefiting from new hardware without being rewritten.

---

## Marks

| | |
|---|---:|
| Q1 The Layers | 18 |
| Q2 Decoding by Hand | 26 |
| Q3 Trace the Cycle | 26 |
| Q4 Cache Geometry | 16 |
| Q5 After Moore's Law | 14 |
| **Total** | **100** |

---

*CS 201 · Week 0 · Problem Set 0*
