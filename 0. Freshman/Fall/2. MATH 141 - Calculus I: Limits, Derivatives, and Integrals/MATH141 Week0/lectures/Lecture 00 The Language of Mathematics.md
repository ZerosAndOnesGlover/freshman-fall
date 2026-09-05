# MATH 141 · Calculus I
## Week 0 · Lecture 0 of 4
### The Language of Mathematics: Sets, Notation & Logic

**Date:** Monday 17 August 2026 · 11:00–11:50 · Week 0

---

**Course:** MATH 141: Calculus I: Limits, Derivatives, and Integrals
**Semester:** Fall, Year 1
**Prerequisites:** None — this is the entry point
**Reading:** Stewart, Appendix A (Numbers, Inequalities, Absolute Values) | Spivak Ch. 1 (Basic Properties of Numbers)

---

## Why This Lecture Exists Before Everything Else

Every other lecture in this course will hand you sentences like this one:

$$\text{Domain} = \{x \in \mathbb{R} : x \neq 3\} = (-\infty, 3) \cup (3, \infty)$$

That sentence contains no calculus. It contains no algebra. It is entirely *notation*, and if you cannot read it aloud, fluently, without stopping, then every subsequent lecture will cost you twice what it should. You will be decoding symbols with half your attention and trying to learn limits with the other half.

This is the single most common reason capable students struggle in a first calculus course. Not the calculus. The **language the calculus is written in**, which is assumed rather than taught.

So we teach it. This lecture introduces no mathematical *content* — you will learn no new facts about numbers. It teaches you to read. Everything here gets used from Lecture 1 onward and never stops being used.

> **How to use this lecture.** Every piece of notation below is introduced with an **Aloud:** line that tells you exactly how to say it in English. Read those out loud. Actually out loud. Notation becomes fluent through the ear far faster than through the eye, and the sentences in this course are *meant* to be spoken — they were spoken at blackboards for two hundred years before they were typeset.

---

## 1. Sets: The Container Idea

A **set** is a collection of objects. That is the whole definition. The objects in a set are its **elements** (or **members**).

We write sets with curly braces:

$$A = \{1, 2, 3\}$$

> **Aloud:** "*A* is the set containing 1, 2, and 3."

Two symbols do almost all the work:

| Symbol | Meaning | Aloud |
|--------|---------|-------|
| $\in$ | is an element of | "is in" / "belongs to" |
| $\notin$ | is not an element of | "is not in" |

So with $A = \{1,2,3\}$ above:

$$2 \in A \qquad 7 \notin A$$

> **Aloud:** "2 is in *A*."  
> "7 is not in *A*."

The slash through a symbol always means **not**. This is universal: $\neq$ is "not equal", $\notin$ is "not in", $\nsubseteq$ is "not a subset of". Learn the base symbol and you get the negation free.

### 1.1 Order and Repetition Don't Matter

A set records only *membership*, nothing else:

$$\{1, 2, 3\} = \{3, 1, 2\} = \{1, 1, 2, 3, 3\}$$

All three are the same set. This will matter when we talk about solution sets: writing the solutions of an equation as $\{2, 3\}$ or $\{3, 2\}$ is identical.

### 1.2 The Empty Set

The set with no elements at all is the **empty set**, written $\emptyset$ or $\{\}$.

> **Aloud:** "the empty set."

It shows up constantly as an answer: "this equation has no real solutions" is written "the solution set is $\emptyset$."

> ⚠️ **Do not write $\{\emptyset\}$ when you mean $\emptyset$.** 
> $\emptyset$ is a box with nothing in it. $\{\emptyset\}$ is a box with an empty box inside it — it has one element.
> This distinction is invisible now and important in CS 250 (Discrete Mathematics).

### 1.3 Subsets

$A \subseteq B$ means every element of $A$ is also an element of $B$.

> **Aloud:** "*A* is a subset of *B*," or "*A* is contained in *B*."

$$\{1, 2\} \subseteq \{1, 2, 3\} \qquad \text{but} \qquad \{1, 4\} \nsubseteq \{1,2,3\}$$

> **Check 1.1** — True or false: $\emptyset \subseteq \{1,2,3\}$.
>
> *Answer:* **True.** "Every element of $\emptyset$ is in $\{1,2,3\}$" — there are no elements of $\emptyset$ to check, so nothing can fail. The empty set is a subset of every set.

