import math

# Part 1: secant slopes for f(x) = x^2 at a = 2
def f(x):
    return x**2


def forward(a, h):
    return (f(a + h) - f(a)) / h


print("Q1: forward difference for f(x)=x^2 at a=2")
for h in [1, 0.1, 0.01, -0.01]:
    print(h, forward(2, h))

# Part 4: numerical differentiation of f(x) = sqrt(x) at a = 4
def g(x):
    return math.sqrt(x)


def forward_g(a, h):
    return (g(a + h) - g(a)) / h


def central(a, h):
    return (g(a + h) - g(a - h)) / (2 * h)


print("\nQ8/Q9: f=sqrt(x) at a=4, exact f'(4)=0.25")
for h in [0.1, 0.01, 0.001, 1e-15]:
    fr = forward_g(4, h)
    ce = central(4, h)
    print(h, fr, abs(fr - 0.25), ce, abs(ce - 0.25))
