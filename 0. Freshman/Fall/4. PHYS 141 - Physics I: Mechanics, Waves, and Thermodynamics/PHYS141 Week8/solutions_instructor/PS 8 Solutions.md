# PHYS 141 — Problem Set 8 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally. $g = 9.81$ m/s².

---

## Part A — SHM Kinematics

### 1. *(5 pts)* $m = 0.750$ kg, $k = 30.0$ N/m, $A = 0.0800$ m

$$\omega = \sqrt{\frac{30.0}{0.750}} = \mathbf{6.32~\text{rad/s}} \qquad T = \frac{2\pi}{\omega} = \mathbf{0.993~\text{s}} \qquad f = \mathbf{1.01~\text{Hz}}$$
$$v_{\max} = A\omega = \mathbf{0.506~\text{m/s}} \qquad a_{\max} = A\omega^2 = \mathbf{3.20~\text{m/s}^2} \qquad E = \tfrac12kA^2 = \mathbf{0.0960~\text{J}}$$

*Marking: 1 for $\omega$, 1 for $T$ and $f$, 1 each for $v_{\max}$, $a_{\max}$, $E$.*

---

### 2. *(5 pts)* $A = 0.120$ m, $T = 0.500$ s, at $x = 0.060$ m

$\omega = 2\pi/T = 12.566$ rad/s.

$$v = \omega\sqrt{A^2-x^2} = 12.566\sqrt{0.120^2-0.060^2} = \mathbf{1.31~\text{m/s}}$$
$$a = -\omega^2 x = -(12.566)^2(0.060) = \mathbf{-9.47~\text{m/s}^2}$$

*The sign of $a$ matters — it points back towards equilibrium. Deduct 1 for a positive answer.*

---

### 3. *(5 pts)* $x(t) = 0.250\cos(12.0t+\pi/3)$

$A = 0.250$ m; $\omega = 12.0$ rad/s; $T = 2\pi/12 = \mathbf{0.524~\text{s}}$;
$f = \mathbf{1.91~\text{Hz}}$; $\phi = \pi/3$; $x(0) = 0.250\cos(\pi/3) = \mathbf{0.125~\text{m}}$.

First zero: $12t+\pi/3 = \pi/2 \Rightarrow t = \dfrac{\pi/6}{12} = \mathbf{0.0436~\text{s}}$.

*Marking: 3 for the six parameters, 2 for the zero crossing. Students who use $\cos^{-1}(0)=\pi/2$
without checking it is the **first** crossing after $t=0$ should be watched, though here it is.*

---

### 4. *(5 pts)* Speed $= v_{\max}/2$

$$\omega\sqrt{A^2-x^2} = \tfrac12\omega A \;\Longrightarrow\; A^2 - x^2 = \tfrac14A^2 \;\Longrightarrow\; x = \frac{\sqrt3}{2}A \approx \mathbf{0.866A}$$

**Note the asymmetry worth pointing out:** at 87% of the amplitude the mass still moves at half its
top speed. Speed falls off slowly near the centre and rapidly near the turning points.

---

### 5. *(5 pts)* Sketches

Released from rest at $x = +A$ means $\phi = 0$:

| | Curve | Zero at | Extremal at |
|---|---|---|---|
| $x$ | $+A\cos\omega t$ | $T/4$, $3T/4$ | $0$, $T/2$, $T$ |
| $v$ | $-A\omega\sin\omega t$ | $0$, $T/2$, $T$ | $T/4$, $3T/4$ |
| $a$ | $-A\omega^2\cos\omega t$ | $T/4$, $3T/4$ | $0$, $T/2$, $T$ |

**Phase relationships:** $v$ leads $x$ by $90°$ ($T/4$); $a$ is $180°$ out of phase with $x$.

*Marking: 3 for three correct curves, 2 for the phase statements. The single most common error is
drawing $v$ in phase with $x$.*

---

## Part B — Energy in SHM

### 6. *(5 pts)* At $x = 0.0400$ m for Problem 1's oscillator

