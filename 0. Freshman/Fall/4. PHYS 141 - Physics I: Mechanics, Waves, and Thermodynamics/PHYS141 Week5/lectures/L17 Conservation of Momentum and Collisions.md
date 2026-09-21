# PHYS 141 · Lecture 17
# Conservation of Momentum & Collisions

> **Core Principle:** For an isolated system (no external forces), total momentum is exactly conserved — a direct consequence of Newton's Third Law. This is true regardless of what happens internally: elastic bounces, sticky collisions, explosions. Momentum conservation is the single most powerful tool for analyzing collisions, because it holds even when we know nothing about the complicated forces during impact.

**Date:** Tuesday 27 October 2026 · 14:00–14:50 · Week 5

---


## Where This Fits

**Previously:** **L16** defined momentum and impulse. Collisions are where momentum conservation earns its place, because the internal forces cancel.

---

## 1. Conservation of Momentum — Derivation from Newton's Third Law

Consider two objects, A and B, interacting only with each other (isolated system — no external forces). By Newton's Third Law:

$$\vec{F}_{A\text{ on }B} = -\vec{F}_{B\text{ on }A}$$

By Newton's second law (momentum form), the force on each object equals its rate of change of momentum:

$$\vec{F}_{B\text{ on }A} = \frac{d\vec{p}_A}{dt} \qquad \vec{F}_{A\text{ on }B} = \frac{d\vec{p}_B}{dt}$$

Substituting the Third Law relationship:

$$\frac{d\vec{p}_B}{dt} = -\frac{d\vec{p}_A}{dt} \implies \frac{d\vec{p}_A}{dt} + \frac{d\vec{p}_B}{dt} = 0 \implies \frac{d(\vec{p}_A+\vec{p}_B)}{dt} = 0$$

This means the **total momentum** $\vec p_{total} = \vec p_A + \vec p_B$ is constant in time:

$$\boxed{\vec{p}_{total,i} = \vec{p}_{total,f}}$$

$$m_A\vec{v}_{A,i} + m_B\vec{v}_{B,i} = m_A\vec{v}_{A,f} + m_B\vec{v}_{B,f}$$

> **Deep Why:** Conservation of momentum is not a separate law of nature layered on top of Newton's laws — it is a direct mathematical consequence of the Third Law. Any time two objects interact only with each other (internal forces), the internal forces cancel in pairs when you sum over the whole system, leaving total momentum unchanged. This is why momentum conservation applies during collisions regardless of how complicated or violent the interaction forces are — we never need to know F(t) in detail, only that the forces are internal (Third Law pairs).

### 1.1 The Condition: Isolated System

Momentum conservation strictly requires **no net external force** on the system (or that the collision time is so short that external impulses like gravity or friction are negligible compared to the internal collision forces — a very good approximation for most collisions, which happen over milliseconds).

---

## 2. Types of Collisions

Collisions are classified by whether kinetic energy is conserved:

| Type | Momentum conserved? | Kinetic energy conserved? | Example |
|------|---------------------|----------------------------|---------|
| **Elastic** | Yes | Yes | Billiard balls, atomic/subatomic collisions |
| **Inelastic** | Yes | No (some KE → heat/sound/deformation) | Car crashes, most everyday collisions |
| **Perfectly inelastic** | Yes | No (maximum KE loss) | Objects stick together after collision |

**Momentum is ALWAYS conserved in an isolated system, regardless of collision type.** Kinetic energy conservation is the special, more restrictive case.

---

## 3. Perfectly Inelastic Collisions

Objects stick together after collision, moving with a common final velocity.

$$m_A v_{A,i} + m_B v_{B,i} = (m_A+m_B)v_f$$

$$\boxed{v_f = \frac{m_A v_{A,i} + m_B v_{B,i}}{m_A+m_B}}$$

### Energy Loss in Perfectly Inelastic Collisions

$$\Delta KE = KE_f - KE_i = \frac{1}{2}(m_A+m_B)v_f^2 - \left[\frac{1}{2}m_Av_{A,i}^2 + \frac{1}{2}m_Bv_{B,i}^2\right]$$

This is always negative (kinetic energy is lost) except in the trivial case where both objects already share the same velocity before collision.

---

## 4. Elastic Collisions in 1D — Full Derivation

Two conditions hold simultaneously:

