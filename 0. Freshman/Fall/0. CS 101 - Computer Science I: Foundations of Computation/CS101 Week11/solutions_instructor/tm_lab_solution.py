"""
CS 101 -- Lab 11 REFERENCE SOLUTION: a Turing machine simulator.

Fill in the TODOs. Run this file to see which tests pass:

    python3 tm_lab_starter.py

Every test that passes prints PASS; failures print FAIL with an explanation.
Do not edit the tests -- edit the implementation above them.
"""

BLANK = "_"


class Halted(Exception):
    """Raised internally when the machine reaches a halting state."""
    def __init__(self, accepted, tape, steps):
        self.accepted, self.tape, self.steps = accepted, tape, steps


class TuringMachine:
    """A single-tape, one-way-infinite Turing machine.

    transitions: dict mapping (state, symbol) -> (next_state, write_symbol, move)
                 where move is "L", "R", or "S" (stay).
    """

    def __init__(self, transitions, start, accept, reject=None, blank=BLANK):
        self.transitions = transitions
        self.start = start
        self.accept = accept
        self.reject = reject
        self.blank = blank

    # ---- Part 2 ---------------------------------------------------------
    def step(self, tape, head, state):
        # Invariant: on entry AND on return, head is a valid index into tape.
        while head >= len(tape):
            tape.append(self.blank)
        next_state, write, move = self.transitions[(state, tape[head])]
        tape[head] = write
        if move == "R":
            head += 1
        elif move == "L":
            head = max(0, head - 1)   # one-way-infinite tape: clamp at the left edge
        # Re-establish the invariant after moving right off the end.
        while head >= len(tape):
            tape.append(self.blank)
        return tape, head, next_state

    # ---- Part 3 ---------------------------------------------------------
    def run(self, input_string, max_steps=10_000, trace=False):
        tape = list(input_string) or [self.blank]
        head, state, steps = 0, self.start, 0
        while steps < max_steps:
            if state == self.accept:
                return ("accept", "".join(tape).rstrip(self.blank), steps)
            if state == self.reject:
                return ("reject", "".join(tape).rstrip(self.blank), steps)
            try:
                tape, head, state = self.step(tape, head, state)
            except KeyError:
                return ("stuck", "".join(tape).rstrip(self.blank), steps)
            steps += 1
            if trace:
                print(f"    {steps:>4}: {''.join(tape)!r} head={head} state={state}")
        return ("timeout", "".join(tape).rstrip(self.blank), steps)


# ---- Part 4: build these machines ---------------------------------------

def unary_increment():
    return TuringMachine({("q0", "1"): ("q0", "1", "R"),
                          ("q0", BLANK): ("qa", "1", "S")}, "q0", "qa")


def even_ones():
    return TuringMachine({
        ("even", "0"): ("even", "0", "R"), ("even", "1"): ("odd", "1", "R"),
        ("even", BLANK): ("qa", BLANK, "S"),
        ("odd", "0"): ("odd", "0", "R"), ("odd", "1"): ("even", "1", "R"),
        ("odd", BLANK): ("qr", BLANK, "S"),
    }, "even", "qa", "qr")


def a_n_b_n():
    return TuringMachine({
        ("q0", "a"): ("q1", "X", "R"), ("q0", "Y"): ("q3", "Y", "R"),
        ("q0", BLANK): ("qa", BLANK, "S"),
        ("q1", "a"): ("q1", "a", "R"), ("q1", "Y"): ("q1", "Y", "R"),
        ("q1", "b"): ("q2", "Y", "L"),
        ("q2", "a"): ("q2", "a", "L"), ("q2", "Y"): ("q2", "Y", "L"),
        ("q2", "X"): ("q0", "X", "R"),
        ("q3", "Y"): ("q3", "Y", "R"), ("q3", BLANK): ("qa", BLANK, "S"),
    }, "q0", "qa")


# =========================================================================
# Tests -- do not edit
# =========================================================================

def _check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   -- {detail}" if not cond and detail else ""))
    return bool(cond)


