# PROG 102 · Problem Set 1 — Solutions and Marking Notes
## A `Vector3D` Class, and a Class That Owns Memory

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux, `-std=c++17`. Copy counts and allocation counts
are exact and should match. Addresses and garbage byte patterns will not.

**Calibration:** Part A is 34 points of straightforward implementation and most students will do well.
The course-relevant marks are in **B4, C2 and D3** — 26 points for running experiments and reporting
what happened. A student strong in A and weak in those has written correct C++ without understanding
what it costs, which is precisely the gap this course exists to close.

---

> **Revised 2026-09-22.** Removed D1 (reproducing Lecture 06's six-row table) and D3 (the five-configuration elision sweep,
> already in Lecture 06 §6); D2 is now D1. C2 now uses the forced-failure harness printed in Lecture
> 06 §1 (added there; verified to reproduce both transcripts under ASan). Throwing in A1/A2 is taught
> in the new Lecture 04 §4.2. Items re-weighted to keep 100.

## Part A — `Vector3D` (36)

### A1 (6)

```cpp
class Vector3D {
    double e[3];
public:
    Vector3D() : e{0,0,0} {}
    Vector3D(double x, double y, double z) : e{x,y,z} {}
    double  operator[](int i) const {
        if (i<0||i>2) throw std::out_of_range("Vector3D index"); return e[i]; }
    double& operator[](int i) {
        if (i<0||i>2) throw std::out_of_range("Vector3D index"); return e[i]; }
};
```

*Marking: 2 constructors, 2 the `operator[]` pair, 2 both throwing.*

**The non-`const` version must return `double&`.** Returning `double` means `v[0] = 5;` does not
compile. Deduct 2 and point at Lecture 04 §4.

### A2 (8) — compound assignments

Each returns `Vector3D&` and returns `*this`. `(a += b) += c` must compile; with `a=(1,..)`,
`b=(2,..)`, `c=(3,..)` the first component is **6**.

*Marking: 2 per operator, half marks if it returns by value (chaining breaks) or `void`.*

`operator/=` throws `std::domain_error` on zero. **Accept a check on exact `== 0.0`** — floating-point
subtlety about near-zero divisors is not this week's material.

### A3 (8) — binary operators

```cpp
Vector3D operator+(Vector3D a, const Vector3D& b) { a += b; return a; }
Vector3D operator*(Vector3D v, double s) { v *= s; return v; }
Vector3D operator*(double s, Vector3D v) { v *= s; return v; }
```

The required error, from making `operator*` a member:

```
error: no match for 'operator*' (operand types are 'double' and 'Vector3D')
```

*Marking: 5 for the five operators plus unary minus, 3 for the pasted error. Full marks for taking the
left operand by `const&` and copying inside — it is equivalent, just longer. **Deduct 3 for any
operator returning `Vector3D&`** and check whether `-Wreturn-local-addr` fired; if the student ignored
it, that is worth a comment.*

### A4 (6) — comparisons

`!=` defined as `!(a==b)`. Ordering by `norm()`.

**The strict-weak-ordering justification is the assessed part.** A correct answer notes that ordering
by magnitude *is* a valid strict weak ordering, and that two distinct vectors of equal magnitude are
**equivalent but not equal** — so `a < b` and `b < a` are both false while `a == b` is also false.

*Marking: 3 implementation, 3 justification. **Full marks require noticing the equivalent-but-not-equal
case.** A student who says "yes it's a SWO" with no discussion gets 1 of the 3.*

### A5 (4)

Free function, takes and returns `std::ostream&`, no newline inside.

*Marking: 2 correct signature, 1 chaining demonstrated, 1 no embedded newline. **Deduct the last point
for `std::endl` inside the operator** — it flushes on every print.*

### A6 (4)

`dot` and `cross` are named because **there are two products competing for one symbol**, and neither is
"the" multiplication of vectors. `a * b` would not tell the reader which.

*Marking: 2 for that idea. "Because they're not operators" is 0.*

### Reference output

```
a+b = (5, 7, 9)     b-a = (3, 3, 3)     a*2 = (2, 4, 6)     2*a = (2, 4, 6)
-a  = (-1, -2, -3)  a/2 = (0.5, 1, 1.5) dot = 32            cross = (-3, 6, -3)
|a| = 3.74166
```

$|a| = \sqrt{14}$.

---

## Part B — A Class That Owns Memory (32)

### Why `Vector3D` needs none of the three (2)

Its only member is `double e[3]` — an array of built-ins with no heap allocation. **It owns no
resource**, so memberwise copy is already correct and there is nothing for a destructor to release.

*Marking: 2. Must say *owns nothing* or equivalent. "Because it's small" is 0.*

### B1 (6), B2 (8), B3 (8) — plus 2 for the Vector3D line

Standard deep-copy `Buffer`. The four-step assignment:

