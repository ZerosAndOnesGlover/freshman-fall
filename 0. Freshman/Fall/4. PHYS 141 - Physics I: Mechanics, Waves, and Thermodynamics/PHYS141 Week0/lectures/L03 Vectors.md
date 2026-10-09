# PHYS 141 · Lecture 3
# Vectors: Algebra, Dot Product, Cross Product

*“Symmetrical equations are good in their place, but 'vector' is a useless survival, or offshoot from quaternions, and has never been of the slightest use to any creature.”* — Lord Kelvin, letter to G. F. FitzGerald (1896) — history did not agree with him

> **Core Principle:** A vector is a quantity with both magnitude and direction, obeying specific addition rules (the parallelogram rule). Scalars (mass, temperature, energy) have magnitude only. The distinction is not pedantic — it determines what operations are physically meaningful.

**Date:** Friday 25 September 2026 · 14:00–14:50 · Week 0

**Reading:** Serway & Jewett §3.2–3.4, §7.3 (scalar product), §11.1 (vector product)

**Coursework:** 📝 **PS 0** released today 15:00, due Fri 2 Oct 17:00 · 📊 **Quiz 0** Mon 28 Sep 14:00 · 🔬 **Lab 1** Thu 1 Oct 14:00–17:00

---


## Where This Fits

**Previously:** **L02** gave us axes to project onto. Vectors are quantities that need both a magnitude and a direction relative to those axes.

---

## 1. What Makes Something a Vector?

It is tempting to say "a vector is anything with magnitude and direction" — but this is incomplete. The rigorous definition: **a vector is a quantity that transforms in a specific way under rotation of the coordinate system** (it transforms "covariantly"). 

For this course, the operational definition suffices: a vector has a magnitude (always ≥ 0) and a direction, and vectors add according to the **parallelogram rule** (equivalently, tip-to-tail addition).

**Examples of vectors:** position, displacement, velocity, acceleration, force, momentum, electric field

**Examples of scalars:** mass, time, temperature, energy, electric charge, distance (note: distance is the *magnitude* of displacement, hence scalar)

---

## 2. Vector Notation

We write vectors with an arrow or boldface: $\vec{A}$ or **A**. The magnitude is written $|\vec{A}|$ or simply $A$.

### 2.1 Component Form

In Cartesian coordinates:
$$\vec{A} = A_x\hat{x} + A_y\hat{y} + A_z\hat{z}$$

The magnitude is found via the Pythagorean theorem in 3D:
$$|\vec{A}| = \sqrt{A_x^2 + A_y^2 + A_z^2}$$

### 2.2 Direction

A vector's direction can be specified by:
- An angle (in 2D, measured from a reference axis)
- A **unit vector** Â = A⃗/|A⃗| (a vector of magnitude 1 pointing in the same direction)

---

## 3. Vector Addition and Subtraction

### 3.1 Geometric (Tip-to-Tail) Method

Place the tail of the second vector at the tip of the first; the resultant vector goes from the tail of the first to the tip of the second.

### 3.2 Algebraic (Component) Method — Always Exact

$$\vec{A} + \vec{B} = (A_x+B_x)\hat{x} + (A_y+B_y)\hat{y} + (A_z+B_z)\hat{z}$$

**Why the component method is preferred:** Geometric addition requires careful scale drawings and is prone to measurement error. Component addition is exact, scalable to any number of vectors, and trivial to implement in code.

### 3.3 Vector Subtraction

$$\vec{A} - \vec{B} = \vec{A} + (-\vec{B})$$

where $-\vec{B}$ has the same magnitude as $\vec{B}$ but points in the opposite direction.

---

## 4. Scalar Multiplication

Multiplying a vector by a scalar c scales its magnitude by |c| and:
- Preserves direction if c > 0
- Reverses direction if c < 0

$$c\vec{A} = cA_x\hat{x} + cA_y\hat{y} + cA_z\hat{z}$$

---

## 5. The Dot Product (Scalar Product)

### 5.1 Definition

$$\vec{A} \cdot \vec{B} = |\vec{A}||\vec{B}|\cos\theta$$

where θ is the angle between the two vectors. In component form:

$$\vec{A} \cdot \vec{B} = A_xB_x + A_yB_y + A_zB_z$$

**These two formulas are equivalent** — proving this equivalence is a standard early derivation using the law of cosines.

### 5.2 Properties

