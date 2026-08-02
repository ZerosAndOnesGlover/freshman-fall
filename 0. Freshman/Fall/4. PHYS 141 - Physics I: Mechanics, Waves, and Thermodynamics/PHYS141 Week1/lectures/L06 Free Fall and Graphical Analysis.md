# PHYS 141 · Lecture 6
# Free Fall & Graphical Analysis of Motion

> **Core Principle:** Free fall is constant-acceleration motion with a = −g, where g = 9.81 m/s² is determined by the Earth's mass and radius alone — completely independent of the mass, size, or composition of the falling object. Reading motion graphs fluently is as important as solving equations; graphs reveal structure that algebra alone can hide.

---


## Where This Fits

**Previously:** **L05** produced the constant-acceleration equations. Near Earth's surface gravity supplies a constant acceleration, so those equations apply directly.

---

## 1. Free Fall — The Fundamental Case of Constant Acceleration

### 1.1 What is Free Fall?

**Free fall** means motion under gravity alone — no air resistance, no contact forces. In free fall, every object near Earth's surface accelerates downward at the same rate:

$$g = 9.81 \text{ m/s}^2 \approx 9.8 \text{ m/s}^2 \approx 10 \text{ m/s}^2 \text{ (quick estimate)}$$

> **The deep why — Galileo vs. Aristotle:** Aristotle taught that heavier objects fall faster. Galileo (ca. 1590–1638) argued — and famously demonstrated — that all objects fall at the same rate in the absence of air resistance. The theoretical justification came from Newton: gravitational force is proportional to mass (F = mg), and Newton's second law says acceleration = force/mass. Therefore a = F/m = mg/m = g. The mass cancels exactly — which is why all objects fall equally. This cancellation seems almost accidental, but it reflects something deep: the equality of **gravitational mass** (which determines how strongly gravity pulls) and **inertial mass** (which determines how much an object resists acceleration). Einstein elevated this to the **Equivalence Principle**, the cornerstone of General Relativity.

### 1.2 Sign Convention for Free Fall

**The most common source of error in free fall problems is sign inconsistency.**

**Recommended convention (take up as positive):**
- Position x: positive upward from the chosen origin
- Velocity v: positive when moving upward, negative when moving downward
- Acceleration a = **−g = −9.81 m/s²** (gravity pulls downward, which is the negative direction)

You can equally well take downward as positive (a = +g), but you must be consistent throughout every equation in the problem.

### 1.3 Value of g

At Earth's surface: g = 9.81 m/s² (standard value)

g varies slightly with:
- **Altitude:** g decreases with altitude as 1/r² (Moon's g ≈ 1.62 m/s²; Mars's g ≈ 3.71 m/s²)
- **Latitude:** Earth's equatorial bulge and rotation make g slightly smaller at the equator (~9.78 m/s²) than at the poles (~9.83 m/s²)
- **Local geology:** Dense ore deposits nearby slightly increase g

For this course: g = 9.81 m/s² unless otherwise specified.

---

## 2. Applying the Kinematic Equations to Free Fall

The kinematic equations from Lecture 5 apply directly, with a = −g (taking up as positive):

| Kinematic equation | Free-fall form (up positive) |
|-------------------|------------------------------|
| v = v₀ + at | v = v₀ − gt |
| Δx = v₀t + ½at² | Δy = v₀t − ½gt² |
| v² = v₀² + 2aΔx | v² = v₀² − 2gΔy |
| Δx = ½(v₀+v)t | Δy = ½(v₀+v)t |

---

## 3. Key Free Fall Results to Know

### 3.1 Time to Reach Maximum Height

At maximum height, v = 0. From v = v₀ − gt:

$$t_{top} = \frac{v_0}{g}$$

### 3.2 Maximum Height Reached

Using v² = v₀² − 2gΔy with v = 0:

$$\Delta y_{max} = \frac{v_0^2}{2g}$$

### 3.3 Symmetry of Free Fall

