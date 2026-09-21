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

## Section 4 — Python: Function Property Checker (25 min)

Create `function_tools.py`.

### Exercise 4.1 — Injective/Surjective Checker for Finite Domains

```python
def is_injective(f, domain):
    """Check if f: domain -> anything is injective, by brute force."""
    outputs = [f(x) for x in domain]
    return len(outputs) == len(set(outputs))

def is_surjective(f, domain, codomain):
    """Check if f: domain -> codomain is surjective, by brute force."""
    outputs = set(f(x) for x in domain)
    return set(codomain) == outputs

def is_bijective(f, domain, codomain):
    return is_injective(f, domain) and is_surjective(f, domain, codomain)

def classify_function(f, domain, codomain, name="f"):
    inj = is_injective(f, domain)
    sur = is_surjective(f, domain, codomain)
    if inj and sur:
        result = "BIJECTIVE"
    elif inj:
        result = "INJECTIVE ONLY (not surjective)"
    elif sur:
        result = "SURJECTIVE ONLY (not injective)"
    else:
        result = "NEITHER"
    print(f"{name}: {result}")
    return inj, sur
```

**Task:** Add to `function_tools.py`. Test on:

```python
domain = list(range(-10, 11))  # -10 to 10

classify_function(lambda x: x**2, domain, domain, "x^2")
classify_function(lambda x: x+5, domain, [x+5 for x in domain], "x+5 (correct codomain)")
classify_function(lambda x: abs(x), domain, list(range(0,11)), "|x|")
classify_function(lambda x: x**3, domain, [x**3 for x in domain], "x^3 (correct codomain)")
```

For each, compare the program's classification to your hand-derived answer from Section 1 (where applicable — note the domains here are finite truncations, so behavior may differ from the infinite-domain case; discuss any discrepancies).

---

### Exercise 4.2 — Composition and Inverse Finder (Finite Domains)

```python
def compose(g, f):
    """Returns g∘f as a new function."""
    return lambda x: g(f(x))

def find_inverse(f, domain, codomain):
    """
    For a bijective f: domain -> codomain, find and return
    the inverse as a dictionary mapping codomain -> domain.
    Returns None if f is not bijective.
    """
    if not is_bijective(f, domain, codomain):
        return None
    return {f(x): x for x in domain}

# Example
domain = list(range(1, 6))
f = lambda x: 6 - x   # a bijection on {1,...,5}
inv = find_inverse(f, domain, domain)
print(inv)  # should map each f(x) back to x
```

**Task:** Use `find_inverse` to compute the inverse of the permutation from Exercise 1.1(d). Verify it matches your hand computation.

---

## Section 5 — Reflection (5 min)

1. In Exercise 4.1, did any function change classification between the "hand" analysis (infinite domain) and the "Python" analysis (finite truncated domain)? Explain why domain restriction can change injectivity/surjectivity.

2. Why does `is_injective` in the Python code use `len(set(outputs)) == len(outputs)` as the test? Connect this to the formal definition of injectivity.


---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: at least 4 of 6 functions correctly classified with proof
- [ ] Exercise 2.2: at least 2 complete inverse derivations with verification
- [ ] `function_tools.py` running: demonstrate `classify_function` and `find_inverse`

---

*Bring `set_tools.py`, `predicate_tools.py`, and `function_tools.py` to Lab 6 — relations build directly on functions.*
