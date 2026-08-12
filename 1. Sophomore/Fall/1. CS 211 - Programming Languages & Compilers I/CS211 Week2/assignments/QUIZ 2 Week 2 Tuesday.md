# CS 211 · Quiz 2
## Administered: Tuesday, Week 2 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 1** — tokens, regular expressions, maximal munch, finite automata, the subset construction, minimisation, and the limits of finite state.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** A token carries three things. Name them, and say which one exists purely for error messages.

&nbsp;

&nbsp;

---

**Q2.** State the maximal munch rule, including the tie-break.

&nbsp;

&nbsp;

---

**Q3.** How does the Cyan lexer tokenise `x-->y`? Give the tokens.

&nbsp;

&nbsp;

---

**Q4.** In the subset construction, what *is* a single DFA state?

&nbsp;

&nbsp;

---

**Q5.** An NFA has $n$ states. What is the largest number of states its DFA can have, and does minimisation avoid it?

&nbsp;

&nbsp;

---

**Q6.** Cyan comments do not nest. What does `a/* /* */ */b` lex to?

&nbsp;

&nbsp;

---

**Q7.** True or false: no finite automaton can recognise the language of parentheses balanced and nested **at most 100 deep**. Justify in one sentence.

&nbsp;

&nbsp;

---

\pagebreak

---

## Answer Key — mark your own before leaving

**Q1.** **A kind** (`IDENT`, `OP`, …), **the text** (the lexeme), and **a source position** (line and column). **The position exists for error messages** — nothing else in the compiler needs it, and it cannot be recovered later if the lexer drops it.

---

**Q2.** **At each position take the longest match. If two rules match the same longest string, take the one listed first.**

*Both halves are needed. The first settles `<=` against `<` then `=`; the second settles `if` matching both the keyword rule and `IDENT`.*

---

**Q3.** **`IDENT(x)` `OP(-)` `OP(->)` `IDENT(y)`** — four tokens.

At the first `-`, the longest match is just `-`, because `--` is not a Cyan operator and `->` needs a `>` next. At the second `-`, `->` matches.

*Give yourself the mark only for all four in the right order. The parser then rejects this in Week 2 — but the lexer did its job correctly.*

---

**Q4.** **A set of NFA states** — precisely the set of NFA states the machine could currently be in, closed under $\varepsilon$-transitions.

*"A state of the DFA" is not an answer. The content of the idea is the word* set.

---

**Q5.** **Up to $2^n$.** **No — minimisation does not avoid it.**

$(a\mid b)^*a(a\mid b)^n$ attains it: an NFA of 58 states gives a minimal DFA of exactly 512. Minimisation removed **one** state. The remaining states are not redundant, because the machine genuinely must distinguish $2^{n+1}$ different histories.

---

**Q6.** **`IDENT(a)` `OP(*)` `OP(/)` `IDENT(b)`.**

The comment opens at the first `/*` and closes at the **first** `*/`. The inner `/*` is just characters. What remains, ` */b`, is live code: `*`, `/`, `b`.

---

**Q7.** **False — it *is* regular, and a DFA needs about 102 states.**

One state per depth 0–100, plus a dead state. **The counter is bounded, so it fits in finite memory.** The impossibility proof requires *unbounded* nesting: it feeds $k+1$ strings of increasing depth to force two into the same state, and with depth capped at 100 there are only 101 depths to feed.

*This is the most-missed question of the week. "Finite automata cannot count" is a slogan missing its qualifier, and the qualifier is the content.*

---

### If you got fewer than 5

**Re-read L04 §5 and §7 before Thursday.** Week 2 opens with a parser that needs a stack, and the reason it needs one is Q7's proof — with the unbounded case, not the bounded one.

---

*CS 211 · Quiz 2 · Covers Week 1 · Unmarked*
