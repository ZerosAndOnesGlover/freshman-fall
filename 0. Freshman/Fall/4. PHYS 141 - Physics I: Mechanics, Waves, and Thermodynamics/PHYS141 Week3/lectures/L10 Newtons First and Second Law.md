# PHYS 141 · Lecture 10
# Newton's First and Second Laws

> **Core Principle:** Force is not what keeps objects moving — it is what changes their motion. Newton's first law destroys the ancient Aristotelian notion that sustained force is needed to sustain motion. Newton's second law makes this quantitative: the net force on an object equals its mass times its acceleration. These two laws, together with the third, form the complete foundation of classical mechanics.

**Date:** Monday 7 September 2026 · 14:00–14:50 · Week 3

---


## Where This Fits

**Previously:** **L01–L09** described motion without asking what causes it. That was kinematics. Newton's laws begin dynamics.

---

## 1. The Failure of the Aristotelian Worldview

For nearly 2000 years after Aristotle, the dominant view of motion was: objects naturally come to rest, and a continuous force is required to keep them moving. This seems to agree with everyday experience — a pushed box slows down and stops.

Galileo identified the flaw: **friction**. The box stops not because the push stopped, but because friction opposes its motion. On a frictionless surface, a pushed object would keep moving forever. Galileo's thought experiment extended this: in a perfectly frictionless environment with no air resistance, a ball rolled along a horizontal surface would roll on indefinitely at constant velocity.

Newton formalized Galileo's insight into the First Law.

---

## 2. Newton's First Law — The Law of Inertia

> **Newton's First Law:** An object at rest remains at rest, and an object in motion continues in motion at constant velocity, unless acted upon by a net external force.

This is the definition of a **force**: something that changes the state of motion. More precisely, a force is an interaction between two objects that causes acceleration.

### 2.1 What the First Law Really Says

The first law has two parts that are easy to misread:

1. **An object at rest stays at rest** unless a net force acts. This is the intuitive part.
2. **An object in motion stays in motion at constant velocity** unless a net force acts. This is the part Aristotle got wrong — no force is needed to maintain constant velocity motion.

### 2.2 Inertial Reference Frames

The first law also defines what we mean by a valid reference frame for applying Newton's laws. An **inertial reference frame** is one in which the first law holds — a frame that is not itself accelerating. If you observe an object in an inertial frame and see it accelerating, you can conclude a net force acts on it. If you are in a non-inertial frame (an accelerating car, a rotating platform), fictitious forces appear that have no physical source.

> **Deep Why:** The existence of inertial frames is a deep empirical fact about the universe, not a logical necessity. The laws of physics take their simplest form in inertial frames. In General Relativity, gravity is reinterpreted as the curvature of spacetime, and inertial frames become freely falling frames — frames in which gravity is locally undetectable. The equivalence between "no forces" and "freely falling" is the Equivalence Principle (recall Lecture 6).

### 2.3 Inertia Defined

**Inertia** is the tendency of an object to resist changes in its state of motion. The more massive an object, the more inertia it has — the harder it is to change its velocity.

---

## 3. Mass vs. Weight — A Critical Distinction

These two words are used interchangeably in everyday language. In physics, they mean very different things:

| Property | Mass (m) | Weight (W) |
|----------|----------|------------|
| What it is | Amount of matter; measure of inertia | Gravitational force on the object |
| SI unit | kilogram (kg) | Newton (N) |
| Type | Scalar | Vector (downward) |
| Location dependence | Constant everywhere | Varies (depends on local g) |
| Formula | — | W = mg |
| On the Moon | Same as on Earth | ~1/6 of Earth value |

A 70 kg astronaut has mass 70 kg everywhere in the universe. On Earth, their weight is 70 × 9.81 = 686 N. On the Moon (g ≈ 1.62 m/s²), their weight is 70 × 1.62 = 113 N. In deep space far from any mass, their weight is essentially zero — but their mass is still 70 kg. Pushing them still requires the same force to produce the same acceleration.

