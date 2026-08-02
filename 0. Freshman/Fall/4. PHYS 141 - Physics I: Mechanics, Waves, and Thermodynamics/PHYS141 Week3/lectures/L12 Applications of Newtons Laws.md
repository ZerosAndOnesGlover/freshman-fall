# PHYS 141 — Lecture 12
# Applications of Newton's Laws: Friction, Inclines, and Connected Systems

> **Core Principle:** Newton's second law is one equation — ΣF⃗ = ma⃗ — applied over and over to different systems with different forces. Mastery of this week's material comes from methodical FBD construction and disciplined component decomposition, not from memorizing special cases.

---


## Where This Fits

**Previously:** **L11** established the free body diagram method. This lecture applies it where the forces are least obvious.

---

## 1. Friction

Friction is a contact force that opposes relative motion (or the tendency of relative motion) between two surfaces. It arises from microscopic interactions between surface irregularities and adhesive bonds at the contact interface.

### 1.1 Two Types of Friction

**Static friction (f_s):** Acts when the surfaces are not sliding relative to each other. It exactly opposes the applied force up to a maximum value:

$$f_s \leq \mu_s N$$

where μ_s is the **coefficient of static friction** and N is the normal force. Static friction takes whatever value is needed to prevent sliding — up to its maximum. The maximum occurs just at the point of slipping.

**Kinetic friction (f_k):** Acts when the surfaces are sliding. It has a fixed magnitude (independent of speed, for the model we use):

$$f_k = \mu_k N$$

where μ_k is the **coefficient of kinetic friction**. Unlike static friction, kinetic friction is not an inequality — it always has exactly this value during sliding.

### 1.2 Key Properties

- Always: **μ_k < μ_s** — it takes more force to start sliding than to keep sliding
- Both coefficients are **dimensionless** and depend on the pair of surfaces in contact
- Friction is **independent of contact area** (for the standard model) — a wide block and a narrow block of the same mass have the same friction force
- Friction is **proportional to the normal force** — pressing harder increases friction
- Direction: always **parallel to the surface, opposing relative motion** (kinetic) or opposing the tendency of motion (static)

### 1.3 Typical Coefficient Values

| Surface pair | μ_s | μ_k |
|-------------|-----|-----|
| Rubber on dry concrete | 0.80 | 0.65 |
| Steel on steel | 0.74 | 0.57 |
| Wood on wood | 0.40 | 0.20 |
| Ice on ice | 0.10 | 0.03 |
| Teflon on steel | 0.04 | 0.04 |
| Synovial joint (knee) | 0.01 | 0.003 |

> **Deep Why — Why does friction exist?** At the microscopic level, two surfaces in contact actually touch only at tiny high points (asperities). The real contact area is much smaller than the apparent area. At these contact points, atoms form temporary adhesive bonds. Sliding requires breaking these bonds — that resistance is kinetic friction. Static friction is the force needed to begin breaking them. The independence of friction from contact area holds because: larger apparent area → more contact points → each carrying less force → same total adhesion. This model breaks down for very smooth surfaces (where area matters) and for rubbers (where adhesion dominates).

---

## 2. Friction Problem-Solving

### Step-by-step procedure:

1. Draw FBD
2. Identify whether static or kinetic friction applies (is the object sliding or not?)
3. Write ΣFᵧ = 0 (if no vertical acceleration) to find N
4. For static: check if applied force exceeds μ_s N. If not, f_s = F_applied (equilibrium). If yes, the object slides and f_k = μ_k N applies.
5. Write ΣFₓ = ma with the correct friction force
6. Solve for unknown

---

## 3. Worked Examples — Friction

### Example 12.1 — Does it slide?

A 10 kg box sits on a surface with μ_s = 0.40, μ_k = 0.25. A horizontal force of 35 N is applied.

**Step 1:** Find maximum static friction.
N = mg = 10 × 9.81 = 98.1 N
f_s,max = μ_s N = 0.40 × 98.1 = 39.2 N

**Step 2:** Compare applied force to f_s,max.
F_applied = 35 N < 39.2 N → **the box does NOT slide.**

