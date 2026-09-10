#!/usr/bin/env python3
"""MATH 241 Week 10 -- every number quoted in L30-L32, reproduced.

Pure Python, no dependencies.  Run it:

    python3 symmetric.py

Week 7 diagonalised A = S Lambda S^-1 and found two ways for it to be
worthless: S may not exist, and it may exist with cond(S) = 1.3e8.
Symmetric matrices have neither problem.  This file is the evidence:
the spectral theorem worked out exactly in Fraction on one matrix, the
five tests for positive definiteness agreeing to the exact value of a
parameter, and -- the week's headline -- a measurement of how far
eigenvalues move when you nudge the matrix, symmetric against not.

Exact in Fraction wherever exactness is available.  Float only where
the point is what floating point does, and labelled where it is.
"""

from fractions import Fraction as F
import math
import random

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


# ----------------------------------------------------------------- exact
def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def T(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def is_sym(A):
    return all(A[i][j] == A[j][i] for i in range(len(A)) for j in range(len(A)))


def show(A, name, w=8):
    print(f"  {name} =")
    for row in A:
        print("    [" + " ".join(f"{str(v):>{w}}" for v in row) + "]")


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def outer(u, v):
    return [[a * b for b in v] for a in u]


def pivots(A):
    """Exact pivots of a symmetric matrix, no row exchanges.

    Symmetric positive definite matrices never need them (L32 section 2),
    and for the indefinite examples here the pivots exist anyway.
    """
    n = len(A)
    M = [r[:] for r in A]
    out = []
    for k in range(n):
        out.append(M[k][k])
        if M[k][k] == 0:                      # a zero pivot: elimination stops
            return out
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= f * M[k][j]
    return out


def leading_minors(A):
    return [det(([row[:k + 1] for row in A[:k + 1]])) for k in range(len(A))]


def det(A):
    n = len(A)
    M = [r[:] for r in A]
    d = F(1)
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
            for j in range(k, n):
                M[i][j] -= f * M[k][j]
    return d


# ------------------------------------------------------- float eigen (Jacobi)
def jacobi_eig(Ain, sweeps=100):
    """Eigenvalues and orthonormal eigenvectors of a symmetric matrix.

    Jacobi's method: repeatedly pick an off-diagonal entry and rotate it
    to zero.  Each rotation is orthogonal, so the running product V is
    orthogonal to machine precision by construction -- the L28 argument
    for Householder, applied to the eigenvalue problem.  It works ONLY
    for symmetric matrices, which is the point: there is no comparable
    method in general, and Week 7's failures are why.

    Returns (eigenvalues descending, V) with A = V diag(vals) V^T.
    """
    n = len(Ain)
    A = [[float(v) for v in row] for row in Ain]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    fro = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n)))
    if fro == 0.0:
        return [0.0] * n, V
    for _ in range(sweeps):
        off = math.sqrt(sum(A[i][j] ** 2
                            for i in range(n) for j in range(n) if i != j))
        if off <= 1e-17 * fro:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if A[p][q] == 0.0:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                sgn = 1.0 if theta >= 0 else -1.0
                t = sgn / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):                       # A <- A J
                    kp, kq = A[k][p], A[k][q]
                    A[k][p] = c * kp - s * kq
                    A[k][q] = s * kp + c * kq
                for k in range(n):                       # A <- J^T A
                    pk, qk = A[p][k], A[q][k]
                    A[p][k] = c * pk - s * qk
                    A[q][k] = s * pk + c * qk
                for k in range(n):                       # V <- V J
                    kp, kq = V[k][p], V[k][q]
                    V[k][p] = c * kp - s * kq
                    V[k][q] = s * kp + c * kq
    vals = [A[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: -vals[i])
    return ([vals[i] for i in order],
            [[V[i][o] for o in order] for i in range(n)])


# ============================================================ 1. the matrix
#
# A is built so that the whole week can be done exactly.  Its eigenvectors
# are three integer vectors of equal length 3, mutually perpendicular:
#
#     u1 = (1, 2, 2)   u2 = (2, 1, -2)   u3 = (2, -2, 1)
#
# so Q = [u1 u2 u3]/3 is an orthogonal matrix with RATIONAL entries and
# every identity below is checkable in Fraction with no rounding at all.

A = mat((5, 0, -2), (0, 3, -2), (-2, -2, 4))
U = [(1, 2, 2), (2, 1, -2), (2, -2, 1)]
LAM = [F(1), F(7), F(4)]


def part1():
    banner("1.  THE SPECTRAL THEOREM, EXACTLY  (L30 sections 1-4)")
    show(A, "A", 3)
    print(f"  symmetric: {is_sym(A)}     trace = {sum(A[i][i] for i in range(3))}"
          f"     det = {det(A)}")

    print("\n  Eigenvectors are integer and mutually perpendicular:")
    for u, lam in zip(U, LAM):
        Au = mv(A, [F(c) for c in u])
        print(f"    A{u} = {tuple(str(v) for v in Au)}"
              f"  = {lam} * {u}   -> lambda = {lam}")
    print("\n    pairwise dot products:", end=" ")
    for i in range(3):
        for j in range(i + 1, 3):
            print(f"u{i+1}.u{j+1} = {dot(U[i], U[j])}", end="   ")
    print("\n    lengths:", [math.sqrt(dot(u, u)) for u in U],
          " -- all 3, so Q is rational")

    print(f"\n  sum of eigenvalues = {sum(LAM)} = trace A = "
          f"{sum(A[i][i] for i in range(3))}")
    print(f"  product            = {LAM[0]*LAM[1]*LAM[2]} = det A = {det(A)}")

    Q = [[F(U[j][i], 3) for j in range(3)] for i in range(3)]
    L = [[LAM[i] if i == j else F(0) for j in range(3)] for i in range(3)]
    show(Q, "Q", 6)
    print(f"\n  Q^T Q = I exactly:            {mul(T(Q), Q) == eye(3)}")
    print(f"  Q^-1 = Q^T (no inversion):    {mul(Q, T(Q)) == eye(3)}")
    print(f"  Q Lambda Q^T = A exactly:     {mul(mul(Q, L), T(Q)) == A}")
    print("\n  Every one of those is an EXACT rational identity.  Week 7's")
    print("  A = S Lambda S^-1 needed an inverse; here the inverse is the")
    print("  transpose, and cond(Q) = 1 -- the answer to L22 section 4.")
    return Q, L


# ================================================== 2. spectral decomposition
def part2(Q):
    banner("2.  A AS A SUM OF RANK-ONE PROJECTIONS  (L30 section 5)")
    P = []
    for k in range(3):
        q = [Q[i][k] for i in range(3)]
        P.append(outer(q, q))
    print("  P_k = q_k q_k^T is the projection onto the k-th eigenvector.")
    for k in range(3):
        idem = mul(P[k], P[k]) == P[k]
        symm = is_sym(P[k])
        tr = sum(P[k][i][i] for i in range(3))
        print(f"    P{k+1}:  P^2 = P {idem}    P^T = P {symm}    trace = {tr}"
              f"  (= rank 1)")
    print("\n  Mutually annihilating (they project onto perpendicular lines):")
    for i in range(3):
        for j in range(i + 1, 3):
            z = mul(P[i], P[j])
            print(f"    P{i+1} P{j+1} = 0 : "
                  f"{all(v == 0 for row in z for v in row)}")
    S = [[sum(P[k][i][j] for k in range(3)) for j in range(3)] for i in range(3)]
    print(f"\n  P1 + P2 + P3 = I :            {S == eye(3)}")
    R = [[sum(LAM[k] * P[k][i][j] for k in range(3)) for j in range(3)]
         for i in range(3)]
    print(f"  1*P1 + 7*P2 + 4*P3 = A :      {R == A}")
    print("\n  So a symmetric matrix IS a weighted sum of perpendicular")
    print("  projections.  Week 8's P = A(A^T A)^-1 A^T was one term of this.")


# ========================================= 3. why real, and what breaks it
def part3():
    banner("3.  REAL EIGENVALUES ARE A CONSEQUENCE, NOT A COINCIDENCE  (L30 s.2)")
    print("  Drop symmetry and the reality goes with it.  A quarter turn:")
    R = mat((0, -1), (1, 0))
    show(R, "R", 3)
    print(f"    R^T = -R  (antisymmetric):  {T(R) == [[-v for v in r] for r in R]}")
    print("    char poly  lambda^2 + 1 = 0  ->  lambda = +i, -i")
    print("    No real eigenvector exists: a rotation sends no real")
    print("    direction to a multiple of itself.  Week 6 said so; the")
    print("    point here is that SYMMETRY is what rules this out.")

    print("\n  And the converse of the spectral theorem holds too.  A matrix")
    print("  with an orthonormal eigenbasis and real eigenvalues MUST be")
    print("  symmetric, because A = Q L Q^T gives A^T = Q L^T Q^T = A.")

    print("\n  In 2x2 the whole theorem is one discriminant.  Compare")
    print("      S(e) = [[5, e], [e, 3]]        symmetric")
    print("      B(e) = [[5, e], [-e, 3]]       the same size, not symmetric")
    print("  Both have trace 8; det S = 15 - e^2 and det B = 15 + e^2, so")
    print("      disc S = 64 - 4(15 - e^2) = 4 + 4e^2   -- positive for EVERY e")
    print("      disc B = 64 - 4(15 + e^2) = 4 - 4e^2   -- negative once e > 1\n")
    print("      e      disc S    eigenvalues of S        disc B    "
          "eigenvalues of B")
    for e in (F(0), F(1, 2), F(1), F(2), F(5)):
        ds, db = 4 + 4 * e * e, 4 - 4 * e * e
        rs = [(8 + math.sqrt(float(ds))) / 2, (8 - math.sqrt(float(ds))) / 2]
        if db >= 0:
            rb = f"{(8+math.sqrt(float(db)))/2:.4f}, {(8-math.sqrt(float(db)))/2:.4f}"
        else:
            rb = f"4 +- {math.sqrt(-float(db))/2:.4f} i"
        print(f"    {str(e):>4}   {str(ds):>7}    {rs[0]:7.4f}, {rs[1]:7.4f}"
              f"      {str(db):>7}    {rb}")
    print("\n  disc S = 4 + 4e^2 CANNOT be negative.  That is the 2x2 spectral")
    print("  theorem, and the general proof (L30 section 2) is the same idea")
    print("  written with conjugates instead of a discriminant.")
    print("\n  At e = 1, B has the double eigenvalue 4 and only ONE")
    print("  eigenvector -- Week 7's defect, one entry away from A.")
    Bd = mat((5, 1), (-1, 3))
    M = [[Bd[i][j] - (4 if i == j else 0) for j in range(2)] for i in range(2)]
    print(f"      B(1) - 4I = {[[str(v) for v in r] for r in M]},  "
          f"det = {det(M)},  rank 1  ->  eigenspace has dimension 1")


# ==================================== 4. repeated eigenvalues are still fine
def part4():
    banner("4.  A REPEATED EIGENVALUE IS STILL NOT A DEFECT  (L30 section 6)")
    C = mat((3, 1, 1), (1, 3, 1), (1, 1, 3))
    show(C, "C = 2I + J", 3)
    print("    C(1,1,1) =", tuple(str(v) for v in mv(C, [F(1)] * 3)),
          " -> lambda = 5")
    for v in ((1, -1, 0), (1, 0, -1), (1, 1, -2)):
        print(f"    C{v} = {tuple(str(x) for x in mv(C, [F(c) for c in v]))}"
              f"  -> lambda = 2")
    print("\n  lambda = 2 is a DOUBLE root and its eigenspace is 2-dimensional:")
    print("  the whole plane perpendicular to (1,1,1).  Week 7's defective")
    print("  matrices had a double root and a 1-dimensional eigenspace.")
    print("  That cannot happen here, for any symmetric matrix, ever.")
    print("\n  The eigenvectors within that plane are NOT determined -- (1,-1,0)")
    print("  and (1,0,-1) are both eigenvectors and are not perpendicular")
    print(f"  (dot = {dot((1,-1,0),(1,0,-1))}).  But an ORTHONORMAL pair always")
    print("  exists inside the eigenspace: run Gram-Schmidt (Week 8) on the")
    print("  two you have.")
    g2 = (1, -1, 0)
    # Gram-Schmidt: (1,0,-1) minus its projection on (1,-1,0)
    c = F(dot((1, 0, -1), g2), dot(g2, g2))
    g3 = [F(x) - c * F(y) for x, y in zip((1, 0, -1), g2)]
    print(f"    Gram-Schmidt gives {tuple(str(v) for v in g3)}"
          f"   (i.e. (1,1,-2)/2),  dot with (1,-1,0) = "
          f"{sum(a*F(b) for a, b in zip(g3, g2))}")
    vals, _ = jacobi_eig(C)
    print(f"\n  Jacobi confirms, in floating point: {[round(v, 12) for v in vals]}")


# =============================================== 5. five tests, one threshold
def Ab(b):
    return mat((5, 0, -2), (0, 3, -2), (-2, -2, b))


def part5():
    banner("5.  FIVE TESTS FOR POSITIVE DEFINITE, ONE THRESHOLD  (L31 s.3)")
    print("  A(b) = A with the corner entry replaced by b.  A itself is b = 4.")
    print("  det A(b) = 15b - 32, so the determinant test says b > 32/15.")
    print(f"  32/15 = {float(F(32,15)):.10f}\n")
    print("     b     eigenvalues (Jacobi)                 pivots (exact)"
          "            leading minors  pd?")
    print("  " + "-" * 96)
    for b in (F(1), F(2), F(32, 15) - F(1, 1000), F(32, 15),
              F(32, 15) + F(1, 1000), F(3), F(4)):
        M = Ab(b)
        vals, _ = jacobi_eig(M)
        pv = pivots(M)
        lm = leading_minors(M)
        pd_eig = all(v > 1e-13 for v in vals)
        pd_piv = len(pv) == 3 and all(p > 0 for p in pv)
        pd_min = all(m > 0 for m in lm)
        agree = (pd_eig == pd_piv == pd_min)
        print(f"  {float(b):8.5f} {' '.join(f'{v:9.5f}' for v in vals)}  "
              f"{' '.join(f'{float(p):8.5f}' for p in pv):>28}  "
              f"{' '.join(str(m) for m in lm):>18}  "
              f"{'YES' if pd_eig else 'no':>3}  "
              f"{'all agree' if agree else 'DISAGREE'}")
    print("\n  All three tests flip at exactly b = 32/15, and the exact")
    print("  determinant is what locates it.  At b = 32/15 the matrix is")
    print("  positive SEMI-definite: smallest eigenvalue 0, last pivot 0.")

    print("\n  The other two tests, on A itself (b = 4):")
    xs = [[F(1), F(0), F(0)], [F(1), F(1), F(1)], [F(3), F(-2), F(5)],
          [F(1), F(2), F(2)]]
    for x in xs:
        q = dot(x, mv(A, x))
        print(f"    x = {str(tuple(str(v) for v in x)):<26} x^T A x = {q}")
    print("    (the last is the eigenvector u1, and 9 = 1 * |u1|^2 = 1 * 9)")
    print("\n    A = R^T R with R independent columns: Cholesky, section 7.")


# ============================== 6. pivots, eigenvalues and diagonal entries
def part6():
    banner("6.  PIVOTS, EIGENVALUES, DIAGONAL: SAME SIGNS, DIFFERENT NUMBERS  (L31 s.4)")
    print("  Sylvester's law of inertia: the SIGNS agree.  Nothing else does.\n")
    tests = [("A  (this week's matrix)", A),
             ("[[1,3],[3,1]]", mat((1, 3), (3, 1))),
             ("[[2,-1,0],[-1,2,-1],[0,-1,2]]",
              mat((2, -1, 0), (-1, 2, -1), (0, -1, 2))),
             ("[[1,0],[0,-1]]", mat((1, 0), (0, -1)))]
    for name, M in tests:
        vals, _ = jacobi_eig(M)
        pv = pivots(M)
        dg = [M[i][i] for i in range(len(M))]
        sig = lambda xs: "".join("+" if float(x) > 1e-12 else
                                 ("-" if float(x) < -1e-12 else "0") for x in xs)
        print(f"  {name}")
        print(f"    eigenvalues {[round(v,6) for v in vals]}   signs {sig(vals)}")
        print(f"    pivots      {[str(p) for p in pv]}   signs {sig(pv)}")
        print(f"    diagonal    {[str(d) for d in dg]}   signs {sig(dg)}")
        print(f"    -> signs of pivots match signs of eigenvalues: "
              f"{sig(pv) == sig(vals)}")
        print(f"    -> signs of diagonal match:                     "
              f"{sig(dg) == sig(vals)}\n")
    print("  The third row of the second example is the trap: BOTH diagonal")
    print("  entries are positive and the matrix is indefinite.  Positive")
    print("  diagonal is necessary and nowhere near sufficient.")


# ================================== 7. LDL^T, completing the square, Cholesky
def ldlt(M):
    """Exact LDL^T of a symmetric matrix with nonzero pivots."""
    n = len(M)
    W = [r[:] for r in M]
    L = eye(n)
    for k in range(n):
        for i in range(k + 1, n):
            f = W[i][k] / W[k][k]
            L[i][k] = f
            for j in range(k, n):
                W[i][j] -= f * W[k][j]
    D = [[W[i][j] if i == j else F(0) for j in range(n)] for i in range(n)]
    return L, D


def cholesky(M):
    """A = R^T R for symmetric positive definite M.  Float: sqrt is needed."""
    n = len(M)
    R = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            s = float(M[i][j]) - sum(R[k][i] * R[k][j] for k in range(i))
            if i == j:
                if s <= 0:
                    return None               # not positive definite
                R[i][i] = math.sqrt(s)
            else:
                R[i][j] = s / R[i][i]
    return R


def part7():
    banner("7.  LDL^T IS COMPLETING THE SQUARE; CHOLESKY IS ITS SQUARE ROOT  (L31 s.5, L32 s.2)")
    L, D = ldlt(A)
    show(L, "L", 8)
    show(D, "D", 8)
    print(f"\n  L D L^T = A exactly: {mul(mul(L, D), T(L)) == A}")
    print("  D holds the pivots 5, 3, 28/15 -- Week 5's pivots, unchanged.")
    print("\n  x^T A x = sum d_k (k-th row of L^T times x)^2.  Check at")
    print("  random rational x, exactly:")
    random.seed(241)
    for _ in range(4):
        x = [F(random.randint(-9, 9)) for _ in range(3)]
        lhs = dot(x, mv(A, x))
        y = mv(T(L), x)
        rhs = sum(D[k][k] * y[k] ** 2 for k in range(3))
        print(f"    x = {str(tuple(str(v) for v in x)):<24} x^T A x = "
              f"{str(lhs):>8}   sum d_k y_k^2 = {str(rhs):>8}   "
              f"{'equal' if lhs == rhs else 'DIFFER'}")
    print("\n  Every d_k > 0, so x^T A x is a sum of positive multiples of")
    print("  squares: positive unless every y_k = 0, i.e. unless x = 0.")
    print("  That IS the proof that positive pivots imply positive definite.")

    R = cholesky(A)
    print("\n  Cholesky A = R^T R (float; sqrt is unavoidable):")
    for row in R:
        print("    [" + " ".join(f"{v:12.8f}" for v in row) + "]")
    err = max(abs(sum(R[k][i] * R[k][j] for k in range(3)) - float(A[i][j]))
              for i in range(3) for j in range(3))
    print(f"    max |R^T R - A| = {err:.3e}")
    print(f"    R[0][0] = sqrt(5) = {math.sqrt(5):.10f},   "
          f"R[2][2] = sqrt(28/15) = {math.sqrt(28/15):.10f}")
    print("\n  Cholesky on an INDEFINITE matrix stops rather than lying:")
    print(f"    cholesky([[1,3],[3,1]]) -> {cholesky(mat((1,3),(3,1)))}")
    print("    A negative number under the square root IS the test.")

    print("\n  Cost, in Week 0's units (multiply-subtract pairs, L03 section 2):")
    print("     n     elimination (n^3/3)   Cholesky (n^3/6)     ratio")
    for n in (10, 100, 1000, 5000):
        lu, ch = n ** 3 / 3, n ** 3 / 6
        print(f"    {n:5d}   {lu:17.3e}   {ch:16.3e}     {lu/ch:.1f}")
    print("  Half the work, half the storage, and NO pivoting -- the only")
    print("  factorisation in this course that needs no row exchanges at all.")


# ================================== 8. the quadratic form as an ellipse
def part8():
    banner("8.  x^T A x = 1 IS AN ELLIPSE, AND THE AXES ARE EIGENVECTORS  (L31 s.6)")
    E = mat((5, 4), (4, 5))
    show(E, "E", 3)
    print("    E(1,1)  = (9,9)   -> lambda = 9, axis direction (1,1)/sqrt2")
    print("    E(1,-1) = (1,-1)  -> lambda = 1, axis direction (1,-1)/sqrt2")
    print("\n  x^T E x = 1 is an ellipse with semi-axis 1/sqrt(lambda):")
    for lam, d in ((9, (1, 1)), (1, (1, -1))):
        n = math.sqrt(2)
        r = 1 / math.sqrt(lam)
        x = [r * d[0] / n, r * d[1] / n]
        q = sum(x[i] * sum(float(E[i][j]) * x[j] for j in range(2))
                for i in range(2))
        print(f"    lambda = {lam}:  semi-axis {r:.10f} along {d},"
              f"  x^T E x = {q:.12f}")
    print("\n  Longest axis 1/sqrt(1) = 1 along (1,-1); shortest 1/3 along (1,1).")
    print("  The ratio of axes is sqrt(lambda_max/lambda_min) = 3 = sqrt(cond).")
    print("  A round ellipse means a well-conditioned matrix.  Literally.")


# ====================================== 9. Rayleigh quotient and cond
def part9():
    banner("9.  THE RAYLEIGH QUOTIENT IS TRAPPED BY THE EIGENVALUES  (L32 s.4)")
    vals, V = jacobi_eig(A)
    print(f"  eigenvalues of A: {[round(v, 12) for v in vals]}")
    print("\n  x^T A x / x^T x over 200000 random unit vectors:")
    random.seed(1010)
    lo, hi = float("inf"), float("-inf")
    for _ in range(200000):
        x = [random.gauss(0, 1) for _ in range(3)]
        q = sum(x[i] * sum(float(A[i][j]) * x[j] for j in range(3))
                for i in range(3)) / sum(v * v for v in x)
        lo, hi = min(lo, q), max(hi, q)
    print(f"    observed minimum {lo:.9f}   (lambda_min = {vals[-1]:.9f})")
    print(f"    observed maximum {hi:.9f}   (lambda_max = {vals[0]:.9f})")
    print("    Random sampling gets close and never crosses.  The bounds are")
    print("    attained exactly at the eigenvectors:")
    for k in (0, 2):
        q = [V[i][k] for i in range(3)]
        val = sum(q[i] * sum(float(A[i][j]) * q[j] for j in range(3))
                  for i in range(3))
        print(f"      at eigenvector {k+1}:  x^T A x = {val:.12f}")
    print(f"\n  cond_2(A) = lambda_max / lambda_min = {vals[0]/vals[-1]:.6f}"
          f"   (= 7, exactly)")
    print("  For a symmetric matrix the condition number is READ OFF the")
    print("  eigenvalues.  For a general matrix it is not -- Week 11.")


# ============================ 10. Hilbert: Week 0's matrix, diagnosed
def hilbert(n):
    return [[F(1, i + j + 1) for j in range(n)] for i in range(n)]


def inv_exact(S):
    n = len(S)
    aug = [S[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for k in range(n):
        p = next(i for i in range(k, n) if aug[i][k] != 0)
        aug[k], aug[p] = aug[p], aug[k]
        pv = aug[k][k]
        aug[k] = [v / pv for v in aug[k]]
        for i in range(n):
            if i != k and aug[i][k] != 0:
                f = aug[i][k]
                aug[i] = [a - f * b for a, b in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def norm_inf(S):
    return max(sum(abs(v) for v in row) for row in S)


def part10():
    banner("10.  WEEK 0'S HILBERT MATRIX, NOW DIAGNOSED  (L32 section 5)")
    print("  Week 0 reported cond_inf(H_n) from the exact inverse and could")
    print("  not say WHERE the badness lived.  It lives in lambda_min.\n")
    print("    n   lambda_max      lambda_min       cond_2 = ratio    "
          "cond_inf (exact)")
    print("  " + "-" * 78)
    for n in (3, 5, 8, 10, 12):
        H = hilbert(n)
        vals, _ = jacobi_eig(H)
        c2 = vals[0] / vals[-1]
        ci = norm_inf(H) * norm_inf(inv_exact(H))
        print(f"   {n:3d}   {vals[0]:.8f}   {vals[-1]:.3e}     {c2:.3e}"
              f"       {float(ci):.3e}")
    print("\n  lambda_max barely moves; lambda_min collapses.  H_n is not")
    print("  'nearly singular' in any vague sense -- it has one direction in")
    print("  which it does almost nothing, and the condition number is the")
    print("  ratio.  Every H_n is positive definite (all eigenvalues > 0),")
    print("  so 'positive definite' does NOT mean 'well behaved'.")
    print("\n  cond_2 and cond_inf differ (different norms) and track each")
    print("  other closely.  Week 0 quoted cond_inf; both are right.")
    print("\n  HONESTY ABOUT THE LAST ROW.  lambda_min for H_12 is about")
    print("  1e-17, which is smaller than the rounding error in the stored")
    print("  entries of H_12 itself.  That figure is at the noise floor and")
    print("  its digits are not to be trusted -- only its order of magnitude,")
    print("  which the exactly-computed cond_inf column corroborates.  This")
    print("  is the L03 section 7 warning applied to this very table.")
    print("\n  And H_n is the Gram matrix of 1, x, x^2, ... on [0,1] (Week 9's")
    print("  L29 section 5), i.e. A^T A for polynomial fitting -- symmetric")
    print("  and positive definite by construction, exactly as section 11 says.")


# ================================ 11. A^T A is symmetric positive semidefinite
def part11():
    banner("11.  A^T A IS ALWAYS SYMMETRIC, AND POSITIVE (SEMI)DEFINITE  (L31 s.7)")
    Ms = [("independent columns", mat((1, 0), (1, 1), (1, 2))),
          ("dependent columns   ", mat((1, 2), (1, 2), (1, 2))),
          ("Week 9's fitting A  ", mat((1, 1), (1, 2), (1, 3)))]
    for name, M in Ms:
        G = mul(T(M), M)
        vals, _ = jacobi_eig(G)
        print(f"  {name}   A^T A = {[[str(v) for v in r] for r in G]}")
        print(f"      symmetric {is_sym(G)}   eigenvalues "
              f"{[f'{v:.6f}' for v in vals]}   det = {det(G)}")
        print(f"      -> {'positive definite' if all(v > 1e-12 for v in vals) else 'positive SEMIdefinite (a zero eigenvalue)'}\n")
    print("  x^T (A^T A) x = (Ax).(Ax) = |Ax|^2 >= 0, always.  It is zero")
    print("  exactly when Ax = 0, so A^T A is positive DEFINITE precisely")
    print("  when N(A) = {0} -- independent columns.  That is PS 2 Q5(c),")
    print("  proved in Week 2 and used every week since Week 8.")


# ======================= 12. THE HEADLINE: how far do eigenvalues move?
def part12():
    banner("12.  HOW FAR DO EIGENVALUES MOVE WHEN YOU NUDGE THE MATRIX?  (L32 s.6)")
    print("  SYMMETRIC.  Perturb A by a symmetric E of size delta and watch")
    print("  the eigenvalues.  Weyl's inequality says they move by at most")
    print("  |E|; the measurement says they move by at most |E|.\n")
    base, _ = jacobi_eig(A)
    print("     delta        max |lambda(A+E) - lambda(A)|      ratio to delta")
    random.seed(7)
    for d in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        worst = 0.0
        for _ in range(200):
            E = [[0.0] * 3 for _ in range(3)]
            for i in range(3):
                for j in range(i, 3):
                    E[i][j] = E[j][i] = random.gauss(0, 1)
            s = max(abs(v) for v in jacobi_eig(E)[0])   # |E|_2
            sc = d / s
            B = [[float(A[i][j]) + sc * E[i][j] for j in range(3)]
                 for i in range(3)]
            vals, _ = jacobi_eig(B)
            worst = max(worst, max(abs(a - b) for a, b in zip(vals, base)))
        print(f"    {d:.0e}        {worst:.6e}                  "
              f"{worst/d:.4f}")
    print("\n  The ratio never exceeds 1.  A symmetric eigenvalue problem is")
    print("  PERFECTLY conditioned: the answer moves no further than the")
    print("  question.  No other problem in this course does that.")

    print("\n  " + "-" * 64)
    print("  NOT SYMMETRIC.  Take the n x n matrix C with 1s on the")
    print("  superdiagonal and eps in the bottom-left corner:")
    print("      C^n = eps * I  exactly, so lambda^n = eps and |lambda| =")
    print("      eps^(1/n).  Verified below in Fraction, not estimated.\n")

    def shift(n, eps):
        C = [[F(0)] * n for _ in range(n)]
        for i in range(n - 1):
            C[i][i + 1] = F(1)
        C[n - 1][0] = eps
        return C

    def mpow(M, k):
        R = eye(len(M))
        for _ in range(k):
            R = mul(R, M)
        return R

    print("     n     eps        C^n = eps*I ?     |lambda| = eps^(1/n)   "
          "amplification")
    for n, eps in ((5, F(1, 10 ** 10)), (10, F(1, 10 ** 10)),
                   (10, F(1, 10 ** 16)), (20, F(1, 10 ** 16))):
        C = shift(n, eps)
        ok = mpow(C, n) == [[eps if i == j else F(0) for j in range(n)]
                            for i in range(n)]
        mag = float(eps) ** (1.0 / n)
        print(f"    {n:3d}   1e-{-round(math.log10(float(eps))):<3d}       "
              f"{str(ok):<10}        {mag:.6e}          {mag/float(eps):.3e}")
    print("\n  At n = 10, eps = 1e-10: the matrix is perturbed by 1e-10 and")
    print("  every eigenvalue moves from 0 to magnitude 0.1.  The answer")
    print("  moves a BILLION times further than the question.")
    print("\n  At eps = 0 the matrix is Week 7's worst case -- a single")
    print("  Jordan block, one eigenvalue 0 repeated n times, ONE")
    print("  eigenvector.  Defectiveness and eigenvalue sensitivity are the")
    print("  same phenomenon, and symmetry rules out both at once.")


# =============================== 13. singular values, for Week 11
def part13():
    banner("13.  A PREVIEW: SINGULAR VALUES OF A SYMMETRIC MATRIX  (L32 s.7)")
    for name, M in (("A (eigenvalues 1, 4, 7)", A),
                    ("[[1,3],[3,1]] (eigenvalues 4, -2)", mat((1, 3), (3, 1)))):
        vals, _ = jacobi_eig(M)
        gram, _ = jacobi_eig(mul(T(M), M))
        sig = [math.sqrt(max(v, 0.0)) for v in gram]
        print(f"  {name}")
        print(f"    eigenvalues       {[round(v, 9) for v in vals]}")
        print(f"    sqrt(eig(A^T A))  {[round(v, 9) for v in sig]}")
        print(f"    |eigenvalues|     {sorted((round(abs(v), 9) for v in vals), reverse=True)}\n")
    print("  For a symmetric matrix the singular values are the ABSOLUTE")
    print("  VALUES of the eigenvalues -- the sign is thrown away, because")
    print("  A^T A cannot see it.  Week 11 defines singular values for every")
    print("  matrix, symmetric or not, square or not.")


if __name__ == "__main__":
    Q, L = part1()
    part2(Q)
    part3()
    part4()
    part5()
    part6()
    part7()
    part8()
    part9()
    part10()
    part11()
    part12()
    part13()
    print("\n" + BAR)
    print("Everything above is reproducible.  The Fraction results are exact;")
    print("the float results are what IEEE double precision actually returns.")
    print(BAR)
