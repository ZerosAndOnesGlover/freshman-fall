#!/usr/bin/env python3
"""
ps2.py
CS 101 — Problem Set 2: Control Flow

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""

import math   # allowed for math.sqrt in B6


# ══════════════════════════════════════════════════════════════════════════════
# B1: Number Analysis
# ══════════════════════════════════════════════════════════════════════════════

def analyze_number(n):
    """
    Analyze a positive integer and return a dictionary of properties.

    Keys:
        "digits"         — list of digits, most-significant first
        "digit_sum"      — sum of digits
        "digit_product"  — product of digits
        "is_palindrome"  — True if digits read same forwards and backwards
        "largest_digit"  — maximum single digit
        "num_digits"     — count of digits
        "digital_root"   — repeat summing digits until single digit

    Args:
        n (int): a positive integer

    Returns:
        dict: the analysis dictionary

    Example:
        analyze_number(9875) →
            {"digits": [9,8,7,5], "digit_sum": 29, "digit_product": 2520,
             "is_palindrome": False, "largest_digit": 9, "num_digits": 4,
             "digital_root": 2}

    Constraint: Do NOT convert n to a string. Use // and % to extract digits.
    """
    # Step 1: Extract digits using while loop
    # (collect in reverse — least significant first — then reverse)
    digits_reversed = []
    temp = n

    # TODO: while temp > 0: extract last digit, append, shift
    # ...

    digits = list(reversed(digits_reversed))  # most-significant first

    # Step 2: Compute each property
    digit_sum = None         # TODO
    digit_product = None     # TODO
    is_palindrome = None     # TODO: compare digits to its reverse
    largest_digit = None     # TODO
    num_digits = None        # TODO

    # Step 3: Digital root (nested while loops)
    dr = digit_sum           # start from digit_sum (already computed)
    # TODO: while dr >= 10: sum its digits
    # ...

    return {
        "digits":        digits,
        "digit_sum":     digit_sum,
        "digit_product": digit_product,
        "is_palindrome": is_palindrome,
        "largest_digit": largest_digit,
        "num_digits":    num_digits,
        "digital_root":  dr,
    }


# ══════════════════════════════════════════════════════════════════════════════
# B2: Sequence Generators
# ══════════════════════════════════════════════════════════════════════════════

def fibonacci_sequence(n):
    """
    Return a list of the first n Fibonacci numbers.
    F(0)=0, F(1)=1, F(k)=F(k-1)+F(k-2).

    fibonacci_sequence(8) → [0, 1, 1, 2, 3, 5, 8, 13]
    fibonacci_sequence(0) → []
    fibonacci_sequence(1) → [0]

    Use a for loop.

    === Loop Invariant ===
    At the start of iteration i (0-indexed):
      TODO: state invariant here
    ======================
    """
    if n == 0:
        return []
    if n == 1:
        return [0]

    result = [0, 1]

    # TODO: for loop from 2 to n-1 (inclusive), appending F(k) = F(k-1) + F(k-2)

    return result[:n]


def geometric_sequence(first, ratio, n):
    """
    Return a list of n terms of a geometric sequence.
    Terms: first, first*ratio, first*ratio^2, ..., first*ratio^(n-1)

    geometric_sequence(2, 3, 5) → [2, 6, 18, 54, 162]
    geometric_sequence(1, 0.5, 4) → [1, 0.5, 0.25, 0.125]

    Use a for loop.
    """
    # TODO
    pass


def convergents_of_sqrt2(n):
    """
    Return the first n convergents of the continued fraction for √2.

    Starting with (p, q) = (1, 1):
        next p = p + 2*q
        next q = p + q  (using OLD p)

    convergents_of_sqrt2(5) → [(1,1), (3,2), (7,5), (17,12), (41,29)]

    Each (p, q) approximates √2 as p/q. The approximation improves each step.

    Use a for loop.
    """
    if n == 0:
        return []

    result = []
    p, q = 1, 1

    # TODO: for loop n times: append (p,q), then update p and q
    # Remember: both updates use the OLD values, so compute new_p first,
    # then new_q uses OLD p.

    return result


def look_and_say(n):
    """
    Return the first n terms of the Look-and-Say sequence as strings.

    Starting from "1":
        "1"      → read as "one 1" → "11"
        "11"     → read as "two 1s" → "21"
        "21"     → read as "one 2, one 1" → "1211"
        "1211"   → read as "one 1, one 2, two 1s" → "111221"

    look_and_say(5) → ["1", "11", "21", "1211", "111221"]
    look_and_say(1) → ["1"]

    Hint: to generate the next term from current:
        Walk through current with index i.
        At each position, count how many consecutive identical chars follow.
        Append count + char to the next term string.

    Use a while loop inside a for loop.
    """
    if n == 0:
        return []

    terms = ["1"]

    for _ in range(1, n):
        current = terms[-1]
        next_term = ""
        i = 0
        # TODO: while i < len(current):
        #   char = current[i]
        #   count = 1
        #   while i + count < len(current) and current[i + count] == char:
        #       count += 1
        #   next_term += str(count) + char
        #   i += count
        terms.append(next_term)

    return terms


# ══════════════════════════════════════════════════════════════════════════════
# B3: Pattern Printer
# ══════════════════════════════════════════════════════════════════════════════

def right_triangle(n):
    """
    Print a right triangle of * with n rows.
    Row i (1-indexed) has i stars.

    right_triangle(5):
        *
        **
        ***
        ****
        *****
    """
    # TODO: for loop
    pass


def diamond(n):
    """
    Print a diamond shape. n is the half-height (number of rows in top half).
    Total rows = 2*n - 1. Middle row has 2*n-1 stars.

    diamond(3):
      *
     ***
    *****
     ***
      *

    Hint: top half has rows 1..n, bottom half has rows n-1..1.
    Stars in row i (1-indexed from top): 2*i - 1
    Leading spaces in row i: n - i
    """
    # TODO: two for loops — top half (rows 1..n), bottom half (rows n-1..1)
    pass


def multiplication_table(n):
    """
    Print an n×n multiplication table with aligned columns.

    multiplication_table(5):
        1    2    3    4    5
        2    4    6    8   10
        3    6    9   12   15
        4    8   12   16   20
        5   10   15   20   25

    Use f-string with a fixed width. Width hint: len(str(n*n)) + 1
    """
    # TODO: nested for loops
    pass


def number_spiral(n):
    """
    Print numbers 1..n² arranged in a clockwise spiral.

    number_spiral(4):
         1  2  3  4
        12 13 14  5
        11 16 15  6
        10  9  8  7

    Strategy:
    1. Create an n×n grid (list of lists), initialized to 0.
    2. Walk through the grid in a clockwise spiral, placing 1, 2, 3, ...
    3. Directions: right (0,1) → down (1,0) → left (0,-1) → up (-1,0) → repeat
    4. Turn when you hit a wall (row/col out of bounds) or a filled cell.
    5. Print the grid with aligned columns.

    Width per cell: len(str(n*n)) + 1
    """
    # Step 1: Create empty grid
    grid = [[0] * n for _ in range(n)]

    # Step 2: Spiral fill
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    dir_idx = 0
    row, col = 0, 0

    # TODO: for num in range(1, n*n + 1):
    #   grid[row][col] = num
    #   compute next_row, next_col
    #   if next position is valid and empty: move there
    #   else: turn (dir_idx = (dir_idx + 1) % 4), update row/col accordingly

    # Step 3: Print
    width = len(str(n * n)) + 1
    # TODO: nested for loops to print grid with f"{val:{width}}" formatting
    pass


# ══════════════════════════════════════════════════════════════════════════════
# B4: String Processing
# ══════════════════════════════════════════════════════════════════════════════

def word_frequency(text):
    """
    Return the most frequently occurring word in text (lowercase, split on whitespace).
    On a tie, return the first one alphabetically.

    word_frequency("the cat sat on the mat the cat") → "the"

    Constraint: No dictionaries. Use nested loops to count.
    """
    words = text.lower().split()
    if not words:
        return ""

    # TODO:
    # For each unique word, count how many times it appears.
    # Track the word with the highest count (tie-breaking: alphabetically first).
    # Hint: outer loop over words, inner loop counts occurrences.
    # Skip words already counted (use a "seen" list or check if word
    # was already processed in a previous outer iteration).
    pass


def run_length_encode(s):
    """
    Compress a string using run-length encoding.

    Consecutive identical characters → count + character.

    run_length_encode("aaabbbccddddee") → "3a3b2c4d2e"
    run_length_encode("abcd")           → "1a1b1c1d"
    run_length_encode("")               → ""

    Use a while loop with an index i tracking position.
    """
    if not s:
        return ""

    result = ""
    i = 0

    # TODO: while i < len(s):
    #   char = s[i]
    #   count = 1
    #   while i + count < len(s) and s[i + count] == char: count += 1
    #   result += str(count) + char
    #   i += count

    return result


def run_length_decode(s):
    """
    Decompress a run-length encoded string.

    run_length_decode("3a3b2c4d2e") → "aaabbbccddddee"
    run_length_decode("")           → ""

    Assumes format: (digit+)(letter) pairs, like "3a", "12b".
    Use a while loop: collect digit characters, then read the letter.
    """
    if not s:
        return ""

    result = ""
    i = 0

    # TODO: while i < len(s):
    #   collect digits: num_str = ""
    #   while s[i].isdigit(): num_str += s[i]; i += 1
    #   char = s[i]; i += 1
    #   result += char * int(num_str)

    return result


def is_pangram(sentence):
    """
    Return True if sentence contains every letter a-z at least once (case-insensitive).

    is_pangram("The quick brown fox jumps over the lazy dog") → True
    is_pangram("Hello world") → False

    Use a for loop over the alphabet.
    """
    lower = sentence.lower()
    # TODO: for each letter in 'abcdefghijklmnopqrstuvwxyz':
    #   if it's not in lower: return False
    # return True
    pass


# ══════════════════════════════════════════════════════════════════════════════
# B5: Number Theory
# ══════════════════════════════════════════════════════════════════════════════

def gcd(a, b):
    """
    Compute the greatest common divisor of a and b using the Euclidean algorithm.

    Euclidean algorithm:
        while b != 0:
            a, b = b, a % b
        return a

    gcd(48, 18) → 6
    gcd(100, 75) → 25
    gcd(7, 13) → 1    (coprime)

    === Loop Invariant ===
    At the start of each iteration: gcd(a, b) == gcd(original_a, original_b)
    (The GCD is preserved by the operation (a,b) → (b, a%b).)

    Proof sketch:
        gcd(a, b) = gcd(b, a % b) because any divisor of a and b
        also divides a % b (since a % b = a - (a//b)*b), and vice versa.
    ======================

    Use a while loop.
    """
    # TODO: implement the Euclidean algorithm
    # Add a comment referencing the invariant above
    pass


def lcm(a, b):
    """
    Compute the least common multiple of a and b.
    Formula: lcm(a, b) = (a * b) // gcd(a, b)

    lcm(4, 6) → 12
    lcm(21, 6) → 42
    """
    # TODO: one line
    pass


def is_perfect(n):
    """
    Return True if n is a perfect number (equals sum of its proper divisors).

    Proper divisors of n: all positive divisors except n itself.

    is_perfect(6)  → True   (1+2+3=6)
    is_perfect(28) → True   (1+2+4+7+14=28)
    is_perfect(12) → False  (1+2+3+4+6=16≠12)

    Optimization: only check divisors up to n // 2.
    """
    if n < 2:
        return False
    # TODO
    pass


def prime_factorization(n):
    """
    Return the prime factorization of n as a sorted list (with repetition).

    prime_factorization(360) → [2, 2, 2, 3, 3, 5]
    prime_factorization(13)  → [13]
    prime_factorization(1)   → []

    Algorithm:
        factor = 2
        while factor * factor <= n:
            while n % factor == 0:
                factors.append(factor)
                n //= factor
            factor += 1
        if n > 1: factors.append(n)   # n itself is prime
    """
    factors = []
    # TODO
    return factors


def goldbach(n):
    """
    Find one pair (p, q) of primes where p + q = n (Goldbach's conjecture).
    n must be an even integer > 2.

    Returns the pair with the smallest p.
    Raises ValueError if n is invalid.

    goldbach(4)  → (2, 2)
    goldbach(28) → (5, 23)
    goldbach(100) → (3, 97)

    Hint: generate primes up to n using a sieve, then search for the pair.
    """
    if n <= 2 or n % 2 != 0:
        raise ValueError(f"{n} must be an even integer > 2")

    # TODO: get primes up to n, then for each prime p < n//2+1,
    # check if n-p is also prime. Return (p, n-p) for the first match.
    pass


# ══════════════════════════════════════════════════════════════════════════════
# B6: Statistical Analysis
# ══════════════════════════════════════════════════════════════════════════════

def stats(data):
    """
    Compute descriptive statistics for a list of numbers.

    Returns a dict with keys:
        count, sum, mean, min, max, range, variance, std_dev

    Constraint: Do NOT use built-in sum(), min(), max(), sorted().
    You MAY use math.sqrt() for std_dev.

    Raises ValueError if data is empty.
    """
    if not data:
        raise ValueError("Cannot compute stats of empty list")

    # TODO: use for loops to compute each statistic
    # Variance = (1/count) * sum of (x - mean)^2 for each x
    pass


def median(data):
    """
    Return the median of data.
    For even-length lists, return the average of the two middle elements.

    You MAY use Python's built-in sorted() here.

    median([1, 3, 2]) → 2
    median([1, 2, 3, 4]) → 2.5
    """
    if not data:
        raise ValueError("Cannot compute median of empty list")
    # TODO
    pass


def mode(data):
    """
    Return the most frequently occurring value.
    On a tie, return the smallest value.

    Constraint: No dictionaries. Use nested loops.

    mode([4, 7, 7, 3, 4, 7]) → 7
    mode([1, 2, 3]) → 1   (all tied; return smallest)
    """
    if not data:
        raise ValueError("Cannot compute mode of empty list")
    # TODO
    pass


def print_stats_report(data):
    """
    Print a formatted statistics report for data.
    Call stats(), median(), and mode() and display results.
    """
    s = stats(data)
    m = median(data)
    mo = mode(data)

    print("=" * 40)
    print("Statistical Report")
    print("=" * 40)
    # TODO: formatted output, e.g.:
    # Count:    15
    # Sum:      82.00
    # Mean:     5.47
    # Median:   6.00
    # Mode:     7
    # Min:      1.00
    # Max:      13.00
    # Range:    12.00
    # Variance: 10.52
    # Std Dev:  3.24
    print("=" * 40)


# ══════════════════════════════════════════════════════════════════════════════
# B7: Text Adventure Engine
# ══════════════════════════════════════════════════════════════════════════════

def run_adventure():
    """
    Run a text-based adventure game.

    World layout (rooms connected east-west):
        [0] Cave Entrance  →east→  [1] Torch Room  →east→  [2] Treasure Chamber  →east→  [3] Exit

    Each room may have one item.
    Player carries an inventory (a list of strings).

    Commands: go <direction>, look, take <item>, drop <item>, inventory, help, quit

    Win condition: reach room 3 (Exit) while carrying "torch".
    """

    # ── World data ──────────────────────────────────────────────────────────
    room_names = [
        "Cave Entrance",
        "Torch Room",
        "Treasure Chamber",
        "Exit"
    ]
    room_descs = [
        "You stand at the mouth of a dark cave. Cold air drifts outward.",
        "An iron bracket on the wall holds a burning torch.",
        "Gold coins carpet the floor. A tunnel leads east.",
        "Pale daylight streams through an opening. You can escape!"
    ]
    room_items = ["rope", "torch", "gold coin", None]

    # Exits: (north, south, east, west) — -1 means no exit
    room_exits = [
        (-1, -1,  1, -1),   # Cave Entrance → east: Torch Room
        (-1, -1,  2,  0),   # Torch Room → east: Treasure Chamber, west: Cave Entrance
        (-1, -1,  3,  1),   # Treasure Chamber → east: Exit, west: Torch Room
        (-1, -1, -1,  2),   # Exit → west: Treasure Chamber
    ]
    direction_index = {"north": 0, "south": 1, "east": 2, "west": 3}

    # ── Game state ──────────────────────────────────────────────────────────
    current_room = 0
    inventory    = []        # list of item name strings

    # ── Helpers ─────────────────────────────────────────────────────────────
    def look():
        print(f"\n[ {room_names[current_room]} ]")
        print(room_descs[current_room])
        item = room_items[current_room]
        if item:
            print(f"You see: {item}")
        else:
            print("The room is bare.")

    def show_help():
        print("\nCommands:")
        print("  look              — describe current room")
        print("  go <direction>    — move (north/south/east/west)")
        print("  take <item>       — pick up an item")
        print("  drop <item>       — drop an item")
        print("  inventory         — list carried items")
        print("  help              — show this message")
        print("  quit              — exit the game")

    # ── Game start ───────────────────────────────────────────────────────────
    print("=" * 50)
    print("   THE CAVE — A Text Adventure")
    print("=" * 50)
    print("Find the torch and escape through the Exit.")
    print("Type 'help' for commands.\n")
    look()

    # ── Main game loop ───────────────────────────────────────────────────────
    while True:
        raw = input("\n> ").strip().lower()
        if not raw:
            continue

        parts   = raw.split()
        command = parts[0]
        args    = parts[1:]          # remaining words after the command

        # TODO: implement each command:

        if command == "quit":
            print("You leave the cave. Goodbye.")
            break

        elif command == "help":
            show_help()

        elif command == "look":
            look()

        elif command == "inventory":
            # TODO: print inventory, or "You are carrying nothing." if empty
            pass

        elif command == "go":
            # TODO:
            # - if no direction given: print error
            # - if direction not in direction_index: print error
            # - look up exit index from room_exits[current_room][direction_index[direction]]
            # - if exit == -1: print "No exit that way."
            # - else: current_room = exit; call look()
            # - check win condition: if current_room == 3 and "torch" in inventory: print win, break
            pass

        elif command == "take":
            # TODO:
            # - if no item name given: print error
            # - item_name = " ".join(args)
            # - if room_items[current_room] is None: print "Nothing to take."
            # - elif room_items[current_room] != item_name: print "That's not here."
            # - else: inventory.append(item_name); room_items[current_room] = None; confirm
            pass

        elif command == "drop":
            # TODO:
            # - if no item name given: print error
            # - item_name = " ".join(args)
            # - if item_name not in inventory: print "You don't have that."
            # - elif room_items[current_room] is not None: print "No room to drop it here."
            # - else: inventory.remove(item_name); room_items[current_room] = item_name; confirm
            pass

        else:
            print(f"Unknown command: '{command}'. Type 'help' for commands.")


# ══════════════════════════════════════════════════════════════════════════════
# Test Suite
# ══════════════════════════════════════════════════════════════════════════════

def run_tests():
    """Run automated tests for B1–B6. B7 is tested interactively."""

    print("Running PS2 tests...\n")

    # ── B1 ──────────────────────────────────────────────────────────────────
    r = analyze_number(9875)
    assert r["digits"]        == [9, 8, 7, 5],  f"digits: {r['digits']}"
    assert r["digit_sum"]     == 29,             f"digit_sum: {r['digit_sum']}"
    assert r["digit_product"] == 2520,           f"digit_product: {r['digit_product']}"
    assert r["is_palindrome"] == False,          f"is_palindrome: {r['is_palindrome']}"
    assert r["largest_digit"] == 9,              f"largest_digit: {r['largest_digit']}"
    assert r["num_digits"]    == 4,              f"num_digits: {r['num_digits']}"
    assert r["digital_root"]  == 2,              f"digital_root: {r['digital_root']}"

    r2 = analyze_number(121)
    assert r2["is_palindrome"] == True,  f"121 palindrome: {r2['is_palindrome']}"
    assert r2["digital_root"]  == 4,     f"121 digital_root: {r2['digital_root']}"
    print("✓ B1 analyze_number")

    # ── B2 ──────────────────────────────────────────────────────────────────
    assert fibonacci_sequence(0) == []
    assert fibonacci_sequence(1) == [0]
    assert fibonacci_sequence(8) == [0, 1, 1, 2, 3, 5, 8, 13]
    print("✓ B2a fibonacci_sequence")

    assert geometric_sequence(2, 3, 5)   == [2, 6, 18, 54, 162]
    assert geometric_sequence(1, 2, 6)   == [1, 2, 4, 8, 16, 32]
    print("✓ B2b geometric_sequence")

    c = convergents_of_sqrt2(5)
    assert c == [(1,1),(3,2),(7,5),(17,12),(41,29)], f"convergents: {c}"
    # Verify approximation improves:
    for p, q in c:
        assert abs(p/q - 2**0.5) < 1, f"({p},{q}) doesn't approximate sqrt(2)"
    print("✓ B2c convergents_of_sqrt2")

    las = look_and_say(5)
    assert las == ["1","11","21","1211","111221"], f"look_and_say: {las}"
    print("✓ B2d look_and_say")

    # ── B3 (visual — just check they don't crash) ────────────────────────────
    import io, sys
    captured = io.StringIO()
    sys.stdout = captured

    right_triangle(5)
    diamond(3)
    multiplication_table(5)
    number_spiral(4)

    sys.stdout = sys.__stdout__
    output = captured.getvalue()
    assert len(output) > 0, "B3 functions produced no output"
    # Spot-check multiplication table
    assert "25" in output, "multiplication_table(5) should contain 25"
    print("✓ B3 pattern printers (visual check — review output manually)")

    # ── B4 ──────────────────────────────────────────────────────────────────
    assert word_frequency("the cat sat on the mat the cat") == "the"
    assert word_frequency("a b a b c")                      == "a"  # tie: 'a' < 'b'
    print("✓ B4a word_frequency")

    assert run_length_encode("aaabbbccddddee") == "3a3b2c4d2e"
    assert run_length_encode("")               == ""
    assert run_length_encode("a")              == "1a"
    print("✓ B4b run_length_encode")

    assert run_length_decode("3a3b2c4d2e") == "aaabbbccddddee"
    assert run_length_decode("")           == ""
    # Round-trip test
    for s in ["hello", "aaaaabbbcc", "x"]:
        assert run_length_decode(run_length_encode(s)) == s
    print("✓ B4c run_length_decode")

    assert is_pangram("The quick brown fox jumps over the lazy dog") == True
    assert is_pangram("Hello world") == False
    print("✓ B4d is_pangram")

    # ── B5 ──────────────────────────────────────────────────────────────────
    assert gcd(48, 18)  == 6
    assert gcd(100, 75) == 25
    assert gcd(7, 13)   == 1
    assert gcd(0, 5)    == 5
    print("✓ B5a gcd")

    assert lcm(4, 6)  == 12
    assert lcm(21, 6) == 42
    print("✓ B5b lcm")

    assert is_perfect(6)   == True
    assert is_perfect(28)  == True
    assert is_perfect(496) == True
    assert is_perfect(12)  == False
    assert is_perfect(1)   == False
    print("✓ B5c is_perfect")

    assert prime_factorization(360)  == [2, 2, 2, 3, 3, 5]
    assert prime_factorization(13)   == [13]
    assert prime_factorization(1)    == []
    assert prime_factorization(2**8) == [2]*8
    print("✓ B5d prime_factorization")

    p, q = goldbach(28)
    assert p + q == 28 and p <= q
    p2, q2 = goldbach(4)
    assert p2 == 2 and q2 == 2
    print("✓ B5e goldbach")

    # ── B6 ──────────────────────────────────────────────────────────────────
    data = [4, 7, 13, 2, 7, 3, 9, 7, 1, 5, 8, 7, 6, 4, 11]
    s = stats(data)
    assert s["count"] == 15,          f"count: {s['count']}"
    assert s["sum"]   == 94,          f"sum: {s['sum']}"
    assert abs(s["mean"] - 94/15) < 1e-9
    assert s["min"]   == 1,           f"min: {s['min']}"
    assert s["max"]   == 13,          f"max: {s['max']}"
    assert s["range"] == 12,          f"range: {s['range']}"
    print("✓ B6a stats")

    assert median([1, 3, 2])    == 2
    assert median([1, 2, 3, 4]) == 2.5
    print("✓ B6b median")

    assert mode([4, 7, 7, 3, 4, 7]) == 7
    assert mode([1, 2, 3])          == 1
    print("✓ B6c mode")

    print_stats_report(data)   # visual check
    print("✓ B6d print_stats_report (visual — review output)")

    print("\n🎉 All automated tests passed! Run B7 interactively.")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--adventure":
        run_adventure()
    else:
        run_tests()
        print("\nTo play the text adventure: python3 ps2.py --adventure")
