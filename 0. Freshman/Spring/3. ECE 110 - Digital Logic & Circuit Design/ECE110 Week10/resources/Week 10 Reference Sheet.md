# ECE 110 · Digital Logic
## Week 10 · Reference Sheet
### Verilog

---

## The Model

> **Verilog describes a structure that exists all at once — not a sequence of steps.**

| you write | you get |
|---|---|
| `assign y = a & b;` | an AND gate, permanently |
| a `for` loop | **replicated hardware** |
| `if` with no `else` in `always @(*)` | **a latch** |
| `always @(posedge clk)` | **flip-flops** |

**A module instance is a copy of hardware, not a function call.** **Connect ports by name.**

---

## `wire` vs `reg`

| | for | driven by |
|---|---|---|
| `wire` | connections | `assign`, module outputs |
| `reg` | anything assigned in `always` | procedural assignment |

> **`reg` does NOT mean register.** A `reg` in `always @(*)` is plain gates. **The clock decides
> storage.** *(SystemVerilog's `logic` exists because of this confusion.)*

---

## Three Styles

```verilog
xor (s, a, b);                       // structural
assign y = (a & b) | (~a & c);       // dataflow
always @(*) case (op) ... endcase    // behavioural
```

**`assign {cout,sum} = a + b + cin;` builds a real adder** — the tool picks ripple or lookahead from your timing constraints *(Weeks 3, 6)*.

**Parameters:** `module adder #(parameter N=4) (...)` — one description, any width.
**Buses:** `a[3:2]` slice, `{a,b}` concatenate, `{4{x}}` replicate *(Week 3's controlled inverter)*.

---

## Trap 1 — Blocking vs Non-Blocking

$$\boxed{\texttt{<=} \text{ in sequential blocks} \qquad \texttt{=} \text{ in combinational blocks}}$$

**3-stage shift register, measured:**

| cycle | `<=` | `=` |
|:-:|:-:|:-:|
| 0 | `xx1` | `111` |
| 1 | `x10` | `000` |
| 2 | `100` | `000` |

**`<=` evaluates all right-hand sides first, then assigns together — which is what flip-flops do.**
**`=` takes effect immediately, so all three stages see the new value and collapse into one.**

---

## Trap 2 — The Inferred Latch

```verilog
always @(*) if (en) y = sel ? b : a;    // NO else
```

**Measured:** with `en=0`, `y` held its old value of 1 **even after `a` changed to 0.**

**You asked for a mux and got memory.** *(Week 7: an unintended latch is transparent and creates a timing path nobody analysed.)*

**Fix — either:**

```verilog
always @(*) begin
  y = 1'b0;                 // default first
  if (en) y = sel ? b : a;
end
```

**or assign every output in every branch** — an `else`, a `default` in every `case`.

**Synthesis tools warn about this. Read the warnings.**

---

## Trap 3 — The Sensitivity List

```verilog
always @(a) y = a & b;      // b missing
```

**Measured:** changing `b` from 0 to 1 left `y` at 0. The `always @(*)` version gave 1.

> **Simulation obeys the list; synthesis ignores it and builds a proper gate.** **The chip and the
> simulation disagree, and the simulation is the wrong one** — your testbench passes and the hardware
> fails. **The worst class of bug in the subject.**
>
> **Always write `always @(*)`.**

---

## The FSM Idiom

```verilog
always @(posedge clk or posedge rst)          // 1. state register
  if (rst) state <= A; else state <= next;

always @(*) begin                             // 2. next state
  next = state;                               //    default: no latch
  case (state)
    A: next = x ? B : A;
    B: next = x ? B : C;
    C: next = x ? D : A;
    D: next = x ? B : C;
  endcase
end

assign y = (state == D) & x;                  // 3. output (Mealy)
```

**No encoding, no K-maps, no equations.** The tool derives Week 9's $D_1=Q_0\overline X+Q_1\overline{Q_0}X$ — **and may choose one-hot instead**, because on an FPGA that is cheaper *(Weeks 5, 9)*.

> ⚠ **Pulse asynchronous resets.** `reg rst = 1;` gives no `posedge`; the state stays `x`.

---

## Testbench Traps This Course Has Hit

1. **`integer` loop counters** — a 1-bit `reg` wraps and the loop never ends *(Week 2)*.
2. **Mask comparisons to the right width** — a 4-bit result against an unbounded integer gave 240 false failures *(Week 3)*.
3. **`!==` not `!=`** — a comparison involving `x` returns `x`, which is falsy, so a broken design passes *(Week 1)*.

---

## Simulation ≠ Synthesis

**Simulation-only:** `#delays`, `$display`, `initial`, `real`, non-constant loop bounds.

> **In a design module, if you cannot say what gates a line becomes, do not write it.**

---

## Common Errors

1. **Reading Verilog as a program.**
2. **Thinking `reg` means register.**
3. **`=` in a clocked block.**
4. **`if` with no `else`, or a `case` with no `default`.**
5. **A hand-written sensitivity list.**
6. **Positional port connection**, silently swapping wires.
7. **An asynchronous reset that is never pulsed.**

---

*ECE 110 · Week 10 · Reference Sheet*
