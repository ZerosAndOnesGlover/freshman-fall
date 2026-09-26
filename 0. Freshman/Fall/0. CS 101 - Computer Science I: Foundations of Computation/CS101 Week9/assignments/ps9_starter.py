#!/usr/bin/env python3
"""
ps9_starter.py — CS 101 Problem Set 9 scaffold
Strings, Text Processing, and Regular Expressions

Rename to ps9.py and implement every function marked TODO.
Run this file directly to see which tests pass:  python3 ps9.py

Every function must handle the empty string without crashing.
"""

import re
import csv
import io
import unicodedata
from collections import Counter

# ─────────────────────────── B1: normalisation and counting ──────────────────

def normalise(text):
    """NFC-normalise and casefold `text`. Returns a str.

    >>> normalise("CAFÉ") == normalise("café")
    True
    """
    # TODO: apply unicodedata.normalize("NFC", ...) then .casefold()
    raise NotImplementedError


def word_frequencies(text):
    """Counter of normalised words. A word is a run of [\\w'].

    >>> word_frequencies("The the QUICK").most_common()
    [('the', 2), ('quick', 1)]
    """
    # TODO: re.findall(r"[\w']+", text), normalise each, feed to Counter
    raise NotImplementedError


# ─────────────────────────── B2: two-pointer palindrome ──────────────────────

def is_palindrome(s):
    """True if s reads the same both ways, ignoring case, punctuation and
    Unicode composition.  MUST use two pointers and O(1) extra space —
    no slicing, no filtered list.

    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("!!!")
    True
    """
    # TODO: normalise ONCE on the whole string, then walk i up and j down,
    #       skipping non-alphanumeric characters. Re-check i < j in each
    #       inner loop or an all-punctuation string will run off the end.
    raise NotImplementedError


# ─────────────────────────── Part C helper: your Lab 9 log pattern ───────────

# Paste the verbose, anchored, named-group pattern from Lab 9 Exercise 3.2 here
# (named groups: date, time, level, message).
LOG = re.compile(r"""
    # your pattern here
""", re.VERBOSE)


# ─────────────────────────── B3: splitting and doubled words ─────────────────

def split_fields(line):
    """Split one comma-separated line, honouring quoted fields.

    >>> split_fields('name,"Smith, John",42')
    ['name', 'Smith, John', '42']
    """
    # TODO: use the csv module — do NOT hand-roll this
    raise NotImplementedError


def collapse_whitespace(s):
    """Every run of whitespace becomes one space; ends stripped."""
    # TODO
    raise NotImplementedError


def find_doubled_words(text):
    """Words appearing twice in a row, exactly (same case).

    >>> find_doubled_words("the the quick Fox fox fox")
    ['the', 'fox']
    """
    # TODO: a backreference (\1) is the whole trick here (L30 §3)
    raise NotImplementedError


# ─────────────────────────── Part C: log analyser ────────────────────────────

SAMPLE_LOG = [
    "2026-12-01 09:15:02 INFO server started",
    "2026-12-01 11:02:33 ERROR disk full",
    "2026-12-01 11:05:10 WARN disk nearly full",
    "this line is not a log entry",
    "2026-12-01 11:40:00 ERROR disk full again",
    "2026-12-01 14:00:00 INFO backup complete",
    "2026-12-01 11:59:59 INFO user login",
    "",
]

def analyse_log(lines):
    """One pass over a list of log lines; return the summary dict described in the handout.

    Keys: total_lines, parsed, malformed, by_level, busiest_hour, top_words
    """
    # TODO
    raise NotImplementedError


# ─────────────────────────── self-test ───────────────────────────────────────

def _check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        got  {got!r}\n        want {want!r}")
    return ok


def main():
    print("PS9 self-test\n")
    passed = total = 0
    tests = [
        ("normalise idempotent",      lambda: normalise("CAFÉ") == normalise("café"), True),
        ("word_frequencies",          lambda: word_frequencies("The the QUICK").most_common(), [('the', 2), ('quick', 1)]),
        ("palindrome empty",          lambda: is_palindrome(""), True),
        ("palindrome punctuation",    lambda: is_palindrome("!!!"), True),
        ("palindrome classic",        lambda: is_palindrome("A man, a plan, a canal: Panama"), True),
        ("palindrome negative",       lambda: is_palindrome("ab"), False),
        ("split_fields quoted",       lambda: split_fields('name,"Smith, John",42'), ['name', 'Smith, John', '42']),
        ("collapse_whitespace",       lambda: collapse_whitespace("  a   b \t\n c  "), "a b c"),
        ("find_doubled_words",        lambda: find_doubled_words("the the quick Fox fox fox"), ['the', 'fox']),
        ("analyse_log sample",        lambda: analyse_log(SAMPLE_LOG)["busiest_hour"], "11"),
    ]
    for label, fn, want in tests:
        total += 1
        try:
            passed += _check(label, fn(), want)
        except NotImplementedError:
            print(f"  TODO  {label}")
        except Exception as exc:                       # noqa: BLE001
            print(f"  ERROR {label}: {type(exc).__name__}: {exc}")
    print(f"\n{passed}/{total} passing")


if __name__ == "__main__":
    main()
