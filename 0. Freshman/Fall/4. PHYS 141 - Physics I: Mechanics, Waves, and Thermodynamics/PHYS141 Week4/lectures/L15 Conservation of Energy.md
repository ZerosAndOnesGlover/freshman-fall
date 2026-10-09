# PHYS 141 · Lecture 15
# Conservation of Energy & Power

*“The quantity of force which can be brought into action in the whole of Nature is unchangeable, and can neither be increased nor diminished.”* — Hermann von Helmholtz, "On the Conservation of Force" (1862)

> **Core Principle:** Total mechanical energy — kinetic plus potential — is conserved when only conservative forces do work. When non-conservative forces (friction, drag) are present, mechanical energy is not conserved, but it is not lost either — it is transformed into other forms (primarily heat). The universal law of conservation of energy, of which mechanical energy conservation is a special case, is one of the deepest principles in all of physics.

**Date:** Friday 23 October 2026 · 14:00–14:50 · Week 4

**Reading:** Serway & Jewett §8.1–8.5 · HRK Ch. 13

**Coursework:** 📝 **PS 3** due today 17:00 · 📝 **PS 4** released today 15:00, due Fri 30 Oct 17:00 · 📊 **Quiz 4** Mon 26 Oct 14:00 · 🔬 **Lab 5** Thu 29 Oct 14:00–17:00

---


## Where This Fits

**Previously:** **L13** gave the work-energy theorem and **L14** gave potential energy. Combining them yields conservation of mechanical energy.

---

## 1. Conservation of Mechanical Energy — Derivation

Define **total mechanical energy**:

$$E_{mech} = KE + U$$

From the work-energy theorem (Lecture 13): $W_{net} = \Delta KE$

Split the net work into conservative and non-conservative contributions:

$$W_{net} = W_{cons} + W_{nc}$$

From Lecture 14: $W_{cons} = -\Delta U$

Substituting:

$$-\Delta U + W_{nc} = \Delta KE$$

$$W_{nc} = \Delta KE + \Delta U = \Delta(KE + U) = \Delta E_{mech}$$

$$\boxed{W_{nc} = \Delta E_{mech} = E_{mech,f} - E_{mech,i}}$$

### The Special Case: No Non-Conservative Forces

If $W_{nc} = 0$ (only conservative forces do work — e.g., no friction, no air resistance, no applied forces doing work):

$$\boxed{\Delta E_{mech} = 0 \implies KE_i + U_i = KE_f + U_f}$$

**Mechanical energy is conserved.** This is the single most powerful problem-solving tool in introductory mechanics — it lets you relate speeds and heights at two different points in a motion without any reference to the details of the path between them.

> **Deep Why:** Conservation of mechanical energy is not an independent law — it is a direct algebraic consequence of Newton's second law (via the work-energy theorem) plus the existence of a potential energy function for conservative forces. It is not "extra physics" beyond Newton's laws; it is Newton's laws viewed through a particularly convenient lens.

---

## 2. Problem-Solving with Energy Conservation

### The Method

1. Identify the initial and final states (positions and speeds, where `knowns/unknowns` are).
2. Identify all forces doing work. Classify each as conservative or non-conservative.
3. If only conservative forces act: use $KE_i + U_i = KE_f + U_f$.
4. If non-conservative forces act (friction, applied force): use $KE_i + U_i + W_{nc} = KE_f + U_f$, being careful with signs (friction does negative work as it removes mechanical energy).
5. Solve algebraically for the unknown.

### Why This Is Often Easier Than Newton's Laws

Energy conservation relates **states** (positions and speeds) without requiring you to know the acceleration profile, the time elapsed, or the detailed shape of a curved path (as long as you know the height change and can compute the work done by non-conservative forces). This is especially powerful for motion along curves, loops, and ramps, where applying F=ma directly would require calculus at every point.

---

## 3. Worked Examples — Pure Conservation

### Example 15.1 — Ball dropped from height

