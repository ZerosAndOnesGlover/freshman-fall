# CS 201 · Computer Organization & Architecture
## Week 12 · Lecture 1 of 3
### Architecture Frontiers

*“The best way to predict the future is to invent it.”* — Alan Kay, at a meeting at Xerox PARC (1971)

---

**Reading:** CS:APP §5.1 (revisited), Patterson & Hennessy §6.7–6.11 · **Previous:** L36, benchmarking honestly

**Coursework:** 🔬 **Lab 11** Tue this week 15:00–16:50 · 📝 **PS 12** released Wed this week, due Fri this week 17:00 · 📋 **Project 2** due Fri this week 17:00 · 📝 **PS 11** due Fri this week 17:00

---

## A Note on This Lecture

**No GPU, no RISC-V hardware, and no quantum computer sits in BH 210.** So this lecture is a tour, not a lab — the one place in the course where the material is genuinely beyond the machine in front of you. Where a claim can be checked on this machine it is; everything else is cited and says so. **The point is not to use these machines but to see the shape of where the field is going, and why.**

---

## 1. Why the Frontier Moved

Week 0 §L03 told you the founding fact: **Dennard scaling ended around 2005, and single-core performance stopped rising for free.** For a decade the answer was *more cores* (Week 10). But that has limits too — Amdahl caps parallel speedup, and a general-purpose core spends most of its transistors on caches, prediction and out-of-order machinery (Weeks 4–5) that a *specific* workload may not need.

**So the frontier turned to specialisation: build a different machine for the workload, and spend the transistors on exactly what that workload needs.** This is the through-line of the whole lecture — TPUs, FPGAs, RISC-V and neuromorphic chips are all answers to "the general-purpose core has stopped getting faster, so what do we build instead?"

---

## 2. RISC-V — Simplicity as a Strategy

You have spent this course reading x86-64, and you have seen its complications: variable-length instructions (Week 2), a `mov` that is really a family, and instructions that do several things at once.

Watch one of those complications directly. This C loop:

```c
int sum(int *a, int n){ int s=0; for(int i=0;i<n;i++) s+=a[i]; return s; }
```

compiles on x86-64 to a loop whose body is:

```
add    eax, DWORD PTR [rdi]     ; load a[i] AND add it, in ONE instruction
add    rdi, 0x4
cmp    rdi, rdx
jne    ...
```

*(Verified.)* **`add eax,[rdi]` reads memory and adds in a single instruction** — a CISC "load-op". On **RISC-V** the same work is *two* instructions, because a RISC design forbids memory operands on arithmetic:

```
lw    t0, 0(a0)      # load a[i]
add   a1, a1, t0     # add it        (RISC-V — separate load and add)
```