- **Commutative:** A⃗·B⃗ = B⃗·A⃗
- **Distributive:** A⃗·(B⃗+C⃗) = A⃗·B⃗ + A⃗·C⃗
- **Result is a scalar** (a number, not a vector)
- A⃗·A⃗ = |A⃗|² (dotting a vector with itself gives magnitude squared)

### 5.3 Physical Meaning: Projection

The dot product measures **how much one vector points along the direction of another**. Geometrically, A⃗·B⃗ is the magnitude of A⃗ projected onto the direction of B⃗, times the magnitude of B⃗.

- If θ = 0° (parallel vectors): A⃗·B⃗ = |A⃗||B⃗| (maximum, positive)
- If θ = 90° (perpendicular vectors): A⃗·B⃗ = 0
- If θ = 180° (antiparallel vectors): A⃗·B⃗ = -|A⃗||B⃗| (maximum negative)

### 5.4 Why the Dot Product Matters in Physics

**Work** is the canonical example: W = F⃗·d⃗. Only the component of force **along the direction of motion** does work. A force perpendicular to motion (like the normal force on a flat floor, or gravity on a horizontal walk) does **zero** work — this is a direct and profound consequence of the dot product definition, not an arbitrary rule.

$$W = \vec{F}\cdot\vec{d} = |F||d|\cos\theta$$

We will derive the work-energy theorem from this definition in Week 4.

---

## 6. The Cross Product (Vector Product)

### 6.1 Definition

$$\vec{A} \times \vec{B} = |\vec{A}||\vec{B}|\sin\theta \, \hat{n}$$

where θ is the angle between the vectors, and n̂ is a unit vector perpendicular to both A⃗ and B⃗, with direction given by the **right-hand rule**.

### 6.2 Component Form (Determinant Method)

$$\vec{A} \times \vec{B} = \begin{vmatrix} \hat{x} & \hat{y} & \hat{z} \\ A_x & A_y & A_z \\ B_x & B_y & B_z \end{vmatrix}$$

Expanding:
$$\vec{A} \times \vec{B} = (A_yB_z - A_zB_y)\hat{x} - (A_xB_z - A_zB_x)\hat{y} + (A_xB_y - A_yB_x)\hat{z}$$

### 6.3 Properties

- **Anti-commutative:** A⃗×B⃗ = -(B⃗×A⃗) — order matters!
- **Distributive:** A⃗×(B⃗+C⃗) = A⃗×B⃗ + A⃗×C⃗
- **NOT associative:** A⃗×(B⃗×C⃗) ≠ (A⃗×B⃗)×C⃗ in general
- **Result is a vector** (specifically, a "pseudovector" — see note below)
- A⃗×A⃗ = 0 (a vector crossed with itself is always zero)

### 6.4 Physical Meaning: Perpendicularity and Rotation

The cross product measures **how perpendicular** two vectors are, and produces a new vector perpendicular to both — essential for describing rotational quantities.

- If θ = 0° or 180° (parallel/antiparallel): |A⃗×B⃗| = 0
- If θ = 90° (perpendicular): |A⃗×B⃗| = |A⃗||B⃗| (maximum)

### 6.5 Why the Cross Product Matters in Physics

**Torque:** τ⃗ = r⃗ × F⃗ — only the component of force perpendicular to the lever arm produces torque (rotational effect). A force pulling directly along the lever arm (toward or away from the pivot) produces zero torque.

**Angular momentum:** L⃗ = r⃗ × p⃗

