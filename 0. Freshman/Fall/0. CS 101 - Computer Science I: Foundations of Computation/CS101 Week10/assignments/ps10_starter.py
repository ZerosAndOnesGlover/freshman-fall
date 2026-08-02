#!/usr/bin/env python3
"""
ps10_starter.py — CS 101 Problem Set 10 scaffold
Files, I/O, and Error Handling

Rename to ps10.py and implement every function marked TODO.
Run directly to see which tests pass:  python3 ps10.py

Every function must survive a missing file, an empty file, and a malformed row.
"""

import csv
import io
import json
import os
import tempfile
from pathlib import Path

# ─────────────────────────── exception types ─────────────────────────────────

class DataError(Exception):
    """Base for every data-pipeline failure."""

class SourceMissing(DataError):
    """A required input file does not exist."""

class SourceMalformed(DataError):
    """An input file exists but could not be understood."""


# ─────────────────────────── B1: counting ────────────────────────────────────

def count_lines(path):
    """Number of lines in a text file. Stream — do not load it all.

    >>> count_lines("empty.txt")
    0
    """
    # TODO: open with an explicit encoding and sum over the file object
    raise NotImplementedError


# ─────────────────────────── B2: config loading ──────────────────────────────

def read_config(path):
    """Return a dict from a JSON file.

    SourceMissing   — file absent
    SourceMalformed — invalid JSON, or valid JSON that is not an object
    DataError       — any other OS failure
    Every raise must preserve its cause with `from`.
    """
    # TODO: catch FileNotFoundError BEFORE OSError (specific first)
    #       then json.JSONDecodeError, then check isinstance(data, dict)
    raise NotImplementedError


# ─────────────────────────── B3: atomic write ────────────────────────────────

def atomic_write(path, data, encoding="utf-8"):
    """Write data to path so path is never left partially written.

    Requirements: temp file in the TARGET's directory; fsync before rename;
    os.replace (not os.rename); cleanup under BaseException.
    """
    # TODO
    raise NotImplementedError


# ─────────────────────────── B4: defensive CSV ───────────────────────────────

def load_records(path):
    """Return (good, bad).

    good — [{"name": str, "score": int}, ...]
    bad  — [(line_number, reason), ...]   header is line 1, first data row is 2

    One malformed row must not abort the rest.
    """
    # TODO: csv.DictReader, enumerate(..., start=2)
    #       catch KeyError, ValueError AND TypeError — a short row yields None,
    #       and int(None) raises TypeError, not ValueError
    raise NotImplementedError


# ─────────────────────────── B5: writing and summarising ─────────────────────

def save_records(path, records):
    """Write records to CSV with a header, atomically, with correct quoting."""
    # TODO: format into io.StringIO(newline="") then hand to atomic_write
    raise NotImplementedError


def summarise(records):
    """{"count", "mean", "best"} — empty input gives count 0, mean 0.0, best None."""
    # TODO
    raise NotImplementedError


# ─────────────────────────── Part C: the pipeline ────────────────────────────

def run_pipeline(config_path):
    """Read config (input, output, optional min_score), load, filter, save, summarise."""
    # TODO
    raise NotImplementedError


# ─────────────────────────── self-test ───────────────────────────────────────

def _tmpdir():
    d = Path(tempfile.mkdtemp(prefix="ps10_"))
    (d / "empty.txt").write_text("")
    (d / "three.txt").write_text("a\nb\nc\n")
    (d / "nonl.txt").write_text("a\nb\nc")
    (d / "ok.json").write_text('{"a": 1}')
    (d / "bad.json").write_text("{oops}")
    (d / "arr.json").write_text("[1, 2]")
    (d / "recs.csv").write_text(
        'name,score\nAda,95\n"Smith, John",88\nBob,notanumber\nCy\nDee,70\n')
    (d / "keep.txt").write_text("ORIGINAL")
    return d


def _check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        got  {got!r}\n        want {want!r}")
    return ok


def _raises(label, fn, exc_type):
    try:
        fn()
    except exc_type:
        print(f"  PASS  {label}")
        return True
    except NotImplementedError:
        print(f"  TODO  {label}")
        return False
    except Exception as e:                                   # noqa: BLE001
        print(f"  FAIL  {label}: raised {type(e).__name__}, wanted {exc_type.__name__}")
        return False
    print(f"  FAIL  {label}: no exception, wanted {exc_type.__name__}")
    return False


def main():
    d = _tmpdir()
    print(f"PS10 self-test  (scratch dir {d})\n")
    passed = total = 0

    value_tests = [
        ("count_lines empty",        lambda: count_lines(d / "empty.txt"), 0),
        ("count_lines 3 lines",      lambda: count_lines(d / "three.txt"), 3),
        ("count_lines no final \\n", lambda: count_lines(d / "nonl.txt"),  3),
        ("read_config valid",        lambda: read_config(d / "ok.json"), {"a": 1}),
        ("load_records good count",  lambda: len(load_records(d / "recs.csv")[0]), 3),
        ("load_records bad count",   lambda: len(load_records(d / "recs.csv")[1]), 2),
        ("load_records quoted comma",lambda: load_records(d / "recs.csv")[0][1]["name"], "Smith, John"),
        ("load_records bad linenos", lambda: [n for n, _ in load_records(d / "recs.csv")[1]], [4, 5]),
        ("summarise empty",          lambda: summarise([]), {"count": 0, "mean": 0.0, "best": None}),
        ("summarise best",           lambda: summarise(load_records(d / "recs.csv")[0])["best"], "Ada"),
    ]
    for label, fn, want in value_tests:
        total += 1
        try:
            passed += _check(label, fn(), want)
        except NotImplementedError:
            print(f"  TODO  {label}")
        except Exception as e:                               # noqa: BLE001
            print(f"  ERROR {label}: {type(e).__name__}: {e}")

    raise_tests = [
        ("read_config missing -> SourceMissing",   lambda: read_config(d / "nope.json"), SourceMissing),
        ("read_config bad json -> SourceMalformed",lambda: read_config(d / "bad.json"),  SourceMalformed),
        ("read_config array -> SourceMalformed",   lambda: read_config(d / "arr.json"),  SourceMalformed),
    ]
    for label, fn, exc in raise_tests:
        total += 1
        passed += _raises(label, fn, exc)

    # atomic_write: original must survive a failed write
    total += 1
    try:
        atomic_write(d / "keep.txt", "REPLACED")
        ok = (d / "keep.txt").read_text() == "REPLACED" and not list(d.glob("*.tmp"))
        passed += _check("atomic_write replaces and leaves no .tmp", ok, True)
    except NotImplementedError:
        print("  TODO  atomic_write replaces and leaves no .tmp")

    print(f"\n{passed}/{total} passing")


if __name__ == "__main__":
    main()
