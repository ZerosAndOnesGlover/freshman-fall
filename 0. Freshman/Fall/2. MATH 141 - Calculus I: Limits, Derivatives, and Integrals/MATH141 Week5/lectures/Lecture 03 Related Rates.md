# MATH 141 · Calculus I
## Week 5 · Lecture 3 (Wednesday)
### Related Rates

---

**Reading:** Stewart §3.9 | Spivak Ch. 11 (applications of differentiation)
**Problem Set 5 released today. Due: Wednesday, Week 4.**

---

## 1. What Are Related Rates?

When two or more quantities are related by an equation and both change with time, their **rates of change** are also related. Related rates problems use implicit differentiation with respect to time $t$ to connect these rates.

**The core idea:** If $A$ and $B$ are related by $f(A, B) = 0$, then differentiating with respect to $t$ gives a relationship between $\frac{dA}{dt}$ and $\frac{dB}{dt}$.

---

## 2. Problem-Solving Strategy

1. **Draw a diagram** — label all quantities that change with time as variables
2. **Identify** what rate is given and what rate is wanted
3. **Write an equation** relating the relevant quantities (geometry, physics, similar triangles, etc.)
4. **Differentiate both sides** with respect to $t$ (implicit differentiation — chain rule throughout)
5. **Substitute** known values and solve for the unknown rate
6. **Check units and sign** — negative rate means decreasing

> ⚠️ **Critical error to avoid:** Do NOT substitute the given values for the variables before differentiating. The variables must remain as variables during differentiation. Substitute only after you have an equation relating the rates.

---

## 3. Worked Examples

### Example 1 — Expanding Circle

Air is pumped into a spherical balloon so its volume increases at $100\ \text{cm}^3/\text{s}$. How fast is the radius increasing when the radius is $5\ \text{cm}$?

**Given:** $\dfrac{dV}{dt} = 100\ \text{cm}^3/\text{s}$ when $r = 5\ \text{cm}$. **Find:** $\dfrac{dr}{dt}$.

**Equation:** $V = \dfrac{4}{3}\pi r^3$

**Differentiate with respect to $t$:**
$$\frac{dV}{dt} = 4\pi r^2 \frac{dr}{dt}$$

**Substitute and solve:**
$$100 = 4\pi(5)^2 \frac{dr}{dt} = 100\pi \frac{dr}{dt}$$

$$\frac{dr}{dt} = \frac{1}{\pi} \approx 0.318\ \text{cm/s}$$

**Interpretation:** The radius grows more slowly as the balloon expands — the same volume increase spreads over a larger surface area.

---

### Example 2 — Sliding Ladder

A 10-meter ladder leans against a wall. The bottom slides away from the wall at $2\ \text{m/s}$. How fast is the top sliding down when the bottom is $6\ \text{m}$ from the wall?

**Variables:** $x$ = distance of bottom from wall, $y$ = height of top on wall. Both change with $t$.

**Given:** $\dfrac{dx}{dt} = 2\ \text{m/s}$ when $x = 6\ \text{m}$. **Find:** $\dfrac{dy}{dt}$.

**Equation:** $x^2 + y^2 = 100$

When $x = 6$: $y = \sqrt{100-36} = 8\ \text{m}$.

**Differentiate with respect to $t$:**
$$2x\frac{dx}{dt} + 2y\frac{dy}{dt} = 0$$

**Substitute:**
$$2(6)(2) + 2(8)\frac{dy}{dt} = 0 \implies 24 + 16\frac{dy}{dt} = 0$$

$$\frac{dy}{dt} = -\frac{24}{16} = -\frac{3}{2}\ \text{m/s}$$

**Interpretation:** The top slides down at $1.5\ \text{m/s}$. The negative sign confirms it is moving downward (decreasing $y$).

---

### Example 3 — Conical Water Tank

Water drains from a conical tank (vertex down) at $2\ \text{m}^3/\text{min}$. The tank has height $H = 4\ \text{m}$ and radius $R = 2\ \text{m}$ at the top. How fast is the water level falling when the water is $3\ \text{m}$ deep?

