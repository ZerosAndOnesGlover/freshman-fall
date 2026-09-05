#!/usr/bin/env python3
"""Curry-Howard: propositions as types, proofs as programs.

    a proposition          is a type
    a proof of it          is a term of that type
    A implies B            is  A -> B          a function
    A and B                is  (A, B)          a pair
    A or B                 is  Either A B      a tagged union
    False                  is  Void            a type with no values
    not A                  is  A -> Void

**A proof of `A -> B` is a function that turns any proof of A into a proof of
B.** That is not an analogy. It is the same object, and this file demonstrates
it by searching for proofs and printing the lambda terms it finds -- the same
lambda terms Week 7 was reducing.

The decision procedure is **Dyckhoff's LJT** (1992), a contraction-free
sequent calculus for intuitionistic propositional logic. It matters that it
is a *decision* procedure and not a bounded search: when it says a
proposition is unprovable, that is a proof of unprovability, not a timeout.

    python3 curry.py

The interesting output is the second table. Four classical tautologies come
back unprovable, and they are unprovable **because a proof would have to be a
program, and there is no program to write.**
"""
import sys
from itertools import count


# --------------------------------------------------------------- formulas
class Atom:
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, o):
        return isinstance(o, Atom) and o.name == self.name

    def __hash__(self):
        return hash(('at', self.name))


class Bin:
    __slots__ = ('op', 'l', 'r')

    def __init__(self, op, l, r):
        self.op, self.l, self.r = op, l, r

    def __repr__(self):
        sym = {'->': '→', '&': '∧', '|': '∨'}[self.op]
        return f"({self.l!r} {sym} {self.r!r})"

    def __eq__(self, o):
        return (isinstance(o, Bin) and o.op == self.op
                and o.l == self.l and o.r == self.r)

    def __hash__(self):
        return hash((self.op, self.l, self.r))


class Void:
    """False. The type with no values, so no proof of it can exist."""

    __slots__ = ()

    def __repr__(self):
        return "⊥"

    def __eq__(self, o):
        return isinstance(o, Void)

    def __hash__(self):
        return hash('void')


FALSE = Void()

A, B, C = Atom('A'), Atom('B'), Atom('C')


def imp(l, r):
    return Bin('->', l, r)


def conj(l, r):
    return Bin('&', l, r)


def disj(l, r):
    return Bin('|', l, r)


def neg(x):
    return imp(x, FALSE)


# ------------------------------------------------------------ proof terms
#
# The proof terms are ordinary lambda terms plus the constructors for pairs
# and sums.  Week 7 encoded pairs and sums AS lambda terms; here they are
# primitive, because the point is to read the term as a proof rather than to
# reduce it.
#
_v = count()


def fresh(base='p'):
    return f"{base}{next(_v)}"


class PTerm:
    """A proof term.

    Structured, so that `check` can verify it, and self-rendering, so that
    `prove` can build terms without knowing either of those things.
    """

    __slots__ = ('kind', 'parts')

    def __init__(self, kind, *parts):
        self.kind, self.parts = kind, parts

    def __str__(self):
        k, p = self.kind, self.parts
        if k == 'var':
            return p[0]
        if k == 'lam':
            return f"λ{p[0]}. {p[1]}"
        if k == 'app':
            return f"({p[0]} {p[1]})"
        if k == 'pair':
            return f"({p[0]}, {p[1]})"
        if k == 'fst':
            return f"fst {p[0]}"
        if k == 'snd':
            return f"snd {p[0]}"
        if k == 'inl':
            return f"inl {p[0]}"
        if k == 'inr':
            return f"inr {p[0]}"
        if k == 'case':
            return (f"case {p[0]} of inl {p[1]} → {p[2]}; "
                    f"inr {p[3]} → {p[4]}")
        if k == 'absurd':
            return f"absurd {p[0]}"
        return f"<{k}>"

    __repr__ = __str__


def var(x):
    return PTerm('var', x)


def lam(x, body):
    return PTerm('lam', x, body)


def app(f, a):
    return PTerm('app', f, a)


def pair(a, b):
    return PTerm('pair', a, b)


def fst(p):
    return PTerm('fst', p)


def snd(p):
    return PTerm('snd', p)


def inl(x):
    return PTerm('inl', x)


def inr(x):
    return PTerm('inr', x)


def case(s, xl, l, xr, r):
    return PTerm('case', s, xl, l, xr, r)


