# CS 201 · Computer Organization & Architecture
## Week 0 · Lecture 2 of 3
### The Von Neumann Machine and the Fetch-Decode-Execute Cycle

---

**Reading:** CS:APP §1.4, §4.1 · **Previous:** L01, the abstraction hierarchy

---

## 1. One Idea, 1945

The von Neumann architecture is a single design decision with enormous consequences: **instructions and data live in the same memory, addressed the same way.**

```
        ┌─────────────────────────────────┐
        │              CPU                │
        │  ┌───────────┐  ┌────────────┐  │
        │  │  Control  │  │    ALU     │  │
        │  │   unit    │  │            │  │
        │  └───────────┘  └────────────┘  │
        │        ┌──────────────┐         │
        │        │  Registers   │         │
        │        │  rax…r15, rip│         │
        │        └──────────────┘         │
        └────────────────┬────────────────┘
                         │  system bus
        ┌────────────────┴────────────────┐
        │                                 │
   ┌────┴─────┐                     ┌─────┴────┐
   │  Memory  │                     │   I/O    │
   │ code+data│                     │ devices  │
   └──────────┘                     └──────────┘
```

**Before this, "programming" meant rewiring.** ENIAC was configured with plugboards and switches; changing the program took days. Storing the program *as data* means a program can be loaded, copied, written to disk — and modified by another program. **Compilers, linkers, loaders, operating systems and JIT compilers all exist because of this one choice.**

It also created the field's most durable security problem. If code is data, then data can be made into code, and Week 9 is about what happens when an attacker arranges exactly that.

---

## 2. The Cycle

Every instruction, on every von Neumann machine ever built, goes through the same sequence:

| Stage | What happens |
|---|---|
| **Fetch** | Read the instruction at the address in `rip`. Advance `rip` past it. |
| **Decode** | Work out which operation this is and where its operands are. |
| **Execute** | Perform the operation in the ALU. |
| **Memory** | Read or write memory, if the instruction needs to. |
| **Writeback** | Store the result into a register. |

**`rip` is advanced during fetch, before the instruction executes.** This is not a detail — it is why a jump works by *overwriting* `rip`, and why a relative branch is measured from the address of the *next* instruction rather than the current one. You will use that fact in §5.

> The five stages here are the classic teaching pipeline, and Week 5 turns them into an actual
> pipeline where five instructions are in flight at once. For now, treat them as strictly
> sequential — one instruction fully finishes before the next begins. That model is wrong about
> modern hardware and exactly right for reasoning about what a program *means*.

---

## 3. A Real Function, Fetched and Decoded

This is `sum_to` from Lecture 1, compiled with `gcc -O0` so nothing is optimised away:

```c
int sum_to(int n) {
    int total = 0;
    for (int i = 1; i <= n; i++)
        total += i;
    return total;
}
```

```
$ gcc -O0 -g -o sum_O0 sum.c
$ objdump -d -M intel sum_O0
```

```
0000000000001149 <sum_to>:
    1149:  f3 0f 1e fa           endbr64
    114d:  55                    push   rbp
    114e:  48 89 e5              mov    rbp,rsp
    1151:  89 7d ec              mov    DWORD PTR [rbp-0x14],edi
    1154:  c7 45 f8 00 00 00 00  mov    DWORD PTR [rbp-0x8],0x0
    115b:  c7 45 fc 01 00 00 00  mov    DWORD PTR [rbp-0x4],0x1
    1162:  eb 0a                 jmp    116e <sum_to+0x25>
    1164:  8b 45 fc              mov    eax,DWORD PTR [rbp-0x4]
    1167:  01 45 f8              add    DWORD PTR [rbp-0x8],eax
    116a:  83 45 fc 01           add    DWORD PTR [rbp-0x4],0x1
    116e:  8b 45 fc              mov    eax,DWORD PTR [rbp-0x4]
    1171:  3b 45 ec              cmp    eax,DWORD PTR [rbp-0x14]
    1174:  7e ee                 jle    1164 <sum_to+0x1b>
    1176:  8b 45 f8              mov    eax,DWORD PTR [rbp-0x8]
    1179:  5d                    pop    rbp
    117a:  c3                    ret
```

**Sixteen instructions for a four-line function.** You are not expected to read this fluently yet — that is Week 2 — but three things are worth seeing now.

**The local variables are not in registers.** `total` is at `[rbp-0x8]` and `i` is at `[rbp-0x4]`; both live on the stack, and every use is a memory access. That is what `-O0` means. At `-O2` the same function keeps everything in registers and unrolls the loop, as Lecture 1 showed.

**The parameter arrived in a register.** `mov DWORD PTR [rbp-0x14],edi` — the caller put `n` in `edi` and the function's first act is to spill it to the stack. Why `edi` specifically is the System V calling convention, and it is Week 3.

