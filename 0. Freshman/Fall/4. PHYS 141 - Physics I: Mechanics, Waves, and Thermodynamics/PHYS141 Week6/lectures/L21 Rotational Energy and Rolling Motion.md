# PHYS 141 · Lecture 21
# Rotational Kinetic Energy & Rolling Motion

> **Core Principle:** A rotating object stores kinetic energy in its rotation, exactly analogous to translational kinetic energy but with moment of inertia replacing mass and angular velocity replacing linear velocity. An object that both rotates AND translates (like a rolling ball) carries both forms of kinetic energy simultaneously — and the split between them, governed by the rolling-without-slipping condition, determines everything about how such objects accelerate down inclines.

**Date:** Friday 6 November 2026 · 14:00–14:50 · Week 6

---


## Where This Fits

**Previously:** **L20** gave τ = Iα, the rotational F = ma. Just as L13 offered energy as an alternative to force, rotational energy offers an alternative to torque analysis.

---

## 1. Rotational Kinetic Energy — Derivation

Consider a rigid body rotating about a fixed axis with angular velocity ω. Each particle $i$ at distance $r_i$ from the axis has speed $v_i = r_i\omega$ and kinetic energy $\frac{1}{2}m_iv_i^2 = \frac{1}{2}m_ir_i^2\omega^2$.

Summing over all particles:

$$KE_{rot} = \sum_i \frac{1}{2}m_ir_i^2\omega^2 = \frac{1}{2}\omega^2\sum_i m_ir_i^2 = \frac{1}{2}\omega^2 I$$

$$\boxed{KE_{rot} = \frac{1}{2}I\omega^2}$$

This is the direct rotational analog of $KE_{trans}=\frac{1}{2}mv^2$, with $I \leftrightarrow m$ and $\omega \leftrightarrow v$.

---

## 2. Rolling Without Slipping — The Kinematic Constraint

An object that rolls without slipping (no skidding) on a surface has its rotational and translational motions linked by a single condition:

$$\boxed{v_{cm} = R\omega}$$

where $v_{cm}$ is the speed of the center of mass, R is the object's radius, and ω is its angular velocity about the center of mass axis.

### 2.1 Why This Condition Holds

At the instant a point on the rolling object touches the ground, that contact point has **zero velocity relative to the ground** (this is the definition of "not slipping" — no relative sliding at the contact point). The contact point's velocity is the vector sum of the center of mass translation ($v_{cm}$, forward) and the rotational velocity at that point ($R\omega$, backward relative to the center, since the bottom of a forward-rolling wheel moves backward relative to the axle). Setting these to cancel:

$$v_{cm} - R\omega = 0 \implies v_{cm} = R\omega$$

Differentiating both sides with respect to time gives the corresponding acceleration relationship:

$$a_{cm} = R\alpha$$

---

## 3. Total Kinetic Energy of a Rolling Object

A rolling object has BOTH translational KE (motion of its center of mass) and rotational KE (spinning about its center of mass):

$$KE_{total} = KE_{trans} + KE_{rot} = \frac{1}{2}Mv_{cm}^2 + \frac{1}{2}I_{cm}\omega^2$$

Using the rolling condition $\omega = v_{cm}/R$:

$$KE_{total} = \frac{1}{2}Mv_{cm}^2 + \frac{1}{2}I_{cm}\left(\frac{v_{cm}}{R}\right)^2 = \frac{1}{2}Mv_{cm}^2\left(1+\frac{I_{cm}}{MR^2}\right)$$

This form is extremely useful: define the dimensionless shape factor $\beta = I_{cm}/(MR^2)$ (values from the moment of inertia table, Lecture 20):

| Shape | β = I_cm/(MR²) |
|-------|-----------------|
| Solid sphere | 2/5 = 0.400 |
| Solid cylinder/disk | 1/2 = 0.500 |
| Thin spherical shell | 2/3 = 0.667 |
| Thin hoop/ring | 1 = 1.000 |

