#!/usr/bin/env python3
"""The same three results, in a language you already use.

Everything L16 says about evaluation order is a statement about Python, and
this file is the proof.  Python is call-by-value: it evaluates every argument
before entering the function, it does not look inside a `lambda` until the
lambda is called, and `if` is a keyword rather than a function.

    python3 strict.py

Nothing here imports lam.py.  That is the point -- these are not properties
of our interpreter.
"""
import sys


def rule(title):
    print(f"\n; ---- {title} ----")


# ---------------------------------------------------------------------- 1
def const(x, y):
    """`\\x y. x` -- return the first argument, ignore the second."""
    return x


def bottom():
    """A term with no normal form, in Python. `omega` from prelude.lam."""
    return bottom()


def demo_strictness():
    rule("1. call-by-value evaluates arguments it does not need")

    print("  const(1, 2)                    =", const(1, 2))

    print("  const(1, bottom())             = ", end="", flush=True)
    try:
        print(const(1, bottom()))
    except RecursionError:
        print("RecursionError")
    print("    The function never uses its second argument. Python "
          "evaluated it anyway.")

    print("  1 if True else bottom()        = ", end="", flush=True)
    print(1 if True else bottom())
    print("    `if` is a KEYWORD. It is the one construct here that does not "
          "evaluate\n    the branch it does not take -- which is exactly what "
          "`const` could not do.")

    print("  const(1, lambda: bottom())()   -> not called, so:", end=" ")
    print(const(1, lambda: bottom()))
    print("    Wrapping the argument in a lambda hides it from the evaluator.")
    print("    That is a THUNK, and it is what `lazyif` does in prelude.lam.")


# ---------------------------------------------------------------------- 2
def demo_shortcircuit():
    rule("2. `and` and `or` are not functions either")

    def and_fn(p, q):
        return p and q

    print("  False and bottom()             = ", end="", flush=True)
    print(False and bottom())
    print("    The operator short-circuits: `bottom()` is never evaluated.")

    print("  and_fn(False, bottom())        = ", end="", flush=True)
    try:
        print(and_fn(False, bottom()))
    except RecursionError:
        print("RecursionError")
    print("    The identical logic, written as a function, diverges.")
    print("    **Short-circuiting is not a property of `and`. It is a "
          "property of not\n    being a function.**")


# ---------------------------------------------------------------------- 3
def demo_fixpoints():
    rule("3. Y diverges in Python; Z does not")

    Y = lambda f: (lambda x: f(x(x)))(lambda x: f(x(x)))
    Z = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))
    factgen = lambda r: lambda n: 1 if n == 0 else n * r(n - 1)

    print("  Y(factgen)                     = ", end="", flush=True)
    try:
        f = Y(factgen)
        print(f(5))
    except RecursionError:
        print("RecursionError  <- before it was ever applied to 5")
    print("    `x(x)` is an argument to `f`, so Python evaluates it first, "
          "which\n    calls `x(x)` again. The recursion never reaches "
          "`factgen`.")

    print("  Z(factgen)(5)                  = ", end="", flush=True)
    print(Z(factgen)(5))
    print("    `lambda v: x(x)(v)` is a VALUE. Python will not look inside "
          "it, so the\n    unfolding stops until the recursive call is "
          "actually made.")
    print("    Z is Y eta-expanded, and eta-expansion is the standard way to "
          "delay\n    evaluation in a strict language.")

    print("\n  Z(factgen)(n) for n = 0..9     =",
          [Z(factgen)(n) for n in range(10)])

    fibgen = lambda r: lambda n: n if n < 2 else r(n - 1) + r(n - 2)
    print("  Z(fibgen)(n)  for n = 0..9     =",
          [Z(fibgen)(n) for n in range(10)])
    print("    Recursion, with no function ever referring to itself by name.")


# ---------------------------------------------------------------------- 4
def demo_laziness():
    rule("4. what a lazy language does instead")

    def naturals():
        n = 0
        while True:
            yield n
            n += 1

    from itertools import islice
    print("  first 10 of an infinite sequence:",
          list(islice(naturals(), 10)))
    print("    A generator is call-by-need, bolted onto a call-by-value "
          "language.")
    print("    Haskell has this everywhere and by default; Python has it "
          "where you\n    ask for it. The difference is a default, not a "
          "capability.")


def main():
    print(f"; ---- Python {sys.version.split()[0]} ----")
    print("; Python is call-by-value. So are C, Java, Rust, Go, OCaml and "
          "Swift.")
    sys.setrecursionlimit(200)          # fail fast rather than after a while
    demo_strictness()
    demo_shortcircuit()
    demo_fixpoints()
    demo_laziness()
    print("\n; ---- the summary ----")
    print("  Three constructs in this file do not evaluate their operands:")
    print("    `if`/`else`, `and`/`or`, and `lambda`.")
    print("  The first two are keywords because they could not be functions.")
    print("  The third is how you build the first two out of functions "
          "anyway.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