---

## 2. The Number Systems

Five sets of numbers come up so often they have permanent reserved symbols, written in a distinctive "blackboard bold" typeface.

| Symbol | Name | Contains | Example members |
|--------|------|----------|-----------------|
| $\mathbb{N}$ | Naturals | Counting numbers | $1, 2, 3, \ldots$ |
| $\mathbb{Z}$ | Integers | Naturals, their negatives, and 0 | $\ldots, -2, -1, 0, 1, 2, \ldots$ |
| $\mathbb{Q}$ | Rationals | Ratios of integers $p/q$, $q \neq 0$ | $\tfrac{1}{2},\ -\tfrac{7}{3},\ 5,\ 0.25$ |
| $\mathbb{R}$ | Reals | Every point on the number line | $\tfrac12,\ \sqrt{2},\ \pi,\ -e$ |
| $\mathbb{C}$ | Complex | $a + bi$ where $i^2 = -1$ | $3 + 2i$ |

> **Aloud:** $\mathbb{R}$ is "the reals" or "R". $x \in \mathbb{R}$ is "*x* is a real number."

Each sits inside the next:

$$\mathbb{N} \subseteq \mathbb{Z} \subseteq \mathbb{Q} \subseteq \mathbb{R} \subseteq \mathbb{C}$$

**Why $\mathbb{Z}$ for integers?** From German *`Zahlen`*, "numbers." **Why $\mathbb{Q}$ for rationals?** From *`quotient`*. The notation is historical, not logical — don't look for a pattern.

### 2.1 Why the $\mathbb{Q}$ / $\mathbb{R}$ Distinction Matters

$\sqrt{2}$ is a real number but not a rational one — it cannot be written as a ratio of integers. Neither can $\pi$ or $e$. Numbers in $\mathbb{R}$ but not $\mathbb{Q}$ are called **irrational**.

This is not trivia. The rationals have *gaps*: there is a hole in $\mathbb{Q}$ exactly where $\sqrt{2}$ should be. The reals have no gaps — and that `gaplessness` (the technical term is **completeness**) is precisely what makes limits work. Every theorem in Weeks 1–12 quietly depends on it. When Week 5 tells you a continuous function on $[a,b]$ must attain a maximum, the reason is completeness.

**This entire course lives in $\mathbb{R}$.** Unless a problem says otherwise, "number" means "real number", and "no solution" means "no *real* solution" — $x^2 = -1$ has no solution in this course, even though it has two in $\mathbb{C}$.

---

## 3. Set-Builder Notation

Listing elements works for $\{1,2,3\}$. It fails for "all real numbers except 3" — you cannot list those. **Set-builder notation** describes a set by a *property* instead.

The template:

