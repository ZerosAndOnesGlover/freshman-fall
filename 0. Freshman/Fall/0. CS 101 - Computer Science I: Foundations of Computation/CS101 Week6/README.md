# CS 101 · Week 6: Algorithm Analysis — Big-O Notation

---

## Contents

```
CS101_Week6/
│
├── README.md                                        ← You are here
│
├── lectures/
│   ├── L19 Big O Formal Definitions.md               ← Wed: formal O/Ω/Θ definitions with
│   │                                                     worked proofs, complexity hierarchy,
│   │                                                     loop analysis rules, space complexity
│   ├── L20 Recurrence Relations and Master Theorem.md ← Thu: writing recurrences, recursion
│   │                                                     tree/substitution/Master Theorem,
│   │                                                     amortized analysis preview
│   └── L21 Complexity Classes and Synthesis.md      ← Fri: every complexity class in depth,
│                                                          log-log plot math, worst/avg/best
│                                                          case, limits of Big-O, course synthesis
│
├── lab/
│   ├── LAB 6 Empirical vs Theoretical Complexity.md  ← Tue 10 Nov (W7): analyze 8 functions by hand FIRST,
│   │                                                     then count their steps, estimate
│   │                                                     exponents, formal proof practice
│   └── count_growth_starter.py                      ← Lab starter — the functions + step-count tables
│
├── assignments/
│   ├── QUIZ 6 Week 6 Wednesday.md                        ← In-class quiz (covers Week 5)
│   ├── PS 6 Algorithm Analysis.md                    ← Problem Set 6 (due Fri 13 Nov, 17:00)
│   ├── ps6_starter.py                               ← Scaffold: classifying code, tribonacci
│   │                                                     call counts, amortized append simulation
│   └── MIDTERM 1 Review and Practice Exam.md         ← Full practice exam + complete answer key
│                                                          (Weeks 0–5)
│
├── resources/
│   └── Reading Guide Week 6.md                       ← 3 practice sessions, formula reference
│                                                          card, 5 mistakes, self-test
│
└── solutions_instructor/
    └── LAB 6 Solutions.md                            ← Expected answers and marking notes
```

---

## Week 6 at a Glance

**Theme:** Making rigorous everything you have measured empirically since Week 4. Big-O, Big-Ω, and Big-Θ are not new intuitions — they are the mathematical language for the intuitions you already have.

| Day | Event | Topic |
|-----|-------|-------|
| Wed 4 Nov | Lecture 19 + Quiz 6 | Formal O/Ω/Θ definitions, worked proofs, loop analysis rules |
| Thu 5 Nov | Lecture 20 | Recurrence relations: recursion tree, substitution, Master Theorem |
| Fri 6 Nov | Lecture 21 + PS6 released | Complexity classes in depth, log-log math, limits of Big-O |
| Tue 10 Nov (W7) | Lab 6 (graded) | Step counts vs predicted complexity, growth exponents, Big-O proofs |

**⚠️ Midterm 1 this week** — covers Weeks 0 through 5. A full practice exam with answer key is included in [[CS101 Week6/assignments/MIDTERM 1 Review and Practice Exam|MIDTERM 1 Review and Practice Exam]].

---

## Your To-Do List

### Before Wednesday
- [ ] Read CLRS Ch. 3.1–3.2 (asymptotic notation, formal definitions)
- [ ] Review Week 5 — Quiz 6 covers searching and sorting

### Wednesday
- [ ] Quiz 6 (10 min — covers Week 5)
- [ ] Notes for L19

### Before Thursday
- [ ] Practice Session A from Reading Guide (proof intuition — work all 4 practice proofs)
- [ ] Read CLRS Ch. 4.3–4.5 (Master Method)

### Thursday
- [ ] Notes for L20
- [ ] Practice Session B (recurrence practice — all 4 recurrences)

### Tuesday 10 November Lab, Week 7 (Required, Graded)
- [ ] Complete Part 1 (theoretical analysis) BEFORE writing any code
- [ ] Instrument the functions and record the step-count tables
- [ ] Answer the prediction-vs-count questions (watch function H)
- [ ] Complete all 4 formal Big-O proofs in Part 4
- [ ] TA checkoff

### Friday
- [ ] Notes for L21
- [ ] Practice Session C (empirical doubling test in the REPL)
- [ ] PS6 released — read completely

### **This Week — Midterm 1 Preparation**
- [ ] **Take the full practice exam in [[CS101 Week6/assignments/MIDTERM 1 Review and Practice Exam|MIDTERM 1 Review and Practice Exam]] under timed, closed-book conditions**
- [ ] Grade yourself against the answer key
- [ ] Reread any lecture (Weeks 0–5) corresponding to topics you missed
- [ ] Prepare your one-sided handwritten cheat sheet

