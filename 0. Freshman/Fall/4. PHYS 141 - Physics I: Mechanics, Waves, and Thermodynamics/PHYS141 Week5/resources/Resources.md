# PHYS 141 · Week 5 Resources

## Required Textbook Reading

- **HRK:** Ch. 9 (Center of Mass and Linear Momentum) — all sections
- **Serway:** Ch. 9 (Linear Momentum and Collisions) — all sections

## Simulations

- **PhET "Collision Lab"** — Set up 1D and 2D collisions with adjustable masses, velocities, and elasticity. Turn on momentum and kinetic energy displays to watch conservation (or lack thereof) in real time. Essential for building intuition before lab.
- **PhET "Center of Mass"** (or equivalent simulation) — Visualize how the center of mass position responds to mass distribution changes.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 10: "Conservation of Momentum" — includes Feynman's discussion of why momentum conservation is arguably more fundamental than energy conservation in classical mechanics, since it follows directly and simply from Newton's Third Law.
- For the historically minded: momentum conservation was recognized (in a rudimentary form) by Descartes before Newton fully formalized the Third Law — an interesting case where a physical principle was correctly guessed before it was properly derived.

## The Rocket Equation (Enrichment — Beyond Course Scope, But Illuminating)

A rocket expels mass (exhaust) to gain momentum in the opposite direction — a continuous version of the "cannon recoil" problem (Problem 19 this week). Because the rocket's mass is *changing* as fuel burns, F=ma cannot be applied directly (recall Lecture 16: the momentum form of Newton's second law is the general one). The famous **Tsiolkovsky rocket equation**,

$$\Delta v = v_{exhaust}\ln\left(\frac{m_i}{m_f}\right)$$

is derived by applying momentum conservation to the rocket+expelled-mass system at each instant. This is a beautiful and practically vital extension of exactly the physics covered this week, and is worth looking up if you're curious how spacecraft trajectories are actually calculated.

## Common Pitfalls This Week

1. **Applying kinetic energy conservation in an inelastic collision.** Only momentum is guaranteed conserved in ALL collisions. Only use KE conservation if the problem explicitly states (or you can verify) the collision is elastic.

2. **Sign errors in 1D collision problems.** Always define a positive direction explicitly and assign correct signs to velocities moving in the opposite direction — this is the single most common source of error in this topic.

3. **Confusing "isolated system" with "no forces at all."** An isolated system has no *external* forces (or negligible external impulse compared to internal collision forces). Internal forces (the collision itself) are exactly what conserve momentum — they are not absent, they cancel in pairs.

4. **Forgetting the center of mass moves at constant velocity only when there's no external force** — not automatically in every system. If gravity acts (e.g., a thrown, exploding firework), the center of mass still follows a parabola (accelerating at g) — it's not "frozen," it just moves as if unaffected by the internal explosion.

5. **Using the elastic collision formulas when one object is NOT initially at rest.** The general formulas presented handle this case correctly (they include both v_{A,i} and v_{B,i}), but the "special case" simplifications (equal masses, heavy/light limits) assume the target starts at rest — don't misapply these shortcuts when both objects are moving initially.
