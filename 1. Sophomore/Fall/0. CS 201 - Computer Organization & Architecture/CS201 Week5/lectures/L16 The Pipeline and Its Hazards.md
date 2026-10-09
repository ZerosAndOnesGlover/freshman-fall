# CS 201 · Computer Organization & Architecture
## Week 5 · Lecture 1 of 3
### The Pipeline and Its Hazards

*“Optimism is an occupational hazard of programming: feedback is the treatment.”* — Kent Beck, *Extreme Programming Explained* (2000), p. 31

---

**Reading:** CS:APP §4.4–4.5 · **Previous:** L15, locality as leverage

**Coursework:** 📊 **Quiz 5** today · 📘 **Midterm 1** today 18:00–19:15 · 🔬 **Lab 4** Tue this week 15:00–16:50 · 📝 **PS 5** released Wed this week, due Fri of Week 6 17:00 · 📝 **PS 4** due Fri this week 17:00

---

## 1. The Conveyor Belt

Week 0 gave you the five stages an instruction passes through: **Fetch, Decode, Execute, Memory, Writeback.** Then it said to treat them as strictly sequential.

That was a useful lie. **A real CPU overlaps them.**

```
        cycle:   1    2    3    4    5    6    7    8    9
  instruction 1: F    D    E    M    W
  instruction 2:      F    D    E    M    W
  instruction 3:           F    D    E    M    W
  instruction 4:                F    D    E    M    W
  instruction 5:                     F    D    E    M    W
```

**Latency is unchanged** — each instruction still takes five cycles end to end. **Throughput improves fivefold** — once the pipeline is full, one instruction completes every cycle.

This is the difference between *latency* and *throughput*, and it is the single most important distinction in performance work. A washing machine takes 90 minutes whether or not you have a dryer; owning both lets you finish four loads in the time one machine would take for two.

**The ideal is one instruction per cycle (IPC = 1).** Everything in this lecture is a reason you do not get it.

---

## 2. Deeper Is Not Better

If five stages give 5× throughput, why not fifty?

**Because the pipeline registers between stages cost time**, and because the penalty for getting anything wrong grows with depth. The Pentium 4 pushed to 20–31 stages chasing clock speed, and its **misprediction penalty was correspondingly ruinous** — every wrong branch threw away 20+ cycles of work.

Modern designs settled around 14–19 stages. **The i5-8250U in front of you is roughly 14**, and its predecessors' 31-stage experiment is why.

---

## 3. Three Ways a Pipeline Stalls

### Structural hazards

Two instructions need the same hardware in the same cycle. **Mostly designed away** — this is why the L1 cache is split into instruction and data halves, so a fetch and a load can proceed together (L02 §6).

### Data hazards

An instruction needs a result that is not ready.

```
add  rax, rbx        ; writes rax in stage W (cycle 5)
sub  rcx, rax        ; needs rax in stage E (cycle 4)
```

**The value is needed before it is written.** Three kinds exist, but only one is a real problem on any modern machine:

| Name | Pattern | Real? |
|---|---|---|
| **RAW** — read after write | `sub` reads what `add` wrote | **Yes.** A true dependency. Unavoidable |
| **WAR** — write after read | A later instruction overwrites a register an earlier one still needs | No — **register renaming** removes it (L17) |
| **WAW** — write after write | Two instructions write the same register | No — renaming removes it too |

**Only RAW is a genuine dependency**, because it reflects the actual flow of data. WAR and WAW are artefacts of having a finite number of register *names*, and the hardware fixes them by having more physical registers than names.

### Control hazards

A branch. **The pipeline must fetch something next cycle, and it does not yet know what.**

This is the expensive one, and L17 is about it.

---

## 4. Forwarding Makes RAW Nearly Free

The naive fix for a RAW hazard is to stall until the value is written back. **Three wasted cycles per dependent pair** — which would be catastrophic, since dependent pairs are everywhere.

**Forwarding (bypassing) routes the result directly from where it is produced to where it is needed**, without waiting for the register file:

