#!/usr/bin/env python3
"""Church encodings, and the machinery to check them.

The lambda calculus has variables, abstraction and application.  It does not
have numbers, booleans, pairs, lists or conditionals.  This module shows that
it does not *need* them: each of those is a lambda term that behaves the way
the thing it encodes behaves, and "behaves the way it behaves" turns out to
be the only sense in which any of them ever existed.

The trick throughout is the same one, and it is worth naming once:

    **A datum is encoded as the function that uses it.**

A Church numeral `n` is not a quantity; it is *the operation of doing
something n times*.  A boolean is not a bit; it is *the choice between two
alternatives*.  A pair is not a box with two slots; it is *a function waiting
to be told what to do with two things*.  Once you see this, every encoding
below writes itself, and so does the reason `if` is not a function in C.

`decode` runs the encoding backwards so that tests can say `== 120` instead
of comparing forty-node terms by eye.
"""
import sys

from lam import (Var, Abs, App, parse, load, reduce, show, alpha_eq,
                 Diverged, Stats, free_vars)


# The definitions themselves live in `prelude.lam`, so that the lab can read
# them as lambda calculus rather than as Python that builds lambda calculus.
import os
PRELUDE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'prelude.lam')


def prelude():
    return load(PRELUDE)


# ---------------------------------------------------------------- decoding
def church_int(t):
    """If `t` is a Church numeral, return the int; otherwise None.

    A numeral is `λf x. f (f (... (f x)))` with n applications, so we count
    the nesting and check that nothing else is going on.
    """
    if not isinstance(t, Abs) or not isinstance(t.body, Abs):
        return None
    f, x, body = t.param, t.body.param, t.body.body
    n = 0
    while isinstance(body, App):
        if not (isinstance(body.fn, Var) and body.fn.name == f):
            return None
        n += 1
        body = body.arg
    if isinstance(body, Var) and body.name == x:
        return n
    return None


def church_bool(t):
    """`λt f. t` is true, `λt f. f` is false."""
    if not isinstance(t, Abs) or not isinstance(t.body, Abs):
        return None
    a, b, body = t.param, t.body.param, t.body.body
    if isinstance(body, Var):
        if body.name == a:
            return True
        if body.name == b:
            return False
    return None


class Ambiguous:
    """One term, more than one reading, and no way to tell them apart.

    `λf x. x` is the Church numeral **zero** -- apply f to x no times.  It is
    also the boolean **false** -- of two alternatives, take the second.  It is
    also the empty list **nil** -- of "what to do with a head and tail" and
    "what to do with nothing", take the second.

    Those are not three similar terms.  `alpha_eq` says they are the *same
    term*, and no function of that term can distinguish which one was meant,
    because there is nothing there to distinguish.  That is what "untyped"
    means, said concretely, and L16 section 3 is about what it costs.
    """

    __slots__ = ('readings',)

    def __init__(self, **readings):
        self.readings = readings

    def __repr__(self):
        return ' or '.join(f"{v!r} ({k})" for k, v in self.readings.items())

    def __eq__(self, o):
        # Deliberately does NOT compare equal to any of its own readings.
        # An earlier version of this file returned a plain 0 here, every
        # boolean test in the self-test below "passed", and the reason was
        # that Python thinks `0 == False`.  A harness whose notion of
        # equality is looser than the property under test cannot detect a
        # violation of it.
        return isinstance(o, Ambiguous) and o.readings == self.readings

    def __hash__(self):
        return hash(tuple(sorted(self.readings.items())))


ZERO_OR_FALSE = Ambiguous(numeral=0, boolean=False)


def decode(t):
    """An int, a bool, an `Ambiguous`, or None.

    Exactly one collision exists among the encodings in `prelude.lam`, and it
    is between the three values you reach for most often.  Everything else is
    unambiguous:

      * `λt f. t` is `true` and is not a numeral -- its body is a bare
        variable that is not the second parameter, so the numeral pattern
        fails.
      * `λf x. f x` is `1` and is not a boolean -- its body is an
        application, and a boolean's body is a bare variable.
      * `λf x. x` is `0` **and** `false` **and** `nil`.
    """
    n = church_int(t)
    b = church_bool(t)
    if n is not None and b is not None:
        return Ambiguous(numeral=n, boolean=b)
    if n is not None:
        return n
    return b


