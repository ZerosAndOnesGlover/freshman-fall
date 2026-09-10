#!/usr/bin/env python3
"""MATH 241 Week 5 -- every number quoted in L16-L18, reproduced.

Pure Python, no dependencies.  Run it:

    python3 determinants.py

The determinant is one number attached to a square matrix.  This script
computes it three ways -- from the pivots, from cofactors, and from the
big permutation formula -- confirms they agree, and then measures the
gap between the way you should compute it and the way the definition
suggests.
"""

from fractions import Fraction as F
from itertools import permutations
import math
import time

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def show(name, A, w=5):
    print("%s =" % name)
    for row in A:
        print("    [" + " ".join(("%" + str(w) + "s") % v for v in row) + "]")


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


# --------------------------------------------------------------------------
# Three ways to compute one number.
# --------------------------------------------------------------------------

def det_pivots(A):
    """By elimination: the product of the pivots, with a sign per exchange.
    This is the O(n^3/3) method, and it is what every library does."""
    A = [row[:] for row in A]
    n = len(A)
    sign, pivots = 1, []
    for k in range(n):
        p = next((i for i in range(k, n) if A[i][k] != 0), None)
        if p is None:
            return F(0), []                 # a missing pivot: singular
        if p != k:
            A[k], A[p] = A[p], A[k]
            sign = -sign
        pivots.append(A[k][k])
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    d = F(sign)
    for p in pivots:
        d *= p
    return d, pivots


def det_cofactor(A):
    """Expansion along the first row.  O(n!) -- the definition, not a method."""
    n = len(A)
    if n == 1:
        return A[0][0]
    total = F(0)
    for j in range(n):
        minor = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        total += (-1) ** j * A[0][j] * det_cofactor(minor)
    return total


def det_permutations(A):
    """The big formula: n! terms, one per permutation, signed."""
    n = len(A)
    total = F(0)
    for perm in permutations(range(n)):
        # sign of the permutation, by counting inversions
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        term = F(-1) ** inv
        for i in range(n):
            term *= A[i][perm[i]]
        total += term
    return total


# --------------------------------------------------------------------------
# L16: the determinant of Week 1's matrix.
# --------------------------------------------------------------------------

A = mat((2, 1, -1),
        (4, 5, 0),
        (-2, 8, 11))

banner("L16: three routes to one number  (Week 1's matrix, a fourth time)")
show("A", A)
d, pivots = det_pivots(A)
print("\npivots from elimination:", [str(p) for p in pivots],
      " -- exactly the 2, 3, 4 of Week 1's L02")
print("\n  product of the pivots   : %s" % d)
print("  cofactor expansion      : %s" % det_cofactor(A))
print("  the big formula (n! = 6): %s" % det_permutations(A))
print("\nAll three agree, as they must.  Week 1 computed the pivots and")
print("never multiplied them together; that product was the determinant.")


# --------------------------------------------------------------------------
# L16: the properties, checked.
# --------------------------------------------------------------------------

banner("L16: the three defining properties, and what follows")

I3 = mat((1, 0, 0), (0, 1, 0), (0, 0, 1))
print("det I = %s" % det_cofactor(I3))

swap = [A[1], A[0], A[2]]
print("swap two rows: det = %s   (was %s -- the sign flipped)"
      % (det_cofactor(swap), det_cofactor(A)))

scaled = [[2 * v for v in A[0]], A[1], A[2]]
print("scale ONE row by 2: det = %s   (= 2 x %s)"
      % (det_cofactor(scaled), det_cofactor(A)))

allscaled = [[2 * v for v in row] for row in A]
print("scale the WHOLE matrix by 2: det = %s   (= 2^3 x %s)"
      % (det_cofactor(allscaled), det_cofactor(A)))

addrow = [A[0], [A[1][j] + 5 * A[0][j] for j in range(3)], A[2]]
print("add 5 x row1 to row2: det = %s   -- UNCHANGED" % det_cofactor(addrow))
print("   which is why elimination can be used to compute it at all.")

dup = [A[0], A[0], A[2]]
print("two equal rows: det = %s" % det_cofactor(dup))
print("   (swapping them changes nothing and must flip the sign, so d = -d)")


# --------------------------------------------------------------------------
# L17: what the definition costs.
# --------------------------------------------------------------------------

banner("L17: the big formula is a definition, not a method")
print("%5s  %-14s  %-12s  %s" % ("n", "n! terms", "n^3/3 ops", "ratio"))
for n in (5, 10, 15, 20, 25):
    f = math.factorial(n)
    print("%5d  %-14.4g  %-12.4g  %.3g" % (n, f, n ** 3 / 3, f / (n ** 3 / 3)))