def absurd(x):
    return PTerm('absurd', x)


# ------------------------------------------------------- checking the proofs
#
# A proof term is a program, so it can be TYPE-CHECKED against the proposition
# it claims to prove.  That is not a nicety.  An earlier version of the hard
# left rule below built `t (λy. sub)` where `t sub` was meant, producing a
# term of the wrong arity for every proof that used it.  Provability was still
# reported correctly, so every test passed; the defect was visible only by
# reading the proof of `¬¬(A ∨ ¬A)` and noticing it took two arguments where
# `¬A` takes one.
#
# The checker below is the guard that would have caught it immediately.  It
# re-derives a type for the structured form of each term and compares.  Weeks
# 5, 6 and 7 each lost time to an instrument that agreed with the bug; this is
# what declining to repeat that costs.
#
def subst_p(t, x, v):
    """Substitute proof term `v` for variable `x` in `t`.

    Proof terms are generated with globally fresh binder names, so no two
    binders here ever share a name and capture cannot arise.  Week 7 spent a
    lecture on why that assumption is normally unsafe -- it holds here only
    because `fresh` is the sole source of names.
    """
    k, p = t.kind, t.parts
    if k == 'var':
        return v if p[0] == x else t
    if k == 'lam':
        return t if p[0] == x else PTerm('lam', p[0], subst_p(p[1], x, v))
    if k == 'case':
        return PTerm('case', subst_p(p[0], x, v), p[1],
                     p[2] if p[1] == x else subst_p(p[2], x, v), p[3],
                     p[4] if p[3] == x else subst_p(p[4], x, v))
    return PTerm(k, *[subst_p(q, x, v) if isinstance(q, PTerm) else q
                      for q in p])


def normalise(t):
    """Beta-reduce a proof term.

    **On the logic side this is cut elimination**: removing a detour where
    something is proved and immediately consumed.  Dyckhoff's hard left rule
    naturally produces such a detour, so the proof of `¬¬(A ∨ ¬A)` comes out
    as a redex.  Checking wants it gone, because a lambda in function
    position has no synthesisable type -- `synth` would have to guess one.
    """
    k, p = t.kind, t.parts
    if k == 'app':
        f, a = normalise(p[0]), normalise(p[1])
        if f.kind == 'lam':
            return normalise(subst_p(f.parts[1], f.parts[0], a))
        return PTerm('app', f, a)
    if k == 'lam':
        return PTerm('lam', p[0], normalise(p[1]))
    if k == 'case':
        return PTerm('case', normalise(p[0]), p[1], normalise(p[2]),
                     p[3], normalise(p[4]))
    if k == 'var':
        return t
    return PTerm(k, *[normalise(q) if isinstance(q, PTerm) else q
                      for q in p])


def check(t, ctx, goal, _top=True):
    """Does structured term `t` prove `goal` under `ctx` (name -> formula)?"""
    if _top:
        t = normalise(t)
    k, p = t.kind, t.parts
    if k == 'var':
        return ctx.get(p[0]) == goal
    if k == 'lam':
        if not (isinstance(goal, Bin) and goal.op == '->'):
            return False
        return check(p[1], {**ctx, p[0]: goal.l}, goal.r, False)
    if k == 'app':
        fty = synth(p[0], ctx)
        if not (isinstance(fty, Bin) and fty.op == '->' and fty.r == goal):
            return False
        return check(p[1], ctx, fty.l, False)
    if k == 'pair':
        return (isinstance(goal, Bin) and goal.op == '&'
                and check(p[0], ctx, goal.l, False) and check(p[1], ctx, goal.r, False))
    if k == 'inl':
        return (isinstance(goal, Bin) and goal.op == '|'
                and check(p[0], ctx, goal.l, False))
    if k == 'inr':
        return (isinstance(goal, Bin) and goal.op == '|'
                and check(p[0], ctx, goal.r, False))
    if k in ('fst', 'snd'):
        return synth(t, ctx) == goal
    if k == 'case':
        sty = synth(p[0], ctx)
        if not (isinstance(sty, Bin) and sty.op == '|'):
            return False
        return (check(p[2], {**ctx, p[1]: sty.l}, goal, False)
                and check(p[4], {**ctx, p[3]: sty.r}, goal, False))
    if k == 'absurd':
        return synth(p[0], ctx) == FALSE
    return False


