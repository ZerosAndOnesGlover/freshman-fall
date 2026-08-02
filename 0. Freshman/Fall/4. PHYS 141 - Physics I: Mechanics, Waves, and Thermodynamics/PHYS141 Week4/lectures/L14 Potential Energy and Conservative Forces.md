# PHYS 141 · Lecture 14
# Potential Energy & Conservative Forces

> **Core Principle:** Some forces allow energy to be perfectly recovered — stored as "potential" energy and later converted back into kinetic energy without loss. These are conservative forces. Others (friction, air resistance) irreversibly convert mechanical energy into heat. The distinction between these two categories is not a labeling convenience — it reflects a deep property of the force itself: path-independence of work.

---


## Where This Fits

**Previously:** **L13** defined work and the work-energy theorem. For *conservative* forces the work done depends only on endpoints, which lets us define a stored energy.

---

## 1. Conservative Forces — The Defining Property

> **A force is conservative if the work it does on an object moving between two points is independent of the path taken.**

Equivalently: **the work done by a conservative force around any closed path is zero.**

### 1.1 Examples of Conservative Forces

- **Gravity** (near Earth's surface, and the general inverse-square law)
- **Spring force** (Hooke's Law)
- **Electrostatic force** (Coulomb's Law) — covered in later courses

### 1.2 Examples of Non-Conservative Forces

- **Friction** (kinetic and static during sliding)
- **Air resistance / drag**
- **Applied forces from motors, muscles** (in general — these can do positive or negative work depending on the specific setup, and typically depend on the path/process)

### 1.3 Why the Distinction Matters

For a conservative force, we can define a **potential energy function** U(x) associated with it, such that:

$$W_{conservative} = -\Delta U = U_i - U_f$$

This is only possible because the work doesn't depend on the path — only on the start and end points. For non-conservative forces, no such potential energy function exists, because the work done depends on the specific path (e.g., a longer sliding path means more friction work, even between the same two endpoints).

> **Deep Why — path independence and closed loops:** If work around any closed loop is zero for a conservative force, then the work from point A to point B must be the same regardless of path — otherwise you could choose a path A→B that does more work than B→A (reversed), and the round trip A→B→A would have nonzero net work, violating the closed-loop condition. This equivalence (path-independence ⟺ zero work on closed loops) is a standard and important argument you should be able to reconstruct.

---

## 2. Gravitational Potential Energy

### 2.1 Derivation Near Earth's Surface

Consider an object moving from height y_i to height y_f under gravity alone (force F⃗ = −mgŷ, constant near Earth's surface).

$$W_{gravity} = \int_{y_i}^{y_f} (-mg)\,dy = -mg(y_f - y_i) = -mg\Delta y$$

Define gravitational potential energy:

$$\boxed{U_{grav} = mgy}$$

Then:
$$W_{gravity} = -(U_f - U_i) = -\Delta U_{grav}$$

confirming the general relationship $W_{cons} = -\Delta U$.

### 2.2 The Arbitrary Reference Point

Notice that U_grav = mgy depends on where you set y = 0. This is not a flaw — **only differences in potential energy are physically meaningful**, never the absolute value. You are always free to choose the reference point (y = 0) wherever is most convenient for a given problem (e.g., the ground, a table top, the lowest point of a swing).

---

## 3. Elastic (Spring) Potential Energy

From Lecture 13, Example 13.3, the work done by a spring stretched from 0 to x is:

$$W_{spring} = -\frac{1}{2}kx^2$$

Define elastic potential energy:

$$\boxed{U_{spring} = \frac{1}{2}kx^2}$$

where x is the displacement from the spring's natural (unstretched) length. This applies to both stretching (x > 0) and compression (x < 0) — since x² is always positive, U_spring is always ≥ 0, with minimum (zero) at the natural length.

---

## 4. General Relationship: Force from Potential Energy

Since $W = \int F\,dx = -\Delta U$, differentiating gives:

$$F(x) = -\frac{dU}{dx}$$

**This is one of the most useful relationships in all of physics.** Given any potential energy function, you can find the force by taking the negative derivative — the force always points in the direction that decreases potential energy (toward lower U).

### Verification

- $U_{grav} = mgy \implies F = -\frac{dU}{dy} = -mg$ (downward, as expected) ✓
- $U_{spring} = \frac{1}{2}kx^2 \implies F = -\frac{dU}{dx} = -kx$ (Hooke's Law, restoring force toward equilibrium) ✓

> **Deep Why:** This relationship generalizes to 3D as $\vec F = -\nabla U$ (the negative gradient), which you'll see in later physics courses. The physical picture: potential energy is like a landscape of hills and valleys; objects experience a force that pushes them "downhill" — toward lower potential energy — with the steepness of the hill determining the force's magnitude.

---

## 5. Potential Energy Diagrams

A graph of U(x) vs. x is one of the most information-dense tools in mechanics. From it, you can read off:

| Feature of U(x) graph | Physical meaning |
|-----------------------|-------------------|
| Slope of U(x) | −F(x) (force is negative slope) |
| U(x) minimum | Equilibrium point (F = 0); typically stable |
| U(x) maximum | Equilibrium point (F = 0); typically unstable |
| Region where U(x) < E_total | Allowed region (object can be there; has KE = E−U > 0) |
| Region where U(x) > E_total | Forbidden region (would require negative KE — impossible) |
| U(x) = E_total | Turning point (KE = 0; object momentarily at rest here) |

### Example: The Spring Potential Well

U_spring(x) = ½kx² is a parabola with a minimum at x = 0. An object with total energy E oscillates between turning points at x = ±√(2E/k) — it cannot go beyond these points because that would require negative kinetic energy. This is the mechanical energy picture of simple harmonic motion (formalized in Week 8).

---

## 6. Worked Examples

### Example 14.1 — Gravitational PE reference point

A 2.0 kg ball is at height 5.0 m above the ground, which is itself 3.0 m above a basement floor.

**(a)** Taking the ground as the reference (y=0): U = mgy = 2.0×9.81×5.0 = **98.1 J**

**(b)** Taking the basement floor as the reference: the ball is at height 5.0+3.0 = 8.0 m. U = 2.0×9.81×8.0 = **156.96 J**

**(c)** The difference in potential energy between the ball's position and the ground is the same in both cases: 156.96 − (2.0×9.81×3.0) = 156.96−58.86 = 98.1 J ✓ — matches part (a). This confirms only differences matter physically.

---

### Example 14.2 — Force from potential energy

A particle has potential energy U(x) = 3x² − 12x + 7 (Joules, x in meters). Find the force as a function of x, and find the equilibrium position(s).

$$F(x) = -\frac{dU}{dx} = -(6x - 12) = -6x + 12$$

**Equilibrium:** F(x) = 0 → x = 2 m.

Check stability: $\frac{d^2U}{dx^2} = 6 > 0$ → U has a minimum at x=2 → **stable equilibrium**.

---

### Example 14.3 — Verifying path independence for gravity

A 3.0 kg object moves from point A (0, 0) to point B (4, 3) meters under gravity alone (in the −y direction), via two different paths: (i) straight line from A to B; (ii) first horizontal from (0,0) to (4,0), then vertical from (4,0) to (4,3).

**Path (i):** Displacement (4,3). Work by gravity = F⃗·d⃗ = (0,−mg)·(4,3) = −mg(3) = −3.0×9.81×3 = **−88.3 J**

**Path (ii):** Segment 1 (0,0)→(4,0): displacement (4,0), gravity does zero work (perpendicular). Segment 2 (4,0)→(4,3): displacement (0,3), work = −mg×3 = **−88.3 J**. Total = 0 + (−88.3) = **−88.3 J**

Both paths give the same work ✓ — confirming gravity is conservative, independent of path, depending only on the change in height.

---

## 7. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Conservative force | W independent of path | Zero work around closed loops |
| Gravitational PE | U = mgy | Reference point arbitrary; only ΔU matters |
| Elastic PE | U = ½kx² | x = displacement from natural length |
| Force from PE | F = −dU/dx | Force points toward decreasing U |
| Stable equilibrium | U minimum (d²U/dx² > 0) | Small displacements restore position |
| Unstable equilibrium | U maximum (d²U/dx² < 0) | Small displacements grow |

---


---

## CS Connection — Path Independence and Memoisation

A conservative force is one whose work is path-independent — so a single number attached to each position (the potential) captures everything. That is a lookup table replacing a computation, which is exactly memoisation. Non-conservative forces like friction are path-dependent, so no such table exists: you must know the route taken, not just the destination.

---

## Looking Ahead

**L15** combines kinetic and potential energy into the conservation law, the most useful single tool in mechanics.

## Conceptual Questions

1. Why can't we define a potential energy function for friction? Use the path-independence criterion to justify your answer with a concrete example (e.g., two different paths of different lengths between the same two points).

2. A ball is at the bottom of a symmetric potential energy well U(x) = x² (in some units). Sketch the force F(x) as a function of x. What is the direction of the force just to the left of x=0? Just to the right?

3. If you double the spring constant k, how does the elastic potential energy at a fixed displacement x change? How does the force at that displacement change?

4. Explain why "height" in U = mgy must be measured relative to some reference, but "kinetic energy" ½mv² still requires an implicit reference frame for velocity. Are these two "arbitrariness" issues fundamentally the same, or different? (This is a subtle conceptual question — think carefully.)
