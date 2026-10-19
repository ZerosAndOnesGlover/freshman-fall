---
assessment: PS 3
course: PHYS 141
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-16
submitted: 2026-10-23
graded: 2026-10-24
source: "PS 3 Newtons Three Laws of Motion.md"
---

# PHYS 141 · Problem Set 3
## Newton's Three Laws of Motion

**Assessment:** `PS 3 Newtons Three Laws of Motion.md`
**Released:** Friday 16 October 2026 · **Due:** Friday 23 October 2026, 17:00
**Points:** 100

> **Renumbering note:** the instructor solutions keep an older lettering (4 sub-parts per problem).
> I follow the revised two-part numbering printed on the handout. Mapping of the sub-parts I use:
> 1(a,b)=(c,d) · 2(a,b)=(b,e) · 3(a,b)=(c,d) · 4(a,b)=(c,d) · 5(a,b)=(a,b) ·
> 6(a,b)=(a,c) · 7(a,b)=(b,d) · 8(a,b)=(d,e) · 9(a,b)=(a,c) · 10(a,b)=(b,c).

---

## Part A — Newton's First and Second Laws (30 pts)

### Problem 1 — Car acceleration and braking (10 pts)
$a=\frac{\Delta v}{t}=\frac{25-0}{8.0}=3.125\ \text{m/s}^2$.

**(a)** $F_{\text{net}}=ma=1200\times3.125=3750\ \text{N}$. With engine force $5500$ N forward,
$F_{\text{friction}}=5500-3750=\boxed{1750\ \text{N}}$ opposing motion.

**(b)** Braking: $a=\frac{0-25}{5.0}=-5.0\ \text{m/s}^2$. $F_{\text{brake}}=ma=1200\times5.0=\boxed{6000\ \text{N}}$ opposing motion.

*Marks: 10 / 10*

---

### Problem 2 — Person on a scale in an elevator (10 pts)
$\Sigma F_y=N-mg=ma$; the scale reads the normal force $N$.

**(a)** $a=+2.5\ \text{m/s}^2$ (up):
$N=m(g+a)=70(9.81+2.5)=70\times12.31=\boxed{862\ \text{N}}$ — the person feels heavier.

**(b)** Free fall, cable snapped: $a=-g$, so $N=m(g-g)=\boxed{0\ \text{N}}$. The scale reads **0 N**; the person feels **weightless**, floating as if in orbit — no contact force acts on them.

*Marks: 10 / 10*

---

### Problem 3 — Ball suspended by two strings (10 pts)
$W=mg=0.50\times9.81=4.905\ \text{N}$. Let $T_1$ = tension in the **left** string (30° from vertical), $T_2$ = **right** string (60° from vertical).

**(a)** Equilibrium, $\Sigma F_x=0$: $T_2\sin60^\circ=T_1\sin30^\circ$; $\Sigma F_y=0$: $T_1\cos30^\circ+T_2\cos60^\circ=mg$.
$T_1=T_2\frac{\sin60^\circ}{\sin30^\circ}=1.732T_2$. Substituting: $1.732T_2(0.866)+T_2(0.500)=4.905\Rightarrow2.000T_2=4.905$.
$T_2=\boxed{2.45\ \text{N}}$, $T_1=1.732\times2.45=\boxed{4.24\ \text{N}}$.

**(b)** As the right string's angle from vertical increases toward 90°, $\cos60^\circ\to0$: the string becomes nearly **horizontal** and its vertical component of tension vanishes. To still balance $mg$ while staying horizontal the tension must blow up — $T_2\to\infty$. Physically: a perfectly horizontal cable **cannot** support a vertical load; there is no finite tension that does so. This is why suspension cables are always angled.

*Marks: 10 / 10*

---

## Part B — Newton's Third Law (20 pts)

### Problem 4 — Astronaut pushes a satellite (10 pts)
**(a)** $F=m_{\text{sat}}a_{\text{sat}}=200\times0.50=100\ \text{N}$. By Newton's Third Law the satellite pushes the astronaut back with $100$ N.
$a_{\text{astronaut}}=\frac{F}{m_{\text{astro}}}=\frac{100}{60}=\boxed{1.67\ \text{m/s}^2}$, **opposite** in direction to the satellite's motion.

**(b)** After $t=2.0$ s from rest (initial separation 0):
$d_{\text{sat}}=\frac12 a_{\text{sat}}t^2=\frac12(0.50)(4)=1.0\ \text{m}$; $d_{\text{astro}}=\frac12(1.67)(4)=3.33\ \text{m}$ in the opposite direction.
Separation $=1.0+3.33=\boxed{4.33\ \text{m}}$.

*Marks: 10 / 10*

---

### Problem 5 — Car tows a trailer (10 pts)
**(a)** Whole system $2000$ kg; net drive $=4000-(600+200)=3200$ N.
$a=\frac{3200}{2000}=\boxed{1.60\ \text{m/s}^2}$.

**(b)** Isolate the **trailer** ($500$ kg): only $T$ forward and $200$ N resistance back.
$\Sigma F=T-200=500\times1.60\Rightarrow T=800+200=\boxed{1000\ \text{N}}$.

