# ECE 110 · Digital Logic
## Week 10 · Lecture 1 (Wednesday)
### Describing Hardware, Not Programming It

---

**Reading:** Harris & Harris §4.1–4.3 | Mano & Ciletti §3.9
**Quiz 9** — at the start of today's lecture. **Covers Week 9.** Ungraded.

---

## 1. The Mental Model

> **Verilog describes a structure that exists all at once. It does not describe a sequence of steps.**

**In C, statements execute in order.** In Verilog, every `assign` and every `always` block **exists simultaneously and permanently** — they are wires and gates, not instructions.

| you write | you get |
|---|---|
| `assign y = a & b;` | an AND gate, forever |
| a `for` loop | **replicated hardware**, not iteration |
| `if` with no `else` | **a latch**, to hold the unassigned case |
| `x = x + 1;` | *(in a clocked block)* an incrementer and a register |

> **If you read Verilog as a program you will write code that simulates and does not synthesise, or
> worse, synthesises into something you did not intend.** Every trap in tomorrow's lecture is this
> one mistake wearing a different hat.

---

## 2. The Module

```verilog
module full_adder(
  output s, cout,
  input  a, b, cin
);
  wire s1, c1, c2;
  xor (s1, a, b);
  and (c1, a, b);
  xor (s, s1, cin);
  and (c2, s1, cin);
  or  (cout, c1, c2);
endmodule
```

**A module is a component with ports.** Instantiating one is placing a copy of that hardware — **not calling a function.** Ten instantiations are ten copies of the gates.

**Connect ports by name in anything non-trivial:**

```verilog
full_adder f0 (.s(sum[0]), .cout(c1), .a(A[0]), .b(B[0]), .cin(0));
```

**Positional connection is how you silently swap two wires** and spend an afternoon finding it.

---

## 3. `wire` vs `reg`

**The single most misleading pair of keywords in the language.**

| | use for | driven by |
|---|---|---|
| **`wire`** | a connection | `assign`, or a module output |
| **`reg`** | anything assigned inside `always` | procedural assignment |

> **`reg` does NOT mean "register".** It means "assigned procedurally". A `reg` in a combinational
> `always @(*)` block synthesises to **plain gates with no storage at all.**
>
> **Whether you get a flip-flop is decided by the clock, not by the keyword.** SystemVerilog renamed
> this to `logic` precisely because the name has confused every beginner for thirty years.

---

## 4. The Three Styles

### Structural — a netlist in text

**Gate primitives wired together.** This is what you have written since Week 2. **Use it when the schematic matters** — matching a hand design, or teaching.

### Dataflow — continuous assignment

```verilog
assign y = (a & b) | (~a & c);
assign {cout, sum} = a + b + cin;
```

**`assign` describes a permanent connection.** The right-hand side is re-evaluated whenever anything in it changes, because that is what a wire does.

**The `+` there is real: the tool builds an adder.** Which adder — ripple, carry-lookahead — is the tool's choice, guided by your timing constraints. **Weeks 3 and 6 are what it is choosing between.**

### Behavioural — procedural blocks

```verilog
always @(*) begin
  case (op)
    3'b000: y = a + b;
    3'b001: y = a - b;
    default: y = 4'b0000;
  endcase
end
```

**This is how you describe an ALU or an FSM without drawing it.** **The `default` is not optional** — tomorrow explains why.

---

## 5. Parameters and Buses

```verilog
module adder #(parameter N = 4) (
  output [N-1:0] sum, output cout,
  input  [N-1:0] a, b, input cin
);
```

**One description, any width.** `adder #(64) big(...)` gives a 64-bit adder from the same source.

**Bus notation:** `[N-1:0]` declares a vector; `a[3]` selects a bit; `a[3:2]` a slice; `{a, b}` concatenates; `{4{x}}` replicates.

**`{4{sub}}` is exactly Week 3's controlled inverter** — one control bit fanned out to four XORs.

---

## 6. The Testbench

**A testbench is *not* synthesised. It is a program**, and there the sequential reading is correct.

```verilog
module tb;
  reg [3:0] a, b; wire [3:0] sum; wire co;
  integer i, j, fails;
  adder #(4) dut(sum, co, a, b, 1'b0);
  initial begin
    fails = 0;
    for (i = 0; i < 16; i = i + 1)
      for (j = 0; j < 16; j = j + 1) begin
        a = i[3:0]; b = j[3:0]; #1;
        if ({co, sum} !== (i + j)) fails = fails + 1;
      end
    $display("%0d failures", fails);
  end
endmodule
```

**Three things this course has already taught you the hard way:**

- **Use `integer` loop counters.** A 1-bit `reg` wraps and the loop never ends *(Week 2)*.
- **Mask your comparisons to the right width.** A 4-bit result against an unbounded integer reports hundreds of false failures *(Week 3)*.
- **Use `!==`, not `!=`.** A comparison involving `x` returns `x`, which is falsy, so a broken design passes silently *(Week 1)*.

---

## 7. What To Take From This Lecture

1. **Verilog describes structure, not sequence.**
2. **A module instance is a copy of hardware, not a function call.** Connect ports by name.
3. **`reg` does not mean register.** The clock decides storage, not the keyword.
4. **Three styles — structural, dataflow, behavioural — all synthesise.**
5. **`assign` is a permanent connection; `+` builds a real adder** and the tool picks which kind.
6. **Parameters give one description at any width.**
7. **A testbench is a program**, and this course's three testbench traps are `integer`, masking, and `!==`.

---

*Next: Thursday — Sequential Verilog and the Classic Traps*