> **Deep Why — The two kinds of mass:** The mass that appears in F = ma (inertial mass, resistance to acceleration) and the mass that appears in W = mg (gravitational mass, how strongly gravity pulls) are different physical concepts. They happen to be exactly equal — this equality is the Equivalence Principle. Experiments have verified this equality to one part in 10¹³. Einstein elevated it from an observed coincidence to a cornerstone of General Relativity.

---

## 4. Force — Quantified

A **force** is a vector quantity representing an interaction between two objects. Forces have:
- Magnitude (measured in Newtons: 1 N = 1 kg·m/s²)
- Direction
- A source (the object exerting the force)
- A target (the object experiencing the force)

### Types of Forces We Study This Semester

| Force | Symbol | Source | Direction |
|-------|--------|--------|-----------|
| Gravity (weight) | W or F_g | Earth (or other body) | Downward (toward center of Earth) |
| Normal force | N | Surface in contact | Perpendicular to surface, away from surface |
| Tension | T | String, rope, cable | Along string, away from object |
| Friction (static) | f_s | Surface in contact | Parallel to surface, opposing tendency to slip |
| Friction (kinetic) | f_k | Surface in contact | Parallel to surface, opposing motion |
| Applied force | F or F_app | External agent | As specified in problem |
| Spring force | F_sp | Spring | Along spring, opposing deformation |

### Force is a Vector — Forces Add as Vectors

The **net force** (resultant force) on an object is the vector sum of all forces acting on it:

$$\vec{F}_{net} = \sum_i \vec{F}_i = \vec{F}_1 + \vec{F}_2 + \vec{F}_3 + \cdots$$

---

## 5. Newton's Second Law

> **Newton's Second Law:** The net force on an object equals the product of the object's mass and its acceleration:
> $$\vec{F}_{net} = m\vec{a}$$

This is the central equation of classical mechanics. Everything else we do for the next several weeks is an application of this one equation.

### 5.1 Component Form

Since F⃗ = ma⃗ is a vector equation, it holds component by component:

$$\sum F_x = ma_x \qquad \sum F_y = ma_y \qquad \sum F_z = ma_z$$

This gives us up to three independent scalar equations — one per dimension. Most problems this semester are 2D (x and y only).

### 5.2 What Newton's Second Law Tells Us

- **Cause and effect:** Force is the cause; acceleration is the effect. Not velocity — acceleration.
- **Proportionality:** For a given mass, doubling the net force doubles the acceleration.
- **Inversely proportional to mass:** For a given force, doubling the mass halves the acceleration.
- **Instantaneous relationship:** F⃗_net at time t determines a⃗ at time t. If the force changes, the acceleration changes immediately.
- **Net force only:** Only the vector sum of all forces produces acceleration. Individual forces do not each produce their own independent accelerations — they combine first.

### 5.3 The Unit of Force

$$1\text{ N} = 1\text{ kg}\cdot\text{m/s}^2$$

This follows directly from F = ma: if a 1 kg object accelerates at 1 m/s², the force on it is 1 N.

### 5.4 Equilibrium

A special but important case: when ΣF⃗ = 0⃗, the object has zero acceleration. This means it is either at rest (static equilibrium) or moving at constant velocity (dynamic equilibrium). Both cases satisfy the same mathematical condition:

$$\sum F_x = 0 \qquad \sum F_y = 0$$

Equilibrium problems — bridges, hanging signs, balanced beams — are solved with these two equations.

---

## 6. Applying Newton's Second Law — The Method

Every Newton's law problem follows the same procedure:

1. **Identify the system** — which object are you applying the law to?
2. **Draw a free body diagram (FBD)** — every force on the object, drawn as arrows from the object's center
3. **Establish a coordinate system** — choose axes that simplify the algebra (often align one axis with acceleration)
4. **Write ΣF = ma component-wise** — one equation per axis
5. **Solve the algebra** — for the unknown force(s) or acceleration
6. **Check: units, sign, and magnitude**

---

## 7. Worked Examples

### Example 10.1 — Horizontal push

A 5.0 kg box on a frictionless floor is pushed by a horizontal force F = 20 N. Find its acceleration.

**FBD forces:** Applied force F = 20 N (right), weight W = mg = 49 N (down), normal force N (up). No friction (frictionless).

