"""
CS 101 -- Project 2 REFERENCE CORE (instructor).

This file is a SCAFFOLD, not a solution. It gives you the Tracer contract that
the rest of your project depends on, one worked algorithm (bubble sort) as a
model, and a self-test you can run at any time:

    python3 project2_starter.py

You are expected to replace and extend this heavily. The only thing you must
NOT change is the Tracer's recorded-frame format, because the grading harness
and your own renderer both depend on it.

Frame format:  (event, snapshot, indices)
    event    -- "compare" | "swap" | "write"
    snapshot -- a COPY of the full array at that moment (list)
    indices  -- tuple of the positions involved
"""


class Tracer:
    """Wraps an array and records every operation performed on it.

    All algorithms must go through this class. Touching `tracer.data`
    directly bypasses instrumentation and will cost you marks.
    """

    def __init__(self, data):
        self.data = list(data)
        self.frames = []
        self.comparisons = 0
        self.swaps = 0
        self.reads = 0
        self.writes = 0

    def compare(self, i, j):
        """Record a comparison of positions i and j. Returns (data[i], data[j])."""
        self.comparisons += 1
        self.reads += 2
        self.frames.append(("compare", list(self.data), (i, j)))
        return self.data[i], self.data[j]

    def compare_value(self, i, value):
        """Record a comparison of position i against an external `value`.

        Needed by search algorithms, where the target is not in the array.
        The recorded frame uses a one-element index tuple.
        """
        self.comparisons += 1
        self.reads += 1
        self.frames.append(("compare", list(self.data), (i,)))
        return self.data[i]

    def swap(self, i, j):
        """Record and perform a swap of positions i and j."""
        self.swaps += 1
        self.writes += 2
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.frames.append(("swap", list(self.data), (i, j)))

    def write(self, i, value):
        """Record and perform a write of `value` into position i."""
        self.writes += 1
        self.data[i] = value
        self.frames.append(("write", list(self.data), (i,)))

    def stats(self):
        return {"comparisons": self.comparisons, "swaps": self.swaps,
                "reads": self.reads, "writes": self.writes,
                "frames": len(self.frames)}


# =========================================================================
# Algorithms -- bubble_sort is worked for you as a model. Implement the rest.
# =========================================================================

def bubble_sort(t):
    """WORKED EXAMPLE. Note: every read goes through t.compare, every
    mutation through t.swap. Your algorithms must do the same."""
    n = len(t.data)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            a, b = t.compare(j, j + 1)
            if a > b:
                t.swap(j, j + 1)
                swapped = True
        if not swapped:
            break


def insertion_sort(t):
    for i in range(1, len(t.data)):
        j = i
        while j > 0:
            a, b = t.compare(j - 1, j)
            if a <= b:
                break
            t.swap(j - 1, j)
            j -= 1


def selection_sort(t):
    n = len(t.data)
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            a, b = t.compare(m, j)
            if b < a:
                m = j
        if m != i:
            t.swap(i, m)


