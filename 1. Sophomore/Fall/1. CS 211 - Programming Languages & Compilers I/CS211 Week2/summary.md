# CS 211 · Week 2 · Summary

**Topic —** Parsing: recursive descent, left recursion, FIRST/FOLLOW and LL(1); shift-reduce, items, LALR(1), and how to read a conflict report.
**Lectures —** L05 Recursive Descent, and the Grammars That Fight Back; L06 Bottom-Up Parsing, and What Bison Is Telling You.
**Work —** PS 2 (100), Lab 2 (unmarked, Friday of Week 2), Quiz 2 (unmarked, Tuesday, covers Week 1).
**Takeaway —** A conflict report is a statement about the tool. bison finds two reduce/reduce conflicts in Cyan's grammar on `[` and `.`; Week 0's counter proved the same grammar gives exactly one tree to each of 23 valid programs. Both are right — bison decides *is this LALR(1)*, which is decidable, not *is this ambiguous*, which is not. The dangling else really is ambiguous, and left factoring moves its LL(1) conflict without removing it.
**Next —** Week 3 — semantic analysis, and the first phase that rejects programs the parser was perfectly happy with.
