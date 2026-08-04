# MATH 142 · Calculus II
## Course Overview & Week-by-Week Road-map

---

**Course:** MATH 142: Calculus II — Integration Techniques and Series
**Credits:** 4
**Semester:** Spring, Year 1
**Meeting:** 3 lectures per week (50 min each) + weekly lab (2 hr)
**Prerequisites:** MATH 141

---

## Instructor Note to the Student

Calculus I asked two questions and answered them: *how fast is this changing?* and *how much has accumulated?* The Fundamental Theorem tied them together, and for a while it looked as though integration was solved.

It is not solved. **Most functions you can write down have no antiderivative you can write down.** $e^{-x^2}$ has none. $\frac{\sin x}{x}$ has none. $\sqrt{1+x^3}$ has none. This is not a gap in your education — it is a theorem (Liouville, 1835), and it is the fact that organises this entire course.

Calculus II is the response, and it comes in two halves.

**The first half (Weeks 0–5) is technique.** Integration by parts, trigonometric substitution, partial fractions: a toolkit for the integrals that *can* be done in closed form, plus the honesty to recognise the ones that cannot. You will also learn what an integral means when the region is unbounded, which is where probability begins.

**The second half (Weeks 6–12) is the deeper answer: infinite series.** If you cannot write $e^{-x^2}$'s antiderivative in finitely many symbols, write it in infinitely many. A power series turns a transcendental function into something a computer can evaluate with nothing but addition and multiplication — which is precisely how your machine computes `sin`, `exp`, and `log`.

For a computer scientist this is the more consequential half by a wide margin:

- **Taylor series** are how every numerical method is derived and how every floating-point library works
- **Convergence and error bounds** are how you know an approximation is good enough to ship
- **Fourier analysis** — which is series in disguise — underlies audio, image, and video compression
- **Sequences and their limits** are the continuous shadow of loop invariants and iterative algorithms
- **Differential equations** are the language of every simulation and every continuous model

When CS 331 tells you a gradient method converges linearly, or when you find out why `float` arithmetic loses precision near $\pi/2$, the answer will be a series argument from this course.

---

## Assessment

| Component | Weight | Notes |
|-----------|--------|-------|
| Weekly Problem Sets (12) | **30%** | PS 0–11, released Wednesday, due the following Wednesday at the start of class. Lowest 1 dropped. **Exception: PS 0** is released Monday of Week 0 and due **Friday of Week 0, 11:59 PM** — Week 0 is compressed so the course can begin Week 1 on schedule. Week 12's Problem Set 12 is an **ungraded** self-diagnostic and carries no weight. |
| Midterm Exam 1 (Week 5) | **15%** | 75 minutes. Covers Weeks 0–4. 1 cheat sheet (handwritten, 1 side). |
| Midterm Exam 2 (Week 10) | **15%** | 75 minutes. Covers Weeks 5–9. Same rules. |
| Final Exam (Week 12) | **20%** | 150 minutes. Comprehensive. 2-page cheat sheet. |
| Lab Sections (13 labs) | **10%** | Weekly 2-hr lab. Graded on completion + correctness. |
| Weekly Quizzes (12) | **10%** | 15 minutes at the start of Monday's lecture, Weeks 1–12. Quiz *N* covers Week *N−1*. Lowest 1 dropped. |

> **A note on these weights.** The Year 1 curriculum document specifies this course's topics,
> textbooks, prerequisites and credit hours, but **not its assessment breakdown**. The division above
> matches the one MATH 141 uses, so that the two-semester calculus sequence is graded on a single
> scheme, and it is the one the Academic Registry gradebook implements. If the curriculum document is
> later revised to specify weights, that revision governs.

**Grading Scale:** this course uses the **university-wide 13-band scale** defined in
`UNIVERSITY POLICIES.md` (Academic Registry) — A+ 97–100, A 93–96, A− 90–92, B+ 87–89, B 83–86,
B− 80–82, C+ 77–79, C 73–76, C− 70–72, D+ 67–69, D 63–66, D− 60–62, F below 60. The registry copy
governs if the two ever differ.

**Credit hours:** 4

---

## Required Textbooks

1. **Stewart, J.** — *Calculus: Early Transcendentals*, 9th ed. (Cengage, 2020)
   *Primary text, continuing from MATH 141. Chapters 7–11 are this course. Every problem set and exam draws from its exercises.*

2. **Apostol, T.** — *Calculus*, Vol. 1, 2nd ed. (Wiley, 1967)
   *The rigorous classic. Used for supplementary reading on series — Apostol proves what Stewart asserts. Read it when a convergence test feels like a rule handed down rather than a fact.*

**Strongly Recommended:**
- **`3Blue1Brown` — Essence of Calculus**, episodes 10–11 (Taylor series): the best visual account of why a power series works
- **Paul's Online Math Notes** (tutorial.math.lamar.edu): Calculus II section, free, exhaustive worked examples
- **MIT `OpenCourseWare` 18.01SC**, Unit 5: single-variable series with recitations

---

## Complete Week-by-Week Roadmap

