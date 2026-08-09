# ECE 110 · Digital Logic
## Midterm · Revision Guide
### Covering Weeks 0–5

---

## The Exam

| | |
|---|---|
| **When** | Week 6 |
| **Duration** | **75 minutes** |
| **Covers** | **Weeks 0–5** — number systems through multiplexers |
| **Not covered** | **Week 6** (the ALU and carry-lookahead). Those are on the final. |
| **Weight** | **25%** of the course |
| **Total** | 100 points |
| **Allowed** | **One handwritten sheet, one side.** No calculator. |

**Character.** Roughly half the paper is *do it* — convert this, minimise that, draw this circuit. The rest is *justify it*: state a rule, prove an impossibility, explain which cost you are paying. **A correct circuit with no gate count or no stated convention loses marks.**

---

## Topic Checklist

Tick only what you could do **from a blank page, under time.**

### Week 0 — Number systems
- [ ] Convert between binary, octal, hex, decimal — **grouping from the right**
- [ ] Repeated division (integers) and repeated multiplication (fractions)
- [ ] Which fractions terminate in binary, **and why** (denominator's prime factors)
- [ ] Two's complement encode/decode; the **asymmetric range**; $-(-128)=-128$
- [ ] **Sign extension**, not zero extension
- [ ] **Carry vs overflow are independent**; $V=C_{in}\oplus C_{out}$
- [ ] BCD, the add-six correction, and what BCD is actually exact about

### Week 1 — Boolean algebra
- [ ] The axioms; **$A+BC=(A+B)(A+C)$** and absorption
- [ ] **De Morgan** both ways; $\overline{AB}\ne\overline A\,\overline B$
- [ ] Duality — **and that it is not complementation**
- [ ] Consensus $AB+\overline AC+BC=AB+\overline AC$
- [ ] Canonical SOP and POS; **minterms complement on 0, maxterms on 1**
- [ ] $2^{2^n}$ functions

### Week 2 — Gates
- [ ] Seven gates; **CMOS transistor counts** (NOT 2, NAND/NOR 4, AND/OR 6, XOR 12)
- [ ] **Why AND costs more than NAND**
- [ ] The digital abstraction, restoration, noise margins, **floating inputs**
- [ ] NAND and NOR are each **universal** — the constructions
- [ ] **$\{$AND, OR$\}$ is not** — the monotonicity proof
- [ ] AND-OR → NAND-NAND conversion is **free**
- [ ] **Fan-in, fan-out, critical path**

### Week 3 — Adders
- [ ] Half adder (2 gates), full adder (5 gates)
- [ ] $S=A\oplus B\oplus C_{in}$; $C_{out}=AB+(A\oplus B)C_{in}$
- [ ] **$t_{\text{ripple}}=2N+1$** — and be able to derive it
- [ ] Adder/subtractor: **`SUB` drives the XORs *and* the carry-in**
- [ ] $V=C_{N-1}\oplus C_{out}$
- [ ] **Gate count is area, critical path is speed**

### Week 4 — Karnaugh maps
- [ ] Gray order; **edges and corners wrap**
- [ ] Group rules; **maximal groups, then fewest**
- [ ] **Prime and essential prime implicants**
- [ ] Don't-cares — **and that they are a claim about the world**
- [ ] POS from the zeros; **neither form always wins**
- [ ] Quine–McCluskey exists and why tools use heuristics

### Week 5 — MSI blocks
- [ ] Decoder ($2^n$ ANDs), encoder, **priority encoder and its valid bit**
- [ ] Mux, demux, **demux = decoder with enable as data**
- [ ] **Shannon expansion**
- [ ] **A $2^{k-1}$:1 mux implements any $k$-variable function**
- [ ] Why a LUT's cost is function-independent

---

## The Ten Errors That Cost The Most Marks

**Every one has appeared on a problem set or quiz.**

1. **Grouping bits from the left** when converting to hex or octal.
2. **Zero-extending a negative number.**
3. **Treating carry-out as an error flag for signed arithmetic.**
4. **$\overline{AB}=\overline A\,\overline B$** — breaking the bar without changing the operator.
5. **Complementing variables when forming a dual.**
6. **Complementing maxterms on 0** instead of 1.
7. **Missing the four-corner group** on a K-map.
8. **Stopping at a correct cover** without checking every group is maximal.
9. **Forgetting `SUB` drives the carry-in**, not just the XORs.
10. **Giving a gate count with no stated convention.**

> **Six of these are failures to check something you already knew to check.**

---

## Building Your Sheet

**One side. That is deliberately tight** — you cannot fit everything, so you must choose.

| Put on it | Leave off |
|---|---|
| CMOS transistor counts | anything you can re-derive in 10 seconds |
| $t=2N+1$; full adder equations | the seven gate truth tables |
| $V=C_{in}\oplus C_{out}$ | conversion procedures you have drilled |
| K-map template with minterm numbers | the Boolean axioms *(you know these)* |
| Prime/essential definitions | |
| Mux data-input derivation method | |
| **Your own three recurring errors** | |

> **Write it by hand from the reference sheets.** The writing is the revision.

---

---

# Sample Paper

**75 minutes. 100 points. One handwritten sheet. No calculator.**

---

**Q1 (14 pts) — Number systems.**
**(a)** Convert $203_{10}$ to binary, octal and hex.
**(b)** Give $-45$ in 8-bit two's complement, and sign-extend it to 16 bits.
**(c)** For $100+50$ in 8-bit signed arithmetic, give the result, $C$ and $V$, and say which reader — signed or unsigned — has a correct answer.

---

**Q2 (14 pts) — Boolean algebra.**
**(a)** Simplify $\overline A B + AB + A\overline B$.
**(b)** Complement $(A+\overline B)C$.
**(c)** Prove the consensus theorem $AB+\overline AC+BC = AB+\overline AC$.

---

**Q3 (16 pts) — Gates.**
**(a)** Why does AND cost 6 transistors and NAND 4?
**(b)** Build XOR from NAND gates. How many, and which sub-expression is shared?
**(c)** **Prove** that $\{$AND, OR$\}$ is not functionally complete.

---

**Q4 (18 pts) — Adders.**
**(a)** Give $S$ and $C_{out}$ for a full adder and its gate count.
**(b)** Derive the delay of an $N$-bit ripple-carry adder. Evaluate at $N=8$.
**(c)** Show how one adder does both addition and subtraction. **What does `SUB` drive?**
**(d)** A 64-bit ripple adder is 320 gates and 129 gate delays. **Which number is the problem, and against what is it measured?**

---

**Q5 (20 pts) — Karnaugh maps.**
**(a)** Minimise $F=\sum m(0,2,8,10)$.
**(b)** Minimise $F=\sum m(0,1,2,3,4,5,10,11,14,15)$ as SOP **and** as POS. Which is cheaper?
**(c)** Minimise $\sum m(5,6,7,8,9)+\sum d(10,11,12,13,14,15)$, and state what you are assuming.

---

**Q6 (18 pts) — MSI blocks.**
**(a)** Why does a plain encoder need a *valid* output?
**(b)** Implement $F=\sum m(1,2,4,7)$ on a 4:1 mux with $A,B$ selecting. Give the data inputs and name the function.
**(c)** A LUT costs the same whatever function is in it. **What does that imply for minimisation on an FPGA?**

---

---

# Sample Paper — Answers

---

**Q1 (14).**
**(a)** $203 = \boxed{11001011_2 = 313_8 = \texttt{CB}_{16}}$ *(verified)*
**(b)** $-45 = \boxed{11010011}$; sign-extended $\boxed{1111111111010011}$ *(verified)*
**(c)** $100+50$: bits $10010110$, $C=\mathbf0$, $V=\mathbf1$. **Signed reads $-106$ — wrong. Unsigned reads $150$ — correct.** *(Verified.)* **The unsigned reader is right; the signed reader should have checked $V$.**

**Q2 (14).**
**(a)** $\overline AB+AB+A\overline B = B(\overline A+A)+A\overline B = B+A\overline B = \boxed{A+B}$ *(verified)*
**(b)** $\overline{(A+\overline B)C} = \overline{A+\overline B}+\overline C = \boxed{\overline AB+\overline C}$ *(verified)*
**(c)** $AB+\overline AC+BC = AB+\overline AC+BC(A+\overline A) = AB(1+C)+\overline AC(1+B) = AB+\overline AC$ ∎

**Q3 (16).**
**(a)** CMOS naturally produces the **complement** of its pull-down condition, so NAND is one 4-transistor stage; **AND is a NAND plus an inverter**, $4+2=6$.
**(b)** $A\oplus B = (A\,\text{NAND}\,X)\,\text{NAND}\,(B\,\text{NAND}\,X)$ with $X=A\,\text{NAND}\,B$. $\boxed{4}$ gates; **$X$ is shared** — computing it twice gives 5.
**(c)** AND and OR are **monotone**; composition preserves monotonicity; **NOT is not monotone**; therefore NOT is unbuildable. ∎ *(Verified.)*

**Q4 (18).**
**(a)** $S=A\oplus B\oplus C_{in}$, $C_{out}=AB+(A\oplus B)C_{in}$, $\boxed{5}$ gates.
**(b)** Stage 0's carry costs 3, each later stage 2, the top sum bit 1: $t=3+2(N-1)=\boxed{2N+1}$. **At $N=8$: 17.** *(Verified.)*
**(c)** One XOR per $B$ bit, driven by `SUB`; **`SUB` also drives the least significant carry-in**, supplying the $+1$ of $A+\overline B+1$.
**(d)** **The delay.** 320 gates is negligible against a chip's budget; **129 gate delays is measured against the clock period** — 2.58 ns against 0.33 ns is 7.7 cycles.

**Q5 (20).**
**(a)** $\boxed{\overline B\,\overline D}$ — the four corners, both edges wrapping. *(Verified.)*
**(b)** SOP $AC+\overline A\,\overline B+\overline A\,\overline C$ (**6** literals); POS $(C+\overline A)(A+\overline B+\overline C)$ (**5**). $\boxed{\text{POS is cheaper}}$ *(verified)*
**(c)** $\boxed{A+BC+BD}$ — 5 literals. **Assumption: the inputs $1010$–$1111$ cannot occur**, because the value is a BCD digit. *(Verified.)*

**Q6 (18).**
**(a)** Because code $00$ is ambiguous: it means both "$I_0$ asserted" and "nothing asserted". **The valid bit distinguishes them.**
**(b)** Data inputs $\boxed{C,\ \overline C,\ \overline C,\ C}$; the function is $\boxed{\text{parity}}$, $A\oplus B\oplus C$. *(Verified.)*
**(c)** **Minimisation stops mattering.** A LUT holds $2^k$ bits whether the function is 2 gates or 11 literals, so an FPGA tool packs and routes instead of minimising.

---

## Marking of the Sample Paper

| Q | Points | Where the marks are |
|---|---|---|
| 1 | 14 | 6 + 4 + 4; **(c) needs both readings and a verdict** |
| 2 | 14 | 4 + 4 + 6; **(c) needs the $(A+\overline A)$ step** |
| 3 | 16 | 5 + 5 + 6; **(c) is worthless without the property** |
| 4 | 18 | 4 + 5 + 4 + 5; **(b) must be derived, not recalled** |
| 5 | 20 | 6 + 8 + 6; **(c) needs the stated assumption** |
| 6 | 18 | 6 + 6 + 6 |

**A pass is about 55; a strong performance is 80+.**

> **If you scored below 50, look at where.** Losses in Q1 and Q4 mean the arithmetic thread —
> reread Weeks 0 and 3 together, since they are one topic. Losses in Q3(c) and Q5 mean you are
> computing but not justifying, which is half the paper.

---

## The Week Before

1. **Rework PS 0–5 from a blank page**, timed.
2. **Drill K-maps** until the four-corner and eight-cell groups are automatic. Highest-value revision available.
3. **Be able to derive $2N+1$**, not recite it.
4. **Practise the two impossibility proofs** — they are 6 marks and they are short.
5. **Build your sheet by hand**, and put your own recurring errors on it.
6. **Do this sample paper in one 75-minute sitting.**

---

**Good luck.** *State your convention, count your gates, and check the thing you already know to check.*

---

*ECE 110 · Midterm Revision Guide · covers Weeks 0–5*