$$U = \tfrac12kx^2 = \tfrac12(30.0)(0.0400)^2 = \mathbf{0.0240~\text{J}}$$
$$K = E - U = 0.0960 - 0.0240 = \mathbf{0.0720~\text{J}}$$

**Check:** $v = \omega\sqrt{A^2-x^2} = 0.438$ m/s, so $\tfrac12mv^2 = 0.0720$ J ✓

*Note $x = A/2$ gives $U = E/4$, not $E/2$ — energy is quadratic in displacement. This trips up most
of the class at least once.*

---

### 7. *(5 pts)* $K = U$

$$\tfrac12kx^2 = \tfrac12\left(\tfrac12kA^2\right) \;\Longrightarrow\; x^2 = \tfrac12A^2 \;\Longrightarrow\; x = \frac{A}{\sqrt2} \approx \mathbf{0.707A}$$

---

### 8. *(5 pts)* Doubling $A$

| Quantity | Factor |
|---|---|
| Period $T$ | **1** (unchanged) |
| Frequency $f$ | **1** (unchanged) |
| $v_{\max} = A\omega$ | **2** |
| $a_{\max} = A\omega^2$ | **2** |
| $E = \tfrac12kA^2$ | **4** |

*The first two are the point of the question — isochronism. Award 2 of 5 if the student changes $T$.*

---

### 9. *(5 pts)* Derivation

$$\tfrac12mv^2 + \tfrac12kx^2 = \tfrac12kA^2 \;\Longrightarrow\; mv^2 = k\left(A^2-x^2\right) \;\Longrightarrow\; v = \sqrt{\frac{k}{m}\left(A^2-x^2\right)} = \omega\sqrt{A^2-x^2}$$

using $\omega^2 = k/m$ at the last step. ∎

---

## Part C — Pendulums

### 10. *(5 pts)* $T = 1.00$ s

$$L = g\left(\frac{T}{2\pi}\right)^2 = 9.81\left(\frac{1.00}{2\pi}\right)^2 = \mathbf{0.248~\text{m}}$$

---

### 11. *(5 pts)* $L = 0.750$ m, $\theta_0 = 12°$

$$T = 2\pi\sqrt{0.750/9.81} = \mathbf{1.74~\text{s}}$$

At $12°$: $\theta = 0.20944$ rad and $\sin\theta = 0.20791$, so the linear approximation overstates
the restoring force by $0.735\%$. The true period is therefore **slightly longer** than 1.74 s, by
roughly a few tenths of a percent.

*Marking: 3 for the period, 2 for a quantitative error estimate. Any estimate in the 0.1–1% range
with correct reasoning earns the marks; the sign (true period longer) is what must be right.*

---

### 12. *(5 pts)* Uniform rod, $L = 0.800$ m, pivoted at one end

$$T = 2\pi\sqrt{\frac{\tfrac13mL^2}{mg(L/2)}} = 2\pi\sqrt{\frac{2L}{3g}} = \mathbf{1.47~\text{s}}$$

Equivalent simple-pendulum length: $2L/3 = \mathbf{0.533~\text{m}}$.

**Why it swings faster:** a simple pendulum has all its mass at distance $L$, giving $I = mL^2$. The
rod's mass is spread from 0 to $L$, giving only $\tfrac13mL^2$ — much less rotational inertia — while
its centre of mass sits at $L/2$, so the restoring torque falls by only half. Less inertia relative
to torque means a shorter period.

---

### 13. *(5 pts)* Disc pivoted at the rim, $R = 0.150$ m

Parallel axis: $I = \tfrac12mR^2 + mR^2 = \tfrac32mR^2$, and $d = R$.

$$T = 2\pi\sqrt{\frac{\tfrac32mR^2}{mgR}} = 2\pi\sqrt{\frac{3R}{2g}} = \mathbf{0.952~\text{s}}$$

*Marking: 2 for the parallel-axis step, 1 for $d = R$, 2 for the arithmetic. Forgetting the
parallel-axis term is the standard error and gives 0.777 s.*

---

### 14. *(5 pts)* Clock losing 30 s per day

