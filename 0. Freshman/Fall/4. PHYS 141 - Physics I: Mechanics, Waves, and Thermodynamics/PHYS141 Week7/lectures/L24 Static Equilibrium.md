# PHYS 141 · Lecture 24
# Static Equilibrium

*“Equal weights at equal distances are in equilibrium and equal weights at unequal distances are not in equilibrium but incline towards the weight which is at the greater distance.”* — Archimedes, *On the Equilibrium of Planes*, Book I, Postulate 1

> **Core Principle:** An object is in static equilibrium when it has zero linear acceleration AND zero angular acceleration — both the net force and the net torque must vanish. These are two genuinely independent conditions: a system can have zero net force but still spin up (if torques don't balance), or zero net torque but still accelerate linearly (if forces don't balance). Solving equilibrium problems requires satisfying both simultaneously.

**Date:** Friday 13 November 2026 · 14:00–14:50 · Week 7

**Reading:** Serway & Jewett §12.1–12.3

**Coursework:** 📝 **PS 6** due today 17:00 · 📝 **PS 7** released today 15:00, due Fri 20 Nov 17:00 · 📊 **Quiz 7** Mon 16 Nov 14:00 · 🔬 **Lab 8** Thu 19 Nov 14:00–17:00

---


## Where This Fits

**Previously:** **L23** covered rotation with no net torque but non-zero angular momentum. Static equilibrium is the stricter case: both ΣF = 0 and Στ = 0, so nothing accelerates at all.

---

## 1. The Two Conditions for Static Equilibrium

For an object to remain at rest (or move at constant velocity with no rotation), TWO independent conditions must both hold:

**Condition 1 — Translational equilibrium:**
$$\sum \vec{F} = 0 \quad \text{(equivalently, } \sum F_x=0, \sum F_y=0\text{)}$$

**Condition 2 — Rotational equilibrium:**
$$\sum \vec{\tau} = 0 \quad \text{(about ANY chosen pivot point)}$$

### 1.1 Why Both Conditions Are Necessary

Consider a see-saw with equal weights at equal distances from the pivot but pushed in opposite directions by additional forces at the very ends that happen to cancel in net force but not in net torque (a force couple). The net force could be zero (ΣF=0) while the see-saw still angularly accelerates — because the torques from the two forces do NOT cancel (they act at different points, both causing rotation in the same sense). This shows ΣF=0 alone is insufficient; Στ=0 must be separately imposed.

Conversely, an object can have zero net torque about its center of mass while still accelerating linearly — e.g., two equal forces pushing in the same direction at symmetric points on either side of the center of mass produce no net torque about the center (their torques cancel) but a large net force (they add).

**Both conditions are independent and both must be satisfied for true static equilibrium.**

---

## 2. The Freedom to Choose Any Pivot Point

A remarkable and extremely useful fact: **if an object is in equilibrium (ΣF=0), then Στ=0 about ANY point** — not just the center of mass, not just a physical hinge. This means you are free to choose whichever pivot point makes the algebra easiest, typically one that eliminates an unknown force from the torque equation entirely (since a force acting AT the chosen pivot point has zero lever arm, and hence contributes zero torque about that point).