If an object is thrown upward with speed v₀ and returns to the same height:
- The time to go up equals the time to come down
- The speed on return equals the launch speed v₀ (but velocity is negative — downward)
- The trajectory is perfectly symmetric in time about the top point

**Proof of symmetry:** Let the object go up for time t_top = v₀/g, reaching height h_max = v₀²/2g.
On the way down: Δy = 0 − h_max = −v₀²/2g. Using Δy = ½(0 + v)t_down:
- v (downward) = −v₀
- t_down = 2h_max/|v| = v₀/g = t_top ✓

### 3.4 Range of Fall from Rest

If dropped from rest (v₀ = 0) from height h:
$$h = \frac{1}{2}gt^2 \Rightarrow t_{fall} = \sqrt{\frac{2h}{g}}$$
$$v_{impact} = \sqrt{2gh}$$

---

## 4. Graphical Analysis of Motion

Reading and drawing motion graphs is a crucial skill. The three graphs — x(t), v(t), a(t) — contain the same information but display it differently.

### 4.1 The Three Graphs and Their Relationships

**From x(t) → v(t):** Slope of x(t) = v(t)
**From v(t) → a(t):** Slope of v(t) = a(t)
**From v(t) → Δx:** Area under v(t) = Δx
**From a(t) → Δv:** Area under a(t) = Δv

These are just the derivative and integral relationships, displayed geometrically.

### 4.2 Constant Acceleration Graphs

For motion with a = constant:

- **x(t):** Parabola (if a ≠ 0) or straight line (if a = 0)
- **v(t):** Straight line with slope = a
- **a(t):** Horizontal line at height a

### 4.3 Reading v(t) Graphs Fluently

The following must become second nature:

| Feature on v(t) graph | What it means |
|----------------------|---------------|
| v > 0 | Moving in +x direction |
| v < 0 | Moving in −x direction |
| v = 0 | Momentarily at rest |
| v crossing zero | Object reverses direction |
| Slope of v(t) > 0 | Positive acceleration |
| Slope of v(t) < 0 | Negative acceleration |
| Large |v| | Moving fast |
| v increasing in magnitude | Speeding up |
| v decreasing in magnitude | Slowing down |
| Area above t-axis | Positive displacement |
| Area below t-axis | Negative displacement |
| Net area (above − below) | Total displacement |
| Total area (|above| + |below|) | Total distance traveled |

---

## 5. Common Graphical Analysis Tasks

### Task 1: From x(t) graph, draw v(t)

At each time t, the instantaneous velocity equals the slope of x(t). Procedure:
1. Identify regions of constant slope (straight x(t)) → constant v sections
2. Identify curves → v is changing
3. Identify peaks/troughs/flat regions of x(t) → v = 0
4. Sketch v(t) accordingly

### Task 2: From v(t) graph, draw x(t)

1. Identify regions of constant v → x(t) is linear there
2. Identify regions of linearly changing v (constant a) → x(t) is parabolic there
3. Identify where v = 0 → x(t) has a local maximum or minimum
4. Compute areas to determine the net displacement

### Task 3: From v(t) graph, draw a(t)

1. Take the slope of each segment of v(t)
2. A linearly changing v segment → constant a (horizontal line on a(t) graph)
3. Instantaneous changes in slope on v(t) → discontinuities in a(t) — physically this means an impulsive force at that instant

---

## 6. Worked Examples

### Example 6.1 — Classic free fall

A stone is thrown upward from a bridge 45 m above a river with initial speed 12 m/s. Taking up as positive:

**(a) When does it hit the water?**
Use Δy = v₀t − ½gt² with Δy = −45 m (the water is 45 m below the launch point):
$$-45 = 12t - 4.9t^2$$
$$4.9t^2 - 12t - 45 = 0$$
$$t = \frac{12 \pm \sqrt{144 + 882}}{9.8} = \frac{12 \pm 32.03}{9.8}$$