**Reasoning first.** Losing time means the pendulum is too **slow**, i.e. its period is too long.
Since $T \propto \sqrt L$, the pendulum must be **shortened** — so the bob is **raised**.

The clock runs slow by a factor $86400/(86400-30)$, so the required period is smaller by that factor:

$$T_{\text{new}} = 2.000039 \times \frac{86370}{86400} = 1.999345~\text{s} \;\Longrightarrow\; L_{\text{new}} = 0.993310~\text{m}$$

$$\Delta L = 0.9940 - 0.99331 = \mathbf{0.69~\text{mm}}, \text{ raised}$$

*Marking: 2 for the direction with justification, 3 for the magnitude. **Award the 2 even if the
arithmetic fails** — reasoning about direction before computing is the skill being tested. A student
who lowers the bob has it backwards.*

---

## Part D — Damping and Resonance

### 15. *(6 pts)* $m = 0.250$ kg, $k = 100$ N/m, $b = 0.500$ kg/s

$$\omega_0 = \sqrt{100/0.250} = \mathbf{20.0~\text{rad/s}} \qquad \gamma = \frac{b}{2m} = \mathbf{1.00~\text{s}^{-1}}$$
$$\omega_d = \sqrt{20.0^2-1.00^2} = \mathbf{19.975~\text{rad/s}} \qquad Q = \frac{\omega_0}{2\gamma} = \mathbf{10.0}$$

**Classification:** $2\sqrt{mk} = 10.0$ kg/s, and $b = 0.500 \ll 10.0$, so **underdamped**.

*Marking: 1 each for the four quantities, 2 for the classification **with the comparison shown**.*

---

### 16. *(6 pts)* Decay to 25%

Amplitude: $e^{-\gamma t} = 0.25 \Rightarrow t = \ln4/\gamma = \mathbf{1.39~\text{s}}$.
Energy: $e^{-2\gamma t} = 0.25 \Rightarrow t = \ln4/2\gamma = \mathbf{0.693~\text{s}}$.

**Why the factor of two:** $E \propto A^2$, so if $A \propto e^{-\gamma t}$ then
$E \propto e^{-2\gamma t}$. The energy decay constant is twice the amplitude decay constant, so the
energy reaches any given fraction in half the time.

*Marking: 2 each for the times, 2 for the explanation.*

---

### 17. *(5 pts)* Critical damping

$$b_{\text{crit}} = 2\sqrt{mk} = 2\sqrt{(0.250)(100)} = \mathbf{10.0~\text{kg/s}}$$

**What it achieves:** the **fastest possible return to equilibrium without overshooting**.
Underdamped systems oscillate through equilibrium repeatedly; overdamped systems approach it without
oscillating but more slowly. Critical damping is the boundary and the optimum, which is why door
closers, car suspensions, and galvanometers are tuned to it.

---

### 18. *(6 pts)* Driven response, $\omega_0 = 40.0$, $\gamma = 1.50$, $F_0/m = 2.00$

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

### 19. *(4 pts)* Why the response peaks at $\omega_0$

At resonance the driving force stays **in phase with the velocity** throughout the cycle, so the
power delivered $P = \vec F\cdot\vec v$ is positive at all times and energy accumulates every cycle.
Amplitude grows until the energy fed in per cycle equals the energy removed by damping.

Off resonance, the driving force spends part of each cycle opposing the motion, removing energy it
put in earlier. The net input per cycle is small, and the steady-state amplitude is correspondingly
small.

*Marking: full marks require the phase argument. "Because it matches the natural frequency" is a
restatement, not an explanation — 1 mark.*

---

### 20. *(3 pts)* Worn shock absorbers

Shock absorbers **provide** the damping, so worn ones mean **less** damping — the suspension is now
**underdamped**. The driver feels the car continue to bounce after a bump instead of settling in one
motion.

Manufacturers target critical damping because it returns the wheel to the road fastest without
oscillation. Overdamping would be equally bad in a different way: the suspension would respond too
sluggishly to follow the road surface, reducing grip.

---

*PHYS 141 · Week 8 · PS 8 Solutions · Instructor copy*
