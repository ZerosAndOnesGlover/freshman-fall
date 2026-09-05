#!/usr/bin/env python3
"""Parser combinators: the grammar, as a value.

Week 2 wrote a recursive-descent parser by hand -- one function per
non-terminal, `parse_expr` calling `parse_add` calling `parse_mul`, four
hundred lines of it in `parser.py`. The structure of the grammar was
*encoded in the call graph*, which meant it existed only in the shape of the
code and could not be examined, transformed, or built at run time.

A parser combinator is a parser that is a **value**. `seq(a, b)` is a parser;
`alt(a, b)` is a parser; `many(a)` is a parser. The grammar becomes an
expression you can pass around, store in a dict, and generate.

    python3 combinators.py

**This is an internal DSL** -- a little language for grammars, embedded in
Python, using nothing but functions and operators. Compare with an external
DSL like bison (Week 2's `cyan.y`), which has its own syntax, its own file,
and its own generator program.

The trade is measured at the bottom of this file, and it is not one-sided.
"""
import re
import sys
from dataclasses import dataclass


# ------------------------------------------------------------------ results
@dataclass(frozen=True)
class Ok:
    value: object
    rest: str

    def __bool__(self):
        return True


@dataclass(frozen=True)
class Err:
    expected: str
    at: str

    def __bool__(self):
        return False

    def __str__(self):
        where = self.at[:18].replace('\n', ' ') or '<end of input>'
        return f"expected {self.expected} at {where!r}"


class Parser:
    """A function from input to a result, wrapped so operators work.

    `>>` maps a function over the result. `|` is alternation. `+` is
    sequencing. Those three operators are the whole surface of the DSL, and
    everything below is built from them.
    """

    __slots__ = ('fn', 'name')

    def __init__(self, fn, name='?'):
        self.fn, self.name = fn, name

    def __call__(self, s):
        return self.fn(s)

    def __or__(self, other):
        return alt(self, other)

    def __add__(self, other):
        return seq(self, other)

    def __rshift__(self, f):
        return mapp(self, f)

    def __repr__(self):
        return f"<parser {self.name}>"

    def parse(self, s):
        """Run and require that the whole input was consumed."""
        r = self(s.strip())
        if not r:
            raise SyntaxError(str(r))
        if r.rest.strip():
            raise SyntaxError(f"trailing input at {r.rest.strip()[:18]!r}")
        return r.value


# ---------------------------------------------------------------- primitives
def regex(pattern, name=None):
    rx = re.compile(pattern)

    def go(s):
        m = rx.match(s.lstrip())
        if not m:
            return Err(name or pattern, s)
        consumed = len(s) - len(s.lstrip())
        return Ok(m.group(0), s[consumed + m.end():])
    return Parser(go, name or pattern)


def lit(text):
    def go(s):
        t = s.lstrip()
        if t.startswith(text):
            consumed = len(s) - len(t)
            return Ok(text, s[consumed + len(text):])
        return Err(repr(text), s)
    return Parser(go, repr(text))


def seq(*ps):
    def go(s):
        out = []
        for p in ps:
            r = p(s)
            if not r:
                return r
            out.append(r.value)
            s = r.rest
        return Ok(out, s)
    return Parser(go, ' '.join(p.name for p in ps))


def alt(*ps):
    def go(s):
        errs = []
        for p in ps:
            r = p(s)
            if r:
                return r
            errs.append(r.expected)
        return Err(' or '.join(errs), s)
    return Parser(go, ' | '.join(p.name for p in ps))


def many(p):
    def go(s):
        out = []
        while True:
            r = p(s)
            if not r:
                return Ok(out, s)
            if r.rest == s:                # zero-width match: would loop
                raise RuntimeError(f"{p.name} matched without consuming")
            out.append(r.value)
            s = r.rest
    return Parser(go, f"({p.name})*")


def mapp(p, f):
    def go(s):
        r = p(s)
        return Ok(f(r.value), r.rest) if r else r
    return Parser(go, p.name)


def lazy(thunk):
    """A parser defined in terms of itself, later.

    Needed because a grammar is recursive and Python evaluates eagerly: at
    the moment you write `expr`, `expr` does not exist yet. This is Week 7's
    thunk, doing Week 7's job, in a completely different setting.
    """
    return Parser(lambda s: thunk()(s), 'lazy')


def sep_by(p, sepp):
    rest = many(seq(sepp, p) >> (lambda v: v[1]))
    return (seq(p, rest) >> (lambda v: [v[0]] + v[1])) | Parser(
        lambda s: Ok([], s), 'empty')