```
add  rax, rbx    F  D  E──┐ M  W
sub  rcx, rax       F  D  E  M  W        <- gets rax from the forwarding path
                          ↑
                    result available at the end of E, used at the start of the next E
```

**Back-to-back dependent ALU operations run at one per cycle.** The dependency is real; the stall is not.

**But forwarding cannot beat physics.** A load's result is not available until the end of the M stage, one cycle later than an ALU result:

```
mov  rax, [rbx]  F  D  E  M──┐ W
add  rcx, rax       F  D  ×  E  M  W     <- one unavoidable stall
```

**This is the load-use hazard, and it is the one that still costs.** Compilers schedule loads early precisely to give the result time to arrive — which is why `-O2` listings often load values several instructions before they are used.

---

## 5. Dependencies Are Measurable

The theory says a chain of dependent operations runs at the *latency* of each operation, while independent operations run at the *throughput*. Measure it.

```c
double a = 0;                            double b0=0,b1=0,b2=0,b3=0;
for (long i = 0; i < N; i++)             for (long i = 0; i < N; i += 4)
    a += 1.0;                                { b0+=1.0; b1+=1.0; b2+=1.0; b3+=1.0; }
```

**Exactly the same number of additions** — 200 million. The left has one dependency chain; the right has four independent ones.

```
1 chain,  200000000 adds   0.4768 s   2.38 ns/add
4 chains, 200000000 adds   0.1191 s   0.60 ns/add
speedup 4.00x  (same number of additions)
```

*(Measured, and reproducible to two decimal places across runs.)*

**Exactly 4.00×.** The single chain is limited by the *latency* of a floating-point add — each one must complete before the next begins. The four chains are limited by *throughput*, and the hardware overlaps them.

> **This is the practical meaning of instruction-level parallelism.** The processor will overlap
> independent work automatically and aggressively, but it cannot invent independence that is not
> there. **A serial dependency chain is the one thing that reliably defeats a modern CPU**, and
> breaking accumulator chains is one of the highest-value transformations in numerical code.
>
> It is also why Week 1's Kahan summation is slow: each step depends on the last, by construction.

---

## 6. How Fast Is This Machine, Really?

Worth establishing, since the next two lectures quote cycles.

A loop of dependent integer `add`s — one cycle latency on any x86-64 since about 2006:

```
2e9 dependent add/sub/jne iterations in 0.6230 s
=> ~3.21 GHz
```

*(Measured.)* And `/proc/cpuinfo` reports 3399 MHz on the active cores at the time. **So ~3.2–3.4 GHz sustained**, which is what Week 4's cycle conversions assumed.

**Measure your own machine before trusting any cycle figure in these notes.** The governor is `powersave`, cores idle at 400 MHz, and a lightly loaded core turbos — a "cycles" number quoted without a measured clock is guesswork.

---

## 7. What to Take Away

1. **Pipelining improves throughput, not latency.** Five stages, one instruction per cycle at best.
2. **Deeper pipelines raise the misprediction penalty**; 20–31 stages was tried and abandoned.
3. **Structural, data, control** — three hazard classes.
4. **Only RAW is a true dependency.** WAR and WAW are naming artefacts, removed by renaming.
5. **Forwarding makes ALU-to-ALU dependencies free.** The load-use hazard still costs a cycle.
6. **Independent work overlaps: four chains ran 4.00× faster than one**, on identical arithmetic.
7. **A serial dependency chain is what defeats a modern CPU.**

---

## Exercises

1. A 5-stage pipeline at 1 GHz against a non-pipelined design at 1 GHz. Compare latency and throughput for one instruction, and for 1000.
2. Identify every hazard in this sequence and name its type:

```
mov  rax, [rbx]
add  rax, rcx
mov  [rdx], rax
sub  rcx, rdi
mov  rcx, [rsi]
```

3. Explain why register renaming removes WAR and WAW but cannot remove RAW.
4. The load-use hazard costs one cycle even with forwarding. Why can forwarding not eliminate it, when it eliminates the ALU-to-ALU case entirely?
5. The four-chain loop ran 4.00× faster. Predict what eight chains would give, then say what would limit it.

---

*Next: L17 — what the CPU does when it does not know where the branch goes.*
