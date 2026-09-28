---
assessment: Quiz 01
course: MATH 141
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-09-28
submitted: 2026-09-28
graded: 2026-09-28
source: "QUIZ 01 With Answer Key.md"
---

# MATH 141 · Quiz 01

## Answer Sheet

**Assessment:** `QUIZ 01 With Answer Key.md`
**Points available:** 20

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Answer

**Your answer:**

**Q1 (4 pts).** Domain of $f(x)=\dfrac{\sqrt{3-x}}{x^2-x-2}$

- Numerator: the radicand must be non-negative, so $3-x\ge 0 \Rightarrow x\le 3$.
- Denominator: $x^2-x-2=(x-2)(x+1)\ne 0 \Rightarrow x\ne 2$ and $x\ne -1$.
- Combined: $x\le 3$, $x\ne -1$, $x\ne 2$.

**Domain:** $(-\infty,-1)\cup(-1,2)\cup(2,3]$

**Q2 (4 pts).** $f(x)=\dfrac{1}{x+1}$, $g(x)=x^2-1$

(a) $(f\circ g)(x)=f(g(x))=f(x^2-1)=\dfrac{1}{(x^2-1)+1}=\boxed{\dfrac{1}{x^2}}$

(b) $g$ is defined for all real $x$. $f$ needs its input $\ne -1$, so $x^2-1\ne -1 \Rightarrow x^2\ne 0 \Rightarrow x\ne 0$.

**Domain:** $(-\infty,0)\cup(0,\infty)$

**Q3 (3 pts).** $x^2-2x-8>0$

Factor: $(x-4)(x+2)>0$. Critical points: $x=-2$ and $x=4$.

Sign chart:

| Interval       | $x+2$ | $x-4$ | Product |
| -------------- | ----- | ----- | ------- |
| $(-\infty,-2)$ | $-$   | $-$   | $+$     |
| $(-2,4)$       | $+$   | $-$   | $-$     |
| $(4,\infty)$   | $+$   | $+$   | $+$     |

**Answer:** $(-\infty,-2)\cup(4,\infty)$

**Q4 (3 pts).**

(a) $\sin\!\left(\dfrac{5\pi}{6}\right)=\sin\!\left(\pi-\dfrac{\pi}{6}\right)=\sin\!\left(\dfrac{\pi}{6}\right)=\boxed{\dfrac{1}{2}}$

(b) $\cos\!\left(-\dfrac{\pi}{4}\right)=\cos\!\left(\dfrac{\pi}{4}\right)=\boxed{\dfrac{\sqrt{2}}{2}}$ (cosine is even)

(c) $\tan\!\left(\dfrac{2\pi}{3}\right)=\tan\!\left(\pi-\dfrac{\pi}{3}\right)=-\tan\!\left(\dfrac{\pi}{3}\right)=\boxed{-\sqrt{3}}$

**Q5 (3 pts).** $2^{3x-1}=16$

$16=2^4$, so $2^{3x-1}=2^4 \Rightarrow 3x-1=4 \Rightarrow 3x=5 \Rightarrow \boxed{x=\dfrac{5}{3}}$

**Q6 (3 pts).** $\ln(x+2)+\ln(x-1)=\ln 4$

$\ln[(x+2)(x-1)]=\ln 4$

$(x+2)(x-1)=4 \Rightarrow x^2+x-2=4 \Rightarrow x^2+x-6=0 \Rightarrow (x+3)(x-2)=0$

So $x=-3$ or $x=2$.

**Check:**

- $x=-3$: $\ln(-1)$ is undefined, so this solution is extraneous and rejected.
- $x=2$: $\ln 4+\ln 1=\ln 4+0=\ln 4$ ✓

**Answer:** $\boxed{x=2}$

_Marks: 20 / 20_

---

## Grading Summary

_Filled in by the grader._

|             |                |
| ----------- | -------------- |
| **Score**   | **20 / 20**    |
| **Percent** | 100%           |
| **Graded**  | 2026-09-28     |

**Feedback:**

All six questions are correct, and every mark in the key's rubric is earned.

| Q   | Rubric                                                  | Marks |
| --- | ------------------------------------------------------- | ----- |
| Q1  | numerator restriction 2 · factoring 1 · interval notation 1 | 4 / 4 |
| Q2  | (a) composition simplified 2 · (b) domain 2             | 4 / 4 |
| Q3  | factoring 1 · sign chart 1 · intervals 1                | 3 / 3 |
| Q4  | (a) 1 · (b) 1 · (c) 1                                   | 3 / 3 |
| Q5  | 16 = 2⁴ 1 · equating exponents 1 · solving 1            | 3 / 3 |
| Q6  | combining logs 1 · solving quadratic 1 · rejecting −3 1 | 3 / 3 |

**The answers were checked independently, not only against the key.** Q1: at x = 3 the
numerator is 0 and the denominator is 4, so 3 is included; −1 and 2 are the roots of the
denominator. Q2: g(x) = −1 only at x = 0, which is the one point where 1/x² hides a
restriction. Q3: the parabola opens upward, so it is positive outside its roots. Q4: the
reference angles and quadrant signs are right (sine positive in Q2, tangent negative in
Q2, cosine even). Q5: 2^(3·5/3 − 1) = 2⁴ = 16. Q6: x = 2 gives ln 4 + ln 1 = ln 4, and
x = −3 makes both logarithms undefined.

Two points in the working deserve credit beyond the rubric. Q2(b) finds the domain from the
composition f(g(x)) rather than from the simplified 1/x². Here both routes give x ≠ 0,
but reasoning from the simplified form is the usual way this question goes wrong. Q6 checks
both roots against the original equation instead of just discarding the negative one.

**A process note, not charged against this score.** The quiz is a 15-minute, closed-book
paper, but `QUIZ 01 With Answer Key.md` keeps the instructor key in the same file, directly
below the questions. The working here also follows the key almost line for line (Q1's
three bullets, Q4's reduction chains, Q6's step sequence). For questions this standard that
is plausible, since there are few ways to write them. Still, the grade cannot confirm that
the work was done under quiz conditions. For future quizzes, keep the question paper and the
key in separate files and open the key only when grading, so the score measures what it
is meant to measure.

*Graded against `QUIZ 01 With Answer Key.md` (instructor key, per-question rubric).*
