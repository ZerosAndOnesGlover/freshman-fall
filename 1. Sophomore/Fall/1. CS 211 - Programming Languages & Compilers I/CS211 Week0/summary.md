# CS 211 · Week 0 · Summary

**Topic —** Syntax against semantics, the four paradigms, and context-free grammars: derivations, parse trees, ambiguity, and how to remove it.
**Lectures —** L01 What a Language Is and Why There Are So Many; L02 Grammars, Derivations, and Ambiguity.
**Work —** PS 0 (100), Lab 0 (unmarked, checked off in session, Friday of Week 0). **No quiz** — Quiz 1 in Week 1 covers this week.
**Takeaway —** A grammar decides a language rather than describing one. `E ::= E "+" E | n` admits 58,786 parse trees for twelve operands — the Catalan numbers, counted mechanically — and the stratified `E ::= E "+" T | T` admits exactly one while generating the identical language. Ambiguity belongs to the grammar, not the language. Measured alongside: C's `-7 / 2` is `-3` and Python's is `-4`, because C's rule is one `idiv` and Python's is not.
**Next —** Week 1 — lexical analysis, regular languages, and why the first phase provably needs no stack.
