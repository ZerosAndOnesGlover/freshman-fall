#!/usr/bin/env python3
"""What a macro can do that a function cannot, measured.

    python3 demo.py      (or: python3 lisp.py)

Five demonstrations, in the order L21 uses them:

  1. code is data
  2. a function cannot be `unless`; a macro can
  3. `while`, as library code, in six lines
  4. the macro is gone before anything runs
  5. **variable capture** -- Week 7's bug, in a macro system, shipped
"""
import sys

from lisp import (run, read, write, global_env, leval, macroexpand,
                  LispError, S)


def rule(n, title):
    print(f"\n; ---- {n}. {title} ----")


def show(src, env, label=None):
    """Evaluate, printing either the value or the error it raised."""
    try:
        r, _ = run(src, env)
        out = write(r)
    except LispError as e:
        out = f"ERROR: {e}"
    except RecursionError:
        out = "ERROR: recursion limit"
    print(f"  {label or src:<44} => {out}")
    return out


def main():
    env = global_env()

    # ---------------------------------------------------------------- 1
    rule(1, "code is data")
    show("(quote (if a b c))", env)
    show("(car (quote (if a b c)))", env)
    show("(length (quote (if a b c)))", env)
    show("(cons (quote *) (cdr (quote (+ 2 3))))", env)
    print("\n      That last line BUILT A PROGRAM: `(* 2 3)`, out of a")
    print("      quoted `(+ 2 3)` and a symbol, using `cons` and `cdr` --")
    print("      the same list operations you would use on any data.")
    print("      A Lisp program is a Lisp list. That is homoiconicity, and")
    print("      it is why a macro is an ordinary list-manipulating function.")

    # ---------------------------------------------------------------- 2
    rule(2, "a function cannot be `unless`; a macro can")
    run("(define unless-fn (lambda (test body) (if test nil body)))", env)
    run("(defmacro unless-mac (test body) `(if ,test nil ,body))", env)

    print("  `boom` raises if it is ever evaluated.\n")
    show("(unless-fn #t (boom))", env)
    show("(unless-mac #t (boom))", env)
    print()
    show("(unless-fn #f 42)", env)
    show("(unless-mac #f 42)", env)
    print("\n      Identical definitions of the same idea. The function")
    print("      evaluated the branch it was about to discard, because a")
    print("      function's arguments are evaluated before it is entered.")
    print("      **This is Week 7 section 10, and the macro is the way out.**")

    # ---------------------------------------------------------------- 3
    rule(3, "`while`, as library code")
    run("""
      (defmacro while (test . body)
        `(begin
           (define loop-fn
             (lambda () (if ,test (begin ,@body (loop-fn)) nil)))
           (loop-fn)))
    """, env)
    run("(define i 0)", env)
    run("(define total 0)", env)
    show("(while (< i 5) (set! total (+ total i)) (set! i (+ i 1)))",
         env, "(while (< i 5) ...) then total")
    show("total", env)
    print("\n      A loop, added to the language, by a user, in six lines.")
    print("      No change to the evaluator: `while` is not a special form.")

    # ---------------------------------------------------------------- 4
    rule(4, "the macro is gone before anything runs")
    for src in ("(unless-mac #t (boom))",
                "(unless-mac (> x 3) (print x))"):
        form = read(src)[0]
        print(f"  {src}")
        print(f"      expands to  {write(macroexpand(form, env))}")
    print("\n      Expansion happens once, at expansion time. What the")
    print("      evaluator sees contains no macro at all -- exactly like")
    print("      Week 8's dictionary passing, where the `=>` became a `->`")
    print("      and nothing type-class-shaped survived.")

    # ---------------------------------------------------------------- 5
    rule(5, "variable capture: Week 7's bug, shipped")
    run("""
      (defmacro swap-bad (a b)
        `(begin (define tmp ,a) (set! ,a ,b) (set! ,b tmp)))
    """, env)
    run("(define x 1)", env)
    run("(define y 2)", env)
    show("(begin (swap-bad x y) (list x y))", env, "swap-bad x y")
    print("      correct so far.\n")

    run("(define tmp 100)", env)
    run("(define z 7)", env)
    print("  now the caller happens to have a variable called `tmp`:")
    show("(begin (swap-bad tmp z) (list tmp z))", env, "swap-bad tmp z")
    print("      expected (7 100).")
    form = read("(swap-bad tmp z)")[0]
    print(f"      expands to  {write(macroexpand(form, env))}")
    print("\n      The macro's `tmp` and the caller's `tmp` are the same name.")
    print("      **This is capture** -- Week 7 section 5, in a macro system,")
    print("      and it is exactly why C's `#define SWAP(a,b)` is unsafe.")

    print("\n  the fix, and it is the same fix Week 7 used -- a fresh name:")
    run("""
      (defmacro swap (a b)
        (define g (gensym))
        `(begin (define ,g ,a) (set! ,a ,b) (set! ,b ,g)))
    """, env)
    run("(define tmp 100)", env)
    run("(define z 7)", env)
    show("(begin (swap tmp z) (list tmp z))", env, "swap tmp z")
    form = read("(swap tmp z)")[0]
    print(f"      expands to  {write(macroexpand(form, env))}")
    print("\n      `gensym` is `fresh` from Week 7's `subst`, under another")
    print("      name, solving the same problem for the same reason.")
    print("      A macro system that does this automatically is called")
    print("      **hygienic**: Scheme's `syntax-rules`, Rust's `macro_rules!`.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
