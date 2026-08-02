# PHYS 141 — Lecture 2
# Coordinate Systems

> **Core Principle:** A coordinate system is a labeling scheme for points in space — a human convention, not a physical truth. Physics must be independent of which coordinate system you choose. Choosing the *right* coordinate system for a problem's symmetry is one of the most powerful problem-solving techniques in physics.

---


## Where This Fits

**Previously:** **L01** established that every physical quantity needs a number and a unit. A quantity also needs a *place* and often a *direction*.

---

## 1. Why Coordinate Systems Matter

Physical phenomena don't care whether you describe them with Cartesian, polar, or spherical coordinates — the underlying physics (forces, energies, trajectories) is the same. But the *algebra* required to solve a problem can be dramatically simpler or harder depending on your choice.

**The deep principle:** Choose the coordinate system that matches the symmetry of the problem.
- A problem with circular symmetry (planetary orbits, circular motion) → polar coordinates
- A problem with cylindrical symmetry (wire's magnetic field, pipe flow) → cylindrical coordinates
- A problem with spherical symmetry (gravity from a point mass, electric field from a charge) → spherical coordinates
- A problem with no particular symmetry (projectile motion near Earth's surface) → Cartesian coordinates

---

## 2. Cartesian Coordinates (2D and 3D)

### 2.1 Definition

A point in 3D space is specified by three numbers (x, y, z), the perpendicular distances along three mutually orthogonal axes.

**Unit vectors:** x̂, ŷ, ẑ (sometimes written î, ĵ, k̂) — each has magnitude 1 and points along its respective axis. They satisfy:

$$\hat{x} \cdot \hat{y} = 0, \quad \hat{x} \cdot \hat{x} = 1, \quad \hat{x} \times \hat{y} = \hat{z} \text{ (right-hand rule)}$$

### 2.2 Position Vector

$$\vec{r} = x\hat{x} + y\hat{y} + z\hat{z}$$

### 2.3 Why Cartesian is the "Default"

Cartesian coordinates have the unique property that the unit vectors **do not change direction** as you move through space. This makes differentiation trivial — a major reason it's the default choice unless symmetry suggests otherwise.

---

## 3. Polar Coordinates (2D)

### 3.1 Definition

A point in the xy-plane is specified by (r, θ):
- **r** = distance from origin (r ≥ 0)
- **θ** = angle measured counterclockwise from the positive x-axis

### 3.2 Conversion Formulas

**Polar → Cartesian:**
$$x = r\cos\theta, \quad y = r\sin\theta$$

**Cartesian → Polar:**
$$r = \sqrt{x^2 + y^2}, \quad \theta = \arctan\left(\frac{y}{x}\right) \text{ (with quadrant correction)}$$

> **Critical subtlety:** The standard `arctan(y/x)` only returns values in (-π/2, π/2), which is wrong for points in the 2nd and 3rd quadrants. Always use the **atan2(y, x)** function in code, which correctly handles all four quadrants by examining the signs of both x and y.

### 3.3 Polar Unit Vectors

Unlike Cartesian unit vectors, the polar unit vectors r̂ and θ̂ **change direction** depending on where you are in space:

$$\hat{r} = \cos\theta\,\hat{x} + \sin\theta\,\hat{y}$$
$$\hat{\theta} = -\sin\theta\,\hat{x} + \cos\theta\,\hat{y}$$

r̂ always points radially outward from the origin; θ̂ always points in the direction of increasing θ (counterclockwise), perpendicular to r̂.

**This is the single most important fact about polar coordinates** — and it's why velocity and acceleration in polar coordinates have extra terms (centripetal and Coriolis-like terms) that don't appear in Cartesian coordinates. We will derive this explicitly when we study circular motion in later weeks.

### 3.4 When to Use Polar Coordinates

- Circular or near-circular motion (orbits, rotating objects)
- Central force problems (gravity, Coulomb force) where the force depends only on r
- Any problem where the natural boundary is a circle

---

## 4. Cylindrical Coordinates (3D)

Cylindrical coordinates extend polar coordinates by adding a z-axis:

$$(r, \theta, z)$$

- r, θ describe the projection onto the xy-plane (same as 2D polar)
- z is the height, identical to Cartesian z

**Conversion:**
$$x = r\cos\theta, \quad y = r\sin\theta, \quad z = z$$

**Use cases:** Problems with an axis of symmetry — current-carrying wires, rotating cylinders, pipes, solenoids.

---

## 5. Spherical Coordinates (3D)

### 5.1 Definition

A point in 3D space is specified by (r, θ, φ) [physics convention]:

- **r** = distance from origin (r ≥ 0)
- **θ** = polar angle, measured from the positive z-axis (0 ≤ θ ≤ π)
- **φ** = azimuthal angle, measured in the xy-plane from the positive x-axis (0 ≤ φ < 2π)

> **Convention warning:** Mathematics texts often swap θ and φ relative to physics texts! Always check which convention a source is using. We use the **physics convention**: θ is the polar (colatitude) angle from the z-axis, φ is the azimuthal angle in the xy-plane.

### 5.2 Conversion Formulas

**Spherical → Cartesian:**
$$x = r\sin\theta\cos\varphi, \quad y = r\sin\theta\sin\varphi, \quad z = r\cos\theta$$

**Cartesian → Spherical:**
$$r = \sqrt{x^2+y^2+z^2}, \quad \theta = \arccos\left(\frac{z}{r}\right), \quad \varphi = \text{atan2}(y, x)$$

### 5.3 Why Spherical Coordinates Matter

Any problem with a force or field that depends only on distance from a central point (gravity from a point mass, electric field from a point charge, the hydrogen atom's potential) has **spherical symmetry**. In spherical coordinates, such problems often reduce to a 1D problem in r alone — a dramatic simplification compared to solving a full 3D Cartesian problem.

---

## 6. Comparing the Three Systems

| System | Coordinates | Natural Symmetry | Position Vector Formula |
|--------|-------------|-------------------|--------------------------|
| Cartesian | (x, y, z) | None / rectangular | r⃗ = xx̂ + yŷ + zẑ |
| Cylindrical | (r, θ, z) | Axial (line) symmetry | r⃗ = r·r̂ + z·ẑ |
| Spherical | (r, θ, φ) | Point (central) symmetry | r⃗ = r·r̂ |

---

## 7. The Right-Hand Rule

When defining 3D coordinate systems and cross products, physicists use a universal convention: the **right-hand rule**.

**For axes:** Point your right hand's fingers along x̂, curl them toward ŷ; your thumb points along ẑ. This defines a **right-handed coordinate system** — the standard in physics.

**For cross products:** Point your fingers along the first vector, curl toward the second vector; your thumb gives the direction of the cross product.

**For rotational quantities (angular velocity, angular momentum, torque):** Curl your right-hand fingers in the direction of rotation; your thumb points along the angular velocity/momentum/torque vector.

> **Why this matters:** A left-handed convention would flip the sign of every cross product and angular quantity in physics — magnetic forces, torques, angular momentum. The convention itself is arbitrary, but once chosen, it must be applied **consistently** throughout a calculation, or signs will come out wrong.

---

## 8. Worked Examples

**Example 2.1:** A point has Cartesian coordinates (3, 4, 0). Find its polar/cylindrical coordinates.

$$r = \sqrt{3^2+4^2} = 5, \quad \theta = \text{atan2}(4,3) = 53.13°$$

So the point is at (r, θ) = (5, 53.13°) in the xy-plane (and z = 0 if cylindrical).

**Example 2.2:** A point has spherical coordinates (r, θ, φ) = (10, 60°, 30°). Find its Cartesian coordinates.

$$x = 10\sin(60°)\cos(30°) = 10(0.866)(0.866) = 7.50$$
$$y = 10\sin(60°)\sin(30°) = 10(0.866)(0.500) = 4.33$$
$$z = 10\cos(60°) = 10(0.5) = 5.00$$

So (x, y, z) = (7.50, 4.33, 5.00).

**Example 2.3:** Show that the polar unit vector r̂ has unit magnitude for all θ.

$$|\hat{r}| = \sqrt{\cos^2\theta + \sin^2\theta} = \sqrt{1} = 1 \quad \checkmark \text{ (Pythagorean identity)}$$

This confirms r̂ is always a unit vector, regardless of direction — only its *direction* changes with θ, not its magnitude.

---

## 9. Summary Table

| Concept | Key Point |
|---------|-----------|
| Cartesian | Fixed unit vectors; simplest algebra; default for no-symmetry problems |
| Polar (2D) | r, θ; unit vectors r̂, θ̂ rotate with position; best for circular symmetry |
| Cylindrical (3D) | Polar + z; best for axial symmetry (wires, pipes) |
| Spherical (3D) | r, θ, φ; best for point/central symmetry (gravity, point charges) |
| atan2(y,x) | Always use this instead of arctan(y/x) to avoid quadrant errors |
| Right-hand rule | Universal convention for axes, cross products, rotational vectors |

---


---

## CS Connection — Coordinate Systems and Data Representation

Choosing Cartesian vs. polar is choosing a data representation, and the choice has the same character as picking a data structure: nothing changes about the underlying reality, but the operations you care about get cheaper or more expensive. Rotation is trivial in polar and awkward in Cartesian; translation is the reverse. Computer graphics carries both and converts constantly. This is the same trade-off CS 101 makes when choosing a list versus a dict — the data is identical, the access costs are not.

---

## Looking Ahead

**L03** generalises this: once you have axes, a quantity with direction becomes a vector, and vectors have their own algebra.

## Conceptual Questions

1. Why do the polar unit vectors r̂ and θ̂ depend on position, while Cartesian unit vectors do not?

2. A planet orbits the Sun in an ellipse, not a perfect circle. Is polar coordinates still a good choice? Why?

3. If you used a left-handed coordinate system consistently throughout a calculation, would your final answer for a measurable, physical quantity (like the magnitude of a force) come out different? Why or why not?

4. Sketch (mentally or on paper) the set of points where θ = 45° in spherical coordinates, with r and φ free to vary. What 3D shape does this describe?
