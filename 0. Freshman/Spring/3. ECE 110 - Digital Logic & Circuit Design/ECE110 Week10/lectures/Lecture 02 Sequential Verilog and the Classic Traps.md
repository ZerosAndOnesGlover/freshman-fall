# ECE 110 · Digital Logic
## Week 10 · Lecture 2 (Thursday)
### Sequential Verilog and the Classic Traps

---

**Reading:** Harris & Harris §4.4–4.6 | Mano & Ciletti §5.8
**PS 10** released today, due Thursday of Week 11.

---

## 1. Describing a Flip-Flop

```verilog
always @(posedge clk)
  q <= d;
```

**That is a D flip-flop.** The sensitivity to `posedge clk` is what makes it storage — **not the word `reg`.**

**With an asynchronous reset:**

```verilog
always @(posedge clk or posedge rst)
  if (rst) q <= 0;
  else     q <= d;
```

> ⚠ **A reset already asserted at time 0 never fires** — `posedge rst` needs a rising *edge*. Your
> state stays `x`. **Pulse it: 0 → 1 → 0.** *(This cost us a debugging session in Week 9, and it is
> the same lesson as Week 8's ring counter stuck at `0000`.)*

---

## 2. Trap One — Blocking vs Non-Blocking

**`=` is blocking: it takes effect immediately, and later statements see the new value.**
**`<=` is non-blocking: the right-hand sides are all evaluated first, then all the assignments happen together.**

**Hardware updates all its flip-flops simultaneously on the edge. That is what `<=` models.**

### Measured

**A three-stage shift register, written both ways:**

| cycle | `<=` | `=` |
|:-:|:-:|:-:|
| 0 | `xx1` | `111` |
| 1 | `x10` | `000` |
| 2 | `100` | `000` |
| 3 | `000` | `000` |

*(Measured.)*

**With `<=` the 1 walks through the register, which is what a shift register does.**

**With `=`, `q[0]=d` takes effect immediately, so `q[1]=q[0]` sees the *new* value, and so does `q[2]`.** All three bits get $d$ in the same cycle — **three flip-flops behaving as one.**

$$\boxed{\texttt{<=} \text{ in sequential blocks} \qquad \texttt{=} \text{ in combinational blocks}}$$

**This is not a style preference. The two produce different hardware.**

---

## 3. Trap Two — The Inferred Latch

```verilog
always @(*)
  if (en) y = sel ? b : a;      // no else
```

**What did you ask for when `en=0`?** Nothing. **So the tool must build something that holds `y` at its previous value — a latch.**

### Measured

| $a$ | $b$ | $sel$ | $en$ | this code | with a default |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | 0 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | **0** | **1** *(held)* | **0** |
| **0** | 0 | 0 | 0 | **1** *(still held)* | 0 |

*(Measured — the output stayed at 1 even after its input changed.)*

**You asked for a multiplexer and got memory.**

### Why it is serious

**Week 7: a latch is level-sensitive and transparent.** An unintended one in a synchronous design creates a timing path nobody analysed, and it is a standard source of designs that pass simulation and fail on silicon.

**The fixes, either one:**

```verilog
always @(*) begin
  y = 1'b0;                     // default first
  if (en) y = sel ? b : a;
end
```

**or make every branch assign every output** — an `else`, and a `default` in every `case`.

> **Synthesis tools warn about inferred latches. Read the warnings.** Nearly every real one is a bug.

---

## 4. Trap Three — The Sensitivity List

```verilog
always @(a) y = a & b;        // b is missing
```

### Measured

| $a$ | $b$ | this code | `always @(*)` |
|:-:|:-:|:-:|:-:|
| 1 | 0 | 0 | 0 |
| 1 | **1** | **0** | **1** |

*(Measured — changing `b` did nothing.)*

**Simulation obeys the list.** **Synthesis ignores it** and builds a proper AND gate, because a gate has no sensitivity list.

> **So the simulation and the chip disagree — and the simulation is the one that is wrong.** Your
> testbench passes, the hardware fails, and nothing in your verification flow can tell you.
>
> **This is the worst class of bug in the subject**, and the fix is one character: **always write
> `always @(*)`.**

---

## 5. Describing an FSM

**The idiom is three blocks, and it directly mirrors Week 9's procedure.**

```verilog
// 1. state register — sequential
always @(posedge clk or posedge rst)
  if (rst) state <= A;
  else     state <= next;

// 2. next-state logic — combinational
always @(*) begin
  next = state;                       // default: no latch
  case (state)
    A: next = x ? B : A;
    B: next = x ? B : C;
    C: next = x ? D : A;
    D: next = x ? B : C;
  endcase
end

// 3. output logic
assign y = (state == D) & x;          // Mealy
```

**Notice what you did *not* write: no state encoding, no K-maps, no next-state equations.**

> **The tool derives them.** Week 9's $D_1=Q_0\overline X+Q_1\overline{Q_0}X$ is what synthesis
> produces from that `case` statement — **and it will often choose one-hot instead**, because on an
> FPGA that is cheaper *(Week 5, Week 9)*.
>
> **You spent Wednesday of Week 9 deriving by hand what a tool now does in milliseconds.** That was
> not wasted: **you can read what it produced, and you know what to do when it produces something
> wrong.**

---

## 6. Simulation Is Not Synthesis

**Constructs that simulate and do not synthesise:** delays (`#5`), `$display`, `initial` blocks, `real`, most loops with non-constant bounds.

**Those belong in testbenches.** **In a design module, if you cannot say what gates a line becomes, do not write it.**

---

## 7. What To Take From This Lecture

1. **`always @(posedge clk)` makes storage** — the clock does, not `reg`.
2. **Pulse asynchronous resets.**
3. **`<=` sequential, `=` combinational.** Measured: blocking collapsed a 3-stage shift register into one stage.
4. **An `if` without an `else` in `always @(*)` builds a latch.** Assign a default.
5. **An incomplete sensitivity list makes simulation and silicon disagree.** Write `always @(*)`.
6. **The three-block FSM idiom** replaces Week 9's hand derivation — and the tool may re-encode your states.
7. **If you cannot say what gates a line becomes, it does not belong in a design module.**

---

*Next: Friday — Lab 10, simulate then compare with the hardware*
