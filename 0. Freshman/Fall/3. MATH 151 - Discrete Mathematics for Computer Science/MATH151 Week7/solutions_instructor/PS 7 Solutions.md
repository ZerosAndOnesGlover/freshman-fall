# MATH 151 · Week 7
## PS7 Solutions — INSTRUCTOR ONLY

---

## Part A

### A1(a): 4-course meals
$5\times8\times4\times3 = 480$

### A1(b): Password (2 uppercase + 4 digits)
$26\times26\times10\times10\times10\times10 = 676\times10000=6{,}760{,}000$

### A1(c): Divisible by 4 or 6, 1-500
$|A|$(÷4)$=\lfloor500/4\rfloor=125$
$|B|$(÷6)$=\lfloor500/6\rfloor=83$
$|A\cap B|$(÷12, since lcm(4,6)=12)$=\lfloor500/12\rfloor=41$
$|A\cup B|=125+83-41=167$

### A1(d): 8-bit strings starting "11" or ending "00"
Total strings: $2^8=256$.
Start with "11": remaining 6 bits free: $2^6=64$.
End with "00": remaining 6 bits free: $2^6=64$.
Both start "11" AND end "00": remaining 4 middle bits free: $2^4=16$.
By Inclusion-Exclusion: $64+64-16=112$.

### A1(e): 5-digit numbers (first digit ≠0) with at least one digit =7

Total 5-digit numbers: $9\times10\times10\times10\times10=90000$ (first digit 1-9, rest 0-9).

No 7 at all: first digit has 8 choices (1-9 excluding 7), remaining 4 digits have 9 choices each (0-9 excluding 7): $8\times9^4=8\times6561=52488$.

At least one 7: $90000-52488=37512$.

---

## Part B

### B1(a): Arrange 6 books
Order matters, no repetition, all 6 used: $P(6,6)=6!=720$

### B1(b): President/VP/Secretary/Treasurer from 15
Order matters (distinct roles), no repetition: $P(15,4)=15\times14\times13\times12=32760$

### B1(c): 4-person subcommittee from 15 (no roles)
Order doesn't matter, no repetition: $\binom{15}{4}=\dfrac{15\times14\times13\times12}{24}=1365$

### B1(d): 8 snacks from 6 types, repeats allowed, order irrelevant
$\binom{6+8-1}{8}=\binom{13}{8}=\binom{13}{5}=1287$

### B1(e): 7-character strings from {A,B,C}, repetition allowed
Order matters, repetition allowed: $3^7=2187$

### B1(f): Arrangements of "ENGINEERING"
Letters: E(3),N(3),G(2),I(2),R(1). Total 11 letters. Check: E-N-G-I-N-E-E-R-I-N-G → E:3,N:3,G:2,I:2,R:1. Sum: 3+3+2+2+1=11 ✓

$$\frac{11!}{3!3!2!2!1!} = \frac{39916800}{6\times6\times2\times2\times1} = \frac{39916800}{144}=277200$$

### B1(g): 3 distinct toppings from 10, no repeats, order irrelevant
$\binom{10}{3}=120$

### B1(h): 12 identical chairs, 4 distinguishable classrooms
Stars and bars: $\binom{4+12-1}{12}=\binom{15}{12}=\binom{15}{3}=455$

---

## Part C

### C1. Exactly 3 kings in a 5-card hand

Choose 3 of the 4 kings: $\binom{4}{3}=4$.
Choose 2 of the remaining 48 non-king cards: $\binom{48}{2}=1128$.

Multiply (Multiplication Rule — independent sub-selections): $4\times1128=4512$.

---

### C2. At least 4 women in a 6-person committee (8 men, 5 women)

