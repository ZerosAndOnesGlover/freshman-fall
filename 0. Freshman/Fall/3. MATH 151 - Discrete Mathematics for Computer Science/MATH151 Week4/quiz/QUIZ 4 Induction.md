# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 4 — Mathematical Induction
### Administered: Monday, Week 4 (first 15 minutes of class)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

---

**Instructions:** Closed notes. 15 minutes. Include base case, IH, inductive step, and conclusion.

**Total: 20 points**

---

### Problem 1 (7 points)

Prove by weak induction: for all $n \geq 0$,
$$\sum_{i=0}^{n} 2^i = 2^{n+1} - 1$$

State your base case, induction hypothesis, and inductive step clearly.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Problem 2 (6 points)

Prove by weak induction: for all $n \geq 1$,
$$4 \mid (5^n - 1)$$

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Problem 3 (7 points)

The following is a "proof" that $n < 2^n$ implies... actually, consider this flawed proof and answer the questions below.

**Claim:** For all $n \geq 1$, $n! \geq n^2$.

**"Proof":**
*Base case* ($n=1$): $1! = 1 \geq 1 = 1^2$. ✓

*Base case* ($n=2$): $2! = 2 \geq 4 = 2^2$? No, $2 < 4$. 

*(The student notices this fails but continues anyway.)*

*Inductive step:* Assume $k! \geq k^2$ for some $k \geq 1$.
$$(k+1)! = (k+1)\cdot k! \geq (k+1)\cdot k^2$$
We want $(k+1)k^2 \geq (k+1)^2$, i.e., $k^2 \geq k+1$, which holds for $k \geq 2$.
So $(k+1)! \geq (k+1)^2$ for $k \geq 2$. ✓

Therefore by induction, $n! \geq n^2$ for all $n \geq 1$. ∎

**(a)** (3 pts) Is the claim TRUE or FALSE for all $n \geq 1$? If false, identify the exact value(s) of $n$ where it fails.

&nbsp;

&nbsp;

**(b)** (2 pts) What is the actual error in the "proof" — specifically, where does the base-case/inductive-step structure break down?

&nbsp;

&nbsp;

**(c)** (2 pts) State a corrected theorem (with a corrected starting value $n_0$) that IS true, based on this pattern.

&nbsp;

&nbsp;

---

*End of Quiz 4*
