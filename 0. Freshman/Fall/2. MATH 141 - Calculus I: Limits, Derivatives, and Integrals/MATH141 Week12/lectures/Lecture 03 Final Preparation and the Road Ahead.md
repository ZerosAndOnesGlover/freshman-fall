# MATH 141 · Calculus I
## Week 12 · Lecture 3 (Wednesday)
### Final Preparation and the Road Ahead

*“If you expect to continue learning all your life, you will be teaching yourself much of the time. You must learn to learn, especially the difficult topic of mathematics.”* — Richard Hamming, *Methods of Mathematics Applied to Calculus, Probability, and Statistics* (1985)

**Date:** Wednesday 16 December 2026 · 11:00–11:50 · Week 12

**Reading:** Stewart, the Review exercises at the end of Chapters 2–6; Problems Plus after Chapters 3 and 4 (optional) | Spivak — none

**Coursework:** 📝 **PS 11** due today 11:00 · 🔬 **Lab 12** Fri 18 Dec 15:00–16:50 · 📕 **Final exam** Wed 23 Dec 09:00–11:30

---

## Part I — How to Prepare

### Do not re-read your notes

Re-reading produces recognition, and recognition is not recall. You will feel prepared and be unable
to start a problem under time pressure.

**Do this instead**, in order of value:

1. **Work Midterms 1 and 2 cold**, timed, before looking at the solutions. They are the best
   available predictors of the final's shape.
2. **Redo problems you got wrong.** Your marked problem sets are the highest-value material you own —
   they are a personalised list of your own failure modes.
3. **Reconstruct one derivation from scratch** with the notes closed: the ε-δ proof that
   $\lim_{x\to2}x^2=4$, the quotient rule from the product rule, or FTC Part 2 from Part 1.
4. **Explain a topic aloud** without notes. Where you stall is the gap.

### The formula sheet

You may bring one side of A4, handwritten. **Making it is the revision**; the sheet itself matters
less than you think.

Put on it what you **cannot derive**: the standard derivatives and antiderivatives, the washer and
shell formulas, the exact statements of the MVT, IVT and both parts of the FTC.

Leave off what you can reconstruct: anything you can get by differentiating something else, and any
formula you have used often enough to know.

---

## Part II — What the Exam Rewards

**Show the method.** A correct answer with no working earns at most half marks; correct reasoning
with an arithmetic slip usually earns most of them. The method is what is being assessed.

**State which case you are in.** Top or bottom; increasing or decreasing; which curve is outer;
whether $v$ changes sign. Most set-up errors are unstated assumptions.

**Sketch.** For every area, volume or optimisation problem. It costs thirty seconds and prevents the
errors that cost whole questions.

**Check the sign.** Areas, volumes and distances are positive. A negative answer to any of them is a
missing split or a swapped subtraction — and noticing it in the exam is worth more than the two
minutes it takes.

**Name the theorem you are using.** "By the IVT, since $f$ is continuous and $f(1)<0<f(2)$…" is
worth marks that "there's a root here" is not.

---

## Part III — The Ten Most Expensive Errors

| Error | Correction |
|---|---|
| Writing $\lim=\infty$ and calling the limit existent | It **does not exist** |
| Continuous ⟹ differentiable | Backwards. $\lvert x\rvert$ is the counterexample |
| Dropping the chain rule's inner factor | $\frac{d}{dx}f(g)=f'(g)\cdot g'$ |
| $(fg)'=f'g'$ | $f'g+fg'$ — two terms |
| "Speeding up because $a>0$" | Compare **signs** of $v$ and $a$ |
| Applying the FTC across a discontinuity | Check continuity on the **whole** interval first |
| One integral where curves cross | Split — verified to give $0$ for $\sin$ vs $\cos$ |
| $\int(R_o-R_i)^2$ for a washer | Square first: off by **5×** in the standard example |
| Forgetting to change limits after substituting | Or substitute back before evaluating |
| Treating distance as displacement | Equal only when $v$ never changes sign |

---

## Part IV — Where This Goes

### Immediately

**MATH 142 (Calculus II).** Integration techniques in depth, improper integrals, arc length and
surface area, sequences and series — and Taylor series properly, answering the convergence questions
Tuesday could only raise.

**PHYS 141.** Work, centre of mass, moments of inertia. All of it is Week 11's slicing with different
units.

### Soon

**MATH 241 (Linear Algebra)** and **MATH 251 (Probability & Statistics)**. In MATH 251,
$\int_a^b f = P(a\le X\le b)$, and Week 9's error function becomes the normal distribution.

