#!/usr/bin/env python3
"""MATH 241 Week 12 -- every number quoted in L36-L38, reproduced.

Pure Python, no dependencies.  Run it:

    python3 applications.py

Week 0's syllabus promised four applications and said "all four are the
same theorem".  This file measures all four -- regression, PCA,
PageRank and Fourier -- with the tools of Weeks 7-11, and L38 section 6
is honest about the one of the four that is NOT the same theorem.

Exact in Fraction where exactness is available (PageRank's answer, the
Fourier coefficients' formula).  Float everywhere else, and labelled.
"""

from fractions import Fraction as F
import cmath
import math
import random

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


# ------------------------------------------------------------ small tools
def T(A):
    return [list(r) for r in zip(*A)]


def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def svd(Ain):
    """One-sided Jacobi SVD (Week 11's svd.py, trimmed).  A = U diag(s) V^T."""
    m, n = len(Ain), len(Ain[0])
    if m < n:
        s, U, V = svd(T(Ain))
        return s, V, U
    W = [[float(v) for v in row] for row in Ain]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(80):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                a = sum(W[i][p] ** 2 for i in range(m))
                b = sum(W[i][q] ** 2 for i in range(m))
                g = sum(W[i][p] * W[i][q] for i in range(m))
                if g == 0.0 or abs(g) <= 1e-15 * math.sqrt(a * b):
                    continue
                rotated = True
                zeta = (b - a) / (2.0 * g)
                t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                for i in range(m):
                    wp, wq = W[i][p], W[i][q]
                    W[i][p], W[i][q] = c * wp - s * wq, s * wp + c * wq
                for i in range(n):
                    vp, vq = V[i][p], V[i][q]
                    V[i][p], V[i][q] = c * vp - s * vq, s * vp + c * vq
        if not rotated:
            break
    sig = [math.sqrt(sum(W[i][j] ** 2 for i in range(m))) for j in range(n)]
    order = sorted(range(n), key=lambda j: -sig[j])
    U = [[W[i][j] / sig[j] if sig[j] > 0 else 0.0 for j in order] for i in range(m)]
    return [sig[j] for j in order], U, [[V[i][j] for j in order] for i in range(n)]


def lstsq(A, b):
    """Least squares through the SVD, discarding sigma below the usual threshold."""
    s, U, V = svd(A)
    m, n = len(A), len(A[0])
    tol = max(m, n) * 2.2e-16 * s[0]
    x = [0.0] * n
    for k in range(n):
        if s[k] > tol:
            c = sum(U[i][k] * b[i] for i in range(m)) / s[k]
            for j in range(n):
                x[j] += c * V[j][k]
    return x


def jacobi_eig(Ain):
    """Eigenvalues of a symmetric matrix (Week 10's symmetric.py, trimmed)."""
    n = len(Ain)
    A = [[float(v) for v in row] for row in Ain]
    fro = math.sqrt(sum(v * v for row in A for v in row)) or 1.0
    for _ in range(100):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= 1e-17 * fro:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if A[p][q] == 0.0:
                    continue
                th = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    kp, kq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * kp - s * kq, s * kp + c * kq
                for k in range(n):
                    pk, qk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * pk - s * qk, s * pk + c * qk
    return sorted((A[i][i] for i in range(n)), reverse=True)


# ======================================= 1. regression, and overfitting
def legendre(t, deg):
    P = [1.0, t]
    for k in range(1, deg):
        P.append(((2 * k + 1) * t * P[k] - k * P[k - 1]) / (k + 1))
    return P[:deg + 1]


