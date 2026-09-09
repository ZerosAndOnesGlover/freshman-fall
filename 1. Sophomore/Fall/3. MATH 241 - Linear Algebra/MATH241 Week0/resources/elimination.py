#!/usr/bin/env python3
"""MATH 241 Week 0 -- every number quoted in L01-L03, reproduced.

Pure Python, no dependencies.  Run it:

    python3 elimination.py

The point is not the code.  The point is that nothing in the notes is a
number you have to take on trust: the exact results are exact, and the
floating-point results are what your machine will actually print.
"""

from fractions import Fraction as F
import time

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


# --------------------------------------------------------------------------
# The running example.  A = LU exactly, with integer L, U and pivots.
# --------------------------------------------------------------------------

A = [[2, 1, -1],
     [4, 5, 0],
     [-2, 8, 11]]
B = [1, 14, 47]


def eliminate(A, b, pivot=False, exact=True):
    """Forward elimination.  Returns (U|c), the pivots, and the multipliers.

    exact=True works in Fraction, so the arithmetic is the arithmetic you
    would do by hand.  exact=False works in float, which is the arithmetic
    your computer does, and the two are not the same thing (L03 SS4).
    """
    n = len(A)
    one = F(1) if exact else 1.0
    M = [[one * v for v in row] + [one * bi] for row, bi in zip(A, b)]
    mult, swaps = [], []
    for k in range(n):
        if pivot:
            p = max(range(k, n), key=lambda r: abs(M[r][k]))
            if p != k:
                M[k], M[p] = M[p], M[k]
                swaps.append((k, p))
        if M[k][k] == 0:
            raise ZeroDivisionError("zero pivot in column %d -- singular, "
                                    "or needs a row exchange" % k)
        for i in range(k + 1, n):
            m = M[i][k] / M[k][k]
            mult.append(((i, k), m))
            for j in range(k, n + 1):
                M[i][j] -= m * M[k][j]
    return M, [M[k][k] for k in range(n)], mult, swaps


def back_substitute(M):
    n = len(M)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


banner("L01-L02: the running example, exactly")
M, pivots, mult, _ = eliminate(A, B)
print("A =", A, "   b =", B)
print("\nrow echelon form [U | c]:")
for row in M:
    print("   ", [str(v) for v in row])
print("\npivots      :", [str(p) for p in pivots])
print("multipliers :", [("l%d%d" % (i + 1, k + 1), str(m)) for (i, k), m in mult])
det = 1
for p in pivots:
    det *= p
print("determinant : product of the pivots =", det)
print("solution    :", [str(v) for v in back_substitute(M)])


# --------------------------------------------------------------------------
# L03 SS4: what partial pivoting is for.
# --------------------------------------------------------------------------

banner("L03: eps*x + y = 1 ; x + y = 2   -- the same algorithm, two orders")
print("%-10s  %-24s %-24s" % ("eps", "no pivoting", "partial pivoting"))
for eps in (1e-15, 1e-16, 1e-17, 1e-20):
    Ae, be = [[eps, 1.0], [1.0, 1.0]], [1.0, 2.0]
    plain = back_substitute(eliminate(Ae, be, pivot=False, exact=False)[0])
    piv = back_substitute(eliminate(Ae, be, pivot=True, exact=False)[0])
    print("%-10g  x=%-22r x=%-22r" % (eps, plain[0], piv[0]))
print("\nthe exact answer is x = 1/(1-eps), which is 1 to every digit a")
print("double can hold.  Without pivoting the multiplier is 1/eps.")


# --------------------------------------------------------------------------
# L03 SS5: a matrix can be nonsingular and still useless.
# --------------------------------------------------------------------------

def hilbert(n, exact=True):
    return [[F(1, i + j + 1) if exact else 1.0 / (i + j + 1)
             for j in range(n)] for i in range(n)]


def inverse(Mx):
    """Gauss-Jordan.  Exact if the entries are Fractions."""
    n = len(Mx)
    one = F(1) if isinstance(Mx[0][0], F) else 1.0
    aug = [row[:] + [one * (i == j) for j in range(n)]
           for i, row in enumerate(Mx)]
    for k in range(n):
        p = max(range(k, n), key=lambda r: abs(aug[r][k]))
        aug[k], aug[p] = aug[p], aug[k]
        pv = aug[k][k]
        aug[k] = [v / pv for v in aug[k]]
        for i in range(n):
            if i != k and aug[i][k]:
                f = aug[i][k]
                aug[i] = [vi - f * vk for vi, vk in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def norm_inf(Mx):
    return max(sum(abs(v) for v in row) for row in Mx)


banner("L03: the Hilbert matrices -- nonsingular, and hopeless")
print("%3s  %-16s  %-14s" % ("n", "cond_inf(H)  exact", "max |x_i - 1|"))
for n in (3, 5, 8, 10, 12):
    He = hilbert(n)
    cond = norm_inf(He) * norm_inf(inverse(He))
    Hf = hilbert(n, exact=False)
    bf = [sum(Hf[i]) for i in range(n)]          # so the exact answer is all ones
    x = back_substitute(eliminate(Hf, bf, pivot=True, exact=False)[0])
    print("%3d  %-16.6g  %-14.3g" % (n, float(cond), max(abs(v - 1.0) for v in x)))
print("\nEvery one of these is invertible.  det(H_10) is about 2.2e-53,")
print("and it is not the determinant that is the problem.")


# --------------------------------------------------------------------------
# L03 SS2: the cost.
# --------------------------------------------------------------------------

banner("L03: what elimination costs")
print("%7s  %-14s  %-14s  %-10s" % ("n", "elimination", "back-sub", "ratio"))
print("%7s  %-14s  %-14s  %-10s" % ("", "~n^3/3", "~n^2/2", ""))
for n in (10, 100, 1000, 10000):
    fwd, back = n ** 3 / 3, n * n / 2
    print("%7d  %-14.3g  %-14.3g  %-10.0f" % (n, fwd, back, fwd / back))

import random

random.seed(241)
n = 100
Ar = [[F(random.randint(-9, 9)) for _ in range(n)] for _ in range(n)]
br = [F(random.randint(-9, 9)) for _ in range(n)]
t = time.perf_counter()
_, piv, _, _ = eliminate(Ar, br, pivot=True)
dt = time.perf_counter() - t
digits = max(len(str(p.numerator)) + len(str(p.denominator)) for p in piv)
print("\nexact elimination on a random %dx%d integer matrix: %.2f s" % (n, n, dt))
print("the widest pivot it produced needs %d decimal digits to write down." % digits)
print("\nFractions are slow because the numerators grow like that.  The growth")
print("is why numerical linear algebra is done in floating point, and floating")
print("point is why SS4 above is a lecture and not a footnote.")
