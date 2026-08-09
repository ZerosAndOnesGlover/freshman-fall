# ECE 110 · Digital Logic
## Lab 9 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures from Icarus Verilog 12.0 and a Python reference.

---

## Part A — Design On Paper (25 pts)

### A1 (8), A2 (7)

**Four states; the overlap arc is $D\xrightarrow{1}B$.** *(Students who send it to $A$ will fail B2's trace at the sixth bit — let them find it there.)*

### A3 (10)

$$D_1=Q_0\overline X+Q_1\overline{Q_0}X \qquad D_0=X \qquad Y=Q_1Q_0X$$

*(Verified.)*

*Marking: **maps must be shown.** The equations are printed in the lab text, so answers without maps earn 3 of 10.*

---

## Part B — Build It (25 pts)

### B1 (15), B2 (6)

**Trace for `1011011011`, starting in $A$:**

| bit | state before | $Y$ | state after |
|:-:|:-:|:-:|:-:|
| 1 | $A$ | 0 | $B$ |
| 0 | $B$ | 0 | $C$ |
| 1 | $C$ | 0 | $D$ |
| **1** | $D$ | **1** | $B$ |
| 0 | $B$ | 0 | $C$ |
| 1 | $C$ | 0 | $D$ |
| **1** | $D$ | **1** | $B$ |
| 0 | $B$ | 0 | $C$ |
| 1 | $C$ | 0 | $D$ |
| **1** | $D$ | **1** | $B$ |

$$\text{output} = \texttt{0001001001}$$

*(Verified.)*

### B3 (4)

**Reset returns the machine to $A$.**

**Why not optional:** flip-flops power up in an undefined state, so without a reset the machine may begin in any state — or, in simulation, in `x`. **Week 8's ring counter stuck at `0000` is the same lesson.**

---

## Part C — Both Machines in Verilog (30 pts)

### C1 (10), C2 (10)

**Moore needs five states** because "a match just completed" must be a property of the state itself.

### C3 (10)

$$\textbf{4000 cycles, 0 failures}\ \text{(Mealy)}; \quad \textbf{2000 random sequences, 0 mismatches}\ \text{(both, against the reference)}$$

*(Measured.)*

> ⚠ **The reset bug is real and we hit it.** With `reg rst = 1;` and
> `always @(posedge clk or posedge rst)`, **there is no rising edge on `rst`**, so the asynchronous
> reset never fires: `q` stays `xx` and `y` is `x` for the first cycles. Our first run reported
> exactly one failure, at $t=2$, with `y=x`.
>
> **Expect this in submissions.** The symptom is a small number of failures at the very start and
> `x` in the output. **The fix is to pulse the reset.**

*Marking: 6 testbench, **4 for reporting both machines' counts.** A student who hit the reset bug and diagnosed it should be given full marks and told so.*

---

## Part D — Compare (20 pts)

### D1 (6)

| | states | flip-flops | next-state literals |
|---|---:|---:|---:|
| **Mealy** | **4** | **2** | 5 ($D_1$) + 0 ($D_0$) |
| Moore | 5 | 3 | more |

### D2 (7)

**Both produce `0001001001`** — *(verified)* — **provided Moore's output is read from the post-transition state.** Read from the pre-transition state it lags by one cycle.

*Marking: 4 agreement, **3 for naming the convention.***

### D3 (7)

$$\boxed{\text{Moore.}}$$

**A Mealy output is fed directly by $X$, so a glitch on $X$ reaches $Y$ within the cycle.** **In Lab 8 we photographed exactly that class of glitch** on a decoder watching a ripple counter — narrow pulses on an output that should have been quiet.

**If $Y$ is a write-enable, such a pulse is a spurious write.** Moore's output depends only on flip-flop outputs and is stable for the whole cycle.

*(A registered Mealy output is also a full-marks answer.)*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 30 |
| D | 20 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **A1's overlap arc goes to $B$**
2. **A3 shows the K-maps**
3. B2's trace matches `0001001001`
4. B3 explains why reset is mandatory
5. **C2 says why Moore needs five states**
6. C3 reports counts for both machines
7. **D2 names the output convention**
8. **D3 chooses Moore and cites Lab 8**

---

## Note for the Debrief

**Start with the overlap arc, because it is where half the room went wrong.**

> **From state $D$, on a 1, you go to $B$ — not back to the start.** The pattern you just detected
> **ends** in a 1, and that same 1 is the first bit of the next possible match. **Sending it to $A$
> throws away information the machine already has**, and the failure only shows up on the sixth bit
> of the test sequence.

Then the two-machine comparison:

> **Same specification, two machines, both correct.** Mealy: four states, two flip-flops, responds in
> the same cycle. Moore: five states, three flip-flops, output cannot glitch.
>
> **Neither is better. They are a trade**, and you now have the numbers.

Then close the sequential arc, and set up Week 10:

> **Three weeks ago a circuit could not remember anything. Today you built one that recognises a
> pattern in an unbounded stream using two flip-flops and five literals.**
>
> **Everything in it was Week 4's K-maps and Week 7's flip-flops.** What is new is the *procedure* —
> and the procedure is mechanical enough that a machine could do it.
>
> **Next week you find out that one does.** You will write this machine in Verilog as a state
> diagram in text, and a tool will produce the equations you spent Wednesday deriving by hand.

---

*ECE 110 · Week 9 · Lab 9 Solutions · Instructor Only*
