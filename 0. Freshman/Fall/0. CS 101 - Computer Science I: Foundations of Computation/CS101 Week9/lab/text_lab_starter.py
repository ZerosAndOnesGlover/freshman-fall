#!/usr/bin/env python3
"""text_lab_starter.py — CS 101 Lab 9 scaffold."""
import re, time, timeit

# ── Part 1 ───────────────────────────────────────────────────────────────────
def bench_concat_vs_join(sizes=(2000, 8000, 32000)):
    """Print the MISLEADING benchmark (refcount optimisation active)."""
    for n in sizes:
        t_cat  = timeit.timeit("s=''\nfor c in src: s+=c", setup=f"src='x'*{n}", number=3)/3
        t_join = timeit.timeit("''.join(src)",             setup=f"src='x'*{n}", number=3)/3
        print(f"  n={n:>6}  concat {t_cat*1000:8.3f} ms  join {t_join*1000:7.4f} ms  ratio {t_cat/t_join:5.0f}x")

def bench_concat_honest(sizes=(2000, 8000, 32000)):
    """TODO: keep a live alias so the in-place resize cannot fire."""
    raise NotImplementedError

# ── Part 2 ───────────────────────────────────────────────────────────────────
def naive_search(haystack, needle):
    """TODO: return (index, comparisons). Empty needle -> (0, 0)."""
    raise NotImplementedError

def compare_search(sizes=(2000, 8000, 32000), k=50):
    """TODO: table of comparisons, formula (n-k)(k+1), naive time, str.find time."""
    raise NotImplementedError

# ── Part 3 ───────────────────────────────────────────────────────────────────
LOG = re.compile(r"""
    # TODO: anchored, verbose, named groups: date time level message
""", re.VERBOSE)

def parse_logs(lines):
    """TODO: skip malformed lines."""
    raise NotImplementedError

def valid_email_fullmatch(s):
    """TODO: correct version."""
    raise NotImplementedError

def valid_email_search(s):
    """TODO: deliberately wrong version — find an input it wrongly accepts."""
    raise NotImplementedError

# ── Part 4 ───────────────────────────────────────────────────────────────────
def redos_demo(sizes=(18, 20, 22, 24)):
    """Time ^(a+)+$ against 'a'*n + '!'.  DO NOT exceed n=26."""
    bad = re.compile(r"^(a+)+$")
    prev = None
    for n in sizes:
        s = "a"*n + "!"
        t0 = time.perf_counter(); bad.search(s); el = time.perf_counter() - t0
        ratio = f"{el/prev:5.1f}x" if prev else "   —"
        print(f"  {n} a's: {el*1000:9.2f} ms   ratio {ratio}")
        prev = el
    good = re.compile(r"^a+$")
    t0 = time.perf_counter(); good.search("a"*100000 + "!")
    print(f"  safe ^a+$ on 100000 a's: {(time.perf_counter()-t0)*1000:.3f} ms")

# ── Part 5 ───────────────────────────────────────────────────────────────────
def html_boundary():
    for html in ('<a href="x">link</a>', '<a href="a>b">link</a>'):
        print(f"  {html!r:26} -> {re.sub(r'<.*?>', '', html)!r}")

if __name__ == "__main__":
    print("Part 1 (misleading):");  bench_concat_vs_join()
    print("\nPart 4 (ReDoS):");     redos_demo()
    print("\nPart 5 (HTML):");      html_boundary()
    print("\nRemaining parts: implement the TODOs.")
