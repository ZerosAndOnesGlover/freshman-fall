#!/usr/bin/env python3
"""The untyped lambda calculus: terms, substitution, and reduction.

Three constructs.  That is the entire language:

    x           a variable
    \\x. e       an abstraction -- the function of x whose body is e
    e1 e2       an application -- e1 applied to e2

No numbers, no booleans, no conditionals, no data structures, no recursion,
no assignment, no heap.  Week 6 spent two lectures on what to do about
memory; this language has none, and is Turing-complete anyway.

**Everything hard in this file is in one function**, and it is not the
reducer.  It is `subst`: replacing a variable by a term without changing
which binder any other variable refers to.  Get it wrong and you do not get
an error, you get a different program -- L15 section 5 measures exactly what
that costs, using the `naive=True` switch below.

Conventions, and they are the standard ones:

  * Application associates **left**:  `f a b`  is  `(f a) b`.
  * Abstraction bodies extend as far **right** as possible: `\\x. f x` is
    `\\x. (f x)`, never `(\\x. f) x`.
  * `\\x y. e` abbreviates `\\x. \\y. e`.

Both `\\` and the character lambda are accepted on input.  Output uses
lambda, because this is 2025 and the terminal can take it.
"""
import sys
from itertools import count


class LamError(Exception):
    pass


# ------------------------------------------------------------------- terms
class Term:
    __slots__ = ()


class Var(Term):
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name


class Abs(Term):
    __slots__ = ('param', 'body')

    def __init__(self, param, body):
        self.param, self.body = param, body


class App(Term):
    __slots__ = ('fn', 'arg')

    def __init__(self, fn, arg):
        self.fn, self.arg = fn, arg


# --------------------------------------------------------------- printing
def show(t, top=True):
    """Render a term with the minimum number of parentheses.

    Minimum matters more than you would think.  A printer that parenthesises
    everything is correct and unreadable, and a reduction trace you cannot
    read is a reduction trace you will not check -- which is how Week 5's
    `store` bug survived a week.
    """
    if isinstance(t, Var):
        return t.name
    if isinstance(t, Abs):
        params = [t.param]
        b = t.body
        while isinstance(b, Abs):
            params.append(b.param)
            b = b.body
        s = f"λ{' '.join(params)}. {show(b)}"
        return s if top else f"({s})"
    # App
    fn = show(t.fn, top=False) if not isinstance(t.fn, Abs) else f"({show(t.fn)})"
    if isinstance(t.fn, App):
        fn = show(t.fn, top=False)
    arg = show(t.arg, top=False)
    if isinstance(t.arg, App) or isinstance(t.arg, Abs):
        arg = f"({show(t.arg)})"
    s = f"{fn} {arg}"
    return s if top else s


def size(t):
    """Nodes in the term.

    Iterative, not recursive, and that is not a style preference.  A term
    under applicative-order `Y` grows without bound in *depth*, so a
    recursive walk over it dies of stack exhaustion long before the step
    limit is reached -- reporting a `RecursionError` from the measuring
    instrument instead of the divergence being measured.
    """
    n, stack = 0, [t]
    while stack:
        x = stack.pop()
        n += 1
        if isinstance(x, Abs):
            stack.append(x.body)
        elif isinstance(x, App):
            stack.append(x.fn)
            stack.append(x.arg)
    return n