> **Deep Why:** This freedom follows directly from the fact that if ΣF=0, then the torque about any two different points P₁ and P₂ differs only by a term proportional to ΣF (which is zero). Formally: $\vec\tau_{P_2} = \vec\tau_{P_1} + (\vec r_{P_1}-\vec r_{P_2})\times\sum\vec F$. If ΣF⃗=0, the extra term vanishes, and the torque is the same about every point. This is why choosing a clever pivot (often through an unknown force's point of application) is the single most powerful technique for simplifying equilibrium problems.

---

## 3. Center of Gravity

The **center of gravity** is the point at which the total weight of an object can be considered to act, for the purposes of computing torque. In a uniform gravitational field (an excellent approximation for all problems in this course — Earth's surface, over the small size of ordinary objects), **the center of gravity coincides exactly with the center of mass** (from Week 5).

$$\vec{r}_{cg} = \vec{r}_{cm} \quad \text{(uniform gravitational field)}$$

For extended objects (beams, ladders, planks), the weight is treated as a single force $Mg$ acting at the center of gravity/mass for all torque calculations.

---

## 4. The Standard Method for Solving Equilibrium Problems

1. **Draw a complete free body diagram** — all forces, including weight (acting at the center of gravity), applied forces, normal forces, tensions, and friction if present.
2. **Choose a pivot point** wisely — ideally at the location of an unknown force, to eliminate it from the torque equation.
3. **Write ΣF_x = 0 and ΣF_y = 0.**
4. **Write Στ = 0** about your chosen pivot, being careful with signs (counterclockwise positive is the standard convention).
5. **Solve the resulting system of equations** (typically 2–3 equations) for the unknowns.

---

## 5. Worked Examples

### Example 24.1 — Simple beam with two supports

A uniform beam of length 6.0 m and weight 400 N rests horizontally on two supports: one at the left end, one 4.0 m from the left end. Find the force exerted by each support.

**FBD:** Weight 400 N downward at the center (x=3.0 m from left end). Support forces $N_1$ (at x=0) and $N_2$ (at x=4.0 m), both upward.

**Choose pivot at $N_1$'s location (x=0)** — this eliminates $N_1$ from the torque equation.

**Torque equation (counterclockwise positive):**
$$\sum\tau = N_2(4.0) - 400(3.0) = 0$$
$$N_2 = \frac{1200}{4.0} = 300 \text{ N}$$

**Force equation:**
$$N_1 + N_2 - 400 = 0 \implies N_1 = 400-300 = \mathbf{100 \text{ N}}$$

**$N_1=100$ N, $N_2=300$ N.**

**Check with a second pivot (at $N_2$'s location) as verification:**
$$\sum\tau = 400(1.0) - N_1(4.0) = 0 \implies N_1 = \frac{400}{4.0} = 100 \text{ N} \checkmark$$

(Here, the weight's lever arm from $N_2$'s position is $4.0-3.0=1.0$ m, on the opposite side, hence positive torque; $N_1$ acts at distance 4.0 m from this pivot, producing negative/clockwise torque since it's upward on the opposite side.)

---

### Example 24.2 — Ladder against a wall

A 5.0 m uniform ladder of weight 250 N leans against a frictionless wall, making a 60° angle with the ground. The floor provides both a normal force and friction (needed to prevent the ladder from slipping); the wall provides only a normal force (frictionless). Find the normal force from the floor, the normal force from the wall, and the minimum coefficient of static friction at the floor needed to prevent slipping.

**FBD:** Weight W=250 N downward at the ladder's midpoint (2.5 m along the ladder from either end). Normal force from floor $N_f$ (upward, at base). Friction from floor $f_s$ (horizontal, at base, pointing toward the wall to prevent the base from sliding away). Normal force from wall $N_w$ (horizontal, pointing away from the wall, at the top).

**Geometry:** Ladder length L=5.0 m at 60° from horizontal.
Horizontal distance from base to top (where it touches the wall) = $L\cos60°=2.5$ m
Height of top of ladder = $L\sin60°=4.33$ m
Weight acts at the midpoint: horizontal distance from base = $\frac{L}{2}\cos60°=1.25$ m

**Force equations:**
$$\sum F_y = N_f - W = 0 \implies N_f = 250 \text{ N}$$
$$\sum F_x = N_w - f_s = 0 \implies f_s = N_w$$

**Torque equation about the base (eliminates $N_f$ and $f_s$, both acting at the base):**
$$\sum\tau = N_w(L\sin60°) - W\left(\frac{L}{2}\cos60°\right) = 0$$
$$N_w(4.33) = 250(1.25)$$
$$N_w = \frac{312.5}{4.33} = \mathbf{72.2 \text{ N}}$$

Then $f_s = N_w = 72.2$ N (from the x-force equation).

**Minimum coefficient of static friction:**
$$\mu_{s,min} = \frac{f_s}{N_f} = \frac{72.2}{250} = \mathbf{0.289}$$

If the actual coefficient of static friction between the ladder and floor is less than 0.289, the ladder will slip.

---

### Example 24.3 — Hanging sign supported by a cable and a hinge

A uniform horizontal beam of length 3.0 m and weight 150 N is attached to a wall by a hinge at one end. A cable attached to the other end of the beam runs to the wall at an angle of 40° above the beam, supporting a sign of weight 80 N hung from the far end of the beam. Find the tension in the cable and the force exerted by the hinge on the beam.

**FBD:** Weight of beam (150 N) at the midpoint (1.5 m from hinge). Weight of sign (80 N) at the far end (3.0 m from hinge). Cable tension T at 40° above the beam, acting at the far end. Hinge force $(H_x, H_y)$ at the hinge (unknown direction, so keep as components).

**Choose pivot at the hinge** — eliminates the unknown hinge force entirely from the torque equation.

**Torque equation (counterclockwise positive; weights produce clockwise/negative torque, cable's vertical component produces counterclockwise/positive torque):**

$$\sum\tau = T\sin40°(3.0) - 150(1.5) - 80(3.0) = 0$$
$$T\sin40°(3.0) = 225+240=465$$
$$T(0.643)(3.0) = 465$$
$$T = \frac{465}{1.928} = \mathbf{241.2 \text{ N}}$$

**Force equations:**
$$\sum F_x = H_x - T\cos40° = 0 \implies H_x = 241.2\times0.766=\mathbf{184.7 \text{ N}}$$
$$\sum F_y = H_y+T\sin40°-150-80=0 \implies H_y = 230-241.2(0.643)=230-155.1=\mathbf{74.9 \text{ N}}$$

**Hinge force magnitude:** $|H|=\sqrt{184.7^2+74.9^2}=\sqrt{34114+5610}=\sqrt{39724}=\mathbf{199.3 \text{ N}}$

---

## 6. Summary

| Concept | Equation | Key Point |
|---------|----------|-----------|
| Translational equilibrium | ΣF⃗=0 | Independent condition |
| Rotational equilibrium | Στ⃗=0 | Independent condition; can choose ANY pivot if ΣF=0 |
| Center of gravity | = center of mass (uniform g) | Weight acts here for torque purposes |
| Pivot choice strategy | Choose pivot at an unknown force's location | Eliminates that force from the torque equation |

---


---

## CS Connection — Equilibrium as Constraint Satisfaction

A statics problem is a system of simultaneous equations: ΣFx = 0, ΣFy = 0, Στ = 0. Solving it is linear algebra (MATH 241, Year 2), and choosing a pivot to eliminate an unknown force is the same tactic as choosing a pivot to eliminate a variable in Gaussian elimination. Finite element analysis scales this to millions of equations, which is why structural engineering is a computational discipline.

---

## Looking Ahead

This is the final lecture of PHYS 141. The sequel is oscillations, waves, and thermodynamics — and the mechanics built here underpins ECE 110's circuit analysis (Spring), where Kirchhoff's laws play the role that force and torque balance play now.

## Conceptual Questions

1. Explain why choosing the pivot point at the location of an unknown hinge force is almost always the most efficient strategy for equilibrium problems, using the freedom-of-pivot-choice principle.

2. A meter stick is balanced on a pivot not at its center (say, at the 30 cm mark), with a weight hung from one end. Explain, using torque balance, how you could determine the meter stick's own weight if you know the value of the hanging weight and the balance point.

3. A ladder is more likely to slip when leaned at a shallow angle (nearly horizontal) than at a steep angle (nearly vertical) against a wall. Using the torque equation from Example 24.2 (generalized to angle θ instead of 60°), explain why $\mu_{s,min}$ increases as θ decreases.

4. Why does the location of the center of gravity matter for the stability of an object (e.g., why is a car with a low center of gravity less likely to tip over in a turn)? Connect this to the torque produced by gravity when the object is tilted.
