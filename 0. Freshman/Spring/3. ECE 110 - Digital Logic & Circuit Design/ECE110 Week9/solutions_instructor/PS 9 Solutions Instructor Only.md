# ECE 110 · Digital Logic
## Problem Set 9 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Both machines verified against a reference on 2000 random 24-bit sequences; the gate-level Mealy machine verified in Verilog over 4000 cycles.

---

## Part A (5 pts each)

**A1 (5).** Words → what to remember; state diagram; state table; state assignment; equations; circuit and verification.

**Only step 1 requires judgement.** *(Steps 3–5 are mechanical; step 5 is Week 4.)*

**A2 (5).** **The longest matching prefix of `1011`** — nothing, `1`, `10`, `101`. **Four states.**

**Remembering the whole input is impossible** because the input is unbounded and the machine is *finite*; the design insight is that only the prefix affects the future.

**A3 (5).** Diagram as in the reference sheet. **The overlap arc is $D\xrightarrow{1}B$**: a completed `1011` ends in `1`, and that `1` is already a one-bit match for the next pattern — going to $A$ would discard it and miss overlapping matches.

*Marking: 3 diagram, **2 for the overlap explanation.***

**A4 (5).** The four-row state table. *(Verified.)*

---

## Part B (6 pts each)

**B1 (6).** Transition table over $(Q_1,Q_0,X)$ with $A{=}00,B{=}01,C{=}10,D{=}11$.

**B2 (6).**

$$D_1=\sum m(2,5,6) \Rightarrow \boxed{Q_0\overline X + Q_1\overline{Q_0}X}$$
$$D_0=\sum m(1,3,5,7) \Rightarrow \boxed{X}$$
$$Y=\sum m(7) \Rightarrow \boxed{Q_1Q_0X}$$

*(All verified.)*

**B3 (6).** **Two flip-flops.** Logic: 5 literals for $D_1$ (2 ANDs + 1 OR + inverters), a wire for $D_0$, and one 3-input AND for $Y$.

**B4 (6).** **Not luck — a consequence of the assignment.**

$D_0=X$ falls out because in this encoding $Q_0$ is 1 exactly in states $B$ and $D$, which are precisely the states entered on input 1. **A different assignment destroys that alignment** and leaves $D_0$ needing real logic.

> **State assignment is a free choice that costs money**, and this is the concrete demonstration.

*Marking: 3 "not luck", **3 for identifying the alignment.***

**B5 (6).**

$$\texttt{1011011011} \Rightarrow \boxed{\texttt{0001001001}}$$

*(Verified.)*

---

## Part C (6 pts each)

**C1 (6).** **Moore: output depends only on the state.** **Mealy: output depends on the state and the current input.**

**C2 (6).** **Five states.** Because the output must be a property of the state alone, "a match has just completed" needs **its own state** — Mealy expressed that on an arc instead. *(Verified: 5 vs 4.)*

**C3 (6).** **Both give `0001001001`** — *(verified on 2000 random sequences, zero mismatches)* — **when Moore's output is taken from the state after the transition.**

**It depends on the output convention.** Taken from the pre-transition state, Moore lags by one cycle. *Full marks require naming the dependence.*

*Marking: 3 sequences, **3 for the convention.** A bare "yes they agree" earns 3.*

**C4 (6).** **Mealy can glitch**, because its output is combinational logic fed directly by an input — any glitch or slow transition on $X$ appears at $Y$ within the same cycle.

**Consequence (Week 8):** if $Y$ drives a memory write-enable, a glitch is a **spurious write** — at speed, intermittently, invisible to single-stepping. **Moore's output is a function of flip-flop outputs only and is stable for the whole cycle.**

**C5 (6).** **Registered Mealy:** compute $g(S,X)$ combinationally, then pass it through a flip-flop.

**It buys Moore's glitch-free timing with Mealy's smaller state count**, at the cost of one cycle of latency and one flip-flop.

---

## Part D (5 pts each)

**D1 (5).**

| encoding | flip-flops | logic |
|---|---|---|
| binary | $\lceil\log_2n\rceil$ — fewest | most |
| one-hot | $n$ | **least**; output decode is free |
| Gray | $\lceil\log_2n\rceil$ | middling; one bit changes per transition |

**D2 (5).** **Because an FPGA has flip-flops in abundance and logic cells (LUTs) as the scarce resource** *(Week 5)*. One-hot trades the plentiful thing for the scarce one, and **the state bits are already the decoded outputs**, so output logic vanishes. **Tools often convert binary to one-hot without being asked.**

**D3 (5).** $2^3-5 = \boxed{3}$ unused codes.

**You must decide what happens if the machine enters one** — through a glitch, an upset, or a bad power-up. **Either give each a transition to a known state, or guarantee the reset.** A machine that can enter an unused state and stay there **hangs**.

**D4 (5).** Moore, three states, with timer input $T$:

| state | outputs | on $T=0$ | on $T=1$ |
|---|---|:-:|:-:|
| **GREEN** | G=1, Y=0, R=0 | GREEN | YELLOW |
| **YELLOW** | G=0, Y=1, R=0 | YELLOW | RED |
| **RED** | G=0, Y=0, R=1 | RED | GREEN |

**Moore is correct here** — the lights are the state, and they must not glitch.

*Marking: 3 diagram, 2 outputs. **Accept a Mealy version only if the student justifies it**; the natural answer is Moore and the outputs being state-only is the point.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 30 |
| D | 20 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **A3:** the overlap arc going to $A$ instead of $B$ — the single most common FSM error.
2. **B4:** calling $D_0=X$ a coincidence.
3. **C3:** comparing outputs without stating the Moore output convention.
4. **C4:** naming the glitch without a consequence.
5. **D3:** "it can't happen."

---

*ECE 110 · Week 9 · PS 9 Solutions · Instructor Only*
