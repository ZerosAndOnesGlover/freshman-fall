#!/usr/bin/env python3
"""MATH 241 Week 4 -- every number quoted in L13-L15, reproduced.

Pure Python, no dependencies.  Run it:

    python3 transformations.py

Weeks 0-3 treated a matrix as a thing you eliminate.  Week 4 treats it
as what it has been all along -- a function -- and asks which matrix
you get, which depends on a choice of basis that nobody made
explicitly until now.

Exact arithmetic in Fraction everywhere except the rotations, which
need real angles and say so.
"""

from fractions import Fraction as F
import math

BAR = "=" * 68


def banner(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def mat(*rows):
    return [[F(v) for v in r] for r in rows]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def show(name, A, w=6):
    print("%s =" % name)
    for row in A:
        print("    [" + " ".join(("%" + str(w) + "s") % v for v in row) + "]")


def vec(v):
    return "(" + ", ".join(str(x) for x in v) + ")"


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


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


def inverse2(A):
    d = det2(A)
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


# --------------------------------------------------------------------------
# L13-L14: the matrix is built from the images of the basis vectors.
# --------------------------------------------------------------------------

banner("L14: every column is T applied to a basis vector")

E1, E2 = [F(1), F(0)], [F(0), F(1)]
maps = {
    "reflect across y = x": lambda v: [v[1], v[0]],
    "project onto y = x":   lambda v: [(v[0] + v[1]) / 2, (v[0] + v[1]) / 2],
    "shear, factor 2":      lambda v: [v[0] + 2 * v[1], v[1]],
    "scale x by 3":         lambda v: [3 * v[0], v[1]],
    "rotate by 90 degrees": lambda v: [-v[1], v[0]],
}
for name, T in maps.items():
    c1, c2 = T(E1), T(E2)
    A = [[c1[0], c2[0]], [c1[1], c2[1]]]
    print("\n%s" % name)
    print("   T(e1) = %-10s T(e2) = %-10s" % (vec(c1), vec(c2)))
    show("   A", A, 4)

print("\nThat is the whole construction: put T(e_j) in column j.")
print("It works because e_1,...,e_n is a basis, and L13 SS5 says a linear")
print("map is completely determined by what it does to a basis.")


# --------------------------------------------------------------------------
# L14: composition is multiplication -- rotations add.
# --------------------------------------------------------------------------

banner("L14: composing transformations multiplies their matrices")


def rot(deg):
    t = math.radians(deg)
    return [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]


def mulf(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


prod = mulf(rot(30), rot(60))
direct = rot(90)
print("R(30) R(60) =")
for row in prod:
    print("    [" + " ".join("%9.6f" % v for v in row) + "]")
print("R(90)       =")
for row in direct:
    print("    [" + " ".join("%9.6f" % v for v in row) + "]")
gap = max(abs(a - b) for ra, rb in zip(prod, direct) for a, b in zip(ra, rb))
print("\nlargest disagreement: %.2e  -- rounding, not mathematics." % gap)
print("Rotating by 30 then 60 is rotating by 90, and the matrices know it.")
print("\nThis is why matrix multiplication is defined as it is (Week 1 L04 SS1):")
print("it was BUILT to make composition work, and here is the payoff.")
print("\nAnd R(30)R(60) = R(60)R(30) -- rotations commute, unusually:")
print("   max difference %.2e" % max(abs(a - b)
                                     for ra, rb in zip(mulf(rot(30), rot(60)),
                                                       mulf(rot(60), rot(30)))
                                     for a, b in zip(ra, rb)))


# --------------------------------------------------------------------------
# L13-L14: differentiation is a matrix.
# --------------------------------------------------------------------------

banner("L13: d/dx on P_3 is a 4x4 matrix")

print("basis 1, x, x^2, x^3.  Differentiate each and read off coordinates:")
print("   D(1)   = 0        -> (0, 0, 0, 0)")
print("   D(x)   = 1        -> (1, 0, 0, 0)")
print("   D(x^2) = 2x       -> (0, 2, 0, 0)")
print("   D(x^3) = 3x^2     -> (0, 0, 3, 0)")

D = mat((0, 1, 0, 0), (0, 0, 2, 0), (0, 0, 0, 3), (0, 0, 0, 0))
show("\nD", D, 3)

R, piv = rref(D)
print("\nrank %d, nullity %d, and %d + %d = 4 = dim P_3   (Week 3 L11 SS6)"
      % (len(piv), 4 - len(piv), len(piv), 4 - len(piv)))
print("   kernel  = N(D) = the constants          -- dim 1")
print("   range   = C(D) = polynomials of deg <=2 -- dim 3")
print("\nAnd D is nilpotent -- differentiate a cubic four times:")
Dk = D
for k in range(2, 5):
    Dk = mul(Dk, D)
    nz = sum(1 for row in Dk for v in row if v)
    print("   D^%d has %d nonzero entries%s" % (k, nz, "  <- zero matrix" if nz == 0 else ""))
print("\nD^3 sends x^3 to 6, which is exactly the third derivative of x^3.")
print("No matrix of numbers built from a geometry problem does this;")
print("nilpotency is a real property of differentiation on a bounded degree.")


# --------------------------------------------------------------------------
# L15: change of basis.
# --------------------------------------------------------------------------

banner("L15: the same transformation, a better basis")

A = mat((0, 1), (1, 0))                 # reflect across y = x, standard basis
Mb = mat((1, 1), (1, -1))               # columns are the new basis vectors
Mi = inverse2(Mb)

show("A  (standard basis)", A, 5)
show("M  (new basis in its columns)", Mb, 5)
B = mul(Mi, mul(A, Mb))
show("B = M^-1 A M", B, 5)

print("\nThe new basis is v1 = (1,1) -- along the mirror line -- and")
print("v2 = (1,-1) -- perpendicular to it.  The reflection fixes v1 and")
print("negates v2, so in THAT basis it is diagonal: diag(1, -1).")
print("\nSame transformation.  Different numbers.  The geometry did not move;")
print("the description did.")

P = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
show("\nP  (project onto y = x, standard basis)", P, 5)
show("M^-1 P M", mul(Mi, mul(P, Mb)), 5)
print("\ndiag(1, 0): keep the component along the line, discard the other.")
print("P^2 = P holds in both bases (%s) -- an idempotent is idempotent"
      % (mul(P, P) == P))
print("however you describe it.  Week 8 calls these projections.")


banner("L15: similar matrices share what belongs to the transformation")

print("%-22s %-10s %-10s %-8s" % ("matrix", "trace", "det", "rank"))
for name, X in [("A  = reflection", A), ("B = M^-1 A M", B),
                ("P  = projection", P), ("M^-1 P M", mul(Mi, mul(P, Mb)))]:
    _, pv = rref([row[:] for row in X])
    print("%-22s %-10s %-10s %-8d" % (name, trace(X), det2(X), len(pv)))

print("\nA and B are the same map in two bases, and they agree on trace,")
print("determinant and rank.  So do P and its diagonal form.")
print("\nThose three numbers are properties of the TRANSFORMATION.  The")
print("four individual entries are properties of the basis you chose.")
print("Week 5 explains the determinant, Weeks 6-7 add the eigenvalues to")
print("this list, and Week 7 is the search for a basis making B diagonal.")
