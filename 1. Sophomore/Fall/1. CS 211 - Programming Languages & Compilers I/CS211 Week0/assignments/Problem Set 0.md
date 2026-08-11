# CS 211 · Problem Set 0
## Grammars, Trees, and Ambiguity

---

**Released:** Week 0, Wednesday · **Due:** Week 1, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS0_{LastName}_{StudentID}.pdf`

> Collaboration: discussing approaches is fine and encouraged. The write-up must be yours. State at
> the top: *"I worked on this problem set independently"* or name who you discussed which question
> with.
>
> **Q1, Q2 and Q3 must be done by hand.** You may check with `cfg_count.py` afterwards — you should
> — but show derivations and trees, not tool output. **Q4 and Q5 expect tool output**, and marks
> there depend on you having run it.

---

### Q1: Derivations and Trees (20 points)

Use this grammar throughout Q1:

```bnf
S ::= S ";" A | A
A ::= IDENT "=" E
E ::= E "+" T | T
T ::= T "*" F | F
F ::= IDENT | NUM | "(" E ")"
```

**(a) [6]** Give the **leftmost** derivation of `x = a + b * c`. Show every step.

**(b) [4]** Give the **rightmost** derivation of the same string.

**(c) [4]** Draw the parse tree. State how many nodes it has, counting every non-terminal and every terminal.

**(d) [6]** Draw the **AST** — operators and operands only, no `S`, `A`, `E`, `T` or `F` nodes. How many nodes does it have? **Express the discarded nodes as a percentage of the parse tree**, and say in one sentence what those nodes were *for*, given that they carry no meaning.

---

### Q2: Ambiguity by Hand (22 points)

```bnf
E ::= E "-" E | NUM
```

**(a) [5]** Draw **all** parse trees for `9 - 5 - 2`. There are more than one.

**(b) [5]** Evaluate each tree. Do they agree? **This is the point of the question** — state precisely what the grammar has failed to specify.

**(c) [6]** Rewrite the grammar so that `-` is **left**-associative, and confirm by drawing the single tree that `9 - 5 - 2` now gets. What does it evaluate to?

**(d) [6]** Now rewrite it so `-` is **right**-associative instead. What does `9 - 5 - 2` evaluate to under that grammar? **Name a language, any language, in which subtraction is right-associative** — or, if you believe there is none in common use, say why the left-associative choice is universal.

---

### Q3: Counting Without Counting (14 points)

**(a) [6]** The ambiguous grammar `E ::= E "+" E | n` gives $C_{k-1}$ parse trees for $k$ operands, where $C$ is the Catalan sequence $1, 1, 2, 5, 14, 42, \dots$

**Derive the recurrence yourself.** Let $T(k)$ be the number of trees for $k$ operands. The root `+` splits the operands into a left group of $i$ and a right group of $k - i$. Write $T(k)$ as a sum, and state the base case.

**(b) [4]** Use your recurrence to compute $T(7)$ by hand. Show the arithmetic.

**(c) [4]** $C_k$ grows as roughly $4^k / k^{1.5}$. A 30-operand expression is not unusual in real code. **Approximately how many parse trees would the ambiguous grammar admit for it?** An order of magnitude is enough. Comment, in one sentence, on what this means for a parser that tried to enumerate them.

---

### Q4: The Ambiguity Checker (24 points)

Use `cfg_count.py` from Lab 0.

Both grammars below are attempts at a list with an **optional trailing comma** — `[1, 2, 3,]` legal, as in Python, Rust and Go. **Each is broken, and they are broken in different ways.** Telling the two kinds of defect apart is the point of the question.

**(a) [8]** Grammar One:

```python
LIST_A = {
    'L': [('[', 'items', ']'), ('[', ']')],
    'items': [('items', ',', 'items'), ('e',), ('items', ',')],
    'e': [('n',)],
}
```

**Find a string with more than one parse tree.** Report the shortest one you can find and its count, then report the count for `[ n , n , n , ]`. Explain, in terms of which productions fire, *where* two of the derivations diverge.

**(b) [8]** Grammar Two:

```python
LIST_B = {
    'L': [('[', 'items', ']'), ('[', ']')],
    'items': [('items', ',', 'e'), ('e',), ('items', ',')],
    'e': [('n',)],
}
```

**Run the counter on `[ n , n , ]` and on `[ n , , n ]`.** Grammar Two is *not* ambiguous — every string it accepts gets exactly one tree. **State precisely what is wrong with it anyway**, and say why the ambiguity checker alone would never have told you.

> This is the lesson: **"unambiguous" and "correct" are independent properties.** A grammar can give
> exactly one tree to a string that should not have been in the language at all.

**(c) [8]** **Write a grammar with neither defect.** A trailing comma must still be permitted. Verify with the counter that all of these give exactly 1:

```
[ ]      [ n ]      [ n , ]      [ n , n ]      [ n , n , ]      [ n , n , n , ]
```

and that all of these give 0:

```
[ , ]      [ , n ]      [ n , , n ]      [ n n ]
```

Paste your grammar and the counter's output for all ten strings.

---

### Q5: Design Under Constraint (20 points)

Cyan's `cmp_expr` is **non-associative**, so `a < b < c` is a syntax error (L02 §7, and `The Cyan Language Reference` §3).

**(a) [6]** C accepts `a < b < c` and evaluates it as `(a < b) < c`. With `a = 1, b = 5, c = 3`, C prints `1`. **Show the arithmetic** that produces `1`, and state why a reader would call it wrong even though C is behaving exactly as specified.

**(b) [6]** Python accepts it too, and answers `False`, by desugaring `a < b < c` into `a < b && b < c`. **The desugaring is not quite that simple.** Consider `f() < g() < h()` where each call has a side effect. Write the desugaring Python actually needs, and say which naive version would be wrong and why.

**(c) [8]** Three languages, three answers: C reinterprets, Python special-cases, Cyan refuses. **Argue for one of the three** as the best design, and — this is where the marks are — **state explicitly what your choice costs**, naming a concrete situation where a user of your chosen language is worse off than a user of one of the other two.

---

## Marks

| Question | Topic | Points |
|---|---|---|
| Q1 | Derivations, parse trees, ASTs | 20 |
| Q2 | Ambiguity and associativity by hand | 22 |
| Q3 | The Catalan recurrence | 14 |
| Q4 | The ambiguity checker, applied | 24 |
| Q5 | Design under constraint | 20 |
| **Total** | | **100** |

---

*Quiz 1, at the start of Tuesday's lecture in Week 1, covers this week's material — Lectures 1 and 2, and the grammar vocabulary in Q1 and Q2 above.*
