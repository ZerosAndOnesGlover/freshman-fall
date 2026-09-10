#!/usr/bin/env python3
"""MATH 241 Week 11 -- every number quoted in L33-L35, reproduced.

Pure Python, no dependencies.  Run it:

    python3 svd.py

Week 10 factored symmetric matrices as Q Lambda Q^T and needed that one
hypothesis.  This week drops it.  Every matrix -- rectangular, singular,
non-symmetric, anything -- is U Sigma V^T, and the price is using a
different orthonormal basis at the input and at the output.

Three matrices below were built so that their SVDs are RATIONAL, and
those are checked exactly in Fraction.  Everything else is computed by a
one-sided Jacobi SVD written out in full, in float, and says so.
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


def zeros(m, n):
    return [[F(0)] * n for _ in range(m)]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def show(A, name, w=8):
    print(f"  {name} =")
    for row in A:
        print("    [" + " ".join(f"{str(v):>{w}}" for v in row) + "]")


def cols_to_mat(cols, scale=1):
    """Columns given as integer tuples, divided by `scale`."""
    return [[F(c[i], scale) for c in cols] for i in range(len(cols[0]))]


def rank_exact(A):
    M = [r[:] for r in A]
    m, n = len(M), len(M[0])
    r = 0
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


def inv(S):
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


# ------------------------------------------------ float SVD (one-sided Jacobi)
def fl(A):
    return [[float(v) for v in row] for row in A]


def svd(Ain, count=None):
    """Thin SVD of an m x n float matrix: A = U diag(s) V^T.

    One-sided Jacobi (Hestenes, 1958).  Rotate pairs of columns of A
    until every pair is orthogonal.  What is left is A V = U Sigma: the
    column norms are the singular values and the normalised columns are
    U.  Every step is a plane rotation, so V is orthogonal by
    construction -- the same reason Week 9's Householder QR and Week 10's
    Jacobi eigenvalue method never drift.

    Works for m < n by factoring the transpose.  Singular values come
    back in descending order; a zero singular value gets a zero column in
    U, which complete() fills in when a full basis is wanted.
    `count`, if given, is a one-element list accumulating the number of
    floating-point multiply-adds spent -- a deterministic cost measure.
    """
    m, n = len(Ain), len(Ain[0])
    if m < n:
        s, U, V = svd(T(Ain), count)
        return s, V, U
    W = [[float(v) for v in row] for row in Ain]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(80):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                a = sum(W[i][p] * W[i][p] for i in range(m))
                b = sum(W[i][q] * W[i][q] for i in range(m))
                g = sum(W[i][p] * W[i][q] for i in range(m))
                if count is not None:
                    count[0] += 3 * m
                if g == 0.0 or abs(g) <= 1e-15 * math.sqrt(a * b):
                    continue
                rotated = True
                zeta = (b - a) / (2.0 * g)
                t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                for i in range(m):
                    wp, wq = W[i][p], W[i][q]
                    W[i][p] = c * wp - s * wq
                    W[i][q] = s * wp + c * wq
                for i in range(n):
                    vp, vq = V[i][p], V[i][q]
                    V[i][p] = c * vp - s * vq
                    V[i][q] = s * vp + c * vq
                if count is not None:
                    count[0] += 2 * m + 2 * n
        if not rotated:
            break
    sig = [math.sqrt(sum(W[i][j] ** 2 for i in range(m))) for j in range(n)]
    order = sorted(range(n), key=lambda j: -sig[j])
    s_out = [sig[j] for j in order]
    top = s_out[0] if s_out and s_out[0] > 0 else 1.0
    U = [[(W[i][j] / sig[j]) if sig[j] > 1e-300 * top and sig[j] > 0 else 0.0
          for j in order] for i in range(m)]
    V = [[V[i][j] for j in order] for i in range(n)]
    return s_out, U, V


def complete(U, k):
    """Extend the first k columns of U (orthonormal) to a full basis."""
    m = len(U)
    basis = [[U[i][j] for i in range(m)] for j in range(k)]
    for e in range(m):
        v = [1.0 if i == e else 0.0 for i in range(m)]
        for b in basis:
            d = sum(x * y for x, y in zip(v, b))
            v = [x - d * y for x, y in zip(v, b)]
        nv = math.sqrt(sum(x * x for x in v))
        if nv > 1e-8:
            basis.append([x / nv for x in v])
        if len(basis) == m:
            break
    return [[basis[j][i] for j in range(m)] for i in range(m)]


def recon(s, U, V, r=None):
    r = len(s) if r is None else r
    m, n = len(U), len(V)
    return [[sum(s[k] * U[i][k] * V[j][k] for k in range(r)) for j in range(n)]
            for i in range(m)]


def maxabs(A, B):
    return max(abs(float(a) - float(b)) for ra, rb in zip(A, B)
               for a, b in zip(ra, rb))


def fro(A):
    return math.sqrt(sum(float(v) ** 2 for row in A for v in row))


def norm2(A):
    return svd(A)[0][0]


# ============================================================ the matrices
#
# Each is U Sigma V^T with U and V built from integer vectors of equal
# length, so that U and V are rational.  They were chosen backwards -- the
# SVD first, the matrix second -- and L33 section 3 says so.

# 2 x 2, not symmetric.  sigma = 20, 5.
A2 = mat((12, 11), (4, 12))
A2_U = [(4, 3), (-3, 4)]            # /5
A2_V = [(3, 4), (-4, 3)]            # /5
A2_S = [20, 5]

# 3 x 2, rectangular.  sigma = 25, 20.
B = mat((9, 12), (12, 16), (-16, 12))
B_U = [(3, 4, 0), (0, 0, 5), (-4, 3, 0)]     # /5
B_V = [(3, 4), (-4, 3)]                       # /5
B_S = [25, 20]

# 3 x 3, rank 2.  sigma = 18, 9, 0.
M = mat((6, 0, 6), (9, 6, 6), (6, 12, 0))
M_U = [(1, 2, 2), (2, 1, -2), (2, -2, 1)]    # /3
M_V = [(2, 2, 1), (1, -2, 2), (2, -1, -2)]   # /3
M_S = [18, 9, 0]


def exact_svd(A, Uc, uscale, S, Vc, vscale):
    m, n = len(A), len(A[0])
    U = cols_to_mat(Uc, uscale)
    V = cols_to_mat(Vc, vscale)
    Sig = zeros(m, n)
    for k, sk in enumerate(S):
        Sig[k][k] = F(sk)
    return U, Sig, V


# ============================================= 1. the SVD, exactly, three times
def part1():
    banner("1.  A = U Sigma V^T, CHECKED EXACTLY  (L33 section 3)")
    for name, A, Uc, us, S, Vc, vs in (
            ("A (2x2, not symmetric)", A2, A2_U, 5, A2_S, A2_V, 5),
            ("B (3x2, rectangular)", B, B_U, 5, B_S, B_V, 5),
            ("M (3x3, rank 2)", M, M_U, 3, M_S, M_V, 3)):
        U, Sig, V = exact_svd(A, Uc, us, S, Vc, vs)
        print(f"\n  {name}")
        show(A, "matrix", 5)
        print(f"    U^T U = I : {mul(T(U), U) == eye(len(U))}"
              f"     V^T V = I : {mul(T(V), V) == eye(len(V))}")
        print(f"    U Sigma V^T = matrix, exactly : {mul(mul(U, Sig), T(V)) == A}")
        print(f"    singular values {S}")
        for k, sk in enumerate(S):
            v = [V[i][k] for i in range(len(V))]
            u = [U[i][k] for i in range(len(U))]
            Av = mv(A, v)
            print(f"      A v{k+1} = {[str(x) for x in Av]}"
                  f"  = {sk} * u{k+1} : {Av == [sk * x for x in u]}")

    print("\n  The eigenvalues of A are NOT its singular values:")
    tr, dt = F(24), 12 * 12 - 11 * 4
    disc = tr * tr - 4 * dt
    print(f"    trace 24, det {dt}, eigenvalues 12 +- sqrt({disc/4})"
          f" = {12 + math.sqrt(disc/4):.6f}, {12 - math.sqrt(disc/4):.6f}")
    print("    singular values 20, 5.  Products agree (both 100 = |det|);")
    print("    nothing else does.  Only a symmetric positive semidefinite")
    print("    matrix has the two lists equal (Week 10's L32 section 7).")


# ============================================= 2. built from A^T A and A A^T
def part2():
    banner("2.  WHERE IT COMES FROM: A^T A AND A A^T  (L33 section 2)")
    G = mul(T(B), B)
    H = mul(B, T(B))
    show(G, "B^T B (2x2)", 6)
    show(H, "B B^T (3x3)", 6)
    V = cols_to_mat(B_V, 5)
    U = cols_to_mat(B_U, 5)
    for k, sk in enumerate(B_S):
        v = [V[i][k] for i in range(2)]
        u = [U[i][k] for i in range(3)]
        print(f"    B^T B v{k+1} = {sk*sk} v{k+1} : {mv(G, v) == [sk*sk*x for x in v]}"
              f"      B B^T u{k+1} = {sk*sk} u{k+1} : {mv(H, u) == [sk*sk*x for x in u]}")
    u3 = [U[i][2] for i in range(3)]
    print(f"    B B^T u3 = 0 : {mv(H, u3) == [0, 0, 0]}   (the extra eigenvalue is 0)")
    print(f"\n    trace B^T B = {G[0][0]+G[1][1]} = 625 + 400"
          f"      trace B B^T = {H[0][0]+H[1][1]+H[2][2]} = 625 + 400 + 0")
    print("  Same nonzero eigenvalues, different sizes.  The bigger one pads")
    print("  with zeros.  Both are symmetric PSD, so Week 10 applies to both.")


# ============================================= 3. geometry: circle -> ellipse
def part3():
    banner("3.  THE UNIT CIRCLE GOES TO AN ELLIPSE  (L33 section 4)")
    A = fl(A2)
    lo, hi, argmax = float("inf"), 0.0, None
    N = 360000
    for k in range(N):
        th = 2 * math.pi * k / N
        x = (math.cos(th), math.sin(th))
        y = (A[0][0] * x[0] + A[0][1] * x[1], A[1][0] * x[0] + A[1][1] * x[1])
        r = math.hypot(*y)
        if r > hi:
            hi, argmax = r, x
        lo = min(lo, r)
    print(f"  max |Ax| over the unit circle = {hi:.9f}   (sigma1 = 20)")
    print(f"  min |Ax| over the unit circle = {lo:.9f}   (sigma2 = 5)")
    print(f"  attained at x = ({argmax[0]:.6f}, {argmax[1]:.6f})"
          f"   (v1 = (0.6, 0.8))")
    print("\n  So |A|_2 = sigma1 = 20.  Compare the other candidates:")
    print(f"    largest entry            = 12")
    print(f"    Frobenius norm           = sqrt(425) = {math.sqrt(425):.6f}"
          f" = sqrt(20^2 + 5^2)")
    lam = 12 + math.sqrt(44)
    print(f"    largest |eigenvalue|     = {lam:.6f}")
    print("  Only sigma1 is the most that A can stretch a vector.")
    print("\n  Rotation, stretch, rotation.  V^T turns v1, v2 onto the axes;")
    print("  Sigma stretches by 20 and 5; U turns the axes onto u1, u2.")
    V = cols_to_mat(A2_V, 5)
    U = cols_to_mat(A2_U, 5)
    print(f"    det V = {V[0][0]*V[1][1]-V[0][1]*V[1][0]}"
          f"   det U = {U[0][0]*U[1][1]-U[0][1]*U[1][0]}"
          f"   (both +1: rotations, no reflection)")
    ang = lambda Q: math.degrees(math.atan2(float(Q[1][0]), float(Q[0][0])))
    print(f"    V rotates by {ang(V):.4f} deg, U by {ang(U):.4f} deg")


# ==================================== 4. the four subspaces, all at once
def part4():
    banner("4.  FOUR SUBSPACES, FOUR ORTHONORMAL BASES, ONE FACTORISATION  (L34 s.1)")
    U = cols_to_mat(M_U, 3)
    V = cols_to_mat(M_V, 3)
    show(M, "M", 4)
    r = rank_exact(M)
    print(f"  rank by elimination = {r};   nonzero singular values: 18, 9  -> 2")
    u = [[U[i][k] for i in range(3)] for k in range(3)]
    v = [[V[i][k] for i in range(3)] for k in range(3)]
    Mt = T(M)
    print("\n    C(M)   = span{u1, u2}:  M v1 = 18 u1, M v2 = 9 u2   (above)")
    print(f"    N(M^T) = span{{u3}}:     M^T u3 = {[str(x) for x in mv(Mt, u[2])]}")
    print(f"    C(M^T) = span{{v1, v2}}: M^T u1 = {[str(x) for x in mv(Mt, u[0])]}"
          f" = 18 v1 : {mv(Mt, u[0]) == [18*x for x in v[0]]}")
    print(f"    N(M)   = span{{v3}}:     M v3   = {[str(x) for x in mv(M, v[2])]}")
    print("\n  Orthogonality is automatic -- the bases come from orthogonal U, V:")
    print(f"    u1.u3 = {dot(u[0], u[2])}, u2.u3 = {dot(u[1], u[2])},"
          f"  v1.v3 = {dot(v[0], v[2])}, v2.v3 = {dot(v[1], v[2])}")
    print("\n  Row rank = column rank, EXPLAINED rather than proved:")
    print("    M v_k = sigma_k u_k  and  M^T u_k = sigma_k v_k.  The same")
    print("    sigma_k pairs one row-space direction with one column-space")
    print("    direction.  Nonzero sigmas come in matched pairs, so the two")
    print("    dimensions are the same count.")

    print("\n  Week 3's L12 section 4 matrix, run through the float SVD:")
    W3 = mat((1, 3, 3, 2), (2, 6, 9, 7), (-1, -3, 3, 4))
    s, _, _ = svd(fl(W3))
    print(f"    [[1,3,3,2],[2,6,9,7],[-1,-3,3,4]]  (rank by elimination {rank_exact(W3)})")
    print(f"    singular values {[f'{x:.6g}' for x in s]}")
    print("    Two singular values, then rounding noise.  Four columns in R^3,")
    print("    three rows in R^4, and one count of nonzero sigmas for both.")


# ================================================== 5. norms and cond
def part5():
    banner("5.  NORMS, CONDITION NUMBERS, AND WEEK 9'S SQUARING  (L34 s.2)")
    for name, A, S in (("A", A2, A2_S), ("B", B, B_S), ("M", M, M_S)):
        f2 = sum(v * v for row in A for v in row)
        print(f"  {name}: |.|_F^2 = {f2} = sum sigma^2 = {sum(x*x for x in S)}"
              f"    |.|_2 = sigma1 = {S[0]}")
    print("\n  cond_2 = sigma_max / sigma_min:")
    print("    A: 20/5 = 4      B: 25/20 = 1.25      M: 18/0 -> infinite (singular)")
    print("\n  A^T A has singular values sigma^2, so cond(A^T A) = cond(A)^2:")
    s, _, _ = svd(fl(mul(T(A2), A2)))
    print(f"    singular values of A^T A: {[round(x, 9) for x in s]}"
          f"   cond = {s[0]/s[1]:.9f} = 4^2")
    print("  Week 9's L28 section 1 asserted this.  It is now one line:")
    print("  A^T A = V Sigma^T U^T U Sigma V^T = V (Sigma^T Sigma) V^T.")

    print("\n  Lauchli again (Week 9), singular values of A and A^T A:")
    for e in (1e-4, 1e-7, 1e-8):
        L = [[1.0, 1.0], [e, 0.0], [0.0, e]]
        sA, _, _ = svd(L)
        G = [[1 + e * e, 1.0], [1.0, 1 + e * e]]
        sG, _, _ = svd(G)
        print(f"    eps={e:.0e}  sigma(A) = {sA[0]:.6f}, {sA[1]:.3e}"
              f"   cond(A) = {sA[0]/sA[1]:.3e}"
              f"   computed sigma_min(A^T A) = {sG[1]:.3e}")
    print("  At 1e-8, sigma_min(A) = 1e-8 is perfectly representable.  Its")
    print("  square, 1e-16, is below the rounding in 1 + eps^2, and A^T A's")
    print("  smallest singular value comes out as exactly 0.")


# ============================================= 6. the pseudoinverse
def part6():
    banner("6.  THE PSEUDOINVERSE  (L34 section 3)")
    U = cols_to_mat(M_U, 3)
    V = cols_to_mat(M_V, 3)
    Sp = zeros(3, 3)
    Sp[0][0], Sp[1][1] = F(1, 18), F(1, 9)
    Mp = mul(mul(V, Sp), T(U))
    show(Mp, "M+ = V Sigma+ U^T", 8)
    print("  The four Penrose conditions, exactly:")
    print(f"    M M+ M  = M    : {mul(mul(M, Mp), M) == M}")
    print(f"    M+ M M+ = M+   : {mul(mul(Mp, M), Mp) == Mp}")
    P1, P2 = mul(M, Mp), mul(Mp, M)
    print(f"    (M M+)^T = M M+ : {T(P1) == P1}")
    print(f"    (M+ M)^T = M+ M : {T(P2) == P2}")
    show(P1, "M M+  (projection onto C(M))", 7)
    print(f"    (M M+)^2 = M M+ : {mul(P1, P1) == P1}    trace = {sum(P1[i][i] for i in range(3))}")
    show(P2, "M+ M  (projection onto C(M^T))", 7)
    print(f"    (M+ M)^2 = M+ M : {mul(P2, P2) == P2}    trace = {sum(P2[i][i] for i in range(3))}")
    print("\n  M has no inverse.  M+ inverts it where it can -- on the row")
    print("  space -- and sends the rest to zero.  Week 8's projections are")
    print("  M M+ and M+ M.")


# ============================== 7. least squares with dependent columns
def rank_factor_pinv(A):
    """Exact pseudoinverse via a full-rank factorisation A = C R.

    C = pivot columns of A, R = nonzero rows of rref(A).  Then
    A+ = R^T (R R^T)^-1 (C^T C)^-1 C^T, all rational.
    """
    m, n = len(A), len(A[0])
    Rr = [r[:] for r in A]
    piv, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, m) if Rr[i][c] != 0), None)
        if p is None:
            continue
        Rr[r], Rr[p] = Rr[p], Rr[r]
        pv = Rr[r][c]
        Rr[r] = [x / pv for x in Rr[r]]
        for i in range(m):
            if i != r and Rr[i][c] != 0:
                f = Rr[i][c]
                Rr[i] = [a - f * b for a, b in zip(Rr[i], Rr[r])]
        piv.append(c)
        r += 1
    C = [[A[i][c] for c in piv] for i in range(m)]
    R = Rr[:r]
    return mul(mul(T(R), inv(mul(R, T(R)))), mul(inv(mul(T(C), C)), T(C)))


def part7():
    banner("7.  LEAST SQUARES WHEN THE COLUMNS ARE DEPENDENT  (L34 section 4)")
    print("  Week 9's L27 section 6: two predictors that say the same thing.")
    print("  x = years of schooling, and age on leaving school = x + 5 for a")
    print("  cohort that all started at five.  Columns 1, x, x + 5:")
    xs = [8, 10, 12, 16]
    ys = [F(30), F(34), F(41), F(52)]
    A = [[F(1), F(x), F(x + 5)] for x in xs]
    show(A, "A", 4)
    G = mul(T(A), A)
    detG = (G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1])
            - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0])
            + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0]))
    print(f"  rank A = {rank_exact(A)},  det(A^T A) = {detG}  -> normal equations singular")
    Ap = rank_factor_pinv(A)
    xp = mv(Ap, ys)
    print(f"\n  x+ = A+ b = {[str(v) for v in xp]}")
    p = mv(A, xp)
    e = [y - q for y, q in zip(ys, p)]
    print(f"  fitted p  = {[str(v) for v in p]}")
    print(f"  A^T e     = {[str(v) for v in mv(T(A), e)]}   (still orthogonal)")
    # other minimisers: add any multiple of the null vector (5, 1, -1)
    nvec = [F(5), F(1), F(-1)]
    print(f"  null vector (5, 1, -1): A(5,1,-1) = {[str(v) for v in mv(A, nvec)]}")
    print("\n  Every x+ + t(5,1,-1) fits equally well.  Their lengths:")
    for t in (F(-2), F(-1), F(0), F(1), F(2)):
        x = [a + t * b for a, b in zip(xp, nvec)]
        print(f"    t = {str(t):>3}   |x|^2 = {float(dot(x, x)):12.6f}"
              f"   residual^2 = {float(dot(e, e)):.6f}")
    print(f"  x+ . (5,1,-1) = {dot(xp, nvec)}  -> x+ lies in the row space, so")
    print("  it is the SHORTEST minimiser.  That is what A+ picks.")
    s, U, V = svd(fl(A))
    print(f"\n  float SVD: singular values {[f'{v:.6g}' for v in s]}")
    tol = max(len(A), len(A[0])) * 2.2e-16 * s[0]
    x = [0.0] * 3
    for k in range(3):
        if s[k] > tol:
            c = sum(U[i][k] * float(ys[i]) for i in range(4)) / s[k]
            for j in range(3):
                x[j] += c * V[j][k]
    print(f"  truncating sigma below {tol:.2e}: x = {[round(v, 9) for v in x]}")
    print(f"  exact x+ as floats          : {[round(float(v), 9) for v in xp]}")


# =========================================== 8. numerical rank
def part8():
    banner("8.  NUMERICAL RANK: ELIMINATION COUNTS PIVOTS, THE SVD MEASURES  (L34 s.5)")
    random.seed(11)
    n = 6
    a = [[random.randint(-5, 5) for _ in range(n)] for _ in range(2)]
    b = [[random.randint(-5, 5) for _ in range(n)] for _ in range(2)]
    R2 = [[a[0][i] * b[0][j] + a[1][i] * b[1][j] for j in range(n)] for i in range(n)]
    print("  R = a1 b1^T + a2 b2^T, a 6x6 integer matrix of rank exactly 2.")
    print(f"  exact rank = {rank_exact([[F(v) for v in r] for r in R2])}")
    E = [[random.gauss(0, 1) * 1e-10 for _ in range(n)] for _ in range(n)]
    X = [[R2[i][j] + E[i][j] for j in range(n)] for i in range(n)]
    # partial-pivoting elimination in float, count nonzero pivots
    W = [r[:] for r in X]
    piv = []
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(W[i][k]))
        W[k], W[p] = W[p], W[k]
        piv.append(W[k][k])
        if W[k][k] == 0.0:
            continue
        for i in range(k + 1, n):
            f = W[i][k] / W[k][k]
            for j in range(k, n):
                W[i][j] -= f * W[k][j]
    print("\n  Add noise of size 1e-10 (a measurement, a rounding, anything):")
    print(f"    pivots by elimination: {[f'{abs(v):.3e}' for v in piv]}")
    print(f"    nonzero pivots: {sum(1 for v in piv if v != 0.0)}  -> 'rank 6'")
    s, _, _ = svd(X)
    print(f"    singular values:       {[f'{v:.3e}' for v in s]}")
    gap = s[1] / s[2]
    print(f"    sigma2 / sigma3 = {gap:.3e}  -> rank 2, plus noise")
    print("\n  Elimination cannot tell a small pivot from a real one: a pivot's")
    print("  size depends on the row order.  A singular value is the distance")
    print("  to the nearest matrix of lower rank (section 9), so a gap of ten")
    print("  orders of magnitude is a measurement, not a guess.")
    print("  numpy.linalg.matrix_rank and lstsq's rcond do exactly this.")


# ============================================= 9. Eckart-Young
def part9():
    banner("9.  THE BEST RANK-r APPROXIMATION  (L35 sections 1-2)")
    random.seed(35)
    m, n = 8, 6
    A = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    s, U, V = svd(A)
    print(f"  A: 8x6 random integers.  sigma = {[round(v, 4) for v in s]}")
    print("\n     r    |A - A_r|_2   sigma_(r+1)    |A - A_r|_F   sqrt(tail sum)")
    for r in range(1, n):
        Ar = recon(s, U, V, r)
        D = [[A[i][j] - Ar[i][j] for j in range(n)] for i in range(m)]
        print(f"    {r:2d}   {norm2(D):12.6f}  {s[r]:12.6f}   {fro(D):12.6f}"
              f"   {math.sqrt(sum(x*x for x in s[r:])):12.6f}")
    print("\n  Competitors at rank 2 -- every one does worse:")
    r = 2
    best = s[r]
    trials = [
        ("keep the two largest-norm columns",
         lambda: col_keep(A, 2)),
        ("A_2 with factors nudged by 1%",
         lambda: nudged(s, U, V, 2, 0.01)),
        ("a random rank-2 projection of A",
         lambda: rand_proj(A, 2)),
    ]
    for name, f in trials:
        C = f()
        D = [[A[i][j] - C[i][j] for j in range(n)] for i in range(m)]
        print(f"    {name:<36} error_2 = {norm2(D):9.6f}   (best {best:.6f})")
    worst_ratio = float("inf")
    for _ in range(2000):
        C = rand_proj(A, 2)
        D = [[A[i][j] - C[i][j] for j in range(n)] for i in range(m)]
        worst_ratio = min(worst_ratio, norm2(D) / best)
    print(f"    2000 random rank-2 projections: smallest error / best = {worst_ratio:.6f}")


def col_keep(A, r):
    m, n = len(A), len(A[0])
    norms = sorted(range(n), key=lambda j: -sum(A[i][j] ** 2 for i in range(m)))[:r]
    # project A onto the span of those columns (least squares, Week 9)
    Q = []
    for j in norms:
        v = [float(A[i][j]) for i in range(m)]
        for q in Q:
            d = sum(x * y for x, y in zip(v, q))
            v = [x - d * y for x, y in zip(v, q)]
        nv = math.sqrt(sum(x * x for x in v))
        Q.append([x / nv for x in v])
    return [[sum(q[i] * sum(q[k] * A[k][j] for k in range(m)) for q in Q)
             for j in range(n)] for i in range(m)]


def nudged(s, U, V, r, amt):
    m, n = len(U), len(V)
    rng = random.Random(5)
    U2 = [[U[i][k] * (1 + amt * rng.gauss(0, 1)) for k in range(len(U[0]))] for i in range(m)]
    V2 = [[V[j][k] * (1 + amt * rng.gauss(0, 1)) for k in range(len(V[0]))] for j in range(n)]
    return recon(s, U2, V2, r)


def rand_proj(A, r):
    m, n = len(A), len(A[0])
    Q = []
    for _ in range(r):
        v = [random.gauss(0, 1) for _ in range(m)]
        for q in Q:
            d = sum(x * y for x, y in zip(v, q))
            v = [x - d * y for x, y in zip(v, q)]
        nv = math.sqrt(sum(x * x for x in v))
        Q.append([x / nv for x in v])
    return [[sum(q[i] * sum(q[k] * A[k][j] for k in range(m)) for q in Q)
             for j in range(n)] for i in range(m)]


# ============================================= 10. an image
def picture(parts=False):
    """A 24 x 32 test image: a bar, a post and a ring."""
    h, w = 24, 32
    bar = lambda i, j: 2 <= i <= 6 and 2 <= j <= 29
    post = lambda i, j: 2 <= i <= 21 and 4 <= j <= 7
    ring = lambda i, j: 4.0 <= math.hypot(i - 14.5, j - 20.5) <= 6.5
    grid = lambda f: [[1.0 if f(i, j) else 0.0 for j in range(w)] for i in range(h)]
    if parts:
        return [("the bar", grid(bar)), ("the post", grid(post)),
                ("bar and post", grid(lambda i, j: bar(i, j) or post(i, j))),
                ("the ring", grid(ring))]
    return grid(lambda i, j: bar(i, j) or post(i, j) or ring(i, j))


def ascii_img(img):
    chars = " .:-=+*#@"
    out = []
    for row in img:
        out.append("".join(chars[min(8, max(0, int(round(v * 8))))] for v in row))
    return out


def part10():
    banner("10.  COMPRESSING A PICTURE  (L35 section 3)")
    img = picture()
    h, w = len(img), len(img[0])
    s, U, V = svd(img)
    print(f"  {h}x{w} image, {h*w} numbers.  Singular values:")
    print("   " + " ".join(f"{v:.2f}" for v in s[:12]) + " ...")
    nz = sum(1 for v in s if v > 1e-10 * s[0])
    print(f"  numerical rank {nz} of a possible {min(h, w)}")
    total = sum(v * v for v in s)
    print("\n     k   stored numbers   of full   rel. error |A-A_k|_F/|A|_F   energy kept")
    for k in (1, 2, 3, 4, 5, 6, nz):
        stored = k * (h + w + 1)
        err = math.sqrt(sum(v * v for v in s[k:]) / total)
        print(f"    {k:2d}   {stored:12d}    {100*stored/(h*w):5.1f}%"
              f"          {err:.4f}                   {100*(1-err*err):6.2f}%")
    for k in (1, 2, 5):
        Ak = recon(s, U, V, k)
        print(f"\n  rank {k}:")
        for line in ascii_img(Ak):
            print("    |" + line + "|")
    print("\n  original:")
    for line in ascii_img(img):
        print("    |" + line + "|")
    h2, w2 = len(img), len(img[0])
    parts = picture(parts=True)
    print("\n  Where the rank comes from -- each shape on its own:")
    for name, im in parts:
        sp, _, _ = svd(im)
        r = sum(1 for v in sp if v > 1e-10 * sp[0])
        print(f"    {name:<16} numerical rank {r}")
    print("  A rectangle aligned with the pixel grid is one row pattern times")
    print("  one column pattern: rank 1.  A ring is not, and it costs the most.")


# ============================================= 11. total least squares
def part11():
    banner("11.  TOTAL LEAST SQUARES: FITTING A LINE PERPENDICULARLY  (L35 s.4)")
    random.seed(9)
    pts = []
    for _ in range(40):
        t = random.uniform(-3, 3)
        pts.append((t + random.gauss(0, 0.6), 2 * t + random.gauss(0, 0.6)))
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    D = [[p[0] - mx, p[1] - my] for p in pts]
    sxx = sum(d[0] * d[0] for d in D)
    syy = sum(d[1] * d[1] for d in D)
    sxy = sum(d[0] * d[1] for d in D)
    ols_yx = sxy / sxx
    ols_xy = syy / sxy
    s, U, V = svd(D)
    v2 = (V[0][1], V[1][1])
    tls = -v2[0] / v2[1]
    print("  40 points near y = 2x, noise of the same size in BOTH coordinates.")
    print(f"    regress y on x (Week 9):          slope {ols_yx:.6f}")
    print(f"    regress x on y, then invert:      slope {ols_xy:.6f}")
    print(f"    total least squares (SVD):        slope {tls:.6f}")
    print("  The two ordinary fits disagree, because each assumes all the")
    print("  error is in one coordinate.  TLS lies between them.")
    perp = sum((d[0] * v2[0] + d[1] * v2[1]) ** 2 for d in D)
    print(f"\n  sum of squared perpendicular distances = {perp:.6f}")
    print(f"  sigma2^2                               = {s[1]**2:.6f}")
    print("  The line is along v1; its normal is v2; the error it leaves is")
    print("  sigma2^2.  No other line through the centroid does better --")
    print("  that is section 9 at rank 1.")


# ============================================= 12. Lauchli, fourth column
def householder_solve(cols, b):
    m, n = len(cols[0]), len(cols)
    A = [[cols[j][i] for j in range(n)] for i in range(m)]
    rhs = b[:]
    for k in range(n):
        x = [A[i][k] for i in range(k, m)]
        nx = math.sqrt(sum(v * v for v in x))
        if nx == 0:
            continue
        alpha = -nx if x[0] >= 0 else nx
        v = x[:]
        v[0] -= alpha
        nv = math.sqrt(sum(t * t for t in v))
        if nv == 0:
            continue
        v = [t / nv for t in v]
        for j in range(k, n):
            sd = sum(v[i - k] * A[i][j] for i in range(k, m))
            for i in range(k, m):
                A[i][j] -= 2 * sd * v[i - k]
        sd = sum(v[i - k] * rhs[i] for i in range(k, m))
        for i in range(k, m):
            rhs[i] -= 2 * sd * v[i - k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (rhs[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x


def svd_solve(A, b, rcond=None):
    s, U, V = svd(A)
    m, n = len(A), len(A[0])
    tol = (rcond if rcond is not None else max(m, n) * 2.2e-16) * s[0]
    x = [0.0] * n
    for k in range(n):
        if s[k] > tol:
            c = sum(U[i][k] * b[i] for i in range(m)) / s[k]
            for j in range(n):
                x[j] += c * V[j][k]
    return x


def part12():
    banner("12.  WEEK 9'S TABLE, WITH THE SVD ADDED  (L35 section 5)")
    print("  Lauchli, b = (1, 0, 0), exact x1 = x2 = 1/(2 + eps^2).  Reported: x1.\n")
    print("    eps      normal equations    Householder QR    SVD            exact")
    for e in (1e-3, 1e-5, 1e-7, 1e-8, 1e-10):
        A = [[1.0, 1.0], [e, 0.0], [0.0, e]]
        b = [1.0, 0.0, 0.0]
        a11 = 1.0 + e * e
        det = a11 * a11 - 1.0
        ne = "FAILED (singular)" if det == 0.0 else f"{(a11 - 1.0) / det:.9f}"
        hh = householder_solve([[1.0, e, 0.0], [1.0, 0.0, e]], b)[0]
        sv = svd_solve(A, b)[0]
        print(f"    {e:.0e}   {ne:>17}   {hh:.9f}       {sv:.9f}    {1/(2+e*e):.9f}")
    print("\n  Householder and the SVD both survive.  The SVD also survives the")
    print("  case Householder cannot: exactly dependent columns (section 7),")
    print("  where R has a zero on its diagonal and back substitution divides")
    print("  by it.")
    cnt_s = [0]
    random.seed(1)
    n = 40
    A = [[random.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    svd(A, cnt_s)
    print(f"\n  Cost on a random {n}x{n}, counted in multiply-adds:")
    print(f"    elimination (Week 0, n^3/3 pairs x 2) ~ {2*n**3//3:>10,d}")
    print(f"    one-sided Jacobi SVD, as run          ~ {cnt_s[0]:>10,d}"
          f"   ({cnt_s[0]/(2*n**3/3):.1f}x)")
    print("  Jacobi is the simplest SVD to write, not the fastest; LAPACK's")
    print("  Golub-Kahan SVD is cheaper (Trefethen & Bau, Lecture 31) and still")
    print("  a large multiple of elimination.  The most informative")
    print("  factorisation is the most expensive, and that is why Week 9 did")
    print("  not start here.")


if __name__ == "__main__":
    part1()
    part2()
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
    print("\n" + BAR)
    print("Everything above is reproducible.  The Fraction results are exact;")
    print("the float results are what IEEE double precision actually returns.")
    print(BAR)
