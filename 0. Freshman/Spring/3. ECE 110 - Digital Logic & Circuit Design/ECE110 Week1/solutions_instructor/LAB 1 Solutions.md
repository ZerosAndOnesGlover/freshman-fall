# ECE 110 · Digital Logic
## Lab 1 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab in both languages.

---

> **Revised 2026-09-23.** Verilog is taught in Week 10; this lab's Verilog part is now a Python
> simulation of the same circuit, and the expected counts are unchanged. The reference code below was
> run for this revision (Python 3.14).

## Part A — The Python Checker (25 pts)

### A1 (10)

`check` must return a **counterexample**, not just `False`. A boolean-only return costs 3 of the 10 — the counterexample is what makes Part C tractable.

### A2 (10)

$$\textbf{16 identities checked, 0 failures.}$$

*(Verified.)*

*Marking: 6 for the runs, **4 for reporting the count.***

### A3 (5)

$$\overline{AB} = \overline A\,\overline B \quad\text{FAILS, first counterexample } (A,B) = (1,0)$$

Left side $\overline{1\cdot0} = \overline0 = 1$; right side $\overline1\cdot\overline0 = 0\cdot1 = 0$.

**Correct law:** $\overline{AB} = \overline A + \overline B$.

*(Accept $(0,1)$ too — search order decides which appears first.)*

---

## Part B — A Second, Independent Checker (30 pts)

### B1 (15)

Reference, all sixteen A2 identities on packed truth-table columns:

```python
A, B, C = 0b11110000, 0b11001100, 0b10101010
M = 0xFF
def N(x): return ~x & M
ids = [(A|0, A), (A&M, A), (A|M, M), (A&0, 0), (A|A, A), (A&A, A), (A|N(A), M), (A&N(A), 0),
       (N(N(A)), A), (A|(A&B), A), (A&(A|B), A), (A&(B|C), (A&B)|(A&C)), (A|(B&C), (A|B)&(A|C)),
       (N(A&B), N(A)|N(B)), (N(A|B), N(A)&N(B)), ((A&B)|(N(A)&C)|(B&C), (A&B)|(N(A)&C))]
print(len(ids), "identities,", sum(l != r for l, r in ids), "failures")   # 16 identities, 0 failures
```

$$\textbf{0 failures.}$$

*Marking: 10 working checker, 5 for the failure count printed. **Forgetting the `& 0xFF` on NOT**
makes every identity with a complement fail — the commonest error, and a good one, because B2 then
catches it.*

### B2 (8)

**Both checkers report 0 failures on the same 16 identities.** *(Verified.)*

*Marking: 4 both counts, 4 for stating they agree. **If a student's checkers disagreed and they
diagnosed it, award full marks** — that is the lab working as intended.*

### B3 (7)

Breaking the distributive law in either checker — writing `(A&B)|(A|C)` for `(A&B)|(A&C)` — makes it fail on
three rows (the row-by-row checker reports them individually; the integer checker shows
`0b...` values that differ in three bits):

```
  FAIL distributive * over + at a=0 b=0 c=1  (0 vs 1)
  FAIL distributive * over + at a=0 b=1 c=1  (0 vs 1)
  FAIL distributive * over + at a=1 b=0 c=0  (0 vs 1)
  failures: 3
```

*(Measured.)*

**Note it fails on three of the eight assignments, not one.** A student who expected a single failing row and got three has learned something useful: **a broken identity is usually broken over a whole region of the input space**, which is why a single spot-check is not a test.

*Marking: 7. **The point is that the disagreement is detected**, not which identity was broken or how many rows failed.*

---

## Part C — Three Claims (25 pts)

| | claim | verdict |
|---|---|---|
| **C1** | $A\oplus B = A\overline B + \overline AB$ | **TRUE** |
| **C2** | $\overline{A\oplus B} = \overline A\oplus\overline B$ | **FALSE** |
| **C3** | $A\oplus(B\oplus C) = (A\oplus B)\oplus C$ | **TRUE** |

