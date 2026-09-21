# PHYS 141 · Lecture 16
# Momentum & Impulse

> **Core Principle:** Momentum is a measure of "quantity of motion" — mass in motion. The impulse-momentum theorem, derived directly from Newton's second law, tells us that a force applied over time changes momentum by exactly the integral of that force. This is the time-integrated counterpart to the work-energy theorem's position-integrated relationship.

**Date:** Monday 26 October 2026 · 14:00–14:50 · Week 5

---


## Where This Fits

**Previously:** **L15** established energy conservation. Momentum is the other great conserved quantity, and it behaves differently: it is a vector, and it survives collisions that destroy kinetic energy.

---

## 1. Linear Momentum — Definition

$$\vec{p} = m\vec{v}$$

Momentum is a **vector** quantity, pointing in the same direction as velocity, with magnitude equal to mass times speed.

**SI unit:** kg·m/s (no special name, unlike the Joule or Newton)

### Why Introduce Yet Another Quantity?

We already have velocity, force, and energy. Momentum earns its place because of a special property: **in an isolated system, total momentum is exactly conserved — always, in every kind of interaction**, including cases (like inelastic collisions) where kinetic energy is NOT conserved. This makes momentum a uniquely powerful tool for analyzing collisions, explosions, and interactions where we don't know the details of the forces involved.

---

## 2. Newton's Second Law in Terms of Momentum

Newton originally stated his second law not as F = ma, but as:

$$\vec{F}_{net} = \frac{d\vec{p}}{dt}$$

For a **constant mass** object, this reduces to the familiar form:

$$\vec{F}_{net} = \frac{d(m\vec{v})}{dt} = m\frac{d\vec{v}}{dt} = m\vec{a}$$

But the momentum form is **more general** — it also correctly describes systems where mass changes (like a rocket burning fuel, covered in enrichment material), which F=ma cannot handle without modification.

---

## 3. Impulse — Definition

**Impulse** is the integral of force over time:

$$\vec{J} = \int_{t_i}^{t_f} \vec{F}\,dt$$

For a **constant force**:
$$\vec{J} = \vec{F}\Delta t$$

> **Scoped preview — the definite integral.** MATH 141 does not reach the definite integral until
> **Week 8**; you need it here in Week 5. The rule was given in **Lecture 4 §7.1** and used again in
> **Lecture 13**, and it is all you need:
>
> $$\int_a^b t^{n}\,dt = \left[\frac{t^{\,n+1}}{n+1}\right]_a^b \qquad (n \neq -1)$$
>
> So a force ramping as $F(t) = ct$ over $[0,T]$ delivers $J = \int_0^T ct\,dt = c\left[\tfrac{t^2}{2}\right]_0^T = \tfrac{1}{2}cT^2$.
> **Geometrically, impulse is the area under the F–t curve** — exactly as work is the area under
> F–x. When a problem hands you a force–time *graph* rather than a formula, read off the area;
> no integration required.

