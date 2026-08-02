# MATH 141 · Week 4 Overview
## Differentiation Rules

---

## This Week

Week 3 defined the derivative and computed a few from first principles. That is unsustainable —
the limit definition is correct but slow. This week builds the machinery that makes differentiation
mechanical, and then asks what the results *mean*.

| Day | Lecture | Topic |
|---|---|---|
| Monday | 1 | Differentiation Rules: Power, Product, Quotient |
| Tuesday | 2 | The Chain Rule |
| Wednesday | 3 | Higher Derivatives and Rates of Change |
| — | Lab 04 | Rules, Chains, and Motion |

**Quiz 04** at the start of Monday's lecture, covering Week 3.
**Problem Set 4** due at the start of Wednesday's lecture next week.

---

## Learning Objectives

1. Differentiate any elementary combination using power, product, quotient and chain rules
2. Recognise which rule a given expression needs, and in what order
3. Compute higher derivatives and identify their patterns
4. Interpret $f'$ and $f''$ as rate and rate-of-rate in a stated context
5. Distinguish displacement from distance travelled
6. Explain when a derivative approximates a difference, and what controls the error

---

## Key Results

| | |
|---|---|
| Power rule | $\dfrac{d}{dx}x^n = nx^{n-1}$ |
| Product | $(fg)' = f'g + fg'$ |
| Quotient | $\left(\dfrac fg\right)' = \dfrac{f'g-fg'}{g^2}$ |
| Chain | $\dfrac{d}{dx}f(g(x)) = f'(g(x))\,g'(x)$ |
| $n$th derivative of $x^k$ | $\dfrac{k!}{(k-n)!}x^{k-n}$, then $0$ for $n>k$ |
| $\dfrac{d^n}{dx^n}e^x$ | $e^x$ |
| $\dfrac{d^n}{dx^n}\sin x$ | cycles with period 4 |
| Speeding up | $v$ and $a$ share a sign |
| Displacement vs distance | Split at every $v=0$ |

---

## Common Errors

| Error | Correction |
|---|---|
| $(fg)' = f'g'$ | The product rule has **two** terms |
| Forgetting the inner derivative | The chain rule's $g'(x)$ factor is not optional |
| $f^4$ for the fourth derivative | Write $f^{(4)}$ — $f^4$ is the fourth power |
| "Speeding up because $a>0$" | Compare the **signs** of $v$ and $a$ |
| Displacement = distance | They differ whenever direction reverses |

---

## Connections

**Back:** Week 3's limit definition is what these rules replace — each is *proved* from it, and
Wednesday's higher derivatives rest on Week 3's insight that $f'$ is itself a function.

**Forward:** Week 5 applies the chain rule to implicitly defined curves and related rates. Week 6
uses $f'$ and $f''$ to locate extrema and describe shape. Week 12's Taylor polynomials are built
entirely from higher derivatives.

---

*MATH 141 · Week 4 · © CSE Department*
