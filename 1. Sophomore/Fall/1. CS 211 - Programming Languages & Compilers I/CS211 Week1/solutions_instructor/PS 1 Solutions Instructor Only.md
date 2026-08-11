# CS 211 · Problem Set 1 · Solutions
## Instructor Only

---

> **Automaton sizes below were computed** by a Thompson-construction, subset-construction and
> partition-refinement implementation in Python, and cross-checked against `flex -v` where
> applicable. Where a student's automaton differs in state count but is correct after minimisation,
> **mark it correct** — Thompson's construction has variants and Q2(a) counts will legitimately vary.

---

## Q1: Regular Expressions, Formally (16)

### (a) [4] Even length

$$((a \mid b)(a \mid b))^*$$

**Pairs, repeated.** Accept any equivalent form. **−2** for an answer that only handles even numbers of `a`s — that is (b), and confusing the two is the point of setting them together.

### (b) [4] An even number of `a`s

$$b^*\,(a\,b^*\,a\,b^*)^*$$

**Reasoning:** `b`s are unconstrained, so allow them freely; `a`s must come in pairs.

**Check against `aab`:** two `a`s then a `b`. Matches — $b^*$ empty, then one iteration $a\,b^*(\text{empty})\,a\,b^*(=b)$. ✅
**Check against `aba`:** two `a`s separated by a `b`. Matches. ✅
**Check against `ab`:** one `a`. Must not match. ✅

**Common wrong answer:** $(aa \mid b)^*$ — this fails on `aba`, which has two `a`s but not adjacent. **Ask for the `aba` check**; a student who tested only `aab` will not have caught it.

### (c) [4] Why `\\.` is needed

Without it, the alternatives are `[^"\\\n]` only — **any character except a quote, a backslash or a newline.** A literal containing an escape cannot match at all, because the backslash is excluded and nothing else admits it.

**Concrete failure:** `"hi\n"`. The `\` matches nothing, so the `( ... )*` stops after `hi`, and the pattern then demands a closing `"` but finds `\`. **The literal does not lex.**

Worse, if the backslash were simply *allowed* in the first alternative instead, `"a\"b"` would terminate at the escaped quote — the escape is what makes `\"` a quote-that-does-not-close.

**Mark scheme:** 2 for identifying that escapes cannot be matched, 2 for a concrete literal. `"hi\n"` or `"a\"b"` both earn it.

### (d) [4] `([ab]+)\1` is not regular

The language is $\{ww \mid w \in \{a,b\}^+\}$.

> Suppose a DFA with $k$ states accepts it. Consider the $k+1$ strings
> $ab,\; a^2b,\; \dots,\; a^{k+1}b$. There are $k+1$ of them and only $k$ states, so **by pigeonhole
> two land in the same state** — say $a^ib$ and $a^jb$ with $i \ne j$.
>
> From that shared state the machine behaves identically on any suffix, so it accepts
> $a^i b\,a^i b$ if and only if it accepts $a^j b\,a^i b$. **The first is in the language and the
> second is not.** Contradiction.

**Mark scheme:** 1 for choosing a suitable family of strings, 1 for the pigeonhole step, 1 for the shared-suffix argument, 1 for the contradiction.

**The note in the question is doing real work**, and the strongest answers engage with it: over a one-letter alphabet `(a+)\1` denotes $(aa)^+$, which is regular. **"Backreferences make a pattern non-regular" is false as stated** — they make it *possible* to write non-regular patterns, which is a different claim. A student who says so unprompted deserves a comment.

**Watch for:** a proof using strings $a, aa, aaa, \dots$ over the single-letter sub-alphabet. That family cannot produce the contradiction, for exactly the reason the note gives. **Worth 2 of 4** with a pointer to why.

---

## Q2: Thompson and the Subset Construction (24)

$r = (a \mid b)^* b a$

### (a) [8] The NFA

**Reference construction gives 12 states.** *(Measured.)*

Variants of Thompson's construction differ by a state or two — some omit the extra start/accept pair for `*` when the inner fragment already has them. **Accept 10–14 states** provided the diagram is correct and $\varepsilon$-transitions are marked.

**What must be right:** one start, one accept, $\varepsilon$-transitions for the star's loop and exit, and the concatenation joining `(a|b)*` → `b` → `a`.