def decode_list(t, env=None, limit=100_000):
    """Decode a Church-encoded list into a Python list of ints, or None.

    A list *is* its own fold, so its normal form is `λc n. c e1 (c e2 (... n))`
    and the elements can be read straight off that spine.
    """
    nf, _ = reduce(t, limit=limit)
    if isinstance(nf, Abs) and isinstance(nf.body, Abs):
        c, n = nf.param, nf.body.param
        body, out = nf.body.body, []
        while True:
            if isinstance(body, Var) and body.name == n:
                return out
            if not (isinstance(body, App) and isinstance(body.fn, App)
                    and isinstance(body.fn.fn, Var) and body.fn.fn.name == c):
                return None
            elem = decode(body.fn.arg)
            out.append(elem)
            body = body.arg
    return None


# ------------------------------------------------------------------ helpers
def num(n):
    """Build the Church numeral for n directly, without parsing."""
    body = Var('x')
    for _ in range(n):
        body = App(Var('f'), body)
    return Abs('f', Abs('x', body))


def run(src, env=None, strategy='normal', limit=100_000):
    """Parse, reduce, and return (normal form, stats)."""
    return reduce(parse(src, env or prelude()), strategy, limit)


def check(src, want, env=None, strategy='normal', limit=100_000):
    """Reduce `src` and compare the decoded result against `want`."""
    env = env or prelude()
    nf, st = run(src, env, strategy, limit)
    got = decode(nf)
    # `type(...) is type(...)` and not `==`.  See Ambiguous.__eq__ for why
    # this matters: bool is a subclass of int in Python, so `0 == False` is
    # True and a looser check would silently pass the very tests that are
    # supposed to expose the collision.
    ok = type(got) is type(want) and got == want
    return ok, got, st


# --------------------------------------------------------------------- main
def main(argv):
    env = prelude()
    if len(argv) > 1:
        nf, st = run(' '.join(argv[1:]), env)
        print(f"  {show(nf)}")
        print(f"  decodes to: {decode(nf)}")
        print(f"  {st}")
        return 0

    print(f"; ---- prelude.lam defines {len(env)} names ----")
    print('  ' + ', '.join(sorted(env)))
    print()
    print("; ---- three names, one term ----")
    same = all(alpha_eq(env['zero'], env[n]) for n in ('false', 'nil'))
    print(f"  zero = {show(env['zero'])}    false = {show(env['false'])}"
          f"    nil = {show(env['nil'])}")
    print(f"  alpha-equivalent: {same}")
    print("  So a result of `λf x. x` is 0 AND false AND the empty list, and")
    print("  the tests below expect exactly that rather than pretending"
          " otherwise.")
    print()

    print("; ---- self-test ----")
    Z0 = ZERO_OR_FALSE
    tests = [
        # unambiguous numerals
        ("one", 1), ("three", 3),
        ("succ three", 4),
        ("add two three", 5),
        ("mult three four", 12),
        ("exp two five", 32),
        ("pred three", 2),
        ("sub five two", 3),
        ("if true one zero", 1),
        ("fst (pair one two)", 1),
        ("snd (pair one two)", 2),
        # unambiguous booleans
        ("true", True),
        ("or true false", True),
        ("iszero zero", True),
        ("leq two three", True),
        ("eq three three", True),
        # the collision -- these are 0 and false at the same time
        ("zero", Z0), ("false", Z0), ("nil", Z0),
        ("and true false", Z0),
        ("not true", Z0),
        ("if false one zero", Z0),
        ("iszero three", Z0),
        ("leq three two", Z0),
    ]
    bad = 0
    for src, want in tests:
        ok, got, st = check(src, want, env)
        if not ok:
            bad += 1
        print(f"  {'ok ' if ok else 'FAIL'}  {src:<24} = {got!s:<28} "
              f"({st.betas} betas)")
    print(f"\n  {len(tests) - bad}/{len(tests)} passed")

    print()
    print("; ---- lists ----")
    for src, want in [("nil", []),
                      ("cons one (cons two (cons three nil))", [1, 2, 3])]:
        got = decode_list(parse(src, env))
        mark = 'ok ' if got == want else 'FAIL'
        if got != want:
            bad += 1
        print(f"  {mark}  {src:<38} -> {got}")
    for src, want in [("sum (cons one (cons two (cons three nil)))", 6),
                      ("length (cons one (cons two nil))", 2)]:
        ok, got, st = check(src, want, env)
        if not ok:
            bad += 1
        print(f"  {'ok ' if ok else 'FAIL'}  {src:<38} -> {got} "
              f"({st.betas} betas)")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
