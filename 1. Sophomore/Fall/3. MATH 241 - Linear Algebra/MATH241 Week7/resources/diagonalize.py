#!/usr/bin/env python3
"""MATH 241 Week 7 -- every number quoted in L21-L23, reproduced.

Pure Python, no dependencies.  Run it:

    python3 diagonalize.py

Week 6 found the eigenvalues.  This week assembles them into
A = S Lambda S^-1 and cashes it in: matrix powers become scalar
powers, Fibonacci gets a closed form, and a Markov chain's limit
becomes a one-line calculation.

Exact in Fraction where the answer is rational; float where the answer
involves sqrt(5) or a limit, and labelled as such.
"""

from fractions import Fraction as F
import math

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def show(name, A, w=6, fmt=str):
    print("%s =" % name)
    for row in A:
        print("    [" + " ".join(("%" + str(w) + "s") % fmt(v) for v in row) + "]")


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def eye(n, one=F(1)):
    return [[one if i == j else one * 0 for j in range(n)] for i in range(n)]


def mpow(X, k):
    R = eye(len(X), X[0][0] * 0 + (1 if isinstance(X[0][0], float) else F(1)))
    for _ in range(k):
        R = mul(R, X)
    return R


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


def diag(vals):
    n = len(vals)
    return [[F(vals[i]) if i == j else F(0) for j in range(n)] for i in range(n)]


# --------------------------------------------------------------------------
# L21: A = S Lambda S^-1, on Week 6's matrix.
# --------------------------------------------------------------------------

A = mat((2, -1, 1),
        (-1, 2, -1),
        (1, 1, 2))

banner("L21: A = S Lambda S^-1   (Week 6's matrix, assembled)")
show("A", A)

print("\nWeek 6 found eigenvalues 1, 2, 3 with eigenvectors")
print("   (-1, 0, 1)   (-1, 1, 1)   (-1, 1, 0)")
print("\nPut them in the COLUMNS of S, in the same order as Lambda's diagonal:")

S = mat((-1, -1, -1),
        (0, 1, 1),
        (1, 1, 0))
L = diag([1, 2, 3])
Si = inv(S)

show("S", S)
show("Lambda", L)
show("S^-1", Si)

prod = mul(S, mul(L, Si))
print("\nS Lambda S^-1 == A :", prod == A)
print("\nBoth S and S^-1 are integer matrices here, which is luck -- det S = %s."
      % (S[0][0] * (S[1][1] * S[2][2] - S[1][2] * S[2][1])
         - S[0][1] * (S[1][0] * S[2][2] - S[1][2] * S[2][0])
         + S[0][2] * (S[1][0] * S[2][1] - S[1][1] * S[2][0])))
print("Nothing in the theorem promises it; eigenvectors are usually irrational.")


banner("L21: what it is for -- powers become scalar powers")
for k in (2, 5, 10):
    direct = mpow(A, k)
    viaS = mul(S, mul(mpow(L, k), Si))
    print("A^%-3d naively (%d matrix products) : row 0 = %s"
          % (k, k - 1, [str(v) for v in direct[0]]))
    print("      via S Lambda^%-2d S^-1          : agrees = %s" % (k, direct == viaS))
show("Lambda^10", mpow(L, 10), 7)
print("\nLambda^10 is three scalar powers.  A^10 is 9 matrix products naively,")
print("or 4 by repeated squaring, at 2n^3 flops each.  And for A^1000 the")
print("diagonal route is still three scalar powers, while squaring needs 14")
print("matrix products.  The gap grows without limit in k, which is the")
print("whole point of Week 7.")


# --------------------------------------------------------------------------
# L22: when it fails.
# --------------------------------------------------------------------------

banner("L22: the hypothesis is necessary")

def geo_mult(X, lam):
    """dim N(X - lam I), by rref."""
    n = len(X)
    B = [[X[i][j] - (lam if i == j else 0) for j in range(n)] for i in range(n)]
    B = [row[:] for row in B]
    pivots, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, n) if B[i][c] != 0), None)
        if p is None:
            continue
        B[r], B[p] = B[p], B[r]
        pv = B[r][c]
        B[r] = [v / pv for v in B[r]]
        for i in range(n):
            if i != r and B[i][c] != 0:
                f = B[i][c]
                B[i] = [a - f * b for a, b in zip(B[i], B[r])]
        pivots.append(c)
        r += 1
        if r == n:
            break
    return n - len(pivots)


cases = [
    ("3I  (repeated, fine)",      mat((3, 0), (0, 3)),  F(3), 2),
    ("[[3,1],[0,3]] (defective)", mat((3, 1), (0, 3)),  F(3), 2),
]
print("%-28s %-10s %-10s %s" % ("matrix", "algebraic", "geometric", "diagonalisable?"))
for name, X, lam, alg in cases:
    g = geo_mult(X, lam)
    print("%-28s %-10d %-10d %s" % (name, alg, g, "yes" if g == alg else "NO"))