$$KE_{total} = \frac{1}{2}Mv_{cm}^2(1+\beta)$$

---

## 4. Rolling Down an Incline — Energy Method

A classic and important problem: an object of mass M, radius R, and shape factor β starts from rest at height h on a frictionless-for-sliding-but-sufficient-for-rolling incline (i.e., there IS friction, but it's static friction that enables rolling without slipping, and it does NO work because the contact point has zero velocity — no relative sliding, hence no energy dissipation).

### 4.1 Why Static Friction Does No Work Here

This is a subtle but crucial point: **static friction is necessary for rolling without slipping** (it provides the torque that links rotation to translation), but because the contact point has zero instantaneous velocity (by the rolling condition), the friction force does **zero work** — $W = \vec F \cdot \vec v_{contact} = \vec F \cdot 0 = 0$. This means we CAN use pure energy conservation, even though friction is present.

### 4.2 Energy Conservation

$$Mgh = \frac{1}{2}Mv_{cm}^2(1+\beta)$$

$$\boxed{v_{cm} = \sqrt{\frac{2gh}{1+\beta}}}$$

### 4.3 The Key Result: Shape Matters, Size and Mass Don't

Notice mass M cancels entirely (as with all our previous energy-based falling/rolling problems), and radius R does NOT appear at all in the final speed — **only the shape factor β matters.**

**Ranking by final speed (fastest to slowest), for the same starting height:**

1. **Solid sphere** (β=0.400) — fastest, most speed converted to translation
2. **Solid cylinder/disk** (β=0.500)
3. **Thin spherical shell** (β=0.667)
4. **Thin hoop/ring** (β=1.000) — slowest, most energy "wasted" on rotation

> **Deep Why:** Objects with more mass concentrated far from their rotation axis (larger β) require more energy to spin up to a given ω, leaving less energy available for translational motion. A hoop, with all its mass at the rim, has the highest β and is the slowest roller; a solid sphere, with mass distributed close to the center on average, has the lowest β and is the fastest. This is a beautiful, classic demonstration — race a solid ball against a hoop down a ramp, and the ball wins every time, regardless of their masses or sizes (as long as both roll without slipping).

---

## 5. Rolling Down an Incline — Force/Torque Method (Cross-Check)

We can also derive the acceleration using Newton's second law and τ = Iα directly, as a check on the energy method.

**Forces on the rolling object:** gravity component along incline $Mg\sin\theta$ (down-slope), normal force N (perpendicular), static friction $f_s$ (up-slope, providing the torque for rotation).

**Translation (along incline):**
$$Mg\sin\theta - f_s = Ma_{cm} \tag{1}$$

**Rotation (about center of mass, friction is the only force with a lever arm about the CM):**
$$f_sR = I_{cm}\alpha = I_{cm}\frac{a_{cm}}{R} \tag{2}$$

From (2): $f_s = \dfrac{I_{cm}a_{cm}}{R^2} = \beta Ma_{cm}$ (using $I_{cm}=\beta MR^2$)

Substitute into (1):
$$Mg\sin\theta - \beta Ma_{cm} = Ma_{cm}$$
$$g\sin\theta = a_{cm}(1+\beta)$$

$$\boxed{a_{cm} = \frac{g\sin\theta}{1+\beta}}$$

This matches the energy method exactly (differentiate $v_{cm}^2 = 2gh/(1+\beta)$ using kinematics, with $h = L\sin\theta$, and you recover the same acceleration formula) — a valuable consistency check between two independent methods.

---

## 6. Worked Examples

### Example 21.1 — Race down an incline

A solid sphere and a thin hoop, both of the same mass and radius, are released from rest at the same height h = 2.0 m on a ramp. Find each one's speed at the bottom.

**Sphere (β=0.4):** $v = \sqrt{2gh/1.4} = \sqrt{2(9.81)(2.0)/1.4} = \sqrt{39.24/1.4} = \sqrt{28.03} = \mathbf{5.29 \text{ m/s}}$

**Hoop (β=1.0):** $v = \sqrt{2gh/2.0} = \sqrt{39.24/2.0} = \sqrt{19.62} = \mathbf{4.43 \text{ m/s}}$

The sphere is significantly faster — about 19% faster in speed (and would win the race by an even larger margin in elapsed time, since it also accelerates faster throughout).

---

### Example 21.2 — Rotational KE of a spinning disk

A solid disk (M=5.0 kg, R=0.25 m) spins at 20 rad/s about its central axis. Find its rotational kinetic energy.

$$I = \frac{1}{2}MR^2 = \frac{1}{2}(5.0)(0.0625) = 0.15625 \text{ kg·m}^2$$
$$KE_{rot} = \frac{1}{2}I\omega^2 = \frac{1}{2}(0.15625)(400) = \mathbf{31.25 \text{ J}}$$

---

### Example 21.3 — Total KE of a rolling ball

A solid ball (M=0.60 kg, R=0.10 m) rolls without slipping at $v_{cm}=4.0$ m/s. Find its translational KE, rotational KE, and total KE.

$$KE_{trans} = \frac{1}{2}(0.60)(16) = 4.8 \text{ J}$$

$$\omega = v_{cm}/R = 4.0/0.10 = 40 \text{ rad/s}$$
$$I = \frac{2}{5}MR^2 = \frac{2}{5}(0.60)(0.01) = 0.0024 \text{ kg·m}^2$$
$$KE_{rot} = \frac{1}{2}(0.0024)(1600) = 1.92 \text{ J}$$

$$KE_{total} = 4.8+1.92 = \mathbf{6.72 \text{ J}}$$

**Check with shortcut formula:** $KE_{total} = \frac{1}{2}Mv^2(1+\beta) = \frac{1}{2}(0.60)(16)(1.4) = 4.8\times1.4=6.72$ J ✓

Note: for a solid sphere, rotational KE is exactly $\beta = 0.4 = 40\%$ of translational KE (1.92/4.8 = 0.4 ✓), and $\frac{KE_{rot}}{KE_{total}} = \frac{\beta}{1+\beta} = \frac{0.4}{1.4} = 28.6\%$ of the total.

---

## 7. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Rotational KE | KE_rot = ½Iω² | Direct analog of ½mv² |
| Rolling condition | v_cm = Rω, a_cm = Rα | No slipping at contact point |
| Total rolling KE | KE = ½Mv²(1+β), β=I_cm/(MR²) | Shape factor β determines the split |
| Rolling incline speed | v=√(2gh/(1+β)) | Mass and radius cancel; only shape matters |
| Rolling incline acceleration | a=g sinθ/(1+β) | Matches energy-method result |
| Static friction in rolling | Does zero work | Contact point has zero velocity |

---


---

## CS Connection — Rolling Constraints and Coupled Variables

Rolling without slipping ties v = ωR — one constraint removing one degree of freedom, so translation and rotation can no longer be solved independently. Constraint propagation of exactly this kind drives layout engines and constraint solvers; the physics is a small instance of a general pattern where relationships between variables reduce the search space.

---

## Looking Ahead

**L22** introduces angular momentum, the rotational analogue of the momentum from L16.

## Conceptual Questions

1. A solid sphere and a solid cylinder of DIFFERENT masses and DIFFERENT radii are released from the same height on the same incline. Which reaches the bottom first? Does the answer depend on the specific masses or radii?

2. Why does static (not kinetic) friction act at the contact point of a rolling-without-slipping object? What would happen (physically) if the object began to slip?

3. A ball rolling without slipping on a horizontal frictionless-for-sliding surface (imagine a magic surface with just enough friction to maintain rolling but no dissipation) continues at constant velocity forever. Reconcile this with the fact that friction is present.

4. If you compare a rolling object's total KE to what it would have if it were sliding (not rolling) at the same v_cm with no rotation, which is larger? What does this imply about how much speed a rolling object "loses" to spinning, for a given amount of gravitational PE converted?
