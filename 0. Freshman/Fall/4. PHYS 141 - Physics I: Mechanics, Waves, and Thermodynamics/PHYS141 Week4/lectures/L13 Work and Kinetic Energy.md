# PHYS 141 · Lecture 13
# Work and Kinetic Energy

> **Core Principle:** Work is the mechanism by which force transfers energy to or from an object. The work-energy theorem — derivable directly from Newton's second law — states that the net work done on an object equals its change in kinetic energy. This single theorem lets us solve many problems without ever computing acceleration or time explicitly.

**Date:** Monday 14 September 2026 · 14:00–14:50 · Week 4

---


## Where This Fits

**Previously:** **L10–L12** solved problems by tracking forces instant by instant. Some problems are far easier if you track energy instead.

---

## 1. Why We Need Energy Methods

Newton's second law is powerful, but some problems are extremely difficult to solve using forces and kinematics directly — especially when force varies with position (e.g., a spring, or gravity over large distances) or when we don't care about the details of the motion, only the initial and final states.

**Energy methods** provide an alternative, often far simpler, route to the same physics. They are not new physics — they are Newton's laws, integrated over distance rather than applied instant-by-instant.

---

## 2. Work Done by a Constant Force

### 2.1 Definition

$$W = \vec{F}\cdot\vec{d} = Fd\cos\theta$$

where F is the magnitude of the force, d is the magnitude of displacement, and θ is the angle between the force vector and displacement vector.

**Units:** Newton-meter = Joule (J). $1\text{ J} = 1\text{ N}\cdot\text{m} = 1\text{ kg}\cdot\text{m}^2/\text{s}^2$

### 2.2 The Sign of Work

- θ < 90°: **W > 0** (positive work — force has a component along the motion; energy is added to the object)
- θ = 90°: **W = 0** (force does no work — entirely perpendicular to motion)
- θ > 90°: **W < 0** (negative work — force opposes motion; energy is removed from the object)

### 2.3 Key Examples of Zero Work

- **Normal force on a horizontal surface:** always perpendicular to horizontal motion → W_N = 0
- **Tension in circular motion (string swinging a ball):** always perpendicular to velocity → W_T = 0
- **Gravity on a horizontal walk:** perpendicular to horizontal displacement → W_gravity = 0
- **Any centripetal force:** always perpendicular to velocity in circular motion → does zero work

> **Deep Why:** This is why circular motion at constant speed requires a centripetal force but no "engine" to maintain it — the force does zero work, so it doesn't change the kinetic energy (speed), only the direction. This connects directly back to Week 2's insight that centripetal acceleration changes direction, not speed.

---

## 3. Work Done by a Variable Force — The Integral Definition

Most real forces are not constant (spring forces, gravity over large distances, air resistance). The general definition of work requires calculus:

$$W = \int_{x_i}^{x_f} F(x)\, dx \quad \text{(1D case)}$$

**Geometric interpretation:** Work equals the **area under the F(x) vs. x graph** between the initial and final positions. This directly parallels displacement being the area under a v(t) graph (Lecture 4) — both are applications of the same calculus idea.

For a constant force, this integral reduces to $W = F\Delta x$, consistent with the simple formula above.

> **Scoped preview — the definite integral.** MATH 141 reaches Riemann sums and the definite
> integral in **Week 8** and the Fundamental Theorem in **Week 9**. You need it here, in Week 4.
> Everything required was already given in **Lecture 4 §7.1**; this is the whole of it:
>
> $$\int_a^b t^{n}\,dt = \left[\frac{t^{\,n+1}}{n+1}\right]_a^b = \frac{b^{\,n+1}-a^{\,n+1}}{n+1} \qquad (n \neq -1)$$
>
> Antidifferentiate term by term, evaluate at the top limit, subtract the value at the bottom.
> For a spring, $F(x) = -kx$, so $W = \int_0^{d}(-kx)\,dx = -k\left[\tfrac{x^2}{2}\right]_0^{d} = -\tfrac{1}{2}kd^2$ —
> which is exactly the spring result quoted later in this lecture. You will not be assessed on the
> theory of integration in this course, only on using it.

