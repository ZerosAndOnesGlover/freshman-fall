# MATH 141 · Problem Set 11 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-21 out of the student handout, where it had been printed below the questions.*

---

*Every value below verified by numerical integration.*

### Part A

**A1.** On $(0,1)$, $x^2>x^3$. $A=\int_0^1(x^2-x^3)dx=\tfrac13-\tfrac14=\mathbf{\tfrac{1}{12}}$
*(verified $0.0833333333$)*.

*The trap is assuming $x^3>x^2$ from the exponent. On $(0,1)$ higher powers are smaller.*

**A2.** Intersections at $x=\pm2$. $A=\int_{-2}^{2}(8-2x^2)dx=\mathbf{\tfrac{64}{3}}\approx21.33$
*(verified $21.3333333333$)*. Even integrand — halve the work by symmetry.

**A3.** Cross at $x=\pi/4$.

$$A=\int_0^{\pi/4}(\cos x-\sin x)dx+\int_{\pi/4}^{\pi/2}(\sin x-\cos x)dx=\mathbf{2(\sqrt2-1)}\approx0.8284$$

*(verified $0.8284271247$)*

**Why the split is necessary:** without it the single integral $\int_0^{\pi/2}(\sin x-\cos x)dx$
evaluates to **exactly 0** — verified — because the two equal regions cancel. A visibly non-empty
region with area zero is always a missing split.

*4 of the 8 marks are for this explanation.*

**A4.** $y^2=y+2\Rightarrow(y-2)(y+1)=0\Rightarrow y=-1,2$. The line is to the right:

$$A=\int_{-1}^{2}\big[(y+2)-y^2\big]dy=\mathbf{\tfrac92}$$ *(verified $4.5$)*

**Why $x$ needs two integrals:** the lower boundary changes at $x=1$ — it is the lower branch
$y=-\sqrt x$ for $0\le x\le1$, then the line $y=x-2$ for $1\le x\le4$. Horizontally, the right
boundary is the line and the left the parabola throughout. *(4 of the 10 marks.)*

### Part B

**B1.** $V=\pi\int_0^2x^4dx=\mathbf{\tfrac{32\pi}{5}}\approx20.11$ *(verified $20.10619298$)*

**B2.** $\sqrt x$ is outer on $(0,1)$:
$V=\pi\int_0^1(x-x^2)dx=\mathbf{\tfrac{\pi}{6}}\approx0.524$ *(verified $0.52359878$)*

*Award 0 for $\pi\int(\sqrt x-x)^2dx$, which gives $\pi/30\approx0.1047$ — verified, and wrong by a
factor of 5. Square each radius **before** subtracting.*

**B3.** Revolve $y=\tfrac rh x$ on $[0,h]$:
$V=\pi\tfrac{r^2}{h^2}\int_0^hx^2dx=\mathbf{\tfrac13\pi r^2h}$ *(verified at $r=h=3$: $9\pi=28.274$)*

**B4.** Side $=2\sqrt{4-x^2}$ — the **full chord**, above and below the axis. So $A(x)=4(4-x^2)$ and

$$V=\int_{-2}^{2}4(4-x^2)dx=\mathbf{\tfrac{128}{3}}\approx42.67$$ *(verified $42.66666667$)*

*Using $\sqrt{4-x^2}$ as the side gives $32/3$ — a quarter of the answer. 3 of the 8 marks are for
identifying the full chord.*

### Part C

**C1.** $V=2\pi\int_0^3x^3dx=\mathbf{\tfrac{81\pi}{2}}\approx127.23$ *(verified $127.234502$)*

**C2.** $V=2\pi\int_0^4x^{3/2}dx=\mathbf{\tfrac{128\pi}{5}}\approx80.42$ *(verified $80.424772$)*

**C3.** **Shells:** $2\pi\int_0^2x^3dx=8\pi$.
**Washers in $y$:** outer radius $2$, inner $\sqrt y$, so $\pi\int_0^4(4-y)dy=8\pi$.

Both give $\mathbf{8\pi\approx25.133}$ — verified identically as $25.13274123$ by each route.

*Marking: 5 for each method, 2 for the comparison. Most students find shells easier because no
inversion is needed; accept either preference if justified. The agreement of two genuinely different
set-ups is the best available check on a hard volume, and saying so earns the final 2.*

### Part D

**D1.** $W=\int_0^{0.3}200x\,dx=100(0.09)=\mathbf 9$ J *(verified $9.000000$)*.
General: $W=\tfrac12kd^2$.

**D2.**

| Application | One slice contributes |
|---|---|
| Area between curves | A rectangle, height $(f-g)$, width $\Delta x$ |
| Volume by disks | A disk of area $\pi f(x)^2$, thickness $\Delta x$ |
| Volume by shells | A shell, circumference $2\pi x$, height $f(x)$, thickness $\Delta x$ |
| Displacement | Distance $v(t)\Delta t$ over a short time |

**What they share:** each treats the quantity as **constant across a thin slice**, sums the slices,
and takes the limit as the thickness $\to0$ — which is the definition of the definite integral.

*3 of the 7 marks are for the final sentence. The formulas are interchangeable trivia; the
construction is the content.*

---

*MATH 141 · Week 11 · Problem Set 11 · © CSE Department*