**SI unit:** N·s (which is dimensionally identical to kg·m/s — the same units as momentum, as we're about to show).

---

## 4. The Impulse-Momentum Theorem — Full Derivation

Starting from Newton's second law in momentum form:

$$\vec{F}_{net} = \frac{d\vec{p}}{dt}$$

Integrate both sides over time from t_i to t_f:

$$\int_{t_i}^{t_f} \vec{F}_{net}\,dt = \int_{t_i}^{t_f} \frac{d\vec{p}}{dt}\,dt = \int_{\vec{p}_i}^{\vec{p}_f} d\vec{p} = \vec{p}_f - \vec{p}_i$$

$$\boxed{\vec{J} = \Delta\vec{p} = \vec{p}_f - \vec{p}_i}$$

**The impulse-momentum theorem: the net impulse on an object equals its change in momentum.**

> **Deep Why — parallel structure to the work-energy theorem:** Notice the beautiful symmetry:
> - **Work-energy theorem:** $\int F\,dx = \Delta KE$ (force integrated over **distance** gives change in kinetic energy)
> - **Impulse-momentum theorem:** $\int F\,dt = \Delta p$ (force integrated over **time** gives change in momentum)
>
> Both are derived from the same starting point (Newton's second law) but integrated with respect to a different variable. Choosing which one to use depends on what information you have: if you know how force varies with position, use work-energy; if you know how force varies with time, use impulse-momentum.

---

## 5. Impulse from a Force-Time Graph

Just as work is the area under an F(x) graph, **impulse is the area under an F(t) graph**:

$$J = \int F\,dt = \text{area under } F(t) \text{ curve}$$

This is especially useful for impact problems (bat hitting ball, airbag deployment, hammer strikes) where the force rises sharply, peaks, and falls over a very short time interval — the exact functional form is often unknown or irrelevant, but the total area (impulse) can be measured or estimated.

---

## 6. Average Force from Impulse

Often we don't know the detailed force-time profile of a collision, but we know the impulse (from Δp) and the duration Δt. We can then define an **average force**:

$$\bar{F} = \frac{J}{\Delta t} = \frac{\Delta p}{\Delta t}$$

This is extremely useful for estimating collision forces — car crashes, sports impacts, packaging design — where the actual force profile is complex but the average is what matters for safety analysis.

> **Deep Why — why airbags and padding work:** For a given Δp (say, decelerating a person from 15 m/s to 0 in a crash), the impulse is fixed. But $\bar F = \Delta p/\Delta t$ — the average force is **inversely proportional to the time over which the momentum change occurs**. An airbag, seatbelt stretch, or padded surface increases Δt (spreading the same momentum change over a longer time), which directly reduces the average force experienced. This is not a minor detail — it's the entire physical principle behind essentially all impact-safety engineering.

---

## 7. Worked Examples

### Example 16.1 — Impulse from constant force

A 0.50 kg ball is hit by a bat, changing its velocity from +20 m/s to −25 m/s (reversing direction) over a contact time of 4.0 ms.

**Change in momentum:**
$$\Delta p = m(v_f - v_i) = 0.50(-25 - 20) = 0.50(-45) = -22.5 \text{ kg·m/s}$$

**Impulse = Δp = −22.5 kg·m/s** (negative — in the direction opposite the ball's initial velocity)

**Average force:**
$$\bar{F} = \frac{\Delta p}{\Delta t} = \frac{-22.5}{0.004} = \mathbf{-5625 \text{ N}}$$

The magnitude, 5625 N, is enormous compared to the ball's weight (0.50×9.81 ≈ 5 N) — over 1000 times its weight — illustrating why bat-ball collisions involve huge instantaneous forces despite lasting only milliseconds.

---

### Example 16.2 — Safety engineering: stopping time and force

A 1500 kg car traveling at 20 m/s (45 mph) crashes into a wall and stops. Compare the average force if the stopping time is (a) 0.1 s (crumple zone absorbs impact) vs. (b) 0.01 s (rigid, no crumple zone).

$$\Delta p = m(0 - v_i) = 1500(-20) = -30000 \text{ kg·m/s}$$

**(a)** $\bar{F} = -30000/0.1 = \mathbf{-300{,}000 \text{ N}}$

**(b)** $\bar{F} = -30000/0.01 = \mathbf{-3{,}000{,}000 \text{ N}}$

A 10× shorter stopping time produces a 10× larger average force — this is the direct physics justification for crumple zones, which extend collision time to reduce peak force on occupants.

---

### Example 16.3 — Impulse from a varying force

A force varies as F(t) = 200 − 50t (Newtons, t in seconds) for 0 ≤ t ≤ 4 s, acting on a 10 kg object initially at rest.

**Find the impulse and the final velocity.**

$$J = \int_0^4 (200-50t)\,dt = \left[200t - 25t^2\right]_0^4 = 800 - 400 = 400 \text{ N·s}$$

$$\Delta p = J \implies mv_f - 0 = 400 \implies v_f = \frac{400}{10} = \mathbf{40 \text{ m/s}}$$

---

## 8. Momentum vs. Kinetic Energy — Two Different Vector/Scalar Tools

| Quantity | Type | Formula | Conserved when? |
|----------|------|---------|-----------------|
| Momentum p⃗ | Vector | mv⃗ | Always, for isolated systems (all collisions) |
| Kinetic Energy KE | Scalar | ½mv² | Only in elastic collisions |

This distinction is central to next lecture's discussion of collisions: momentum conservation is universal; kinetic energy conservation is not.

---

## 9. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Momentum | p⃗ = mv⃗ | Vector; same direction as velocity |
| Newton's 2nd Law (general) | F⃗_net = dp⃗/dt | Reduces to F=ma for constant mass |
| Impulse | J⃗ = ∫F⃗dt = F⃗Δt (constant F) | Area under F(t) graph |
| Impulse-momentum theorem | J⃗ = Δp⃗ | Derived from F=dp/dt integrated over time |
| Average force | F̄ = Δp/Δt | Larger Δt → smaller average force for fixed Δp |

---


---

## CS Connection — Impulse and Discrete Time Steps

Impulse J = FΔt is force integrated over time — and in a simulation running at a fixed timestep, that integral *is* the discrete update. Collision resolution in a game engine applies an impulse directly to velocity rather than a force over many frames, precisely because the interaction is shorter than one timestep.

---

## Looking Ahead

**L17** applies momentum conservation to collisions, where it does the work that energy conservation cannot.

## Conceptual Questions

1. A 60 kg person jumps off a 1 m high platform and lands stiff-legged (short stopping time) vs. bending their knees (longer stopping time). Using the impulse-momentum theorem, explain why bending the knees reduces injury risk, even though the change in momentum is identical in both cases.

2. Two objects have the same momentum but different masses. Do they necessarily have the same kinetic energy? Show algebraically using KE = p²/(2m).

3. A perfectly rigid ball bounces off a wall, reversing its velocity exactly (elastic bounce). A perfectly inelastic ball hits the same wall and sticks (comes to rest). Which case involves a larger magnitude of impulse from the wall? Explain using Δp for each case.

4. Why do boxers "roll with the punch" (move their head backward as they're hit) rather than holding perfectly still? Analyze using the impulse-momentum theorem.
