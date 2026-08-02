# PHYS 141 — Week 6 Resources

## Required Textbook Reading

- **HRK:** Ch. 10 (Rotational Kinematics) — all sections; Ch. 11 (Rotational Dynamics) — §11.1–11.5
- **Serway:** Ch. 10 (Rotation of a Rigid Object About a Fixed Axis) — all sections

## Simulations

- **PhET "Torque"** — Apply forces at different points and angles on a rotating object; watch angular acceleration respond in real time. Directly visualizes the lever-arm concept from Lecture 20.
- **PhET "Rotational Motion"** or equivalent — compare angular and linear kinematics side by side.

## The Race Down the Incline — Try It Yourself

Before lab, if you have access to a solid ball (e.g., a marble or steel ball) and a ring/hoop-shaped object (e.g., a napkin ring or embroidery hoop) of any size, prop up a book or ramp and race them. The sphere will win every time, regardless of their relative sizes or masses — a striking, immediate demonstration of the β-dependence derived in Lecture 21. This is one of the most reliable and surprising demonstrations in all of introductory mechanics — even after seeing the derivation, most people find the outcome counter-intuitive on a gut level (surely the heavier one wins? surely the bigger one wins? — no, only the *shape* matters).

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 18–19: "Rotation in Two Dimensions" and "Center of Mass; Moment of Inertia" — Feynman's treatment includes an elegant derivation of several moments of inertia using symmetry arguments that avoid heavy integration.

## Common Pitfalls This Week

1. **Forgetting to convert rpm to rad/s.** Every rotational formula in this course (τ=Iα, KE=½Iω², v=rω) requires ω in rad/s. Always convert first: ω[rad/s] = rpm × π/30.

2. **Using the wrong moment of inertia formula.** Double-check whether the axis is through the center of mass or through an edge/end — these give very different I values (factor of 3 or 4 difference for a rod, for example). When in doubt, use the parallel axis theorem starting from the center-of-mass value.

3. **Confusing torque (N·m) with energy (J).** Although dimensionally identical (both are force × distance), torque and energy are fundamentally different physical quantities — torque is a vector related to rotational tendency; energy is a scalar related to capacity to do work. Never write torque values with units of "Joules."

4. **Applying constant-α kinematic equations when torque (and hence α) varies with angle.** As seen in Problem 14, a torque due to gravity on a swinging rod changes as the rod's angle changes — this is NOT constant angular acceleration, and the simple kinematic equations do not apply. Energy methods (introduced fully in the next problem set) are needed for such cases.

5. **Forgetting that static friction does zero work in rolling without slipping.** This is what allows pure energy conservation to be used for rolling-down-an-incline problems, even though friction is present and essential to the physics (it's what causes the rolling in the first place).