**The loop was rotated.** The `jmp` at `1162` jumps *forward* to the condition test at `116e`, and the body sits above it at `1164`. So the test happens before the first iteration, and the backward branch at the bottom does double duty as both "loop again" and "test". One branch per iteration instead of two.

---

## 4. Instructions Are Not All the Same Size

Look at the byte column. `push rbp` is **one** byte (`55`). `mov DWORD PTR [rbp-0x8],0x0` is **seven** (`c7 45 f8 00 00 00 00`).

Across this whole binary:

| Instruction length | Count |
|---:|---:|
| 1 byte | 18 |
| 2 bytes | 16 |
| 3 bytes | 22 |
| 4 bytes | 19 |
| 5 bytes | 10 |
| 6 bytes | 8 |
| 7 bytes | 20 |

*(Measured — counted from `objdump -d` over the entire executable.)*

**x86-64 is a variable-length encoding**, from 1 to 15 bytes. The trade is density against decode complexity: common operations get short encodings, so code is compact and the instruction cache holds more of it — but the CPU cannot know where instruction *N+1* starts until it has decoded instruction *N*.

**This is a real cost, not a theoretical one.** Decoding four x86-64 instructions per cycle in parallel requires speculating about where each one begins and discarding the guesses that were wrong. RISC-V and ARM64 use fixed 4-byte instructions precisely to make that problem disappear. Week 5 comes back to this when the pipeline needs a steady supply of decoded instructions.

---

## 5. Decoding One Instruction by Hand

Take the backward branch:

```
1174:  7e ee    jle 1164
```

Two bytes. `7e` is the opcode for "jump if less-or-equal", and `ee` is a **signed 8-bit displacement**:

$$\texttt{0xee} = 238_{10} \;\rightarrow\; 238 - 256 = -18$$

The displacement is added to `rip`, **and `rip` already points past this instruction** — that is §2's point made concrete. The instruction starts at `0x1174` and is two bytes long, so:

$$\texttt{rip} = \texttt{0x1176}, \qquad \texttt{0x1176} + (-18) = \texttt{0x1176} - \texttt{0x12} = \texttt{0x1164}$$

**Which is exactly the target `objdump` printed.** *(Verified.)*

> **Why relative and not absolute?** Because the code can then be loaded at any address without
> rewriting a single branch. Every relative jump inside a function stays correct no matter where the
> loader puts it. This is what makes shared libraries and ASLR possible — and ASLR is one of the
> main defences you will study in Week 9.

---

## 6. The Von Neumann Bottleneck

The architecture's founding decision is also its permanent constraint: **instructions and data share one path to memory.**

Every cycle, the CPU may need to fetch an instruction *and* read or write data. On the original design those contend for the same bus, and the processor waits. Backus named this the "von Neumann bottleneck" in his 1977 Turing Award lecture, and the entire memory hierarchy — Weeks 4 and 6 — is the accumulated response to it.

The first and largest mitigation is a **split L1 cache**: a separate instruction cache and data cache, so a fetch and a load can proceed in the same cycle. That is a Harvard architecture, locally. Modern machines are **von Neumann in their contract and Harvard in their L1** — one address space as far as any program can tell, two physical paths where it counts.

**Order-of-magnitude figures, which Week 4 makes precise:**

| Access | Cost |
|---|---|
| Register | < 1 cycle |
| L1 cache | ~4 cycles |
| L2 cache | ~12 cycles |
| L3 cache | ~40 cycles |
| DRAM | 200+ cycles |

**A DRAM access costs more than two hundred `add` instructions.** Nearly everything in Weeks 4, 6, 10 and 11 follows from that one ratio.

---

## 7. What to Take Away

1. **Stored-program means code is data.** Compilers, loaders and JITs depend on it; so do code-injection attacks.
2. **Fetch, decode, execute, memory, writeback** — the same five stages for every instruction, on every machine.
3. **`rip` advances at fetch**, which is why relative branches are measured from the following instruction.
4. **x86-64 instructions are 1–15 bytes.** Dense code, hard decode.
5. **One memory, one bottleneck.** The cache hierarchy is the whole answer, and it is most of this course.

---

## Exercises

1. Instruction `mov DWORD PTR [rbp-0x4],0x1` at `0x115b` is seven bytes. Account for them: which encode the operation, which the destination, which the value?
2. The `jmp` at `0x1162` is `eb 0a`. Compute its target by hand and check it against the listing.
3. Why can a two-byte `jle` only reach ±127 bytes, and what must the assembler do when the loop body is larger than that?
4. `sum_to` at `-O0` touches memory on every loop iteration; at `-O2` it touches none. The ISA contract is identical in both cases. What exactly does the contract *not* say, that leaves the compiler free to choose?
5. A split L1 cache gives instructions and data separate paths. Name a program for which this helps almost not at all, and say why.

---

*Next: L03 — Moore's Law, why it stopped, and what x86-64 actually looks like.*