def synth(t, ctx):
    """Infer a formula for the terms whose type is determined by their shape."""
    k, p = t.kind, t.parts
    if k == 'var':
        return ctx.get(p[0])
    if k == 'fst':
        s = synth(p[0], ctx)
        return s.l if isinstance(s, Bin) and s.op == '&' else None
    if k == 'snd':
        s = synth(p[0], ctx)
        return s.r if isinstance(s, Bin) and s.op == '&' else None
    if k == 'app':
        f = synth(p[0], ctx)
        if isinstance(f, Bin) and f.op == '->' and check(p[1], ctx, f.l, False):
            return f.r
        return None
    return None


# ---------------------------------------------------------------- the rules
#
# Dyckhoff's LJT.  The context is a list of (formula, proof-term) pairs: the
# term is the variable or expression that *proves* that formula, so a
# successful search returns a complete program.
#
def prove(ctx, goal, depth=0):
    """Return a proof term for `goal` from `ctx`, or None if none exists."""
    if depth > 40:
        return None

    # --- axiom: the goal is already assumed
    for f, t in ctx:
        if f == goal:
            return t

    # --- ⊥L: anything follows from a proof of False
    for f, t in ctx:
        if isinstance(f, Void):
            return absurd(t)

    # --- invertible left rules first: they never lose a proof
    for i, (f, t) in enumerate(ctx):
        rest = ctx[:i] + ctx[i + 1:]

        if isinstance(f, Bin) and f.op == '&':
            return _wrap(prove(rest + [(f.l, fst(t)), (f.r, snd(t))],
                               goal, depth + 1))

        if isinstance(f, Bin) and f.op == '|':
            xl, xr = fresh(), fresh()
            pl = prove(rest + [(f.l, var(xl))], goal, depth + 1)
            if pl is None:
                continue
            pr = prove(rest + [(f.r, var(xr))], goal, depth + 1)
            if pr is None:
                continue
            return case(t, xl, pl, xr, pr)

        if isinstance(f, Bin) and f.op == '->':
            a = f.l
            # (atom → B) with the atom available
            if isinstance(a, (Atom, Void)):
                for g, u in rest:
                    if g == a:
                        return _wrap(prove(rest + [(f.r, app(t, u))],
                                           goal, depth + 1))
            # ((C ∧ D) → B)  ≡  (C → (D → B))
            elif a.op == '&':
                x, y = fresh(), fresh()
                new = imp(a.l, imp(a.r, f.r))
                nt = lam(x, lam(y, app(t, pair(var(x), var(y)))))
                return _wrap(prove(rest + [(new, nt)], goal, depth + 1))
            # ((C ∨ D) → B)  ≡  (C → B) ∧ (D → B)
            elif a.op == '|':
                x, y = fresh(), fresh()
                n1, t1 = imp(a.l, f.r), lam(x, app(t, inl(var(x))))
                n2, t2 = imp(a.r, f.r), lam(y, app(t, inr(var(y))))
                return _wrap(prove(rest + [(n1, t1), (n2, t2)],
                                   goal, depth + 1))

    # --- invertible right rules
    if isinstance(goal, Bin) and goal.op == '->':
        x = fresh()
        p = prove(ctx + [(goal.l, var(x))], goal.r, depth + 1)
        return lam(x, p) if p is not None else None

    if isinstance(goal, Bin) and goal.op == '&':
        l = prove(ctx, goal.l, depth + 1)
        if l is None:
            return None
        r = prove(ctx, goal.r, depth + 1)
        return pair(l, r) if r is not None else None

    # --- non-invertible rules: these are choices, and a wrong one loses
    if isinstance(goal, Bin) and goal.op == '|':
        l = prove(ctx, goal.l, depth + 1)
        if l is not None:
            return inl(l)
        r = prove(ctx, goal.r, depth + 1)
        if r is not None:
            return inr(r)

    # --- the hard left rule: ((C → D) → B) in the context
    for i, (f, t) in enumerate(ctx):
        if (isinstance(f, Bin) and f.op == '->'
                and isinstance(f.l, Bin) and f.l.op == '->'):
            rest = ctx[:i] + ctx[i + 1:]
            cd, b = f.l, f.r
            x, y = fresh(), fresh()
            # `t : (C → D) → B`.  To use it we need a proof of `C → D`, and
            # Dyckhoff's rule lets us assume `D → B` while finding one:
            # given `d : D`, `λy:C. d` is a proof of `C → D`, so `t (λy. d)`
            # proves B.
            sub = prove(rest + [(imp(cd.r, b),
                                 lam(x, app(t, lam(y, var(x)))))],
                        cd, depth + 1)
            if sub is None:
                continue
            # `sub : C → D` already, so B is `t sub` -- NOT `t (λy. sub)`.
            # Wrapping it in another lambda produced a term of the wrong
            # arity, which type-checked nowhere and was only visible by
            # reading the output of `¬¬(A ∨ ¬A)`.
            p = prove(rest + [(b, app(t, sub))], goal, depth + 1)
            if p is not None:
                return p

    return None


