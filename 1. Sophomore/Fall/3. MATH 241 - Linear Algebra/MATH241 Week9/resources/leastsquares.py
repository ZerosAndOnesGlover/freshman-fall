#!/usr/bin/env python3
"""MATH 241 Week 9 -- every number quoted in L27-L29, reproduced.

Pure Python, no dependencies.  Run it:

    python3 leastsquares.py

Week 2 said Ax = b has no solution when b is outside C(A) and stopped
there.  Week 8 found the nearest reachable point.  This week does the
arithmetic, and then shows why the obvious way to do it is the wrong
way -- forming A^T A squares the condition number, and on one standard
example it destroys the problem outright.

Exact in Fraction for the fits; float where the point is what floating
point does, and labelled.
"""

from fractions import Fraction as F
import math

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def T(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


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


def vec(v, fmt=str):
    return "(" + ", ".join(fmt(x) for x in v) + ")"


# --------------------------------------------------------------------------
# L27: fitting a line.
# --------------------------------------------------------------------------

banner("L27: the best line through three points that are not collinear")

pts = [(1, 1), (2, 2), (3, 2)]
print("data:", "  ".join("(%d, %d)" % p for p in pts))
print("\nWe want y = c + d x through all three.  Three equations, two")
print("unknowns, and no solution -- the points are not collinear.\n")

A = mat(*[(1, x) for x, _ in pts])
b = [F(y) for _, y in pts]
print("A ="); [print("    ", [str(v) for v in r]) for r in A]
print("b =", vec(b))

AtA = mul(T(A), A)
Atb = mv(T(A), b)
print("\nA^T A =", [[str(v) for v in r] for r in AtA], "   A^T b =", vec(Atb))

xh = mv(inv(AtA), Atb)
print("\nnormal equations give  c = %s,  d = %s" % (xh[0], xh[1]))
print("   best line:  y = %s + %s x" % (xh[0], xh[1]))

p = mv(A, xh)
e = [b[i] - p[i] for i in range(3)]
print("\n   fitted values p = %s" % vec(p))
print("   residuals   e = %s" % vec(e))
print("   ||e||^2 = %s" % sum(x * x for x in e))
print("\n   A^T e = %s   <- the residual is orthogonal to both columns,"
      % vec(mv(T(A), e)))
print("   which is what 'least squares' means: no other line does better.")

print("\nsanity check -- perturb the answer and the error grows:")
for dc, dd in [(F(1, 10), 0), (0, F(1, 10)), (F(-1, 10), F(1, 20))]:
    xx = [xh[0] + dc, xh[1] + dd]
    ee = [b[i] - mv(A, xx)[i] for i in range(3)]
    print("   c%+.2f, d%+.2f -> ||e||^2 = %-10s %s"
          % (float(dc), float(dd), sum(x * x for x in ee),
             "worse" if sum(x * x for x in ee) > sum(x * x for x in e) else "BETTER?!"))


# --------------------------------------------------------------------------
# L28: why not the normal equations.
# --------------------------------------------------------------------------

banner("L28: forming A^T A squares the condition number")

print("The Lauchli matrix:   A = [[1, 1], [eps, 0], [0, eps]]")
print("Its columns are independent for every eps != 0 -- obviously so.\n")
print("A^T A = [[1+eps^2, 1], [1, 1+eps^2]],  det = 2 eps^2 + eps^4\n")

print("%-10s %-22s %-16s %s" % ("eps", "1 + eps^2 as a double", "computed det", "A^T A is"))
for e in (1e-3, 1e-5, 1e-7, 1e-8, 1e-10):
    one = 1.0 + e * e
    d = one * one - 1.0
    print("%-10.0e %-22.17g %-16.3g %s"
          % (e, one, d, "SINGULAR" if d == 0.0 else "fine"))

print("\nmachine epsilon is %.3g, so 1 + eps^2 rounds to 1 once eps < %.2e."
      % (2.0 ** -52, math.sqrt(2.0 ** -52)))
print("\nAt eps = 1e-8 the matrix A^T A is EXACTLY singular in floating point,")
print("while A itself has two obviously independent columns.  Forming A^T A")
print("destroyed the problem.  Nothing is wrong with the data; the method")
print("threw the information away.")

print("\nWhy: cond(A^T A) = cond(A)^2.")
print("%-10s %-16s %-16s" % ("eps", "cond(A)  approx", "cond(A^T A)"))
for e in (1e-3, 1e-5, 1e-7):
    ca = math.sqrt(2.0) / e          # the two singular values are sqrt2 and eps
    print("%-10.0e %-16.3g %-16.3g" % (e, ca, ca * ca))
print("\nSo a problem you could solve to 8 digits becomes one you cannot")
print("solve at all, purely by choosing the wrong algorithm.")


banner("L28: the QR route, which never forms A^T A")

print("Substituting A = QR into A^T A x = A^T b:")
print("   (QR)^T (QR) x = (QR)^T b")
print("   R^T (Q^T Q) R x = R^T Q^T b        and Q^T Q = I")
print("   R^T R x = R^T Q^T b                and R^T is invertible")
print("   ==> R x = Q^T b                    <- a triangular solve\n")


def mgs_solve(cols, b):
    """Least squares by modified Gram-Schmidt QR -- Week 8's L26 SS3."""
    Q, n = [], len(cols)
    R = [[0.0] * n for _ in range(n)]
    for j in range(n):
        w = cols[j][:]
        for i, q in enumerate(Q):
            R[i][j] = sum(x * y for x, y in zip(q, w))
            w = [x - R[i][j] * qi for x, qi in zip(w, q)]
        R[j][j] = math.sqrt(sum(x * x for x in w))
        Q.append([x / R[j][j] for x in w])
    qtb = [sum(q[i] * b[i] for i in range(len(b))) for q in Q]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (qtb[i] - sum(R[i][j] * x[j] for j in range(i + 1, n))) / R[i][i]
    return x


def householder_solve(cols, b):
    """Least squares by Householder QR -- what LAPACK actually does.

    Q is never formed.  Each step reflects the working matrix and the
    right-hand side together, and the reflections are orthogonal to
    machine precision by construction, so nothing can drift.
    """
    m, n = len(cols[0]), len(cols)
    A = [[cols[j][i] for j in range(n)] for i in range(m)]
    rhs = b[:]
    for k in range(n):
        x = [A[i][k] for i in range(k, m)]
        nx = math.sqrt(sum(v * v for v in x))
        if nx == 0:
            continue
        alpha = -nx if x[0] >= 0 else nx      # sign chosen to avoid cancellation
        v = x[:]
        v[0] -= alpha
        nv = math.sqrt(sum(t * t for t in v))
        if nv == 0:
            continue
        v = [t / nv for t in v]
        for j in range(k, n):                 # apply I - 2vv^T
            sdot = sum(v[i - k] * A[i][j] for i in range(k, m))
            for i in range(k, m):
                A[i][j] -= 2 * sdot * v[i - k]
        sdot = sum(v[i - k] * rhs[i] for i in range(k, m))
        for i in range(k, m):
            rhs[i] -= 2 * sdot * v[i - k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (rhs[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x


print("Three methods on the Lauchli least-squares problem, exact answer")
print("x1 = x2 = 1/(2 + eps^2).  Reported: x1.\n")
print("%-8s %-20s %-20s %-20s %s"
      % ("eps", "normal equations", "Gram-Schmidt QR", "Householder QR", "exact"))
for e in (1e-3, 1e-5, 1e-7, 1e-8, 1e-10):
    cols = [[1.0, e, 0.0], [1.0, 0.0, e]]
    rhs = [1.0, 0.0, 0.0]
    exact = 1.0 / (2.0 + e * e)
    a11 = 1.0 + e * e
    det = a11 * a11 - 1.0
    ne = "FAILED (singular)" if det == 0 else "%.9f" % ((a11 - 1.0) / det)
    g = mgs_solve(cols, rhs)
    h = householder_solve(cols, rhs)
    print("%-8.0e %-20s %-20.9f %-20.9f %.9f" % (e, ne, g[0], h[0], exact))

print("\nThree methods, three different failure points.")
print("\n  Normal equations  die at eps = 1e-8, when A^T A goes exactly")
print("                    singular.  Their good values above are LUCK:")
print("                    cond(A^T A) is already 2e14 at eps = 1e-7.")
print("  Gram-Schmidt QR   degrades from eps = 1e-5 and is useless by 1e-7,")
print("                    because the columns are nearly dependent and the")
print("                    subtractions cancel -- Week 8's L26 SS5, measured.")
print("  Householder QR    is right to nine digits throughout.")
print("\nSo 'use QR instead of the normal equations' is not enough advice.")
print("It matters WHICH QR, and Week 8's L26 SS5 said so: Gram-Schmidt is")
print("the right thing to understand and the wrong thing to run.  LAPACK's")
print("dgels uses Householder, and this table is why.")


# --------------------------------------------------------------------------
# L29: fitting a parabola, and what least squares assumes.
# --------------------------------------------------------------------------

banner("L29: the same machinery fits anything linear in the parameters")

pts2 = [(0, 1), (1, 3), (2, 7), (3, 13)]
print("data:", "  ".join("(%d, %d)" % p for p in pts2))
print("\nFit y = c0 + c1 x + c2 x^2.  Still LINEAR least squares: the model")
print("is nonlinear in x and linear in the unknowns c, which is all that")
print("matters.  The columns are 1, x, x^2 evaluated at the data points.\n")

A2 = mat(*[(1, x, x * x) for x, _ in pts2])
b2 = [F(y) for _, y in pts2]
print("A ="); [print("    ", [str(v) for v in r]) for r in A2]

AtA2 = mul(T(A2), A2)
xh2 = mv(inv(AtA2), mv(T(A2), b2))
print("\nbest fit: y = %s + %s x + %s x^2" % (xh2[0], xh2[1], xh2[2]))
p2 = mv(A2, xh2)
e2 = [b2[i] - p2[i] for i in range(4)]
print("   residuals = %s   ||e||^2 = %s" % (vec(e2), sum(x * x for x in e2)))
print("   A^T e = %s" % vec(mv(T(A2), e2)))


banner("L29: one outlier moves the whole line")

base = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
print("Five points exactly on y = x.  Fit a line, then move ONE point.\n")
print("%-28s %-22s %s" % ("data change", "fitted line", "||e||^2"))
for label, pts3 in [("none", base),
                    ("(5,5) -> (5,7)", base[:4] + [(5, 7)]),
                    ("(5,5) -> (5,15)", base[:4] + [(5, 15)])]:
    A3 = mat(*[(1, x) for x, _ in pts3])
    b3 = [F(y) for _, y in pts3]
    c = mv(inv(mul(T(A3), A3)), mv(T(A3), b3))
    p3 = mv(A3, c)
    e3 = [b3[i] - p3[i] for i in range(len(pts3))]
    print("%-28s y = %-6s + %-6s x  %s"
          % (label, c[0], c[1], sum(x * x for x in e3)))

print("\nMoving one point by 10 changes the slope from 1 to %s."
      % mv(inv(mul(T(mat(*[(1, x) for x, _ in base[:4] + [(5, 15)]])),
                   mat(*[(1, x) for x, _ in base[:4] + [(5, 15)]]))),
            mv(T(mat(*[(1, x) for x, _ in base[:4] + [(5, 15)]])),
               [F(y) for _, y in base[:4] + [(5, 15)]]))[1])
print("Least squares minimises the SQUARE of the error, so a residual of")
print("10 counts a hundred times a residual of 1.  That is a modelling")
print("choice, not a law, and it is the choice that makes outliers loud.")
