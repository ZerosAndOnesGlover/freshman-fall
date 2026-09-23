# ECE 110 · Digital Logic
## Final Exam · Revision Guide
### Covering Weeks 0–12

---

## The Exam

| | |
|---|---|
| **When** | **Monday 19 April 2027, 08:00–10:00** (finals week) |
| **Duration** | **120 minutes** |
| **Covers** | **Weeks 0–12 — comprehensive** |
| **Weight** | **15%** of the course |
| **Total** | 100 points |
| **Allowed** | **Two handwritten pages.** No calculator. |

**Weighting.** Combinational logic (Weeks 0–6) is about half the paper; sequential (7–9) about a third; Verilog, memory and programmable logic (10–12) the remainder. **The midterm's material is examinable again** — this is a comprehensive paper, not a second midterm.

**Character.** Half *do it*, half *justify it*. **A circuit with no gate count, or a count with no stated convention, loses marks.**

---

## Topic Checklist

Tick only what you could do **from a blank page, under time.**

### Weeks 0–2 — numbers, algebra, gates
- [ ] Conversions, **grouping from the right**; which fractions terminate and why
- [ ] Two's complement; **asymmetric range**; $-(-128)=-128$; **sign extension**
- [ ] **Carry and overflow are independent**; $V=C_{in}\oplus C_{out}$
- [ ] BCD, the add-six correction, and what BCD is exact about
- [ ] The axioms; $A+BC=(A+B)(A+C)$; absorption; **consensus**
- [ ] **De Morgan**; duality is *not* complementation
- [ ] Canonical SOP/POS; **minterms complement on 0, maxterms on 1**
- [ ] **CMOS counts** (2/4/4/6/6/12); **why AND costs more than NAND**
- [ ] NAND and NOR universal; **the monotonicity proof that $\{$AND,OR$\}$ is not**
- [ ] AND-OR → NAND-NAND is free; **fan-in, fan-out, critical path**

### Weeks 3–6 — arithmetic and blocks
- [ ] Half/full adder; $C_{out}=AB+(A\oplus B)C_{in}$
- [ ] **$t_{\text{ripple}}=2N+1$, derived not recalled**
- [ ] Adder/subtractor: **`SUB` drives the XORs *and* the carry-in**
- [ ] K-maps: **wrapping edges and corners**, maximal groups, **prime and essential implicants**
- [ ] Don't-cares — **a claim about the world**
- [ ] Decoder, priority encoder and its **valid** bit, mux, demux
- [ ] **Shannon**; a $2^{k-1}$:1 mux does any $k$-variable function
- [ ] ALU structure; **shift and compare cost no gates**; $C$, $V$, $Z$, $N$; **$A<B$ is $N\oplus V$**
- [ ] $G_i$, $P_i$, the carry recurrence; **why flat 64-bit lookahead is impossible**

### Weeks 7–9 — sequential
- [ ] SR latch; **why $S=R=1$ is forbidden**; the race
- [ ] Gated D latch makes it unreachable; **master–slave is edge-triggered**
- [ ] JK toggles; **excitation tables and JK's don't-cares**
- [ ] $T_{clk}\ge t_{cq}+t_{\text{logic}}+t_{su}$; **hold violations need delay, not a slower clock**
- [ ] Metastability and the synchroniser — **a probability, not a guarantee**
- [ ] **Ripple counter transients**; synchronous $T_k$ = AND of lower bits
- [ ] Mod-N by detect-and-clear; **ring counters need no decode**
- [ ] FSM six steps; **overlap arcs**; Mealy vs Moore; **state assignment is free and costs money**

### Weeks 10–12 — description and silicon
- [ ] **`<=` sequential, `=` combinational**; the inferred latch; the sensitivity list
- [ ] `reg` does not mean register
- [ ] SRAM 6T, DRAM 1T, flip-flop ~20T; **refresh arithmetic**
- [ ] **Square arrays**; row/column strobes; locality
- [ ] ROM = decoder + OR plane; **three routes to the lookup table**
- [ ] PLA vs PAL vs ROM sizing; **LUT cost is function-independent**

---

## The Twelve Errors That Cost The Most Marks

