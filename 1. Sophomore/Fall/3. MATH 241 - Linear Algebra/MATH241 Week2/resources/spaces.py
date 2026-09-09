#!/usr/bin/env python3
"""MATH 241 Week 2 -- every number quoted in L07-L09, reproduced.

Pure Python, no dependencies.  Run it:

    python3 spaces.py

Week 0 asked whether Ax = b has a solution and answered it one b at a
time.  Week 2 answers it for every b at once, and the answer is two
subspaces.  This script computes both, for the matrix the three
lectures share.
"""

from fractions import Fraction as F

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def vec(v):
    """(1, 2, -1) rather than [Fraction(1, 1), ...]."""
    return "(" + ", ".join(str(x) for x in v) + ")"


def show(name, M):
    print("%s =" % name)
    for row in M:
        print("    [" + "  ".join("%4s" % v for v in row) + "]")


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def mv(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def col(A, j):
    return [A[i][j] for i in range(len(A))]


# --------------------------------------------------------------------------
# Reduced row echelon form.  Week 0's elimination, carried upward and scaled.
# --------------------------------------------------------------------------

def rref(A):
    """Return (R, pivot_columns).  Exact, in Fraction."""
    A = [row[:] for row in A]
    m, n = len(A), len(A[0])
    pivots, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, m) if A[i][c] != 0), None)
        if p is None:
            continue                      # no pivot in this column: it is free
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]     # scale the pivot to 1
        for i in range(m):                # clear the column, up and down
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return A, pivots


def null_basis(A):
    """One special solution per free column: set it to 1, the others to 0."""
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
    return basis, pivots, free


# --------------------------------------------------------------------------
# The matrix all three lectures use.
# --------------------------------------------------------------------------

A = mat((1, 3, 3, 2),
        (2, 6, 9, 7),
        (-1, -3, 3, 4))

banner("L07-L09: the running example, a 3x4 matrix")
show("A", A)
print("\ncolumns of A:")
for j in range(4):
    print("   a%d = %s" % (j + 1, vec(col(A, j))))
print("\na2 = 3*a1 exactly:", col(A, 1) == [3 * v for v in col(A, 0)])


banner("L08: the column space")
R, pivots = rref(A)
show("rref(A)", R)
print("\npivot columns: %s      free columns: %s"
      % ([c + 1 for c in pivots], [c + 1 for c in range(4) if c not in pivots]))
print("rank = number of pivots =", len(pivots))
print("\nC(A) is spanned by the PIVOT columns of A -- a1 and a3:")
print("   a1 =", vec(col(A, 0)))
print("   a3 =", vec(col(A, 2)))
print("\nTwo independent vectors in R^3 span a plane.  Its equation:")
print("   5*b1 - 2*b2 + b3 = 0")
print("\nevery column satisfies it:")
for j in range(4):
    c = col(A, j)
    print("   a%d: 5(%s) - 2(%s) + (%s) = %s"
          % (j + 1, c[0], c[1], c[2], 5 * c[0] - 2 * c[1] + c[2]))

print("\n--- and row operations CHANGE the column space ---")
print("C(A)       is the plane  5b1 - 2b2 + b3 = 0")
print("C(rref(A)) is the plane  b3 = 0        -- rref's rows 1,2 span it")
print("They are different planes.  What survives elimination is which")
print("columns depend on which, not the space the columns live in.")


banner("L09: the null space")
basis, pivots, free = null_basis(A)
print("free variables: %s -> %d special solutions\n"
      % (["x%d" % (f + 1) for f in free], len(basis)))
for f, v in zip(free, basis):
    print("   s%d = %-20s  A s%d = %s" % (f + 1, vec(v), f + 1, vec(mv(A, v))))
print("\nN(A) = all combinations of those, a 2-dimensional subspace of R^4.")
print("rank %d + nullity %d = %d = number of columns." % (len(pivots), len(free), len(A[0])))


banner("L09: the complete solution")
b = mv(A, [F(1)] * 4)
print("Take b = A(1,1,1,1) =", vec(b), " -- consistent by construction.")
aug = [A[i] + [b[i]] for i in range(len(A))]
Raug, pa = rref(aug)
show("rref[A | b]", Raug)
xp = [F(0)] * 4
for i, c in enumerate(pa):
    if c < 4:
        xp[c] = Raug[i][4]
print("\nparticular solution (every free variable set to 0):")
print("   xp =", vec(xp), "  A xp =", vec(mv(A, xp)))
print("\ncomplete solution:  x = xp + t*s2 + u*s4")
print("   check t=u=1:", vec([a + c + d for a, c, d in zip(xp, basis[0], basis[1])]),
      "-- which is the (1,1,1,1) we started from.")

bad = [b[0], b[1], b[2] + 1]
print("\nNow move b off the plane:  b = %s, where 5b1-2b2+b3 = %s"
      % (vec(bad), 5 * bad[0] - 2 * bad[1] + bad[2]))
Rbad, _ = rref([A[i] + [bad[i]] for i in range(len(A))])
print("last row of rref[A | b] is", vec(Rbad[-1]), "-- which reads 0 = 1.")
print("No solution, and the plane equation predicted it without eliminating.")


banner("L07: what is and is not a subspace")
tests = [
    ("{(x,y) : y = 2x}",            True,  "a line through the origin"),
    ("{(x,y) : y = 2x + 1}",        False, "misses 0"),
    ("{(x,y) : xy = 0}",            False, "the two axes: (1,0)+(0,1) escapes"),
    ("{(x,y) : x >= 0}",            False, "not closed under -1"),
    ("{x in R^4 : Ax = 0}",         True,  "the null space -- L09"),
    ("{x in R^4 : Ax = b}, b != 0", False, "misses 0; a translate, not a subspace"),
    ("upper triangular 3x3",        True,  "closed under + and scaling"),
    ("invertible 3x3",              False, "I + (-I) = 0, which is not invertible"),
]
print("%-32s %-6s %s" % ("set", "sub?", "why"))
for name, ok, why in tests:
    print("%-32s %-6s %s" % (name, "yes" if ok else "NO", why))
