#!/usr/bin/env python3
"""De Bruijn indices: the same calculus with the names taken out.

A bound variable's name carries no information.  `\\x. x` and `\\y. y` are the
same function, and `alpha_eq` in lam.py exists only to say so.  De Bruijn's
observation is that if the name is meaningless, do not store it: store **how
many binders outwards** the variable's own binder is.

    \\x. x                ->  \\. 0
    \\x. \\y. x            ->  \\. \\. 1
    \\x. \\y. y            ->  \\. \\. 0
    \\f. \\x. f (f x)      ->  \\. \\. 1 (1 0)          -- the numeral 2

Two things follow immediately, and they are the reason every serious
implementation does this:

  * **Alpha-equivalence becomes structural equality.**  Two terms are the
    same function exactly when they are the same tree.  `alpha_eq` is
    replaced by `==`.
  * **Capture cannot happen**, because there is no name to capture.  The
    substitution below has no `fresh`, no `free_vars` check, and no rename
    branch -- the whole hazard that L15 section 5 measured is gone, not
    handled.

What replaces it is **shifting**: moving a term under a binder means every
free index in it must be incremented, because it is now one binder further
from home.  That is `shift` below, and it is where de Bruijn bugs live.  The
hazard did not disappear; it changed shape into one a type-checker and a
handful of tests can actually catch.
"""
import sys

from lam import Var, Abs, App, parse, load, show, Stats


class DVar:
    __slots__ = ('idx',)

    def __init__(self, idx):
        self.idx = idx

    def __eq__(self, o):
        return isinstance(o, DVar) and o.idx == self.idx

    def __hash__(self):
        return hash(('v', self.idx))


class DFree:
    """A variable with no binder in this term.  Keeps its name, because there
    is nothing to count to."""

    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def __eq__(self, o):
        return isinstance(o, DFree) and o.name == self.name

    def __hash__(self):
        return hash(('f', self.name))


class DAbs:
    __slots__ = ('body',)

    def __init__(self, body):
        self.body = body

    def __eq__(self, o):
        return isinstance(o, DAbs) and o.body == self.body

    def __hash__(self):
        return hash(('a', self.body))


class DApp:
    __slots__ = ('fn', 'arg')

    def __init__(self, fn, arg):
        self.fn, self.arg = fn, arg

    def __eq__(self, o):
        return isinstance(o, DApp) and o.fn == self.fn and o.arg == self.arg

    def __hash__(self):
        return hash(('p', self.fn, self.arg))


# ------------------------------------------------------------- conversion
def to_db(t, env=None):
    """Named term -> nameless term."""
    env = env or []
    if isinstance(t, Var):
        for i, n in enumerate(reversed(env)):
            if n == t.name:
                return DVar(i)
        return DFree(t.name)
    if isinstance(t, Abs):
        return DAbs(to_db(t.body, env + [t.param]))
    return DApp(to_db(t.fn, env), to_db(t.arg, env))


_NAMES = 'xyzabcdefghijklmnopqrstuvw'