| Week | Topic | Key Concept | Assessment |
|------|-------|-------------|------------|
| **0** | Review of Integration; Applications | The FTC, resaid and put to work | PS 0, Lab 0, Diagnostic Quiz |
| **1** | Integration by Parts; Trigonometric Integrals | Undoing the product rule | PS 1, Lab 1, **Quiz 01** |
| **2** | Trigonometric Substitution; Partial Fractions | Trading one integral for an easier one | PS 2, Lab 2, Quiz 02 |
| **3** | Improper Integrals; Comparison Tests | Integrating to infinity | PS 3, Lab 3, Quiz 03 |
| **4** | Volumes of Revolution, Arc Length, Surface Area | Slice, approximate, sum, take the limit | PS 4, Lab 4, Quiz 04 |
| **5** | Parametric Curves; Polar Coordinates | Curves that are not graphs of functions | PS 5, Lab 5, Quiz 05, **MIDTERM 1** |
| **6** | Sequences: Convergence and Divergence | The limit of a list | PS 6, Lab 6, Quiz 06 |
| **7** | Series: Geometric, p-series, Integral, Comparison | An infinite sum is a limit of finite ones | PS 7, Lab 7, Quiz 07 |
| **8** | Alternating Series; Ratio and Root Tests | Absolute vs conditional convergence | PS 8, Lab 8, Quiz 08 |
| **9** | Power Series; Radius and Interval of Convergence | A series with a variable in it | PS 9, Lab 9, Quiz 09 |
| **10** | Taylor and Maclaurin Series; Applications | Any smooth function, as a polynomial | PS 10, Lab 10, Quiz 10, **MIDTERM 2** |
| **11** | Differential Equations: Separable and Linear | Equations whose unknown is a function | PS 11, Lab 11, Quiz 11 |
| **12** | Systems; Numerical Methods Preview; Review | Where the exact answer runs out | PS 12 *(ungraded)*, Lab 12, Quiz 12, **FINAL** |

---

## The Conceptual Arc of the Course

```
WEEK 0:  Review: FTC, substitution, area ─────────────────┐
                                                          │ Technique
WEEK 1:  Integration by Parts, Trig Integrals             │
WEEK 2:  Trig Substitution, Partial Fractions ────────────┤
WEEK 3:  Improper Integrals ← where "area" is redefined ──┤ Extension
WEEK 4:  Volumes, Arc Length, Surface Area                │
WEEK 5:  Parametric and Polar ────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEEK 6:  Sequences ───────────────────────────────────────┐
WEEK 7:  Series and the convergence tests                 │ Series
WEEK 8:  Alternating, Ratio, Root                         │
WEEK 9:  Power Series ────────────────────────────────────┤
WEEK 10: Taylor Series ← THE CLIMAX ──────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEEK 11: Differential Equations ──────────────────────────┐ Payoff
WEEK 12: Systems, Numerical Methods ──────────────────────┘
```

**Taylor's Theorem** (Week 10) is to this course what the Fundamental Theorem was to MATH 141. It says that a function which is differentiable enough is, near a point, *indistinguishable from a polynomial* — and it comes with a remainder term that tells you exactly how wrong you are. Everything in Weeks 6–9 is built to make that statement precise, and everything after it is a consequence.

---

## A Warning Specific to This Course

MATH 141 was a course about ideas with a modest amount of computation. **Weeks 1–5 of this course invert that ratio.** Integration technique is a craft, and craft is learned by repetition: there is no conceptual insight that will let you do a trigonometric substitution you have never practised. Students who coasted through MATH 141 on understanding alone are the ones who struggle here, and they usually discover it at Midterm 1.

Then in Week 6 it inverts again. **Series are conceptually the hardest material in the first-year sequence** — the computations are easy and the reasoning is subtle, which is the exact opposite of Weeks 1–5. Expect to feel competent in October and lost in November. That is the course working as designed, not evidence that you have fallen behind.

---

## How to Succeed in This Course

### Weekly Workflow

**Before lecture (30 min):** read the assigned section; note what you don't follow.

**During lecture (50 min):** rework each example yourself as it goes up. In Weeks 1–5 especially, watching an integration technique is nothing like doing one.

**Same day (60 min):** redo the lecture's examples from a blank page. If you cannot start one, you did not understand it — you recognised it.

**Problem set (spread across the week):** try each problem alone first. After 20 minutes stuck, read the section; after another 20, look at a worked example and then return to the problem. Then ask.

**Before exams:** rework problem sets from scratch, under time.

### The Two Most Important Rules

> **In Weeks 1–5: check by differentiating.**
> Every antiderivative you produce can be verified in under a minute by differentiating it. There is
> no other topic in mathematics where checking your answer is this cheap. Students who lose marks on
> integration almost never lose them for lack of understanding — they lose them to a dropped
> constant that thirty seconds of differentiation would have caught.

> **In Weeks 6–12: state which test you are using, and check its hypotheses.**
> Most lost marks on series are not wrong conclusions but unjustified ones — a Ratio Test applied
> where it is inconclusive, a Comparison Test with an inequality pointing the wrong way, an
> Alternating Series Test used on a sequence that is not decreasing. The test's name and its
> hypotheses are part of the answer.

---

## Office Hours & Resources

- **Instructor Office Hours:** TBD — posted on course portal
- **TA Office Hours:** Daily coverage — schedule on portal
- **Math Help Center:** Open 8am–8pm weekdays, no appointment needed
- **Online:** Course discussion board (post within 24 hours of getting stuck)
- **Peer Tutoring:** Available through Academic Success office

---

## Calculator Policy

A scientific calculator is permitted for labs and homework. **Calculators are NOT permitted on quizzes or exams.** Every exam problem is designed to have a clean exact answer if you know the technique. A calculator will not tell you which substitution to make, and that is the entire skill being assessed.

Labs are the exception and deliberately so: several labs ask you to compute a numerical approximation and compare it against an exact value, which is the only honest way to see how good an approximation is.

---

## Academic Integrity

Homework: discussion of approach is allowed. All written work must be independently completed. Copying is plagiarism.

Exams/Quizzes: closed book, closed neighbour, closed device. The cheat sheet allowance is generous — build it yourself, because building it is most of the revision.

---

*Welcome to Calculus II. MATH 141 gave you the two operations. This course is about what to do when the symbols run out.*
