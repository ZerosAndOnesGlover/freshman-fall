# CS 211 · Week 0 · Reading Guide
## The Dragon Book's First Two Chapters, and Why SICP Is on This List

---

**Set reading:** Aho et al., *Compilers: Principles, Techniques, and Tools*, 2nd ed. — **§1.1–1.2**, **§2.2**, **§4.2–4.3**.
**Also set:** Abelson & Sussman, *SICP* — **§1.1**. Free at [mitpress.mit.edu](https://mitpress.mit.edu/sites/default/files/sicp/index.html).
**Optional:** Appel, *Modern Compiler Implementation*, **Ch. 1–2**.

**Read Dragon §1.1–1.2 and §2.2 before Lecture 2.** The rest can follow the lecture; §4.2–4.3 is the formal treatment of what L02 does by example, and it lands better second.

---

## How to Read the Dragon Book

**Do not read it front to back.** It is a reference that happens to be bound like a textbook, and reading it linearly is the single most common way students lose a term to CS 211.

**Read it against a question.** The guides in this course will always tell you which sections and what to look for. When a lecture leaves you unsure, that is the moment to open the corresponding section — and you will find it answers precisely, in a page, what the lecture had forty minutes for.

> **The Dragon Book is dense in a specific way:** it states things once, exactly, with no redundancy.
> Appel says the same things twice from two angles. **If a Dragon section does not land, read
> Appel's version of it before rereading the Dragon** — you will usually find the Dragon section was
> clear all along and you were missing one definition.

---

## Section by Section

### Dragon §1.1–1.2 — Language Processors and Compiler Structure

| § | What to take from it |
|---|---|
| **1.1** | Compiler versus interpreter, and the hybrid — read this against L01 §6. The book's diagram of the language processing system (preprocessor, compiler, assembler, linker) is the same one CS:APP gave you in CS 201 Week 0, from the other side |
| **1.2** | **The phase list.** This is L01 §5 stated by the authors. Note that they split "analysis" (front end) from "synthesis" (back end) and note where they put the symbol table — *beside* the phases, not inside one |

**Their diagram has a symbol table running the full height of the page.** That is not a drawing convenience. It is the one structure that every phase from lexing to code generation reads and writes, and it is why Week 3 is positioned where it is.

### Dragon §2.2 — Syntax Definition

**This is the core Week 0 reading.** It covers everything in L02 §1–§5 and is worth reading slowly.

| § | What to take from it |
|---|---|
| **2.2.1** | The formal definition of a CFG — the four-tuple from L02 §1 |
| **2.2.2** | Derivations. Note their notation: $\Rightarrow$ for one step, $\stackrel{*}{\Rightarrow}$ for zero or more |
| **2.2.3** | Parse trees, and the statement that a parse tree and a derivation are different views of the same thing |
| **2.2.4** | **Ambiguity.** Their example is `id + id * id`, which is L02 §4's `n + n * n` |
| **2.2.5** | **Associativity.** The clearest half-page on why left recursion gives left associativity that exists anywhere |
| **2.2.6** | **Precedence.** The stratification technique from L02 §5, presented as a general recipe |

**§2.2.5 and §2.2.6 are the two you will come back to.** They are the method for turning a precedence table into a grammar, and you will apply it twice more — in Lab 0 Part 4 and again in Week 2.

### Dragon §4.2–4.3 — Context-Free Grammars, Formally

**Read after Lecture 2.** This is the same material at a higher altitude, and it introduces two things L02 deliberately skipped.

| § | What to take from it |
|---|---|
| **4.2.1–4.2.4** | Formal notation, derivations, parse trees. Skim if §2.2 landed |
| **4.2.5** | **Why grammars are more powerful than regular expressions.** This is Week 1's central result, arriving early — the argument is that no finite automaton can count nesting depth |
| **4.2.7** | **Ambiguity is undecidable.** Stated and referenced, not proved. Note it and move on |
| **4.3.1–4.3.2** | Eliminating ambiguity, and the **dangling else** — their treatment is L02 §6 with the grammar transformation written out fully |
| **4.3.3** | **Elimination of left recursion.** Read it now, but you will not need it until Week 2 — recursive descent cannot handle left recursion, and this is the fix |
| **4.3.4** | Left factoring. Same — Week 2 |

> **§4.3.3 is the one to remember exists.** In Week 2 you will write a recursive descent parser for
> a grammar written left-recursively in `The Cyan Language Reference`, and it will not work. The
> transformation in §4.3.3 is the reason it can be made to.

### SICP §1.1 — The Elements of Programming

**Why a 1985 Scheme textbook is on a compilers reading list.**

SICP's opening asks what the *elements* of any programming language are, and answers: primitive expressions, means of combination, means of abstraction. **That is a design checklist**, and you will use it in Week 12 to evaluate languages and in Lab 0 Part 5 without noticing.

| § | What to take from it |
|---|---|
| **1.1.1–1.1.2** | Expressions and naming. Note how little machinery is needed before something is a language |
| **1.1.3** | **The substitution model of evaluation.** Read carefully — this is Week 7's beta-reduction, ten weeks early and in friendlier notation |
| **1.1.5** | Applicative versus normal order. **This is a genuine semantic choice**, exactly like C's versus Python's division, and languages really do differ |
| **1.1.7** | Newton's method — skim for the recursion, ignore the numerics |

**§1.1.3 and §1.1.5 are the two that matter.** They are the reason SICP is set in Week 0 rather than Week 7: the substitution model is the simplest complete account of what evaluation *is*, and having seen it now, Week 7's lambda calculus will look like a formalisation rather than a novelty.

---

## Questions to Read Against

Do not write these up. They are for reading with a purpose, and several return in PS 0 and in Quiz 1.

**On Dragon §1.2**

1. The symbol table spans every phase in their diagram. Name one thing the *code generator* needs from it that the *parser* put there.
2. They divide the phases into analysis and synthesis. Which side does optimisation fall on, and is that division as clean as the diagram suggests?

**On Dragon §2.2**

3. §2.2.4 shows `id + id * id` has two parse trees. Which of the two would a reader of C expect, and what in the language definition makes that expectation correct?
4. §2.2.5 argues left recursion produces left associativity. Construct the argument yourself for `E ::= E "-" T`, in one sentence, before reading theirs.
5. The stratification recipe in §2.2.6 adds one non-terminal per precedence level. Cyan has seven levels. **What does that cost at parse time**, and does it cost anything at runtime?

**On Dragon §4.2–4.3**

6. §4.2.5 argues that regular expressions cannot describe balanced parentheses. Reconstruct the argument in terms of what a finite automaton can remember.
7. §4.2.7 says ambiguity is undecidable. **Why is that not fatal in practice?** What do real parser generators check instead? *(L02 §8 has the answer; see whether the book's phrasing sharpens it.)*
8. §4.3.1 removes the dangling else by grammar transformation. Compare that with Cyan's approach of requiring braces. Which produces the better error message when the programmer gets it wrong?

**On SICP §1.1**

9. §1.1.5's applicative order evaluates arguments before the call; normal order does not. **Give a program that terminates under one and not the other.**
10. SICP's three elements — primitives, combination, abstraction. Name Cyan's, one for each, from `The Cyan Language Reference`.

---

## Two Things to Check on Your Own Machine

**1. Your Python's AST.** L01 §4 dumped `1 + 2 * 3` and got `Add` above `Mult`. Run it yourself and then try three more: `1 - 2 - 3`, `2 ** 3 ** 2`, and `not a or b`.

```bash
python3 -c "import ast; print(ast.dump(ast.parse('2 ** 3 ** 2', mode='eval'), indent=2))"
```

**Which of those three is right-associative?** The tree tells you, and you will need the answer in Lab 0 Part 5.

**2. Your gcc's opinion of the dangling else.** L02 §6 got a warning from `-Wall`. Check that your compiler agrees, because you will use `-Wall` all term:

```bash
printf '#include <stdio.h>\nint main(void){int a=0,b=0;\nif(a==1)\n if(b==1)printf("x\\n");\nelse printf("y\\n");\nreturn 0;}\n' > d.c
gcc -Wall -o d d.c && ./d
```

**It should warn and print nothing.** If it prints `y`, your compiler is not C — check what you actually invoked.

---

*Next week's guide covers Dragon Ch. 3 in full — the lexer, regular expressions, and the subset construction. It is the longest single reading of the term, so start it over the weekend.*
