# MATH 151 · Counting Formulas Reference
## Week 7: Multiplication/Addition Rules, Permutations, Combinations, Binomial Theorem

---

## The Two Fundamental Rules

| Rule | Condition | Formula |
|---|---|---|
| Multiplication (Product) Rule | Sequential/independent steps | $n_1\times n_2\times\cdots\times n_k$ |
| Addition (Sum) Rule | Mutually exclusive alternatives | $n_1+n_2+\cdots+n_k$ |

**If categories in an Addition Rule problem overlap:** use Inclusion-Exclusion instead:
$$|A\cup B|=|A|+|B|-|A\cap B|$$

---

## The Four Counting Scenarios

| Order Matters | Repetition | Name | Formula |
|---|---|---|---|
| Yes | No | Permutation | $P(n,r)=\dfrac{n!}{(n-r)!}$ |
| No | No | Combination | $\dbinom{n}{r}=\dfrac{n!}{r!(n-r)!}$ |
| Yes | Yes | Permutation w/ repetition | $n^r$ |
| No | Yes | Combination w/ repetition | $\dbinom{n+r-1}{r}$ |

### Diagnostic Questions

1. Does swapping two chosen items produce a different outcome? → Order matters (permutation-type)
2. Can the same item/type be chosen more than once? → Repetition allowed

---

## Special Cases

| Scenario | Formula |
|---|---|
| Permutations of all $n$ distinct objects | $n!$ |
| Number of functions $f:A\to B$ (finite) | $|B|^{|A|}$ |
| Number of subsets of an $n$-set | $2^n$ |
| Arrangements with $n_1,\ldots,n_k$ indistinguishable groups | $\dfrac{n!}{n_1!n_2!\cdots n_k!}$ |

---

## Complementary Counting

$$|\text{at least one}| = |\text{Total}| - |\text{none}|$$

Use whenever direct counting of "at least one X" is harder than counting "no X at all."

---

## Binomial Coefficient Properties

| Property | Formula |
|---|---|
| Symmetry | $\binom{n}{r}=\binom{n}{n-r}$ |
| Boundary | $\binom{n}{0}=\binom{n}{n}=1$ |
| Pascal's Rule | $\binom{n}{r}=\binom{n-1}{r-1}+\binom{n-1}{r}$ |
| Row sum | $\sum_{r=0}^n\binom{n}{r}=2^n$ |
| Alternating sum | $\sum_{r=0}^n(-1)^r\binom{n}{r}=0$ ($n\geq1$) |
| Hockey Stick | $\sum_{i=r}^n\binom{i}{r}=\binom{n+1}{r+1}$ |
| Vandermonde | $\binom{m+n}{r}=\sum_{k=0}^r\binom{m}{k}\binom{n}{r-k}$ |

---

## The Binomial Theorem

$$(x+y)^n = \sum_{k=0}^n\binom{n}{k}x^{n-k}y^k$$

**To find the coefficient of $x^{n-k}y^k$:** it is $\binom{n}{k}$.

**Useful substitutions:**
| Substitution | Result |
|---|---|
| $x=y=1$ | $2^n=\sum\binom{n}{k}$ |
| $x=1,y=-1$ | $0=\sum(-1)^k\binom{n}{k}$ ($n\geq1$) |
| $x=1,y=c$ | $(1+c)^n=\sum\binom{n}{k}c^k$ |

---

## Stars and Bars — Visual Setup

To distribute $r$ identical items among $n$ distinguishable categories (repetition allowed, order irrelevant):

Represent as a string of $r$ stars and $n-1$ bars. The number of such strings is:
$$\binom{n+r-1}{r} = \binom{n+r-1}{n-1}$$

**Equivalent formulation:** number of non-negative integer solutions to $x_1+x_2+\cdots+x_n=r$ is $\binom{n+r-1}{r}$.

---

## Combinatorial Proof Technique

To prove an identity like $A=B$ where both sides are counting formulas:

1. Describe a single combinatorial scenario (a set of objects to count).
2. Show that the LHS counts this scenario one way.
3. Show that the RHS counts the SAME scenario a different way (often via case-splitting with the Addition Rule).
4. Conclude $A=B$ since both count the same set.

**This is different from an algebraic proof** (manipulating factorial expressions) — combinatorial proofs are often more illuminating and are frequently requested explicitly.

---

## Common Errors to Avoid

| Error | Correction |
|---|---|
| Confusing $P(n,r)$ and $\binom{n}{r}$ | $P(n,r)=\binom{n}{r}\times r!$ — permutations count $r!$ times more than combinations |
| Using Addition Rule on overlapping categories | Check disjointness first; use Inclusion-Exclusion if categories overlap |
| Forgetting "no repetition" reduces choices at each step | Position 2 has one fewer choice than position 1 when no repeats allowed |
| Directly counting "at least one" | Almost always easier via complementary counting |
| Misapplying stars-and-bars to a "no repetition" problem | Stars and bars is ONLY for repetition-allowed, order-irrelevant scenarios |
| Treating labeled and unlabeled groupings the same | Splitting into "Group A vs B" (labeled) differs from unlabeled group division — divide by extra symmetry factor for unlabeled cases |
