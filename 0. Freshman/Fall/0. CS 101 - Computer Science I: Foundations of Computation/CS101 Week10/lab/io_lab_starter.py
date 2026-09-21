#!/usr/bin/env python3
"""io_lab_starter.py — CS 101 Lab 10 scaffold."""
import csv, io, os, tempfile, time
from pathlib import Path

# ── Part 1 ───────────────────────────────────────────────────────────────────
def mode_table(tmp=Path("t.txt")):
    """Show what each open mode does to an existing file."""
    for mode in ("r", "w", "a", "r+", "w+"):
        tmp.write_text("EXISTING")
        try:
            with open(tmp, mode) as f:
                pos = f.tell()
            print(f"  {mode:3} tell={pos:<3} file after = {tmp.read_text()!r}")
        except OSError as e:
            print(f"  {mode:3} {type(e).__name__}: {e}")
    tmp.unlink(missing_ok=True)

def truncation_demo(p=Path("data.txt")):
    p.write_text("IRREPLACEABLE")
    try:
        with open(p, "w") as f:
            raise RuntimeError("simulated failure before writing")
    except RuntimeError:
        pass
    print(f"  after crash during open('w'): {p.read_text()!r}")
    p.unlink(missing_ok=True)

def atomic_write(path, data, encoding="utf-8"):
    """TODO: temp in the TARGET's dir, fsync, os.replace, cleanup on BaseException."""
    raise NotImplementedError

# ── Part 2 ───────────────────────────────────────────────────────────────────
def encoding_demo(p=Path("enc.txt")):
    p.write_text("café 日本語", encoding="utf-8")
    print("  raw bytes:", open(p, "rb").read())
    print("  utf-8    :", repr(open(p, encoding="utf-8").read()))
    try:
        open(p, encoding="ascii").read()
    except UnicodeDecodeError as e:
        print(f"  ascii    : UnicodeDecodeError ({e.reason}) at byte {e.start}")
    print("  replace  :", repr(open(p, encoding="ascii", errors="replace").read()))
    p.unlink(missing_ok=True)

# ── Part 3 ───────────────────────────────────────────────────────────────────
def ordering_demo(fail):
    log = []
    try:
        log.append("try")
        if fail: raise ValueError("x")
        log.append("try-end")
    except ValueError:
        log.append("except")
    else:
        log.append("else")
    finally:
        log.append("finally")
    return log

# ── Part 4 ───────────────────────────────────────────────────────────────────
def load_records(path):
    """TODO: return (good, bad); header is line 1 so data starts at line 2.
       Catch KeyError, ValueError AND TypeError."""
    raise NotImplementedError

if __name__ == "__main__":
    print("Part 1 — modes:");        mode_table()
    print("\nPart 1 — truncation:"); truncation_demo()
    print("\nPart 2 — encoding:");   encoding_demo()
    print("\nPart 3 — ordering:")
    print("  no exception:", ordering_demo(False))
    print("  exception   :", ordering_demo(True))
    print("\nRemaining parts: implement the TODOs.")
