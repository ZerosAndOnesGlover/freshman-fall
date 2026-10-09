# PHYS 141 · Week 4 Resources

## Required Textbook Reading

- **HRK:** Halliday, Resnick & Krane, *Physics*, 5th ed. — Ch. 11 (Work and Kinetic Energy); Ch. 12 (Potential Energy); Ch. 13 (Conservation of Energy)
- **Serway:** Serway & Jewett, *Physics for Scientists and Engineers*, 10th ed. — Ch. 7 (Energy of a System) §7.1–7.9; Ch. 8 (Conservation of Energy) §8.1–8.5

## Simulations

- **PhET "Energy Skate Park"** — The single best tool for building intuition about kinetic/potential energy conversion. Build custom tracks, add friction, and watch a real-time bar graph of KE, PE, and thermal energy. Verify the loop-the-loop minimum height result from Lecture 15 experimentally in the simulation before lab.
- **PhET "Masses and Springs"** — Explore elastic potential energy and the U(x) = ½kx² relationship directly.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 4: "Conservation of Energy" — Feynman's famous analogy of energy conservation to a mother counting toy blocks, regardless of where they're hidden. One of the most quoted passages in physics pedagogy.
- Richard Feynman's block-counting analogy captures a deep truth: energy conservation doesn't tell you the mechanism, only that the total is preserved — this is both its power and its limitation as an explanatory tool.

## The Deeper Story: Why Is Energy Conserved At All?

This week we showed that mechanical energy conservation follows algebraically from Newton's second law and the existence of a potential energy function. But *why* do conservative forces exist at all, and why is total energy (including heat, chemical, nuclear, etc.) always conserved even when mechanical energy is not?

The deepest answer comes from a result called **Noether's Theorem** (1918): every continuous symmetry of a physical system corresponds to a conserved quantity. Conservation of energy corresponds to symmetry under time translation — the laws of physics are the same today as they were yesterday and will be tomorrow. If the laws of physics changed from moment to moment, energy would not be conserved. This is well beyond the scope of this course, but it's worth knowing that conservation of energy is not an arbitrary rule — it reflects the fact that physics doesn't care what time it is.

## Common Pitfalls This Week

1. **Forgetting normal force and tension (in circular motion) do zero work.** These forces are always perpendicular to the relevant displacement — don't include them in your energy equation's W_nc term unless the geometry genuinely gives them a component along the motion.

2. **Sign errors with friction work.** Friction always removes mechanical energy from the system (assuming it opposes motion), so W_friction is always negative in the ΔE_mech = W_nc equation.

3. **Using v = √(2gh) when non-conservative forces are present.** This formula is only valid for the frictionless free-fall/incline case. With friction, you must include the −f_k·d term.

4. **Confusing the reference point for potential energy with a physical requirement.** You can choose U = 0 anywhere. The physics (ΔU, forces, motion) is unaffected by this choice — but you must be consistent throughout a single problem.

5. **Assuming path independence for non-conservative forces.** Never say "gravity or friction does the same work regardless of path" — this is true for gravity (conservative) but categorically false for friction (non-conservative, depends on total path length).
