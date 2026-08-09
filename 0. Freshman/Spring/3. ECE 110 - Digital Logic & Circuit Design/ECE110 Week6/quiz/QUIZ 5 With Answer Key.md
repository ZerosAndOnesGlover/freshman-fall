# ECE 110 · Digital Logic
## Quiz 5 — With Answer Key
### Week 6 · Wednesday · **Covers Week 5**

---

**Time:** 10 minutes · **Closed book** · **UNGRADED**
**Covers Week 5:** decoders, encoders, priority encoders, multiplexers, demultiplexers.

---

## Questions

**Q1.** How many AND gates does a 4:16 decoder need? **What does that growth mean for large decoders?**

**Q2.** A plain 4:2 encoder outputs $00$. **What are the two possible situations, and what fixes the ambiguity?**

**Q3.** Give the output equation of a 4:1 multiplexer.

**Q4.** State Shannon's expansion theorem, and say what size mux implements any 4-variable function.

**Q5.** $F=\sum m(1,3,5,6,7)$ minimises to two gates. Implemented as an 8:1 mux it is one package. **A colleague changes the spec to $\sum m(0,3,5,6,7)$. Which implementation is cheaper to change, and why?**

---
---

# ANSWER KEY

---

**Q1.** $2^4 = \boxed{16}$ AND gates *(plus 4 inverters)*.

**Growth is exponential**, so large decoders are built as **trees of smaller ones** — e.g. a 3:8 from two 2:4 plus an inverter, using the enables.

**Q2.** Either **$I_0$ is asserted**, or **no input is asserted at all**. *(Verified — both give $00$.)*

**The fix is a *valid* output**, as in a priority encoder: valid $=1$ means the code names a real line.

**Q3.** $Y=\overline{S_1}\,\overline{S_0}D_0+\overline{S_1}S_0D_1+S_1\overline{S_0}D_2+S_1S_0D_3$

*(The four product terms are a 2:4 decoder on the selects.)*

**Q4.** $F = x\cdot F|_{x=1}+\overline x\cdot F|_{x=0}$.

**An $\boxed{8:1}$ mux** — $2^{k-1}$ with $k=4$ — with three variables selecting and the fourth appearing as $0$, $1$, $D$ or $\overline D$ on the data inputs.

**Q5.** **The mux, decisively.**

**Mux:** change two constants ($D_0$ to 1, $D_1$ to 0). **Same package, same wiring.**

**Gates:** the minimal form changes from $C+AB$ **(3 literals)** to $AB+AC+BC+\overline A\,\overline B\,\overline C$ **(11 literals)** — *(verified)* — so you redo the map and rebuild, and **the result is nearly four times bigger.**

> **A lookup table's cost does not depend on the function inside it.** That is why FPGAs do not
> minimise.

---

## Notes for the Instructor

- **Q5 is the one that matters** and it previews nothing — it is the week's conclusion, and worth two minutes if the room is split.
- **Q2 catches students who learned the priority encoder's behaviour without the reason for the valid bit.**

---

*ECE 110 · Quiz 5 · Week 6 · ungraded*
