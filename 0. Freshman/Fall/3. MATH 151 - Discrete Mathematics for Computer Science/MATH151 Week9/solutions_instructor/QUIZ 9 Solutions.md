# MATH 151 — Quiz 9 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 20 points.** All values verified computationally.

---

**Q1. (4 pts)** **Pigeons:** the 20 integers. **Pigeonholes:** the 19 possible remainders
$\{0,1,\ldots,18\}$ on division by 19.

Since $20 > 19$, by the Pigeonhole Principle two integers fall in the same remainder class — that is,
two leave the same remainder. ∎

*Marking: 1 pigeons, 1 pigeonholes, 2 for the argument. A proof without pigeons/pigeonholes named
scores at most 2, as announced in the Quiz 9 Preview.*

*Common error: saying there are 19 remainders $\{1,\ldots,19\}$. The remainders on division by 19 are
$0$ through $18$. The count is right, the set is wrong — deduct 0.5.*

---

**Q2. (4 pts)** $\lfloor300/4\rfloor = 75$, $\lfloor300/9\rfloor = 33$, and the intersection uses
$\mathrm{lcm}(4,9) = 36$, giving $\lfloor300/36\rfloor = 8$.

$$75 + 33 - 8 = \mathbf{100}$$

*(Verified by enumeration.)*

*Marking: 2 for the two counts, 1 for using lcm $=36$, 1 for the answer. Using $4\times9=36$ happens
to be right here because 4 and 9 are coprime — ask in review what would happen with 4 and 6.*

---

**Q3. (4 pts)** Total strings: $26^6$. Strings with **no** vowel: $21^6$ (consonants only).

$$26^6 - 21^6 = 308{,}915{,}776 - 85{,}766{,}121 = \mathbf{223{,}149{,}655}$$

*Marking: 1 for the total, 1 for recognising 21 consonants, 2 for the subtraction and value. A direct
case-split by number of vowels is correct but should be noted in feedback as six times the work.*

---

**Q4. (4 pts)** $D_5 = \mathbf{44}$.

$$P = \frac{D_5}{5!} = \frac{44}{120} = \mathbf{0.3667}$$

which is already within $0.0012$ of $1/e \approx 0.3679$.

*Marking: 2 for $D_5$, 2 for the probability. Accept $11/30$ as an exact form.*

---

**Q5. (4 pts, 2 each)**

**(a) Pigeonhole.** 30 people (pigeons) into 53 weeks (pigeonholes) — and here $30 < 53$, so
**pigeonhole does not apply** and the claim is false. A student who spots this earns full marks plus
a note; a student who answers "pigeonhole" without checking the counts earns 1.

**(b) Inclusion–Exclusion.** A count with two "at least one" conditions, so the complement is a
union.

*This question is a deliberate trap on (a), mirroring PS 8's Part A(b). The lesson is the same:
**verify pigeons > pigeonholes before invoking the principle.** Expect roughly half the class to
miss it; it is worth five minutes in review.*

---

## Grade Distribution Notes

Q5(a) is the discriminator and will lower the mean. That is intended — it tests the one habit that
prevents the most common Pigeonhole error, and students who lose the mark here rarely lose it again.
