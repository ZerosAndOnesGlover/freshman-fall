# CS 211 · Reading Guide · Week 7
## Functional Programming: The Lambda Calculus

**Read against a question.** This week's literature has an unusual failure mode: it is *beautiful*, and it is easy to spend an evening reading about the Y combinator and end up unable to reduce a term by hand. **Reduce terms by hand.** Everything else follows and nothing substitutes for it.

---

## Before Tuesday (L15 — syntax, substitution, reduction)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Pierce, TAPL** | **ch. 5.1** | Syntax, currying, and the conventions. The clearest statement of "body extends rightwards" in print. | 6 |
| **Pierce, TAPL** | **ch. 5.3** | Formal definitions of substitution, free variables, and alpha-conversion. **Read Definition 5.3.5 with `lam.py`'s `subst` open** — they are the same function. | 5 |
| **Appel** | **ch. 15.1** | The same material from a compiler-writer's angle, in four pages. | 4 |
| **Barendregt** | **ch. 2** | The canonical treatment. Denser than you need; read §2.1 for the variable convention and stop. | 8 |

**Skip for now:** anything on confluence and the Church–Rosser theorem. It is beautiful, it is not needed until L16 §8, and it will crowd out substitution.

---

## Before Thursday (L16 — encodings, recursion, evaluation order)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Pierce, TAPL** | **ch. 5.2** | Church numerals, booleans, pairs, and `fix`. **The single best twelve pages on this week's material.** | 12 |
| **SICP** | **§1.3** | Higher-order procedures. Not lambda calculus, but it is where "a datum is the function that uses it" becomes natural rather than clever. Free at mitpress.mit.edu. | 20 |
| **SICP** | **§3.5.1–3.5.2** | Streams, and the `delay`/`force` pair. **This is L16 §10's thunk, in Scheme, with the motivation spelled out.** | 12 |
| **Pierce, TAPL** | **ch. 5.3, "Evaluation"** | Call-by-value stated formally, and why `fix` needs its extra lambda. | 4 |

---

## Papers, If You Want Them

- **Church, A. (1936), "An Unsolvable Problem of Elementary Number Theory."** The paper. Short, and §7 is the undecidability result L16 §13 leans on.
- **Turing, A. (1937), "Computability and λ-Definability."** The equivalence proof, by Turing, in twelve pages.
- **Wadsworth, C. (1971), thesis, ch. 4.** Where call-by-need — the strategy PS 7 Part B3 asks you to implement — was invented. The graph-reduction picture is worth more than the prose.
- **Hughes, J. (1989), "Why Functional Programming Matters."** Not about the calculus at all; it is the argument for why laziness buys modularity. **Read it if PS 7 B3 leaves you asking what sharing is *for*.**

---

## Documentation

- **`docs.python.org/3/reference/expressions.html#lambda`** — Python's one-expression restriction on `lambda`, and why it exists. Relevant to `strict.py`.
- **The Haskell Report, §3.1** — where the language commits to non-strict semantics. Two paragraphs, and they are the whole difference from every language in `strict.py`.

---

## The One Thing Worth Reading Twice

**TAPL Definition 5.3.5, the substitution rule** — specifically its side condition, `y ∉ FV(s)`.

Read it, then run:

```bash
python3 lam.py '(\x y. x) y'
python3 lam.py '(\x y. x) y' --naive
```

The book states the side condition and moves on. **It does not tell you that violating it produces a well-formed term that computes a different function silently** — you get the identity where you asked for a constant function, with no error, in one step.

Noticing that the side condition is the *entire content* of the definition — that everything else in it is bookkeeping — is the difference between having read §5.3 and having understood it.

---

## A Note on What This Week Is For

It is reasonable to reach Thursday wondering why a compilers course spent a week on a language with no numbers.

Three answers, in increasing order of how much they matter.

**The immediate one:** your compiler cannot lower a lambda. `tac.py` raises `NotImplementedError` on the `Lambda` node your parser has been building since Week 2, and Project 1 lists first-class functions as one of its two hardest options. You cannot implement closures without knowing what a closure is a representation *of*.

**The structural one:** this is where the rest of the term's ideas came from. Substitution is Week 3's scope rule. Evaluation order is Week 4's decision about when `&&` evaluates its right operand. Eta-reduction is a real pass in a real optimiser. Undecidability is why every analysis in Week 5 was an approximation and had to be.

**The one that lasts:** the untyped calculus is where you find out that `zero`, `false` and `nil` are the same term, and that nothing in the language can tell them apart. **Week 8 is the answer to that**, and it will not land unless you have felt the problem. Do Lab 7 Q8 honestly.

---

*CS 211 · Week 7 · Reading Guide · © CSE Department*
