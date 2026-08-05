# MATH 142 · Calculus II
## Week 9 · Overview
### Power Series; Radius and Interval of Convergence

---

**Topic:** series with a variable in them — and the first step toward representing functions
**Reading:** Stewart §11.8–11.9 | Apostol Ch. 11 §11.1–11.5
**Assessment this week:** PS 9, Lab 9, **Quiz 09** *(Monday — covers Week 8)*

---

## Putting a Variable In

$$\sum_{n=0}^\infty c_n(x-a)^n = c_0 + c_1(x-a)+c_2(x-a)^2+\cdots$$

**For each fixed $x$ this is an ordinary series**, of the kind you have spent two weeks learning to test. So there is no new theory — but there is a new *question*:

> **For which $x$ does it converge?**

The answer has a remarkably clean shape.

> **Theorem.** For any power series exactly one of the following holds:
> - it converges **only at $x=a$**;
> - it converges for **all real $x$**;
> - there is a number $R>0$ such that it converges for $|x-a|<R$ and diverges for $|x-a|>R$.

**$R$ is the radius of convergence**, and the set of $x$ where the series converges is an **interval** centred at $a$ — never anything more complicated.

---

## The Ratio Test Finds $R$, and Then Falls Silent

Applying the Ratio Test to $\sum c_n(x-a)^n$ gives

$$L = |x-a|\cdot\lim_{n\to\infty}\left|\frac{c_{n+1}}{c_n}\right|$$

so $L<1$ exactly when $|x-a|<R$ with $R = \left(\lim\left|\frac{c_{n+1}}{c_n}\right|\right)^{-1}$.

**And at $|x-a| = R$ we get $L=1$ exactly** — which Week 8 established means **silence.**

> **This is why endpoints must be checked separately, by hand.** The Ratio Test locates the boundary
> and then tells you nothing about it. **At each endpoint you get an ordinary numerical series**, and
> you settle it with the tests of Weeks 7 and 8.
>
> **Week 8's most-repeated warning becomes this week's main procedure.**

---

## Four Intervals, All Realised

The two endpoints are independent, so all four combinations occur — and with $R=1$ centred at 0, one example of each:

| Series | Interval | At $x=-1$ | At $x=+1$ |
|---|---|---|---|
| $\sum x^n$ | $(-1,1)$ | diverges | diverges |
| $\sum\dfrac{x^n}{n}$ | $[-1,1)$ | converges to $-\ln2$ | diverges |
| $\sum\dfrac{(-1)^nx^n}{n}$ | $(-1,1]$ | diverges | converges |
| $\sum\dfrac{x^n}{n^2}$ | $[-1,1]$ | converges to $-\frac{\pi^2}{12}$ | converges to $\frac{\pi^2}{6}$ |

*(all verified)*

**Same radius, four different intervals.** The coefficients decide the endpoints, and nothing but a direct test will tell you which case you are in.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Power Series and the Radius | The Ratio Test, and the three cases |
| **Lecture 2** | Tuesday | Endpoints and the Interval | Where the Ratio Test stops and Weeks 7–8 start |
| **Lecture 3** | Wednesday | Functions as Power Series | Term-by-term operations, and why they are legal |

---

## What Lecture 3 Unlocks

Reading the geometric series **backwards** turns it into a statement about a function:

$$\frac{1}{1-x} = \sum_{n=0}^\infty x^n \qquad (|x|<1)$$

*(Verified.)*

From this one identity, by substitution, differentiation and integration, you obtain

$$\ln(1+x) = \sum_{n=1}^\infty\frac{(-1)^{n+1}x^n}{n}, \qquad \arctan x = \sum_{n=0}^\infty\frac{(-1)^nx^{2n+1}}{2n+1}$$

*(both verified)* — and setting $x=1$ in each recovers **$\ln2$** and **$\pi/4$**, the two series you met in Week 8 without knowing where they came from.

> **Term-by-term differentiation and integration are legal because a power series converges
> absolutely inside its radius** — which is exactly the licence Week 8 said absolute convergence
> provides. **The two weeks fit together precisely.**

---

## A Warning Lab 9 Will Make Concrete

**Convergence inside the radius can be very slow near the boundary.** For $\sum\frac{x^n}{n}$, the number of terms needed for ten-digit accuracy is

| $x$ | terms |
|---|---|
| $0.5$ | $29$ |
| $0.9$ | $190$ |
| $0.99$ | $1{,}988$ |
| $0.999$ | $19{,}974$ |

*(Measured.)* **The cost blows up as $x\to R$.**

And worse — **the boundary is not visible numerically.** At $N=200$ terms, the partial sums at $x=1.0$ (divergent) and $x=1.01$ (divergent) and $x=0.99$ (convergent) are $5.88$, $9.54$ and $4.56$. **Nothing in those three numbers reveals which is which.**

> **Lab 3's lesson, for the third time:** a finite computation cannot decide a convergence question.
> **The Ratio Test can, in one line.**

---

## What Will Be Hard

**Endpoints are not optional.** "Radius $R=2$" is not an answer to "find the interval of convergence"; you must test $x=a\pm R$ and report one of four intervals.

**The Ratio Test is applied to $|x-a|$, not to $x$.** For a series centred at $a=3$, the condition is $|x-3|<R$, and the interval is $(3-R,3+R)$.

**Series in $x^2$ or $x^{2n+1}$ need care.** Applying the ratio test to consecutive *nonzero* terms is what matters, and a missing-term series will otherwise give a wrong radius.

---

## This Week's Work

1. **Quiz 09** — Monday, 15 minutes, **covers Week 8** (alternating series, absolute convergence, Ratio/Root)
2. **PS 9** — released Wednesday, due Wednesday of Week 10
3. **Lab 9** — finding radii, watching the boundary, and deriving $\pi/4$ by integrating a series

---

## Looking Ahead

This week asks **where** a power series converges. **Week 10 asks the question that makes it matter:**

> Given a function, is there a power series that equals it?

The answer — **Taylor's theorem** — is the climax of the course, and it is how your computer evaluates $\sin$, $\exp$ and $\log$, and how $\int e^{-x^2}dx$ from Week 0 finally becomes computable.

---

*Next: Monday — Power Series and the Radius of Convergence*