**Variables:** $h$ = water depth, $r$ = surface radius. Both change. $V$ = volume of water.

**Given:** $\dfrac{dV}{dt} = -2\ \text{m}^3/\text{min}$ (negative — draining). $h = 3\ \text{m}$. **Find:** $\dfrac{dh}{dt}$.

**Key step — eliminate $r$:** By similar triangles, $\dfrac{r}{h} = \dfrac{R}{H} = \dfrac{2}{4} = \dfrac{1}{2}$, so $r = \dfrac{h}{2}$.

**Equation:** $V = \dfrac{1}{3}\pi r^2 h = \dfrac{1}{3}\pi\left(\dfrac{h}{2}\right)^2 h = \dfrac{\pi h^3}{12}$

**Differentiate with respect to $t$:**
$$\frac{dV}{dt} = \frac{\pi}{12}\cdot 3h^2\frac{dh}{dt} = \frac{\pi h^2}{4}\frac{dh}{dt}$$

**Substitute $dV/dt = -2$ and $h = 3$:**
$$-2 = \frac{\pi(9)}{4}\frac{dh}{dt}$$

$$\frac{dh}{dt} = \frac{-8}{9\pi} \approx -0.283\ \text{m/min}$$

**Key insight:** The similar-triangles step reduced two variables ($r$ and $h$) to one. Always reduce to one variable before differentiating when possible.

---

### Example 4 — Angle of Elevation

A person stands $30\ \text{m}$ from the base of a building and watches a window washer descend. When the washer is $40\ \text{m}$ above ground and descending at $1.5\ \text{m/s}$, how fast is the angle of elevation changing?

**Variables:** $y$ = height of washer, $\theta$ = angle of elevation. Both change.

**Given:** $\dfrac{dy}{dt} = -1.5\ \text{m/s}$ when $y = 40\ \text{m}$. **Find:** $\dfrac{d\theta}{dt}$.

**Equation:** $\tan\theta = \dfrac{y}{30}$

**Differentiate with respect to $t$:**
$$\sec^2\theta\,\frac{d\theta}{dt} = \frac{1}{30}\frac{dy}{dt}$$

At $y = 40$: $\tan\theta = 40/30 = 4/3$, so $\sec^2\theta = 1 + \tan^2\theta = 1 + 16/9 = 25/9$.

$$\frac{25}{9}\,\frac{d\theta}{dt} = \frac{1}{30}(-1.5) = -\frac{1}{20}$$

$$\frac{d\theta}{dt} = -\frac{9}{25\cdot20} = -\frac{9}{500}\ \text{rad/s}$$

---

### Example 5 — Two Ships (Pythagorean Setup)

At noon, ship A is 100 km west of ship B. Ship A sails north at 35 km/h, ship B sails south at 25 km/h. How fast is the distance between them increasing at 4:00 PM?

**At 4:00 PM:** Ship A has traveled $35 \times 4 = 140$ km north. Ship B has traveled $25 \times 4 = 100$ km south.

**Set up coordinates:** Let $y$ = total north-south separation (A above B). $y = 140 + 100 = 240$ km. Horizontal separation is always $x = 100$ km.

**Equation:** $D^2 = x^2 + y^2 = 100^2 + y^2$

At 4 PM: $D = \sqrt{10000 + 57600} = \sqrt{67600} = 260$ km.

**Given:** $x = 100$ (constant, so $dx/dt = 0$). $\dfrac{dy}{dt} = 35 + 25 = 60\ \text{km/h}$ (both ships moving away from each other vertically).

**Differentiate:** $2D\dfrac{dD}{dt} = 2y\dfrac{dy}{dt}$

$$\frac{dD}{dt} = \frac{y}{D}\cdot\frac{dy}{dt} = \frac{240}{260}\cdot 60 = \frac{144000}{260} = \frac{7200}{13} \approx 553.8\ \text{km/h}$$

---

## 4. General Principles

**Setting up the geometry equation** is the hardest step. Common tools:

