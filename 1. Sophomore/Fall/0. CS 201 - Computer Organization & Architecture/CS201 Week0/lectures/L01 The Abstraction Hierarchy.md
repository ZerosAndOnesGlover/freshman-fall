# CS 201 · Computer Organization & Architecture
## Week 0 · Lecture 1 of 3
### The Abstraction Hierarchy — Transistors to Programs

---

**Reading:** CS:APP §1.1–1.4 · **Next:** L02, the von Neumann machine

---

## 1. The Stack You Have Been Standing On

You have written programs in Python, C and C++ for a year. Underneath every one of them is this:

| Layer | What it is | What it hides | You met it in |
|---|---|---|---|
| **Python / high-level** | An interpreter written in C | Memory, types, the machine | CS 101 |
| **C** | A thin notation over the ISA | Register allocation, addressing | PROG 101 |
| **Assembly** | The ISA, made readable | Binary encoding | **CS 201, Week 2** |
| **ISA** | The hardware/software contract | How the contract is honoured | **CS 201, this week** |
| **Microarchitecture** | One implementation of the ISA | Pipelines, caches, prediction | **CS 201, Weeks 4–5** |
| **Circuits** | Adders, multiplexers, registers | Gate delay | ECE 110 |
| **Gates** | AND, OR, NOT out of transistors | Physics | ECE 110 |
| **Transistors** | A voltage-controlled switch | Everything | PHYS 141 |

**The pattern is the same at every boundary.** A layer offers a simplified interface and takes freedom in exchange. The layer above gets to stop thinking about something; in return it gives up the ability to control it.

> **This is not a hierarchy of importance.** It is a hierarchy of *concern*. A kernel developer and a
> web developer are both doing real work; they are doing it at different layers, and the difference
> that matters is whether they know which layer they are on.

---

## 2. The ISA Is the Only Layer That Is a Promise

Every other boundary is a convention. **The ISA is a contract**, and it is the reason a binary compiled in 2008 still runs today.

The ISA specifies exactly three things:

1. **What operations exist** — add, compare, jump, load, store.
2. **What state exists** — how many registers, how wide, how memory is addressed.
3. **What each operation does to that state.**

It says *nothing* about how any of it is achieved. Intel and AMD both implement x86-64; internally they share almost nothing. That silence is the whole value of the contract: **hardware can be redesigned completely without breaking a single program.**

**Concretely.** An i5-8250U executes `add` with an out-of-order superscalar core built in 2017. A 1978 8086 executed the same conceptual operation with a fraction of the transistors. Same contract, forty years apart.

---

## 3. What a Layer Costs — Measured

Abstraction costs are usually discussed in the abstract, which is a poor way to learn what they are. Here is the same computation — sum the integers from 1 to $10^8$ — at three points on the stack.

**Python:**

```python
t = 0
for i in range(1, 100_000_001):
    t += i
```

**C:**

```c
long sum_to(long n) {
    long t = 0;
    for (long i = 1; i <= n; i++)
        t += i;
    return t;
}
```

Measured on an **Intel Core i5-8250U**, GCC 13.3.0, Python 3.14.2:

| | Time | Relative |
|---|---:|---:|
| Python 3.14 | 12.06 s | 1× |
| C, `gcc -O0` | 0.258 s | **46× faster** |
| C, `gcc -O2` | *see below* | — |

*(Measured. C figure is the median of three runs: 0.2641, 0.2584, 0.2574 s.)*

**Where did the 46× go?** Python's loop does, per iteration, roughly: fetch a bytecode, decode it, look up `t` in a dictionary, check that `t` and `i` are both integers, allocate a new integer object for the result, adjust two reference counts, and store it back. **The C loop does one `add` and one compare.** The 46× is not Python being badly written — it is the price of the guarantees Python makes, paid one iteration at a time.

---

## 4. The `-O2` Result, Which Is the Real Lesson

The optimised C build reported **0.0000 seconds**. That is not a measurement error and it is not a fast loop.

```
$ objdump -d --no-show-raw-insn -M intel bench_O2 | sed -n '/<main>:/,/ret/p'
```

```
10c0:   call   1070 <clock_gettime@plt>
10c5:   lea    rsi,[rsp+0x10]
10ca:   mov    edi,0x1
10cf:   call   1070 <clock_gettime@plt>
...
1101:   movabs rdx,0x11c3793adb7080
```

