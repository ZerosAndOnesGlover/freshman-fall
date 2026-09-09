#!/usr/bin/env python3
"""MATH 241 Week 1 -- every number quoted in L04-L06, reproduced.

Pure Python, no dependencies.  Run it:

    python3 matrices.py

Week 0's script showed you that elimination is exact when you let it be.
This one is about the three claims of Week 1 that people disbelieve:
matrix multiplication does not commute, where you put the parentheses is
worth three orders of magnitude, and you should almost never compute an
inverse.
"""

from fractions import Fraction as F
import random
import time

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def mul(X, Y):
    """The definition, written out.  Three loops, and the order of the two
    outer ones is the only thing a fast implementation changes."""
    n, K, p = len(X), len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][j] for k in range(K)) for j in range(p)]
            for i in range(n)]


def show(name, M):
    print("%s =" % name)
    for row in M:
        print("   ", [str(v) for v in row])


# --------------------------------------------------------------------------
# L04 SS3: AB and BA are different questions.
# --------------------------------------------------------------------------

banner("L04: AB != BA, and not by a little")
P = [[0, 1], [0, 0]]
Q = [[0, 0], [1, 0]]
show("P", P)
show("Q", Q)
show("PQ", mul(P, Q))
show("QP", mul(Q, P))
print("\nPQ and QP are both diagonal, both idempotent, and they have no")
print("nonzero entry in common.  P and Q are each their own square root of")
print("zero: P*P = %s." % mul(P, P))


# --------------------------------------------------------------------------
# L04 SS5: associativity is free; the parenthesisation is not.
# --------------------------------------------------------------------------

banner("L04: (AB)C against A(BC), A 1000x2, B 2x1000, C 1000x1")
m, n, p, q = 1000, 2, 1000, 1
left = 2 * m * n * p + 2 * m * p * q
right = 2 * n * p * q + 2 * m * n * q
print("(AB)C : %10d flops, and an intermediate of %d x %d = %.1f MB"
      % (left, m, p, m * p * 8 / 1e6))
print("A(BC) : %10d flops, and an intermediate of %d x %d"
      % (right, n, q))
print("ratio : %.0f to 1, from moving two brackets" % (left / right))

random.seed(241)
A = [[random.random() for _ in range(n)] for _ in range(m)]
B = [[random.random() for _ in range(p)] for _ in range(n)]
C = [[random.random()] for _ in range(p)]

t = time.perf_counter()
r1 = mul(mul(A, B), C)
t1 = time.perf_counter() - t
t = time.perf_counter()
r2 = mul(A, mul(B, C))
t2 = time.perf_counter() - t
gap = max(abs(a[0] - b[0]) for a, b in zip(r1, r2))
print("\nmeasured: (AB)C %.3f s   A(BC) %.6f s   speedup %.0fx"
      % (t1, t2, t1 / t2))
print("the two answers differ by at most %.2e -- rounding, not disagreement."
      % gap)


# --------------------------------------------------------------------------
# L05: the inverse, and L06: A = LU, on Week 0's matrix.
# --------------------------------------------------------------------------

M = [[F(2), F(1), F(-1)],
     [F(4), F(5), F(0)],
     [F(-2), F(8), F(11)]]


def lu(A):
    """Elimination, keeping the multipliers.  No row exchanges needed here."""
    n = len(A)
    U = [row[:] for row in A]
    L = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(k + 1, n):
            L[i][k] = U[i][k] / U[k][k]
            for j in range(k, n):
                U[i][j] -= L[i][k] * U[k][j]
    return L, U


