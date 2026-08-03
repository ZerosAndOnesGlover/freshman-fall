# CS 102 · Quiz 11

**Week 11, Monday, first 15 minutes of lecture · 20 points**
**Covers Week 10** — string matching, suffix arrays. **Not** this week's material.

Closed book. Every number here is exact.

> **This is the last quiz.** **PROJECT 2 is due Friday of Week 12**, and the **FINAL EXAM** is in
> Week 12 and is comprehensive.

---

**Q1.** *(3)* Give the failure function of the pattern `abcabcabd`.

State in one sentence what $f[i]$ means.

---

**Q2.** *(4)* KMP's inner `while` loop can run $\Theta(m)$ times in a single iteration of the outer
loop, and the algorithm is still $\Theta(n + m)$.

Give the potential argument. Name the quantity, say what increases it, and say what the `while` loop
does to it.

---

**Q3.** *(3)* Rabin–Karp compares hashes and then verifies with a string comparison.

- **(a)** *(2)* What does removing the verification change about the algorithm?
- **(b)** *(1)* What determines how often the verification runs?

---

**Q4.** *(3)* Boyer–Moore examines **0.144** characters per text character on a 26-letter alphabet and
**1.490** on a binary alphabet.

Explain the difference in one or two sentences.

---

**Q5.** *(4)* Give the suffix array and the LCP array of `banana`.

Then state the longest repeated substring, and read off which LCP entry gives it.

---

**Q6.** *(3)* You must answer thousands of substring queries against one fixed 3-gigabyte text.

Name the structure you would use, give its build and query costs, and say why KMP is the wrong choice
here.

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 11 · Quiz 11 · © CSE Department*