**Momentum conservation:**
$$m_A v_{A,i} + m_B v_{B,i} = m_A v_{A,f} + m_B v_{B,f} \tag{1}$$

**Kinetic energy conservation:**
$$\frac{1}{2}m_Av_{A,i}^2 + \frac{1}{2}m_Bv_{B,i}^2 = \frac{1}{2}m_Av_{A,f}^2 + \frac{1}{2}m_Bv_{B,f}^2 \tag{2}$$

Solving these two equations simultaneously (a standard but somewhat lengthy algebraic exercise) yields:

$$\boxed{v_{A,f} = \frac{m_A-m_B}{m_A+m_B}v_{A,i} + \frac{2m_B}{m_A+m_B}v_{B,i}}$$

$$\boxed{v_{B,f} = \frac{2m_A}{m_A+m_B}v_{A,i} + \frac{m_B-m_A}{m_A+m_B}v_{B,i}}$$

### Special Cases Worth Memorizing the Logic Of (not the formulas)

**Case 1: Equal masses (m_A = m_B), B initially at rest (v_{B,i}=0):**
$$v_{A,f} = 0, \qquad v_{B,f} = v_{A,i}$$
The incoming object stops completely; the target takes all the velocity. (This is why a cue ball stops when hitting an equal-mass stationary ball head-on.)

**Case 2: Very heavy target (m_B >> m_A), B initially at rest:**
$$v_{A,f} \approx -v_{A,i}, \qquad v_{B,f} \approx 0$$
The light object bounces back with nearly the same speed; the heavy object barely moves. (A ball bouncing off a wall.)

**Case 3: Very heavy incoming object (m_A >> m_B), B initially at rest:**
$$v_{A,f} \approx v_{A,i}, \qquad v_{B,f} \approx 2v_{A,i}$$
The heavy object continues almost unaffected; the light target is launched at roughly twice the incoming speed.

> **Deep Why:** These limiting cases are not arbitrary curiosities — they are essential physical intuition checks. Any time you derive a general collision formula, plugging in these mass-ratio limits (equal masses; one much larger) is the fastest way to verify your algebra is correct, because the physical outcome in each limit is intuitively predictable.

---

## 5. The Coefficient of Restitution (Enrichment)

A more general way to characterize collisions between the fully elastic and fully inelastic extremes is the **coefficient of restitution**, e:

$$e = \frac{v_{B,f} - v_{A,f}}{v_{A,i} - v_{B,i}} = \frac{\text{relative speed of separation}}{\text{relative speed of approach}}$$

- e = 1: perfectly elastic
- e = 0: perfectly inelastic (objects move together after, so relative separation speed = 0)
- 0 < e < 1: partially inelastic (real-world collisions almost always fall in this range)

---

## 6. Collisions in 2D

When objects collide off-center (not head-on), momentum conservation applies **component-wise**:

$$\sum p_{x,i} = \sum p_{x,f} \qquad \sum p_{y,i} = \sum p_{y,f}$$

This gives two independent scalar equations. For a general 2D collision with 4 unknown final velocity components, you need 2 additional pieces of information (e.g., one final angle plus the elastic-collision condition, or both final angles given) to fully solve the system.

---

## 7. Worked Examples

### Example 17.1 — Perfectly inelastic collision

A 1200 kg car traveling at 15 m/s collides with a stationary 1500 kg car, and they stick together. Find the common final velocity, and the fraction of kinetic energy lost.

$$v_f = \frac{1200(15) + 1500(0)}{1200+1500} = \frac{18000}{2700} = \mathbf{6.67 \text{ m/s}}$$

**Energy loss:**
$$KE_i = \frac{1}{2}(1200)(15)^2 = 135{,}000 \text{ J}$$
$$KE_f = \frac{1}{2}(2700)(6.67)^2 = 60{,}015 \text{ J}$$
$$\Delta KE = 60{,}015 - 135{,}000 = -74{,}985 \text{ J}$$
$$\text{Fraction lost} = \frac{74{,}985}{135{,}000} = \mathbf{55.5\%}$$

More than half the kinetic energy is converted to heat, sound, and deformation — this is why perfectly inelastic collisions are the most damaging kind in vehicle crashes.

---

### Example 17.2 — Elastic collision, equal masses

A 0.20 kg billiard ball moving at 3.0 m/s hits an identical stationary ball head-on (elastic collision). Find both final velocities.