def part1():
    banner("1.  MORE COLUMNS ALWAYS FIT BETTER -- MEASURED ON NEW DATA  (L36 s.2-3)")
    random.seed(12)
    f = lambda t: math.sin(2.5 * t)
    train = [(t, f(t) + random.gauss(0, 0.15)) for t in [random.uniform(-1, 1) for _ in range(20)]]
    test = [(t, f(t) + random.gauss(0, 0.15)) for t in [random.uniform(-1, 1) for _ in range(400)]]
    print("  20 training points and 400 test points from y = sin(2.5t) + noise")
    print("  (noise standard deviation 0.15).  Fit polynomials of rising degree")
    print("  to the TRAINING points only, then score them on both.\n")
    print("    deg   train RMS   test RMS        cond (monomials)   cond (Legendre)")
    for deg in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 19):
        A = [[t ** k for k in range(deg + 1)] for t, _ in train]
        b = [y for _, y in train]
        x = lstsq(A, b)
        pred = lambda t: sum(c * t ** k for k, c in enumerate(x))
        rtr = math.sqrt(sum((pred(t) - y) ** 2 for t, y in train) / len(train))
        rte = math.sqrt(sum((pred(t) - y) ** 2 for t, y in test) / len(test))
        s, _, _ = svd(A)
        L = [legendre(t, deg) for t, _ in train]
        sl, _, _ = svd(L)
        print(f"    {deg:3d}   {rtr:9.4f}   {rte:14.4f}   {s[0]/s[-1]:14.2e}   {sl[0]/sl[-1]:12.2e}")
    print("\n  Training error falls every time -- L29 section 4, guaranteed.")
    print("  Test error falls, flattens, then EXPLODES.  At degree 19 the curve")
    print("  passes through all 20 training points and predicts nothing.")

    print("\n  Does a better-conditioned basis fix it?  Same fits in the Legendre")
    print("  basis (same column space, so the same projection in exact arithmetic):\n")
    print("    deg   test RMS (monomials)   test RMS (Legendre)   relative difference")
    for deg in (6, 10, 15, 19):
        A = [[t ** k for k in range(deg + 1)] for t, _ in train]
        L = [legendre(t, deg) for t, _ in train]
        b = [y for _, y in train]
        xm, xl = lstsq(A, b), lstsq(L, b)
        rm = math.sqrt(sum((sum(c * t ** k for k, c in enumerate(xm)) - y) ** 2 for t, y in test) / len(test))
        rl = math.sqrt(sum((sum(c * p for c, p in zip(xl, legendre(t, deg))) - y) ** 2 for t, y in test) / len(test))
        print(f"    {deg:3d}   {rm:20.6f}   {rl:19.6f}   {abs(rm-rl)/rl:.2e}")
    print("\n  The Legendre basis IMPROVES the conditioning -- by a factor of about")
    print("  100 at degree 19 -- and does nothing for the OVERFITTING: the two")
    print("  bases span the same space, so they produce the same bad curve, to")
    print("  eleven digits at degree 15.  Numerics and statistics are different")
    print("  problems, and a better basis only helps with the first.")


# ======================================= 2. PCA
def cloud(seed, normal_noise):
    random.seed(seed)
    e1 = (0.6, 0.48, 0.64)          # two orthonormal directions spanning a plane
    e2 = (0.0, 0.8, -0.6)
    pts = []
    for _ in range(300):
        a, b = random.gauss(0, 3), random.gauss(0, 1.5)
        p = [a * e1[i] + b * e2[i] for i in range(3)]
        pts.append([p[i] + random.gauss(0, normal_noise) for i in range(3)])
    return pts, e1, e2


def centred(pts):
    n = len(pts)
    m = [sum(p[i] for p in pts) / n for i in range(3)]
    return [[p[i] - m[i] for i in range(3)] for p in pts], m


def part2():
    banner("2.  PCA IS THE SVD OF THE CENTRED DATA  (L36 section 4)")
    pts, e1, e2 = cloud(3, 0.4)
    D, m = centred(pts)
    s, U, V = svd(D)
    tot = sum(x * x for x in s)
    print("  300 points near a plane in R^3, with noise 0.4 in every direction.")
    print(f"  singular values of the centred 300x3 data: {[round(x, 4) for x in s]}")
    print(f"  variance explained: {[f'{100*x*x/tot:.2f}%' for x in s]}")
    print(f"  cumulative:         {100*s[0]**2/tot:.2f}%, {100*(s[0]**2+s[1]**2)/tot:.2f}%, 100%")
    n = [V[i][2] for i in range(3)]
    true_n = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]
    ang = math.degrees(math.acos(min(1.0, abs(sum(a * b for a, b in zip(n, true_n))))))
    print(f"  third right singular vector (the plane's normal): {[round(x, 5) for x in n]}")
    print(f"  true normal of the generating plane:              {[round(x, 5) for x in true_n]}")
    print(f"  angle between them: {ang:.4f} degrees")
    rec = sum((sum(D[k][i] * n[i] for i in range(3))) ** 2 for k in range(len(D)))
    print(f"\n  sum of squared distances to the PCA plane = {rec:.6f}")
    print(f"  sigma3^2                                   = {s[2]**2:.6f}")
    print("  Week 11's L35 section 5 at rank 2 instead of rank 1.")

    C = [[sum(D[k][i] * D[k][j] for k in range(len(D))) / (len(D) - 1) for j in range(3)] for i in range(3)]
    lam = jacobi_eig(C)
    print("\n  The covariance route: C = D^T D / (N - 1), then its eigenvalues.")
    print(f"    eigenvalues of C:           {[round(x, 6) for x in lam]}")
    print(f"    sigma^2 / (N - 1) from SVD: {[round(x*x/(len(D)-1), 6) for x in s]}")
    print("  Identical here.  They are not always -- section 3.")


