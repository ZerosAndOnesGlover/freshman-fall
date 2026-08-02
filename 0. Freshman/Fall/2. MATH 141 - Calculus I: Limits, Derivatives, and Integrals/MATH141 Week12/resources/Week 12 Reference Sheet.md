# MATH 141 · Week 12 Reference Sheet
## Course Summary and Final Exam Aid

---

## The Structure

$$\text{limits} \;\longrightarrow\; \text{derivatives} \;\underset{\text{FTC}}{\longleftrightarrow}\; \text{integrals}$$

---

## Theorems — Exact Statements

| Theorem | Hypotheses | Conclusion |
|---|---|---|
| **IVT** | $f$ continuous on $[a,b]$; $N$ between $f(a),f(b)$ | Some $c\in(a,b)$ with $f(c)=N$ |
| **EVT** | $f$ continuous on $[a,b]$ **closed and bounded** | $f$ attains an absolute max and min |
| **MVT** | $f$ continuous on $[a,b]$, differentiable on $(a,b)$ | Some $c$ with $f'(c)=\frac{f(b)-f(a)}{b-a}$ |
| **MVT for integrals** | $f$ continuous on $[a,b]$ | Some $c$ with $f(c)=f_{\text{avg}}$ |
| **FTC 1** | $f$ continuous | $\frac{d}{dx}\int_a^x f=f(x)$ |
| **FTC 2** | $f$ continuous on $[a,b]$, $F'=f$ | $\int_a^b f=F(b)-F(a)$ |
| **Differentiable ⟹ continuous** | $f'(a)$ exists | $f$ continuous at $a$ (**converse false**) |

---

## Derivatives

$$\frac{d}{dx}x^n=nx^{n-1}\quad
(fg)'=f'g+fg'\quad
\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}\quad
\big(f(g)\big)'=f'(g)g'$$

| $f$ | $f'$ | | $f$ | $f'$ |
|---|---|---|---|---|
| $e^x$ | $e^x$ | | $\sin x$ | $\cos x$ |
| $\ln x$ | $1/x$ | | $\cos x$ | $-\sin x$ |
| $a^x$ | $a^x\ln a$ | | $\tan x$ | $\sec^2x$ |

---

## Integrals

$$\int x^n dx=\frac{x^{n+1}}{n+1}\ (n\ne-1)\qquad \int\frac{dx}{x}=\ln\lvert x\rvert$$

**Substitution:** $u=g(x)$, $du=g'(x)dx$ — **change the limits**.
**By parts:** $\int u\,dv=uv-\int v\,du$; choose $u$ to simplify on differentiation.

**Properties:** linearity; $\int_a^b=\int_a^c+\int_c^b$; $\int_b^a=-\int_a^b$;
odd on $[-a,a]$ ⟹ $0$; even ⟹ $2\int_0^a$.

---

## Applications

| | |
|---|---|
| Area | $\int(\text{top}-\text{bottom})dx$ — **split at crossings** |
| Disks | $\pi\int f^2dx$ |
| Washers | $\pi\int(R_o^2-R_i^2)dx$ — **square first** |
| Shells | $2\pi\int x f(x)dx$ |
| Displacement / distance | $\int v\,dt$ / $\int\lvert v\rvert dt$ |
| Average value | $\frac{1}{b-a}\int_a^b f$ |
| Work | $\int F\,dx$; spring $\tfrac12kd^2$ |
| Taylor | $T_n(x)=\sum_{k=0}^n\frac{f^{(k)}(a)}{k!}(x-a)^k$ |

---

## Verified Facts

| | |
|---|---|
| $\lvert x\rvert$ at 0 | slopes $\pm1$ — corner |
| $x^{2/3}$ at 0 | $\pm\infty$ — cusp |
| $x^{1/3}$ at 0 | $+\infty$ both sides — vertical tangent |
| Root of $x^3-x-2$ | $1.521379706805$ |
| Bisection to $10^{-4}$ on width 1 | **14** steps |
| $\int_0^{2\pi}\sin$ vs $\int\lvert\sin\rvert$ | $0$ vs $4$ |
| $\int_0^1e^{-x^2}$ | $0.7468241328$ — no elementary antiderivative |
| $\sin$ vs $\cos$ area, unsplit | **0** instead of $0.8284$ |
| Washer error $\int(R_o-R_i)^2$ | wrong by **5×** |
| $y=x^2$ about $y$-axis | $8\pi$ — shells **and** washers |
| $T_{10}(1)$ for $e^x$ | $2.718281801$, error $2.7\times10^{-8}$ |

---

## Exam Technique

**Show the method** — a bare answer earns at most half.
**State the case** — top/bottom, increasing/decreasing, sign of $v$.
**Sketch** every area, volume and optimisation problem.
**Check the sign** — areas, volumes, distances are positive.
**Name the theorem** you are invoking.

---

*MATH 141 · Week 12 · Reference · © CSE Department*