**x:** ΣFₓ = F = ma → 20 = 5.0 · a → **a = 4.0 m/s² (right)**

**y:** ΣFᵧ = N − mg = 0 (no vertical acceleration) → **N = mg = 49 N**

---

### Example 10.2 — Vertical acceleration

An elevator of mass 800 kg accelerates upward at 2.0 m/s². Find the tension in the cable.

**FBD forces on elevator:** Tension T (upward), weight mg = 7848 N (downward).

**y (up positive):** ΣFᵧ = T − mg = ma

$$T = m(g + a) = 800(9.81 + 2.0) = 800 \times 11.81 = \mathbf{9448 \text{ N}}$$

Note: T > mg because the elevator must support its weight AND provide the upward acceleration. If the elevator decelerates (a = −2.0 m/s²), then T = m(g − 2) = 6248 N < mg.

> **Elevator intuition:** You feel heavier when an elevator accelerates upward because the floor pushes up on you with more than your weight. You feel lighter when it decelerates while going up (or accelerates downward). In free fall (a = −g), T = 0 and you feel weightless — this is the physics of the ISS (Week 2, Problem 19).

---

### Example 10.3 — Two forces at angles

Two forces act on a 3.0 kg object: F⃗₁ = (10, 0) N and F⃗₂ = (−4, 8) N. Find the acceleration vector and its magnitude.

**Net force:** F⃗_net = (10−4, 0+8) = (6, 8) N

**Acceleration:** a⃗ = F⃗_net/m = (6/3, 8/3) = (2.0, 2.67) m/s²

**Magnitude:** |a⃗| = √(4 + 7.11) = √11.11 = **3.33 m/s²**

**Direction:** arctan(2.67/2.0) = **53.1° above +x axis**

---

## 8. Limits of Newton's Laws

Newton's second law (as written here) has two known breakdowns:

1. **High speeds (v approaching c):** At relativistic speeds, the relationship F = ma must be replaced by F = dp/dt where p = γmv (relativistic momentum). Mass appears to increase with velocity.

2. **Very small scales (atomic and subatomic):** Quantum mechanics governs the behavior of electrons, photons, and nuclei. Newton's laws are inapplicable at this scale.

For all everyday situations — objects from specks of dust to planets, at speeds below ~10% of c — Newton's laws are accurate to extraordinary precision.

---

## 9. Summary

| Concept | Statement | Key Implication |
|---------|-----------|----------------|
| Newton's 1st Law | No net force → no acceleration | No force needed to maintain constant velocity |
| Inertia | Resistance to change in motion | Mass quantifies inertia |
| Mass vs. weight | m is scalar (kg); W = mg is vector force (N) | Same mass everywhere; weight varies with g |
| Newton's 2nd Law | ΣF⃗ = ma⃗ | Apply component-wise; net force only |
| Equilibrium | ΣF⃗ = 0⃗ | At rest OR constant velocity; both satisfy ΣF = 0 |
| 1 Newton | 1 kg·m/s² | Force needed to give 1 kg an acceleration of 1 m/s² |

---


---

## CS Connection — F = ma as a State Update Rule

Newton's second law is the update rule at the heart of every simulation: forces determine acceleration, acceleration integrates to velocity, velocity to position. A physics engine is this loop plus collision detection. The first law — that constant velocity needs no cause — is why a correct simulation requires no code to keep an object moving, only to change its motion.

---

## Looking Ahead

**L11** adds the third law and the free body diagram — the systematic technique for applying F = ma to any situation.

## Conceptual Questions

1. A hockey puck slides across ice at constant velocity. What is the net force on it? Does any force act on it at all?

2. You push a wall with 50 N. The wall doesn't move. What is the net force on the wall? What is the wall's acceleration? Is Newton's second law violated?

3. A 1 kg object and a 10 kg object are both in free fall near Earth's surface. Both have acceleration g. Use F = ma to explain why the net force on the heavier object is 10 times larger, yet they accelerate identically.

4. Inside a sealed windowless spaceship, can the astronaut determine whether the ship is (a) at rest, (b) moving at constant velocity, or (c) accelerating? What principle does this illustrate?
