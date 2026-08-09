# ECE 110 · Digital Logic
## Quiz 9 — With Answer Key
### Week 10 · Wednesday · **Covers Week 9**

---

**Time:** 10 minutes · **Closed book** · **UNGRADED**
**Covers Week 9:** FSM design, state assignment, Mealy and Moore.

---

## Questions

**Q1.** List the six steps of FSM design. Which requires judgement?

**Q2.** For an overlapping `1011` detector, what must the machine remember? **How many states?**

**Q3.** From the state meaning `101`, on input 1, **which state do you go to and why?**

**Q4.** Give the difference between Mealy and Moore in one sentence each. **Which needs more states for this detector?**

**Q5.** A 5-state machine is encoded in 3 bits. **What must you decide, and what goes wrong if you do not?**

---
---

# ANSWER KEY

---

**Q1.** Words → what to remember; state diagram; state table; state assignment; equations; circuit and verification. **Only step 1 requires judgement.**

**Q2.** **The longest matching prefix** — nothing, `1`, `10`, `101`. $\boxed{4 \text{ states}}$.

**Q3.** **To the state meaning `1`** — *not* the start state.

**The detected `1011` ends in a 1, and that 1 is itself the first bit of the next possible match.** Going to the start state discards information the machine already has and misses overlapping occurrences.

*(This is the most common FSM error on the problem set.)*

**Q4.** **Moore: the output depends only on the state. Mealy: it depends on the state and the current input.**

$$\textbf{Moore needs more — 5 against Mealy's 4.}$$

*(Verified.)* Because "a match just completed" must be its own state for Moore, where Mealy puts it on an arc.

**Q5.** $2^3-5=3$ **unused codes.** You must decide **what each does** — where it transitions to.

**If you do not**, a machine that reaches one through a glitch or a bad power-up **may never leave it: the design hangs.**

---

## Notes for the Instructor

- **Q3 is the diagnostic** and it is the error that separates working detectors from nearly-working ones.
- **Today's lecture changes the medium** — say plainly that from here the tool derives what they derived by hand, and that this is why they had to do it by hand first.

---

*ECE 110 · Quiz 9 · Week 10 · ungraded*