$$\{\ \underbrace{x \in \mathbb{R}}_{\text{what kind of thing}}\ \underbrace{:}_{\text{such that}}\ \underbrace{x \neq 3}_{\text{what's true about it}}\ \}$$

> **Aloud:** "the set of all *x* in $\mathbb{R}$ **such that** *x* is not equal to 3."

Three parts, always in this order:
1. **A variable and where it comes from** — $x \in \mathbb{R}$
2. **A separator** meaning "such that" — a colon $:$ or a vertical bar $\mid$ (both are standard; this course uses the colon)
3. **A condition** the variable must satisfy — $x \neq 3$

More examples, each read aloud:

| Set | Aloud | Plain English |
|-----|-------|---------------|
| $\{x \in \mathbb{R} : x > 0\}$ | "all real *x* such that *x* is greater than 0" | the positive reals |
| $\{n \in \mathbb{Z} : n = 2k \text{ for some } k \in \mathbb{Z}\}$ | "all integers *n* such that *n* equals 2*k* for some integer *k*" | the even integers |
| $\{f(x) : x \in A\}$ | "the set of all $f(x)$ such that *x* is in *A*" | the outputs of $f$ — this is the **range** |

That last row is worth pausing on: it is the definition of *range* from Lecture 1, and it is now readable. The thing before the colon does not have to be a bare variable — it can be any expression built from it.

> **Check 3.1** — Read aloud, then describe in plain English: $\{x \in \mathbb{R} : x^2 = 4\}$.
>
> *Answer:* "The set of all real *x* such that *x* squared equals 4." In plain English: $\{-2, 2\}$.

---

## 4. Interval Notation

Set-builder is fully general but wordy. For the most common case, an unbroken stretch of the number line, we use **interval notation**, which is faster to write and read.

The single rule that governs all of it:

> **Square bracket $[$ or $]$ includes the endpoint. Round parenthesis $($ or $)$ excludes it.**

That is the entire system. Everything below is that rule applied.

| Interval | Set-builder               | Aloud                        | Endpoints     |
| -------- | ------------------------- | ---------------------------- | ------------- |
| $[2, 5]$ | $\{x : 2 \leq x \leq 5\}$ | "closed interval 2 to 5"     | both included |
| $(2, 5)$ | $\{x : 2 < x < 5\}$       | "open interval 2 to 5"       | both excluded |
| $[2, 5)$ | $\{x : 2 \leq x < 5\}$    | "2 inclusive to 5 exclusive" | left only     |
| $(2, 5]$ | $\{x : 2 < x \leq 5\}$    | "2 exclusive to 5 inclusive" | right only    |

**The two ends are chosen independently.** $[2,5)$ is not a typo — the bracket and the parenthesis are each reporting on their own endpoint. This is the single most common misreading of the notation, and it is why $[2,5)$ looks wrong the first fifty times you see it.

Notice the correspondence is mechanical:

$$\big[ \ \longleftrightarrow \ \leq \qquad\qquad \big( \ \longleftrightarrow \ <$$

An inclusive bracket goes with an inequality that has a line under it. Both symbols are "and equals."

### 4.1 Unbounded Intervals

To say "everything above 2" we need an endpoint that isn't a number. We write $\infty$:

| Interval | Set-builder | Aloud |
|----------|-------------|-------|
| $(2, \infty)$ | $\{x : x > 2\}$ | "2 to infinity, open at 2" |
| $[2, \infty)$ | $\{x : x \geq 2\}$ | "2 to infinity, closed at 2" |
| $(-\infty, 5]$ | $\{x : x \leq 5\}$ | "negative infinity to 5, closed at 5" |
| $(-\infty, \infty)$ | $\mathbb{R}$ | "negative infinity to infinity" |

> ⚠️ **$\infty$ always gets a parenthesis, never a bracket.** $[2, \infty]$ is wrong. The reason is not a convention to memorize — it follows from the rule you already know. A bracket means "include this endpoint," and $\infty$ is **not a number**; it is shorthand for "this side never stops." There is nothing there to include. Writing $[2,\infty]$ claims infinity is a value $x$ could equal, and it isn't.

This is your first example of something this course does relentlessly: a rule that looks arbitrary turns out to be a consequence of a rule you already have. Whenever you're tempted to memorize, look for the derivation first.

> **Check 4.1** — Write $\{x \in \mathbb{R} : -3 \leq x < 7\}$ in interval notation.
>
> *Answer:* $[-3, 7)$. Bracket on the left ($\leq$, included), parenthesis on the right ($<$, excluded).

---

## 5. Combining Sets: Union, Intersection, Difference

Some sets are not a single unbroken stretch. "All reals except 3" is the number line with a hole punched in it — two pieces. We need operators to build sets from other sets.

| Symbol | Name | Definition | Aloud |
|--------|------|------------|-------|
| $\cup$ | union | everything in **either** set | "union" |
| $\cap$ | intersection | everything in **both** sets | "intersect" |
| $\setminus$ | difference | in the first, **not** in the second | "minus" / "without" |

With $A = \{1,2,3\}$ and $B = \{3,4\}$:

$$A \cup B = \{1,2,3,4\} \qquad A \cap B = \{3\} \qquad A \setminus B = \{1,2\}$$

**A memory hook that actually works:** $\cup$ is a cup — it holds everything you pour in. $\cap$ is a cap — it's the narrow overlap on top.

### 5.1 The Bridge You Will Use Constantly

This is the most important idea in the lecture:

> **"or" means union $\cup$. "and" means intersection $\cap$.**

Every domain problem, every inequality, every solution set in this course is built by translating English into one of those two operators.

Now the sentence from the opening of this lecture is fully readable:

$$\{x \in \mathbb{R} : x \neq 3\} = (-\infty, 3) \cup (3, \infty)$$

> **Aloud:** "The set of all real *x* such that *x* is not equal to 3 equals the open interval from negative infinity to 3, **union** the open interval from 3 to infinity."

And you can now see *why* the two sides are equal rather than just accepting it. "$x \neq 3$" means "$x < 3$ **or** $x > 3$" — there is no third option. "Or" means union. So the set splits into everything left of 3, union everything right of 3, with 3 itself in neither piece. Both intervals get parentheses at 3, because 3 is exactly what we're excluding.

### 5.2 Why Intersection Shows Up in Domain Problems

When a function has *two* restrictions, you need $x$ to satisfy the first **and** the second. "And" means intersection.

**Example.** Find the domain of $\displaystyle f(x) = \frac{\sqrt{x+1}}{x - 3}$.

The square root demands $x + 1 \geq 0$, i.e. $x \geq -1$, i.e. $[-1, \infty)$.
The denominator demands $x \neq 3$, i.e. $(-\infty,3) \cup (3,\infty)$.

We need **both**, so we intersect:

$$[-1, \infty) \cap \Big[(-\infty,3) \cup (3,\infty)\Big] = [-1, 3) \cup (3, \infty)$$

> **Aloud:** "from $-1$ inclusive up to 3 exclusive, union 3 exclusive to infinity."

In words: start at $-1$ and go right forever, then punch out the single point 3. Lecture 1 will do harder versions of this; the only new thing there will be the algebra, not the notation.

> **Check 5.1** — Express $(-\infty, 4] \cap [0, 9)$ as a single interval.
>
> *Answer:* $[0, 4]$. You need $x \leq 4$ **and** $0 \leq x < 9$; the binding constraints are $0$ on the left (included) and $4$ on the right (included).

---

## 6. Logic: Implication and Equivalence

Mathematics is written in conditional sentences. Three arrows carry them.

### 6.1 Implication $\Rightarrow$

$$P \Rightarrow Q$$

> **Aloud:** "*P* implies *Q*," or "if *P*, then *Q*."

It claims: whenever $P$ is true, $Q$ is also true. Nothing more.

From `Lecture 01`:

$$5 - x \geq 0 \Rightarrow x \leq 5$$

> **Aloud:** "5 minus *x* being greater than or equal to zero implies *x* is less than or equal to 5."

In practice, when you see $\Rightarrow$ in a chain of algebra, read it as "**and therefore**". It marks one legal step to the next:

$$2x + 6 = 10 \Rightarrow 2x = 4 \Rightarrow x = 2$$

> **Aloud:** "$2x + 6 = 10$, and therefore $2x = 4$, and therefore $x = 2$."

You will also see $\implies$ (a longer arrow) and $\to$ used for the same purpose. Same meaning.

### 6.2 The Converse Is a Different Claim

$P \Rightarrow Q$ and $Q \Rightarrow P$ are **not** the same statement. The second is called the **converse**, and it can be false when the first is true.

- **True:** $x = 2 \Rightarrow x^2 = 4$
- **False:** $x^2 = 4 \Rightarrow x = 2$  — because $x$ could be $-2$

That $-2$ is a **counterexample**: a single case where the hypothesis holds and the conclusion fails. One `counterexample` destroys a general claim permanently. You do not need two.

This is not a logic-class technicality. It is the entire reason `Lecture 02` §2.4 tells you to check for extraneous solutions after squaring both sides. Squaring is a $\Rightarrow$ step that isn't reversible, so it can manufacture solutions that don't satisfy the original equation. The notation is warning you, if you can read it.

### 6.3 Equivalence $\iff$

When the implication runs both ways, we write:

$$P \iff Q$$

> **Aloud:** "*P* if and only if *Q*," or "*P* is equivalent to *Q*."

It packs two claims into one symbol: $P \Rightarrow Q$ **and** $Q \Rightarrow P$. The two statements are interchangeable — anywhere one is true, so is the other.

From `Lecture 01`:

$$y = \log_a x \iff a^y = x$$

> **Aloud:** "*y* equals log base *a* of *x* if and only if *a* to the *y* equals *x*."

These are two ways of writing the same fact, which is exactly what makes logarithms and exponentials inverse to each other. You can trade either form for the other, in either direction, at any time.

> ⚠️ **In your own written work, do not use $\Rightarrow$ where you mean $\iff$.** Solving an inequality is a chain of $\iff$ steps — every move must be reversible or you may lose or gain solutions. Getting this wrong is how students lose points on inequality problems without ever knowing why.

> **Check 6.1** — Is this true, and is its converse true? $x > 3 \Rightarrow x > 1$.
>
> *Answer:* The statement is **true** — anything past 3 is past 1. The converse ($x > 1 \Rightarrow x > 3$) is **false**; $x = 2$ is a counterexample.

---

## 7. Quantifiers: "For All" and "There Exists"

Two more symbols, and then you can read anything in this course.

| Symbol | Name | Aloud |
|--------|------|-------|
| $\forall$ | universal quantifier | "for all" / "for every" |
| $\exists$ | existential quantifier | "there exists" / "there is some" |

$$\forall x \in \mathbb{R},\ x^2 \geq 0$$

> **Aloud:** "For every real number *x*, *x* squared is greater than or equal to zero." (True.)

$$\exists x \in \mathbb{R} : x^2 = 4$$

> **Aloud:** "There exists a real number *x* such that *x* squared equals 4." (True — $x = 2$ works, and one witness is enough.)

Note the asymmetry, which is the whole point of having two symbols: to prove a $\forall$ claim you must handle **every** case; to destroy it you need **one** counterexample. To prove an $\exists$ claim you need **one** example; to destroy it you must rule out **every** case.

### 7.1 Order Matters — and This Is Where Week 1 Lives

Swapping $\forall$ and $\exists$ changes the meaning completely. In plain English:

- "**Every** person has **a** mother." — True. Each person gets their own mother.
- "**There is a** mother of **every** person." — False. Claims one woman mothered everyone.

Same words. Different order. Different claims. The second is far stronger.

### 7.2 The Payoff

Here is the definition that opens Week 1 — the hardest idea in the course:

> $\displaystyle\lim_{x \to a} f(x) = L$ means: for every $\varepsilon > 0$, there exists $\delta > 0$ such that
> $$0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon$$

Read it piece by piece with what you now know:

| Fragment | What it says |
|----------|--------------|
| for every $\varepsilon > 0$ | *no matter what* positive tolerance is demanded of the output |
| there exists $\delta > 0$ | *we can supply* a positive tolerance for the input |
| such that | with the following property |
| $0 < \|x - a\| < \delta$ | if $x$ is within $\delta$ of $a$, but not equal to $a$ |
| $\implies$ | then it follows that |
| $\|f(x) - L\| < \varepsilon$ | $f(x)$ is within $\varepsilon$ of $L$ |

And the order is doing real work: $\delta$ comes *after* $\varepsilon$, so $\delta$ is allowed to depend on $\varepsilon$ — a tighter demand gets a tighter answer. Reverse the quantifiers and you'd be claiming one $\delta$ works for all $\varepsilon$ at once, which is a different and much stronger statement that most functions fail.

**You are not expected to understand why this is the right definition of a limit.** That is Week 1, Lecture 2, and it takes most students several days. You *are* expected, starting now, to be able to **read it** — to say it aloud and know what each symbol is doing. Decoding and understanding are separate skills, and you should not be spending Week 1 on the first one.

---

## 8. Symbol Glossary

Everything above, plus the remaining symbols you'll meet in Weeks 0–12. Keep this page.

| Symbol                                                   | Aloud                                             | Meaning                            |
| -------------------------------------------------------- | ------------------------------------------------- | ---------------------------------- |
| $\in$ / $\notin$                                         | "is in" / "is not in"                             | set membership                     |
| $\subseteq$                                              | "is a subset of"                                  | containment                        |
| $\emptyset$                                              | "the empty set"                                   | set with no elements               |
| $\cup$ / $\cap$                                          | "union" / "intersect"                             | or / and                           |
| $\setminus$                                              | "minus"                                           | set difference                     |
| $\mathbb{N},\mathbb{Z},\mathbb{Q},\mathbb{R},\mathbb{C}$ | "naturals, integers, rationals, reals, complexes" | number systems                     |
| $:$ or $\mid$                                            | "such that"                                       | separator in set-builder           |
| $\Rightarrow$, $\implies$                                | "implies" / "and therefore"                       | implication                        |
| $\iff$                                                   | "if and only if"                                  | equivalence                        |
| $\forall$ / $\exists$                                    | "for all" / "there exists"                        | quantifiers                        |
| $\approx$                                                | "is approximately"                                | approximate equality               |
| $\pm$ / $\mp$                                            | "plus or minus"                                   | both signs, paired                 |
| $\mid$                                                   | "divides"                                         | $p \mid a$: $p$ divides $a$ evenly |
| $\lceil x \rceil$                                        | "ceiling of *x*"                                  | round up to nearest integer        |
| $\lfloor x \rfloor$                                      | "floor of *x*"                                    | round down to nearest integer      |
| $\sum$ / $\prod$                                         | "sum" / "product"                                 | repeated addition / multiplication |
| $\Delta$                                                 | "delta" / "change in"                             | $\Delta y = y_2 - y_1$             |
| $\to$                                                    | "approaches" / "tends to"                         | $x \to 3$, $n \to \infty$          |
| $\therefore$                                             | "therefore"                                       | conclusion marker                  |
| $\blacksquare$                                           | "QED"                                             | end of proof                       |

> **Note on the overloaded bar.** $\mid$ means three different things depending on context: "such that" in set-builder, "divides" in number theory, and absolute value when it comes in a pair, $|x|$. Context always `disambiguates`, but the collision is worth knowing about the first time you meet $p \mid a_0$ in the Rational Root Theorem (`Lecture 02` §2.3) and read it as "such that."

---

## 9. Common Misreadings to Eliminate

Parallel to the algebra errors in `Lecture 02` §6 — these are notation errors, and they're just as costly.

**Misreading 1:** Reading $[2,5)$ as a typo.
**Correct:** The ends are chosen independently. $2 \leq x < 5$.

**Misreading 2:** Writing $[2, \infty]$.
**Correct:** $[2, \infty)$. Infinity is not a number and can never be included.

**Misreading 3:** Treating $P \Rightarrow Q$ as reversible.
**Correct:** The converse is a separate claim requiring separate justification. This is the source of every extraneous solution you will ever produce.

**Misreading 4:** Reading $\cup$ as "and" because both pieces are listed.
**Correct:** $\cup$ is **or**. $(-\infty,3) \cup (3,\infty)$ is "less than 3 **or** greater than 3." No number is in both.

**Misreading 5:** Confusing $\{2,3\}$ with $(2,3)$.
**Correct:** $\{2,3\}$ is a set of exactly two numbers. $(2,3)$ is an interval containing infinitely many. (And in `Lecture 02` §4, $(2,3)$ means a *point* in the plane — three meanings for one notation, all resolved by context.)

**Misreading 6:** Writing $\Rightarrow$ between steps of an inequality.
**Correct:** Use $\iff$ unless you genuinely mean one-directional. Inequality solving requires reversibility.

---

## 10. Summary

| Concept | Core idea |
|---------|-----------|
| Set | A collection; membership is all that's recorded |
| $\mathbb{R}$ | Where this entire course lives |
| Set-builder | Describe by property: {variable ∈ where : condition} |
| Interval | Bracket includes, parenthesis excludes — independently per end |
| $\cup$ / $\cap$ | "or" / "and" — the translation you'll use most |
| $\Rightarrow$ | One-directional; the converse needs separate proof |
| $\iff$ | Both directions; the two sides are interchangeable |
| $\forall$ / $\exists$ | Order matters; later variables may depend on earlier ones |

**The deeper point:** notation is not decoration and it is not gatekeeping. Each symbol above compresses a sentence that mathematicians got tired of writing. $(-\infty,3) \cup (3,\infty)$ replaces "every real number that is either strictly less than three or strictly greater than three." Once the compression is fluent, you can hold a whole argument in your head at once — which is the only way the arguments in Week 8 will fit.

Fluency is the goal, and fluency comes from reading aloud. Do that.

---

## Lecture 0 Exercises

1. Write in interval notation: (a) $\{x \in \mathbb{R} : -1 < x \leq 6\}$  (b) $\{x \in \mathbb{R}: x \geq 0\}$  (c) $\{x \in \mathbb{R} : x \neq 0\}$
		*Solution:*          a. (-1, 6]         b. $[0, \infty)$           c. $(-\infty, 0) \cup (0, \infty)$

2. Write in set-builder notation: (a) $[4, 9)$  (b) $(-\infty, -2) \cup (2, \infty)$

3. Simplify to a single interval or union of intervals:
   (a) $[0,5] \cap [3,8]$   (b) $(-\infty,1) \cup (0,\infty)$   (c) $[1,4] \setminus \{2\}$

4. Read each aloud, then say whether it is true:
   (a) $\forall x \in \mathbb{R},\ x^2 > 0$   (b) $\exists x \in \mathbb{Z} : x^2 = 9$   (c) $\sqrt{2} \in \mathbb{Q}$

5. For each, state whether the implication is true, and whether its converse is true:
   (a) $x = 0 \Rightarrow x^2 = 0$   (b) $x > 0 \Rightarrow |x| = x$

6. Translate into symbols: "For every positive real number $\varepsilon$, there is a natural number $n$ such that $1/n$ is less than $\varepsilon$."

7. **(Thinking question)** The domain of $g(x) = \sqrt{x-2}$ is $[2,\infty)$ and the domain of $h(x) = 1/(x-5)$ is $\{x \in \mathbb{R} : x \neq 5\}$. Without doing any algebra beyond set operations, write the domain of $g(x) + h(x)$, and explain in one sentence why the operation you used is intersection rather than union.

### Answers

**1.** (a) $(-1, 6]$ — parenthesis left (strict), bracket right (inclusive).
(b) $[0, \infty)$ — bracket at 0, and $\infty$ always takes a parenthesis.
(c) $(-\infty, 0) \cup (0, \infty)$ — "not equal" splits the line into two pieces.

**2.** (a) $\{x \in \mathbb{R} : 4 \leq x < 9\}$
(b) $\{x \in \mathbb{R} : |x| > 2\}$, or equivalently $\{x \in \mathbb{R} : x < -2 \text{ or } x > 2\}$. Both are correct; the absolute-value form is the one `Lecture 02` §3.4 will prefer.

**3.** (a) $[3,5]$ — the overlap; take the larger left endpoint and the smaller right one.
(b) $(-\infty, \infty) = \mathbb{R}$. Every real is in at least one of the two pieces, since they overlap on $(0,1)$. If you answered $(0,1)$, you read $\cup$ as "and" — that's Misreading 4.
(c) $[1,2) \cup (2,4]$ — removing an interior point splits the interval in two, and 2 is excluded from both halves.

**4.** (a) "For every real *x*, *x* squared is greater than zero." **False** — $x = 0$ gives $0$, which is not $> 0$. (It would be true with $\geq$.)
(b) "There exists an integer *x* such that *x* squared equals 9." **True** — $x = 3$ (also $-3$; one witness suffices).
(c) "Root 2 is in $\mathbb{Q}$." **False** — $\sqrt{2}$ is irrational.

**5.** (a) True. Converse ($x^2 = 0 \Rightarrow x = 0$) is **also true** — zero is the only number whose square is zero. So this one is genuinely $\iff$.
(b) True. Converse ($|x| = x \Rightarrow x > 0$) is **false**: $x = 0$ satisfies $|0| = 0$ but not $0 > 0$. A single boundary counterexample is enough.

**6.** $$\forall \varepsilon > 0,\ \exists n \in \mathbb{N} : \frac{1}{n} < \varepsilon$$
This is the **Archimedean property** of the reals. It is true, it is the reason $1/n \to 0$, and the $\forall$-then-$\exists$ order is essential: $n$ is allowed to depend on $\varepsilon$ (smaller $\varepsilon$ needs bigger $n$).

**7.** $$\text{dom}(g+h) = [2,\infty) \cap \big[(-\infty,5)\cup(5,\infty)\big] = [2,5) \cup (5,\infty)$$
Intersection, because $g(x) + h(x)$ requires *both* $g(x)$ and $h(x)$ to be defined — "and" means $\cap$. Union would be the set where at least one of them works, which is not enough to add them.

---

*Next lecture: [[Lecture 01 Functions]]*
*Reading: Stewart Appendix A; Spivak Ch. 1*