### Weekend
- [ ] Start PS6 — at minimum A1–A3 (proofs) and B2 (classification exercises)

---

## The Central Ideas of Week 6

**1. Big-O is a precise mathematical statement, not a vibe.**
`f(n) = O(g(n))` means: there exist specific constants c and n₀ such that `f(n) ≤ c·g(n)` for all `n ≥ n₀`. Every Big-O claim can — and should — be backed by an explicit proof with real numbers.

**2. O, Ω, and Θ answer different questions.**
O is an upper bound ("no worse than"). Ω is a lower bound ("no better than"). Θ is both — the tight, exact growth rate. Casual usage often says "O" when "Θ" is meant; formal usage distinguishes them precisely.

**3. Loops have mechanical analysis rules.**
Sequential loops add; nested loops multiply; halving loops give log n; function calls inside loops multiply by the called function's own complexity — a rule that is easy to forget and commonly tested.

**4. Recurrence relations formalize recursive algorithm analysis.**
Every recursive function has a recurrence: base case + recursive case. Three methods solve them: recursion trees (intuitive, always works), substitution (guess + prove by induction), and the Master Theorem (fast, but only for the specific `T(n)=aT(n/b)+f(n)` form).

**5. The Master Theorem has a specific shape — know when it doesn't apply.**
Fibonacci's `T(n)=T(n-1)+T(n-2)+O(1)` and the power set's `T(n)=T(n-1)+O(2^(n-1))` do NOT fit the template. Misapplying the Master Theorem to non-conforming recurrences is the single most common analytical mistake at this stage.

**6. Amortized analysis explains why "expensive" operations can still be efficient on average.**
Python's `list.append()` is O(1) amortized, even though individual resize operations are O(n) — because those resizes happen exponentially rarely as the list grows.

**7. Big-O has limits — it does not replace empirical measurement.**
Asymptotic analysis ignores constant factors and lower-order terms. For fixed, real-world input sizes, benchmarking (as in Lab 5 and Lab 6) is how you make final engineering decisions.

---

## Quick Self-Check

Without notes:

1. State the formal (epsilon-n₀ style) definition of Big-O.
2. What's the difference between O(g(n)) and Θ(g(n))?
3. What is the rule for nested loops? For sequential loops?
4. Write and solve the recurrence for binary search.
5. Write and solve the recurrence for merge sort, showing the Master Theorem case used.
6. Why can't the Master Theorem solve `T(n) = T(n-1) + T(n-2) + O(1)`?
7. What is amortized analysis, and what's the canonical example?
8. On a log-log plot of runtime vs. n, what does a line with slope ≈ 1 indicate? Slope ≈ 2?
9. Name two things Big-O notation deliberately ignores.
10. Give an example of an algorithm whose worst case is O(n²) but best case is O(n), and describe the triggering input for each.

*(Answers: 1. ∃c,n₀>0: f(n)≤c·g(n) ∀n≥n₀. 2. O is upper bound only; Θ is upper AND lower — tight. 3. nested: multiply; sequential: add. 4. T(n)=T(n/2)+O(1) → O(log n). 5. T(n)=2T(n/2)+O(n) → Case 2 → O(n log n). 6. sub-problems aren't equal-sized fractions of n (n/b) — they're n minus a constant. 7. average cost per op across many ops; dynamic array doubling. 8. slope≈1 → O(n); slope≈2 → O(n²). 9. constant factors, lower-order terms (also: real hardware effects). 10. insertion sort; worst=reverse-sorted, best=already-sorted.)*

---

## Algorithms and Techniques Introduced This Week

| Technique | Purpose | Example Use |
|-----------|---------|-------------|
| Formal O/Ω/Θ proofs | Rigorously establish growth bounds | Proving `4n³+2n²+100 = Θ(n³)` |
| Recursion tree method | Solve any recurrence by summing level-work | Merge sort, power set |
| Substitution method | Solve recurrences via guess + induction | `T(n)=T(n-1)+n` |
| Master Theorem | Fast-path solution for `T(n)=aT(n/b)+f(n)` | Merge sort, Karatsuba, closest-pair |
| Amortized analysis | Average cost across a sequence of operations | Dynamic array append |
| Log-log regression | Empirically estimate complexity exponent from data | Lab 6 / PS6 B1 |

---

*CS 101 · Week 6 · © CSE Department*