print("\nSame characteristic polynomial (3 - L)^2.  Same trace, determinant")
print("and rank.  One diagonalises and one cannot, and the eigenspace")
print("dimension is the only thing that distinguishes them.")
print("\nA defective matrix is not 'nearly' diagonalisable:")
for off in (1, 7, 1000):
    X = mat((3, off), (0, 3))
    print("   [[3,%5d],[0,3]] : geometric multiplicity %d" % (off, geo_mult(X, F(3))))
print("   [[3,    0],[0,3]] : geometric multiplicity %d" % geo_mult(mat((3, 0), (0, 3)), F(3)))
print("There is no continuous transition -- which is why numerical software")
print("does not test for defectiveness.  Week 10 and 11 avoid the question.")


# --------------------------------------------------------------------------
# L23: Fibonacci.
# --------------------------------------------------------------------------

banner("L23: Fibonacci in closed form")

Fib = mat((1, 1), (1, 0))
show("F", Fib, 3)
print("\ntrace 1, det -1  ->  L^2 - L - 1 = 0  ->  L = (1 +- sqrt 5)/2")
phi = (1 + 5 ** 0.5) / 2
psi = (1 - 5 ** 0.5) / 2
print("   phi = %.12f     psi = %.12f" % (phi, psi))
print("\n%4s %12s %20s %14s" % ("k", "F^k[0][1]", "(phi^k - psi^k)/sqrt5", "phi^k/sqrt5"))
for k in (5, 10, 20, 30):
    exact = mpow(Fib, k)[0][1]
    closed = (phi ** k - psi ** k) / 5 ** 0.5
    print("%4d %12s %20.6f %14.6f" % (k, exact, closed, phi ** k / 5 ** 0.5))
print("\nThe closed form is exact -- Binet's formula -- and it is nothing but")
print("A^k = S Lambda^k S^-1 read off in coordinates.  |psi| < 1, so psi^k")
print("dies and F_k grows like phi^k / sqrt 5: the golden ratio is an")
print("eigenvalue, and that is the entire reason it appears here.")


# --------------------------------------------------------------------------
# L23: a Markov chain.
# --------------------------------------------------------------------------

banner("L23: a Markov chain, and why it settles")

P = [[0.9, 0.2],
     [0.1, 0.8]]
show("P (columns sum to 1)", P, 6, lambda v: "%.1f" % v)
print("\ntrace 1.7, det 0.70  ->  L^2 - 1.7L + 0.7 = 0  ->  L = 1 and 0.7")
print("\nlambda = 1 always, for any Markov matrix: the columns summing to 1")
print("says (1,1) is a left eigenvector, and A and A^T share eigenvalues.")
print("\nsteady state from (P - I)v = 0:  v = (2, 1), normalised (2/3, 1/3)")
print("\n%5s  %s" % ("k", "P^k"))
for k in (1, 5, 20, 60):
    Pk = mpow(P, k)
    print("%5d  [[%.6f, %.6f], [%.6f, %.6f]]"
          % (k, Pk[0][0], Pk[0][1], Pk[1][0], Pk[1][1]))
print("\nEvery column converges to (2/3, 1/3) -- the steady state, whatever")
print("you started from.  The rate is governed by the SECOND eigenvalue:")
for k in (5, 20, 60):
    print("   0.7^%-3d = %.3g" % (k, 0.7 ** k))
print("\nSo 'how fast does it mix' is a question about |lambda_2|, and")
print("Week 12's PageRank is this computation on a 10^9 x 10^9 matrix.")


# --------------------------------------------------------------------------
# L23: complex eigenvalues and spirals.
# --------------------------------------------------------------------------

banner("L23: complex eigenvalues -- |lambda| decides everything")

print("%-26s %-22s %-10s %s" % ("matrix", "eigenvalues", "|lambda|", "orbit of a point"))
for name, a, b in [("rotate 30",           math.cos(math.pi/6), math.sin(math.pi/6)),
                   ("rotate 30, x 1.1",    1.1*math.cos(math.pi/6), 1.1*math.sin(math.pi/6)),
                   ("rotate 30, x 0.9",    0.9*math.cos(math.pi/6), 0.9*math.sin(math.pi/6))]:
    modulus = (a*a + b*b) ** 0.5
    fate = "circle" if abs(modulus-1) < 1e-12 else ("spirals OUT" if modulus > 1 else "spirals IN")
    print("%-26s %-22s %-10.4f %s"
          % (name, "%.4f +- %.4fi" % (a, b), modulus, fate))
print("\nA real 2x2 with complex eigenvalues r e^{+- i theta} is a rotation by")
print("theta together with a scaling by r.  It has no real eigenvector, so it")
print("is not diagonalisable over R -- but it IS over C, and the real form")
print("r[[cos,-sin],[sin,cos]] is as close to diagonal as R allows.")
print("\nAfter 24 steps at r = 1.1 a point is %.2f times further out;" % (1.1 ** 24))
print("at r = 0.9 it is %.3f times closer.  Stability is |lambda| < 1," % (0.9 ** 24))
print("and nothing else.")
