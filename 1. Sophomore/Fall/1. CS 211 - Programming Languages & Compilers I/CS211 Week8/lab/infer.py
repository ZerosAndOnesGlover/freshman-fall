#!/usr/bin/env python3
"""Hindley-Milner inference, pointed at Week 7's lambda terms.

Week 3 wrote this algorithm (`CS211 Week3/lab/hm.py`) over a toy AST with
integers and `if`, and it inferred types for six hand-written expressions.
The engine below is that engine -- unification, the occurs check, `Scheme`,
`instantiate`, `generalise` -- with one thing changed: **it runs on the terms
from `prelude.lam` instead**.

That is the whole experiment. Week 7 built fifty-five definitions in a
language with no types at all and found that three of them were the same
term. Week 8 asks the obvious follow-up: **what happens when you type them?**

Two answers come out, and only one is the one people expect.

    python3 infer.py                # type the whole prelude
    python3 infer.py 'mult three'   # type one term

**Why this file is not called `types.py`.** Because `types` is a module in
Python's standard library, and a file of that name in this directory would
shadow it for every import in the folder.  Week 6 declined to call its
collector `gc.py` for the same reason and Week 7's `lam.py` carries an
entry-point note about the same class of bug.  Three weeks, three near
misses, one lesson: **a module name is a global name, and the global
namespace already has occupants.**
"""
import sys
from itertools import count

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lam import (Var, Abs, App, Let, parse, load, desugar,
                 show as show_term, alpha_eq, LamError)

_fresh = count()


# ------------------------------------------------------------------- types
class TVar:
    """A type we do not know yet. `ref` is set when unification learns it."""

    __slots__ = ('id', 'ref')

    def __init__(self):
        self.id = next(_fresh)
        self.ref = None

    def __repr__(self):
        return repr(prune(self)) if self.ref else _name(self.id)