**MATH 341 (Numerical Methods).** Every verified figure in these lectures came from a numerical
method — Simpson's rule, bisection, central differences. MATH 341 is about when they converge and how
fast, including why the central difference stops improving below $h\approx\varepsilon^{1/3}$
(Week 4's lab).

### In computer science

| Where | What from this course |
|---|---|
| **Machine learning** | Gradient descent is the derivative, used to minimise; backpropagation is the chain rule |
| **Graphics** | Curves, surfaces, and the rate at which light accumulates |
| **Algorithm analysis** | Asymptotic growth is limits at infinity, from Week 1 |
| **Numerical computing** | Everything in MATH 341 |
| **Signal processing** | Integrals of oscillating functions, leading to Fourier analysis |

### The habit worth keeping

This course computed things and then **checked them**. The root of $x^3-x-2$ was bisected to
$1.521379706805$ and the residual confirmed at $1.3\times10^{-15}$. Two volume methods were made to
agree at $8\pi$ to eight decimals. A derivative rule was tested against a central difference.

That reflex — *compute it a second way and see whether the answers agree* — is the most transferable
thing in twelve weeks. It caught a genuine error in these very notes.

---

## Summary

| | |
|---|---|
| Revision | Work old exams cold; redo what you got wrong; derive one thing from scratch |
| The formula sheet | Making it **is** the revision |
| In the exam | Show the method; state the case; sketch; check the sign; name the theorem |
| The ten errors | Reproduced above — most are unstated assumptions |
| Next | MATH 142, PHYS 141, then MATH 251 and MATH 341 |
| The habit | Compute it twice, two ways, and compare |

---

## Lecture 3 Exercises

**1.** Without notes, state: the ε-δ definition, both parts of the FTC, the MVT, and the IVT.

**2.** Derive the quotient rule from the product rule and the chain rule.

**3.** For each, name the theorem that applies and what it gives you:
(a) showing $x^5+x-1$ has a real root
(b) showing a function with $f'=0$ everywhere is constant
(c) showing a continuous function on $[0,1]$ attains a maximum
(d) evaluating $\int_1^4 x^2dx$ without Riemann sums

**4.** Draft your formula sheet. Then, for three items on it, check whether you could have derived
them in under a minute — and remove any you could.

### Answers

**1.** *(Self-check; compare against Week 1 Lecture 2, Week 9, and Week 6.)*

- **ε-δ:** $\lim_{x\to a}f(x)=L$ means for every $\varepsilon>0$ there is $\delta>0$ with
  $0<\lvert x-a\rvert<\delta \Rightarrow \lvert f(x)-L\rvert<\varepsilon$.
- **FTC 1:** $\frac{d}{dx}\int_a^x f(t)dt=f(x)$ for continuous $f$.
- **FTC 2:** $\int_a^b f=F(b)-F(a)$ for any antiderivative $F$.
- **MVT:** $f$ continuous on $[a,b]$, differentiable on $(a,b)$ ⟹ some $c$ with
  $f'(c)=\frac{f(b)-f(a)}{b-a}$.
- **IVT:** $f$ continuous on $[a,b]$, $N$ between $f(a)$ and $f(b)$ ⟹ some $c$ with $f(c)=N$.

*If you could not state the hypotheses as well as the conclusions, that is the gap to close first.*

**2.** Write $\dfrac fg = f\cdot g^{-1}$ and apply the product rule:

$$\left(\frac fg\right)'=f'\cdot g^{-1}+f\cdot\big(g^{-1}\big)'$$

By the chain rule, $\big(g^{-1}\big)'=-g^{-2}g'$, so

$$=\frac{f'}{g}-\frac{fg'}{g^2}=\frac{f'g-fg'}{g^2} \quad\blacksquare$$

*Worth doing once: it shows the quotient rule is not a separate fact to memorise, and it fixes the
numerator order — which is the part people get backwards.*

**3.**

| | Theorem | What it gives |
|---|---|---|
| **(a)** | **IVT** | $f(0)=-1<0<1=f(1)$ and $f$ is continuous, so a root exists in $(0,1)$ — **existence only**, no location |
| **(b)** | **MVT** | For any $x<y$, $f(y)-f(x)=f'(c)(y-x)=0$, so $f$ is constant. *(This is what makes "+C" the general antiderivative.)* |
| **(c)** | **Extreme Value Theorem** | A continuous function on a **closed bounded** interval attains its max and min |
| **(d)** | **FTC Part 2** | $\int_1^4x^2dx=\left[\tfrac{x^3}{3}\right]_1^4=\tfrac{64}{3}-\tfrac13=21$ |

*(b) is the one students miss — it looks obvious, and the MVT is what makes it a theorem rather than
an intuition.*

**4.** Open. The exercise is the audit, not the sheet. Typical items that **should** be removed
because they are derivable in under a minute:

- The quotient rule (Exercise 2 above)
- $\frac{d}{dx}\tan x=\sec^2x$ — quotient rule on $\sin/\cos$
- The washer formula — it is just "outer disc minus inner disc"
- $\int\cos = \sin$ and its relatives — read the derivative table backwards

Typical items that **should stay**: the exact hypotheses of the MVT, IVT and EVT; $\tfrac43\pi R^3$
and $\tfrac13\pi r^2h$ if you want them as checks; the shell formula if you find it hard to
reconstruct; the Taylor coefficient $f^{(k)}(a)/k!$.

---

*This is the end of MATH 141. Good luck in the final — and in MATH 142.*