*Marks: 10 / 10*

---

## Part C — Friction (20 pts)

### Problem 6 — 15 kg box on a horizontal surface (10 pts)
$N=mg=15\times9.81=147.2\ \text{N}$.

**(a)** Minimum force to start sliding $=f_{s,\max}=\mu_sN=0.45\times147.2=\boxed{66.2\ \text{N}}$.

**(b)** While sliding, $f_k=\mu_kN=0.30\times147.2=44.1$ N. With $100$ N applied:
$a=\frac{100-44.1}{15}=\frac{55.9}{15}=\boxed{3.73\ \text{m/s}^2}$.

*Marks: 10 / 10*

---

### Problem 7 — 4.0 kg block on a 38° incline (10 pts)
$N=mg\cos38^\circ=4.0\times9.81\times0.788=30.9$ N. $mg\sin38^\circ=4.0\times9.81\times0.616=24.2$ N. $f_{s,\max}=\mu_sN=0.50\times30.9=15.5$ N.

**(a)** $24.2\ \text{N}>15.5\ \text{N}$, so the block **slides**. $f_k=0.35\times30.9=10.8$ N.
$a=\frac{mg\sin38^\circ-f_k}{m}=\frac{24.2-10.8}{4.0}=\frac{13.4}{4.0}=\boxed{3.35\ \text{m/s}^2}$ down the slope.

**(b)** Pushing up at constant velocity: gravity component **down** the slope plus kinetic friction **down** the slope must balance the applied force **up** the slope.
$F=mg\sin\theta+\mu_kmg\cos\theta=39.24(0.616+0.35\times0.788)=39.24\times0.892=\boxed{35.0\ \text{N}}$ up the slope.

*Marks: 10 / 10*

---

## Part D — Connected Systems and Inclines (30 pts)

### Problem 8 — Atwood machine, $m_1=3.0$ kg, $m_2=5.0$ kg (10 pts)
**(a)** $v^2=2a\Delta y=2(2.45)(2.0)=9.80\Rightarrow v=\boxed{3.13\ \text{m/s}}$ when $m_2$ has fallen $2.0$ m.

**(b)** With the string broken: $m_2$ is already moving **down** at $3.13$ m/s → continues in **free fall** ($a=-g$). $m_1$ is moving **up** at $3.13$ m/s → becomes a **projectile**: it decelerates at $g$, reaches a max height, then falls back up to where it started.

*Marks: 10 / 10*

---

### Problem 9 — 6.0 kg block on 40° incline + 4.0 kg hanging mass, frictionless (10 pts)
Component of $m_1$'s weight along incline (down): $m_1g\sin40^\circ=6.0\times9.81\times0.643=37.8$ N. Hanging weight $m_2g=4.0\times9.81=39.2$ N.

**(a)** $39.2>37.8$ → the **hanging mass pulls the block up the incline**.

**(b)** Block up-slope positive: $T-m_1g\sin40^\circ=m_1a$ → $T-37.8=6.0a$. Hanging mass (down positive): $m_2g-T=m_2a$ → $39.2-T=4.0a$. Adding: $1.4=10.0a\Rightarrow a=\boxed{0.14\ \text{m/s}^2}$. $T=37.8+6.0(0.14)=\boxed{38.6\ \text{N}}$.

*Marks: 10 / 10*

---

### Problem 10 — Double incline (A-frame), $m_L=2.0$ kg @ 30°, $m_R=5.0$ kg @ 50° (10 pts)
Gravity along slope: left $=2.0\times9.81\times\sin30^\circ=9.81$ N; right $=5.0\times9.81\times\sin50^\circ=37.6$ N.

**(a)** $37.6>9.81$ → the **right block slides down and pulls the left block up**.
Right block down-slope positive: $37.6-T=5.0a$. Left block up-slope positive: $T-9.81=2.0a$. Adding: $27.79=7.0a\Rightarrow a=\boxed{3.97\ \text{m/s}^2}$.

**(b)** $T=9.81+2.0(3.97)=9.81+7.94=\boxed{17.8\ \text{N}}$.

*Marks: 10 / 10*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-24 |

| Part | Problems | Marks |
|---|---|---|
| A — Newton's First and Second Laws | 1–3 | 30 / 30 |
| B — Newton's Third Law | 4–5 | 20 / 20 |
| C — Friction | 6–7 | 20 / 20 |
| D — Connected Systems and Inclines | 8–10 | 30 / 30 |
| **Total** | | **100 / 100** |

**Feedback:** All ten problems correct with labelled free-body reasoning, explicit coordinate choices, and symbolic setup before numbers. Key physics handled well: normal force ≠ mg in the elevator (2); third-law pairs kept on separate bodies (4); $f_s\le\mu_sN$ used only as a bound (6, 7); massless-string tension transmitted uniformly (8, 10). The $T\to\infty$ limit as a string becomes horizontal (3b) and the free-fall vs. projectile split after the string breaks (8b) are correctly identified.

---
*PHYS 141 · Week 3 · PS 3 · Adebayo Glover*
