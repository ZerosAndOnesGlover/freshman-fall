#!/usr/bin/env python3
"""PROG 202 · Week 1 · L03 §4 — what a type synonym costs, counted.

Generates all 120 orderings of a Session's five field values, writes each as a
one-line Haskell file, and compiles every one. Counts how many the type accepts.

    python3 orderings.py            # the Week 0 tuple
    python3 orderings.py middle     # Day/Kind as sums, Course/Minutes newtypes
    python3 orderings.py strict     # a distinct newtype per field

Measured on GHC 9.4.7:

    tuple   120 tried, 12 accepted, 11 of them wrong
    middle  120 tried,  2 accepted,  1 of them wrong  -- start/end swapped
    strict  120 tried,  1 accepted,  0 of them wrong

Takes about a minute per design: it really does run ghc 120 times.
"""
import itertools
import os
import subprocess
import sys
import tempfile

TUPLE = ("type Session = (String, String, String, Int, Int)\n",
         ['"PROG 202"', '"LEC"', '"Tue"', '660', '735'],
         "s = (%s)\n" )

MIDDLE = ("""data Day  = Mon | Tue | Wed | Thu | Fri deriving (Show, Eq, Ord, Enum, Bounded)
data Kind = LEC | LAB | REC | SEM       deriving (Show, Eq, Ord, Enum, Bounded)
newtype Course  = Course String         deriving (Show, Eq, Ord)
newtype Minutes = Minutes Int           deriving (Show, Eq, Ord)
data Session = Session
  { course :: Course, kind :: Kind, day :: Day, start :: Minutes, end :: Minutes }
  deriving (Show, Eq)
""",
          ['(Course "PROG 202")', 'LEC', 'Tue', '(Minutes 660)', '(Minutes 735)'],
          "s = Session %s\n")

STRICT = ("""newtype Course = Course String deriving (Show, Eq, Ord)
newtype Kind   = Kind   String deriving (Show, Eq, Ord)
newtype Day    = Day    String deriving (Show, Eq, Ord)
newtype Start  = Start  Int    deriving (Show, Eq, Ord)
newtype End    = End    Int    deriving (Show, Eq, Ord)
data Session = Session
  { course :: Course, kind :: Kind, day :: Day, start :: Start, end :: End }
  deriving (Show, Eq)
""",
          ['(Course "PROG 202")', '(Kind "LEC")', '(Day "Tue")', '(Start 660)', '(End 735)'],
          "s = Session %s\n")

DESIGNS = {"tuple": TUPLE, "middle": MIDDLE, "strict": STRICT}


def run(name):
    preamble, fields, body = DESIGNS[name]
    joiner = ", " if name == "tuple" else " "
    accepted, total = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, perm in enumerate(itertools.permutations(range(5))):
            total += 1
            vals = joiner.join(fields[j] for j in perm)
            src = (preamble + "\ns :: Session\n" + body % vals
                   + "\nmain :: IO ()\nmain = print s\n")
            path = os.path.join(tmp, "P%03d.hs" % i)
            with open(path, "w") as fh:
                fh.write(src)
            if subprocess.run(["ghc", "-fno-code", "-v0", path],
                              capture_output=True).returncode == 0:
                accepted.append(perm)
    right = (0, 1, 2, 3, 4)
    print("design               : %s" % name)
    print("orderings tried      : %d" % total)
    print("accepted by the type : %d" % len(accepted))
    print("intended order       : %s" % (right in accepted))
    wrong = [p for p in accepted if p != right]
    print("wrong but accepted   : %d" % len(wrong))
    if 0 < len(wrong) <= 4:
        print("                       %s" % wrong)


if __name__ == "__main__":
    for arg in (sys.argv[1:] or ["tuple"]):
        if arg not in DESIGNS:
            sys.exit("usage: orderings.py [tuple|middle|strict] ...")
        run(arg)
        print()
