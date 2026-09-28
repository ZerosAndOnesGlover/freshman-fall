# MATH 151 · Discrete Mathematics for Computer Science
## Lab 5 — Function Workshop: Properties, Composition, Bijections
### Wednesday 4 November 2026, 15:00–16:50 · Week 6 | Duration: 2 hours | Covers Week 5 (all three lectures)

---

**Lab Objectives:**
1. Practice classifying functions as injective/surjective/bijective with rigorous proofs
2. Compute compositions and inverses by hand and verify computationally
3. Use bijections to establish that two finite sets have the same size
4. Build a Python function-property checker for finite domains
5. Connect function properties to hash function design

**Materials:** Pencil, paper, laptop with Python 3.

---

## Section 1 — Classification Practice (30 min)

For each function, state the domain/codomain, determine injective/surjective/bijective, and prove your answer. Work quickly but rigorously — this builds the pattern recognition you need for exams.

### Exercise 1.1

**(a)** $f: \mathbb{Z}\to\mathbb{Z}$, $f(n) = n^3$

**(b)** $f: \mathbb{R}\to\mathbb{R}$, $f(x) = e^x$ *(you may use known properties of $e^x$: always positive, strictly increasing)*

**(c)** $f: \mathbb{Z}\to\mathbb{Z}$, $f(n) = n - \lfloor n/3\rfloor \cdot 3$ (i.e., $n \bmod 3$, but codomain is all of $\mathbb{Z}$)

**(d)** $f: \{1,2,3,4,5\}\to\{1,2,3,4,5\}$, $f(1)=3,f(2)=1,f(3)=4,f(4)=2,f(5)=5$

**(e)** $f: \mathbb{Z}\times\mathbb{Z}\to\mathbb{Z}\times\mathbb{Z}$, $f(m,n)=(n,m)$

**(f)** $f: \mathbb{R}\to\mathbb{R}$, $f(x) = \begin{cases}x+1 & x\geq0\\x-1&x<0\end{cases}$

---

## Section 2 — Composition and Inverse Practice (35 min)

### Exercise 2.1

Let $f(x)=x+3$ and $g(x)=2x$, both $\mathbb{Z}\to\mathbb{Z}$.

**(a)** Compute $(f\circ g)(x)$ and $(g\circ f)(x)$ as formulas.

**(b)** Evaluate $(f\circ g)(5)$ and $(g\circ f)(5)$ two ways each: directly from your formula, and by step-by-step application. Confirm they match.

**(c)** Are $f\circ g$ and $g\circ f$ equal as functions? Justify.

---

### Exercise 2.2

For each function below: determine if it's invertible (over the given domain/codomain). If yes, derive $f^{-1}$ explicitly and verify both compositions $f^{-1}\circ f = \text{id}$ and $f\circ f^{-1}=\text{id}$.

**(a)** $f:\mathbb{R}\to\mathbb{R}$, $f(x)=-3x+5$

**(b)** $f:\mathbb{R}\to\mathbb{R}$, $f(x)=x^3+1$

**(c)** $f:(0,\infty)\to\mathbb{R}$, $f(x)=\ln(x)$ *(you may use that $\ln$ and $\exp$ are mutual inverses)*

**(d)** $f:\mathbb{Z}\to\mathbb{Z}$, $f(x)=2x+1$

---

### Exercise 2.3 — Composition Chains

Let $f(x)=2x$, $g(x)=x+1$, $h(x)=x^2$, all $\mathbb{Z}\to\mathbb{Z}$.

**(a)** Compute $(h\circ g\circ f)(x)$.

**(b)** Compute $(f\circ g\circ h)(x)$.

**(c)** Are these equal? What does this tell you about the order-sensitivity of composition chains?

**(d)** Verify associativity concretely: compute $h\circ(g\circ f)$ and $(h\circ g)\circ f$ separately and confirm they produce the same formula.

---

## Section 3 — Python: Function Property Checker (25 min)

Create `function_tools.py`. Everything here uses lists, loops and `def` (CS 101 Weeks 2–3); a function is passed
in as a value (CS 101 Lecture 10 §9), often written as a `lambda` (Lecture 11).

### Exercise 3.1 — Injective and Surjective, by Brute Force

```python
def outputs_of(f, domain):
    """The list [f(x) for each x in domain], built with a loop."""
    result = []
    for x in domain:
        result.append(f(x))
    return result

def is_injective(f, domain):
    """No two different inputs share an output."""
    out = outputs_of(f, domain)
    for i in range(len(out)):
        for j in range(i + 1, len(out)):
            if out[i] == out[j]:
                return False
    return True

def is_surjective(f, domain, codomain):
    """Every element of the codomain is hit."""
    out = outputs_of(f, domain)
    for y in codomain:
        if y not in out:
            return False
    return True
```

**Task:** Write `classify_function(f, domain, codomain, name)` that prints BIJECTIVE, INJECTIVE ONLY,
SURJECTIVE ONLY or NEITHER. Test it with `domain = list(range(-10, 11))`:

```python
classify_function(lambda x: x**2, domain, domain, "x^2")
classify_function(lambda x: x + 5, domain, outputs_of(lambda x: x + 5, domain), "x+5 onto its image")
classify_function(lambda x: abs(x), domain, list(range(0, 11)), "|x|")
```

Compare each with your hand answer from Section 1. The domains here are finite truncations, so the answers may
differ from the infinite case: where they do, say why.

### Exercise 3.2 — Composition and Inverse

```python
def compose(g, f):
    """g ∘ f as a new function."""
    return lambda x: g(f(x))

def inverse_at(f, domain, y):
    """For a bijection f on domain, the x with f(x) == y."""
    for x in domain:
        if f(x) == y:
            return x
    return None
```

**Task:** Store the permutation from Exercise 1.1(d) in a list, so that `perm[x]` is f(x):
`perm = [0, 3, 1, 4, 2, 5]` (position 0 is unused), and `f = lambda x: perm[x]`. For each y in 1..5, print
`inverse_at(f, [1, 2, 3, 4, 5], y)`, and check against your hand computation. Then check that
`compose(f, lambda y: inverse_at(f, [1, 2, 3, 4, 5], y))` sends every y back to itself.

---

## Section 4 — Reflection (5 min)

1. In Exercise 3.1, did any function change classification between the "hand" analysis (infinite domain) and the
Python analysis (finite truncated domain)? Explain why restricting the domain can change injectivity or
surjectivity.

2. `is_injective` compares every pair of outputs. Connect this to the formal definition of injectivity. How many
comparisons does it make for a domain of size n?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: at least 4 of 6 functions correctly classified with proof
- [ ] Exercise 2.2: at least 2 complete inverse derivations with verification
- [ ] `function_tools.py` running: demonstrate `classify_function` and `inverse_at`

---