1. **Grouping bits from the left.**
2. **Zero-extending a negative number.**
3. **Treating carry-out as an error flag for signed arithmetic.**
4. **$\overline{AB}=\overline A\,\overline B$.**
5. **Complementing maxterms on 0.**
6. **Missing a four-corner or eight-cell K-map group.**
7. **Forgetting `SUB` drives the carry-in.**
8. **Using $N$ alone for signed comparison.**
9. **Sending an FSM overlap arc to the start state.**
10. **`=` in a clocked block.**
11. **A gate count with no stated convention.**
12. **Answering "which is better" instead of naming the cost.**

---

## Building Your Two Pages

| page | contents |
|---|---|
| **1** | CMOS transistor counts · two's complement and $V$ · full adder equations and $2N+1$ · K-map template with minterm numbers · prime/essential definitions · mux data-input method |
| **2** | Flip-flop characteristic **and excitation** tables · $T_{clk}$ inequality · counter $T_k$ rule · FSM six steps · Verilog's three traps · memory cell costs and the refresh formula · **your own recurring errors** |

**Write it by hand from the reference sheets. The writing is the revision.**

---

---

# Sample Paper

**120 minutes. 100 points. Two handwritten pages. No calculator.**

---

**Q1 (12) — Numbers.**
**(a)** Convert $156_{10}$ to binary, octal and hex.
**(b)** Give $-75$ in 8-bit two's complement and sign-extend to 16 bits.
**(c)** For $90+60$ in 8 bits, give the result, $C$, $V$, and say which reader — signed or unsigned — is correct.

**Q2 (12) — Algebra and gates.**
**(a)** Simplify $AB+A\overline B+\overline AB$.
**(b)** Complement $(A+\overline B)C$.
**(c)** Prove $\{$AND, OR$\}$ is not functionally complete.

**Q3 (14) — Adders.**
**(a)** Give $S$ and $C_{out}$ for a full adder and its gate count.
**(b)** Derive $t_{\text{ripple}}$ and evaluate at $N=16$.
**(c)** How does one adder do subtraction? What does `SUB` drive?
**(d)** A 64-bit ripple adder is 320 gates and 129 gate delays. **Which is the problem, and measured against what?**

**Q4 (14) — Karnaugh maps.**
**(a)** Minimise $\sum m(0,1,4,5,8,9,12,13)$.
**(b)** Minimise $\sum m(1,5,7,9,11,13,15)$ as SOP **and** POS. Which is cheaper?
**(c)** Minimise $\sum m(2,3,10,11)+\sum d(6,7,14,15)$, **and state your assumption.**

**Q5 (12) — Blocks.**
**(a)** Why does a plain encoder need a *valid* output?
**(b)** Implement $\sum m(0,2,5,7)$ on a 4:1 mux with $A,B$ selecting. Give the data inputs and name the function.
**(c)** Why is a LUT's cost independent of the function in it?

**Q6 (12) — Sequential.**
**(a)** Why is $S=R=1$ forbidden, and what happens when you leave that state?
**(b)** Give the JK excitation table.
**(c)** With $t_{cq}=60$ ps, $t_{su}=40$ ps and 1.30 ns of logic, give $T_{min}$ and $f_{max}$.

**Q7 (12) — Counters and FSMs.**
**(a)** A 4-bit ripple counter goes `0111` → `1000`. **List every intermediate state**, and give a consequence.
**(b)** Give $T_0$–$T_3$ for a synchronous counter.
**(c)** In a `1011` detector, from the state meaning `101` on input 1, **where do you go and why?**

**Q8 (12) — Description and silicon.**
**(a)** What hardware is `always @(*) if (en) y = d;`? Why?
**(b)** Why do simulation and silicon disagree for `always @(a) y = a & b;`? **Which is wrong?**
**(c)** 8192 rows, 64 ms retention, tRFC 350 ns: refresh interval and overhead.

---

---

# Sample Paper — Answers

---

**Q1 (12).**
**(a)** $\boxed{10011100_2 = 234_8 = \texttt{9C}_{16}}$
**(b)** $\boxed{10110101}$; sign-extended $\boxed{1111111110110101}$
**(c)** `10010110`, $C=\mathbf0$, $V=\mathbf1$. **Signed reads $-106$ (wrong); unsigned reads $150$ (correct).** *(All verified.)*

**Q2 (12).**
**(a)** $B(A+\overline A)+A\overline B = B+A\overline B = \boxed{A+B}$
**(b)** $\boxed{\overline AB+\overline C}$ *(verified)*
**(c)** AND and OR are **monotone**; composition preserves monotonicity; **NOT is not monotone**; so NOT is unbuildable. ∎