| Geometry | Equation |
|----------|----------|
| Right triangle | Pythagorean theorem, trig ratios |
| Similar triangles | Proportional sides |
| Circle | Area $= \pi r^2$, circumference $= 2\pi r$ |
| Sphere | $V = \frac{4}{3}\pi r^3$, $SA = 4\pi r^2$ |
| Cone | $V = \frac{1}{3}\pi r^2 h$ |
| Cylinder | $V = \pi r^2 h$ |
| Law of cosines | $c^2 = a^2 + b^2 - 2ab\cos C$ |

**When two variables appear**, look for a geometric constraint to eliminate one before differentiating (similar triangles, constant sum/product, etc.).

---

## 5. CS Connection — Rate Equations in Systems

Related rates are rate equations — differential equations in disguise. $\dfrac{dV}{dt} = f(r)\dfrac{dr}{dt}$ is a simple ODE. More complex systems:

- **Network flow:** Kirchhoff's laws relate rates of current flow — same structure as related rates
- **Queueing theory:** The rate of queue length change depends on arrival rate minus service rate
- **Control systems:** PID controllers work by relating the rate of error change to corrective action

The mathematical structure — implicit differentiation of a constraint with respect to time — is the foundation of **dynamical systems**, which model everything from population growth to circuit behavior to game physics engines.

---

## 6. The Two Errors That Account for Most Lost Marks

**1. Substituting numerical values before differentiating.**

This is the dominant error in related rates, and it is fatal rather than merely costly. Consider
the ripple problem: if you write $A = \pi(3)^2$ *before* differentiating, you have declared the
radius to be the constant 3, and $dA/dt$ comes out as $0$ — the area of a fixed circle does not
change.

> **Rule: every quantity that varies stays a symbol until after $\frac{d}{dt}$ has been applied.**
> Substitute the instantaneous values only in the final step. The only things you may substitute
> early are genuine constants — the radius of a *fixed* tank, the length of a *rigid* ladder.

A useful discipline is to write the relation with explicit time-dependence the first time:
$A(t) = \pi\,[r(t)]^2$. The chain rule then writes itself.

**2. Not identifying which rate is given and which is wanted.**

Before any calculus, write two lines:

```
GIVEN:  dr/dt = 4 m/s
WANT:   dA/dt  when r = 3 m
RELATE: A = pi r^2
```

Most wrong answers are already wrong at this stage — students differentiate a correct relation with
respect to the wrong variable, or solve for the rate they were handed. The "RELATE" line is the
only creative step; everything after it is mechanical.

---

## 7. Choosing the Relating Equation

The relation must connect the variable whose rate you *know* to the one whose rate you *want*, and
must hold **for all time**, not just at the instant of interest.

| Situation | Relation |
|---|---|
| Circle / ripple | $A=\pi r^2$, $C=2\pi r$ |
| Right triangle (ladder, kite, cars) | $a^2+b^2=c^2$ |
| Similar triangles (shadows) | ratio of corresponding sides |
| Cone draining | $V=\tfrac13\pi r^2h$, plus $r/h$ fixed by the cone's shape |
| Cylinder filling | $V=\pi r^2h$ with $r$ **constant** |

The cone is the one worth flagging: $V=\tfrac13\pi r^2h$ has *two* varying quantities, so you must
eliminate one using the fixed ratio $r/h = R/H$ before differentiating. Differentiating with both
left in gives a correct but unusable equation containing two unknown rates.

---

## Lecture 3 Exercises

1. A stone is dropped into a calm pond, creating ripples. The radius of the outer ripple increases at $4\ \text{m/s}$. How fast is the enclosed area increasing when the radius is $3\ \text{m}$?

2. A 2-meter tall person walks away from a 6-meter streetlight at $1.5\ \text{m/s}$. How fast is the length of their shadow increasing?
   *(Hint: use similar triangles to relate shadow length to distance from the lamp.)*

3. A particle moves along the curve $y = \sqrt{x}$. When the particle is at $(4, 2)$, its $x$-coordinate is increasing at $3\ \text{units/s}$. How fast is the $y$-coordinate increasing?

4. Two cars start from the same intersection. Car A drives north at $60\ \text{km/h}$, Car B drives west at $80\ \text{km/h}$. How fast is the distance between them increasing after $30\ \text{minutes}$?