**Magnetic force:** F⃗ = qv⃗ × B⃗ (a charged particle's force depends on its velocity component perpendicular to the magnetic field)

We will use the cross product extensively starting Week 6 (rotational dynamics).

> **Pseudovector note (enrichment):** Strictly, the cross product of two true vectors is a "pseudovector" (or axial vector) — it transforms differently under a mirror reflection than a true (polar) vector does. This subtlety becomes important in advanced E&M and is why physicists are careful about left- vs. right-handed coordinate conventions for cross-product-derived quantities (torque, angular momentum, magnetic field).

---

## 7. Comparing Dot and Cross Products

| Property | Dot Product (A⃗·B⃗) | Cross Product (A⃗×B⃗) |
|----------|---------------------|------------------------|
| Result type | Scalar | Vector |
| Formula | \|A\|\|B\|cosθ | \|A\|\|B\|sinθ n̂ |
| Max value | When parallel (θ=0°) | When perpendicular (θ=90°) |
| Zero when | Perpendicular (θ=90°) | Parallel/antiparallel (θ=0° or 180°) |
| Commutativity | Commutative | Anti-commutative |
| Physics example | Work: W = F⃗·d⃗ | Torque: τ⃗ = r⃗×F⃗ |
| Measures | Alignment / projection | Perpendicularity / rotation |

---

## 8. Vector Decomposition

Any vector can be decomposed into perpendicular components — this is the inverse of vector addition and is essential for solving 2D and 3D problems.

**2D Example:** A force of magnitude 50 N is applied at 30° above the horizontal.

$$F_x = F\cos\theta = 50\cos(30°) = 43.3 \text{ N}$$
$$F_y = F\sin\theta = 50\sin(30°) = 25.0 \text{ N}$$

This decomposition is the foundation of every 2D/3D mechanics problem you'll solve this semester — break every vector into perpendicular (usually x, y, z) components, solve each component **independently**, then recombine if needed.

> **Why this works:** Because perpendicular directions are physically independent. A force in the x-direction produces no acceleration in the y-direction (Newton's second law applies component-wise). This independence of perpendicular components is one of the most important simplifying principles in all of mechanics.

---

## 9. Worked Examples

**Example 3.1 (Vector addition):** A⃗ = (3, 4, 0), B⃗ = (-1, 2, 5). Find A⃗+B⃗ and its magnitude.

$$\vec{A}+\vec{B} = (3-1, 4+2, 0+5) = (2, 6, 5)$$
$$|\vec{A}+\vec{B}| = \sqrt{4+36+25} = \sqrt{65} \approx 8.06$$

**Example 3.2 (Dot product / angle between vectors):** Find the angle between A⃗ = (1, 0, 0) and B⃗ = (1, 1, 0).

$$\vec{A}\cdot\vec{B} = (1)(1)+(0)(1)+(0)(0) = 1$$
$$|\vec{A}| = 1, \quad |\vec{B}| = \sqrt{2}$$
$$\cos\theta = \frac{1}{(1)(\sqrt{2})} = \frac{1}{\sqrt{2}} \Rightarrow \theta = 45°$$

**Example 3.3 (Cross product / torque):** A force F⃗ = (0, 10, 0) N is applied at position r⃗ = (2, 0, 0) m from a pivot. Find the torque.

$$\vec{\tau} = \vec{r}\times\vec{F} = \begin{vmatrix}\hat{x}&\hat{y}&\hat{z}\\2&0&0\\0&10&0\end{vmatrix}$$
$$= \hat{x}(0\cdot0 - 0\cdot10) - \hat{y}(2\cdot0-0\cdot0) + \hat{z}(2\cdot10-0\cdot0) = (0,0,20) \text{ N·m}$$

The torque points in the +z direction (out of the page if x is right, y is up), with magnitude 20 N·m.

---

## 10. Summary Table

| Concept | Formula | Key Insight |
|---------|---------|-------------|
| Vector magnitude | \|A\| = √(Ax²+Ay²+Az²) | Pythagorean theorem in n dimensions |
| Vector addition | Component-wise sum | Always exact; preferred over geometric method |
| Dot product | A·B = \|A\|\|B\|cosθ = ΣAᵢBᵢ | Measures alignment; result is scalar |
| Cross product | \|A×B\| = \|A\|\|B\|sinθ | Measures perpendicularity; result is vector ⊥ to both |
| Decomposition | Resolve into perpendicular components | Perpendicular components are physically independent |

---


---

## CS Connection — Vectors as Arrays, and Why Components Matter

A vector in code is an array of components, and vector addition is elementwise addition — the same operation NumPy vectorises across millions of elements. The physically important step, resolving into components, is what makes the arithmetic elementwise and therefore parallelisable. This is why graphics and machine-learning hardware is built around vector operations: independence of components means the work maps directly onto SIMD lanes and GPU threads.

---

## Looking Ahead

**L04** applies vectors to motion: displacement is the first physical vector you will use in anger, and velocity is its rate of change.

## Conceptual Questions

1. Can the dot product of two non-zero vectors be negative? What does this mean physically (e.g., for work done by a force)?

2. If A⃗×B⃗ = 0⃗ but neither A⃗ nor B⃗ is the zero vector, what can you conclude about their relationship?

3. Why is "distance" a scalar but "displacement" a vector? Give an example where they have different numerical values.

4. Prove using components that A⃗·(B⃗×C⃗) = (A⃗×B⃗)·C⃗ (the scalar triple product is cyclic). [Hint: expand both sides explicitly.]