**The two clock readings are adjacent.** Nothing runs between them. And `0x11c3793adb7080` is `5000000050000000` — the answer.

GCC noticed that `n` was a compile-time constant, unrolled and analysed the loop, computed the whole sum during compilation, and emitted the result as a single immediate operand. **The hundred-million-iteration loop does not exist in the program.**

> **Why this belongs in Lecture 1.** Every intuition you have about "what the code does" is an
> intuition about the *source*. The machine does not run your source. It runs whatever the compiler
> decided was equivalent, and "equivalent" is defined by the language standard, not by your mental
> picture. From here on, when the question is what the machine does, **the answer comes from
> `objdump`, not from reading the C.**

For completeness — the standalone `sum_to` symbol *is* still emitted, and it is not folded, because it has external linkage and some other translation unit might call it:

```
1270:   lea    rdx,[rdx+rax*2+0x1]
1275:   add    rax,0x2
1279:   cmp    rax,rcx
127c:   jne    1270 <sum_to+0x30>
```

**Four instructions, and read the first one carefully.** `lea rdx,[rdx+rax*2+0x1]` computes `rdx = rdx + 2*rax + 1`. With `rax` holding $i$, that is $i + (i+1)$ — **the loop has been unrolled two iterations at a time, and both additions folded into one address-arithmetic instruction that is not doing address arithmetic at all.** `lea` is the compiler's favourite general-purpose adder. You will see this constantly from Week 2 onward.

---

## 5. Why Every Layer Exists

Not decoration. Each layer solved a specific problem that the one below it created.

| Layer | The problem it solved |
|---|---|
| **Gates** | Transistors are analogue. Gates restore a clean 0 or 1 at every stage, so error does not accumulate across a circuit. |
| **Circuits** | Gates compute one bit. Circuits compose them into arithmetic on words. |
| **ISA** | Every new chip design would otherwise obsolete every program. |
| **Assembly** | Machine code is unreadable and unrelocatable by hand. |
| **C** | Assembly is not portable, and register allocation by hand does not scale past a few hundred lines. |
| **Python** | Manual memory management is the largest source of security bugs in the history of the field. |

**Read that table upward and it is the history of computing. Read it downward and it is this course.**

---

## 6. Breaking Through a Layer

The engineer's skill is not staying at one level. It is knowing when the abstraction is costing more than it is worth, and having the ability to go one level down and look.

Three real cases you will meet this term:

- **Week 4.** Two loops over the same array, algorithmically identical, differ by an order of magnitude. Nothing in the C explains it; the cache does.
- **Week 9.** A program with no bug visible in the source is exploitable, because the *calling convention* — a layer down — puts the return address somewhere reachable.
- **Week 11.** A profiler tells you the bottleneck is a line you would never have suspected, and the roofline model tells you whether it is even possible to fix.

> **The rule.** Go down a layer when the layer you are on cannot explain what you are seeing. Do not
> go down out of curiosity in production code, and never go down without measuring first — Week 11
> is entirely about why.

---

## 7. What to Take Away

1. **The stack is layers of hidden complexity, and hiding always costs something.**
2. **The ISA is the one boundary that is a contract**, which is why binaries outlive hardware.
3. **The compiler is not a transcription service.** It emits something *equivalent*, on its own terms.
4. **`objdump` is the ground truth** for what the machine does. Get used to reaching for it — Lab 0 is mostly practice at exactly that.

---

## Exercises

1. The Python loop is 46× slower than `-O0` C here. Name three of the per-iteration costs Python pays that C does not, and say which you think dominates.
2. `gcc -O2` folded the loop away because `n` was a compile-time constant. What one change to `main` would prevent it, and why?
3. `lea rdx,[rdx+rax*2+0x1]` performs an addition, not an address computation. Why does an instruction meant for addressing turn out to be a useful general adder? *(Hint: what operands can the addressing mode take, and what does it not touch?)*
4. Take a layer boundary from §5 and argue the other side: name a real situation in which that layer's guarantees are worth *less* than what they cost.

---

*Next: L02 — the von Neumann machine, and the cycle every one of those instructions goes through.*
