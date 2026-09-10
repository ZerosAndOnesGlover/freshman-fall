#!/usr/bin/env python3
"""MATH 241 Week 6 -- every number quoted in L19-L20, reproduced.

Pure Python, no dependencies.  Run it:

    python3 eigen.py

Week 4 asked, without the vocabulary, which vectors a transformation
sends to multiples of themselves.  Week 5 built the tool.  This script
answers the question for the week's matrix and for six transformations
whose eigenvalues you can predict from the geometry -- including two
that go wrong, which is what Week 7 is for.

Everything is exact, in Fraction, except the complex eigenvalues of a
rotation, which are reported as surds.
"""

from fractions import Fraction as F

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def vec(v):
    return "(" + ", ".join(str(x) for x in v) + ")"


def show(name, A, w=5):
    print("%s =" % name)
    for row in A:
        print("    [" + " ".join(("%" + str(w) + "s") % v for v in row) + "]")


def det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    return sum((-1) ** j * A[0][j] *
               det([[A[i][k] for k in range(n) if k != j] for i in range(1, n)])
               for j in range(n))


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def shift(A, lam):
    """A - lam*I."""
    return [[A[i][j] - (lam if i == j else 0) for j in range(len(A))]
            for i in range(len(A))]


def nullspace(A):
    """Basis for N(A), by rref.  Week 2's algorithm, unchanged."""
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
    basis = []
    for f in [c for c in range(n) if c not in pivots]:
        v = [F(0)] * n
        v[f] = F(1)
        for i, c in enumerate(pivots):
            v[c] = -A[i][f]
        basis.append(v)
    return basis


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


def charpoly(A):
    """Coefficients of det(A - x I), lowest power first, by interpolation."""
    n = len(A)
    pts = [(F(x), det(shift(A, F(x)))) for x in range(n + 1)]
    coeffs = [F(0)] * (n + 1)
    for xi, yi in pts:
        basis, denom = [F(1)], F(1)
        for xj, _ in pts:
            if xj == xi:
                continue
            basis = [(basis[k - 1] if k > 0 else F(0)) -
                     xj * (basis[k] if k < len(basis) else F(0))
                     for k in range(len(basis) + 1)]
            denom *= (xi - xj)
        for k, c in enumerate(basis):
            coeffs[k] += yi * c / denom
    return coeffs


def poly_str(c):
    """Render coefficients as a polynomial in L, highest power first."""
    out = []
    for k in range(len(c) - 1, -1, -1):
        if c[k] == 0:
            continue
        term = "" if abs(c[k]) == 1 and k > 0 else str(abs(c[k]))
        if k >= 1:
            term += "L" + ("^%d" % k if k > 1 else "")
        out.append(("- " if c[k] < 0 else "+ ") + term)
    s = " ".join(out)
    return s[2:] if s.startswith("+ ") else "-" + s[2:]


# --------------------------------------------------------------------------
# L19: the week's matrix.
# --------------------------------------------------------------------------

A = mat((2, -1, 1),
        (-1, 2, -1),
        (1, 1, 2))

banner("L19: eigenvalues of the week's matrix")
show("A", A)
c = charpoly(A)
print("\ndet(A - L I) = %s" % poly_str(c))
print("             = -(L - 1)(L - 2)(L - 3)")
print("\nroots: L = 1, 2, 3\n")

lams = [F(1), F(2), F(3)]
for lam in lams:
    B = shift(A, lam)
    ns = nullspace(B)
    print("lambda = %s" % lam)
    print("   det(A - %sI) = %s   <- zero, so A - %sI is singular" % (lam, det(B), lam))
    for v in ns:
        w = integerise(v)
        Aw = [sum(A[i][j] * w[j] for j in range(3)) for i in range(3)]
        print("   eigenvector %-12s  A v = %-12s = %s v  %s"
              % (vec(w), vec(Aw), lam, "OK" if Aw == [lam * x for x in w] else "FAIL"))
    print("   eigenspace dimension: %d" % len(ns))


banner("L20: trace and determinant are the eigenvalues in disguise")
print("trace A       = %s        1 + 2 + 3 = %s" % (trace(A), sum(lams)))
print("det A         = %s        1 x 2 x 3 = %s" % (det(A), lams[0] * lams[1] * lams[2]))
print("\nWeek 4's L15 SS6 could only VERIFY that similar matrices share these")
print("two numbers.  Now they have meanings: the sum and the product of the")
print("eigenvalues -- which are themselves basis-independent, because")
print("det(A - L I) is unchanged by similarity (L20 SS3).")


# --------------------------------------------------------------------------
# L19: six transformations whose eigenvalues you can predict.
# --------------------------------------------------------------------------

banner("L19: eigenvalues you should be able to guess before computing")

cases = [
    ("reflect across y=x",   mat((0, 1), (1, 0)),                        [F(1), F(-1)]),
    ("project onto y=x",     [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]],   [F(1), F(0)]),
    ("scale x3, y x2",       mat((3, 0), (0, 2)),                        [F(3), F(2)]),
    ("shear [[1,1],[0,1]]",  mat((1, 1), (0, 1)),                        [F(1)]),
    ("triangular",           mat((2, 5), (0, 7)),                        [F(2), F(7)]),
]

for name, T, lams_ in cases:
    print("\n%s" % name)
    print("   char poly: det(T - L I) = %s" % poly_str(charpoly(T)))
    print("   trace %-4s det %-6s" % (trace(T), det(T)))
    tot = 0
    for lam in lams_:
        ns = nullspace(shift(T, lam))
        tot += len(ns)
        print("   lambda = %-4s eigenspace dim %d: %s"
              % (lam, len(ns), " ".join(vec(integerise(v)) for v in ns)))
    if tot < len(T):
        print("   *** only %d independent eigenvector%s for a %dx%d matrix ***"
              % (tot, "" if tot == 1 else "s", len(T), len(T)))
        print("   *** DEFECTIVE -- no basis of eigenvectors exists.  Week 7. ***")


banner("L19: a rotation has no real eigenvalues at all")
R = mat((0, -1), (1, 0))                       # rotate 90 degrees
show("R (rotate 90)", R)
print("\ndet(R - L I) = %s" % poly_str(charpoly(R)))
print("L^2 + 1 = 0 has no real root: a rotation fixes no direction,")
print("which is geometrically obvious and algebraically fatal.")
print("\nOver the complex numbers L = i and L = -i, and")
print("   sum  = i + (-i) = 0 = trace R")
print("   prod = i x (-i)  = 1 = det R")
print("so the trace and determinant identities survive; only the")
print("reality of the answers does not.  Week 7 takes this seriously.")


banner("L20: why the two multiplicities differ")
S = mat((1, 1), (0, 1))
print("shear [[1,1],[0,1]]:")
print("   det(S - L I) = %s = (1 - L)^2" % poly_str(charpoly(S)))
print("   algebraic multiplicity of L = 1 : 2   (a double root)")
print("   geometric multiplicity          : %d   (dim of the eigenspace)"
      % len(nullspace(shift(S, F(1)))))
print("\nAlgebraic 2, geometric 1.  The gap is exactly what stops this")
print("matrix from being diagonalisable -- and it settles PS 4 Q5(d):")
print("I and [[1,1],[0,1]] share trace, determinant, rank AND")
print("characteristic polynomial, and are still not similar, because")
print("I has two independent eigenvectors and this has one.")