**Mark scheme:** 6 for a correct diagram, 2 for the count. **−3** if the star fragment has no exit $\varepsilon$ (a very common slip that makes the empty string unmatchable).

### (b) [10] The subset construction

**Four DFA states.** *(Measured.)* Naming them 0–3:

| DFA state | on `a` | on `b` | Accepting? |
|---|---|---|---|
| **0** (start) | 1 | 2 | |
| **1** | 1 | 2 | |
| **2** | **3** | 2 | |
| **3** | 1 | 2 | ✅ |

**Mark scheme:** 8 for a correct table, 2 for showing the subsets rather than only the final names. Students who show only 0–3 with no NFA subsets have not demonstrated the construction — **−2**.

### (c) [6] The states in English

| | Meaning |
|---|---|
| **0** | nothing read yet |
| **1** | the last character was an `a`, and it did not complete a `ba` |
| **2** | **the last character was a `b`** — a `ba` is one `a` away |
| **3** | **the last two characters were `ba`** — accepting |

**This is the check.** A student whose (b) is wrong will usually find one state here they cannot describe, which is the intended diagnostic.

**Mark scheme:** 6, or 4 if one description is muddled but the rest are right.

---

## Q3: Minimisation and Equivalence (20)

### (a) [8] Minimising

**Initial partition:** $\{3\}$ (accepting) and $\{0,1,2\}$.

**Round 1:** in $\{0,1,2\}$, state 2 goes to 3 on `a` while 0 and 1 go to 1. **Split:** $\{3\}$, $\{2\}$, $\{0,1\}$.

**Round 2:** 0 and 1 agree on both symbols — `a` → 1, `b` → 2. **No further split.**

**Minimal DFA: 3 states.** *(Measured.)* States 0 and 1 merge, because "nothing read yet" and "last character was an `a`" have identical futures.

**Note there is no dead state** — every string over $\{a,b\}$ is a prefix of something acceptable, so no dead state is reachable. **A student who reports 4 including a dead state should be asked whether it is reachable**; if they add one to make the DFA total, that is a defensible convention and earns full marks provided they say so.

**Mark scheme:** 5 for the partition rounds, 3 for the count with the merge explained.

### (b) [6] $(a\mid b)^*$ versus $(a^*b^*)^*$

**They denote the same language: all strings over $\{a,b\}$.** Both minimise to **one state**, accepting, with self-loops on both symbols. *(Measured: NFA 8 → DFA 3 → minimal 1, and NFA 10 → DFA 3 → minimal 1.)*

**The argument without automata:** every string over $\{a,b\}$ can be written as a sequence of blocks each of the form $a^ib^j$ — take each character as its own block. So $(a^*b^*)^*$ generates everything, and it obviously generates nothing else.

**Mark scheme:** 4 for the correct answer with justification, 2 for actually constructing both minimal DFAs. **An answer of "no, they differ" is worth 0** and is worth a comment — it usually comes from assuming $(a^*b^*)$ means "all `a`s before all `b`s", which is true of one iteration but not of the starred form.

### (c) [6] Checking with code

**Both routes earn full marks.**

**Route 1 — reason it out.** As above: the block argument needs no code, and a student who says so and gives the argument has answered better than one who wrote a program.

**Route 2 — write the check.** Construct both minimal DFAs and test isomorphism, or (simpler and equally valid) enumerate all strings up to length ~10 over $\{a,b\}$ and confirm both regexes accept all of them.

**Mark scheme:** 6 for either, provided the choice is stated. **−2** for a student who claims `cfg_count.py` can do it — it counts parse trees for a CFG and has no notion of automata, which the question already says.

---

## Q4: Why the Parser Needs a Stack (14)

### (a) [8] The proof

