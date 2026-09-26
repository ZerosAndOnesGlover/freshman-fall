# MATH 141 · Problem Set 11 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-21 out of the student handout, where it had been printed below the questions.*

---

*Every value below verified by numerical integration.*

*(Revised 2026-09-26 to match the 9-problem set; items are numbered as in the new set.)*

### Problem 1 — Area Between Curves (10)

Intersections at $x=\pm2$. $A=\int_{-2}^{2}(8-2x^2)dx=\mathbf{\tfrac{64}{3}}\approx21.33$
*(verified $21.3333333333$)*. Even integrand — halve the work by symmetry.

### Problem 2 — Integrating in y (14)

$y^2=y+2\Rightarrow(y-2)(y+1)=0\Rightarrow y=-1,2$. The line is to the right:

$$A=\int_{-1}^{2}\big[(y+2)-y^2\big]dy=\mathbf{\tfrac92}$$ *(verified $4.5$)*

**Why $x$ needs two integrals:** the lower boundary changes at $x=1$ — it is the lower branch
$y=-\sqrt x$ for $0\le x\le1$, then the line $y=x-2$ for $1\le x\le4$. Horizontally, the right
boundary is the line and the left the parabola throughout. *(5 of the 14 marks.)*

### Problem 3 — A Disk Volume (10)

$V=\pi\int_0^2x^4dx=\mathbf{\tfrac{32\pi}{5}}\approx20.11$ *(verified $20.10619298$)*

### Problem 4 — The Cone (12)

Revolve $y=\tfrac rh x$ on $[0,h]$:
$V=\pi\tfrac{r^2}{h^2}\int_0^hx^2dx=\mathbf{\tfrac13\pi r^2h}$ *(verified at $r=h=3$: $9\pi=28.274$)*

### Problem 5 — Known Cross-Sections (12)

Side $=2\sqrt{4-x^2}$ — the **full chord**, above and below the axis. So $A(x)=4(4-x^2)$ and

$$V=\int_{-2}^{2}4(4-x^2)dx=\mathbf{\tfrac{128}{3}}\approx42.67$$ *(verified $42.66666667$)*

*Using $\sqrt{4-x^2}$ as the side gives $32/3$ — a quarter of the answer. 5 of the 12 marks are for
identifying the full chord.*

### Problem 6 — Shells (10)

$V=2\pi\int_0^3x^3dx=\mathbf{\tfrac{81\pi}{2}}\approx127.23$ *(verified $127.234502$)*

### Problem 7 — Shells Again (10)

$V=2\pi\int_0^4x^{3/2}dx=\mathbf{\tfrac{128\pi}{5}}\approx80.42$ *(verified $80.424772$)*

### Problem 8 — Work (12)

$W=\int_0^{0.3}200x\,dx=100(0.09)=\mathbf 9$ J *(verified $9.000000$)*.
General: $W=\tfrac12kd^2$.

### Problem 9 — One Idea, Four Uses (10)



| Application | One slice contributes |
|---|---|
| Area between curves | A rectangle, height $(f-g)$, width $\Delta x$ |
| Volume by disks | A disk of area $\pi f(x)^2$, thickness $\Delta x$ |
| Volume by shells | A shell, circumference $2\pi x$, height $f(x)$, thickness $\Delta x$ |
| Displacement | Distance $v(t)\Delta t$ over a short time |

**What they share:** each treats the quantity as **constant across a thin slice**, sums the slices,
and takes the limit as the thickness $\to0$ — which is the definition of the definite integral.

*4 of the 10 marks are for the final sentence. The formulas are interchangeable trivia; the
construction is the content.*

---

*MATH 141 · Week 11 · Problem Set 11 · © CSE Department*
