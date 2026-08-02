# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 4 — Scope Preview
### Quiz administered: Monday, Week 4 (first 15 minutes of lecture)

---

**Coverage:** Weeks 3 and 4 material:
- Week 3: Mathematical induction — weak and strong
- Week 4: Sets — operations, power sets, Cartesian products (covered next week)

---

## What You Must Know Cold for Week 3 Material

### 1. Weak Induction Structure

Every proof must have all four components — missing any one loses significant credit:

| Component | What it contains |
|---|---|
| **Statement** | "By mathematical induction on n" + state P(n) clearly |
| **Base case** | Verify P(n₀) by direct computation. Show both sides equal. |
| **Inductive step** | "Let k ≥ n₀. Assume P(k) [write it out]. We prove P(k+1) [write it out]." |
| **Conclusion** | "By the Principle of Mathematical Induction, P(n) holds for all n ≥ n₀." |

### 2. The IH Must Be Stated Explicitly

The induction hypothesis is NOT "assume the formula works" — it is a specific mathematical statement. Write it out completely every time.

**Wrong:** "Assume the formula holds for k."
**Right:** "Assume $\sum_{i=1}^{k} i = \frac{k(k+1)}{2}$."

### 3. Strong vs Weak

Know when strong induction is needed:
- Recurrence uses more than one previous term (Fibonacci-style)
- Algorithm recurses on sub-input that is not exactly n−1
- "Every n has property X" where proving for n depends on arbitrary smaller values

### 4. Classic Results to Know

| Claim | Technique | Key IH Application |
|---|---|---|
| $\sum_{i=1}^n i = n(n+1)/2$ | Weak | Peel off last term, apply IH |
| $\sum_{i=0}^n r^i = (r^{n+1}-1)/(r-1)$ | Weak | Peel off last term |
| $3 \mid (4^n - 1)$ | Weak | Write $4^{k+1} - 1 = 4(4^k - 1) + 3$ |
| $2^n > n$ | Weak | $2^{k+1} = 2 \cdot 2^k > 2k \geq k+1$ |
| Every $n \geq 2$ has a prime factor | Strong | Factor n = ab, apply IH to a and b |
| $F_n < 2^n$ | Strong (2 base cases) | $F_{k+1} = F_k + F_{k-1} < 2^k + 2^{k-1} < 2^{k+1}$ |

### 5. Error Recognition

Know these errors by name:
- **Missing base case:** inductive step alone proves nothing
- **Incorrect base case:** claiming 1=1 when they aren't
- **Circular IH:** assuming P(k+1) to prove P(k+1)
- **Wrong IH form:** "assume for all n" instead of "assume for some fixed k"
- **False base case + valid step:** the horse paradox — step breaks at k=1

---

## Sample Quiz 4 Problems (Week 3 portion)

**Problem 1.** (5 pts) Prove by induction: $\sum_{i=0}^{n} 2^i = 2^{n+1} - 1$ for all $n \geq 0$.

**Problem 2.** (5 pts) Prove by induction: $4 \mid (5^n - 1)$ for all $n \geq 0$.

**Problem 3.** (5 pts) The sequence $a_1 = 3$, $a_n = 2a_{n-1} - 1$ for $n \geq 2$. Conjecture a closed form and prove it by induction.

**Problem 4.** (5 pts) Identify the error in a given broken induction proof.

---

## Study Recommendations

1. **Write three proofs from memory.** Gauss's formula, geometric series, and one divisibility claim. Do not look at notes. Check yourself after.

2. **Practice the IH statement.** For every claim P(n), write out what P(k) and P(k+1) look like explicitly before you start the proof.

3. **Do PS3 completely.** It covers every type that can appear on the quiz.

4. **Know the horse paradox cold.** Quiz questions regularly ask you to find the error in a flawed induction proof — this is the canonical example.

5. **Time yourself.** A complete weak induction proof of a summation formula should take about 5 minutes. If it takes more, practice more.