### 3D General Definition

$$W = \int_{\vec{r}_i}^{\vec{r}_f} \vec{F}\cdot d\vec{r}$$

This is a **line integral** — for this course, we primarily deal with cases where the path can be parameterized simply, or where the force is conservative (Lecture 14), which makes the integral path-independent.

---

## 4. The Work-Energy Theorem — Full Derivation

This is one of the most important derivations in the course. We derive it directly from Newton's second law, using only calculus and algebra — no new physical assumption is introduced.

### Setup (1D, for clarity — the 3D case follows identically)

Start with Newton's second law:
$$F = ma = m\frac{dv}{dt}$$

We want to relate this to work, $W = \int F\,dx$. Substitute:

$$W = \int_{x_i}^{x_f} F\,dx = \int_{x_i}^{x_f} m\frac{dv}{dt}\,dx$$

**Key calculus trick — change of variable using the chain rule:**

$$\frac{dv}{dt} = \frac{dv}{dx}\cdot\frac{dx}{dt} = v\frac{dv}{dx}$$

> **Scoped preview — substitution.** This step is *integration by substitution*, which MATH 141
> formalises in **Week 10**, built on the chain rule it proves in **Week 4**. You are not expected
> to reproduce the general method here. What matters is the pattern: when the variable of
> integration changes from $x$ to $v$, **the limits change with it** — $x_i \to v_i$ and
> $x_f \to v_f$ — which is why the final integral runs over velocities rather than positions.
> Forgetting to change the limits is the single most common error when you meet this properly
> in Week 10.

Substituting:

$$W = \int_{x_i}^{x_f} m\, v\frac{dv}{dx}\,dx = \int_{v_i}^{v_f} mv\,dv$$

The dx cancels, and we've converted the integral over position into an integral over velocity. This is straightforward to evaluate:

$$W = m\int_{v_i}^{v_f} v\,dv = m\left[\frac{v^2}{2}\right]_{v_i}^{v_f} = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2$$

### The Result

$$\boxed{W_{net} = \Delta KE = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2}$$

where we define the **kinetic energy**:

$$\boxed{KE = \frac{1}{2}mv^2}$$

> **Deep Why:** The work-energy theorem is not a separate law of physics — it is Newton's second law rewritten in terms of position rather than time, via the calculus substitution dv/dt = v(dv/dx). This substitution is the single most important trick in this derivation. Whenever you see force as a function of position and want to find speed, this substitution is your tool.

### 4.1 The Meaning of "Net"

**W_net** means the work done by the **net force** — equivalently, the sum of the work done by each individual force:

$$W_{net} = W_1 + W_2 + W_3 + \cdots = \Delta KE$$

This is because work is defined via a dot product, and dot products are linear (distribute over vector sums): $(\vec F_1+\vec F_2)\cdot\vec d = \vec F_1\cdot\vec d + \vec F_2\cdot\vec d$.

---

## 5. Kinetic Energy — Properties

- **Always non-negative:** KE = ½mv² ≥ 0 for any real velocity
- **Scalar** (not a vector) — no direction, only magnitude
- **Depends on speed squared:** doubling speed quadruples kinetic energy
- **Frame-dependent:** kinetic energy depends on the reference frame in which velocity is measured (unlike, say, mass)

---

## 6. Worked Examples

### Example 13.1 — Work by constant force at an angle

A 15 kg box is pulled 8.0 m across a floor by a rope making 30° with the horizontal, with tension 60 N. Find the work done by the tension.

$$W = Fd\cos\theta = 60 \times 8.0 \times \cos30° = 480 \times 0.866 = \mathbf{415.7 \text{ J}}$$

---

### Example 13.2 — Work-energy theorem, direct application

A 2.0 kg object has initial speed 3.0 m/s. A net force does 40 J of work on it. Find the final speed.