def gauss_jordan_inverse(A):
    n = len(A)
    aug = [row[:] + [F(int(i == j)) for j in range(n)]
           for i, row in enumerate(A)]
    for k in range(n):
        pv = aug[k][k]
        aug[k] = [v / pv for v in aug[k]]
        for i in range(n):
            if i != k and aug[i][k]:
                f = aug[i][k]
                aug[i] = [vi - f * vk for vi, vk in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


banner("L06: A = LU on Week 0's matrix -- L is the multipliers")
L, U = lu(M)
show("A", M)
show("L", L)
show("U", U)
print("\nL times U reproduces A:", mul(L, U) == M)
print("The three multipliers l21=2, l31=-1, l32=3 that Week 0 computed and")
print("threw away are exactly the subdiagonal of L.")

banner("L05: the inverse of the same matrix")
Ai = gauss_jordan_inverse(M)
show("A^-1", Ai)
print("\n24 * A^-1 =")
for row in Ai:
    print("   ", [str(v * 24) for v in row])
print("\nA * A^-1 = I:", mul(M, Ai) == [[F(int(i == j)) for j in range(3)]
                                        for i in range(3)])
print("\nL and U hold 6 nonzero entries between them, all integers.")
print("A^-1 holds 9, and not one of them is an integer.  That is the")
print("general picture, and it gets worse with n.")


# --------------------------------------------------------------------------
# L05 SS6: solve, do not invert.
# --------------------------------------------------------------------------

def hilbert_f(n):
    return [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]


def solve_gepp(A, b):
    n = len(A)
    Mx = [A[i][:] + [b[i]] for i in range(n)]
    for k in range(n):
        pr = max(range(k, n), key=lambda r: abs(Mx[r][k]))
        Mx[k], Mx[pr] = Mx[pr], Mx[k]
        for i in range(k + 1, n):
            f = Mx[i][k] / Mx[k][k]
            for j in range(k, n + 1):
                Mx[i][j] -= f * Mx[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (Mx[i][n] - sum(Mx[i][j] * x[j]
                               for j in range(i + 1, n))) / Mx[i][i]
    return x


def invert_f(A):
    n = len(A)
    aug = [A[i][:] + [1.0 * (i == j) for j in range(n)] for i in range(n)]
    for k in range(n):
        pr = max(range(k, n), key=lambda r: abs(aug[r][k]))
        aug[k], aug[pr] = aug[pr], aug[k]
        pv = aug[k][k]
        aug[k] = [v / pv for v in aug[k]]
        for i in range(n):
            if i != k and aug[i][k]:
                f = aug[i][k]
                aug[i] = [vi - f * vk for vi, vk in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


banner("L05: solving Hx = b, against forming H^-1 and multiplying")
print("%3s  %-16s  %-16s  %s" % ("n", "solve", "H^-1 b", "times worse"))
for n in (6, 8, 10, 12, 14):
    H = hilbert_f(n)
    b = [sum(H[i]) for i in range(n)]          # exact answer is all ones
    xs = solve_gepp(H, b)
    Hi = invert_f(H)
    xi = [sum(Hi[i][j] * b[j] for j in range(n)) for i in range(n)]
    es = max(abs(v - 1.0) for v in xs)
    ei = max(abs(v - 1.0) for v in xi)
    print("%3d  %-16.3g  %-16.3g  %.1f" % (n, es, ei, ei / es if es else 0))
print("\nSame matrix, same right-hand side, same pivoting, same machine.")
print("The only difference is whether A^-1 was formed on the way.")


banner("L05: and it costs more, too")
print("%7s  %-14s  %-14s  %s" % ("n", "LU + solve", "invert + mul", "ratio"))
for n in (100, 1000, 10000):
    lu_cost = n ** 3 / 3 + 2 * n * n
    inv_cost = 2 * n ** 3 + 2 * n * n
    print("%7d  %-14.3g  %-14.3g  %.1f" % (n, lu_cost, inv_cost,
                                           inv_cost / lu_cost))
print("\nAnd for k right-hand sides the LU is reused: n^3/3 + 2kn^2 against")
print("2n^3 + 2kn^2.  The inverse never catches up, because the factorisation")
print("you already have does the same job for the same 2n^2 per solve.")


# --------------------------------------------------------------------------
# L05 SS7: the inverse of a sparse matrix is dense.
# --------------------------------------------------------------------------

banner("L05: K is tridiagonal.  K^-1 is not sparse at all")
n = 5
K = [[F(2) if i == j else (F(-1) if abs(i - j) == 1 else F(0))
      for j in range(n)] for i in range(n)]
Ki = gauss_jordan_inverse(K)
show("K", K)
print("6 * K^-1 =")
for row in Ki:
    print("   ", [str(v * 6) for v in row])


def nnz(M):
    return sum(1 for row in M for v in row if v)


Lk, Uk = lu(K)
print("\n%-22s %s" % ("K nonzeros:", nnz(K)))
print("%-22s %s   <- every single entry" % ("K^-1 nonzeros:", nnz(Ki)))
print("%-22s %s and %s, and both keep the band" % ("L, U nonzeros:",
                                                   nnz(Lk), nnz(Uk)))
print("\nK^-1 is symmetric, positive, and has no zero anywhere.  For the")
print("n x n version K has 3n-2 nonzeros and K^-1 has n^2:")
for n2 in (100, 1000, 10000):
    print("   n=%-6d  K: %-9d  K^-1: %-12d  ratio %d"
          % (n2, 3 * n2 - 2, n2 * n2, n2 * n2 // (3 * n2 - 2)))
print("\nThis is the practical reason nobody inverts a sparse matrix: the")
print("inverse does not fit, while L and U do.")