secs = math.factorial(20) / 1e9
print("\nAt a billion terms per second, a 20x20 determinant by the big")
print("formula takes %.4g years.  By elimination it is %d operations." %
      (secs / 3600 / 24 / 365, 20 ** 3 / 3))

n = 8
import random
random.seed(241)
while True:                      # a singular matrix would let elimination
    B = mat(*[[random.randint(-9, 9) for _ in range(n)]     # exit early and
              for _ in range(n)])                           # flatter the timing
    dp, _ = det_pivots(B)
    if dp != 0:
        break
t = time.perf_counter(); dp, _ = det_pivots(B); tp = time.perf_counter() - t
t = time.perf_counter(); dc = det_cofactor(B); tc = time.perf_counter() - t
assert dp == dc, "the two methods disagree"
print("\nmeasured on a nonsingular %dx%d integer matrix (det = %s):" % (n, n, dp))
print("   elimination : %8.5f s" % tp)
print("   cofactors   : %8.5f s   -- %.0fx slower, and n is only %d"
      % (tc, tc / tp, n))


# --------------------------------------------------------------------------
# L18: the product rule and its consequences.
# --------------------------------------------------------------------------

banner("L18: det(AB) = det(A) det(B)")

C = mat((1, 2, 0), (0, 1, 3), (2, 0, 1))
dA, dC = det_cofactor(A), det_cofactor(C)
dAC = det_cofactor(mul(A, C))
print("det A = %s,  det C = %s,  det A x det C = %s" % (dA, dC, dA * dC))
print("det(AC) = %s   %s" % (dAC, "MATCH" if dAC == dA * dC else "MISMATCH"))
print("\nAnd det(CA) = %s -- the same, even though AC and CA are different"
      % det_cofactor(mul(C, A)))
print("matrices.  The determinant does not care about the order.")

print("\ndet(A^T) = %s  -- equal to det A, so every row fact is a column fact"
      % det_cofactor([[A[i][j] for i in range(3)] for j in range(3)]))


banner("L18: similarity invariance -- the theorem Week 4 assumed")

Mb = mat((1, 1, 0), (0, 1, 1), (1, 0, 1))
dM = det_cofactor(Mb)
Mi = None
# invert Mb by Gauss-Jordan in exact arithmetic
aug = [Mb[i][:] + [F(int(i == j)) for j in range(3)] for i in range(3)]
for k in range(3):
    p = next(i for i in range(k, 3) if aug[i][k] != 0)
    aug[k], aug[p] = aug[p], aug[k]
    pv = aug[k][k]
    aug[k] = [v / pv for v in aug[k]]
    for i in range(3):
        if i != k and aug[i][k]:
            f = aug[i][k]
            aug[i] = [a - f * b for a, b in zip(aug[i], aug[k])]
Mi = [row[3:] for row in aug]

Bsim = mul(Mi, mul(A, Mb))
print("det M = %s,  det(M^-1) = %s,  product = %s"
      % (dM, det_cofactor(Mi), dM * det_cofactor(Mi)))
show("B = M^-1 A M", Bsim)
print("\ndet B = %s   det A = %s   %s"
      % (det_cofactor(Bsim), dA, "EQUAL" if det_cofactor(Bsim) == dA else "NOT"))
print("\nWeek 4's L15 SS6 used det(M^-1 A M) = det A and owed you the proof.")
print("It is one line from the product rule:")
print("   det(M^-1) det(A) det(M) = det(A) det(M^-1) det(M) = det(A) det(I) = det(A)")


# --------------------------------------------------------------------------
# L18: area.
# --------------------------------------------------------------------------

banner("L18: the determinant is the volume factor")

for name, T in [("identity",            mat((1, 0), (0, 1))),
                ("scale x by 3",        mat((3, 0), (0, 1))),
                ("scale both by 2",     mat((2, 0), (0, 2))),
                ("shear",               mat((1, 2), (0, 1))),
                ("rotate 90 degrees",   mat((0, -1), (1, 0))),
                ("reflect across y=x",  mat((0, 1), (1, 0))),
                ("project onto y=x",    [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])]:
    d = T[0][0] * T[1][1] - T[0][1] * T[1][0]
    note = ""
    if d == 0:
        note = "   <- collapses the plane to a line"
    elif d < 0:
        note = "   <- reverses orientation"
    print("%-22s det = %-6s area factor = %-5s%s" % (name, d, abs(d), note))

print("\nThe shear has det 1: it slides the unit square into a parallelogram")
print("of the same base and height, so the area is untouched.  The rotation")
print("and the reflection both have |det| = 1 -- rigid motions -- but the")
print("reflection's is negative, which is exactly what 'flips the plane' means.")