def _name(i):
    """t0 -> a, t1 -> b, ... so that printed types read like a textbook."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return letters[i % 26] + ('' if i < 26 else str(i // 26))


class TCon:
    """A type constructor: `Int`, `Bool`, or `->` with two arguments."""

    __slots__ = ('name', 'args')

    def __init__(self, name, args=()):
        self.name, self.args = name, tuple(args)

    def __repr__(self):
        if self.name == '->':
            l, r = self.args
            ls = repr(l)
            if isinstance(prune(l), TCon) and prune(l).name == '->':
                ls = f"({ls})"
            return f"{ls} -> {r!r}"
        if self.args:
            return f"{self.name} {' '.join(map(repr, self.args))}"
        return self.name


INT, BOOL = TCon('Int'), TCon('Bool')


def fn(a, b):
    return TCon('->', (a, b))


def prune(t):
    """Follow the chain of resolved type variables to whatever it ends at."""
    if isinstance(t, TVar) and t.ref is not None:
        t.ref = prune(t.ref)
        return t.ref
    return t


class TypeError_(Exception):
    pass


def occurs(v, t):
    """Does type variable `v` appear inside `t`?

    This is the check that makes `\\x. x x` untypeable, and it is the same
    check that made `T = [T]` unwritable in Week 6's `cyc_array.cy`.  In both
    cases it is refusing to build an infinite type.
    """
    t = prune(t)
    if t is v:
        return True
    if isinstance(t, TCon):
        return any(occurs(v, a) for a in t.args)
    return False


def unify(a, b):
    """Make two types equal, or fail saying why."""
    a, b = prune(a), prune(b)
    if isinstance(a, TVar):
        if a is not b:
            if occurs(a, b):
                raise TypeError_(f"occurs check: cannot construct the "
                                 f"infinite type {a!r} = {b!r}")
            a.ref = b
        return
    if isinstance(b, TVar):
        return unify(b, a)
    if a.name != b.name or len(a.args) != len(b.args):
        raise TypeError_(f"cannot unify {a!r} with {b!r}")
    for x, y in zip(a.args, b.args):
        unify(x, y)


# ------------------------------------------------------------------ schemes
class Scheme:
    """A type with some variables universally quantified: `forall a. a -> a`.

    The quantifier is what makes `let`-bound names polymorphic and
    lambda-bound names monomorphic -- section 6 of L17 is about the
    consequences of that single distinction.
    """

    __slots__ = ('qs', 't')

    def __init__(self, qs, t):
        self.qs, self.t = qs, t

    def __repr__(self):
        if not self.qs:
            return repr(self.t)
        return f"forall {' '.join(_name(q.id) for q in self.qs)}. {self.t!r}"


def type_vars(t, acc=None):
    acc = acc if acc is not None else []
    t = prune(t)
    if isinstance(t, TVar):
        if t not in acc:
            acc.append(t)
    else:
        for a in t.args:
            type_vars(a, acc)
    return acc


def instantiate(s):
    """Replace each quantified variable with a fresh one."""
    m = {q: TVar() for q in s.qs}

    def go(t):
        t = prune(t)
        if isinstance(t, TVar):
            return m.get(t, t)
        return TCon(t.name, tuple(go(a) for a in t.args))

    return go(s.t)


def generalise(env, t):
    """Quantify every variable free in `t` but not free in the environment."""
    env_vars = []
    for s in env.values():
        for v in type_vars(s.t):
            if v not in s.qs:
                env_vars.append(v)
    qs = [v for v in type_vars(t) if v not in env_vars]
    return Scheme(qs, t)


# ---------------------------------------------------------------- inference
def infer(e, env):
    """Algorithm W over `lam.py`'s three constructs. That is all it needs."""
    if isinstance(e, Var):
        if e.name not in env:
            raise TypeError_(f"unbound variable '{e.name}'")
        return instantiate(env[e.name])
    if isinstance(e, Abs):
        tv = TVar()
        # A lambda-bound name is MONOMORPHIC: it goes in with no quantifier.
        return fn(tv, infer(e.body, {**env, e.param: Scheme([], tv)}))
    if isinstance(e, App):
        tf = infer(e.fn, env)
        ta = infer(e.arg, env)
        tr = TVar()
        unify(tf, fn(ta, tr))
        return tr
    if isinstance(e, Let):
        # THE line that distinguishes Hindley-Milner from the simply-typed
        # calculus.  Infer the value's type, then GENERALISE it -- quantify
        # every variable the environment does not constrain -- so that each
        # use in the body may instantiate it differently.
        #
        # `desugar` turns this same term into `(\x. body) val`, whose Abs
        # case above puts `x` in with `Scheme([], tv)`: no quantifier, one
        # type, every use forced to agree.  Same behaviour, different
        # typeability.  L17 section 6.
        tv = infer(e.val, env)
        return infer(e.body, {**env, e.name: generalise(env, tv)})
    raise TypeError_(f"unknown term {e!r}")


def principal(term, env=None):
    """The most general type of `term`, or raise."""
    global _fresh
    return generalise({}, infer(term, env or {}))


# ------------------------------------------------------------------- report
def type_of(name, term, env):
    try:
        return repr(principal(term, env)), None
    except (TypeError_, RecursionError) as ex:
        return None, str(ex).split('\n')[0][:60]


def main(argv):
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    defs = load(os.path.join(here, 'prelude.lam'))

    if len(argv) > 1:
        global _fresh
        _fresh = count()
        t = parse(' '.join(argv[1:]), defs)
        ok, err = type_of('', t, {})
        print(f"  term : {show_term(t)[:100]}")
        print(f"  type : {ok if ok else 'TYPE ERROR -- ' + err}")
        return 0 if ok else 1

    print(f"; ---- Hindley-Milner over prelude.lam "
          f"({len(defs)} definitions) ----")
    print("; the engine is Week 3's, unchanged; only the input is new")
    print()

    typed, untyped = [], []
    for name in defs:
        _fresh = count()
        ok, err = type_of(name, defs[name], {})
        (typed if ok else untyped).append((name, ok or err))

    print(f"; ---- {len(typed)} typeable ----")
    for name, t in typed:
        print(f"  {name:<10} : {t}")

    print(f"\n; ---- {len(untyped)} REJECTED ----")
    for name, err in untyped:
        print(f"  {name:<10} : {err}")

    print(f"\n; ---- the Week 7 collision, retyped ----")
    for name in ('zero', 'false', 'nil'):
        _fresh = count()
        ok, _ = type_of(name, defs[name], {})
        print(f"  {name:<10} : {ok}")
    same = alpha_eq(defs['zero'], defs['false'])
    print(f"  still the same term: {same}")
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except LamError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
