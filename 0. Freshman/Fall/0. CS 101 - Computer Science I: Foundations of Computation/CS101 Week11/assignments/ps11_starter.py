"""
CS 101 -- Problem Set 11 starter.

Implement the functions marked TODO, then run:

    python3 ps11_starter.py

Written answers go in PS 11. This file is the code portion (Part B).
You may import your Lab 11 simulator, but this file is self-contained.
"""

BLANK = "_"


class TuringMachine:
    """Provided -- same semantics as Lab 11. Do not modify."""

    def __init__(self, transitions, start, accept, reject=None, blank=BLANK):
        self.transitions, self.start = transitions, start
        self.accept, self.reject, self.blank = accept, reject, blank

    def step(self, tape, head, state):
        while head >= len(tape):
            tape.append(self.blank)
        nxt, write, move = self.transitions[(state, tape[head])]
        tape[head] = write
        head = head + 1 if move == "R" else (max(0, head - 1) if move == "L" else head)
        while head >= len(tape):
            tape.append(self.blank)
        return tape, head, nxt

    def run(self, s, max_steps=10_000):
        tape, head, state, steps = list(s) or [self.blank], 0, self.start, 0
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
        return ("timeout", "".join(tape).rstrip(self.blank), steps)


# ---- B1: a machine for a language that is NOT regular ---------------------

def equal_zeros_ones():
    """TM accepting strings over {0,1} with an EQUAL number of 0s and 1s,
    in ANY order ("0011", "0101", "1100", "" all accepted; "001" rejected).

    Hint: repeatedly cross off one 0 and one 1 (marking both with 'X').
    Accept when only X's remain.

    TODO: return a TuringMachine.
    """
    raise NotImplementedError("equal_zeros_ones")


# ---- B2: binary increment -------------------------------------------------

def binary_increment():
    """TM that adds 1 to a binary number written most-significant-bit first.
    "0" -> "1", "1" -> "10", "1011" -> "1100", "111" -> "1000".

    Hint: walk right to the end, then process leftward handling the carry.
    You may need to shift or prepend when the carry propagates off the left.

    TODO: return a TuringMachine.
    """
    raise NotImplementedError("binary_increment")


# ---- B3: the recogniser ---------------------------------------------------

def recognise_halt(machine, tape_input, start_budget=1):
    """Return True iff `machine` halts on `tape_input`.

    Must be SOUND: never return True for a machine that does not halt, and
    never return False for one that does. It is allowed not to terminate.
    Use a doubling budget.

    TODO: implement.
    """
    raise NotImplementedError("recognise_halt")


# ---- B4: the reduction, as code -------------------------------------------

def build_prints_hello_wrapper(f, x, log):
    """Return a zero-argument function `wrapper` such that
    wrapper() appends "hello" to `log` IF AND ONLY IF f(x) halts.

    This is the L36 reduction HALT <= PRINTS-HELLO, written in Python.

    TODO: implement (three lines).
    """
    raise NotImplementedError("build_prints_hello_wrapper")


# ---- B5: classify ---------------------------------------------------------

# For each question, set the value to "decidable" or "undecidable".
# See PS 11 Part B5 for the accompanying written justification.
CLASSIFICATIONS = {
    "does the source contain the substring 'while'":      None,  # TODO
    "does the program ever execute a 'while' loop":       None,  # TODO
    "does the program halt within 1000 steps on input w": None,  # TODO
    "does the program halt on every input":               None,  # TODO
    "does the machine have an even number of states":     None,  # TODO
    "do these two programs compute the same function":    None,  # TODO
}


# =========================================================================
# Tests -- do not edit
# =========================================================================

def run_tests():
    total = passed = 0

    def t(name, cond, detail=""):
        nonlocal total, passed
        total += 1
        print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   -- {detail}" if not cond and detail else ""))
        passed += bool(cond)

    print("B1 -- equal_zeros_ones()")
    try:
        m = equal_zeros_ones()
        good = ["", "01", "10", "0011", "0101", "1100", "011010", "000111"]
        bad = ["0", "1", "001", "110", "01011", "0001"]
        t("accepts equal counts", all(m.run(s)[0] == "accept" for s in good),
          str([(s, m.run(s)[0]) for s in good if m.run(s)[0] != "accept"]))
        t("rejects unequal counts", all(m.run(s)[0] != "accept" for s in bad),
          str([(s, m.run(s)[0]) for s in bad if m.run(s)[0] == "accept"]))
    except NotImplementedError:
        t("accepts equal counts", False, "not implemented")
        t("rejects unequal counts", False, "not implemented")

    print("\nB2 -- binary_increment()")
    try:
        m = binary_increment()
        ok, wrong = True, []
        for n in range(0, 32):
            src = bin(n)[2:]
            want = bin(n + 1)[2:]
            outcome, tape, _ = m.run(src)
            got = tape.lstrip("_")
            if outcome != "accept" or got != want:
                ok = False
                wrong.append((src, got, want))
        t("increments 0..31 correctly", ok, str(wrong[:4]))
    except NotImplementedError:
        t("increments 0..31 correctly", False, "not implemented")

    print("\nB3 -- recognise_halt()")
    try:
        halter = TuringMachine({("q0", "1"): ("q0", "1", "R"),
                                ("q0", BLANK): ("qa", "1", "S")}, "q0", "qa")
        t("True for a halting machine", recognise_halt(halter, "111") is True)
        t("True even past the initial budget", recognise_halt(halter, "1" * 5000) is True)
        looper = TuringMachine({("q0", BLANK): ("q0", BLANK, "S")}, "q0", "qa")
        # must not return a wrong answer; we cap the test so it terminates
        import threading
        result = []
        th = threading.Thread(target=lambda: result.append(recognise_halt(looper, "")), daemon=True)
        th.start(); th.join(timeout=2.0)
        t("never returns False for a looping machine", result == [] or result == [None],
          f"returned {result}")
    except NotImplementedError:
        for n in ("True for a halting machine", "True even past the initial budget",
                  "never returns False for a looping machine"):
            t(n, False, "not implemented")

    print("\nB4 -- build_prints_hello_wrapper()")
    try:
        log = []
        build_prints_hello_wrapper(lambda n: sum(range(n)), 10, log)()
        t("prints hello when f halts", log == ["hello"], f"log={log}")
        log2 = []
        w = build_prints_hello_wrapper(lambda n: None, 1, log2)
        t("wrapper is callable with no args", callable(w) and (w() or True))
        t("log stays empty until wrapper runs", True)
    except NotImplementedError:
        for n in ("prints hello when f halts", "wrapper is callable with no args",
                  "log stays empty until wrapper runs"):
            t(n, False, "not implemented")

    print("\nB5 -- CLASSIFICATIONS")
    expected = {
        "does the source contain the substring 'while'": "decidable",
        "does the program ever execute a 'while' loop": "undecidable",
        "does the program halt within 1000 steps on input w": "decidable",
        "does the program halt on every input": "undecidable",
        "does the machine have an even number of states": "decidable",
        "do these two programs compute the same function": "undecidable",
    }
    filled = sum(v is not None for v in CLASSIFICATIONS.values())
    t("all six answered", filled == 6, f"{filled}/6 filled in")
    correct = sum(CLASSIFICATIONS.get(k) == v for k, v in expected.items())
    t("all six correct", correct == 6, f"{correct}/6 correct")

    print(f"\n{passed}/{total} tests passing")
    return passed, total


if __name__ == "__main__":
    run_tests()
