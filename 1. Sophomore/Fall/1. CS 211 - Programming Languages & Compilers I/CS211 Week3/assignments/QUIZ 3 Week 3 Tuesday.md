# CS 211 · Quiz 3
## Administered: Tuesday, Week 3 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 2** — recursive descent, left recursion, FIRST/FOLLOW and LL(1), shift-reduce parsing, LALR(1), and conflict reports.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then mark it yourself before you leave the room.

---

**Q1.** Why does a left-recursive rule break a recursive descent parser? One sentence.

&nbsp;

&nbsp;

---

**Q2.** What does LL(1) stand for — all three parts?

&nbsp;

&nbsp;

---

**Q3.** Why is FOLLOW needed at all? Give the situation where FIRST alone is not enough.

&nbsp;

&nbsp;

---

**Q4.** Left-factoring the dangling-else grammar does not make it LL(1). Why not?

&nbsp;

&nbsp;

---

**Q5.** In a shift-reduce parse of `n + n * n`, the stack holds `E + T` and the next token is `*`. Shift or reduce, and why?

&nbsp;

&nbsp;

---

**Q6.** bison reports a conflict on your grammar. Name the **two** different things that could mean.

&nbsp;

&nbsp;

---

**Q7.** In a bison state report, one action appears in square brackets. What does that signify?

&nbsp;

&nbsp;

---

\pagebreak

---

## Answer Key — mark your own before leaving

**Q1.** **The function calls itself before consuming any input**, so it recurses forever without ever examining a token. `parse_add` whose first action is `parse_add()` never terminates.

*Note it is a structural incompatibility, not a bug — and the left recursion is there on purpose, because it is what makes `+` left-associative.*

---

**Q2.** **L**eft-to-right scan · **L**eftmost derivation · **1** token of lookahead.

---

**Q3.** **Because of ε-productions.** When the parser is at `E'` and the next token is `)`, no production of `E'` *starts* with `)` — but `E' → ε` is legal exactly when the next token can follow `E'`. **FOLLOW is the set that licenses taking the empty production.**

---

**Q4.** **Because the grammar is not merely awkwardly presented — the language is ambiguous.** Left factoring removes shared prefixes; this conflict is not about a shared prefix. After factoring, `else` appears in **both** FIRST(`else S`) and FOLLOW(`S'`), so the conflict simply moves to `S'`.

---

**Q5.** **Shift.** `E + T` *is* the right-hand side of `E → E + T`, but reducing now would be wrong — the `*` means the `T` is not finished, and `T * F` must be reduced to `T` first.

*This is the whole difficulty of bottom-up parsing: a right-hand side on the stack is not necessarily a* handle.

---

**Q6.** Either:

1. **The grammar is genuinely ambiguous** — the dangling else.
2. **The grammar is unambiguous but not LALR(1)** — the tool could not prove determinism with one token of lookahead. **Cyan's own grammar is this case.**

*Full marks require both. "My grammar is ambiguous" alone is the misconception the week exists to correct.*

---

**Q7.** **The action bison disabled.** It is printed so you can see which alternative the resolution discarded — not an additional action.

---

### If you got fewer than 5

**Re-read L06 §5 before Thursday.** Q6 is the one that matters: bison decides *LALR(1)-ness*, which is decidable, and cannot decide *ambiguity*, which is not. That distinction returns in Week 11 when your own compiler reports a conflict and nobody is there to tell you which kind it is.

---

*CS 211 · Quiz 3 · Covers Week 2 · Unmarked*
