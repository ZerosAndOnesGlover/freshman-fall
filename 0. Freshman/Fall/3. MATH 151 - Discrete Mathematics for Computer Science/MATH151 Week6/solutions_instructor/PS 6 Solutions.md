# MATH 151 — Week 6
## PS6 Solutions — INSTRUCTOR ONLY

---

## Part A

### A1(a): $R=\{(a,b)\in\mathbb{Z}\times\mathbb{Z} : a\geq b\}$

**Reflexive:** $a\geq a$ always true. YES. Proof: for any $a$, $a\geq a$ holds trivially.

**Symmetric:** Counterexample: $(3,1)\in R$ (3≥1) but $(1,3)\notin R$ (1≥3 false). NOT symmetric.

**Antisymmetric:** Assume $a\geq b$ and $b\geq a$. Then $a=b$ (standard property of order on ℤ). YES.

**Transitive:** Assume $a\geq b$ and $b\geq c$. Then $a\geq c$ (transitivity of ≥). YES.

**Summary:** Reflexive, antisymmetric, transitive → this is a (total) partial order.

---

### A1(b): $R=\{(a,b) : \gcd(a,b)=1\}$ on $\mathbb{Z}^+$

**Reflexive:** Need $\gcd(a,a)=1$. But $\gcd(a,a)=a$. This is 1 only when $a=1$. Counterexample: $a=2$: $\gcd(2,2)=2\neq1$. NOT reflexive.

**Symmetric:** $\gcd(a,b)=\gcd(b,a)$ always (gcd is symmetric by definition). YES.

**Antisymmetric:** Counterexample: $\gcd(2,3)=1$ and $\gcd(3,2)=1$, both in R, but $2\neq3$. NOT antisymmetric.

**Transitive:** Counterexample: $\gcd(2,3)=1$, $\gcd(3,4)=1$, but $\gcd(2,4)=2\neq1$. NOT transitive.

**Summary:** Only symmetric.

---

### A1(c): $A=\{1,2,3,4,5\}$, $R=\{(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(2,1),(3,4)\}$

**Reflexive:** All 5 self-loops present. YES.

**Symmetric:** Check each non-diagonal pair: $(1,2)$ and $(2,1)$ both present ✓. $(3,4)$ present but $(4,3)$ NOT present. NOT symmetric.

**Antisymmetric:** We have both $(1,2)$ and $(2,1)$ with $1\neq2$ — violates antisymmetry. NOT antisymmetric.

**Transitive:** Check: $(1,2)\in R,(2,1)\in R\Rightarrow$ need $(1,1)\in R$ ✓. $(2,1)\in R,(1,2)\in R\Rightarrow$ need $(2,2)\in R$ ✓. $(3,4)\in R$, but $4$ has no outgoing pairs except $(4,4)$; $(3,4),(4,4)\Rightarrow$ need $(3,4)\in R$ ✓ (already have it). No other chains to check (1,2 only connect to each other and themselves). YES transitive.

**Summary:** Reflexive, transitive, NOT symmetric, NOT antisymmetric.

---

### A1(d): $R=\{(A,B) : A\cap B\neq\emptyset\}$ on $\mathcal{P}(\{1,2,3\})$

**Reflexive:** Need $A\cap A\neq\emptyset$, i.e., $A\neq\emptyset$. Counterexample: $A=\emptyset$: $\emptyset\cap\emptyset=\emptyset$, so $(\emptyset,\emptyset)\notin R$. NOT reflexive.

**Symmetric:** $A\cap B=B\cap A$ always. YES.

**Antisymmetric:** Counterexample: $A=\{1\}$, $B=\{1,2\}$. $A\cap B=\{1\}\neq\emptyset$, so $(A,B)\in R$. Also $B\cap A=\{1\}\neq\emptyset$, so $(B,A)\in R$. But $A\neq B$. NOT antisymmetric.

