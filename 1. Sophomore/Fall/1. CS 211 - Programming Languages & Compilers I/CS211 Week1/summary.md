# CS 211 · Week 1 · Summary

**Topic —** Lexical analysis: tokens, regular expressions, maximal munch, finite automata, the subset construction, minimisation, and why parsing needs a stack.
**Lectures —** L03 Tokens, Regular Expressions, and Maximal Munch; L04 Finite Automata and the Subset Construction.
**Work —** PS 1 (100), Lab 1 (unmarked, Friday of Week 1), Quiz 1 (unmarked, Tuesday, covers Week 0).
**Takeaway —** The subset construction's exponential is attained exactly: $(a|b)^*a(a|b)^n$ gives 58 NFA states against a minimal DFA of 512, and minimisation removes one state and stops. Cyan's whole token set is 70 DFA states from a 176-state NFA — smaller than its NFA. Both lexers agree on 109 tokens of valid input and part on three invalid ones, all about error recovery rather than tokenising.
**Next —** Week 2 — parsing, where the Week 0 grammar becomes one function per non-terminal and left recursion immediately breaks it.
