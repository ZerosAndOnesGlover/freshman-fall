# MATH 151 — Discrete Mathematics for Computer Science
## Lab 2 — Proof Workshop: Writing, Critiquing, and Fixing Proofs
### Wednesday, Week 2 | Duration: 2 hours

---

**Lab Objectives:**
1. Practice writing direct proofs, contrapositive proofs, and contradiction proofs from scratch
2. Develop the skill of reading and critiquing proofs for logical errors
3. Fix broken proofs — a skill as important as writing them
4. Recognize which technique fits which problem
5. Build fluency in mathematical prose style

**Materials:** Pencil, paper. No computers needed for Sections 1–3. Section 4 is optional extension.

---

## Section 1 — Proof Technique Identification (20 min)

Before writing a proof, the most important decision is which technique to use. For each theorem below, do the following — **do not write the proof yet**:

(i) Identify what P and Q are in the form P → Q.
(ii) Write the contrapositive ¬Q → ¬P in plain English.
(iii) Write what "assume for contradiction" would look like — i.e., state P ∧ ¬Q explicitly.
(iv) Choose: direct, contrapositive, or contradiction? Justify in one sentence.

---

**(1.1)** For any integer n, if n is divisible by 6, then n is divisible by 3.

**(1.2)** For any integer n, if n² is divisible by 5, then n is divisible by 5.

**(1.3)** For any integers a and b, if a + b is odd, then exactly one of a, b is even.

**(1.4)** √11 is irrational.

**(1.5)** For any real numbers x and y, if xy > 0, then either both x and y are positive, or both are negative.

**(1.6)** For any integer n, if 4 | (n² − 1), then n is odd.

**(1.7)** There is no integer n such that n ≡ 2 (mod 4) and n ≡ 0 (mod 6) and n < 10, except n = 6.
*(Careful — this is not a universal implication. What form is it?)*

---

## Section 2 — Proof Writing from Scratch (40 min)

Write complete proofs for the following. Use correct mathematical prose. State your technique at the start of each proof.

---

### Exercise 2.1 — Direct Proofs

**(a)** Prove: If n is an odd integer, then 8 | (n² − 1).

*Hint:* Write n = 2k+1, expand n²−1, and factor carefully.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**(b)** Prove: The sum of any three consecutive integers is divisible by 3.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**(c)** Prove: If a | b, then a | (b² − b).

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.2 — Contrapositive Proofs

**(a)** Prove: For any integer n, if n² − 1 is even, then n is odd.

*Hint:* The contrapositive says: if n is even, then n² − 1 is odd. Try that direction.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**(b)** Prove: For any integers a and b, if a² + b² is odd, then a + b is odd.

*Hint:* Think about what parity combinations of (a,b) make a²+b² odd. The contrapositive will split into cases.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.3 — Proof by Contradiction

**(a)** Prove: √13 is irrational.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**(b)** Prove: There is no greatest odd integer.

*Hint:* Assume there is a greatest odd integer N. Derive a contradiction by constructing a larger odd integer.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

## Section 3 — Proof Critique and Repair (35 min)

Each of the following is a flawed proof. For each:
(i) Identify every logical error. Be specific — quote the exact sentence that is wrong.
(ii) Explain why it is wrong.
(iii) Write a correct proof.

---

### Flawed Proof 3.1

**Claim:** If n² is divisible by 4, then n is divisible by 4.

**"Proof":** Assume n² is divisible by 4. Then n² = 4k. So n = 2√k. Since n is an integer, √k must be an integer, say √k = m. Then k = m² and n = 2m. Thus n = 2m, which means 4 | n... well, 2 | n, so since 4 | n², we must also have 4 | n. ∎

**Errors:**

&nbsp;

&nbsp;

**Correct proof or disproof:**

&nbsp;

&nbsp;

&nbsp;

&nbsp;

*(Before writing a proof, check: is the claim actually true? Test n = 2.)*

---

### Flawed Proof 3.2

**Claim:** For any integer n, if n is odd, then n² + n + 1 is odd.

**"Proof":** Assume n is odd. Then n² is odd (proved in class) and n is odd, so n² + n is even (odd + odd = even), so n² + n + 1 is odd (even + 1). ∎

**Errors:**

&nbsp;

&nbsp;

**Is the proof repairable, or is the claim false?**

&nbsp;

&nbsp;

---

### Flawed Proof 3.3

**Claim:** For any integers a and b, if a | b and b | a, then a = b.

**"Proof":** Assume a | b and b | a. Then b = ja and a = kb for some integers j and k. Substituting: b = j(kb) = jkb. Dividing by b: 1 = jk. Since j and k are integers and jk = 1, we must have j = k = 1. Therefore b = 1·a = a. ∎

**Errors:**

&nbsp;

&nbsp;

**Correct proof or corrected claim:**

&nbsp;

&nbsp;

&nbsp;

*(Hint: Is the claim true? Test a = 3, b = −3.)*

---

### Flawed Proof 3.4

**Claim:** For any real number x, if x² = x, then x = 1.

**"Proof":** Assume x² = x. Dividing both sides by x: x = 1. Therefore x = 1. ∎

**Errors:**

&nbsp;

&nbsp;

**Correct proof:**

&nbsp;

&nbsp;

&nbsp;

---

### Flawed Proof 3.5

**Claim:** √2 + √2 = √4 = 2, so √2 is rational.

**"Errors" in the "claim":** *(This one is different — the arithmetic is correct. What is wrong with the logical argument that √2 must be rational?)*

&nbsp;

&nbsp;

---

## Section 4 — Extension: Proof Gallery (remaining time)

If you finish early, attempt these harder proofs. Work in pairs if you wish.

**Gallery Problem 1:** Prove that there are infinitely many integers n such that n² + 1 is not prime.

*(Hint: This is an existence claim — you need to produce infinitely many such n. Try n = km for various values.)*

**Gallery Problem 2:** Prove or disprove: For any prime p > 2, p² − 1 is divisible by 8.

*(Hint: Every prime > 2 is odd. Write p = 2k+1 and compute p²−1.)*

**Gallery Problem 3:** Prove by contradiction: log₂ 6 is irrational.

*(Hint: Combine the idea from log₂ 3 and log₂ 5 proofs. If 2^(p/q) = 6 then 2^p = 6^q = 2^q · 3^q.)*

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: technique identification complete for at least 5 of 7 problems, with justification
- [ ] Exercise 2.1(a): correct proof of 8 | (n²−1) with all algebra shown
- [ ] Exercise 2.2(a) or 2.2(b): complete contrapositive proof
- [ ] Exercise 2.3(a): complete proof that √13 is irrational
- [ ] Section 3: at least 3 of 5 flawed proofs critiqued and corrected
- [ ] Verbal: explain to your TA in one sentence when you would choose contradiction over contrapositive

---

*Bring PS2 questions to next lab — the TA will hold a proof office hour at the start of Lab 3.*