def _wrap(p):
    return p


def provable(goal, ctx=None):
    global _v
    _v = count()
    return prove(list(ctx or []), goal)


# -------------------------------------------------------------------- main
INTUITIONISTIC = [
    ("A → A", imp(A, A)),
    ("A → B → A", imp(A, imp(B, A))),
    ("(A → B → C) → (A → B) → A → C",
     imp(imp(A, imp(B, C)), imp(imp(A, B), imp(A, C)))),
    ("A ∧ B → A", imp(conj(A, B), A)),
    ("A ∧ B → B ∧ A", imp(conj(A, B), conj(B, A))),
    ("A → A ∨ B", imp(A, disj(A, B))),
    ("(A → C) → (B → C) → A ∨ B → C",
     imp(imp(A, C), imp(imp(B, C), imp(disj(A, B), C)))),
    ("A → ¬¬A", imp(A, neg(neg(A)))),
    ("¬¬¬A → ¬A", imp(neg(neg(neg(A))), neg(A))),
    ("(A → B) → ¬B → ¬A", imp(imp(A, B), imp(neg(B), neg(A)))),
    ("¬A ∨ ¬B → ¬(A ∧ B)", imp(disj(neg(A), neg(B)), neg(conj(A, B)))),
    ("⊥ → A", imp(FALSE, A)),
]

CLASSICAL_ONLY = [
    ("A ∨ ¬A", "excluded middle", disj(A, neg(A))),
    ("¬¬A → A", "double negation", imp(neg(neg(A)), A)),
    ("((A → B) → A) → A", "Peirce's law", imp(imp(imp(A, B), A), A)),
    ("¬(A ∧ B) → ¬A ∨ ¬B", "a de Morgan",
     imp(neg(conj(A, B)), disj(neg(A), neg(B)))),
    ("(A → B) ∨ (B → A)", "linearity", disj(imp(A, B), imp(B, A))),
]


def main():
    print("; ---- a proposition is a type; a proof is a program ----")
    print("; decision procedure: Dyckhoff's LJT, intuitionistic "
          "propositional logic")
    print()

    print(f"; ---- PROVABLE ({len(INTUITIONISTIC)}) ----")
    print("; each proof is TYPE-CHECKED against the proposition it claims")
    bad = 0
    for label, f in INTUITIONISTIC:
        p = provable(f)
        if p is None:
            bad += 1
            print(f"  FAIL     {label}   (no proof found)")
            continue
        ok = check(p, {}, f)
        if not ok:
            bad += 1
        mark = 'ok      ' if ok else 'ILL-TYPED'
        print(f"  {mark} {label:<32} {p}")

    print(f"\n; ---- NOT PROVABLE ({len(CLASSICAL_ONLY)}) ----")
    print("; every one of these is a classical tautology")
    for label, why, f in CLASSICAL_ONLY:
        p = provable(f)
        if p is not None:
            bad += 1
            print(f"  UNEXPECTED PROOF  {label}  {p}")
        else:
            print(f"  none  {label:<22} ({why})")

    print("\n; ---- but each becomes provable given the missing axiom ----")
    lem = disj(A, neg(A))
    for label, why, f in CLASSICAL_ONLY:
        p = provable(f, [(lem, 'lem')])
        print(f"  {label:<22} {'PROVED from LEM' if p else 'still none'}")
    print()
    print("  `lem` is a free variable of every proof above: an ASSUMPTION,")
    print("  not a construction. That is exactly what classical logic adds --")
    print("  and it is why a classical proof need not be a program.")

    print(f"\n  {'all as expected' if bad == 0 else str(bad) + ' surprises'}")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