# ------------------------------------------------------------------ parsing
def tokenize(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c == '#':                      # comment to end of line
            while i < len(s) and s[i] != '\n':
                i += 1
        elif c in '()':
            out.append(c); i += 1
        elif c in '\\λ':
            out.append('\\'); i += 1
        elif c == '.':
            out.append('.'); i += 1
        elif c == '=':
            out.append('='); i += 1
        elif c.isalnum() or c in "_'?":
            j = i
            while j < len(s) and (s[j].isalnum() or s[j] in "_'?"):
                j += 1
            out.append(s[i:j]); i = j
        else:
            raise LamError(f"unexpected character {c!r}")
    return out


class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def eat(self, what=None):
        got = self.peek()
        if got is None:
            raise LamError("unexpected end of input")
        if what is not None and got != what:
            raise LamError(f"expected {what!r}, found {got!r}")
        self.i += 1
        return got

    def term(self):
        """term := '\\' var+ '.' term | application"""
        if self.peek() == '\\':
            self.eat('\\')
            params = []
            while self.peek() not in ('.', None):
                params.append(self.eat())
            self.eat('.')
            body = self.term()
            # `\x y. e` is sugar for `\x. \y. e` -- currying, and the reason
            # every function in this language takes exactly one argument.
            for p in reversed(params):
                body = Abs(p, body)
            return body
        return self.application()

    def application(self):
        parts = [self.atom()]
        while self.peek() is not None and self.peek() not in (')', '.'):
            if self.peek() == '\\':
                parts.append(self.term())       # body extends rightwards
                break
            parts.append(self.atom())
        t = parts[0]
        for p in parts[1:]:
            t = App(t, p)                       # application is LEFT assoc
        return t

    def atom(self):
        c = self.peek()
        if c == '(':
            self.eat('(')
            t = self.term()
            self.eat(')')
            return t
        if c == '\\':
            return self.term()
        if c is None or c in ('.', ')'):
            raise LamError(f"expected a term, found {c!r}")
        return Var(self.eat())


def parse(src, env=None):
    """Parse a term.  `env` maps names to previously-defined terms, which is
    the only thing in this file that is not the pure lambda calculus -- and
    it is only an abbreviation, expanded before reduction begins."""
    p = Parser(tokenize(src))
    t = p.term()
    if p.peek() is not None:
        raise LamError(f"trailing input at {p.peek()!r}")
    return expand(t, env or {})


def expand(t, env, seen=()):
    """Replace free variables that name definitions by their definitions."""
    if isinstance(t, Var):
        if t.name in env and t.name not in seen:
            return expand(env[t.name], env, seen + (t.name,))
        return t
    if isinstance(t, Abs):
        # A binder shadows a definition of the same name.  This is Week 3's
        # scope rule, and it has to hold here for the same reason.
        inner = {k: v for k, v in env.items() if k != t.param}
        return Abs(t.param, expand(t.body, inner, seen))
    return App(expand(t.fn, env, seen), expand(t.arg, env, seen))


def load(path):
    """Read a file of `name = term` definitions, in order.  Later definitions
    may use earlier ones."""
    env = {}
    src = open(path).read()
    for lineno, line in enumerate(src.split('\n'), 1):
        line = line.split('#')[0].strip()
        if not line:
            continue
        if '=' not in line:
            raise LamError(f"{path}:{lineno}: expected `name = term`")
        name, rhs = line.split('=', 1)
        name = name.strip()
        try:
            env[name] = parse(rhs, env)
        except LamError as e:
            raise LamError(f"{path}:{lineno}: {e}") from None
    return env


# --------------------------------------------------------------- variables
def free_vars(t):
    """Iterative, for the reason given on `size`."""
    out, stack = set(), [(t, frozenset())]
    while stack:
        x, bound = stack.pop()
        if isinstance(x, Var):
            if x.name not in bound:
                out.add(x.name)
        elif isinstance(x, Abs):
            stack.append((x.body, bound | {x.param}))
        else:
            stack.append((x.fn, bound))
            stack.append((x.arg, bound))
    return out


_fresh = count()


def fresh(base, avoid):
    """A name like `base` that is not in `avoid`."""
    n = base.rstrip("'0123456789") or 'x'
    while True:
        cand = f"{n}{next(_fresh)}"
        if cand not in avoid:
            return cand


# ---------------------------------------------------------- substitution
#
# THE function.  Everything else in this file is bookkeeping.
#
class Stats:
    """Counters, so that claims about cost are measured rather than asserted."""

    def __init__(self):
        self.betas = 0          # beta-reductions performed
        self.substs = 0         # substitutions entered
        self.renames = 0        # alpha-renamings forced by capture avoidance
        self.max_size = 0       # largest term seen

    def __repr__(self):
        return (f"betas={self.betas} substs={self.substs} "
                f"renames={self.renames} max_size={self.max_size}")


def subst(t, x, s, stats=None, naive=False):
    """t[x := s] -- replace free occurrences of `x` in `t` by `s`.

    The whole difficulty is the `Abs` case.  Substituting into the body of a
    binder can move `s` underneath that binder, and if `s` has a free
    variable with the same name as the binder's parameter, that variable is
    silently **captured**: it stops referring to whatever it referred to
    outside and starts referring to the parameter.

    The term is still well-formed.  It is a different function.

        (\\x y. x) y     should give   \\y'. y      -- a constant function
        naive result                   \\y. y       -- the identity

    Nothing raises.  You get the wrong answer, and the wrong answer is a
    perfectly reasonable term.  `naive=True` disables the renaming so L15
    section 5 can measure it.
    """
    if stats:
        stats.substs += 1
    if isinstance(t, Var):
        return s if t.name == x else t
    if isinstance(t, App):
        return App(subst(t.fn, x, s, stats, naive),
                   subst(t.arg, x, s, stats, naive))
    # Abs
    if t.param == x:
        # `x` is rebound here, so no free `x` remains below.  Stop.
        return t
    if naive:
        return Abs(t.param, subst(t.body, x, s, stats, naive))
    fs = free_vars(s)
    if t.param in fs:
        # Capture would occur.  Rename the binder first.
        if stats:
            stats.renames += 1
        new = fresh(t.param, fs | free_vars(t.body) | {x})
        body = subst(t.body, t.param, Var(new), stats, naive)
        return Abs(new, subst(body, x, s, stats, naive))
    return Abs(t.param, subst(t.body, x, s, stats, naive))


def alpha_eq(a, b, ma=None, mb=None):
    """Equality up to the names of bound variables.

    Needed because `\\x. x` and `\\y. y` are the same function, and any test
    that compares printed forms would call them different.
    """
    ma, mb = ma or {}, mb or {}
    if isinstance(a, Var) and isinstance(b, Var):
        return ma.get(a.name, a.name) == mb.get(b.name, b.name)
    if isinstance(a, Abs) and isinstance(b, Abs):
        k = f"#{len(ma)}"
        return alpha_eq(a.body, b.body, {**ma, a.param: k}, {**mb, b.param: k})
    if isinstance(a, App) and isinstance(b, App):
        return alpha_eq(a.fn, b.fn, ma, mb) and alpha_eq(a.arg, b.arg, ma, mb)
    return False


# ----------------------------------------------------------------- reduction
class Diverged(Exception):
    """The step limit was reached.

    Not "the term has no normal form" -- that question is **undecidable**,
    which is exactly the halting problem wearing different notation.  This
    exception means we stopped looking, and nothing more.
    """

    def __init__(self, term, steps, why="step limit"):
        super().__init__(f"no normal form after {steps} steps ({why})")
        self.term, self.steps, self.why = term, steps, why


def _step_normal(t, stats, naive):
    """One beta-step, **leftmost-outermost**: reduce the outermost redex,
    without evaluating arguments first.

    Also called *normal order*, because of a theorem: if a term has a normal
    form, this strategy finds it.  No other strategy can do better, and
    several do worse -- section 7 of L16 has the one that does worse.
    """
    if isinstance(t, App):
        if isinstance(t.fn, Abs):
            stats.betas += 1
            return subst(t.fn.body, t.fn.param, t.arg, stats, naive), True
        fn, did = _step_normal(t.fn, stats, naive)
        if did:
            return App(fn, t.arg), True
        arg, did = _step_normal(t.arg, stats, naive)
        return (App(t.fn, arg), True) if did else (t, False)
    if isinstance(t, Abs):
        body, did = _step_normal(t.body, stats, naive)
        return (Abs(t.param, body), True) if did else (t, False)
    return t, False


def _step_applicative(t, stats, naive):
    """One beta-step, **leftmost-innermost**: reduce the argument to a value
    before applying the function.

    This is call-by-value, and it is what C, Java, Python, Rust, Go and every
    other mainstream language does -- so its failure mode is not a curiosity.
    It is why `if` cannot be an ordinary function in any of them.
    """
    if isinstance(t, App):
        fn, did = _step_applicative(t.fn, stats, naive)
        if did:
            return App(fn, t.arg), True
        arg, did = _step_applicative(t.arg, stats, naive)
        if did:
            return App(t.fn, arg), True
        if isinstance(t.fn, Abs):
            stats.betas += 1
            return subst(t.fn.body, t.fn.param, t.arg, stats, naive), True
        return t, False
    if isinstance(t, Abs):
        body, did = _step_applicative(t.body, stats, naive)
        return (Abs(t.param, body), True) if did else (t, False)
    return t, False


def is_value(t):
    """Under call-by-value, an abstraction is a **value**: you do not look
    inside it, because a function body has not "happened" until the function
    is called.  A free variable is stuck and counts as one too.

    This one line is the whole difference between `Y` working and `Y`
    hanging, and it is why `Z` is written the way it is -- L16 section 7.
    """
    return isinstance(t, (Abs, Var))


def _step_cbv(t, stats, naive):
    """Call-by-value: arguments first, and **never under a lambda**.

    This is what C, Java, Python, Rust, Go, OCaml and Swift do.  Compare it
    with `_step_applicative`, which is the same order of work but *does*
    reduce under lambdas -- a difference that looks like bookkeeping and
    decides whether a fixed-point combinator terminates.
    """
    if isinstance(t, App):
        fn, did = _step_cbv(t.fn, stats, naive)
        if did:
            return App(fn, t.arg), True
        arg, did = _step_cbv(t.arg, stats, naive)
        if did:
            return App(t.fn, arg), True
        if isinstance(t.fn, Abs) and is_value(t.arg):
            stats.betas += 1
            return subst(t.fn.body, t.fn.param, t.arg, stats, naive), True
    return t, False


def _step_cbn(t, stats, naive):
    """Call-by-name: outermost first, and never under a lambda.

    Normal order without the final tidy-up.  Haskell is this plus sharing,
    which turns it into call-by-need; the sharing is a performance property,
    not a semantic one.
    """
    if isinstance(t, App):
        if isinstance(t.fn, Abs):
            stats.betas += 1
            return subst(t.fn.body, t.fn.param, t.arg, stats, naive), True
        fn, did = _step_cbn(t.fn, stats, naive)
        if did:
            return App(fn, t.arg), True
    return t, False


STRATEGIES = {
    # reduce everywhere, including under lambdas -> a full normal form
    'normal': _step_normal,
    'applicative': _step_applicative,
    # stop at a value -> what a real language does
    'cbv': _step_cbv,
    'cbn': _step_cbn,
}


def reduce(t, strategy='normal', limit=10_000, trace=False, naive=False,
           stats=None, max_size=100_000):
    """Reduce to normal form, or raise Diverged.

    Two ways to give up, and they mean different things:

      * **step limit** -- we performed `limit` reductions and the term was
        still not in normal form.
      * **size limit** -- the term grew past `max_size` nodes.  This is the
        interesting one: it says the reduction is not merely long but
        *expanding*, which is what applicative-order `Y` does and what makes
        it diverge rather than merely take a while.

    Neither says the term has no normal form.  **That question is
    undecidable** -- it is the halting problem in different notation -- so an
    interpreter can report only that it stopped looking.
    """
    step = STRATEGIES[strategy]
    stats = stats if stats is not None else Stats()
    stats.max_size = max(stats.max_size, size(t))
    if trace:
        print(f"  {0:>4}  {show(t)}")
    for n in range(1, limit + 1):
        try:
            t, did = step(t, stats, naive)
        except RecursionError:
            raise Diverged(t, n, "term too deep to traverse") from None
        if not did:
            return t, stats
        sz = size(t)
        stats.max_size = max(stats.max_size, sz)
        if sz > max_size:
            raise Diverged(t, n, f"term grew to {sz} nodes")
        if trace:
            print(f"  {n:>4}  {show(t)}")
    raise Diverged(t, limit, "step limit")


def eta_reduce(t):
    """`\\x. f x`  ->  `f`, when x is not free in f.

    Both terms give the same answer for every argument, so they are the same
    function -- extensionally.  A compiler does this transformation under the
    name **eta-reduction**, and it is the reason a wrapper that only forwards
    its argument costs nothing.
    """
    if isinstance(t, Var):
        return t
    if isinstance(t, App):
        return App(eta_reduce(t.fn), eta_reduce(t.arg))
    body = eta_reduce(t.body)
    if (isinstance(body, App) and isinstance(body.arg, Var)
            and body.arg.name == t.param
            and t.param not in free_vars(body.fn)):
        return body.fn
    return Abs(t.param, body)


# -------------------------------------------------------------------- main
def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="reduce a lambda term")
    ap.add_argument('term', nargs='?', help="the term; reads stdin if absent")
    ap.add_argument('--defs', action='append', default=[],
                    help="a file of `name = term` definitions")
    ap.add_argument('--strategy', default='normal',
                    choices=sorted(STRATEGIES))
    ap.add_argument('--limit', type=int, default=10_000)
    ap.add_argument("--max-size", type=int, default=100_000,
                    dest='max_size',
                    help="give up if the term grows past this many nodes")
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--naive', action='store_true',
                    help="substitute WITHOUT capture avoidance (L15 s5)")
    ap.add_argument('--eta', action='store_true',
                    help="eta-reduce the result")
    ap.add_argument('--church', action='store_true',
                    help="also report the result as a number/bool if it is one")
    a = ap.parse_args(argv[1:])

    env = {}
    for f in a.defs:
        env.update(load(f))
    src = a.term if a.term else sys.stdin.read()

    try:
        t = parse(src, env)
    except LamError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if a.trace:
        print(f"; ---- {a.strategy} order"
              f"{', NAIVE substitution' if a.naive else ''} ----")
    try:
        nf, st = reduce(t, a.strategy, a.limit, a.trace, a.naive,
                        max_size=a.max_size)
    except Diverged as d:
        print(f"; ---- DIVERGED after {d.steps} steps: {d.why} ----")
        n = size(d.term)
        if d.why.startswith("term grew"):
            print(f"  the term is EXPANDING: {n} nodes and still growing")
        else:
            print(f"  the term is still reducible; it has {n} nodes")
        print("  NOTE: this does not prove there is no normal form. "
              "That question is undecidable.")
        return 2
    if a.eta:
        nf = eta_reduce(nf)

    lazy = a.strategy in ('cbv', 'cbn')
    kind = "value" if lazy else "normal form"
    print(f"; ---- {kind} in {st.betas} beta-reductions ----")
    print(f"  {show(nf)}")
    print(f"  {st}")

    if a.church:
        import church
        v = church.decode(nf)
        if v is None and lazy:
            # Call-by-value stops at a VALUE -- an abstraction whose body is
            # not reduced.  That is correct and it is what a real language
            # returns; a numeral only becomes readable when something forces
            # the body, which is what printing does.
            try:
                nf2, st2 = reduce(nf, 'normal', a.limit, max_size=a.max_size)
            except Diverged:
                nf2, st2 = None, None
            if nf2 is not None:
                v = church.decode(nf2)
                print(f"  the value is not yet a numeral; normalising it "
                      f"took a further {st2.betas} beta-reductions")
                print(f"  {show(nf2)}")
        if v is not None:
            print(f"  decodes to: {v}")
    return 0


if __name__ == '__main__':
    # Two lines of entry-point hygiene, both learned the hard way.
    #
    # `sys.setrecursionlimit`: `subst` recurses over the term, and a diverging
    # term grows deeper than CPython's default 1000 frames long before it
    # reaches the size limit.  Without this, a term that is EXPANDING is
    # reported as "too deep to traverse" -- an artefact of the measuring
    # instrument rather than a fact about the term.
    sys.setrecursionlimit(20_000)
    #
    # `import lam`: running this file as a script makes it the module
    # `__main__`, and `church.py` does `from lam import ...`, which loads a
    # SECOND copy under the name `lam`.  The two copies have different `Abs`
    # classes, so every `isinstance` in church.py fails and `--church`
    # silently decodes nothing.  This is exactly the bug that cost Week 6 its
    # reference counter -- see `heap.py`'s docstring -- and delegating to the
    # canonical module object is the one-line form of the same fix.
    import lam
    try:
        sys.exit(lam.main(sys.argv))
    except lam.LamError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
