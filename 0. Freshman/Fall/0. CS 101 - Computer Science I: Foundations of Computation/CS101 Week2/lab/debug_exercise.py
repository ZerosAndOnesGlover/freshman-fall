#!/usr/bin/env python3
"""
loops.py
CS 101 — Week 2, Lab 2

Loop implementation exercises: Collatz, Sieve, FizzBuzz, Digital Root, Caesar Cipher.

Student: ____________________________
Date: ______________________________
"""


# ─── Exercise 3.1: Collatz Sequence ───────────────────────────────────────────

def collatz_length(n):
    """
    Return the number of steps for the Collatz sequence starting at n to reach 1.

    Collatz rules:
        if n is even → n = n // 2
        if n is odd  → n = 3 * n + 1
    Keep going until n == 1.

    Examples:
        collatz_length(1) → 0    (already at 1, no steps)
        collatz_length(2) → 1    (2 → 1, one step)
        collatz_length(6) → 8    (6→3→10→5→16→8→4→2→1)

    Loop type: while
    """
    # === Loop Invariant ===
    # At the start of each iteration:
    #   steps == number of Collatz steps taken so far
    #   n > 0  (preserved by both rules — verify this!)
    #
    # Termination: unproven in general (Collatz conjecture), but observed for all
    #              tested values. For this exercise, assume it terminates.
    # =====================

    steps = 0

    # TODO: implement the while loop
    # - Each iteration: apply the Collatz rule to n, increment steps
    # - Stop when n == 1

    return steps


def max_collatz_length(limit):
    """
    Find which starting number in [1, limit] produces the longest Collatz sequence.

    Returns a tuple: (starting_number, length)

    Example:
        max_collatz_length(20) → (18, 20)

    Loop type: outer for loop (over range 1..limit+1), inner: collatz_length()
    """
    best_start  = 1
    best_length = 0

    # TODO: loop from 1 to limit (inclusive)
    # For each i, compute collatz_length(i)
    # Track the i with the largest length

    return best_start, best_length


# ─── Exercise 3.2: Sieve of Eratosthenes ─────────────────────────────────────

def sieve_of_eratosthenes(n):
    """
    Return a sorted list of all prime numbers up to and including n.

    Algorithm:
    1. Create list is_prime[0..n], all True
    2. Set is_prime[0] = is_prime[1] = False
    3. p = 2
       While p * p <= n:
           if is_prime[p]:
               mark is_prime[p*p], is_prime[p*p + p], ... as False
           p += 1
    4. Return all i where is_prime[i] is True

    Examples:
        sieve_of_eratosthenes(10) → [2, 3, 5, 7]
        sieve_of_eratosthenes(1)  → []
        sieve_of_eratosthenes(2)  → [2]
    """
    if n < 2:
        return []

    # Step 1: Initialize
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False

    # Step 2: Sieve
    p = 2
    # TODO: implement the outer while loop
    # - Check if p * p <= n
    # - If is_prime[p]: inner loop to mark multiples from p*p onward
    # - Increment p

    # Step 3: Collect primes
    # TODO: return a list of all i in range(n+1) where is_prime[i] is True
    pass


def prime_gaps(n):
    """
    Return a list of gaps between consecutive primes up to n.

    Example:
        prime_gaps(20) → [1, 2, 2, 4, 2, 4]
        Primes ≤ 20: [2, 3, 5, 7, 11, 13, 17, 19]
        Gaps:         3-2=1, 5-3=2, 7-5=2, 11-7=4, 13-11=2, 17-13=4, 19-17=2
        → [1, 2, 2, 4, 2, 4, 2]  (7 gaps for 8 primes)
    """
    primes = sieve_of_eratosthenes(n)

    if len(primes) < 2:
        return []

    # TODO: use a for loop (with range or enumerate) to compute gaps
    # gaps[i] = primes[i+1] - primes[i]
    gaps = []
    # ...
    return gaps


# ─── Exercise 3.3: FizzBuzz Extended ─────────────────────────────────────────

def fizzbuzz_range(start, end, rules=None):
    """
    Generalized FizzBuzz for a custom range and custom divisor-word rules.

    For each n in [start, end] (inclusive):
        - result = concatenation of words for each (divisor, word) in rules
                   where n % divisor == 0, in rule order
        - if no divisors match, result = str(n)

    rules: list of (int, str) tuples. Defaults to [(3,"Fizz"), (5,"Buzz")].

    Returns a list of strings.

    Examples:
        fizzbuzz_range(1, 5)  → ["1", "2", "Fizz", "4", "Buzz"]
        fizzbuzz_range(13, 15) → ["13", "14", "FizzBuzz"]
        fizzbuzz_range(1, 7, [(2,"Even"), (3,"Three")]) →
            ["1", "Even", "Three", "Even", "5", "EvenThree", "7"]
    """
    if rules is None:
        rules = [(3, "Fizz"), (5, "Buzz")]

    result = []

    # TODO: outer for loop over range(start, end + 1)
    # Inner: build the label string by checking each rule
    # Append label or str(n) to result

    return result


# ─── Exercise 3.4: Digital Root ───────────────────────────────────────────────

def digital_root(n):
    """
    Repeatedly sum the digits of n until the result is a single digit (0–9).

    Examples:
        digital_root(0)   → 0
        digital_root(9)   → 9
        digital_root(10)  → 1    (1+0=1)
        digital_root(493) → 7    (4+9+3=16, 1+6=7)
        digital_root(999) → 9    (9+9+9=27, 2+7=9)

    Loop structure: outer while loop (repeat until single digit),
                    inner while loop (sum the digits — use n % 10, n //= 10)

    IMPORTANT: State the loop invariant as a comment inside the function.
    """
    # Special case
    if n == 0:
        return 0

    # === Loop Invariant ===
    # TODO: state the invariant here
    # At the start of each outer iteration:
    #   [your invariant here]
    # =====================

    # TODO: implement nested while loops
    # Outer loop: while n has more than one digit (n >= 10)
    # Inner loop: sum the digits of n, store in digit_sum
    # After inner loop: n = digit_sum

    return n