A 2.0 kg ball is dropped from rest at height h = 10 m. Find its speed just before hitting the ground, using energy conservation (compare to the kinematic method from Week 1).

**Setup:** Take ground as U = 0 reference. Initial state: KE_i = 0 (at rest), U_i = mgh = 2.0×9.81×10 = 196.2 J. Final state: U_f = 0 (at ground), KE_f = ½mv_f².

$$KE_i + U_i = KE_f + U_f$$
$$0 + 196.2 = \frac{1}{2}(2.0)v_f^2 + 0$$
$$v_f^2 = 196.2 \implies v_f = \mathbf{14.0 \text{ m/s}}$$

**Verify with kinematics:** $v_f = \sqrt{2gh} = \sqrt{2 \times 9.81 \times 10} = \sqrt{196.2} = 14.0$ m/s ✓ — identical result, as expected, since both methods derive from the same underlying physics.

---

### Example 15.2 — Pendulum swing

A pendulum of length L = 1.5 m is released from rest at an angle of 40° from vertical. Find its speed at the bottom of the swing.

**Setup:** Height drop from release point to bottom: $h = L - L\cos\theta = L(1-\cos\theta)$

$$h = 1.5(1-\cos40°) = 1.5(1-0.766) = 1.5 \times 0.234 = 0.351 \text{ m}$$

Energy conservation (tension does zero work — always perpendicular to motion):

$$mgh = \frac{1}{2}mv^2 \implies v = \sqrt{2gh} = \sqrt{2 \times 9.81 \times 0.351} = \sqrt{6.886} = \mathbf{2.62 \text{ m/s}}$$

Note: mass cancels entirely — pendulum speed at the bottom is independent of mass, just like free fall.

---

### Example 15.3 — Spring-launched projectile

A spring (k = 800 N/m) is compressed 0.15 m and used to launch a 0.50 kg ball horizontally. Find the launch speed.

$$U_{spring} = \frac{1}{2}kx^2 = \frac{1}{2}(800)(0.15)^2 = 9.0 \text{ J}$$

Energy conservation: all spring PE converts to KE (assume horizontal launch, no height change, no friction):

$$\frac{1}{2}kx^2 = \frac{1}{2}mv^2 \implies v = \sqrt{\frac{kx^2}{m}} = \sqrt{\frac{800 \times 0.0225}{0.50}} = \sqrt{36} = \mathbf{6.0 \text{ m/s}}$$

---

## 4. Worked Examples — With Non-Conservative Forces

### Example 15.4 — Sliding block with friction

A 3.0 kg block starts at rest at the top of a 25° incline of length 4.0 m. μ_k = 0.20. Find the speed at the bottom, using energy methods.

**Height drop:** $h = L\sin\theta = 4.0\sin25° = 1.69$ m

**Friction work (negative):** Normal force N = mg cos25° = 3.0×9.81×0.906 = 26.66 N. 
$$f_k = \mu_k N = 0.20 \times 26.66 = 5.33 \text{ N}$$
$$W_{friction} = -f_k \times L = -5.33 \times 4.0 = -21.3 \text{ J}$$

**Energy equation:**
$$KE_i + U_i + W_{nc} = KE_f + U_f$$
$$0 + mgh + (-21.3) = \frac{1}{2}mv_f^2 + 0$$
$$3.0 \times 9.81 \times 1.69 - 21.3 = \frac{1}{2}(3.0)v_f^2$$
$$49.7 - 21.3 = 1.5 v_f^2$$
$$v_f^2 = \frac{28.4}{1.5} = 18.9 \implies v_f = \mathbf{4.35 \text{ m/s}}$$

**Compare to frictionless case:** $v_{f,no friction} = \sqrt{2gh} = \sqrt{2 \times 9.81 \times 1.69} = \sqrt{33.16} = 5.76$ m/s. Friction reduces the final speed substantially — the "lost" mechanical energy (21.3 J) has been converted to heat at the block-incline interface.

---

