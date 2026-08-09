# ECE 110 · Digital Logic
## Quiz 8 — With Answer Key
### Week 9 · Wednesday · **Covers Week 8**

---

**Time:** 10 minutes · **Closed book** · **UNGRADED**
**Covers Week 8:** registers, shift registers, ripple and synchronous counters.

---

## Questions

**Q1.** How many gates does an $N$-bit ripple counter need?

**Q2.** A 3-bit ripple counter goes from `011` to `100`. **List every state its outputs actually take**, and say why that matters.

**Q3.** Give $T_0$ through $T_3$ for a 4-bit synchronous counter, and the rule in words.

**Q4.** Give the settling time of an $N$-bit ripple counter and of a synchronous one. **Which earlier circuit does the ripple version resemble?**

**Q5.** Why must a load enable gate the **data** and not the **clock**?

---
---

# ANSWER KEY

---

**Q1.** $\boxed{\text{Zero}}$ — $N$ flip-flops with $\overline Q$ tied to $D$, each clocked by the previous stage.

**Q2.** $\texttt{011}\to\texttt{010}\to\texttt{000}\to\texttt{100}$ — it passes through **2** and **0**. *(Verified.)*

**Why it matters:** a decoder watching the counter **decodes those states**, so an output meant to fire only at 0 fires on every $2^k-1\to2^k$ transition. **If it drives a write-enable, that is a spurious memory write.**

**Q3.** $T_0=1$, $T_1=Q_0$, $T_2=Q_0Q_1$, $T_3=Q_0Q_1Q_2$.

**In words: bit $k$ toggles when every bit below it is 1** — which is what carrying means.

**Q4.** Ripple: $N\cdot t_{cq}$, **linear**. Synchronous: $t_{cq}$ + an AND tree + $t_{su}$, **logarithmic**.

**The ripple counter resembles Week 3's ripple-carry adder** — the same serial dependency chain.

**Q5.** **Gating the clock creates a second clock** with its own skew, so this register samples at a different instant from the rest of the design — and **any glitch on LOAD becomes a spurious clock edge**, which a flip-flop cannot distinguish from a real one.

---

## Notes for the Instructor

- **Q2 is the diagnostic**, and it should be easy after the scope photographs. If it is not, the Lab 8 debrief did not land.
- **Today begins FSMs**, where the first design rule is "one clock for everything" — for exactly the reason in Q2.

---

*ECE 110 · Quiz 8 · Week 9 · ungraded*