def part3():
    banner("3.  PCA THROUGH THE COVARIANCE MATRIX IS WEEK 9'S MISTAKE AGAIN  (L36 s.6)")
    print("  Same plane, but the points now lie ON it to within 1e-9.  The")
    print("  smallest variance is real and tiny.  Two ways to find it:\n")
    pts, e1, e2 = cloud(3, 1e-9)
    D, m = centred(pts)
    s, U, V = svd(D)
    C = [[sum(D[k][i] * D[k][j] for k in range(len(D))) / (len(D) - 1) for j in range(3)] for i in range(3)]
    lam = jacobi_eig(C)
    print(f"    SVD of the data:        sigma3^2/(N-1) = {s[2]**2/(len(D)-1):.4e}"
          f"   (sigma3 = {s[2]:.4e})")
    print(f"    eigenvalues of D^T D/(N-1):   lambda3 = {lam[2]:.4e}")
    print(f"    ratio lambda1 / true lambda3 = {lam[0]/(s[2]**2/(len(D)-1)):.2e}"
          f"   (1/eps_mach = {1/2.22e-16:.2e})")
    print("\n  The true smallest variance is about 1e-18, far below eps_mach times")
    print("  the largest (about 2e-15).  Forming D^T D squares the ratio, so the")
    print("  covariance route returns rounding noise for it -- here NEGATIVE,")
    print("  which no variance can be.  The SVD of D never squares anything and")
    print("  resolves sigma3 directly.  Week 9's L28 section 1, in statistics.")


# ======================================= 4. regression plane vs PCA plane
def part4():
    banner("4.  THE REGRESSION PLANE IS NOT THE PCA PLANE  (L36 section 5)")
    pts, _, _ = cloud(3, 0.4)
    D, m = centred(pts)
    s, U, V = svd(D)
    pca_n = [V[i][2] for i in range(3)]
    A = [[1.0, p[0], p[1]] for p in pts]
    b = [p[2] for p in pts]
    c = lstsq(A, b)
    reg_n = [-c[1], -c[2], 1.0]
    L = math.sqrt(sum(x * x for x in reg_n))
    reg_n = [x / L for x in reg_n]
    ang = math.degrees(math.acos(min(1.0, abs(sum(a * b for a, b in zip(reg_n, pca_n))))))
    print(f"  regression of z on (x, y):  z = {c[0]:.5f} + {c[1]:.5f} x + {c[2]:.5f} y")
    print(f"  its normal:  {[round(x, 5) for x in reg_n]}")
    print(f"  PCA normal:  {[round(x, 5) for x in pca_n]}")
    print(f"  angle between the two planes: {ang:.4f} degrees")
    vert = sum((p[2] - c[0] - c[1] * p[0] - c[2] * p[1]) ** 2 for p in pts)
    perp_reg = sum((sum((p[i] - m[i]) * reg_n[i] for i in range(3))) ** 2 for p in pts)
    perp_pca = s[2] ** 2
    print(f"\n  sum of squared VERTICAL distances:       regression {vert:.4f}")
    print(f"  sum of squared PERPENDICULAR distances:  regression {perp_reg:.4f}   PCA {perp_pca:.4f}")
    print("  Each wins the contest it was built for.  Regression singles out z")
    print("  as the thing to predict; PCA treats x, y and z alike.  Neither is")
    print("  'the' plane -- they answer different questions.")


# ======================================= 5. PageRank
LINKS = {0: [1, 2], 1: [2], 2: [0], 3: [2, 4], 4: [3, 5], 5: []}


def google(alpha, links=LINKS):
    n = len(links)
    G = [[F(0)] * n for _ in range(n)]
    for j in range(n):
        outs = links[j] or list(range(n))            # a dangling page links everywhere
        for i in range(n):
            G[i][j] = alpha * (F(1, len(outs)) if i in outs else 0) + (1 - alpha) * F(1, n)
    return G