$$W_{net} = \Delta KE = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2$$
$$40 = \frac{1}{2}(2.0)v_f^2 - \frac{1}{2}(2.0)(9.0)$$
$$40 = v_f^2 - 9.0 \implies v_f^2 = 49.0 \implies v_f = \mathbf{7.0 \text{ m/s}}$$

Notice: we found the final speed **without ever computing acceleration, time, or distance individually** — the work-energy theorem bypasses the details.

---

### Example 13.3 — Variable force: a spring

A spring exerts force F(x) = −kx (Hooke's Law, where x is displacement from equilibrium, k is the spring constant). Find the work done BY the spring as it is stretched from x = 0 to x = A (positive, stretching).

$$W_{spring} = \int_0^A (-kx)\,dx = -k\left[\frac{x^2}{2}\right]_0^A = -\frac{1}{2}kA^2$$

The work done **by** the spring is negative (the spring pulls back against the stretching direction). The work done **by the external agent** stretching the spring is $+\frac{1}{2}kA^2$ (positive — you must do positive work to stretch it). We will use this quantity extensively as elastic potential energy in Lecture 14.

---

### Example 13.4 — Work-energy theorem with friction

A 4.0 kg block slides 6.0 m across a floor with μ_k = 0.25, starting at 5.0 m/s. Find its final speed.

**Work done by friction:**
$$f_k = \mu_k mg = 0.25 \times 4.0 \times 9.81 = 9.81\text{ N}$$
$$W_{friction} = -f_k \times d = -9.81 \times 6.0 = -58.86 \text{ J (negative — opposes motion)}$$

**Apply work-energy theorem** (friction is the only horizontal force doing work; normal force and gravity do zero work on a horizontal surface):

$$W_{net} = \Delta KE$$
$$-58.86 = \frac{1}{2}(4.0)v_f^2 - \frac{1}{2}(4.0)(25)$$
$$-58.86 = 2v_f^2 - 50$$
$$v_f^2 = \frac{50-58.86}{2}$$

This gives a negative number — meaning the block stops before traveling the full 6.0 m! Let's verify: distance to stop is found by setting v_f = 0:
$$0 - 50 = -f_k \cdot d_{stop} \implies d_{stop} = \frac{50}{9.81} = 5.10 \text{ m}$$

Since 5.10 m < 6.0 m, **the block stops before reaching 6.0 m** — the problem as posed has no real answer for v_f at d=6.0 m because the block never gets there. This illustrates the importance of checking whether your answer makes physical sense.

---

## 7. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Work (constant force) | W = Fd cosθ | Scalar; sign depends on angle |
| Work (variable force) | W = ∫F dx | Area under F(x) graph |
| Kinetic energy | KE = ½mv² | Always ≥ 0; scalar |
| Work-energy theorem | W_net = ΔKE | Derived from F=ma via v dv/dx substitution |
| Zero-work forces | Perpendicular to displacement | Normal force (flat surface), tension (circular motion), any centripetal force |

---


---

## CS Connection — Work-Energy as Amortised Analysis

The work-energy theorem relates start and end states while ignoring the path between them — the same move as amortised analysis in CS 101, which bounds total cost across a sequence of operations without tracking each one. Both replace step-by-step accounting with a statement about accumulated totals, and both are worth reaching for when the intermediate detail is irrelevant.

---

## Looking Ahead

**L14** introduces potential energy, which lets us account for stored energy and makes conservation possible.

## Conceptual Questions

1. A satellite orbits Earth in a perfect circle. Does gravity do any work on it over one full orbit? Over a quarter orbit? Explain using the definition of work.

2. You lift a 5 kg box straight up at constant velocity, then set it back down at the same constant velocity. What is the total work done by you over the round trip? What is the total work done by gravity? Explain why these are not simply zero for trivial reasons.

3. A force does positive work on an object for the first half of its motion and equal-magnitude negative work over the second half. What can you conclude about the object's kinetic energy at the start vs. the end?

4. Using the substitution dv/dt = v(dv/dx), re-derive the work-energy theorem for a force that is NOT constant, i.e., F(x) is some arbitrary function. Confirm the derivation doesn't require F to be constant at any point.