def from_db(t, depth=0):
    """Nameless term -> named term, inventing readable names."""
    if isinstance(t, DFree):
        return Var(t.name)
    if isinstance(t, DVar):
        lvl = depth - t.idx - 1
        return Var(_NAMES[lvl % len(_NAMES)] + ('' if lvl < len(_NAMES)
                                                else str(lvl // len(_NAMES))))
    if isinstance(t, DAbs):
        name = _NAMES[depth % len(_NAMES)] + ('' if depth < len(_NAMES)
                                              else str(depth // len(_NAMES)))
        return Abs(name, from_db(t.body, depth + 1))
    return App(from_db(t.fn, depth), from_db(t.arg, depth))


def show_db(t):
    """Render with indices rather than names."""
    if isinstance(t, DFree):
        return t.name
    if isinstance(t, DVar):
        return str(t.idx)
    if isinstance(t, DAbs):
        return f"(λ. {show_db(t.body)})"
    return f"({show_db(t.fn)} {show_db(t.arg)})"


# ----------------------------------------------------------- substitution
def shift(t, d, cutoff=0, stats=None):
    """Add `d` to every free index in `t`.

    `cutoff` is the number of binders we have descended through inside `t`.
    An index below the cutoff is bound *within* `t` and must not move; an
    index at or above it points outside and must.

    **This is where the difficulty went.** Names made capture possible;
    indices make off-by-one possible. Neither representation makes the
    problem disappear -- but an off-by-one shows up as a variable pointing at
    the wrong binder on the very first test, and capture shows up as a
    program that quietly computes something else.
    """
    if stats:
        stats.substs += 1
    if isinstance(t, DFree):
        return t
    if isinstance(t, DVar):
        return DVar(t.idx + d) if t.idx >= cutoff else t
    if isinstance(t, DAbs):
        return DAbs(shift(t.body, d, cutoff + 1, stats))
    return DApp(shift(t.fn, d, cutoff, stats),
                shift(t.arg, d, cutoff, stats))


def subst_db(t, j, s, stats=None):
    """t[j := s] on nameless terms.

    Compare with `lam.subst`: no `fresh`, no `free_vars`, no rename branch,
    no `naive` switch to get wrong. There is nothing here that could capture.
    """
    if stats:
        stats.substs += 1
    if isinstance(t, DFree):
        return t
    if isinstance(t, DVar):
        return s if t.idx == j else t
    if isinstance(t, DAbs):
        # Going under a binder: j is one further away, and s's free indices
        # must be shifted to match.
        return DAbs(subst_db(t.body, j + 1, shift(s, 1, 0, stats), stats))
    return DApp(subst_db(t.fn, j, s, stats),
                subst_db(t.arg, j, s, stats))


def beta(abs_body, arg, stats=None):
    """(λ. body) arg  ->  body[0 := arg], with the bookkeeping shifts."""
    return shift(subst_db(abs_body, 0, shift(arg, 1, 0, stats), stats),
                 -1, 0, stats)


# -------------------------------------------------------------- reduction
def size_db(t):
    n, stack = 0, [t]
    while stack:
        x = stack.pop()
        n += 1
        if isinstance(x, DAbs):
            stack.append(x.body)
        elif isinstance(x, DApp):
            stack.append(x.fn)
            stack.append(x.arg)
    return n


def _step_normal_db(t, stats):
    if isinstance(t, DApp):
        if isinstance(t.fn, DAbs):
            stats.betas += 1
            return beta(t.fn.body, t.arg, stats), True
        fn, did = _step_normal_db(t.fn, stats)
        if did:
            return DApp(fn, t.arg), True
        arg, did = _step_normal_db(t.arg, stats)
        return (DApp(t.fn, arg), True) if did else (t, False)
    if isinstance(t, DAbs):
        body, did = _step_normal_db(t.body, stats)
        return (DAbs(body), True) if did else (t, False)
    return t, False


def _is_value_db(t):
    return isinstance(t, (DAbs, DFree))


def _step_cbv_db(t, stats):
    if isinstance(t, DApp):
        fn, did = _step_cbv_db(t.fn, stats)
        if did:
            return DApp(fn, t.arg), True
        arg, did = _step_cbv_db(t.arg, stats)
        if did:
            return DApp(t.fn, arg), True
        if isinstance(t.fn, DAbs) and _is_value_db(t.arg):
            stats.betas += 1
            return beta(t.fn.body, t.arg, stats), True
    return t, False


DB_STRATEGIES = {'normal': _step_normal_db, 'cbv': _step_cbv_db}


def reduce_db(t, strategy='normal', limit=200_000, max_size=400_000):
    from lam import Diverged
    step = DB_STRATEGIES[strategy]
    stats = Stats()
    stats.max_size = size_db(t)
    for n in range(1, limit + 1):
        try:
            t, did = step(t, stats)
        except RecursionError:
            raise Diverged(t, n, "term too deep to traverse") from None
        if not did:
            return t, stats
        sz = size_db(t)
        stats.max_size = max(stats.max_size, sz)
        if sz > max_size:
            raise Diverged(t, n, f"term grew to {sz} nodes")
    raise Diverged(t, limit, "step limit")


# -------------------------------------------------------------------- main
def main(argv):
    import church
    env = church.prelude()

    if len(argv) > 1:
        t = to_db(parse(' '.join(argv[1:]), env))
        nf, st = reduce_db(t)
        print(f"  nameless : {show_db(nf)}")
        print(f"  named    : {show(from_db(nf))}")
        print(f"  decodes  : {church.decode(from_db(nf))}")
        print(f"  {st}")
        return 0

    print("; ---- the same term, both ways ----")
    for src in ("\\x. x", "\\x y. x", "\\x y. y", "two", "succ", "add"):
        t = parse(src, env)
        print(f"  {src:<8} named {show(t):<34} nameless {show_db(to_db(t))}")
    print()

    print("; ---- alpha-equivalence is now structural equality ----")
    a, b = to_db(parse("\\x. \\y. x")), to_db(parse("\\a. \\b. a"))
    print(f"  (λx y. x) == (λa b. a) as trees?  {a == b}")
    c = to_db(parse("\\x. \\y. y"))
    print(f"  (λx y. x) == (λa b. b) as trees?  {a == c}")
    print()

    print("; ---- capture: the case that broke the named version ----")
    t = parse("(\\x y. x) y")
    nf, st = reduce_db(to_db(t))
    print(f"  (λx y. x) y  ->  nameless {show_db(nf)}   named {show(from_db(nf))}")
    print("  There was no rename, because there was no name. "
          "Compare `python3 lam.py '(\\x y. x) y' --naive`.")
    print()

    print("; ---- same answers, and what each representation costs ----")
    print("  `visits` counts nodes entered while rewriting: for the named")
    print("  version that is `subst`; for the nameless one it is `subst_db`")
    print("  PLUS the two `shift` traversals every beta-step needs.")
    print()
    print(f"  {'term':<26} {'result':>7} {'betas':>7} {'betas':>7} "
          f"{'named':>10} {'nameless':>10} {'renames':>8}")
    print(f"  {'':<26} {'':>7} {'named':>7} {'db':>7} "
          f"{'visits':>10} {'visits':>10} {'':>8}")
    from lam import reduce as reduce_named, parse as parse_named
    rows = (("mult three four", 'normal'), ("exp two five", 'normal'),
            ("pred five", 'normal'), ("fact three", 'normal'),
            ("factV five", 'cbv'))
    for src, strat in rows:
        nf1, s1 = reduce_named(parse_named(src, env), strat, 500_000,
                               max_size=400_000)
        nf2, s2 = reduce_db(to_db(parse_named(src, env)), strat, 500_000)
        # call-by-value stops at a VALUE, which is not a readable numeral.
        # Normalising afterwards is what a REPL does when it prints.
        if strat == 'cbv':
            nf1, _ = reduce_named(nf1, 'normal', 500_000, max_size=400_000)
            nf2, _ = reduce_db(nf2, 'normal', 500_000)
        r1, r2 = church.decode(nf1), church.decode(from_db(nf2))
        flag = '' if str(r1) == str(r2) else '   MISMATCH'
        print(f"  {src:<26} {str(r1):>7} {s1.betas:>7} {s2.betas:>7} "
              f"{s1.substs:>10} {s2.substs:>10} {s1.renames:>8}{flag}")
    print()
    print("  The beta counts agree exactly -- the two representations perform")
    print("  the same reductions. What differs is the price of one step.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