def stationary(G):
    n = len(G)
    M = [[G[i][j] - (1 if i == j else 0) for j in range(n)] + [F(0)] for i in range(n)]
    M[-1] = [F(1)] * n + [F(1)]                     # replace one equation by sum = 1
    for k in range(n):
        p = next(i for i in range(k, n) if M[i][k] != 0)
        M[k], M[p] = M[p], M[k]
        pv = M[k][k]
        M[k] = [v / pv for v in M[k]]
        for i in range(n):
            if i != k and M[i][k] != 0:
                f = M[i][k]
                M[i] = [a - f * b for a, b in zip(M[i], M[k])]
    return [M[i][n] for i in range(n)]


def charpoly(A):
    """Faddeev-LeVerrier, exact: coefficients of det(lambda I - A), leading 1."""
    n = len(A)
    I = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    Mk = [[F(0)] * n for _ in range(n)]
    c = [F(1)]
    for k in range(1, n + 1):
        AM = [[sum(A[i][t] * Mk[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        Mk = [[AM[i][j] + c[-1] * I[i][j] for j in range(n)] for i in range(n)]
        AMk = [[sum(A[i][t] * Mk[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        c.append(-sum(AMk[i][i] for i in range(n)) / k)
    return c


def roots(coef):
    """Durand-Kerner on a monic polynomial with Fraction coefficients."""
    n = len(coef) - 1
    cf = [float(x) for x in coef]
    p = lambda z: sum(a * z ** (n - i) for i, a in enumerate(cf))
    z = [(0.4 + 0.9j) ** k for k in range(n)]
    for _ in range(2000):
        new = []
        for i in range(n):
            d = 1
            for j in range(n):
                if i != j:
                    d *= (z[i] - z[j])
            new.append(z[i] - p(z[i]) / d)
        if max(abs(a - b) for a, b in zip(new, z)) < 1e-15:
            z = new
            break
        z = new
    return sorted(z, key=lambda w: -abs(w)), max(abs(p(w)) for w in z)


def part5():
    banner("5.  PAGERANK ON A SIX-PAGE WEB, EXACTLY  (L37 sections 2-4)")
    print("  links: 0->1,2   1->2   2->0   3->2,4   4->3,5   5->(nothing)")
    alpha = F(17, 20)
    G = google(alpha)
    x = stationary(G)
    print(f"  damping alpha = {alpha} = {float(alpha)}; page 5 is dangling\n")
    print("  exact PageRank (Fraction):")
    for i, v in enumerate(x):
        print(f"    page {i}: {str(v):>14} = {float(v):.6f}")
    print(f"  sum = {sum(x)}")
    Gx = matvec(G, x)
    print(f"  G x = x exactly: {Gx == x}")
    cs = [sum(G[i][j] for i in range(len(G))) for j in range(len(G))]
    print(f"  every column of G sums to 1: {all(c == 1 for c in cs)}")

    coef = charpoly(G)
    zs, resid = roots(coef)
    print("\n  eigenvalues of G (exact characteristic polynomial, then its roots):")
    for w in zs:
        print(f"    {w.real:+.6f} {w.imag:+.6f}i    |lambda| = {abs(w):.6f}")
    print(f"  largest |p(lambda)| at the computed roots: {resid:.1e}")
    lam2 = abs(zs[1])
    print(f"  |lambda_2| = {lam2:.6f}  <=  alpha = 0.85, as the damping theorem promises")

    print("\n  Power iteration from the uniform vector, in float:")
    Gf = [[float(v) for v in r] for r in G]
    xf = [float(v) for v in x]
    v = [1 / 6] * 6
    errs = {}
    for it in range(1, 61):
        v = matvec(Gf, v)
        errs[it] = sum(abs(a - b) for a, b in zip(v, xf))
    print("     k    L1 error      |lambda_2|^k")
    for it in (1, 5, 10, 20, 30, 40, 50, 60):
        print(f"    {it:2d}   {errs[it]:.3e}     {lam2**it:.3e}")
    rate = (errs[60] / errs[10]) ** (1 / 50)
    print(f"  average reduction per step, k = 10..60: {rate:.4f}   (|lambda_2| = {lam2:.4f})")
    print("  The step-by-step ratio wobbles because lambda_2 is complex: the")
    print("  error spirals in, exactly as Week 7's L23 section 3 said it would.")


def part6():
    banner("6.  WHY THE DAMPING IS THERE  (L37 section 5)")
    print("  (a) A two-page cycle, 0 -> 1 -> 0, no damping.  Eigenvalues 1 and -1:")
    P = [[0.0, 1.0], [1.0, 0.0]]
    v = [1.0, 0.0]
    for it in range(1, 7):
        v = matvec(P, v)
        print(f"      step {it}: {v}")
    print("      |lambda_2| = 1, so nothing decays and the iteration never settles.")
    print("\n  (b) Two separate webs, {0,1} and {2,3}, each a cycle, no damping:")
    links = {0: [1], 1: [0], 2: [3], 3: [2]}
    G0 = google(F(1), links)
    for start in ([F(1, 2), F(1, 2), F(0), F(0)], [F(0), F(0), F(1, 2), F(1, 2)],
                  [F(1, 4)] * 4):
        print(f"      start {[str(s) for s in start]} is fixed: {matvec(G0, start) == start}")
    print("      lambda = 1 has a 2-dimensional eigenspace: the 'ranking' is not")
    print("      unique, and depends on where you start.  Week 6's geometric")
    print("      multiplicity, deciding whether the answer means anything.")
    print("\n  (c) The same two webs WITH damping 0.85:")
    G = google(F(17, 20), links)
    x = stationary(G)
    print(f"      unique PageRank: {[str(v) for v in x]}")
    zs, _ = roots(charpoly(G))
    print(f"      eigenvalue moduli: {[round(abs(w), 6) for w in zs]}")
    print("      Damping mixes in (1 - alpha)/n from every page to every page, so")
    print("      every entry of G is positive.  Perron-Frobenius then guarantees")
    print("      eigenvalue 1 is simple with a positive eigenvector, and every other")
    print("      |lambda| < 1.  A further result (Haveliwala & Kamvar, 2003) sharpens")
    print("      that to |lambda_2| <= alpha -- attained here, where the web splits.")

    print("\n  (d) What it costs at web scale, n = 1e9 pages, ~10 links per page:")
    n, nnz, iters = 1e9, 1e10, 50
    print(f"      elimination, n^3/3            = {n**3/3:.1e} operations")
    print(f"      50 power iterations x nonzeros = {iters*nnz:.1e} operations")
    print(f"      ratio                          = {n**3/3/(iters*nnz):.1e}")
    print("      Week 0's L03 section 2 promised this; Week 7 named the method.")


# ======================================= 7. Fourier
def part7():
    banner("7.  FOURIER COEFFICIENTS ARE PROJECTIONS  (L38 sections 1-2)")
    N = 64
    ts = [2 * math.pi * k / N for k in range(N)]
    basis = [("1", [1.0] * N)]
    for k in range(1, 4):
        basis.append((f"cos {k}t", [math.cos(k * t) for t in ts]))
        basis.append((f"sin {k}t", [math.sin(k * t) for t in ts]))
    G = [[sum(a * b for a, b in zip(u, v)) for _, v in basis] for _, u in basis]
    off = max(abs(G[i][j]) for i in range(len(G)) for j in range(len(G)) if i != j)
    print(f"  64 equally spaced samples of 1, cos t, sin t, ..., cos 3t, sin 3t:")
    print(f"    largest dot product between DIFFERENT ones: {off:.2e}")
    print(f"    squared lengths: {[round(G[i][i], 6) for i in range(len(G))]}")
    print("  Orthogonal, to rounding.  (The integrals over [0, 2pi] are exactly")
    print("  0, and pi or 2pi on the diagonal.)")

    print("\n  The square wave f = +1 on (0, pi), -1 on (pi, 2pi).  Its coefficient")
    print("  on sin kt is <f, sin kt> / <sin kt, sin kt> -- Week 8's L26 section 1(c):")
    M = 4096
    ts = [2 * math.pi * (k + 0.5) / M for k in range(M)]
    f = [1.0 if t < math.pi else -1.0 for t in ts]
    print("     k    projection (4096 samples)    exact 4/(pi k) for odd k, 0 for even")
    for k in range(1, 8):
        s = [math.sin(k * t) for t in ts]
        coef = sum(a * b for a, b in zip(f, s)) / sum(b * b for b in s)
        exact = 4 / (math.pi * k) if k % 2 else 0.0
        print(f"    {k:2d}    {coef:+.8f}                 {exact:+.8f}")


def Si(x, terms=40):
    return sum((-1) ** n * x ** (2 * n + 1) / ((2 * n + 1) * math.factorial(2 * n + 1))
               for n in range(terms))


def part8():
    banner("8.  CONVERGENCE IN THE MEAN, AND GIBBS'S OVERSHOOT THAT NEVER GOES  (L38 s.3)")
    SK = lambda x, K: 4 / math.pi * sum(math.sin(k * x) / k for k in range(1, K + 1, 2))
    print("  S_K = the projection of the square wave onto sin t, sin 3t, ..., sin Kt.\n")
    print("       K    largest value of S_K   where         squared error ||f - S_K||^2")
    for K in (1, 3, 9, 19, 49, 99, 199, 999):
        lo, hi = 1e-9, 2 * math.pi / (K + 1)
        for _ in range(100):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if SK(m1, K) < SK(m2, K):
                lo = m1
            else:
                hi = m2
        xm = (lo + hi) / 2
        err2 = 2 * math.pi - sum(math.pi * (4 / (math.pi * k)) ** 2 for k in range(1, K + 1, 2))
        print(f"    {K:4d}    {SK(xm, K):.9f}           x = {xm:.6f}   {err2:.6e}")
    lim = 2 / math.pi * Si(math.pi)
    print(f"\n  limit of the largest value: (2/pi) Si(pi) = {lim:.9f}")
    print(f"  overshoot above 1: {lim - 1:.6f}, i.e. {100*(lim-1)/2:.4f}% of the jump of 2")
    print("\n  The squared error goes to zero like 1/K (Pythagoras: it is the")
    print("  energy in the discarded coefficients).  The PEAK does not go down at")
    print("  all -- it moves toward the jump and stays 17.9% above 1.  Projection")
    print("  minimises the squared error, and the squared error is all it controls.")


def part9():
    banner("9.  THE DISCRETE COSINE BASIS, AND WHY JPEG USES IT  (L38 section 4)")
    N = 8
    Q = [[(math.sqrt(1 / N) if k == 0 else math.sqrt(2 / N)) * math.cos(math.pi * (2 * i + 1) * k / (2 * N))
          for k in range(N)] for i in range(N)]
    QtQ = [[sum(Q[i][a] * Q[i][b] for i in range(N)) for b in range(N)] for a in range(N)]
    print(f"  8x8 orthonormal DCT-II matrix: max |Q^T Q - I| = "
          f"{max(abs(QtQ[a][b]-(a==b)) for a in range(N) for b in range(N)):.2e}")
    sig = [10 + 3 * i - 0.25 * i * i for i in range(N)]
    c = [sum(Q[i][k] * sig[i] for i in range(N)) for k in range(N)]
    tot = sum(x * x for x in sig)
    print(f"  a smooth signal:      {[round(x, 3) for x in sig]}")
    print(f"  its DCT coefficients: {[round(x, 4) for x in c]}")
    print(f"  energy check: sum signal^2 = {tot:.6f}, sum coeff^2 = {sum(x*x for x in c):.6f}")
    print("\n     keep   error keeping the k largest     error keeping the k largest")
    print("            DCT coefficients                SAMPLES")
    for keep in (1, 2, 3, 4):
        idx = sorted(range(N), key=lambda k: -abs(c[k]))[:keep]
        rec = [sum(Q[i][k] * c[k] for k in idx) for i in range(N)]
        e = math.sqrt(sum((a - b) ** 2 for a, b in zip(sig, rec)) / tot)
        pidx = sorted(range(N), key=lambda i: -abs(sig[i]))[:keep]
        ep = math.sqrt(sum(sig[i] ** 2 for i in range(N) if i not in pidx) / tot)
        print(f"      {keep}          {100*e:7.3f}%                        {100*ep:7.3f}%")
    print("\n  Same signal, same number of kept numbers, an orthonormal change of")
    print("  basis first.  Smooth signals are nearly sparse in cosines and not at")
    print("  all sparse in samples.  JPEG does this on 8x8 blocks of an image.")


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
    print("\n" + BAR)
    print("Everything above is reproducible.  The Fraction results are exact;")
    print("the float results are what IEEE double precision actually returns.")
    print(BAR)
