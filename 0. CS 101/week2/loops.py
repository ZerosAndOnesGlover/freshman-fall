#!/usr/bin/env python3
"""
loops.py
CS 101 — Lab 2, Part 3: Loops to Write
Tuesday 13 October 2026

Weeks 0-2 tools only: if/elif/else, while, for, range, break/continue,
nested loops, lists. No def.
"""

# --- Exercise 3.1(a): Collatz length --------------------------------------------
n = int(input("n: "))
start = n
steps = 0
# Invariant: after `steps` iterations, n is the value reached from the start by `steps` Collatz moves.
# Initialisation: 0 iterations in, n == start, which is reached by 0 moves.
# Preservation: each iteration applies one Collatz move and adds one to `steps`.
# Termination: for every value tested the sequence reaches 1 (still unproven in general),
#              and each iteration shrinks the distance to that point by one, so it stops.
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    steps += 1
print(steps)

# --- Exercise 3.1(b): longest Collatz run for starts 1..20 ----------------------
best_start = 1
best_steps = 0
for start in range(1, 21):
    n = start
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    if steps > best_steps:          # strict > keeps the first on a tie
        best_start = start
        best_steps = steps
print(best_start, best_steps)

# --- Exercise 3.2: Sieve of Eratosthenes ----------------------------------------
n = int(input("n: "))
is_prime = [True] * (n + 1)
is_prime[0] = False
is_prime[1] = False
p = 2
# Invariant: every composite number with a prime factor less than p has been crossed out.
# Initialisation: p == 2, and no smaller prime factor exists, so nothing needs crossing out yet.
# Preservation: crossing out the multiples of p removes every composite whose smallest prime
#              factor is p; advancing p keeps the statement true for the next prime.
# Termination: p grows by one each iteration and stops once p * p > n.
while p * p <= n:
    if is_prime[p]:
        for multiple in range(p * p, n + 1, p):
            is_prime[multiple] = False
    p += 1

primes = []
for k in range(n + 1):
    if is_prime[k]:
        primes.append(k)
print(primes)
print(len(primes))

gaps = []
for i in range(len(primes) - 1):
    gaps.append(primes[i + 1] - primes[i])
print(gaps)