*(All verified.)*

### C2 is the false one

**Counterexample $(A,B) = (0,0)$:** left side $\overline{0\oplus0} = \overline0 = 1$; right side $1\oplus1 = 0$.

**What is actually true:**

$$\overline A \oplus \overline B \;=\; A\oplus B \qquad\text{(the two complements cancel)}$$
$$\overline{A\oplus B} \;=\; A\oplus\overline B \;=\; \overline A\oplus B$$

*(Both verified.)*

> **Complementing *one* input inverts XOR; complementing *both* leaves it alone.** This is the fact
> behind the controlled-inverter trick in Week 6's ALU, where one XOR input is the subtract control —
> so a student who gets C2 right this week has already met the ALU's central idea.

*Marking: 8 + 8 + 9. **For C2, 4 of the 9 are the counterexample and 5 are the corrected statement.** A student who says only "C2 is false" earns 4.*

---

## Part D — Canonical Forms and Cost (20 pts)

### D1 (6)

$$F = \sum m(1,3,5,6,7) = \overline A\,\overline BC + \overline ABC + A\overline BC + AB\overline C + ABC$$

**5 terms, 15 literals.** *(Generated programmatically.)*

*Marking: 6, but **deduct 3 if written out by hand** rather than generated — the exercise is the generation.*

### D2 (6)

**$F = C+AB$ agrees on all 8 rows.** *(Verified.)*

| form | terms | literals |
|---|---:|---:|
| canonical | 5 | 15 |
| minimal | 2 | **3** |

$$\text{literal ratio } = 15/3 = \mathbf{5\times}$$

### D3 (8)

**Stating the convention first is 3 of the 8 marks.** The reference convention: 2-input AND/OR gates only, so an $n$-literal product needs $n-1$ ANDs; one inverter per *distinct* complemented variable, shared across terms.

| form | NOT | AND | OR | **total** |
|---|---:|---:|---:|---:|
| canonical SOP | 3 | 10 | 4 | **17** |
| minimal $C+AB$ | 0 | 1 | 1 | **2** |

*(Counted under the stated convention.)*

$$\boxed{17 \to 2 \text{ gates, an } 8.5\times \text{ reduction}}$$

> **Note the gate ratio (8.5×) is larger than the literal ratio (5×)** — because minimisation removed
> all three inverters as well as shortening the terms. **Literals are a proxy for cost; gates are
> closer to the cost.** Week 4 will minimise literals because that is what the method produces, and
> this table is why that is a reasonable stand-in without being the real thing.

*Marking: 3 convention, 3 counts, 2 for comparing the two ratios. **A student who counts gates without stating a convention earns 0 of the first 3**, because the number is meaningless without it.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 30 |
| C | 25 |
| D | 20 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A1's `check` returns a **counterexample**
2. A2 reports **15 identities, 0 failures**
3. A3 gives $(1,0)$ or $(0,1)$
4. **B1 uses `!==`, not `!=`**
5. B2 states that both tools agree, with both counts
6. B3 shows a detected disagreement
7. **C2 identified as false**, with counterexample and correction
8. D1 generated, not hand-written
9. **D3 states its counting convention before counting**

---

## Note for the Debrief

**Open on the method, because this is the lab that establishes it.**

> **You verified fifteen identities in two languages that share no code, and both said zero
> failures.** That is not the same as being sure — but it is a great deal better than one tool
> agreeing with itself, and it is the standard this course will hold to every week.
>
> **Then Part C handed you three claims and told you one was false.** Nobody in this room could tell
> which by looking. **The checker could, in a millisecond, and it also handed you the
> counterexample.**

Then the cost point:

> **Part D is the first number you have put on the word "better".** The same function: seventeen
> gates, or two. **Nothing about the function changed** — only how you wrote it down.
>
> **Next week those gates stop being symbols and become hardware**, and in Week 4 you get a
> systematic way to find the two-gate version instead of noticing it.

---

*ECE 110 · Week 1 · Lab 1 Solutions · Instructor Only*