**Q3 (14).**
**(a)** $S=A\oplus B\oplus C_{in}$, $C_{out}=AB+(A\oplus B)C_{in}$, **5 gates**.
**(b)** $3+2(N-1)=2N+1$; at $N=16$, $\boxed{33}$.
**(c)** One XOR per $B$ bit driven by `SUB`; **`SUB` also drives the least significant carry-in**, giving the $+1$.
**(d)** **The delay.** 320 gates is negligible; **129 gate delays is measured against the clock period** — 2.58 ns against 0.33 ns is 7.75 cycles.

**Q4 (14).**
**(a)** $\boxed{\overline C}$ — one group of eight. *(Verified.)*
**(b)** SOP $AD+BD+D\overline C$ (**6** literals); POS $D(A+B+\overline C)$ (**4**). $\boxed{\text{POS is cheaper}}$ *(verified)*
**(c)** $\boxed{C}$ — one literal. **Assumption: the don't-care inputs cannot occur.** *(Verified.)*

**Q5 (12).**
**(a)** Code $00$ is ambiguous — "$I_0$ asserted" and "nothing asserted" both give it. **Valid distinguishes them.**
**(b)** Data $\boxed{\overline C,\ \overline C,\ C,\ C}$; the function is $\boxed{\overline{A\oplus C}}$ — **XNOR of $A$ and $C$, independent of $B$.** *(Verified.)*
**(c)** **A LUT stores $2^k$ bits regardless of what those bits are** — the table's size is set by the input count alone.

**Q6 (12).**
**(a)** **Both outputs go to 0**, so $Q$ and $\overline Q$ stop being complementary. **Leaving that state is a race** whose outcome is set by which gate is faster, not by the inputs.
**(b)** $0\to0$: $0\times$; $0\to1$: $1\times$; $1\to0$: $\times1$; $1\to1$: $\times0$.
**(c)** $T_{min}=0.06+1.30+0.04=\boxed{1.40\text{ ns}}$, $f_{max}=\boxed{714\text{ MHz}}$. *(Verified.)*

**Q7 (12).**
**(a)** `0111` → `0110` → `0100` → `0000` → `1000`. **Three transient states.** *(Verified.)* **A decoder watching it glitches** — an output meant for `0000` fires spuriously, and if it is a write-enable that corrupts memory.
**(b)** $T_0=1$, $T_1=Q_0$, $T_2=Q_0Q_1$, $T_3=Q_0Q_1Q_2$.
**(c)** **To the state meaning `1`.** The detected `1011` ends in a 1, which is itself the first bit of the next possible match; going to the start state misses overlapping occurrences.

**Q8 (12).**
**(a)** **A latch.** Nothing is assigned when `en=0`, so `y` must hold its old value.
**(b)** **Simulation obeys the sensitivity list and misses `b` changing; synthesis ignores the list and builds a real AND gate.** $\boxed{\text{The simulation is wrong}}$ — the testbench passes and the chip fails.
**(c)** $64\text{ ms}/8192=\boxed{7.81\ \mu\text{s}}$; $8192\times350\text{ ns}/64\text{ ms}=\boxed{4.5\%}$. *(Verified.)*

---

## Marking

| Q | Points | Where the marks are |
|---|---|---|
| 1 | 12 | **(c) needs both readings and a verdict** |
| 2 | 12 | **(c) is worthless without the property** |
| 3 | 14 | **(b) derived, not recalled; (d) names the clock period** |
| 4 | 14 | **(b) needs both forms; (c) needs the assumption** |
| 5 | 12 | (b) must name the function |
| 6 | 12 | (a) needs the race, not just the forbidden state |
| 7 | 12 | **(a) needs all three transients and a consequence** |
| 8 | 12 | **(b) must say which one is wrong** |

**A pass is about 50; a strong performance is 78+.**

---

## The Week Before

1. **Rework PS 0–11 from a blank page**, timed.
2. **Drill K-maps** until corners and eight-cell groups are automatic.
3. **Derive $2N+1$** rather than recalling it.
4. **Practise the monotonicity proof** — it is short and it is worth 6 marks.
5. **Memorise the three Verilog traps** and what each produces.
6. **Do this paper in one 120-minute sitting.**

---

**Good luck.** *State your convention, count your gates, and name the cost you are paying.*

---

*ECE 110 · Final Exam Revision Guide · covers Weeks 0–12*
