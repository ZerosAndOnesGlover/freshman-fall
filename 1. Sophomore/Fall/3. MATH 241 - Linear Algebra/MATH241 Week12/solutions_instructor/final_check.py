#!/usr/bin/env python3
"""MATH 241 Final Examination -- every number in the mark scheme, checked.

INSTRUCTOR ONLY.  Kept in solutions_instructor/ so that no student
resource contains the paper's answers.  Pure Python; exact in Fraction
throughout, except where a question's answer is irrational and says so.
Every `check` is an assertion: if this file runs to the end, the mark
scheme's arithmetic is right.
"""

from fractions import Fraction as F
import math

n_checks = 0


def check(label, cond):
    global n_checks
    assert cond, label
    n_checks += 1
    print(f"  ok  {label}")


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def T(A):
    return [list(r) for r in zip(*A)]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def mv(A, x):
    return [sum(a * b for a, b in zip(r, x)) for r in A]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def det(A):
    M = [r[:] for r in A]
    n, d = len(M), F(1)
    for k in range(n):
        p = next((i for i in range(k, n) if M[i][k] != 0), None)
        if p is None:
            return F(0)
        if p != k:
            M[k], M[p] = M[p], M[k]
            d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            M[i] = [a - f * b for a, b in zip(M[i], M[k])]
    return d