5. Water is poured into a cylindrical tank of radius $3\ \text{m}$ at $2\ \text{m}^3/\text{min}$. Simultaneously, water drains from the bottom at $0.5\ \text{m}^3/\text{min}$. How fast is the water level rising?

6. **(Hard)** A kite is flying at a height of $80\ \text{m}$ and moving horizontally away from the person holding it at $4\ \text{m/s}$. How fast is the string being let out when $100\ \text{m}$ of string has been released? *(Assume the string is taut and the kite stays at constant height.)*

---

### Answers

**1. Ripple.** GIVEN $dr/dt=4$; WANT $dA/dt$ at $r=3$; RELATE $A=\pi r^2$.
$$\frac{dA}{dt} = 2\pi r\frac{dr}{dt} = 2\pi(3)(4) = \boxed{24\pi \approx 75.4\ \text{m}^2/\text{s}}$$

**2. Shadow.** Let $x$ = distance from the lamp's base, $s$ = shadow length. Similar triangles give
$\dfrac{6}{x+s} = \dfrac{2}{s}$, hence $6s = 2x+2s$ and $\boxed{s = x/2}$.

$$\frac{ds}{dt} = \frac12\frac{dx}{dt} = \frac12(1.5) = \boxed{0.75\ \text{m/s}}$$

Note the answer is **independent of position** — the shadow lengthens at a constant rate no matter
how far away the walker is, because the relation is linear. Students often expect a
position-dependent answer and distrust this one. A frequent variant asks for the speed of the
shadow's *tip*, which is $\frac{d}{dt}(x+s) = 1.5+0.75 = 2.25$ m/s — a different question with a
different answer, so read carefully.

**3. Particle on $y=\sqrt x$.** $\dfrac{dy}{dt} = \dfrac{1}{2\sqrt x}\dfrac{dx}{dt}
= \dfrac{1}{2(2)}(3) = \boxed{0.75\ \text{units/s}}$

**4. Two cars.** After $30$ min: $a=30$ km north, $b=40$ km west, $D=\sqrt{30^2+40^2}=50$ km.
From $D^2=a^2+b^2$:
$$2D\frac{dD}{dt} = 2a\frac{da}{dt}+2b\frac{db}{dt}
\Rightarrow \frac{dD}{dt} = \frac{30(60)+40(80)}{50} = \frac{5000}{50} = \boxed{100\ \text{km/h}}$$

Worth noticing: $100 = \sqrt{60^2+80^2}$. Because both cars travel in fixed perpendicular
directions at constant speed, the separation grows at the constant rate given by the speeds'
resultant — the answer does not depend on the 30 minutes at all.

**5. Cylinder.** Net inflow $= 2-0.5 = 1.5\ \text{m}^3/\text{min}$. With $r=3$ **fixed**,
$V=\pi r^2 h = 9\pi h$, so
$$\frac{dh}{dt} = \frac{1}{9\pi}\frac{dV}{dt} = \frac{1.5}{9\pi} = \boxed{\frac{1}{6\pi}\approx 0.053\ \text{m/min}}$$

The radius is a constant here — this is exactly the case where early substitution is *legitimate*.
Contrast with a cone, where the radius varies with the height.

**6. Kite.** Height $80$ fixed, $x^2+80^2=L^2$. At $L=100$: $x=\sqrt{10000-6400}=60$.
$$2x\frac{dx}{dt} = 2L\frac{dL}{dt} \Rightarrow \frac{dL}{dt} = \frac{x}{L}\frac{dx}{dt}
= \frac{60}{100}(4) = \boxed{2.4\ \text{m/s}}$$

The string is let out **more slowly than the kite moves horizontally**, and always will be: the
factor $x/L = \cos\theta < 1$. Only the component of the kite's velocity *along the string*
lengthens it — the perpendicular component swings the kite around instead. As the kite flies
further out, $x/L \to 1$ and the two rates converge.

---

*Reading for Week 4: Stewart §4.1–4.2 (max/min, Rolle's theorem, MVT)*
*Problem Set 5 released today — see assignment file.*