Cases: exactly 4 women, exactly 5 women (can't have 6 women — only 5 exist).

**Exactly 4 women (+2 men):** $\binom{5}{4}\binom{8}{2}=5\times28=140$

**Exactly 5 women (+1 man):** $\binom{5}{5}\binom{8}{1}=1\times8=8$

Total: $140+8=148$

---

### C3. License plates: 3 letters + 3 digits, all distinct within their group

Letters (no repeat): $P(26,3)=26\times25\times24=15600$
Digits (no repeat): $P(10,3)=10\times9\times8=720$

Multiply: $15600\times720=11{,}232{,}000$

---

### C4. 10 people into two UNLABELED groups of 5

First, treat groups as labeled (Group A, Group B): $\binom{10}{5}=252$ ways to choose Group A (Group B is determined as the rest).

But the groups are **unlabeled**, so every split is counted exactly **twice**: choosing a 5-set $S$
as "Group A" and later choosing its complement as "Group A" produce the same unordered partition.
The two halves are always the same size here, so no split is its own complement and the
double-counting is uniform — there is no fixed point to correct for.

Correct for double-counting: $252/2=126$.

---

## Part D

### D1. Coefficient of $x^7y^5$ in $(2x-y)^{12}$

$(2x-y)^{12} = \sum_{k=0}^{12}\binom{12}{k}(2x)^{12-k}(-y)^k$

Need $12-k=7\Rightarrow k=5$.

Term: $\binom{12}{5}(2x)^7(-y)^5 = 792\times128x^7\times(-1)y^5 = -101376\,x^7y^5$

**Coefficient: $-101376$**

---

### D2. $\sum_{k=0}^n\binom{n}{k}3^k=4^n$

By the Binomial Theorem with $x=1,y=3$:
$$(1+3)^n = \sum_{k=0}^n\binom{n}{k}1^{n-k}3^k = \sum_{k=0}^n\binom{n}{k}3^k$$
$$4^n = \sum_{k=0}^n\binom{n}{k}3^k$$ ∎

---

### D3. Combinatorial proof: $r\binom{n}{r}=n\binom{n-1}{r-1}$

**Scenario:** Choose a committee of size $r$ from $n$ people, and designate one member of the committee as chair.

**Count 1 (LHS):** First choose the committee of $r$ people ($\binom{n}{r}$ ways), then choose the chair from among those $r$ members ($r$ ways). By the Multiplication Rule: $\binom{n}{r}\times r = r\binom{n}{r}$.

**Count 2 (RHS):** First choose the chair directly from all $n$ people ($n$ ways). Then choose the remaining $r-1$ committee members from the other $n-1$ people ($\binom{n-1}{r-1}$ ways). By the Multiplication Rule: $n\times\binom{n-1}{r-1}$.

Both counts describe the SAME set of outcomes (a committee of size $r$ with a designated chair), just constructed in a different order. Therefore:
$$r\binom{n}{r} = n\binom{n-1}{r-1}$$ ∎

---

### D4. Row 8 of Pascal's Triangle

Row 8: $\binom{8}{0},\ldots,\binom{8}{8} = 1, 8, 28, 56, 70, 56, 28, 8, 1$

Sum: $1+8+28+56+70+56+28+8+1$

$= 1+8=9$; $9+28=37$; $37+56=93$; $93+70=163$; $163+56=219$; $219+28=247$; $247+8=255$; $255+1=256$

$256 = 2^8$ ✓

---

## Bonus Solutions

### Bonus 1: "COMBINATORICS" with vowels together

Word: C-O-M-B-I-N-A-T-O-R-I-C-S (13 letters).

Letters: C(2), O(2), M(1), B(1), I(2), N(1), A(1), T(1), R(1), S(1). Total: 2+2+1+1+2+1+1+1+1+1=13 ✓

Vowels: O,I,A,O,I → O(2), I(2), A(1) — 5 vowels total.
Consonants: C,M,B,N,T,R,C,S → C(2), M(1), B(1), N(1), T(1), R(1), S(1) — 8 consonants.

**Treat the vowel block as one unit.** We now arrange: [vowel-block] + 8 consonants = 9 "items" total, but consonants have repeats (C appears twice).

Arrangements of 9 items with C repeated twice: $\dfrac{9!}{2!}=\dfrac{362880}{2}=181440$

**Internal arrangements of the vowel block** (O,I,A,O,I — 5 letters with O×2, I×2, A×1):
$$\frac{5!}{2!2!1!}=\frac{120}{4}=30$$

**Total:** $181440\times30 = 5{,}443{,}200$

---

### Bonus 2: Hockey Stick Identity by induction on $n$

**Claim:** $\sum_{i=r}^n\binom{i}{r}=\binom{n+1}{r+1}$ for fixed $r$, all $n\geq r$.

**Proof.** By induction on $n$, for fixed $r\geq0$.

**Base case ($n=r$):** LHS $=\binom{r}{r}=1$. RHS $=\binom{r+1}{r+1}=1$. Equal. ✓

**Inductive step:** Assume $\sum_{i=r}^{k}\binom{i}{r}=\binom{k+1}{r+1}$ for some $k\geq r$. [IH]

We show $\sum_{i=r}^{k+1}\binom{i}{r}=\binom{k+2}{r+1}$.

$$\sum_{i=r}^{k+1}\binom{i}{r} = \left(\sum_{i=r}^{k}\binom{i}{r}\right) + \binom{k+1}{r} = \binom{k+1}{r+1}+\binom{k+1}{r} \quad\text{[by IH]}$$

By Pascal's Rule: $\binom{k+1}{r+1}+\binom{k+1}{r} = \binom{k+2}{r+1}$.

So $\sum_{i=r}^{k+1}\binom{i}{r}=\binom{k+2}{r+1} = \binom{(k+1)+1}{r+1}$. ✓

By induction, the identity holds for all $n\geq r$. ∎

---

## Part E — The Four-Fold Way

### E1. *(4 pts)* The classification table, $n=5$, $r=3$

| | No repetition | Repetition allowed |
|---|---|---|
| **Order matters** | $P(n,r)=\dfrac{n!}{(n-r)!}$ — **60** | $n^r$ — **125** |
| **Order does not matter** | $\binom nr$ — **10** | $\binom{n+r-1}{r}$ — **35** |

*All four verified: $5\cdot4\cdot3=60$; $5^3=125$; $\binom53=10$; $\binom73=35$.*

*Marking: 0.5 per formula, 0.5 per value. The repetition-allowed unordered case
$\binom{n+r-1}{r}$ (stars and bars) is the one most often missed.*

---

### E2. *(4 pts, 2 each)*

**(a) BANANA.** Order matters and letters repeat, but the repeated letters are
**indistinguishable** — this is the *permutations with repetition* case:

$$\frac{6!}{3!\,2!\,1!} = \frac{720}{12} = \mathbf{60}$$

*(Verified by generating all distinct permutations: exactly 60.)*

**(b) Bit strings of length 8 with exactly three 1s.** Order does not matter among the 1s — you are
choosing **which three of the eight positions** hold a 1, without repetition:

$$\binom 83 = \mathbf{56}$$

*Marking: 1 for the correct classification, 1 for the value, each part. (a) is the discriminator —
students who answer $6!=720$ have ignored the repeated letters, and those who answer $\binom63$ have
misclassified it entirely.*