def rank(A):
    M = [r[:] for r in A]
    m, n, r = len(M), len(M[0]), 0
    for c in range(n):
        p = next((i for i in range(r, m) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


print("Q1  elimination and LU")
A = mat((2, 1, -1), (6, 4, 1), (-4, 1, 9))
L = mat((1, 0, 0), (3, 1, 0), (-2, 3, 1))
U = mat((2, 1, -1), (0, 1, 4), (0, 0, -5))
check("A = LU", mul(L, U) == A)
check("det A = -10 = product of pivots", det(A) == -10 == 2 * 1 * -5)
b = [F(-1), F(4), F(13)]
c = [F(-1), F(7), F(-10)]
check("Lc = b with c = (-1, 7, -10)", mv(L, c) == b)
x = [F(1), F(-1), F(2)]
check("Ux = c with x = (1, -1, 2)", mv(U, x) == c)
check("Ax = b", mv(A, x) == b)
eps = 1e-20
m21 = 1 / eps
u22 = 1 - m21 * 1
check("unpivoted [[1e-20,1],[1,1]]: u22 rounds to -1e20 exactly", u22 == -1e20)
x2 = (2 - m21 * 1) / u22
x1 = (1 - x2) / eps
check("unpivoted solve of [[1e-20,1],[1,1]]x=(1,2): x1 = 0.0, x2 = 1.0", x1 == 0.0 and x2 == 1.0)

print("\nQ2  the four subspaces")
B = mat((1, 2, 0, 1), (2, 4, 1, 4), (3, 6, 1, 5))
check("rank B = 2", rank(B) == 2)
for v in ([-2, 1, 0, 0], [-1, 0, -2, 1]):
    check(f"B{v} = 0", mv(B, [F(t) for t in v]) == [0, 0, 0])
check("y = (1,1,-1) gives y^T B = 0", mv(T(B), [F(1), F(1), F(-1)]) == [0, 0, 0, 0])
check("dims 2 + 2 = 4 and 2 + 1 = 3", 2 + 2 == 4 and 2 + 1 == 3)
check("b = (1,1,2) solvable: 1 + 1 - 2 = 0", rank([r + [bb] for r, bb in zip(B, [F(1), F(1), F(2)])]) == 2)
check("b = (1,1,1) not solvable", rank([r + [bb] for r, bb in zip(B, [F(1), F(1), F(1)])]) == 3)
check("row (0,0,1,2) is in the row space", rank(B + [[F(0), F(0), F(1), F(2)]]) == 2)

print("\nQ3  determinants and eigenvalues")
D4 = mat((2, 0, 0, 0), (1, 3, 0, 0), (5, 6, 1, 0), (7, 8, 9, 4))
check("det of the triangular 4x4 = 24", det(D4) == 24)
C = mat((4, 1), (2, 3))
check("det C = 10, trace 7", det(C) == 10 and C[0][0] + C[1][1] == 7)
check("C(1,1) = 5(1,1)", mv(C, [F(1), F(1)]) == [5, 5])
check("C(1,-2) = 2(1,-2)", mv(C, [F(1), F(-2)]) == [2, -4])
Ci = [[C[1][1] / 10, -C[0][1] / 10], [-C[1][0] / 10, C[0][0] / 10]]
check("det(2 C^-1) = 4/10 = 2/5", det([[2 * v for v in r] for r in Ci]) == F(2, 5))
check("eigenvalues of C^3 + I are 126 and 9", 5 ** 3 + 1 == 126 and 2 ** 3 + 1 == 9)
C3I = mul(mul(C, C), C)
C3I = [[C3I[i][j] + (1 if i == j else 0) for j in range(2)] for i in range(2)]
check("det(C^3 + I) = 126 * 9 = 1134", det(C3I) == 1134)

print("\nQ4  diagonalisation and powers")
M = mat((F(4, 5), F(3, 10)), (F(1, 5), F(7, 10)))
check("columns of M sum to 1", all(M[0][j] + M[1][j] == 1 for j in range(2)))
check("M(3,2) = (3,2)", mv(M, [F(3), F(2)]) == [3, 2])
check("M(1,-1) = (1/2)(1,-1)", mv(M, [F(1), F(-1)]) == [F(1, 2), F(-1, 2)])


def Mk(k):
    h = F(1, 2 ** k)
    return [[(3 + 2 * h) / 5, (3 - 3 * h) / 5], [(2 - 2 * h) / 5, (2 + 3 * h) / 5]]


P = eye(2)
for k in range(1, 9):
    P = mul(P, M)
    check(f"closed form for M^{k}", P == Mk(k))
for k in (19, 20):
    E = Mk(k)
    err = max(abs(E[0][0] - F(3, 5)), abs(E[0][1] - F(3, 5)), abs(E[1][0] - F(2, 5)), abs(E[1][1] - F(2, 5)))
    print(f"      k = {k}: max entry error = {float(err):.3e}")
check("k = 20 is the first power within 1e-6", max(abs(Mk(19)[0][1] - F(3, 5)), F(0)) > F(1, 10 ** 6)
      and abs(Mk(20)[0][1] - F(3, 5)) <= F(1, 10 ** 6))
J = mat((3, 1), (0, 3))
check("[[3,1],[0,3]] - 3I has rank 1 (one eigenvector)", rank([[J[i][j] - (3 if i == j else 0) for j in range(2)] for i in range(2)]) == 1)

print("\nQ5  least squares and QR")
ts = [F(-1), F(0), F(1), F(2)]
ys = [F(0), F(1), F(3), F(4)]
Ad = [[F(1), t] for t in ts]
G = mul(T(Ad), Ad)
check("A^T A = [[4,2],[2,6]]", G == mat((4, 2), (2, 6)))
check("A^T y = (8, 11)", mv(T(Ad), ys) == [8, 11])
xh = [F(13, 10), F(7, 5)]
check("normal equations solved by (13/10, 7/5)", mv(G, xh) == [8, 11])
e = [y - p for y, p in zip(ys, mv(Ad, xh))]
check("e = (1/10, -3/10, 3/10, -1/10)", e == [F(1, 10), F(-3, 10), F(3, 10), F(-1, 10)])
check("A^T e = 0", mv(T(Ad), e) == [0, 0])
check("|e|^2 = 1/5", dot(e, e) == F(1, 5))
check("line passes through the centroid (1/2, 2)", xh[0] + xh[1] * F(1, 2) == 2)
w = [F(-3, 2), F(-1, 2), F(1, 2), F(3, 2)]
check("GS: a2 - (a2.q1)q1 = (-3/2,-1/2,1/2,3/2), |.|^2 = 5", w == [t - F(1, 2) for t in ts] and dot(w, w) == 5)
check("Q^T y second entry = 14/(2 sqrt 5) -> d = 7/5", dot([F(-3), F(-1), F(1), F(3)], ys) == 14 and F(14, 2) / 5 == F(7, 5))
check("R x = Q^T y first row: 2c + d = 4", 2 * xh[0] + xh[1] == 4)

print("\nQ6  symmetric and positive definite")
def Sb(bb):
    return mat((2, 1, 0), (1, 2, 1), (0, 1, bb))
check("det S(b) = 3b - 2 at b = 0, 1, 2/3", det(Sb(0)) == -2 and det(Sb(1)) == 1 and det(Sb(F(2, 3))) == 0)
check("leading minors 2 and 3 for every b", det([[F(2)]]) == 2 and det(mat((2, 1), (1, 2))) == 3)
check("S(2/3)(1,-2,3) = 0", mv(Sb(F(2, 3)), [F(1), F(-2), F(3)]) == [0, 0, 0])
Tm = mat((21, -12), (-12, 14))
check("T(3,4) = 5(3,4)", mv(Tm, [F(3), F(4)]) == [15, 20])
check("T(-4,3) = 30(-4,3)", mv(Tm, [F(-4), F(3)]) == [-120, 90])
Q = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
check("T = Q diag(5,30) Q^T exactly", mul(mul(Q, [[F(5), F(0)], [F(0), F(30)]]), T(Q)) == Tm)
P1 = [[F(9, 25), F(12, 25)], [F(12, 25), F(16, 25)]]
P2 = [[F(16, 25), F(-12, 25)], [F(-12, 25), F(9, 25)]]
check("T = 5 P1 + 30 P2", [[5 * P1[i][j] + 30 * P2[i][j] for j in range(2)] for i in range(2)] == Tm)
check("pivots of T are 21 and 50/7", Tm[1][1] - Tm[0][1] ** 2 / Tm[0][0] == F(50, 7))
for xx, yy in ((1, 1), (2, -3), (7, 4)):
    lhs = 21 * xx * xx - 24 * xx * yy + 14 * yy * yy
    rhs = 21 * (xx - F(4, 7) * yy) ** 2 + F(50, 7) * yy * yy
    check(f"21x^2 - 24xy + 14y^2 = sum of squares at ({xx},{yy}) = {lhs}", lhs == rhs)
check("semi-axes 1/sqrt5 and 1/sqrt30, ratio sqrt6 = sqrt(cond)", abs((1 / math.sqrt(5)) / (1 / math.sqrt(30)) - math.sqrt(6)) < 1e-15)

print("\nQ7  the SVD")
A7 = mat((12, 14), (21, 12))
U7 = [[F(3, 5), F(4, 5)], [F(4, 5), F(-3, 5)]]
V7 = [[F(4, 5), F(-3, 5)], [F(3, 5), F(4, 5)]]
S7 = [[F(30), F(0)], [F(0), F(5)]]
check("A^T A = [[585,420],[420,340]]", mul(T(A7), A7) == mat((585, 420), (420, 340)))
check("trace 925 = 900 + 25, det 22500 = 900 * 25", 585 + 340 == 925 and 585 * 340 - 420 ** 2 == 22500)
check("U^T U = I, V^T V = I", mul(T(U7), U7) == eye(2) and mul(T(V7), V7) == eye(2))
check("A = U Sigma V^T exactly", mul(mul(U7, S7), T(V7)) == A7)
check("det U = -1 (a reflection), det V = +1", det(U7) == -1 and det(V7) == 1)
check("det A = -150 = det U * 30 * 5 * det V", det(A7) == -150)
lam = [12 + math.sqrt(294), 12 - math.sqrt(294)]
check(f"eigenvalues of A real: {lam[0]:.6f}, {lam[1]:.6f}", abs(lam[0] * lam[1] + 150) < 1e-9)
check("5 <= |lambda| <= 30 for both", all(5 <= abs(l) <= 30 for l in lam))
A1 = [[F(30) * U7[i][0] * V7[j][0] for j in range(2)] for i in range(2)]
check("A_1 = [[72/5, 54/5], [96/5, 72/5]]", A1 == [[F(72, 5), F(54, 5)], [F(96, 5), F(72, 5)]])
Dm = [[A7[i][j] - A1[i][j] for j in range(2)] for i in range(2)]
check("|A - A_1|_F^2 = 25", sum(v * v for r in Dm for v in r) == 25)
Ap = mul(mul(V7, [[F(1, 30), F(0)], [F(0), F(1, 5)]]), T(U7))
check("A+ = A^-1 (A invertible)", mul(A7, Ap) == eye(2))
check("A+ = (1/150) [[-12, 14], [21, -12]]", Ap == [[F(-12, 150), F(14, 150)], [F(21, 150), F(-12, 150)]])
check("cond_2(A) = 6", F(30, 5) == 6)

print("\nQ8  applications")
pts = [(4, 3), (-4, -3), (4, 3), (-4, -3), (-3, 4), (3, -4)]
check("the six points are centred", sum(p[0] for p in pts) == 0 and sum(p[1] for p in pts) == 0)
DtD = [[sum(F(p[i] * p[j]) for p in pts) for j in range(2)] for i in range(2)]
check("D^T D = [[82,24],[24,68]]", DtD == mat((82, 24), (24, 68)))
check("D^T D (4,3) = 100 (4,3)", mv(DtD, [F(4), F(3)]) == [400, 300])
check("D^T D (-3,4) = 50 (-3,4)", mv(DtD, [F(-3), F(4)]) == [-150, 200])
check("first component explains 2/3 of the variance", F(100, 150) == F(2, 3))
perp = sum(F((-3 * p[0] + 4 * p[1]) ** 2, 25) for p in pts)
check("sum of squared distances to the first-component line = 50", perp == 50)
check("regression slope y on x = 24/82 = 12/41", F(24, 82) == F(12, 41))
Pw = mat((0, 1), (1, 0))
alpha = F(4, 5)
Gw = [[alpha * Pw[i][j] + (1 - alpha) / 2 for j in range(2)] for i in range(2)]
check("damped two-cycle: G(1,-1) = -4/5 (1,-1)", mv(Gw, [F(1), F(-1)]) == [F(-4, 5), F(4, 5)])
check("damped two-cycle: G(1,1)/2 fixed", mv(Gw, [F(1, 2), F(1, 2)]) == [F(1, 2), F(1, 2)])
check("square wave: first term keeps 8/pi^2 = 81.06% of the energy", abs(8 / math.pi ** 2 - 0.8106) < 1e-4)
kept = 8 / math.pi ** 2 * sum(1 / k ** 2 for k in (1, 3, 5))
check(f"square wave: sin t, sin 3t, sin 5t keep {100*kept:.2f}%", abs(kept - 0.9331) < 1e-4)

print(f"\nAll {n_checks} checks passed.")
