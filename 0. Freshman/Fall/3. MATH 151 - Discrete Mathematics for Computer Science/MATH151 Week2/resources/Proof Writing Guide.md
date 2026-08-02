# MATH 151 — Proof Writing Guide
## How to Write a Mathematical Proof: Week 2

---

## The Golden Rules

**Rule 1: Every claim must be justified.**
Every sentence that is not a hypothesis or a definition must follow from something that came before. "Obviously..." and "clearly..." are red flags — if it were obvious, you wouldn't need to say so. Either prove it or cite a known result.

**Rule 2: Definitions are the entry point.**
You cannot prove anything about an even number without writing n = 2k. You cannot prove anything about divisibility without writing b = ka. The first move in almost every proof is unpacking definitions.

**Rule 3: Name every new object.**
When you compute an expression and need to refer to it, give it a name. "Let m = 2jk + j + k. Then n² = 2m + 1." Unnamed intermediate expressions lead to confusion.

**Rule 4: Integer witnesses must actually be integers.**
When you write "n = 2k for integer k," verify k is an integer. If your "witness" turns out to be 1/2 or √3, the proof fails.

**Rule 5: Write for a skeptical reader.**
Your proof should convince someone who does not already believe the result. Every step should be so clear that no reasonable person can object.

---

## Proof Templates

### Template 1: Direct Proof of P → Q

```
Proof.
Assume [P stated precisely].
By definition of [term], [expand P into algebraic form].
Then [algebraic steps, each justified].
[Show the result has the form required by Q's definition.]
By definition of [term], [Q].
∎
```

### Template 2: Proof by Contrapositive

```
Proof.
We prove the contrapositive: [state ¬Q → ¬P in words].
Assume [¬Q stated precisely].
By definition of [term], [expand ¬Q].
Then [algebraic steps].
[Show result is ¬P.]
By definition, [¬P].
Therefore, by contrapositive, [P → Q]. ∎
```

### Template 3: Proof by Contradiction

```
Proof.
Suppose, for contradiction, that [¬C].
[For implication P → Q: "Suppose P holds and Q fails."]
By definition, [expand ¬C].
Then [algebraic steps].
[Derive R.]
But [derive ¬R from earlier, or from a known fact].
This contradicts [R]. / This is a contradiction since [reason].
Therefore [C]. ∎
```

### Template 4: Proof by Cases

```
Proof.
We consider all possible cases.
Case 1: [first condition].
  [Prove the claim in this case.]
Case 2: [second condition].
  [Prove the claim in this case.]
[... more cases if needed ...]
In all cases, [conclusion]. ∎
```

*Requirement: The cases must be exhaustive (cover every possibility) and each correctly handled.*

---

## Language and Style

### Words That Introduce Steps

| Word/Phrase | Use when |
|---|---|
| "Assume..." | Stating a hypothesis |
| "By definition of [term]..." | Unpacking a definition |
| "Let [var] = [expr]..." | Naming a new object |
| "Then..." / "Thus..." / "Therefore..." | Logical consequence |
| "Since [fact], ..." | Giving a reason |
| "By assumption..." | Using a previously assumed hypothesis |
| "We consider two cases..." | Starting case analysis |
| "In both cases..." | Concluding a case analysis |
| "Suppose, for contradiction, that..." | Starting a contradiction proof |
| "This contradicts [statement]." | Identifying the contradiction |
| "We prove the contrapositive..." | Announcing the contrapositive |

### Words to Avoid

| Avoid | Because |
|---|---|
| "Obviously..." | Either prove it or it isn't obvious |
| "Clearly..." | Same as above |
| "It can be shown that..." | Then show it |
| "We know that..." | Cite where we know it from |
| "Just..." | Mathematically meaningless |
| "etc." | Proofs must be complete |

---

## Common Proof Errors Reference

| Error | Example | Why Wrong | Fix |
|---|---|---|---|
| Assuming conclusion | "Assume n is even. Then n=2k, so n is even." | Circular | Prove n=2k from given info, don't assume it |
| Wrong parity form | "n odd → n = 2k+1, so n+1 = 2k+2 = 2(k+1) → n+1 odd" | 2(k+1) is even, not odd | n+1 = 2(k+1), which is even ✓ |
| Proof by example | "Tested n=2,4,6 — always works." | Proves nothing for infinite domain | Prove for arbitrary n |
| Dividing by zero | "Since ab = ac, dividing by a gives b = c." | a might be 0 | Add hypothesis a ≠ 0, or case split |
| Non-integer witness | "n=√(2k), so n is even." | √(2k) may not be integer | Doesn't establish n is even |
| Wrong negation | Proving converse instead of contrapositive | Converse ≠ contrapositive | Remember: contrapositive swaps AND negates BOTH sides |
| Incomplete cases | Proving only x > 0 case for ∀x ∈ ℝ | Misses x = 0 and x < 0 | Check all cases are covered |
| Contradiction without contradiction | "Suppose X is false. Then ... therefore X is true. ∎" | Haven't derived R ∧ ¬R | Must exhibit explicit impossible statement |

---

## Definitions Reference (Week 2)

| Term | Definition to cite |
|---|---|
| n is even | n = 2k for some k ∈ ℤ |
| n is odd | n = 2k + 1 for some k ∈ ℤ |
| a \| b | b = ka for some k ∈ ℤ |
| r is rational | r = p/q for some p, q ∈ ℤ with q ≠ 0 |
| n is prime | n > 1 and n = ab (a,b ∈ ℤ) implies a = 1 or b = 1 |
| n is composite | n = ab for some a, b ∈ ℤ with 1 < a < n |
| gcd(a,b) = 1 | a and b share no common factor > 1 |

---

## Proof Quality Checklist

Before submitting any proof, verify:

- [ ] Did I state which technique I am using?
- [ ] Did I state all hypotheses explicitly?
- [ ] Did I expand every defined term the first time I use it?
- [ ] Is every new variable named and shown to be an integer (or whatever type is required)?
- [ ] Does every step follow from previous steps, cited definitions, or known results?
- [ ] Did I explicitly state the conclusion?
- [ ] Is the proof written in complete English sentences?
- [ ] If using cases: are they exhaustive?
- [ ] If using contrapositive: did I state ¬Q → ¬P before proving it?
- [ ] If using contradiction: did I identify the explicit contradiction?
