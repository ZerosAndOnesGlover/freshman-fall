#!/usr/bin/env python3
"""MATH 241 Week 3 -- every number quoted in L10-L12, reproduced.

Pure Python, no dependencies.  Run it:

    python3 dimension.py

Week 2 produced two subspaces and used the words "independent" and
"plane" without defining either.  Week 3 defines them, and finds two
more subspaces while doing it.  This script computes all four for the
matrix Weeks 2 and 3 share, and checks the two facts that make them a
theorem rather than a list: the dimensions add up, and the pairs are
orthogonal.
"""

from fractions import Fraction as F

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def vec(v):
    return "(" + ", ".join(str(x) for x in v) + ")"


def show(name, M):
    print("%s =" % name)
    for row in M:
        print("    [" + "  ".join("%4s" % v for v in row) + "]")


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def col(A, j):
    return [A[i][j] for i in range(len(A))]


def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def rref(A):
    A = [row[:] for row in A]
    m, n = len(A), len(A[0])
    pivots, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, m) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return A, pivots


def null_basis(A):
    R, pivots = rref(A)
    n = len(A[0])
    free = [c for c in range(n) if c not in pivots]
    basis = []
    for f in free:
        v = [F(0)] * n
        v[f] = F(1)
        for i, c in enumerate(pivots):
            v[c] = -R[i][f]
        basis.append(v)
    return basis


def integerise(v):
    """Scale a rational vector to the smallest integer one."""
    from math import gcd
    den = 1
    for x in v:
        den = den * x.denominator // gcd(den, x.denominator)
    w = [x * den for x in v]
    g = 0
    for x in w:
        g = gcd(g, abs(int(x)))
    return [x // g for x in w] if g else w


# --------------------------------------------------------------------------
# L10: independence
# --------------------------------------------------------------------------

banner("L10: independence is a statement about the null space")

for name, X in [("independent", mat((1, 2, 1), (2, 5, 3), (3, 7, 5))),
                ("dependent",   mat((1, 2, 1), (2, 5, 3), (3, 7, 4)))]:
    nb = null_basis(X)
    _, piv = rref(X)
    print("\nvectors as the columns of X   (%s)" % name)
    for j in range(3):
        print("   v%d = %s" % (j + 1, vec(col(X, j))))
    print("   rank %d,  nullity %d" % (len(piv), len(nb)))
    if nb:
        c = integerise(nb[0])
        print("   N(X) is NOT trivial: %s" % vec(c))
        print("   which says  %s v1 + %s v2 + %s v3 = 0  -- a real dependency"
              % tuple(c))
    else:
        print("   N(X) = {0}: the only combination giving zero is the trivial one.")

print("\nThe test is one line: the columns are independent exactly when")
print("N(X) = {0}, i.e. when every column is a pivot column.")


# --------------------------------------------------------------------------
# L11 / L12: the four subspaces of one matrix
# --------------------------------------------------------------------------

A = mat((1, 3, 3, 2),
        (2, 6, 9, 7),
        (-1, -3, 3, 4))
m_, n_ = len(A), len(A[0])

banner("L12: the four fundamental subspaces of A  (Week 2's matrix)")
show("A", A)
R, piv = rref(A)
show("rref(A)", R)
r = len(piv)
rows = [row for row in R if any(row)]
AT = transpose(A)
nb, nbT = null_basis(A), null_basis(AT)

print("\nrank r = %d,  A is %d x %d\n" % (r, m_, n_))
print("%-14s %-8s %-6s %s" % ("subspace", "lives in", "dim", "basis"))
print("-" * 68)
print("%-14s %-8s %-6d %s" % ("C(A)", "R^%d" % m_, r,
                              "  ".join(vec(col(A, c)) for c in piv)))
print("%-14s %-8s %-6d %s" % ("N(A)", "R^%d" % n_, n_ - r,
                              "  ".join(vec(v) for v in nb)))
print("%-14s %-8s %-6d %s" % ("C(A^T) row sp", "R^%d" % n_, r,
                              "  ".join(vec(row) for row in rows)))
print("%-14s %-8s %-6d %s" % ("N(A^T) left", "R^%d" % m_, m_ - r,
                              "  ".join(vec(integerise(v)) for v in nbT)))

print("\ndimensions:  r + (n-r) = %d + %d = %d = n" % (r, n_ - r, n_))
print("             r + (m-r) = %d + %d = %d = m" % (r, m_ - r, m_))
print("row rank = column rank = %d  -- the same r in both lines." % r)


banner("L12: the left null space IS Week 2's plane equation")
y = integerise(nbT[0])
print("basis of N(A^T):", vec(y))
print("\nWeek 2's L08 SS5 found C(A) = { b : 5b1 - 2b2 + b3 = 0 } by hand.")
print("Those coefficients are exactly this vector, and here is why:")
print("   y^T A =", vec([sum(y[i] * A[i][j] for i in range(m_)) for j in range(n_)]))
print("so y is perpendicular to every column, hence to everything they span.")
print("Each dimension of N(A^T) is one solvability condition on b, and")
print("dim N(A^T) = m - r = %d, which is why there was exactly one." % (m_ - r))


banner("L12: the pairs are orthogonal  (Week 8, three weeks early)")
print("N(A) against the row space -- every pair:")
for s in nb:
    for row in rows:
        print("   %-16s . %-16s = %s" % (vec(s), vec(row), dot(s, row)))
print("\nN(A^T) against C(A) -- every pair:")
for c in piv:
    print("   %-16s . %-16s = %s" % (vec(y), vec(col(A, c)), dot(y, col(A, c))))
print("\nEvery dot product is zero, and none of it was arranged.")


banner("L12: elimination keeps the ROW space and moves the column space")
print("Every row of A is a combination of rref(A)'s nonzero rows:")
for i, row in enumerate(A):
    coeffs = [row[c] for c in piv]
    built = [sum(coeffs[k] * rows[k][j] for k in range(r)) for j in range(n_)]
    print("   row%d = %s*%s + %s*%s = %s   %s"
          % (i + 1, coeffs[0], vec(rows[0]), coeffs[1], vec(rows[1]),
             vec(built), "OK" if built == row else "MISMATCH"))
print("\nSo C(A^T) = C(rref(A)^T): the row space survives elimination.")
print("C(A) does not -- Week 2's L08 SS4.  Rows are combined; columns are moved.")
print("That is why a basis for the row space is read off rref, and a basis")
print("for the column space has to be read back from A.")
