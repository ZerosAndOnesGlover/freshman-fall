# PHYS 141 · Week 2 Resources

## Required Textbook Reading

- **HRK:** Ch. 4 — Motion in Two and Three Dimensions (all sections)
- **Serway:** Ch. 4 — Motion in Two Dimensions (all sections)

## Simulations

- **PhET "Projectile Motion"** — Adjust launch speed, angle, mass, and air resistance. Watch the parabola change. Set air resistance to zero and verify the 45° maximum range prediction. Then add air resistance and observe how the optimal angle shifts below 45°.
- **PhET "Ladybug Revolution"** — Visualize angular position, velocity, and acceleration in circular motion. Watch how centripetal acceleration always points inward even as direction changes.

## Deeper Reading

- Newton, *Principia Mathematica* (1687), Book I, Proposition 1: the geometric proof that equal areas are swept in equal times — the root of all orbital mechanics. Even a brief reading of the original is historically striking.
- Feynman, *Feynman Lectures Vol. 1*, Ch. 9: "Newton's Laws of Dynamics" — sets up the physics we do next week, but also contains Feynman's elegant derivation of centripetal acceleration.

## Common Pitfalls This Week

1. **Using the range formula when heights differ.** R = v₀²sin2θ/g applies only when the projectile lands at the same height it was launched from. When heights differ, go back to x(t) and y(t) with the actual landing condition.

2. **Forgetting that time is shared between x and y.** The one number that links horizontal and vertical motion is t. Find it in one direction; use it in the other.

3. **Confusing centripetal acceleration direction.** It always points toward the center — radially inward. It is never tangential. At the top of a loop it points downward. At the right side of a circle it points left.

4. **Mixing degrees and radians.** Angular velocity ω must be in rad/s in all formulas (v = rω, a_c = ω²r). Convert RPM to rad/s before computing anything.

5. **Applying range formula to non-45° complement pairs.** Double-check with sin2θ: sin(2×30°) = sin60° = sin(2×60°) = sin120° ✓. This always works — the identity sin(180°−x) = sinx is the reason.
