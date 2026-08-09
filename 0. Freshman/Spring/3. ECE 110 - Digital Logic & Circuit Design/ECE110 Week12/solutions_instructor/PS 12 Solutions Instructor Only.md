# ECE 110 · Digital Logic
## Problem Set 12 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All sizing arithmetic verified.

---

## Part A (6 pts each)

**A1 (6).**

| | AND plane | OR plane |
|---|---|---|
| ROM | fixed (full decoder) | **programmable** |
| PLA | **programmable** | **programmable** |
| PAL | **programmable** | fixed |

**A2 (6).** $\text{PLA}=2np+pm$; $\text{PAL}=2np$; $\text{ROM}=2^n m$.

*(The $2n$ is because each product term can connect to a variable or its complement.)*

**A3 (6).** For $n{=}16$, $m{=}8$, $p{=}64$:

| PLA | PAL | ROM |
|---:|---:|---:|
| 2 560 | 2 048 | **524 288** |

$$\textbf{ROM : PAL} = 524288/2048 = \mathbf{256{:}1}$$

*(Verified.)*

**A4 (6).** **A ROM's AND plane is a full decoder — it generates all $2^n$ minterms whether the design uses them or not.** A PLA generates only the $p$ product terms requested, so its cost tracks the design's complexity rather than its input count.

**A5 (6).** **The PLA and PAL.**

**Fewer product terms is literally fewer rows in the AND plane.** A PAL with a fixed budget — commonly 8 product terms per output — **will not fit a function you did not minimise**, so minimisation becomes a fit/no-fit question rather than a cost question.

> **This is the only architecture in the course where Week 4's algorithm changes whether the design
> is possible**, rather than merely how big it is.

---

## Part B (6 pts each)

**B1 (6).** A $k$-input **LUT**, a **flip-flop**, and a **multiplexer** selecting registered or combinational output — plus programmable interconnect between cells and hard blocks (memory, multipliers, carry chains).

**B2 (6).** $2^6 = \boxed{64}$ bits; $2^{2^6} = \boxed{1.8\times10^{19}}$ functions.

**First met in Week 1** — the count of Boolean functions of $n$ variables, $2^{2^n}$.

**B3 (6).** **About 7 LUTs, 2 levels deep.** *(Verified: $\lceil32/6\rceil = 6$ at the first level, then 1 to combine.)*

**B4 (6).** $\boxed{\text{One 3-input LUT each.}}$ *(Verified.)*

**Implication: minimisation does not reduce cost on an FPGA**, because a LUT's size is set by its input count alone. **The tools optimise packing and routing instead.**

**B5 (6).** HDL → synthesis → technology mapping → placement → routing → bitstream.

**Steps 2–5 are NP-hard in general.** **Week 4 made the same point about Quine–McCluskey's covering step** — which is why synthesis tools do not guarantee a true minimum either.

---

## Part C (7 pts each)

**C1 (7).** **Because a carry chain built from generic LUTs and programmable routing is slow** — each carry crosses the interconnect, which is far slower than a dedicated wire.

**Week 3 showed why it matters:** the ripple adder's serial dependency makes the carry path the critical path, and an FPGA cannot fix that with cleverness in the fabric. **So the fabric contains a hardened special case.**

**C2 (7).** **Obviously right:** small volumes, prototypes, designs still changing, anything where a mask set's cost cannot be amortised, and where a bug found after fabrication would be catastrophic.

**Obviously wrong:** high volume, where the per-unit area and power penalty is multiplied by millions and the mask cost is amortised to nothing — **and anywhere the 10× speed penalty is unacceptable.**

**C3 (7).** **Check exhaustively; suspect the checker; name the cost.**

*Marking: 3 for the three habits, **4 for concrete personal examples.** Generic examples earn 2.*

**C4 (7).** Any three, each with **spent / bought / measured numbers.** Reference set:

| decision | spent | bought |
|---|---|---|
| carry-lookahead | 2× area | 10.8× speed (129 → 12 gate delays) |
| synchronous counter | toggle logic | no transients, log delay |
| DRAM | 4.5% refresh | 6× density |
| minimisation | design effort | 43 gates → 7 |
| LUT | silicon | free changes |
| BCD | 37% more bits | exact decimal |

*Marking: 7. **Numbers are required** — a trade named without a measurement earns 3.*

---

## Presentation (12 pts)

**Arithmetic shown, tables laid out, units stated.**

---

## Marking Summary

| Part | Points |
|---|---|
| A | 30 |
| B | 30 |
| C | 28 |
| Presentation | 12 |
| **Total** | **100** |

---

## The Four Errors To Expect

1. **A2/A3:** sizing a ROM with $p$ rather than $2^n$.
2. **B4:** answering that the 11-literal version needs more LUTs.
3. **C1:** naming the carry chain without connecting it to Week 3.
4. **C4:** naming trades with no measured numbers.

---

*ECE 110 · Week 12 · PS 12 Solutions · Instructor Only*
