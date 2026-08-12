# CS 211 · Week 3 · Summary

**Topic —** Semantic analysis: symbol tables, scope chains, type checking, and Hindley-Milner inference by unification.
**Lectures —** L07 Symbol Tables, Scope, and the First Phase That Says No; L08 Hindley-Milner, and the Algorithm That Guesses Right.
**Work —** PS 3 (100), Lab 3 (unmarked, Friday of Week 3), Quiz 3 (unmarked, Tuesday, covers Week 2). **Midterm 1 announced** — sat Week 4, covers Weeks 0–3.
**Takeaway —** A position must be recorded by the phase that has it. The checker reports `line 4 col 5: '+' needs int operands` because the parser copied the operator token's position onto the node; by then the tokens are gone and nothing can recover it. Eighteen programs that parse cleanly are rejected here. Separately, HM derives `(t -> t) -> t -> t` for `\f -> \x -> f (f x)` with nothing annotated — agreeing with GHC on all six test cases, since the principal type theorem says there is only one answer to find.
**Next —** Week 4 — the typed tree becomes three-address code and a control-flow graph, and Midterm 1 covers everything to here.
