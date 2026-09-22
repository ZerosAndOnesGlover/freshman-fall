# PROG 102 · Problem Set 4 — Solutions and Marking Notes
## A Shape Hierarchy

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux. `sizeof` values, error text and A4's numbers are
exact. Timings and addresses are not.

**This set is due in midterm week.** Expect more late submissions than usual and mark the concepts
generously where the code is nearly right — but **not** on C1 and D1, which are the two parts the exam
draws on directly.

---

> **Revised 2026-09-22.** Removed B2–B3 (GDB vtable dumps — Lab 4 Part B does both) and D1 (the three-attempt dispatch benchmark,
> which is Lecture 14 §5's own measurement). A3 no longer uses `unique_ptr` (Week 5): shapes are
> `Shape*` and are deleted by hand. D2–D3 are D1–D2. Items re-weighted to keep 100.

## Part A — The Hierarchy (36)

### A1 (12)

```cpp
class Shape {
    std::string label_;
public:
    explicit Shape(std::string l) : label_(std::move(l)) {}
    virtual ~Shape() = default;                       // the rule
    virtual double area() const = 0;
    virtual double perimeter() const = 0;
    virtual void draw(std::ostream&) const = 0;
    virtual const char* kind() const = 0;
    const std::string& label() const { return label_; }
};
```

*Marking: 3 abstract base with four pure virtuals, 2 **virtual destructor**, 3 three derived classes
with `override` throughout, 2 validation throwing `std::invalid_argument`.*

**Deduct 2 for a missing `virtual` on the destructor** even though nothing in Part A would detect it —
C1 assesses the consequence, and this is the mark for having got it right unprompted.

**Deduct 1 per missing `override`.** L13 §6 is explicit about it.

### A2 (6)

```cpp
std::ostream& operator<<(std::ostream& os, const Shape& s){ s.draw(os); return os; }
```

**The assessed question:** `draw` is virtual because *what to print differs per shape* and must be
chosen from the object at run time. `operator<<` is not virtual because *how to dispatch* does not
differ — and it cannot be, since a free function cannot be virtual and a member would put `Shape` on
the wrong side of the operator (L04 §3).

*Marking: 3 the operator, 3 the explanation. **Full marks require both halves**: virtual for the
per-type behaviour, non-member because of the left operand. 1 if only one half.*

### A3 (10), A4 (8)

Reference output:

```
Circle(c1, r=1.0000)          area=3.1416   perim=6.2832
Rectangle(r1, 3.0000x4.0000)  area=12.0000  perim=14.0000
Triangle(t1, 3.0000,4.0000,5.0000) area=6.0000 perim=12.0000
total area = 21.1416
largest    = Rectangle r1
rejected   : triangle inequality violated
```

*Marking A3: 4 the container, printing and deleting every shape, 3 STL algorithms for total and max (a raw loop loses these),
3 the rejected construction.*
*Marking A4: 8 for the numbers matching and a sanitizer-clean transcript.*

**The 3-4-5 triangle's area is exactly 6** by Heron. A student reporting 6.0000 has their formula
right; anything else is worth investigating with them.

---

## Part B — The vtable's Size (8)

### B1 (8)

| | `sizeof` |
| --- | --- |
| no virtuals, one `int` | 4 |
| one virtual | 16 |
| ten virtuals | 16 |
| `void*` | 8 |

**The first virtual function costs 8 bytes (the vptr) plus padding. The tenth costs nothing**, because
the vtable is per class and the object holds one pointer to it.

*Marking: 4 the numbers, 2 the explanation. Must say **one vptr regardless of count**.*

## Part C — The Three Traps (32)

### C1 (12)

Without a virtual destructor:

```
  ~BaseNV
ERROR: AddressSanitizer: new-delete-type-mismatch
```

**`~DerNV` never ran**; the allocation leaks. With it: `~DerV` then `~BaseV`.

**(4 of the 10) — the assessed half.** The warning fires **only when the base is already polymorphic**:

| Base | `-Wall -Wextra` |
| --- | --- |
| has a virtual function, non-virtual dtor | **warns** (`-Wdelete-non-virtual-dtor`, part of `-Wall`) |
| no virtual functions at all | **silent** |

The difference: GCC only considers a class polymorphic if it already has a virtual function, and it is
precisely the "I forgot `virtual` entirely" case that gets no warning.

*Marking: 6 the demonstrations, 4 the investigation. **A student who reports only "it warns" or only
"it doesn't" gets 2 of the 4** — the question asks for both cases and the sheet says so.*

### C2 (10)

```
by value    : Shape area=0.00
by reference: Sq    area=9.00
vector<Shape> : Shape(0.00) Shape(0.00)
```

With an abstract base: the by-value parameter and `std::vector<Base>` **fail to compile**; assignment
to a base-typed variable also fails. All three are caught.

*Marking: 5 the three demonstrations, 3 the abstract-base follow-up. **Full marks require noticing that
making the base abstract catches all three**, which is the practical takeaway.*

### C3 (10)

`static_cast<D1*>` on a `D2` printed **222** — the value of `D2::b`, read through `D1::a`'s offset. No
diagnostic. `dynamic_cast` returned `nullptr`.

The chain-versus-virtual count: adding a fourth shape requires editing **every** `dynamic_cast` chain
in the program and **zero** lines of the virtual version (beyond the new class itself).

*Marking: 3 the static_cast garbage **with an explanation of where the number came from**, 2 the
dynamic_cast, 3 the line count. A student who says "222 is garbage" without identifying it as `D2::b`
gets 1 of the 3.*

---

## Part D — What Dispatch Costs (24)

### D1 (12)

```asm
mov  rax, QWORD PTR [rdi]        ; vptr
lea  rdx, _ZNK2Sq4areaEv[rip]    ; expected target
mov  rax, QWORD PTR [rax]        ; slot 0
cmp  rax, rdx
jne  .L8                         ; fall back
movsd xmm0, QWORD PTR 8[rdi]     ; inlined body
```

**Speculative devirtualization.** With a second derived class visible, GCC generally abandons the guess
and emits a plain indirect call.

*Marking: 6 finding the guard, 6 the second-class experiment. **Accept either outcome for the second
experiment if reported honestly** — it depends on version and inlining budget. A student who reports
"the guard survived" and pastes the assembly showing it has done the work.*

### D2 (12)

`dynamic_cast` ≈ **2.8×** a virtual call (19.0–22.2 ms against 53.3–61.4 ms over 10⁷).

**Is virtual dispatch expensive?** Expected substance:

> No. It costs about **2 nanoseconds** per call. That doubles the cost of a loop whose body is a single
> multiply, and is invisible in any loop that touches a string, allocates, or does I/O. The ratio is
> alarming and the absolute number is not, and the absolute number is the one that decides whether it
> matters.

*Marking: 6 the ratio, 6 the judgement. **The answer must use absolute numbers**, as the question
demands — an answer phrased entirely in ratios gets 2 of the 6, because "2×" is exactly the framing
that misleads here.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 36 |
| B | 8 |
| C | 32 |
| D | 24 |
| **Total** | **100** |

---

## What to Watch For

1. **Missing `virtual` on the destructor** in A1. Deduct even though A1 alone would not catch it.
2. **Only one case investigated in C1.** The question asks for two.
3. **"222 is garbage"** without identifying it as `D2::b` (C3).
4. **A ratio-only answer to D2.** The most important correction in the set, and it is exactly what
   Section D of the midterm will probe.

---

## Feeding Into Week 5 and the Midterm

**Midterm 1 is Tuesday 2 March (Week 6).** Two things to say beforehand:

- **Section D is 15 marks of "explain this table",** and PS 4 D2 is the rehearsal.
- The revision guide's ten-item list is not a hint, it is a list. Point at it.

**For Week 5:** PS 4 A3 now uses `std::vector<Shape*>` and makes students `delete` every shape by hand.
Open Lecture 16 by asking who remembered to, and what an early `return` or a thrown exception would
have done to that cleanup loop.

---

*PROG 102 · Week 4 · PS 4 Solutions · © CSE Department*