t₁ = (12+32.03)/9.8 = **4.49 s** (physical — positive time)
t₂ = (12−32.03)/9.8 = −2.05 s (unphysical — before launch)

The stone hits the water at **t = 4.49 s**.

**(b) What is its speed on impact?**
v = v₀ − gt = 12 − 9.81(4.49) = 12 − 44.04 = **−32.0 m/s**

Speed = |−32.0| = **32.0 m/s** (the negative sign confirms it's moving downward at impact ✓)

**(c) What is the maximum height reached above the launch point?**
At the top, v = 0: Δy_max = v₀²/(2g) = 144/19.62 = **7.34 m above the launch point** (or 52.34 m above the water)

### Example 6.2 — Graphical analysis

A v(t) graph shows the following for an object's motion from t = 0 to t = 8 s:
- t = 0 to 2 s: v increases linearly from 0 to +6 m/s
- t = 2 to 4 s: v = +6 m/s (constant)
- t = 4 to 6 s: v decreases linearly from +6 to 0
- t = 6 to 8 s: v decreases linearly from 0 to −4 m/s

Find: (a) acceleration in each phase, (b) total displacement, (c) total distance.

**(a)** 
- Phase 1: a = (6−0)/2 = **+3 m/s²**
- Phase 2: a = 0/2 = **0 m/s²**
- Phase 3: a = (0−6)/2 = **−3 m/s²**
- Phase 4: a = (−4−0)/2 = **−2 m/s²**

**(b) Displacement = net area under v(t):**
- Phase 1: +½(2)(6) = +6 m
- Phase 2: +(2)(6) = +12 m
- Phase 3: +½(2)(6) = +6 m
- Phase 4: −½(2)(4) = −4 m
- **Total displacement = 6 + 12 + 6 − 4 = +20 m**

**(c) Distance = total area (ignoring signs):**
- Phases 1–3 are all positive: 6 + 12 + 6 = 24 m
- Phase 4 is negative (moving backward): 4 m
- **Total distance = 24 + 4 = 28 m**

---

## 7. Summary

| Concept | Key Point |
|---------|-----------|
| Free fall acceleration | a = −g = −9.81 m/s², constant, independent of mass |
| Sign convention | Choose once, use consistently throughout; up positive → a = −9.81 m/s² |
| Symmetry of free fall | t_up = t_down; speed at same height is same on way up and down |
| Slope of x(t) | Instantaneous velocity |
| Area under v(t) | Displacement (signed); need total area for distance |
| Slope of v(t) | Acceleration |
| Constant a | v(t) is linear, x(t) is parabolic, a(t) is horizontal |

---


---

## CS Connection — Graphical Analysis and Reading a Profiler

Extracting velocity from the slope of an x–t graph and displacement from the area under a v–t graph is the same skill as reading a performance profile: the derivative tells you the instantaneous rate, the integral tells you the accumulated total. Confusing the two — reading a rate as a total — is the most common misreading of both a motion graph and a flame graph.

---

## Looking Ahead

**L07** removes the restriction to one dimension — motion in a plane requires treating the components independently.

## Conceptual Questions

1. A ball is dropped from rest from a tall building. After falling for 1 s, it has speed v₁. After falling for 2 s, it has speed v₂. Is v₂ = 2v₁ (twice as fast) or v₂ = √2 · v₁ or something else? What about the distances fallen: is d₂ = 2d₁?

2. Two identical balls are launched from the same height at the same speed: one straight upward, one straight downward. Compare their speeds when they reach the ground. (Derive your answer — don't guess.)

3. An object has a v(t) graph that is a horizontal straight line at v = −5 m/s. Describe the motion in words. What does the x(t) graph look like? What does the a(t) graph look like?

4. An object's a(t) graph is zero from t = 0 to t = 2 s, then jumps instantaneously to a = +4 m/s² from t = 2 s onward. The object starts from rest at x = 10 m. Sketch x(t), v(t), and a(t) for 0 ≤ t ≤ 5 s.