# ─── Exercise 3.5: Caesar Cipher ──────────────────────────────────────────────

def caesar_encrypt(text, shift):
    """
    Apply a Caesar cipher to text.

    Rules:
    - Shift alphabetic characters only (a-z, A-Z)
    - Preserve case
    - Wrap around (modular arithmetic)
    - Leave non-alpha characters unchanged
    - Handle negative and large shifts correctly

    Shifting formula for uppercase letter c:
        chr((ord(c) - ord('A') + shift) % 26 + ord('A'))

    Shifting formula for lowercase letter c:
        chr((ord(c) - ord('a') + shift) % 26 + ord('a'))

    Examples:
        caesar_encrypt("Hello, World!", 3)  → "Khoor, Zruog!"
        caesar_encrypt("abc", 1)            → "bcd"
        caesar_encrypt("xyz", 3)            → "abc"
        caesar_encrypt("ABC", -3)           → "XYZ"
        caesar_encrypt("Hello!", 26)        → "Hello!"  (full rotation = no change)
    """
    result = ""

    # TODO: for loop over characters in text
    # For each char:
    #   if it's uppercase: apply uppercase shift formula
    #   elif it's lowercase: apply lowercase shift formula
    #   else: append unchanged
    # Hint: use c.isupper(), c.islower()

    return result


def caesar_decrypt(text, shift):
    """
    Decrypt a Caesar-encrypted text.

    This is a one-liner: decrypting with shift k is the same as
    encrypting with shift -k.
    """
    # TODO: one line using caesar_encrypt
    pass


# ─── Test Suite ───────────────────────────────────────────────────────────────

def run_tests():
    """Run all tests. A passing test prints ✓. Failure raises AssertionError."""

    print("Running tests...\n")

    # --- collatz_length ---
    assert collatz_length(1)  == 0,   f"Expected 0, got {collatz_length(1)}"
    assert collatz_length(2)  == 1,   f"Expected 1, got {collatz_length(2)}"
    assert collatz_length(6)  == 8,   f"Expected 8, got {collatz_length(6)}"
    assert collatz_length(27) == 111, f"Expected 111, got {collatz_length(27)}"
    print("✓ collatz_length")

    # --- max_collatz_length ---
    start, length = max_collatz_length(20)
    assert start == 18 and length == 20, \
        f"Expected (18, 20), got ({start}, {length})"
    print("✓ max_collatz_length")

    # --- sieve_of_eratosthenes ---
    assert sieve_of_eratosthenes(1)   == [],                        "Primes ≤ 1 = []"
    assert sieve_of_eratosthenes(2)   == [2],                       "Primes ≤ 2 = [2]"
    assert sieve_of_eratosthenes(10)  == [2, 3, 5, 7],              "Primes ≤ 10"
    assert sieve_of_eratosthenes(30)  == [2,3,5,7,11,13,17,19,23,29]
    assert len(sieve_of_eratosthenes(100)) == 25, "25 primes ≤ 100"
    print("✓ sieve_of_eratosthenes")

    # --- prime_gaps ---
    assert prime_gaps(5) == [1, 2],       f"prime_gaps(5): got {prime_gaps(5)}"
    assert prime_gaps(10) == [1, 2, 2],   f"prime_gaps(10): got {prime_gaps(10)}"
    assert prime_gaps(1) == [],            "prime_gaps(1) = []"
    print("✓ prime_gaps")

    # --- fizzbuzz_range ---
    fb = fizzbuzz_range(1, 15)
    assert len(fb) == 15
    assert fb[0]  == "1",        f"fb[0]={fb[0]}"
    assert fb[2]  == "Fizz",     f"fb[2]={fb[2]}"
    assert fb[4]  == "Buzz",     f"fb[4]={fb[4]}"
    assert fb[14] == "FizzBuzz", f"fb[14]={fb[14]}"

    custom = fizzbuzz_range(1, 6, [(2, "Even"), (3, "Three")])
    assert custom == ["1", "Even", "Three", "Even", "5", "EvenThree"], \
        f"Custom fizzbuzz: {custom}"
    print("✓ fizzbuzz_range")

    # --- digital_root ---
    assert digital_root(0)   == 0
    assert digital_root(9)   == 9
    assert digital_root(10)  == 1
    assert digital_root(493) == 7
    assert digital_root(999) == 9
    print("✓ digital_root")

    # --- caesar cipher ---
    assert caesar_encrypt("Hello, World!", 3)  == "Khoor, Zruog!"
    assert caesar_encrypt("abc", 1)            == "bcd"
    assert caesar_encrypt("xyz", 3)            == "abc"
    assert caesar_encrypt("ABC", -3)           == "XYZ"
    assert caesar_encrypt("Hello!", 26)        == "Hello!"
    assert caesar_decrypt("Khoor, Zruog!", 3)  == "Hello, World!"
    # Round-trip test
    msg = "The Quick Brown Fox Jumps Over The Lazy Dog!"
    for k in [1, 13, 25, -5]:
        assert caesar_decrypt(caesar_encrypt(msg, k), k) == msg, \
            f"Round-trip failed for shift {k}"
    print("✓ caesar_encrypt / caesar_decrypt")

    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    run_tests()
