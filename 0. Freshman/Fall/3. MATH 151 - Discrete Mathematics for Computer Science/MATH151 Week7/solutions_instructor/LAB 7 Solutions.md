# MATH 151 · Week 7
## LAB7 Solutions — INSTRUCTOR ONLY

---

## Section 1 Solutions

### Exercise 1.1

**(a)** Order: NO. Repetition: NO. → Combination: $\binom{12}{3}$

**(b)** Order: YES. Repetition: NO. → Permutation: $P(12,3)$

**(c)** Order: YES. Repetition: YES. → $6^5$

**(d)** Order: NO. Repetition: NO. → Combination: $\binom{30}{5}$

**(e)** This is assigning tasks to workers — think of it as: each TASK (5 of them) independently chooses a worker (3 choices), so it's like a function from tasks to workers. Order: N/A in the traditional sense, but structurally: $3^5$ (each of 5 distinguishable tasks picks 1 of 3 workers, repetition of worker choice allowed).

**(f)** Order: NO. Repetition: YES. → $\binom{6+4-1}{4}=\binom{9}{4}$

**(g)** Order: YES. Repetition: NO. → Permutation: $P(10,3)$

---

## Section 2 Solutions

### Exercise 2.1
$\binom{12}{4} = \dfrac{12\times11\times10\times9}{24} = 495$

### Exercise 2.2
$P(20,3) = 20\times19\times18 = 6840$

### Exercise 2.3
$\binom{10}{6} = \dfrac{10!}{6!4!} = 210$

### Exercise 2.4
$P(26,6) = 26\times25\times24\times23\times22\times21 = 165{,}765{,}600$

### Exercise 2.5
Total PINs: $10^4=10000$.
No zero at all: $9^4=6561$.
At least one zero: $10000-6561=3439$.

### Exercise 2.6
Exactly 2 CS + 2 MATH: $\binom{7}{2}\binom{5}{2} = 21\times10=210$

### Exercise 2.7
$\binom{5+20-1}{20}=\binom{24}{20}=\binom{24}{4} = \dfrac{24\times23\times22\times21}{24}=23\times22\times21=10626$

---

## Section 3 — Python Expected Outputs

### Exercise 3.1
```
P(5,3) by formula: 60
P(5,3) by enumeration: 60
C(5,3) by formula: 10
C(5,3) by enumeration: 10
```

### Exercise 3.2
```
Formula C(n+r-1,r) = C(3+4-1,4) = C(6,4): 15
Enumeration count: 15
```

### Exercise 3.3
```
Total strings: 125
No zero: 64 (should be 4^3 = 64)
At least one zero: 61
Direct enumeration count: 61
Match: True
```

### Exercise 3.4

Row sums all match $2^n$ for $n=0$ through $10$. Alternating sum of row 10 = 0.

### Exercise 3.5

All (n,r) pairs tested show "OK" — LHS equals RHS in every case, confirming the Hockey Stick Identity computationally.

---

## Section 4 — Reflection Model Answers

1. Counting "no zero" is easier because it's a simple independent-choice count (each of 3 positions has 4 options, non-zero digits) — a clean application of the Multiplication Rule. Counting "at least one zero" directly requires case-splitting by WHICH position(s) contain a zero, with careful handling of overlap between cases (a string could have zeros in multiple positions) — exactly the complexity that Inclusion-Exclusion or, more simply, De Morgan's Law-style complementary reasoning avoids. "At least one" is the logical/set-theoretic negation of "none," and just as ¬∃ is often harder to verify directly than ∀¬ (Week 1), "at least one" is harder to count directly than its complement.

2. $\binom{50}{10} = 10{,}272{,}278{,}170$ — over 10 billion. Enumerating all of these combinations explicitly (e.g., with `itertools.combinations`) would require iterating over 10 billion tuples — computationally infeasible in reasonable time on ordinary hardware for exploratory/interactive work, though a single pass to just count (not print) is technically feasible on fast machines within minutes; the real infeasibility shows up in problems with $n,r$ even modestly larger (e.g., $\binom{100}{20}$, which has more than $10^{20}$ combinations — utterly impossible to enumerate).

3. Computing $50!$ directly produces an enormous integer (65+ digits) that, while Python handles arbitrary-precision integers natively (avoiding true "overflow"), still involves expensive big-integer arithmetic at every step, and computing $50!/(10!\times40!)$ this way requires forming and then dividing huge intermediate numbers. Pascal's Rule instead builds up the answer using only ADDITION of previously-computed (and comparatively small) values, entry by entry — avoiding both the giant intermediate factorials and any need for division, which is important in contexts (or number systems) where division is expensive or exact big-integer division introduces additional complexity.
