# MATH 151 · Quiz 10 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 20 points.** All closed forms verified against iteration.

---

**Q1. (4 pts)** The last move is either a 1-step (from $n-1$) or a 2-step (from $n-2$):

$$s_n = s_{n-1} + s_{n-2}, \qquad s_0 = 1,\ s_1 = 1$$

**Values:** $1, 1, 2, 3, 5$ — the Fibonacci numbers.

*Marking: 2 for the recurrence, 2 for the initial conditions. $s_0=1$ (one way to climb nothing) is
the discriminator; $s_0=0$ makes every term zero and earns 2 of 4.*

---

**Q2. (4 pts)** $r^2-5r+6=(r-2)(r-3)$, so $r=2,3$ and $a_n=A2^n+B3^n$.

$A+B=1$ and $2A+3B=4$ give $B=2$, $A=-1$:

$$\boxed{a_n = 2\cdot3^n - 2^n}$$

**Check:** $1, 4, 14, 46, 146$ from both recurrence and formula ✓

*Marking: 1 characteristic equation, 1 roots, 2 constants. A sign error in the linear system is the
usual failure — award the first 2 regardless.*

---

**Q3. (4 pts)** $r^2-6r+9=(r-3)^2$ — a **double root** $r=3$.

**The repeated-root case applies**, so the general solution is $(A+Bn)3^n$. The form $A3^n+B3^n$
collapses to a single constant times $3^n$ and cannot satisfy two initial conditions.

$A=1$; $(1+B)\cdot3=9$ gives $B=2$:

$$\boxed{a_n = (1+2n)3^n}$$

**Check:** $1, 9, 45, 189, 729$ ✓

*Marking: 1 for spotting the double root, 1 for naming the case, 2 for the solution. **The question
asks why**, so a correct answer without the collapse argument earns 3.*

---

**Q4. (4 pts)** $$\sum_{n\ge0}4^nx^n = \boxed{\frac{1}{1-4x}}$$

$\dfrac{1}{(1-x)^2}$ has coefficients $\mathbf{1, 2, 3, 4}$ *(that is, $a_n = n+1$)*.

*Marking: 2 each. Writing $\frac{1}{1-x^4}$ for the first is the common slip — that generates
$1,0,0,0,1,\ldots$, not $4^n$.*

---

**Q5. (4 pts)** One factor per coin type, each an unrestricted count in multiples of its value:

$$\boxed{\frac{1}{(1-x^2)(1-x^7)}}$$

*Marking: 2 per factor. Adding rather than multiplying earns 1 — addition models alternatives, not
combinations, and this is the single most common generating-function error.*

---

## Grade Distribution Notes

Q3 separates the class. Students who memorised only the distinct-roots case will produce $A3^n+B3^n$,
find the system degenerate, and either stop or fudge it. Worth five minutes in review, since the
repeated-root case appears on the final.