**More instructions, and that is the point, not a flaw.** RISC-V bets that simple, fixed-length, load-store instructions are easier to pipeline (Week 5), easier to decode in parallel (Week 2's variable-length problem, gone), and easier to build correctly — so the *hardware* is smaller and faster even though the *instruction count* is higher.

**What makes RISC-V a frontier and not just another RISC is that it is open.** x86-64 belongs to Intel and AMD; ARM licenses its designs. **RISC-V is a free, open standard anyone may implement** — which has produced a Cambrian explosion of processors, from research chips to phone controllers to the vector units in supercomputers, because a company can build one without paying or asking anyone. **The instruction set became a commons**, and that is an organisational innovation as much as a technical one.

---

## 3. Domain-Specific Architectures — Spend the Transistors on One Thing

The GPU (Week 10) was the first big specialisation. The frontier is now chips built for a *single* kind of computation.

### The TPU — a machine for one operation

Google's Tensor Processing Unit does essentially **one thing: multiply-accumulate, in bulk**, because that is 99% of a neural network. It is built around a **systolic array** — a grid of tiny multiply-add units through which data flows rhythmically, each cell doing one multiply and passing the result on, so a single load feeds an entire row of computation.

**Compare with everything this course taught about general-purpose cores.** A CPU spends transistors on caches (Week 4), branch prediction (Week 5), out-of-order execution — all to make *unpredictable, branchy, general* code fast. **A neural network is none of those things: it is a fixed sequence of huge, regular matrix multiplies with no branches.** So the TPU throws away the caches and predictors and spends every transistor on multiply-accumulate units. **Cited figures put it at 15–30× the performance-per-watt of a contemporary GPU on inference** — not by being cleverer, but by refusing to spend anything on generality.

### The FPGA — hardware you rewrite

A **Field-Programmable Gate Array** is a chip full of logic blocks and interconnect you configure *after manufacture* to implement any digital circuit — ECE 110's gates, wired up by software. **It sits between the CPU (fully general, programmed with instructions) and the ASIC (fully fixed, one circuit forever):** you get custom hardware for your exact problem without fabricating a chip, at the cost of being slower and larger than a dedicated ASIC. Used where the workload is specialised but the volume does not justify a custom chip — network packet processing, high-frequency trading, prototyping the next TPU.

### The principle

| Machine | Spends transistors on | Best for |
|---|---|---|
| CPU | caches, prediction, OoO | general, branchy, latency-sensitive code |
| GPU | thousands of simple cores | regular, massively parallel, high-intensity |
| TPU/NPU | multiply-accumulate arrays | neural network inference and training |
| FPGA | reconfigurable logic | custom circuits at low volume |
| ASIC | one fixed circuit | one workload at enormous volume |

**Read the table left to right: increasing specialisation, increasing efficiency, decreasing flexibility.** That trade — **generality against efficiency** — is the single axis the whole frontier moves along, and it is Week 0's abstraction-cost lesson at the level of silicon: every transistor spent on flexibility is a transistor not spent on the workload.

---

## 4. Two Genuinely Different Machines

### Quantum — a different model of computation

A classical bit is 0 or 1. A **qubit** exists in a *superposition* of both until measured, and a set of qubits can be **entangled** so their states are correlated in ways no classical system can represent. A quantum computer manipulates these with quantum gates, and for *specific* problems — factoring (Shor's algorithm), simulating quantum chemistry, some search (Grover's) — it can do in polynomial time what a classical machine needs exponential time for.

**It is not a faster computer; it is a different computer**, good at a narrow class of problems and useless at most of what a CPU does. **The engineering is brutal** — qubits must be kept near absolute zero and decohere in microseconds — and today's machines have hundreds of noisy qubits where a useful one needs millions of error-corrected ones. **This is a decades-out frontier**, and the honest statement is that no one knows if it will become practical. *(Everything here is conceptual; there is no quantum hardware to measure.)*

### Neuromorphic — computing like a brain

Conventional chips separate compute (CPU) from memory (DRAM), and Week 4 showed the enormous cost of moving data between them — the von Neumann bottleneck (Week 0). **Neuromorphic chips co-locate compute and memory** in networks of artificial "neurons" that fire like biological ones, spending energy only when active. For certain sensing and pattern-recognition tasks they are cited at orders-of-magnitude better energy efficiency. **Also early-stage**, and also a bet that the workload — sparse, event-driven, always-on sensing — justifies a machine shaped completely unlike a CPU.

---

## 5. The One Idea Under All of It

Every machine in this lecture is an answer to the same question, and it is the question Week 0 opened with:

> **When you cannot make one general core much faster, you build a specific machine for the workload
> that matters — and you pay for its efficiency in flexibility.**

The GPU matched deep learning's shape. The TPU matched it more tightly. RISC-V bet that simplicity wins. FPGAs sell reconfigurability. Quantum and neuromorphic are bets that entirely different *models* of computation will pay off for narrow but important workloads.

**"The architecture reflects the workload"** is the whole frontier in one sentence, and it is why this is a golden age of computer architecture rather than a dead one: the general-purpose free lunch ended, and the field responded by building a hundred special-purpose machines. **You now understand the general-purpose machine well enough to see why each of the specialised ones exists.**

---

## 6. What to Take Away

1. **The frontier turned to specialisation** because general single-core performance stopped rising for free.
2. **RISC-V** trades more instructions for simpler, more-pipelineable hardware — `add eax,[rdi]` becomes `lw` + `add` — and its real innovation is being an **open standard**.
3. **Domain-specific chips spend every transistor on one workload**: the TPU on multiply-accumulate, the FPGA on reconfigurable logic.
4. **The axis is generality vs efficiency** — CPU → GPU → TPU → ASIC, more specialised, more efficient, less flexible.
5. **Quantum and neuromorphic are different *models* of computation**, decades out, honest bets on narrow workloads.
6. **"The architecture reflects the workload"** is the whole story — Week 0's abstraction-cost lesson at the level of silicon.

---

## Exercises

1. `sum` compiled to `add eax,[rdi]` on x86-64 (one instruction) and `lw`+`add` on RISC-V (two). Explain why RISC-V considers the *higher* instruction count a good trade.
2. A TPU throws away branch predictors and large caches that a CPU spends heavily on. Why can it, and what does it gain? Which Week-5 and Week-4 features is it discarding?
3. Place CPU, GPU, TPU, FPGA and ASIC on the generality-vs-efficiency axis, and give a workload for which each is the right choice.
4. RISC-V's key advantage is being open. Explain why that is an *architectural* advantage and not merely a licensing one, using the "Cambrian explosion" idea.
5. A quantum computer is "not faster, but different". Name a problem it helps and a problem it does not, and say what property distinguishes them.
6. Neuromorphic chips co-locate compute and memory. Which bottleneck from Weeks 0 and 4 does that attack, and why does it help only certain workloads?

---

*Next: L38 — the whole course as one machine.*