**Transitive:** Counterexample: $A=\{1\}$, $B=\{1,2\}$, $C=\{2\}$. $A\cap B=\{1\}\neq\emptyset$ ✓. $B\cap C=\{2\}\neq\emptyset$ ✓. But $A\cap C=\emptyset$. NOT transitive.

**Summary:** Only symmetric.

---

## Part B

### B1(a): $a\sim b\iff a\equiv b\pmod4$

**Reflexive:** $a-a=0$, and $4\mid0$. YES.

**Symmetric:** If $4\mid(a-b)$, then $a-b=4k$, so $b-a=4(-k)$, and $-k\in\mathbb{Z}$. YES.

**Transitive:** If $4\mid(a-b)$ and $4\mid(b-c)$: $a-b=4k_1$, $b-c=4k_2$. Sum: $a-c=4(k_1+k_2)$. YES.

**Equivalence classes:**
$[0]=\{\ldots,-8,-4,0,4,8,\ldots\}$
$[1]=\{\ldots,-7,-3,1,5,9,\ldots\}$
$[2]=\{\ldots,-6,-2,2,6,10,\ldots\}$
$[3]=\{\ldots,-5,-1,3,7,11,\ldots\}$

---

### B1(b): Same distance from origin, on $\mathbb{R}^2-\{(0,0)\}$

$(x_1,y_1)\sim(x_2,y_2)\iff x_1^2+y_1^2=x_2^2+y_2^2$

**Reflexive:** $x^2+y^2=x^2+y^2$ trivially. YES.

**Symmetric:** If $x_1^2+y_1^2=x_2^2+y_2^2$, then $x_2^2+y_2^2=x_1^2+y_1^2$ (equality is symmetric). YES.

**Transitive:** If $x_1^2+y_1^2=x_2^2+y_2^2$ and $x_2^2+y_2^2=x_3^2+y_3^2$, then $x_1^2+y_1^2=x_3^2+y_3^2$ (equality is transitive). YES.

**Equivalence classes:** each class is a circle of radius $r>0$ centered at the origin: $[(x_0,y_0)] = \{(x,y) : x^2+y^2 = x_0^2+y_0^2\}$ — a circle through $(x_0,y_0)$.

---

### B1(c): Same number of a's, on strings over $\{a,b\}$

**Reflexive:** $s$ has the same number of a's as itself. YES.

**Symmetric:** If $s$ has $k$ a's and $t$ has $k$ a's, this is symmetric trivially (equality of counts). YES.

**Transitive:** If $s,t$ have equal a-counts, and $t,u$ have equal a-counts, then $s,u$ have equal a-counts (transitivity of numerical equality). YES.

