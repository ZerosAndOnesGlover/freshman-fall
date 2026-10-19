import math

# Q2: sin(1/x) at x = 2/(k*pi), k = 1,3,5,7,9,11
print("Q2: sin(1/x)")
for k in [1, 3, 5, 7, 9, 11]:
    x = 2 / (k * math.pi)
    print(x, math.sin(1 / x))

# Q3: (x^3 - 8)/(x - 2) near x = 2
print("Q3: (x^3 - 8)/(x - 2)")
for x in [1.9, 1.99, 1.999, 2.001, 2.01, 2.1]:
    print(x, (x**3 - 8) / (x - 2))

# Q5: 8 bisection steps on x^3 - 2x - 5 over [2, 3]
print("Q5: 8 bisection steps")
a = 2.0
b = 3.0
step = 0
while step < 8:
    m = (a + b) / 2
    fa = a**3 - 2*a - 5
    fm = m**3 - 2*m - 5
    print(step + 1, a, b, m, fm)
    if fa * fm < 0:
        b = m
    else:
        a = m
    step = step + 1

# Q6: run until the bracket is narrower than 1e-6
print("Q6: until b - a > 1e-6")
a = 2.0
b = 3.0
step = 0
while b - a > 1e-6:
    m = (a + b) / 2
    fa = a**3 - 2*a - 5
    fm = m**3 - 2*m - 5
    if fa * fm < 0:
        b = m
    else:
        a = m
    step = step + 1
print(step, m)

# Q7: step counts for several tolerances
print("Q7: step counts")
for tol in [1e-4, 1e-6, 1e-10]:
    a = 2.0
    b = 3.0
    step = 0
    while b - a > tol:
        m = (a + b) / 2
        fa = a**3 - 2*a - 5
        fm = m**3 - 2*m - 5
        if fa * fm < 0:
            b = m
        else:
            a = m
        step = step + 1
    print(tol, step)
