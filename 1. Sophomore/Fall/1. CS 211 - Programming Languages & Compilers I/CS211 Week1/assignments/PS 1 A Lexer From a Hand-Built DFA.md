# CS 211 · Problem Set 1
## A Lexer From a Hand-Built DFA

---

**Released:** Week 1, Wednesday · **Due:** Week 2, Friday 17:00
**Total: 100 points** · Submit one PDF (`PS1_{LastName}_{StudentID}.pdf`) **and** `lexer.py`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Q1–Q3 are by hand.** You may check with code afterwards, and Q3 tells you how. **Q5 is the code
> deliverable** and is the first piece of `cyanc` you will keep — Week 2's parser consumes its
> output, so it is worth doing properly rather than just passing the tests.

---

### Q1: Regular Expressions, Formally (16 points)

Use only the four operators from L03 §3 — literal, concatenation, alternation, Kleene star. **`+`, `?` and `[a-z]` are permitted as abbreviations**; backreferences are not.

**(a) [4]** Write a regular expression over $\{a, b\}$ for **strings of even length**.

**(b) [4]** Write one for **strings containing an even number of `a`s**. *(These are different languages. Check your answer against `aab`.)*

**(c) [4]** Cyan's `STRING` token is `" ( [^"\\\n] | \\. )* "`. **Explain why the `\\.` alternative is needed** and what goes wrong without it. Give a concrete string literal that lexes incorrectly if it is removed.

**(d) [4]** Python's `re` supports backreferences. Consider `([ab]+)\1` — any non-empty string over $\{a,b\}$ followed by an identical copy. **Argue that this language is not regular.** Use the counting argument from L04 §7; you do not need a formal pumping-lemma statement, but you do need the pigeonhole step.

> **Why `[ab]` and not just `a`.** Over a one-letter alphabet, `(a+)\1` matches exactly the
> even-length strings — which *is* regular, and the backreference buys nothing. **The alphabet
> matters**, and noticing why is half the question.

---

### Q2: Thompson and the Subset Construction (24 points)

Let $r = (a \mid b)^* b a$.

**(a) [8]** Build the NFA by Thompson's construction. **Draw it**, label every state, and mark the $\varepsilon$-transitions. State how many states it has.

**(b) [10]** Run the subset construction. **Show your working as a table** with one row per DFA state:

| DFA state | NFA subset | on `a` | on `b` |
|---|---|---|---|

**(c) [6]** Give the language of each of your DFA states in English — *"the last character was a `b`"*, and so on. **A state whose meaning you cannot state in a short English sentence is usually a sign of an error**, so treat this as a check on (b).

---

### Q3: Minimisation and Equivalence (20 points)

**(a) [8]** Minimise your DFA from Q2 by partition refinement. Show the partition at each round. How many states does the minimal DFA have?

**(b) [6]** L04 §6 states the minimal DFA is **unique up to renaming**, which makes regular-expression equivalence decidable. **Use this to decide** whether

$$(a \mid b)^* \qquad \text{and} \qquad (a^* b^*)^*$$

denote the same language. Construct both minimal DFAs and compare.

**(c) [6]** Check (b) with code. `lab/cfg_count.py` will not help — it counts parse trees, not automata — so **write the check yourself**, or reason it out and say why no code is needed. **Either answer earns full marks if it is right**; state clearly which route you took.

---

### Q4: Why the Parser Needs a Stack (14 points)

**(a) [8]** L04 §7 proves no finite automaton recognises balanced parentheses. **Reproduce the proof.** Be explicit about: how many inputs you feed, how many states are available, which pigeonhole step applies, and what contradiction follows.

**(b) [6]** Now the question that catches people. **Is the language of parentheses balanced and nested at most 100 deep regular?**

Answer, and justify. **If you answer yes, you must say how many states the DFA needs.** If you answer no, you must say where the proof in (a) still applies.

---

### Q5: The Lexer (26 points)

**Write `lexer.py`** — a lexer for Cyan implementing `The Cyan Language Reference` §2 in full.

**Do not use `re`, and do not use `flex`.** Write the character loop by hand. The point is that you have implemented a DFA, not that you have produced tokens.

#### Required interface

```python
tokenize(src: str) -> list[Token]     # Token has .kind, .text, .line, .col
```

with kinds `KEYWORD`, `IDENT`, `INT`, `STRING`, `OP`, `PUNCT`, and a command-line mode:

```bash
$ python3 lexer.py program.cy
KEYWORD(fn)
IDENT(fib)
...
```

#### Requirements

1. **All thirteen keywords**, distinguished from identifiers by a set lookup after matching `IDENT` — not by thirteen separate branches.
2. **Maximal munch** on operators. `<=` is one token; `x-->y` is `x` `-` `->` `y`.
3. **Both comment forms.** `//` to end of line, and `/* */` **not nested**.
4. **String escapes** `\n`, `\t`, `\\`, `\"`. A newline inside a string literal is an error.
5. **`line` and `col` on every token**, 1-based. **Week 3 depends on this**; PS 3 will ask you to report an error at a source position and you will not be given a chance to add it retrospectively.
6. **Errors raise `LexError` with a line number**, and do not silently skip the character.

#### Marks

| | |
|---|---:|
| Produces the correct 109 tokens for `lab/sample.cy` | 8 |
| Maximal munch correct on all six inputs from L03 §4 | 5 |
| Comments and strings, including the `a/* /* */ */b` case | 5 |
| Positions correct — verified by a deliberate error on line 12 of a test file | 4 |
| Errors raised, not swallowed; message names the line | 4 |

**Verify before submitting:**

```bash
python3 lexer.py ../lab/sample.cy | diff - expected_tokens.txt
```

**(b) [included above]** In your PDF, report **one input on which your lexer disagrees with `flex`**, and say which behaviour you chose and why. If you believe there is none, say what you tested — Lab 1 Part 3 found three, so "none" needs evidence.

---

## Marks

| Question | Topic | Points |
|---|---|---|
| Q1 | Regular expressions, formally | 16 |
| Q2 | Thompson and the subset construction | 24 |
| Q3 | Minimisation and equivalence | 20 |
| Q4 | Why the parser needs a stack | 14 |
| Q5 | The lexer | 26 |
| **Total** | | **100** |

---

*Quiz 2, at the start of Tuesday's lecture in Week 2, covers this week — regular expressions, the two automata, maximal munch, and the subset construction.*
