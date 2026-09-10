#!/usr/bin/env python3
"""MATH 241 Week 8 -- every number quoted in L24-L26, reproduced.

Pure Python, no dependencies.  Run it:

    python3 orthogonal.py

Week 2 built vector spaces with no length and no angle, and said they
would come back in Week 8.  Here they are, and they immediately pay
three debts: the four subspaces are orthogonal in pairs (Week 3), a
projection is P = A(A^T A)^-1 A^T with P^2 = P (Weeks 1 and 4), and an
orthonormal basis has condition number exactly 1 (Weeks 0 and 7).

Exact in Fraction throughout, except the normalisations in the QR
section, which need square roots and say so.
"""

from fractions import Fraction as F
import math

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def vec(v, fmt=str):
    return "(" + ", ".join(fmt(x) for x in v) + ")"


def show(name, A, w=7, fmt=str):
    print("%s =" % name)
    for row in A:
        print("    [" + " ".join(("%" + str(w) + "s") % fmt(v) for v in row) + "]")


def T(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def col(A, j):
    return [A[i][j] for i in range(len(A))]


def inv(S):
    n = len(S)
    aug = [S[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for k in range(n):
        p = next(i for i in range(k, n) if aug[i][k] != 0)
        aug[k], aug[p] = aug[p], aug[k]
        pv = aug[k][k]
        aug[k] = [v / pv for v in aug[k]]
        for i in range(n):
            if i != k and aug[i][k]:
                f = aug[i][k]
                aug[i] = [a - f * b for a, b in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def nullspace(A):
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
    out = []
    for f in [c for c in range(n) if c not in pivots]:
        v = [F(0)] * n
        v[f] = F(1)
        for i, c in enumerate(pivots):
            v[c] = -A[i][f]
        out.append(v)
    return out, pivots


def integerise(v):
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
# L24: the four subspaces are orthogonal in pairs.  Week 3's promise.
# --------------------------------------------------------------------------

banner("L24: the four subspaces, orthogonal in pairs  (Week 3's matrix)")

W3 = mat((1, 3, 3, 2),
         (2, 6, 9, 7),
         (-1, -3, 3, 4))
show("A", W3, 4)

nb, _ = nullspace(W3)
nbT, _ = nullspace(T(W3))


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


Rmat, piv = rref(W3)
rowbasis = [row for row in Rmat if any(row)]
colbasis = [col(W3, c) for c in piv]
leftnull = [integerise(v) for v in nbT]

print("\nN(A) against the row space -- every pair:")
for s in nb:
    for q in rowbasis:
        print("   %-18s . %-18s = %s" % (vec(integerise(s)), vec(q), dot(integerise(s), q)))
print("\nN(A^T) against C(A) -- every pair:")
for y in leftnull:
    for c_ in colbasis:
        print("   %-18s . %-18s = %s" % (vec(y), vec(c_), dot(y, c_)))

print("\nEvery dot product is zero.  Week 3's L12 SS7 observed this and could")
print("not prove it, because vector spaces had no dot product until today.")
print("\nThe proof is one line: Ax = 0 says every entry of Ax is zero, and")
print("entry i of Ax is (row i) . x.  So x is perpendicular to every row,")
print("hence to the whole row space.")


# --------------------------------------------------------------------------
# L25: projection.
# --------------------------------------------------------------------------

banner("L25: projecting onto a subspace")

A = mat((1, 1),
        (1, 2),
        (1, 3))
show("A  (its column space is a plane in R^3)", A, 4)

AtA = mul(T(A), A)
show("\nA^T A", AtA, 4)
print("   invertible because A has independent columns  (PS 2 Q5(c))")

P = mul(A, mul(inv(AtA), T(A)))
print("\nP = A (A^T A)^-1 A^T =")
for row in P:
    print("    [" + " ".join("%7s" % v for v in row) + "]")

print("\n   P^2 = P :", mul(P, P) == P, "   (projecting twice changes nothing)")
print("   P^T = P :", T(P) == P, "   (a projection matrix is symmetric)")

print("\nProjecting b = (6, 0, 0):")
b = [F(6), F(0), F(0)]
p = mv(P, b)
e = [b[i] - p[i] for i in range(3)]
print("   p = P b   = %s   <- the nearest point of C(A) to b" % vec(p))
print("   e = b - p = %s   <- the error" % vec(e))
print("\n   e . a1 = %s     e . a2 = %s     <- e is orthogonal to C(A)"
      % (dot(e, col(A, 0)), dot(e, col(A, 1))))
print("   A^T e  = %s               <- so e lies in N(A^T)" % vec(mv(T(A), e)))
print("\nSo b splits as p + e with p in C(A) and e in N(A^T): the two")
print("subspaces of R^3 from L24, and every b splits this way exactly once.")


# --------------------------------------------------------------------------
# L26: orthonormal bases and Gram-Schmidt.
# --------------------------------------------------------------------------

banner("L26: Gram-Schmidt, exactly")

cols = [[F(1), F(1), F(1)],
        [F(1), F(2), F(3)],
        [F(1), F(4), F(9)]]
print("start from the columns  a1 = %s   a2 = %s   a3 = %s"
      % (vec(cols[0]), vec(cols[1]), vec(cols[2])))

orth = []
for j, a in enumerate(cols):
    w = a[:]
    for q in orth:
        c = F(dot(a, q), dot(q, q))
        w = [x - c * qi for x, qi in zip(w, q)]
        print("   subtract %-6s x %s" % (str(c), vec(q)))
    orth.append(w)
    print("   -> w%d = %-24s  |w|^2 = %s" % (j + 1, vec(w), dot(w, w)))

print("\ncleared of fractions:")
for j, w in enumerate(orth):
    print("   w%d ~ %s" % (j + 1, vec(integerise(w))))
print("\npairwise dot products:",
      [dot(orth[i], orth[j]) for i in range(3) for j in range(i + 1, 3)])

print("\nThose three are (1,1,1), (-1,0,1), (1,-2,1): constant, linear and")
print("quadratic, orthogonalised.  They are the discrete Legendre vectors,")
print("and Week 12's Fourier item is the same construction on functions.")


banner("L26: A = QR, and Q^T Q = I")

Amat = [[float(cols[j][i]) for j in range(3)] for i in range(3)]
Q, Rm = [], [[0.0] * 3 for _ in range(3)]
for j in range(3):
    a = [Amat[i][j] for i in range(3)]
    w = a[:]
    for i, q in enumerate(Q):
        Rm[i][j] = sum(x * y for x, y in zip(a, q))
        w = [x - Rm[i][j] * qi for x, qi in zip(w, q)]
    Rm[j][j] = math.sqrt(sum(x * x for x in w))
    Q.append([x / Rm[j][j] for x in w])
Qm = [[Q[j][i] for j in range(3)] for i in range(3)]

show("A", Amat, 9, lambda v: "%.4f" % v)
show("Q", Qm, 9, lambda v: "%.6f" % v)
show("R", Rm, 9, lambda v: "%.6f" % v)

QR = mul(Qm, Rm)
print("\nmax |QR - A| = %.2e" % max(abs(QR[i][j] - Amat[i][j])
                                    for i in range(3) for j in range(3)))
QtQ = mul(T(Qm), Qm)
print("max |Q^T Q - I| = %.2e" % max(abs(QtQ[i][j] - (1.0 if i == j else 0.0))
                                     for i in range(3) for j in range(3)))
print("\nR is upper triangular with the norms of the Gram-Schmidt vectors")
print("on its diagonal: sqrt3 = %.6f, sqrt2 = %.6f, sqrt(2/3) = %.6f"
      % (3 ** .5, 2 ** .5, (2 / 3) ** .5))


banner("L26: why an orthonormal basis is the one to want")

print("For Q with Q^T Q = I:")
print("   Q^-1 = Q^T          -- the inverse is free, no elimination")
print("   ||Qx|| = ||x||      -- lengths are preserved")
print("   cond(Q) = 1         -- the best possible")
print("\nCompare Week 7's near-defective S:")
for eps in (1e-2, 1e-4, 1e-8):
    # S has columns (1,0) and (1,eps): nearly parallel
    s11, s12, s21, s22 = 1.0, 1.0, 0.0, eps
    det = s11 * s22 - s12 * s21
    # 2-norm condition number via the explicit 2x2 formula
    n2 = s11 * s11 + s12 * s12 + s21 * s21 + s22 * s22
    disc = math.sqrt(max(n2 * n2 - 4 * det * det, 0.0))
    smax = math.sqrt((n2 + disc) / 2)
    smin = math.sqrt((n2 - disc) / 2)
    print("   eigenvectors (1,0) and (1,%.0e): cond(S) = %.3g" % (eps, smax / smin))
print("\nAn orthonormal S would give 1 at every row of that table.  This is")
print("why Week 10 (symmetric matrices) and Week 11 (the SVD) both insist")
print("on orthonormal bases: existence is not enough, conditioning matters.")