def merge_sort(t):
    def ms(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        ms(lo, mid)
        ms(mid, hi)
        left, right = t.data[lo:mid], t.data[mid:hi]
        i = j = 0
        k = lo
        while i < len(left) and j < len(right):
            a, b = t.compare(lo + i, mid + j)
            if left[i] <= right[j]:
                t.write(k, left[i]); i += 1
            else:
                t.write(k, right[j]); j += 1
            k += 1
        while i < len(left):
            t.write(k, left[i]); i += 1; k += 1
        while j < len(right):
            t.write(k, right[j]); j += 1; k += 1
    ms(0, len(t.data))


def binary_search(t, target):
    lo, hi = 0, len(t.data) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = t.compare_value(mid, target)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


ALGORITHMS = {
    "bubble": bubble_sort,
    "insertion": insertion_sort,
    "selection": selection_sort,
    "merge": merge_sort,
}


# =========================================================================
# Rendering -- this is YOUR design. The stub below is deliberately minimal.
# =========================================================================

def render_frame(frame, width=60):
    """Render one frame as a string. Replace this entirely.

    The stub prints the array; a real submission draws proportional bars and
    highlights the indices involved.
    """
    event, snapshot, indices = frame
    return f"{event:8} {snapshot} {indices}"


# =========================================================================
# Self-test -- run this often. Do not edit.
# =========================================================================

def inversions(a):
    """Reference: the number of out-of-order pairs. Used to check swap counts."""
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def run_tests():
    import random
    total = passed = 0

    def t(name, cond, detail=""):
        nonlocal total, passed
        total += 1
        print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   -- {detail}" if not cond and detail else ""))
        passed += bool(cond)

    random.seed(1234)
    shapes = {
        "random": lambda n: random.sample(range(n * 3), n),
        "sorted": lambda n: list(range(n)),
        "reversed": lambda n: list(range(n, 0, -1)),
        "duplicates": lambda n: [random.randint(0, 3) for _ in range(n)],
    }

    print("Correctness -- every algorithm sorts every shape")
    for name, fn in ALGORITHMS.items():
        try:
            bad = []
            for sname, gen in shapes.items():
                for n in (0, 1, 2, 5, 17, 40):
                    src = gen(n)
                    tr = Tracer(src)
                    fn(tr)
                    if tr.data != sorted(src):
                        bad.append((sname, n))
            t(f"{name} sorts correctly", not bad, f"failed on {bad[:3]}")
        except NotImplementedError:
            t(f"{name} sorts correctly", False, "not implemented")

    print("\nInstrumentation -- counts must match theory")
    try:
        tr = Tracer(list(range(32, 0, -1)))
        selection_sort(tr)
        t("selection does exactly n(n-1)/2 comparisons", tr.comparisons == 32 * 31 // 2,
          f"got {tr.comparisons}, expected {32*31//2}")
        counts = set()
        for sname, gen in shapes.items():
            tr = Tracer(gen(24))
            selection_sort(tr)
            counts.add(tr.comparisons)
        t("selection comparison count is input-independent", len(counts) == 1,
          f"got {sorted(counts)}")
    except NotImplementedError:
        t("selection does exactly n(n-1)/2 comparisons", False, "not implemented")
        t("selection comparison count is input-independent", False, "not implemented")

    try:
        ok, detail = True, ""
        for n in (10, 25, 50):
            src = random.sample(range(n * 3), n)
            inv = inversions(src)
            tb = Tracer(src); bubble_sort(tb)
            ti = Tracer(src); insertion_sort(ti)
            if not (tb.swaps == inv == ti.swaps):
                ok = False
                detail = f"n={n}: inv={inv} bubble={tb.swaps} insertion={ti.swaps}"
        t("bubble and insertion swaps both equal the inversion count", ok, detail)
    except NotImplementedError:
        t("bubble and insertion swaps both equal the inversion count", False, "not implemented")

    print("\nBest case -- adaptive sorts must be O(n) on sorted input")
    try:
        tb = Tracer(list(range(64))); bubble_sort(tb)
        ti = Tracer(list(range(64))); insertion_sort(ti)
        t("bubble is O(n) on sorted input", tb.comparisons == 63, f"got {tb.comparisons}")
        t("insertion is O(n) on sorted input", ti.comparisons == 63, f"got {ti.comparisons}")
    except NotImplementedError:
        t("bubble is O(n) on sorted input", False, "not implemented")
        t("insertion is O(n) on sorted input", False, "not implemented")

    print("\nGrowth -- merge must beat the quadratic sorts at scale")
    try:
        src = random.sample(range(2000), 256)
        tm = Tracer(src); merge_sort(tm)
        tb = Tracer(src); bubble_sort(tb)
        t("merge uses far fewer comparisons than bubble at n=256",
          tm.comparisons * 5 < tb.comparisons,
          f"merge={tm.comparisons} bubble={tb.comparisons}")
    except NotImplementedError:
        t("merge uses far fewer comparisons than bubble at n=256", False, "not implemented")

    print("\nSearch")
    try:
        arr = list(range(0, 200, 2))
        tr = Tracer(arr)
        found = all(binary_search(Tracer(arr), v) == arr.index(v) for v in arr[::7])
        t("binary_search finds every present value", found)
        t("binary_search returns -1 when absent", binary_search(Tracer(arr), 199) == -1)
        tr = Tracer(arr); binary_search(tr, 198)
        t("binary_search is logarithmic", tr.comparisons <= 10, f"used {tr.comparisons} comparisons")
    except NotImplementedError:
        for n in ("binary_search finds every present value",
                  "binary_search returns -1 when absent",
                  "binary_search is logarithmic"):
            t(n, False, "not implemented")

    print("\nFrame contract")
    tr = Tracer([3, 1, 2]); bubble_sort(tr)
    t("frames are (event, snapshot, indices)",
      all(len(f) == 3 and isinstance(f[1], list) and isinstance(f[2], tuple) for f in tr.frames))
    t("snapshots are independent copies",
      len({id(f[1]) for f in tr.frames}) == len(tr.frames))

    print(f"\n{passed}/{total} tests passing")
    return passed, total


if __name__ == "__main__":
    run_tests()
