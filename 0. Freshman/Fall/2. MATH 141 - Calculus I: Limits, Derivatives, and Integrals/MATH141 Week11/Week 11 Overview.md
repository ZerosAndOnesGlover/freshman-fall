# MATH 141 — Week 11 Overview
## Applications of Integration

---

## This Week

Weeks 8–10 built the integral and the tools to evaluate it. This week spends it. Every application
below is the **same construction** — slice, approximate, sum, take the limit — and recognising that
is the point of the week, not memorising four formulas.

| Day | Lecture | Topic |
|---|---|---|
| Monday | 1 | Area Between Curves |
| Tuesday | 2 | Volumes by Slicing: Disks and Washers |
| Wednesday | 3 | Cylindrical Shells, and Accumulation Revisited |
| — | Lab 11 | Areas, Volumes, and Numerical Checks |

**Quiz 11** at the start of Monday's lecture, covering Week 10.
**Problem Set 11** due Wednesday of Week 12.

---

## Learning Objectives

1. Compute the area between two curves, splitting correctly where they cross
2. Choose between $dx$ and $dy$ slicing, and justify the choice
3. Compute volumes of revolution by disks, washers and shells
4. Choose the method that avoids inverting the function
5. Set up volumes for solids with non-circular cross-sections
6. Recognise every application as one construction: slice → approximate → sum → limit

---

## Key Results

| | |
|---|---|
| Area between curves | $\int_a^b(\text{top}-\text{bottom})\,dx$ |
| Curves that cross | **Split at every crossing** — or integrate $\lvert f-g\rvert$ |
| Horizontal slices | $\int_c^d(\text{right}-\text{left})\,dy$ |
| General volume | $V=\int_a^b A(x)\,dx$ |
| Disks | $V=\pi\int f(x)^2dx$ |
| Washers | $V=\pi\int\big[R_{\text{out}}^2-R_{\text{in}}^2\big]dx$ |
| Shells | $V=2\pi\int x\,f(x)\,dx$ |
| Shifted axis | Radius is the **distance** to the axis |

---

## Common Errors

| Error | Correction |
|---|---|
| One integral across a crossing | Verified to give **0** for $\sin$ vs $\cos$ on $[0,\pi/2]$ — split at $\pi/4$ |
| $\int(R_o-R_i)^2$ | Square **first**, then subtract: $\int(R_o^2-R_i^2)$ |
| Using $f(x)$ as radius about $y=c$ | Radius is $\lvert f(x)-c\rvert$ |
| Half-chord as a square's side | The square spans the **full** chord |
| Assuming $x^3>x^2$ | False on $(0,1)$ — sketch first |

---

## Connections

**Back:** Week 8's signed-area interpretation and symmetry properties; Week 9's FTC, which makes
every integral here evaluable; Week 4's displacement-vs-distance, which reappears as "split where the
curves cross".

**Forward:** MATH 142 adds arc length, surface area and improper integrals. PHYS 141 uses slicing for
work, centre of mass and moments. MATH 341 handles the integrals with no closed form.

---

*MATH 141 · Week 11 · © CSE Department*