### Example 15.5 — Loop-the-loop with energy methods

A ball starts at height h above the bottom of a frictionless circular loop of radius r. Find the minimum h such that the ball maintains contact at the top of the loop.

**Condition at top (from Week 3, Lecture 12):** minimum speed requires gravity alone to provide centripetal force: $mg = \frac{mv_{top}^2}{r} \implies v_{top}^2 = gr$

**Energy conservation from start (height h, at rest) to top of loop (height 2r, speed v_top):**

$$mgh = \frac{1}{2}mv_{top}^2 + mg(2r)$$
$$gh = \frac{1}{2}gr + 2gr = \frac{5}{2}gr$$
$$\boxed{h = \frac{5}{2}r}$$

This is a classic result: the ball must be released from a height of at least 2.5 times the loop radius (measuring from the bottom of the loop) to complete the loop — a beautiful combination of the circular motion analysis from Week 3 and the energy methods from this week.

---

## 5. Power

**Power** is the rate at which work is done, or equivalently the rate of energy transfer:

$$P = \frac{dW}{dt}$$

**Average power:**
$$\bar{P} = \frac{W}{\Delta t}$$

**SI unit:** Watt (W). $1\text{ W} = 1\text{ J/s}$

### 5.1 Power in Terms of Force and Velocity

Since $dW = \vec F \cdot d\vec r$:

$$P = \frac{dW}{dt} = \vec{F}\cdot\frac{d\vec{r}}{dt} = \vec{F}\cdot\vec{v}$$

$$\boxed{P = Fv\cos\theta}$$

This is an extremely useful formula: instantaneous power delivered by a force equals the dot product of force and velocity.

### 5.2 Common Power Units

- 1 horsepower (hp) = 746 W
- Typical human sustained power output: ~75–100 W
- Typical car engine: ~100,000–200,000 W (100–270 hp)

---

## 6. Worked Example — Power

### Example 15.6 — Car climbing a hill

A 1500 kg car climbs a 10° incline at constant speed 20 m/s. Ignoring friction and air resistance, find the power required.

At constant speed, the engine force must balance the component of gravity along the incline:

$$F_{engine} = mg\sin10° = 1500 \times 9.81 \times 0.1736 = 2554 \text{ N}$$

$$P = Fv = 2554 \times 20 = \mathbf{51,080 \text{ W} \approx 51.1 \text{ kW} \approx 68.5 \text{ hp}}$$

---

## 7. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Conservation of mechanical energy | KEᵢ+Uᵢ = KEf+Uf | Only when W_nc = 0 |
| General energy equation | KEᵢ+Uᵢ+W_nc = KEf+Uf | Friction/drag: W_nc < 0 |
| Power | P = dW/dt = Fv cosθ | Rate of energy transfer; Watts |
| Loop-the-loop minimum height | h = 5r/2 | Classic synthesis of circular motion + energy |

---


---

## CS Connection — Conservation Laws as Invariants

A conservation law is a loop invariant: a quantity that holds before and after every step, whatever happens in between. You use it exactly as CS 101 uses invariants — to reason about a final state without simulating the intermediate ones. Non-conservative forces are the equivalent of a step that breaks the invariant, and must be accounted for explicitly with a W_nc term.

---

## Looking Ahead

**L16** introduces a second conserved quantity — momentum — which survives in collisions where energy does not.

## Conceptual Questions

1. A skier goes down two different slopes of the same height but different shapes (one steep-then-flat, one gradually curving). Ignoring friction, do they reach the bottom with the same speed? Would your answer change with friction present?

2. A car engine delivers constant power P. As the car speeds up, does the engine force increase, decrease, or stay the same? (Hint: use P = Fv.)

3. Explain, using the energy equation with W_nc, why perpetual motion machines (that do net positive work forever with no external energy input) are impossible in a system with any friction at all.

4. In the loop-the-loop problem, why does the minimum starting height not depend on the mass of the ball? Trace through the derivation and identify exactly where mass cancels.