def run_tests():
    total = passed = 0

    def t(name, cond, detail=""):
        nonlocal total, passed
        total += 1
        passed += _check(name, cond, detail)

    print("Part 2 -- step()")
    try:
        m = TuringMachine({("q0", "1"): ("q0", "1", "R")}, "q0", "qa")
        tape, head, state = m.step(["1", "1"], 0, "q0")
        t("step moves right", head == 1 and state == "q0", f"got head={head} state={state}")
        tape, head, state = m.step(["1"], 0, "q0")
        t("step extends tape with blank", len(tape) >= 2 and tape[1] == BLANK, f"got tape={tape}")
        m2 = TuringMachine({("q0", "1"): ("q0", "1", "L")}, "q0", "qa")
        tape, head, state = m2.step(["1"], 0, "q0")
        t("step clamps at left edge", head == 0, f"got head={head}")
        try:
            m.step(["0"], 0, "q0")
            t("step raises KeyError when stuck", False, "no exception raised")
        except KeyError:
            t("step raises KeyError when stuck", True)
    except NotImplementedError:
        for n in ("step moves right", "step extends tape with blank",
                  "step clamps at left edge", "step raises KeyError when stuck"):
            t(n, False, "step() not implemented")

    print("\nPart 3+4 -- unary_increment()")
    try:
        inc = unary_increment()
        ok = True
        for n in range(6):
            outcome, tape, steps = inc.run("1" * n)
            if outcome != "accept" or tape != "1" * (n + 1):
                ok = False
        t("increments 0..5 correctly", ok)
        _, _, s3 = inc.run("111")
        t("takes n+1 steps on n ones", s3 == 4, f"got {s3} steps on '111', expected 4")
    except NotImplementedError:
        t("increments 0..5 correctly", False, "not implemented")
        t("takes n+1 steps on n ones", False, "not implemented")

    print("\nPart 3+4 -- even_ones()")
    try:
        ev = even_ones()
        ok = True
        for s in ["", "0", "1", "11", "101", "1111", "10101", "0110"]:
            outcome, _, _ = ev.run(s)
            if (outcome == "accept") != (s.count("1") % 2 == 0):
                ok = False
        t("accepts exactly the even-parity strings", ok)
    except NotImplementedError:
        t("accepts exactly the even-parity strings", False, "not implemented")

    print("\nPart 3+4 -- a_n_b_n()")
    try:
        anbn = a_n_b_n()
        good = ["", "ab", "aabb", "aaabbb", "aaaabbbb"]
        bad = ["a", "b", "ba", "aab", "abb", "aabbb", "aaabb", "abab"]
        ok_good = all(anbn.run(s)[0] == "accept" for s in good)
        ok_bad = all(anbn.run(s)[0] != "accept" for s in bad)
        t("accepts a^n b^n", ok_good,
          str([(s, anbn.run(s)[0]) for s in good if anbn.run(s)[0] != "accept"]))
        t("rejects everything else", ok_bad,
          str([(s, anbn.run(s)[0]) for s in bad if anbn.run(s)[0] == "accept"]))
    except NotImplementedError:
        t("accepts a^n b^n", False, "not implemented")
        t("rejects everything else", False, "not implemented")

    print("\nPart 3 -- termination guards")
    try:
        loop = TuringMachine({("q0", BLANK): ("q0", BLANK, "S")}, "q0", "qa")
        outcome, _, steps = loop.run("", max_steps=500)
        t("timeout is reported, not hung", outcome == "timeout" and steps == 500,
          f"got outcome={outcome} steps={steps}")
        stuck = TuringMachine({}, "q0", "qa")
        t("stuck is reported", stuck.run("x")[0] == "stuck", f"got {stuck.run('x')[0]}")
    except NotImplementedError:
        t("timeout is reported, not hung", False, "not implemented")
        t("stuck is reported", False, "not implemented")

    print(f"\n{passed}/{total} tests passing")
    return passed, total


if __name__ == "__main__":
    run_tests()
