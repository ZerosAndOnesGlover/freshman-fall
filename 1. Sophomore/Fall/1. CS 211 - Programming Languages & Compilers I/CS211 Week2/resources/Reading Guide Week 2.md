# CS 211 · Week 2 · Reading Guide
## Dragon Chapter 4 — parsing, and the chapter you will actually reread

---

**Set reading:** Aho et al., **§4.4** (top-down), **§4.5–4.7** (bottom-up). You met **§4.2–4.3** in Week 0's guide; skim them again if grammars feel shaky.
**Optional but recommended:** Appel, **Chapter 3**. Considerably gentler on LR than the Dragon.
**Reference:** `info bison`, especially *"Understanding Your Parser"* — that node is what Lab 2 Part 3 is doing.

**§4.4 before Tuesday, §4.5–4.7 after.** The LR material does not land before you have seen a shift-reduce trace, and L06 §1 gives you one.

---

## The Honest Warning About §4.6

**§4.6 is the hardest section in the book**, and a lot of otherwise-successful students stall on it. It builds LR(0) item sets, then SLR, then canonical LR(1), then LALR, each as a refinement of the last, over about thirty pages of tables.

**You do not need to be able to construct an LALR(1) table by hand.** Nobody does that; `bison` does it. **What you need is to read the output**, which means understanding items, the dot, and what a conflict is — and that is §4.6.2 and §4.6.5, about eight pages.

> **A pragmatic route through §4.6.** Read §4.6.2 (items and the LR(0) automaton) properly. Read
> §4.6.5 (conflicts) properly. **Skim §4.6.3–4.6.4** — the SLR construction — for the idea rather
> than the mechanics. Then read §4.7.1–4.7.4 for LALR, again for the idea. **Come back and do the
> constructions by hand only if a conflict in Week 11 defeats you**, at which point they will
> suddenly seem worth the effort.

---

## Section by Section

| § | What to take from it |
|---|---|
| **4.4.1** | Recursive descent as a general method, including backtracking. **Note that real parsers do not backtrack** — §4.4.3's predictive parsing is what you write |
| **4.4.2** | **FIRST and FOLLOW.** The algorithms are fiddly and the book states them precisely. `lab/first_follow.py` implements exactly these |
| **4.4.3** | LL(1) grammars, and the two conditions. **This is L05 §4** |
| **4.4.4** | Non-recursive predictive parsing — a table-driven LL(1) parser. Interesting contrast: the same grammar class as recursive descent, driven by a table instead of the call stack |
| **4.4.5** | **Error recovery: panic mode and phrase-level.** Read this — L05 §6 claims hand-written parsers give better errors, and this section is what "better than" is measured against |
| **4.5.1–4.5.2** | Handles and handle pruning. **The word "handle" is the book's name for "the thing you are about to reduce"** |
| **4.5.3** | Shift-reduce parsing. **This is L06 §1's trace** |
| **4.5.4** | The two conflict kinds |
| **4.6.2** | **Items and the LR(0) automaton. Read properly** |
| **4.6.5** | **Conflicts, formally. Read properly** |
| **4.7.1–4.7.4** | LALR. Read for the idea: merging LR(1) states with common cores |
| **4.8.1** | **Precedence and associativity declarations.** This is L06 §6, and it is what `%left` compiles to |
| **4.9** | Parser generators — the `yacc`/`bison` manual section |

---

## Three Things Worth Reading Twice

**§4.4.2's FIRST/FOLLOW algorithms.** They are stated as fixed-point iterations — keep applying rules until nothing changes — which is the same shape as the $\varepsilon$-closure in Week 1 and the dataflow analyses in Week 4. **Fixed-point iteration is one of about five ideas this whole course runs on**, and this is its second appearance.

**§4.5.1's definition of a handle.** The subtlety is that a handle is not just "a right-hand side sitting on the stack" — it is one whose reduction leads to a valid rightmost derivation. **L06 §1's row 9 is exactly this**: `E + T` is on the stack and *is* a right-hand side, but it is not a handle, because reducing would be wrong.

**§4.6.5 on conflicts.** Read it against L06 §5. **The book is careful to say a conflict means the grammar is not in the class**, not that it is ambiguous — but it says so once, quietly, and most readers come away with the wrong impression.

---

## What the Book Does Not Say Loudly Enough

**That production compilers abandoned generated parsers.** The Dragon Book is a parser-generator book; it was written when `yacc` was how you built a compiler. **GCC, Clang, rustc, Go and TypeScript all use hand-written recursive descent**, and the reason in every case is error message quality (L05 §6). The book's §4.4.5 on error recovery is the closest it comes to acknowledging why.

**That `-Wcounterexamples` exists.** It is a bison 3.8 feature, postdating the book by fifteen years, and it turns conflict diagnosis from an item-set exercise into reading two derivations. **Lab 2 Part 2.3 uses it.** If you take one tool away from this week, take that flag.

---

## Questions to Read Against

**On §4.4**

1. §4.4.1 describes recursive descent *with backtracking*. **What does backtracking buy**, and why is it unacceptable in a production compiler? *(Think about what the parser has already done by the time it backtracks.)*
2. §4.4.2's FOLLOW algorithm has a case for $A \to \alpha B$ — the last symbol. Explain why FOLLOW($A$) flows into FOLLOW($B$) there.
3. §4.4.3 gives two LL(1) conditions. **The second involves FOLLOW. Give a grammar that satisfies the first and fails the second.**
4. §4.4.5's panic mode discards tokens until it reaches a synchronising token. **What would you use as synchronising tokens for Cyan?** *(`;` and `}` are the obvious ones — why those?)*

**On §4.5–4.6**

5. §4.5.1: give a configuration where a right-hand side is on top of the stack but is **not** a handle. *(L06 §1 row 9, but construct your own.)*
6. §4.6.2: what does it mean for two items to be in the **same state**? What is the state actually recording?
7. §4.6.5: the book distinguishes shift/reduce from reduce/reduce conflicts. **Which is the more serious symptom, and why?**

**On §4.7–4.8**

8. LALR merges LR(1) states with the same core. **What can that merge introduce that pure LR(1) never has?** Can it introduce shift/reduce conflicts, reduce/reduce, or both?
9. §4.8.1's precedence declarations resolve conflicts without changing the grammar. **What information do they add** that the grammar did not contain?

---

## Two Things to Check on Your Own Machine

**1. That bison and your parser disagree about Cyan.**

```bash
bison -Wall -Wcounterexamples -o cyan_par.c cyan.y
```

**You should see two reduce/reduce conflicts on `[` and `.`.** Your `parser.py` parses the same language with no complaint. **Neither is broken** — L06 §5 explains why, and PS 2 Q3(c) asks you to explain it back.

**2. The flag that makes conflicts readable.**

```bash
bison -Wcounterexamples -o dangling.c dangling.y
```

Compare that output against the same run without the flag. **The difference is the difference between a diagnosis and a complaint.**

---

*Next week's reading is Dragon §2.7, §6.5 and Chapter 5's attribute grammars, plus TAPL Chapter 22 for Hindley-Milner. Shorter than this week, and the TAPL chapter is the one that repays slow reading.*