```cpp
Buffer& operator=(const Buffer& o) {
    if (this == &o) return *this;
    delete[] data; n = o.n; data = new double[n];
    std::memcpy(data, o.data, n * sizeof(double));
    return *this;
}
```

*Marking B2: 4 deep copy, 4 the independence demonstration. A student who shows only that it compiles
has not demonstrated independence — require the modified-copy/unchanged-original transcript.*

### B4 (8) — the traced self-assignment

Reference trace:

```
enter: this=0x...  &o=0x...  same object? YES
old d=0x502000000010 contents="hello"
n=6 (a member, not in the freed block -- survives)
new d=0x502000000030   o.d=0x502000000030  <- o.d IS the new pointer
after memcpy, bytes: be be be be be be
any NUL terminator? NO
```

**(4 of the 8) — the assessed question.** Lecture 05 §7.1's claim **is** true of this trace: the freed
block at the old address is never read. Step 3 (`data = new ...`) replaced the pointer before anything
looked at it, so the copy reads the *new* buffer.

**To make it a genuine use-after-free**, the reallocation would have to come *after* the read, or not
happen at all — for example an operator that does `delete[] data; data = o.data;` (shallow), which then
reads freed memory on the next access.

*Marking: 4 trace, 4 the analysis. **Full marks require identifying that `o.d` aliases the new pointer**
— that is the whole mechanism. A student who says "yes it's a use-after-free" has not read their own
trace and gets 1 of the 4.*

*Accept any fill pattern. `0xbe` is ASan's; a student without the sanitizer may see zeros, which makes
the bug **invisible** — worth a written comment on their script, because it is the more dangerous
outcome.*

---

## Part C — Copy-Swap (22)

### C1 (7)

```cpp
void swap(Buffer& o) noexcept { std::swap(n, o.n); std::swap(data, o.data); }
Buffer& operator=(Buffer o) { swap(o); return *this; }
```

*Marking: 3 `swap` correct and `noexcept`, 3 by-value `operator=` with no guard anywhere. **Search the
submission for `== &`** — a leftover guard means they did not understand why it is unnecessary; deduct
3 and explain.*

### C2 (8)

```
FourStep before: a="hello"
  bad_alloc caught
ERROR: AddressSanitizer: heap-use-after-free

CopySwap before: a="hello"
  bad_alloc caught
CopySwap after : a="hello"
```

*Marking: 4 each. The four-step transcript **must** show the object damaged — a student reporting both
clean has not actually armed the failure, usually because they replaced `operator new` rather than
`operator new[]`.*

### C3 (7)

**(a) (3)** The **strong** exception guarantee. It comes from **ordering**: everything that can throw
(the copy, in the parameter) happens *before* anything is modified (the swap). If the copy fails, the
body never runs.

**(b) (3)** No. If `swap` could throw, it could fail partway — some members exchanged, some not —
leaving the object in a state that is neither the old one nor the new one. The strong guarantee
requires the commit step to be unconditional, and only `noexcept` makes it so.

*Marking: (a) 3, must name the guarantee **and** attribute it to ordering; 1 for the name alone.
(b) 3 for the partial-swap argument.*

---

## Part D — Counting Copies (10)

### D1 (10)

| | copies |
| --- | --- |
| `Vector3D d = f();` — named local | **0** |
| `Vector3D e = Vector3D(1,2,3);` — prvalue | **0** |

Both zero at `-O0` and `-O2`. **They differ only under `-fno-elide-constructors`**, where the named
local costs 1 copy and the prvalue still costs 0.

*Marking: 5 measurement, 5 for having recorded a prediction. **Award the prediction marks even when the
prediction was wrong** — the sheet promises this explicitly, and honest wrong predictions are the point.
A student who "predicted" the exact right answer for all rows should be spot-checked for having
measured first.*


## Marking Summary

| Part | Points |
| --- | --- |
| A | 36 |
| B | 32 |
| C | 22 |
| D | 10 |
| **Total** | **100** |

---

## What to Watch For

1. **A leftover self-assignment guard in Part C.** Grep for `== &`.
2. **Replacing `operator new` instead of `operator new[]`** in C2 — the failure never arms and both
   transcripts come back clean.
3. **"GCC got smarter"** in D3. The single most common wrong answer and the one worth correcting in
   the Monday lecture.
4. **Returning `Vector3D&` from `operator+`.** Check whether they ignored `-Wreturn-local-addr`.
5. **Claiming the B4 trace is a use-after-free** because the textbook says so, when their own transcript
   shows otherwise. Reward the students who trusted their data.

---

## Feeding Into Week 2

Week 2 turns `Buffer` into `Buffer<T>`. **Students whose Rule of Three is shaky will not survive the
templating of it** — a broken copy constructor inside a template produces error messages several
hundred lines long.

Before Week 2's lab, spot-check that each student's Part C compiles and is sanitizer-clean. It is worth
ten minutes.

---

*PROG 102 · Week 1 · PS 1 Solutions · © CSE Department*