# ------------------------------------------------- an arithmetic grammar
#
#   expr  := term (('+'|'-') term)*
#   term  := atom (('*'|'/') atom)*
#   atom  := NUMBER | '(' expr ')'
#
# Compare with Week 2's `parser.py`: three functions, three call levels, and
# the same three productions -- written there as control flow, written here
# as data.
#
NUMBER = regex(r'\d+(?:\.\d+)?', 'number') >> (
    lambda t: float(t) if '.' in t else int(t))


def _fold(v):
    """[first, [(op, operand), ...]] -> a left-associated tree."""
    node, rest = v[0], v[1]
    for op, operand in rest:
        node = (op, node, operand)
    return node


atom = lazy(lambda: NUMBER | (seq(lit('('), expr, lit(')'))
                              >> (lambda v: v[1])))
term = seq(atom, many(seq(lit('*') | lit('/'), atom))) >> _fold
expr = seq(term, many(seq(lit('+') | lit('-'), term))) >> _fold


def evaluate(node):
    if not isinstance(node, tuple):
        return node
    op, l, r = node
    l, r = evaluate(l), evaluate(r)
    return {'+': l + r, '-': l - r, '*': l * r, '/': l / r}[op]


# ------------------------------------------------------------- the trap
#
# The grammar above is right-recursive-ish and works. Write the SAME language
# left-recursively -- which is the natural way to express left associativity
# -- and it does not.
#
bad_expr = lazy(lambda: (seq(bad_expr, lit('+'), NUMBER) >> _fold) | NUMBER)


# -------------------------------------------------------------------- main
def main():
    print("; ---- the grammar is a value ----")
    print(f"  expr = {expr!r}")
    print(f"  it is an object: {type(expr).__name__}, "
          f"built at import time from `seq`, `alt` and `many`")
    print("  Week 2's parser was a call graph. This one is a data structure.")

    print("\n; ---- parsing ----")
    cases = ["1 + 2", "2 * 3 + 4", "2 + 3 * 4", "(2 + 3) * 4",
             "10 - 2 - 3", "1 + 2 * (3 - 1) / 2"]
    bad = 0
    for src in cases:
        tree = expr.parse(src)
        got, want = evaluate(tree), eval(src)
        ok = abs(got - want) < 1e-9
        bad += not ok
        print(f"  {src:<24} => {got!s:<8} "
              f"{'ok' if ok else 'MISMATCH (python says ' + str(want) + ')'}")

    print("\n; ---- associativity is in the fold, not the grammar ----")
    print(f"  10 - 2 - 3  parses as  {expr.parse('10 - 2 - 3')}")
    print("  `_fold` walks left to right, so `-` comes out left-associative.")
    print("  Change `_fold` and you change associativity without touching")
    print("  a single production.")

    print("\n; ---- errors ----")
    for src in ("1 +", "(1 + 2", "1 + + 2", "1 2"):
        try:
            expr.parse(src)
            print(f"  {src:<24} => parsed (unexpectedly)")
            bad += 1
        except SyntaxError as e:
            print(f"  {src:<24} => {e}")

    print("\n; ---- the trap: left recursion ----")
    print("  bad_expr := bad_expr '+' NUMBER | NUMBER")
    try:
        bad_expr.parse("1 + 2")
        print("  parsed (unexpectedly)")
        bad += 1
    except RecursionError:
        print("  => RecursionError: infinite recursion before reading a token")
    except SyntaxError as e:
        print(f"  => {e}")
    print("\n  **This is Week 2's problem, unchanged.** A left-recursive rule")
    print("  calls itself before consuming input, so a top-down parser --")
    print("  hand-written or combinator-built -- never terminates. Combinators")
    print("  did not fix it; they inherited it, because they ARE recursive")
    print("  descent with the call graph reified.")

    print("\n; ---- the size of it ----")
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    w2 = os.path.join(here, '..', '..', 'CS211 Week6', 'lab', 'parser.py')
    lines_here = sum(1 for l in open(__file__)
                     if l.strip() and not l.strip().startswith('#'))
    print(f"  this file, non-comment lines            {lines_here}")
    print("  of which the arithmetic grammar itself   4")
    if os.path.exists(w2):
        n = sum(1 for l in open(w2) if l.strip()
                and not l.strip().startswith('#'))
        print(f"  Week 2/6 hand-written parser.py         {n}")
        print("  (a bigger language -- the comparison is of style, not size)")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
