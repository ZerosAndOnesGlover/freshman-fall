#!/usr/bin/env python3
"""
CS 211 · Lab 0 · A parse-tree counter for context-free grammars.

Given a grammar and a token string, this counts how many distinct parse trees
the grammar admits. That count is the operational definition of ambiguity:

      0  ->  the string is not in the language
      1  ->  in the language, unambiguously
     >1  ->  in the language, and the grammar does not say which tree you meant

You will use it in Lab 0 to watch an ambiguous grammar explode, and again in
Week 2 when bison starts reporting shift/reduce conflicts.

--------------------------------------------------------------------------
HOW GRAMMARS ARE WRITTEN HERE

A grammar is a dict mapping each non-terminal to a list of productions.
Each production is a tuple of symbols. Any symbol that is not a key of the
dict is a terminal.

    expr = {
        'E': [('E', '+', 'T'), ('T',)],     # E ::= E "+" T | T
        'T': [('T', '*', 'F'), ('F',)],     # T ::= T "*" F | F
        'F': [('n',), ('(', 'E', ')')],     # F ::= n | "(" E ")"
    }

Left recursion is fine -- it is detected and handled. The empty production
is written as the empty tuple ().

--------------------------------------------------------------------------
USAGE

    from cfg_count import make_counter
    count = make_counter(expr)
    count("n + n * n".split(), 'E')      # -> 1

Run this file directly for a demonstration:

    $ python3 cfg_count.py
"""


def make_counter(grammar):
    """Build a parse-tree counter for `grammar`.

    Returns a function count(tokens, start) -> int.

    The method is memoised top-down enumeration over spans: for each
    (symbol, i, j) we ask how many trees derive tokens[i:j] from symbol, and
    cache the answer. That makes it polynomial rather than exponential, which
    matters -- section 4 of Lecture 2 counts 58,786 trees for one string, and
    enumerating them one by one would be hopeless.

    Left recursion would loop forever under naive recursion, so a span
    currently being computed is treated as contributing nothing: a derivation
    that reaches A over the same span it started from has added no terminals
    and so cannot lead anywhere new.
    """
    nonterminals = set(grammar)
    memo = {}
    in_progress = set()

    def count_symbol(sym, i, j, toks):
        if sym not in nonterminals:                 # a terminal
            return 1 if j - i == 1 and toks[i] == sym else 0

        key = (sym, i, j)
        if key in memo:
            return memo[key]
        if key in in_progress:                      # left-recursive cycle
            return 0

        in_progress.add(key)
        total = sum(count_seq(prod, 0, i, j, toks) for prod in grammar[sym])
        in_progress.discard(key)

        memo[key] = total
        return total

    def count_seq(prod, k, i, j, toks):
        """Trees for the tail prod[k:] spanning toks[i:j]."""
        if k == len(prod):
            return 1 if i == j else 0
        if k == len(prod) - 1:                      # last symbol takes the rest
            return count_symbol(prod[k], i, j, toks)

        total = 0
        for split in range(i, j + 1):               # try every split point
            left = count_symbol(prod[k], i, split, toks)
            if left:
                total += left * count_seq(prod, k + 1, split, j, toks)
        return total

    def count(tokens, start):
        memo.clear()
        in_progress.clear()
        return count_symbol(start, 0, len(tokens), list(tokens))

    return count


# ---------------------------------------------------------------------------
# The two grammars from Lecture 2.

AMBIGUOUS = {
    'E': [('E', '+', 'E'), ('E', '*', 'E'), ('n',), ('(', 'E', ')')],
}

STRATIFIED = {
    'E': [('E', '+', 'T'), ('T',)],
    'T': [('T', '*', 'F'), ('F',)],
    'F': [('n',), ('(', 'E', ')')],
}


def _plus_chain(k):
    """Token list for k operands joined by '+':  n + n + ... + n"""
    toks = ['n']
    for _ in range(k - 1):
        toks += ['+', 'n']
    return toks


def _demo():
    amb = make_counter(AMBIGUOUS)
    strat = make_counter(STRATIFIED)

    print("Parse trees for  n + n + ... + n\n")
    print(" operands | ambiguous | stratified")
    print("----------+-----------+-----------")
    for k in range(1, 13):
        toks = _plus_chain(k)
        print(f"{k:>9} | {amb(toks, 'E'):>9} | {strat(toks, 'E'):>10}")

    print("\nMixed operators:\n")
    for src in ["n + n * n", "n * n + n", "n + n * n + n", "( n + n ) * n"]:
        toks = src.split()
        print(f"  {src:<16} ambiguous: {amb(toks, 'E'):>2}   "
              f"stratified: {strat(toks, 'E')}")

    print("\nStrings in neither language (both must be 0):\n")
    for src in ["n +", "+ n", "n n", "( n", "n + + n"]:
        toks = src.split()
        print(f"  {src:<16} ambiguous: {amb(toks, 'E'):>2}   "
              f"stratified: {strat(toks, 'E')}")

    print("\nBoth grammars generate exactly the same language.")
    print("They disagree only on how many trees each string gets.")


if __name__ == '__main__':
    _demo()
