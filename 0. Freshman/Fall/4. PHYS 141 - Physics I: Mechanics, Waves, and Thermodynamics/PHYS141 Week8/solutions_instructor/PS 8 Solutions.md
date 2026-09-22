# PHYS 141 · Problem Set 8 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally. $g = 9.81$ m/s².

---

*Revised 2026-09-21 to match the 10-problem set; problems are numbered as in the new set.*

## Part A — SHM Kinematics

### 1. *(10 pts)* $m = 0.750$ kg, $k = 30.0$ N/m, $A = 0.0800$ m

$$\omega = \sqrt{\frac{30.0}{0.750}} = \mathbf{6.32~\text{rad/s}} \qquad T = \frac{2\pi}{\omega} = \mathbf{0.993~\text{s}} \qquad f = \mathbf{1.01~\text{Hz}}$$
$$v_{\max} = A\omega = \mathbf{0.506~\text{m/s}} \qquad a_{\max} = A\omega^2 = \mathbf{3.20~\text{m/s}^2} \qquad E = \tfrac12kA^2 = \mathbf{0.0960~\text{J}}$$

*Marking: 1 for $\omega$, 1 for $T$ and $f$, 1 each for $v_{\max}$, $a_{\max}$, $E$.*

---

### 2. *(10 pts)* $x(t) = 0.250\cos(12.0t+\pi/3)$

$A = 0.250$ m; $\omega = 12.0$ rad/s; $T = 2\pi/12 = \mathbf{0.524~\text{s}}$;
$f = \mathbf{1.91~\text{Hz}}$; $\phi = \pi/3$; $x(0) = 0.250\cos(\pi/3) = \mathbf{0.125~\text{m}}$.

First zero: $12t+\pi/3 = \pi/2 \Rightarrow t = \dfrac{\pi/6}{12} = \mathbf{0.0436~\text{s}}$.

*Marking: 3 for the six parameters, 2 for the zero crossing. Students who use $\cos^{-1}(0)=\pi/2$
without checking it is the **first** crossing after $t=0$ should be watched, though here it is.*

---

### 3. *(10 pts)* Speed $= v_{\max}/2$

$$\omega\sqrt{A^2-x^2} = \tfrac12\omega A \;\Longrightarrow\; A^2 - x^2 = \tfrac14A^2 \;\Longrightarrow\; x = \frac{\sqrt3}{2}A \approx \mathbf{0.866A}$$

**Note the asymmetry worth pointing out:** at 87% of the amplitude the mass still moves at half its
top speed. Speed falls off slowly near the centre and rapidly near the turning points.

---

## Part B — Energy in SHM

### 4. *(10 pts)* At $x = 0.0400$ m for Problem 1's oscillator

$$U = \tfrac12kx^2 = \tfrac12(30.0)(0.0400)^2 = \mathbf{0.0240~\text{J}}$$
$$K = E - U = 0.0960 - 0.0240 = \mathbf{0.0720~\text{J}}$$

**Check:** $v = \omega\sqrt{A^2-x^2} = 0.438$ m/s, so $\tfrac12mv^2 = 0.0720$ J ✓

*Note $x = A/2$ gives $U = E/4$, not $E/2$ — energy is quadratic in displacement. This trips up most
of the class at least once.*

---

### 5. *(10 pts)* $K = U$

$$\tfrac12kx^2 = \tfrac12\left(\tfrac12kA^2\right) \;\Longrightarrow\; x^2 = \tfrac12A^2 \;\Longrightarrow\; x = \frac{A}{\sqrt2} \approx \mathbf{0.707A}$$

---

## Part C — Pendulums

### 6. *(10 pts)* $T = 1.00$ s

$$L = g\left(\frac{T}{2\pi}\right)^2 = 9.81\left(\frac{1.00}{2\pi}\right)^2 = \mathbf{0.248~\text{m}}$$

---

### 7. *(10 pts)* Uniform rod, $L = 0.800$ m, pivoted at one end

$$T = 2\pi\sqrt{\frac{\tfrac13mL^2}{mg(L/2)}} = 2\pi\sqrt{\frac{2L}{3g}} = \mathbf{1.47~\text{s}}$$

Equivalent simple-pendulum length: $2L/3 = \mathbf{0.533~\text{m}}$.

**Why it swings faster:** a simple pendulum has all its mass at distance $L$, giving $I = mL^2$. The
rod's mass is spread from 0 to $L$, giving only $\tfrac13mL^2$ — much less rotational inertia — while
its centre of mass sits at $L/2$, so the restoring torque falls by only half. Less inertia relative
to torque means a shorter period.

---

## Part D — Damping and Resonance

### 8. *(10 pts)* $m = 0.250$ kg, $k = 100$ N/m, $b = 0.500$ kg/s

$$\omega_0 = \sqrt{100/0.250} = \mathbf{20.0~\text{rad/s}} \qquad \gamma = \frac{b}{2m} = \mathbf{1.00~\text{s}^{-1}}$$
$$\omega_d = \sqrt{20.0^2-1.00^2} = \mathbf{19.975~\text{rad/s}} \qquad Q = \frac{\omega_0}{2\gamma} = \mathbf{10.0}$$

**Classification:** $2\sqrt{mk} = 10.0$ kg/s, and $b = 0.500 \ll 10.0$, so **underdamped**.

*Marking: 1 each for the four quantities, 2 for the classification **with the comparison shown**.*

---

### 9. *(10 pts)* Decay to 25%

Amplitude: $e^{-\gamma t} = 0.25 \Rightarrow t = \ln4/\gamma = \mathbf{1.39~\text{s}}$.
Energy: $e^{-2\gamma t} = 0.25 \Rightarrow t = \ln4/2\gamma = \mathbf{0.693~\text{s}}$.

**Why the factor of two:** $E \propto A^2$, so if $A \propto e^{-\gamma t}$ then
$E \propto e^{-2\gamma t}$. The energy decay constant is twice the amplitude decay constant, so the
energy reaches any given fraction in half the time.

*Marking: 2 each for the times, 2 for the explanation.*

---

### 10. *(10 pts)* Driven response, $\omega_0 = 40.0$, $\gamma = 1.50$, $F_0/m = 2.00$

| $\omega$ (rad/s) | Amplitude (m) |
|---|---|
| 20.0 | $1.67\times10^{-3}$ |
| 38.0 | $1.04\times10^{-2}$ |
| **40.0** | $\mathbf{1.67\times10^{-2}}$ |
| 42.0 | $9.67\times10^{-3}$ |

**Resonance at $\omega = \omega_0 = 40.0$ rad/s.**

**Sharpness:** the amplitude at resonance is **10× larger** than at $\omega = 20$, and falls to about
60% of its peak by $\omega = 38$ or $42$ — a shift of only 5%. The peak is narrow, consistent with
$Q = \omega_0/2\gamma = 13.3$.

*Marking: 4 for the values, 1 for identifying resonance, 1 for a comment on sharpness.*

---