**Equivalence classes:** $[s]=\{t : t$ has exactly $k$ a's$\}$ where $k$ is the number of a's in $s$ — one class per non-negative integer $k$.

---

### B1(d): Rational number construction

Full proof given in Thursday's lecture (Section 7). Reproduce here:

**Reflexive:** $(p,q)\sim(p,q)$ requires $pq=qp$ — true by commutativity. ✓

**Symmetric:** Assume $ps=qr$. Then $rq=sp$ (rearranged by commutativity), i.e., $(r,s)\sim(p,q)$. ✓

**Transitive:** Assume $ps=qr$ and $ru=st$. Multiply first by $u$: $psu=qru$. Substitute $ru=st$: $psu=qst$. Since $s\neq0$, divide by $s$: $pu=qt$, i.e., $(p,q)\sim(t,u)$. ✓

Equivalence relation. ∎ (Equivalence classes are exactly the rational numbers.)

---

### B2. Classes for B1(a)

$[0]=\{n\in\mathbb{Z}:4\mid n\}$, representatives: $0,4,-4$ (or $0,4,8$)
$[1]=\{n\in\mathbb{Z}:4\mid(n-1)\}$, representatives: $1,5,-3$
$[2]=\{n\in\mathbb{Z}:4\mid(n-2)\}$, representatives: $2,6,-2$
$[3]=\{n\in\mathbb{Z}:4\mid(n-3)\}$, representatives: $3,7,-1$

---

## Part C

### C1. Partition $\{\{1,4,7\},\{2,5\},\{3,6,8\}\}$ on $A=\{1,\ldots,8\}$

**(a)** The equivalence relation includes all pairs $(a,b)$ where $a,b$ are in the same part:

From $\{1,4,7\}$: $(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)$ — 9 pairs
From $\{2,5\}$: $(2,2),(2,5),(5,2),(5,5)$ — 4 pairs
From $\{3,6,8\}$: $(3,3),(3,6),(3,8),(6,3),(6,6),(6,8),(8,3),(8,6),(8,8)$ — 9 pairs

Total: $R$ = the union of all these, 22 pairs total.

**(b)** Spot checks:
- Reflexive: $(1,1)\in R$ ✓, $(5,5)\in R$ ✓, $(8,8)\in R$ ✓ — all self-loops present since every part contributes its own diagonal pairs.
- Symmetric: $(1,4)\in R$ and $(4,1)\in R$ ✓ both present. $(3,8)\in R$ and $(8,3)\in R$ ✓.
- Transitive: $(1,4)\in R,(4,7)\in R\Rightarrow(1,7)\in R$ ✓ (present). $(3,6)\in R,(6,8)\in R\Rightarrow(3,8)\in R$ ✓ (present).

All spot checks pass, consistent with the Fundamental Theorem (any partition-derived relation is automatically an equivalence relation).

---

### C2. $a\sim b \iff [a]=[b]$

**Proof.**

$(\rightarrow)$ Assume $a\sim b$. We show $[a]=[b]$.

Let $x\in[a]$, so $x\sim a$. Since $a\sim b$, by transitivity $x\sim b$, so $x\in[b]$. Thus $[a]\subseteq[b]$.

By symmetry, $b\sim a$. Let $y\in[b]$, so $y\sim b$. Since $b\sim a$, by transitivity $y\sim a$, so $y\in[a]$. Thus $[b]\subseteq[a]$.

Therefore $[a]=[b]$.

$(\leftarrow)$ Assume $[a]=[b]$. Since $a\in[a]$ (by reflexivity, $a\sim a$), and $[a]=[b]$, we have $a\in[b]$, meaning $a\sim b$.

Both directions proven. ∎

---

## Part D

### D1(a): $A\preceq B\iff A\subseteq B$ on $\mathcal{P}(\{1,2,3,4\})$

**Reflexive:** $A\subseteq A$. YES.
**Antisymmetric:** $A\subseteq B\land B\subseteq A\Rightarrow A=B$ (Week 4). YES.
**Transitive:** $A\subseteq B\land B\subseteq C\Rightarrow A\subseteq C$ (Week 4). YES.

**Partial order: YES.** **Total: NO** — e.g., $\{1\}$ and $\{2\}$ are incomparable.

---

### D1(b): Divisibility on $\mathbb{Z}^+$

Reflexive, antisymmetric, transitive — all proved in Friday's lecture (Example 1).

**Partial order: YES.** **Total: NO** — e.g., 4 and 6 incomparable.

---

### D1(c): $(a,b)\preceq(c,d)\iff a\leq c$ (ignoring second coordinate)

**Reflexive:** $a\leq a$. YES.

**Antisymmetric:** Counterexample: $(1,5)$ and $(1,9)$. $(1,5)\preceq(1,9)$ since $1\leq1$. Also $(1,9)\preceq(1,5)$ since $1\leq1$. But $(1,5)\neq(1,9)$. NOT antisymmetric.

**Transitive:** If $a\leq c$ and $c\leq e$, then $a\leq e$. YES.

**NOT a partial order** (fails antisymmetry — this is only a **preorder**, a weaker structure covered in some advanced courses).

---

### D1(d): Lexicographic order on strings

**Reflexive:** $s\preceq s$ (same string, trivially in lex order). YES.
**Antisymmetric:** if $s\preceq t$ and $t\preceq s$ lexicographically, then $s=t$ (standard property). YES.
**Transitive:** standard property of lexicographic comparison. YES.

**Partial order: YES.** **Total: YES** — any two strings ARE comparable in lexicographic order (one always precedes or equals the other). This is a total order.

---

### D2. Divisibility poset on $\{1,\ldots,12\}$

**(a) Covering relations:**
$1\lessdot2,\ 1\lessdot3,\ 1\lessdot5,\ 1\lessdot7,\ 1\lessdot11$ (primes covered directly by 1)
$2\lessdot4,\ 2\lessdot6,\ 2\lessdot10$
$3\lessdot6,\ 3\lessdot9$
$4\lessdot8,\ 4\lessdot12$
$5\lessdot10$
$6\lessdot12$

(Note: $2\lessdot12$? No — 4 or 6 intermediate. $3\lessdot12$? No — 6 intermediate. $1\lessdot4$? No — 2 intermediate. Etc. — all non-covering pairs correctly excluded.)

**(b) Maximal elements:** elements with nothing above them in {1,...,12}: 7, 8, 9, 10, 11, 12. (Check: is there anything in the set divisible by 7 other than 7? No, 14>12. By 8? No, 16>12. By 9? No. By 10? No. By 11? No. By 12? No, itself only.)

**Minimal elements:** just 1 (divides everything, nothing divides into 1 except itself).

**(c) Maximum element:** Does NOT exist — multiple incomparable maximal elements (7,8,9,10,11,12 are pairwise incomparable, e.g., 7∤8 and 8∤7).

**Minimum element:** YES, 1 — since $1\mid n$ for every $n\in\{1,\ldots,12\}$, 1 is comparable to and below everything.

**(d) Longest chain:** $1,2,4,8$ (length 4: $1\mid2\mid4\mid8$) or $1,2,4,12$ (length 4: $1\mid2\mid4\mid12$) or $1,2,6,12$ (length 4). Longest chain has **4 elements**.

**(e) Antichain of size 5:** $\{7,8,9,10,11\}$ — check pairwise: none divides another (all distinct primes/prime-powers/products in a range where no divisibility holds). Verify pairwise: 7∤8, 7∤9, …, 8∤9, 8∤10, 8∤11, 9∤10, 9∤11, 10∤11 — all incomparable. ✓

**A larger antichain exists:** $\{7,8,9,10,11,12\}$, of size **6**. No element divides another —
in particular $8\nmid12$ and $12\nmid8$. Adding 6 would break it, since $6\mid12$; the run must
start above $n/2$ so that no element can be double another.

*(Grading note: accept antichain of size 5 as requested; award bonus recognition if student finds the size-6 antichain {7,8,9,10,11,12}.)*

---

## Part E

### E1. $R=\{(1,2),(2,3),(3,1)\}$ on $\{1,2,3\}$

$R\circ R$: pairs $(a,c)$ with $\exists b, (a,b)\in R\land(b,c)\in R$.

$(1,2)\in R,(2,3)\in R\Rightarrow(1,3)\in R\circ R$
$(2,3)\in R,(3,1)\in R\Rightarrow(2,1)\in R\circ R$
$(3,1)\in R,(1,2)\in R\Rightarrow(3,2)\in R\circ R$

$R\circ R=\{(1,3),(2,1),(3,2)\}$

$R\circ R\circ R = (R\circ R)\circ R$: pairs $(a,c)$ with $\exists b,(a,b)\in R\land(b,c)\in R\circ R$.

$(1,2)\in R,(2,1)\in R\circ R\Rightarrow(1,1)\in R\circ R\circ R$
$(2,3)\in R,(3,2)\in R\circ R\Rightarrow(2,2)\in R\circ R\circ R$
$(3,1)\in R,(1,3)\in R\circ R\Rightarrow(3,3)\in R\circ R\circ R$

$R\circ R\circ R=\{(1,1),(2,2),(3,3)\}=\text{id}$

**Is $R$ transitive?** Test: $R\circ R\subseteq R$? $R\circ R=\{(1,3),(2,1),(3,2)\}$. Is $(1,3)\in R$? NO (R only has (1,2),(2,3),(3,1)). So $R\circ R\not\subseteq R$. **$R$ is NOT transitive.**

(Makes sense — $R$ is a 3-cycle, clearly not transitive: $1\to2\to3$ but $1\not\to3$ directly.)

---

### E2. Topological sorts

Dependencies: utils≺parser, utils≺lexer, lexer≺compiler, parser≺compiler.

Minimal element: utils (nothing precedes it).

After removing utils: lexer and parser both become minimal (both only depended on utils).

**All valid topological sorts:**
1. utils, lexer, parser, compiler
2. utils, parser, lexer, compiler

(Only 2 valid orderings — since lexer and parser are incomparable to each other but both must precede compiler, and utils must be first.)

---

## Bonus Solutions

### Bonus 1: Graph isomorphism is an equivalence relation

**Reflexive:** The identity map on any graph's vertex set is a bijection preserving adjacency (trivially — same graph mapped to itself). So $G\cong G$.

**Symmetric:** If $G_1\cong G_2$ via bijection $f$, then $f^{-1}$ (which exists since $f$ is bijective, Week 5) is also adjacency-preserving (if $f$ preserves "adjacent ⟺ adjacent," so does its inverse, by the biconditional nature of the preservation property), giving $G_2\cong G_1$.

**Transitive:** If $G_1\cong G_2$ via $f$ and $G_2\cong G_3$ via $g$, then $g\circ f$ is a bijection (composition of bijections is bijective, Week 5) from $G_1$'s vertices to $G_3$'s vertices, and preserves adjacency (composing two adjacency-preserving maps preserves adjacency), giving $G_1\cong G_3$.

Equivalence relation. ∎

---

### Bonus 2: Strict partial orders

**Part 1: irreflexive + transitive ⟹ antisymmetric (vacuously).**

Suppose $(a,b)\in R$ and $(b,a)\in R$ for some $a,b$. By transitivity, $(a,a)\in R$. But $R$ is irreflexive, so $(a,a)\notin R$ — contradiction. So it's impossible to have both $(a,b)\in R$ and $(b,a)\in R$ for ANY $a,b$ (whether equal or not) — in particular, this can never happen for $a\neq b$, so the antisymmetry condition's hypothesis is never satisfied, making it vacuously true. ∎

**Part 2: $R\cup\{(a,a):a\in A\}$ is a genuine partial order.**

Let $R'=R\cup\{(a,a):a\in A\}$.

*Reflexive:* every $(a,a)\in R'$ by construction. ✓

*Antisymmetric:* Suppose $(a,b),(b,a)\in R'$ with $a\neq b$. Since $a\neq b$, neither pair can be one of the added diagonal pairs (which only have equal coordinates), so both $(a,b),(b,a)\in R$. But we just showed this is impossible for the original strict order $R$ (Part 1) unless $a=b$ — contradiction. So $R'$ is antisymmetric. ✓

*Transitive:* Let $(a,b),(b,c)\in R'$. Case both original (in $R$): then $(a,c)\in R\subseteq R'$ by transitivity of $R$. Case one or both are diagonal pairs (e.g., $a=b$): then the composition reduces trivially — e.g., if $(a,a)\in R'$ (diagonal) and $(a,c)\in R'$, the "transitive" requirement is just $(a,c)\in R'$, already true. All cases check out. ✓

$R'$ is reflexive, antisymmetric, transitive — a genuine partial order. ∎