Using the equal-mass special case: $v_{A,f} = 0$, $v_{B,f} = 3.0$ m/s.

**The incoming ball stops dead; the target ball moves off at the original speed.** This is directly observable in any game of pool/billiards with a head-on shot.

---

### Example 17.3 — Elastic collision, general masses

A 2.0 kg ball moving at 5.0 m/s collides elastically with a stationary 3.0 kg ball. Find both final velocities.

$$v_{A,f} = \frac{2.0-3.0}{5.0}(5.0) + \frac{2(3.0)}{5.0}(0) = \frac{-1.0}{5.0}(5.0) = -1.0 \text{ m/s}$$

$$v_{B,f} = \frac{2(2.0)}{5.0}(5.0) + \frac{3.0-2.0}{5.0}(0) = \frac{4.0}{5.0}(5.0) = 4.0 \text{ m/s}$$

**Ball A bounces back at 1.0 m/s; Ball B moves forward at 4.0 m/s.**

**Verify momentum:** $p_i = 2.0(5.0) = 10.0$; $p_f = 2.0(-1.0)+3.0(4.0) = -2.0+12.0=10.0$ ✓

**Verify KE:** $KE_i = \frac{1}{2}(2.0)(25) = 25.0$ J; $KE_f = \frac{1}{2}(2.0)(1.0)+\frac{1}{2}(3.0)(16.0) = 1.0+24.0=25.0$ J ✓

---

### Example 17.4 — 2D collision

A 3.0 kg object moving at 4.0 m/s in the +x direction collides with a stationary 2.0 kg object. After the collision, the 3.0 kg object moves at 2.5 m/s at 30° above the +x axis. Find the velocity of the 2.0 kg object.

**x-momentum:** $3.0(4.0) = 3.0(2.5\cos30°) + 2.0(v_{Bx})$
$$12.0 = 3.0(2.165) + 2.0v_{Bx} = 6.495 + 2.0v_{Bx}$$
$$v_{Bx} = \frac{12.0-6.495}{2.0} = 2.75 \text{ m/s}$$

**y-momentum:** $0 = 3.0(2.5\sin30°) + 2.0(v_{By})$
$$0 = 3.0(1.25) + 2.0v_{By} = 3.75 + 2.0v_{By}$$
$$v_{By} = \frac{-3.75}{2.0} = -1.875 \text{ m/s}$$

**Speed and direction:**
$$|v_B| = \sqrt{2.75^2+1.875^2} = \sqrt{7.5625+3.5156} = \sqrt{11.078} = \mathbf{3.33 \text{ m/s}}$$
$$\theta = \arctan\left(\frac{-1.875}{2.75}\right) = \mathbf{-34.3°} \text{ (below +x axis)}$$

---

## 8. Summary

| Collision type | Equation | KE conserved? |
|-----------------|----------|----------------|
| General (any collision) | Σp⃗ᵢ = Σp⃗f | Not necessarily |
| Perfectly inelastic | v_f = (m_Av_A+m_Bv_B)/(m_A+m_B) | No — maximum loss |
| Elastic (1D) | Use both momentum AND KE conservation | Yes |
| 2D collision | Apply momentum conservation per component (x, y separately) | Depends on type |

---


---

## CS Connection — Elastic vs Inelastic as Lossless vs Lossy

Elastic collisions conserve kinetic energy; inelastic ones do not. The distinction is the physical analogue of lossless versus lossy compression — in both cases something is conserved (momentum, or the essential content) while something else may be irrecoverably lost. Perfectly inelastic is maximal loss subject to the conservation constraint, which is the same shape as a rate-distortion bound.

---

## Looking Ahead

**L18** generalises from colliding pairs to extended bodies, via the centre of mass.

## Conceptual Questions

1. In a perfectly inelastic collision, is it possible for the final kinetic energy to be zero? Under what specific condition on the initial velocities and masses would this happen?

2. Explain why, in an elastic collision between equal masses with one initially at rest, the incoming ball transfers ALL of its kinetic energy to the target ball, even though momentum "transfer" alone wouldn't obviously require this.

3. A bullet embeds in a wooden block (perfectly inelastic). Is momentum conserved during the collision itself? Is momentum conserved for the block+bullet system afterward, as it decelerates due to friction with the table? Explain the distinction.

4. Two ice skaters push off from rest against each other. Using conservation of momentum (not energy), explain why the lighter skater ends up moving faster than the heavier skater.