> Suppose a DFA with $k$ states recognises balanced parentheses. Feed it the $k+1$ strings
> $(^1, (^2, \dots, (^{k+1}$. There are $k+1$ inputs and only $k$ states, so **by pigeonhole two
> land in the same state** — say $(^i$ and $(^j$ with $i \ne j$.
>
> From that shared state the machine's behaviour is identical on any suffix. In particular it
> accepts $(^i)^i$ if and only if it accepts $(^j)^i$.
>
> But $(^i)^i$ **is** balanced and $(^j)^i$ **is not** (since $i \ne j$). **Contradiction.**

**Mark scheme:** 2 for feeding $k+1$ inputs, 2 for the pigeonhole step, 2 for the shared-suffix argument, 2 for the contradiction. **A proof that asserts "a DFA can't count" without the pigeonhole earns 2 of 8.**

### (b) [6] Bounded nesting

**Yes, it is regular**, and this catches a lot of people.

**A DFA needs 102 states**: one for each depth $0$ through $100$, plus a dead state for "depth exceeded or unbalanced". The counter is *bounded*, so it fits in finite state — the machine does not need to count arbitrarily, only up to 100.

**Where the proof in (a) fails:** it fed $k+1$ strings of unboundedly increasing depth. With depth capped at 100 you can only feed 101 distinct depths, so for $k \ge 102$ the pigeonhole never fires. **The proof needs unbounded nesting, and that is exactly what the bound removes.**

**Mark scheme:** 3 for "yes", 3 for the state count *and* for locating where the proof breaks. **An answer of "no" earns 0** — but it is the most common answer, and it is worth stating in review that this is the same question as L03 Exercise 5 and L04 Exercise 5, asked three times deliberately.

> **The general point:** *finite* is a weaker condition than students expect. Any bounded counter is
> finite state. Real parsers still use a stack because real languages do not bound nesting depth —
> and because 102 states for one construct does not scale to a grammar.

---

## Q5: The Lexer (26)

### Reference implementation

`lab/lexer.py` is the model answer. **Do not release it before the deadline** — it is shipped as a Lab 1 starter, so students have had it since Friday of Week 1. **This is intentional**: the marks here are for a correct implementation with positions and errors, not for originality, and a student who reads the reference and writes their own from understanding has done the exercise.

**What that means for marking: look for divergence from the reference, not similarity to it.** A verbatim copy with the comments stripped is a plagiarism question, not a marking one.

### Mark breakdown

| | | Check |
|---|---:|---|
| Correct 109 tokens on `sample.cy` | 8 | `python3 lexer.py ../lab/sample.cy \| diff - ../lab/expected_tokens.txt` |
| Maximal munch on all six L03 §4 inputs | 5 | `a<=b`, `a< =b`, `a<<=b`, `x-->y`, `ifx`, `if x` |
| Comments and strings, incl. `a/* /* */ */b` | 5 | Must give `IDENT(a) OP(*) OP(/) IDENT(b)` |
| Positions correct | 4 | Plant an error on line 12; the message must say 12 |
| Errors raised, not swallowed | 4 | `a&b` must raise, not skip the `&` |

**The four failure modes that account for most lost marks:**

1. **Using `re`.** The question forbids it. **Zero for the implementation marks**, and it is usually obvious from a single `import re`.
2. **Thirteen keyword branches instead of a set lookup.** Costs 2 of the 8 — it works, but it is the thing Requirement 1 specifically rules out.
3. **`col` never incremented, or reset wrongly on newline.** Costs the 4 position marks. Check with a two-line file.
4. **Operators checked shortest-first.** `<=` becomes `<` `=`. Costs the 5 munch marks and is caught immediately by the diff.

### The written part

**One input where the student's lexer disagrees with `flex`, and a defence of the choice.**

Expected answers are the three from Lab 1 Part 3 — `12abc`, `"unterminated`, `a&b`. **Any of them earns the marks** provided the student says which behaviour they chose and why.

**"There is none" requires evidence.** A student claiming full agreement has either implemented flex's recovery behaviour deliberately — which is a fine choice, and they should say so — or has not tested invalid input. **Ask which.**

---

## Mark Distribution

| Question | Points | Common failure |
|---|---:|---|
| Q1 | 16 | `(aa|b)*` for even-many-`a`s; failing the `aba` check |
| Q2 | 24 | Star fragment with no exit ε-transition |
| Q3 | 20 | Claiming $(a^*b^*)^*$ orders the letters |
| Q4 | 14 | **Answering "no" to (b)** — the most-missed question on this set |
| Q5 | 26 | `col` tracking, and shortest-first operator matching |
| **Total** | **100** | |

**Q4(b) is the one to review in class.** It is asked three times across the week's materials — L03 Ex. 5, L04 Ex. 5, and here — and it is still the most-missed, because "finite automata cannot count" is a slogan students carry without the qualifier. **The qualifier is the content.**

---

*CS 211 · PS 1 Solutions · Instructor Only*