Static friction exactly balances: f_s = 35 N (not 39.2 N — that's the maximum, not the actual value).
Net force = 0. Acceleration = 0.

---

### Example 12.2 — Sliding box

Same box, but now F = 50 N is applied horizontally.

50 N > f_s,max = 39.2 N → **box slides.**

Kinetic friction: f_k = μ_k N = 0.25 × 98.1 = 24.5 N (opposing motion)

**x:** ΣFₓ = F − f_k = ma
50 − 24.5 = 10 · a
$$a = \frac{25.5}{10} = \mathbf{2.55 \text{ m/s}^2}$$

---

### Example 12.3 — Block on incline with friction

A 5.0 kg block is on a 25° incline. μ_s = 0.35, μ_k = 0.25. Does it slide? If so, what is the acceleration?

**Axes:** x down the slope, y perpendicular to slope.

**Normal force:** N = mg cos25° = 5.0(9.81)(0.906) = 44.4 N

**Component of gravity along slope:** mg sin25° = 5.0(9.81)(0.423) = 20.7 N (down slope)

**Maximum static friction (up the slope, opposing tendency to slide down):**
f_s,max = μ_s N = 0.35 × 44.4 = 15.5 N

**Comparison:** 20.7 N > 15.5 N → **block slides down.**

**Kinetic friction (up the slope):** f_k = μ_k N = 0.25 × 44.4 = 11.1 N

**x:** mg sin25° − f_k = ma
20.7 − 11.1 = 5.0 · a
$$a = \frac{9.6}{5.0} = \mathbf{1.92 \text{ m/s}^2} \text{ (down the slope)}$$

---

## 4. The Atwood Machine

Two masses m₁ and m₂ are connected by a massless string over a massless, frictionless pulley. Mass m₂ > m₁, so m₂ accelerates downward and m₁ accelerates upward.

### Setting up the equations

**Key insight:** The string is inextensible, so both masses have the same magnitude of acceleration a. The tension T is the same throughout the string.

**Define positive direction:** Let downward be positive for m₂ and upward be positive for m₁ (so both accelerate in their "positive" direction together).

**FBD for m₁ (taking up as positive):**
$$T - m_1 g = m_1 a \tag{1}$$

**FBD for m₂ (taking down as positive):**
$$m_2 g - T = m_2 a \tag{2}$$

**Add equations (1) and (2):** T cancels:
$$m_2 g - m_1 g = (m_1 + m_2) a$$

$$\boxed{a = \frac{(m_2 - m_1)g}{m_1 + m_2}} \tag{Atwood acceleration}$$

**Substitute back to find T:**
$$T = m_1(g + a) = m_1 g + \frac{m_1(m_2-m_1)g}{m_1+m_2} = \frac{2m_1 m_2 g}{m_1 + m_2} \tag{Atwood tension}$$

### Limit checks

- If m₁ = m₂: a = 0 (balanced, no acceleration) ✓
- If m₂ >> m₁: a → g (heavy mass essentially in free fall) ✓
- If m₁ = 0: a = g, T = 0 (massless m₁ has no effect) ✓

---

## 5. Connected Bodies on a Surface

### Example 12.4 — Block pulled by hanging mass

A block of mass M = 4.0 kg sits on a frictionless table. A string over a frictionless pulley connects it to a hanging mass m = 1.5 kg.

**System approach:** Both objects accelerate with the same magnitude a.

**For hanging mass m (down positive):**
$$mg - T = ma \tag{1}$$

**For block M (rightward positive, direction of motion):**
$$T = Ma \tag{2}$$

**Add (1) and (2):**
$$mg = (M + m)a$$
$$a = \frac{mg}{M+m} = \frac{1.5 \times 9.81}{5.5} = \mathbf{2.68 \text{ m/s}^2}$$

**Tension:**
$$T = Ma = 4.0 \times 2.68 = \mathbf{10.7 \text{ N}}$$

Note: T < mg (= 14.7 N). The string doesn't support the full weight of the hanging mass because m is accelerating downward — some of its weight goes into accelerating the system.

---

## 6. The Friction Incline + Hanging Mass System

A more complex connected system: block m₁ on an incline at angle θ (with friction μ_k), connected by string over a pulley at the top of the incline to a hanging mass m₂.

**Assume m₂ is heavy enough to pull m₁ up the incline.**

**Forces on m₁ along incline (up-incline = positive):**
- Tension T (up)
- Weight component mg sinθ (down)
- Kinetic friction f_k = μ_k m₁g cosθ (down, since m₁ moves up)

$$T - m_1 g \sin\theta - \mu_k m_1 g \cos\theta = m_1 a \tag{1}$$

**Forces on m₂ (down = positive):**
$$m_2 g - T = m_2 a \tag{2}$$

**Add:**
$$m_2 g - m_1 g\sin\theta - \mu_k m_1 g\cos\theta = (m_1+m_2)a$$

$$a = \frac{m_2 g - m_1 g(\sin\theta + \mu_k\cos\theta)}{m_1+m_2}$$

This single formula encodes the competition between the hanging mass pulling the system and gravity+friction opposing motion on the incline.

---

## 7. Circular Motion Requires a Real Centripetal Force

From Week 2, we know a_c = v²/r directed inward. Newton's second law tells us there must be a real inward force of magnitude mv²/r. This force is called the **centripetal force** — but it is not a new kind of force. It is whatever physical force happens to point inward in a given situation:

| Situation | What provides centripetal force |
|-----------|-------------------------------|
| Car on circular road | Friction from road on tires |
| Planet orbiting star | Gravity |
| Ball on a string | Tension in string |
| Car on inside of loop | Normal force from track |
| Satellite in orbit | Gravity |

**Setting up circular motion problems:**
$$\sum F_{\text{inward}} = \frac{mv^2}{r}$$

The left side is the net inward force from the FBD. The right side is the required centripetal acceleration times mass.

### Example 12.5 — Car on a banked curve

A car moves at speed v around a circular banked curve (banked at angle θ, radius r). Assuming no friction, what banking angle is needed?

**FBD on car:** Weight mg downward; Normal force N perpendicular to banked surface (angled inward and upward).

**Components of N:** horizontal component = N sinθ (inward, provides centripetal force); vertical component = N cosθ (upward, supports weight).

**y (no vertical acceleration):** N cosθ = mg → N = mg/cosθ

**Centripetal (inward):** N sinθ = mv²/r

**Divide:** tanθ = v²/(rg)

$$\boxed{\theta = \arctan\!\left(\frac{v^2}{rg}\right)}$$

This angle is independent of the car's mass — all cars need the same banking angle for the same v and r. This is why banked highways are designed for a specific speed.

---

## 8. Summary Table

| Situation | Key equation | What to find N from |
|-----------|-------------|-------------------|
| Flat surface, no vertical acceleration | N = mg | ΣFᵧ = 0 |
| Incline angle θ, no friction | a = g sinθ, N = mg cosθ | ΣF⊥ = 0 |
| Incline with kinetic friction | a = g(sinθ − μ_k cosθ) | N from ΣF⊥, then f_k = μ_k N |
| Atwood machine | a = (m₂−m₁)g/(m₁+m₂) | Subtract equations for each mass |
| Circular motion | ΣF_inward = mv²/r | Centripetal condition |
| Banked curve (no friction) | tanθ = v²/(rg) | ΣFᵧ=0 + centripetal |

---


---

## CS Connection — Friction, Constraints, and Solving Systems

Connected systems give simultaneous equations — one F = ma per body plus constraint equations linking them. Solving them is linear algebra, which is MATH 241's subject in Year 2. The static-friction inequality f ≤ μ_s N is a *constraint* rather than an equation, which puts these problems in the same family as the constraint-satisfaction problems CS 331 (Artificial Intelligence) treats.

---

## Looking Ahead

**L13** introduces an alternative to force analysis entirely: energy methods, which sidestep acceleration and time.

## Conceptual Questions

1. Static friction can be less than μ_s N. Explain with an example when static friction is exactly zero, when it is less than maximum, and when it equals its maximum value.

2. A block on an incline is held in place by friction. If you increase the mass of the block (keeping angle and μ_s fixed), does it become easier or harder to hold? Show using the relevant equations.

3. In the Atwood machine, why is the tension T less than m₂g even though m₂ is accelerating downward and T is the only upward force on m₁?

4. A car travels in a circle on a flat road. The centripetal force comes from friction. If the car's speed doubles, by what factor must the friction force increase to maintain the same radius? What does this imply about safe driving in curves?
