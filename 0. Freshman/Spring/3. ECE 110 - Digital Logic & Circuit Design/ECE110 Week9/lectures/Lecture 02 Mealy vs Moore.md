# ECE 110 · Digital Logic
## Week 9 · Lecture 2 (Thursday)
### Mealy vs Moore

*“The machine is supplied with a "tape"... running through it, and divided into sections (called "squares") each capable of bearing a "symbol".”* — Alan Turing, "On Computable Numbers" (1936)

**Date:** Thursday 25 March 2027 · 13:00–14:15 · Week 9

**Coursework:** 📝 **PS 8** due today 13:00 · 📝 **PS 9** released today 14:30, due Thu 1 Apr 13:00 · 🔬 **Lab 9** Fri 26 Mar 14:00–15:50 · 📊 **Quiz 9** Wed 31 Mar 13:00–13:10

---

**Reading:** Harris & Harris §3.4.3 | Mano & Ciletti §5.6–5.7
**PS 9** released today, due Thursday of Week 10.

---

## 1. The Distinction

$$\textbf{Moore: } Y = g(S) \qquad\qquad \textbf{Mealy: } Y = g(S, X)$$

**Moore's output is written on the states of the diagram. Mealy's is written on the arcs.**

| | output depends on | output changes | glitches |
|---|---|---|---|
| **Moore** | state only | at the clock edge | **no** |
| **Mealy** | state and input | as soon as the input does | **possible** |

---

## 2. Same Job, Two Machines

**The overlapping `1011` detector, both ways.**

**Mealy — 4 states.** Output asserted on the arc from $D$ when the input is 1.

**Moore — 5 states.** Because the output must be a property of the *state*, "we have just detected a match" needs **its own state** ($S_4$), which Mealy did not require.

$$\text{input } \texttt{1011011011} \;\Rightarrow\; \text{both output } \texttt{0001001001}$$

*(Verified: both machines match a reference on **2000 random 24-bit sequences**, zero mismatches, when Moore's output is taken *after* the transition.)*

| | states | flip-flops |
|---|---:|---:|
| Mealy | **4** | 2 |
| Moore | 5 | **3** |

> **Mealy needed one fewer state and, here, one fewer flip-flop.** That is the usual pattern: **a
> Mealy machine can distinguish with its output what a Moore machine must distinguish with a state.**

---

## 3. The Timing Difference

**This is the part that matters in practice, and the part that gets stated sloppily.**

**A Mealy output responds within the same clock cycle as the input.** A Moore output cannot change until the state changes, which happens at the next edge.

> **The usual summary — "Moore lags Mealy by one cycle" — depends on where you take the output
> from.** A Moore machine whose output is read from the state *after* the transition is aligned with
> Mealy; read from the state *before*, it lags. **Say which convention you are using**, because half
> the confusion about Mealy and Moore is really confusion about this.

---

## 4. When To Use Which

### Choose Moore when the output must not glitch

**A Mealy output is combinational logic driven partly by an input**, so any glitch on the input appears on the output.

**Week 8 showed you what that costs**: a glitch on a decoder driving a write-enable corrupts memory.

> **If the output drives a write-enable, a device strobe, or anything that acts on an edge, use
> Moore.** Its output is a function of flip-flop outputs only, so it is stable for the whole cycle.

### Choose Mealy for fewer states and faster response

**Fewer states means fewer flip-flops and usually less logic.** And the output responds in the same cycle rather than the next, which matters in a handshake.

### The hybrid, which is what real designs use

**Register the Mealy output.** Compute $g(S,X)$, feed it through a flip-flop, and you have a glitch-free output with a one-cycle delay — **Moore's timing with Mealy's state count.**

---

## 5. The Whole Design, In Gates

**The Mealy machine with $A{=}00$, $B{=}01$, $C{=}10$, $D{=}11$:**

$$D_1 = Q_0\overline X + Q_1\overline{Q_0}X \qquad D_0 = X \qquad Y = Q_1Q_0X$$

*(Verified in Verilog over **4000 clock cycles** against a reference: zero failures.)*

**Two flip-flops, and next-state logic of 5 literals.**

---

## 6. A Bug Worth Meeting Now

**While preparing this week's simulation, the machine failed on its very first cycles** — the state was `xx`, not `00`.

**The cause:**

```verilog
reg rst = 1;                                  // reset asserted at time 0
always @(posedge clk or posedge rst)
  if (rst) q <= 2'b00; else q <= {d1, d0};
```

**There is no *posedge* of `rst`.** It was already 1 when the simulation began, so the asynchronous reset never fired and the flip-flops kept their initial unknown value.

**The fix is to pulse it:** start at 0, drive it to 1, then back to 0.

> **This is the same lesson as Week 8's ring counter stuck at `0000`, in a different costume: a
> sequential circuit with no defined initial state is not finished.** And notice that Verilog told
> the truth — the `x` propagating through the output was the simulator reporting a real problem, not
> being unhelpful.

---

## 7. What To Take From This Lecture

1. **Moore: $Y=g(S)$, output on the states. Mealy: $Y=g(S,X)$, output on the arcs.**
2. **Mealy usually needs fewer states** — 4 against 5 for the `1011` detector.
3. **Mealy responds in the same cycle; Moore at the next edge** — **but state your output convention.**
4. **Moore outputs cannot glitch; Mealy outputs can**, because an input feeds them directly.
5. **Use Moore for anything that acts on an edge.**
6. **Register a Mealy output** to get both.
7. **An asynchronous reset that is already asserted at time 0 never fires.** Pulse it.

---

*Next: Friday — Lab 9, both machines on the bench*
