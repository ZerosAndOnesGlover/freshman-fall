# PROG 102 · Problem Set 0 — Solutions and Marking Notes
## Classes, Constructors, and `const`

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**This is the first C++ these students have written.** Two calibration notes:

1. **Do not deduct twice for the same misunderstanding.** A student who has not internalised
   `const`-correctness will lose marks in B2, D1 and D2. Mark B2 fully, then mark D1/D2 on whether they
   *fixed* it once told, not on whether it was right the first time.
2. **Parts A and E are the ones that matter.** They are 36 of the 100 points and neither asks for
   design. A student who does A and E well and B poorly has understood this week; the reverse has not.

**Reference environment:** g++ 13.3.0, x86-64 Linux, `-std=c++17`. `sizeof` and assembly results are
exact and should match. The C2 garbage values will not match and must not be required to.

---

## Part A — Reading the Machine (20)

### A1 (4)

Both bodies:

```asm
_ZN7Counter3addEi:            _Z8add_freeP7Counteri:
        endbr64                       endbr64
        add     DWORD PTR [rdi], esi  add     DWORD PTR [rdi], esi
        ret                           ret
```

**Identical.** `this` arrives in **`rdi`** — the first argument register in the x86-64 System V ABI.

*Marking: 2 for both listings, 1 for stating they are identical, 1 for naming `rdi`. A student on ARM
or Apple silicon will see `x0` and different mnemonics — **accept it fully**, the claim is that the two
are identical, not that they are any particular instruction.*

### A2 (4)

| Type | `sizeof` |
| --- | --- |
| `struct { int x; double y; }` | 16 |
| the same + 5 member functions | 16 |
| empty struct | 1 |
| empty struct + 2 member functions | 1 |

The empty struct is 1 because **two distinct objects must have distinct addresses**; a size of 0 would
make `&a[0] == &a[1]` in an array.

*Marking: 2 for the four numbers, 2 for the explanation. "Because the standard says so" is 0 for the
explanation — the question asks why the standard says so. Accept any answer mentioning distinct
addresses or array indexing.*

### A3 (4)

- `_ZN6Matrix9transposeEv` → `Matrix::transpose()`
- `_ZNK6Matrix3getEii` → `Matrix::get(int, int) const`

The **`K`** encodes `const`. It is a different symbol because a `const` member function takes
`const Matrix*` as `this` rather than `Matrix*` — **a different parameter type is a different
function**, which is exactly what lets you overload on `const`.

*Marking: 1 each for the demanglings, 2 for the `K` explanation. The link to `this` is what is being
assessed; "K means const" alone is 1 of the 2.*

### A4 (4)

An in-class definition is **implicitly `inline`**, and an inline function with no callers is never
emitted — there is nothing to generate a symbol for.

To make it reappear without moving the definition, any of:

- call it from somewhere in the same file;
- compile with `-fkeep-inline-functions`;
- take its address (`auto p = &Counter::add;`).

*Marking: 2 for the explanation using both words, 2 for any working method. Accept `-O0` if the student
demonstrates it works on their setup — GCC still usually elides it, so check they actually ran it
rather than assuming.*

### A5 (4)

```
plain_c_function              <- extern "C"
_Z3fooi                       <- ordinary C++
```

You give up **overloading**. Mangling is what gives overloads distinct symbols; without it, two
functions of the same name produce one symbol and the linker cannot distinguish them.

*Marking: 2 for the `nm` output, 2 for the explanation. The explanation must connect to symbols — "you
can't overload" alone is 1.*

---

## Part B — A Class That Owns Memory (28)

### B1 (8)

```cpp
class CharBuffer {
    int   size;
    char* data;
public:
    explicit CharBuffer(int n) : size(n), data(new char[n]) {
        std::memset(data, 0, static_cast<std::size_t>(n));
    }
    ~CharBuffer() { delete[] data; }
    // ...
};
```

*Marking: 3 constructor allocating and zeroing, 2 destructor with `delete[]`, 2 initializer list in
declaration order, 1 `new[]` rather than `malloc`.*

**Deduct 2 for `delete` instead of `delete[]`.** It is undefined behaviour, ASan catches it, and it is
the single most common error in this part. **Deduct 2 for a list written out of declaration order**
even though it happens to work here — the habit is the point, and `-Wreorder` will have told them.

### B2 (6)

```cpp
int  capacity()      const;   // const -- reads only
char at(int i)       const;   // const -- reads only
void set(int i, char c);      // NOT const -- writes
const char* c_str()  const;   // const -- reads only
```

Three are `const`; only `set` is not.

**The question says "two of the four are not, or should not be" — this is deliberate.** There is only
one that genuinely must not be `const`. A student who says so, and says the question's premise is
wrong, gets **full marks**. A student who forces a second one to be non-`const` to fit the question has
been led by the wording and should get 4.

*Marking: 4 for correct `const` marking, 2 for the justifications. The `c_str()` case is the
interesting one — it returns `const char*`, so it can be `const`; had it returned `char*` it should
not be. Award the full 2 to anyone who notices that.*

### B3 (6)

```cpp
CharBuffer b = 8;      // compiles without explicit; fails with it
```

```
error: conversion from 'int' to non-scalar type 'CharBuffer' requested
```

**The specific bug:** any function taking a `CharBuffer` by value can be called with a bare `int`,
silently allocating a buffer. `process(42)` would compile and allocate 42 bytes.

*Marking: 2 for the line, 1 for the error text, 3 for the explanation. As stated on the sheet: a
generic "prevents implicit conversion" is 3 of the 6; naming what goes wrong **in this class** earns
all 6.*

### B4 (8)

Reference:

```
capacity=8 contents="hi"
const object: capacity=4 at(0)=0
```

Clean under `-fsanitize=address,undefined`, exit 0.

*Marking: 4 program correct, 2 sanitizer-clean transcript, 2 exercising the `const` object.*

**The `const CharBuffer` line is the assessed part**, because it is where a missing `const` on an
accessor surfaces. A student whose `const` object cannot call `capacity()` has found their own B2 bug —
if they fixed it and said so, full marks.

---

## Part C — Initialization (20)

### C1 (6)

Adding `const int id;` breaks the assign-in-body version:

```
error: uninitialized const member in 'const int'
note:  'const int S::id' should be initialized
error: assignment of read-only member 'S::id'
```

By the time the body runs, **every member has already been initialized**. The body assigns; it cannot
initialize. A `const` member cannot be assigned, so there is no way to give it a value from the body.

*Marking: 3 both versions, 1 error text, 2 explanation. "Because const can't change" is 1 of the 2 —
the point is about *when* initialization happens, not what `const` means.*

### C2 (8)

Instrumented `operator new[]` on the reference machine, asking for 4 integers:

| Build | Integers allocated |
| --- | --- |
| `-O0` | 99,539,950 |
| `-O2` | 1,600,677,166 |

> **Do not mark against these numbers.** They are uninitialized stack bytes. **Any large wrong number
> is correct**, and a student who reports 4 has almost certainly not reproduced the bug — check their
> declaration order, which is the usual cause.

**(a) (2)** Both fire:

```
warning: 'Wrong::size' will be initialized after [-Wreorder]
warning: '*this.Wrong::size' is used uninitialized [-Wuninitialized]
```

**(b) (3)** After swapping the declarations, `-Wreorder` still fires but the bug is gone. So
**`-Wreorder` means "your list order is misleading", not "your code is wrong"** — it compares list
order against declaration order and says nothing about whether a member is read before it is set.
`-Wuninitialized` is the one that fires only on the genuine fault.

*Marking: 3 for the allocation report, 2 for (a), 3 for (b). **(b) is the assessed idea of Part C.** A
student who says "both warnings mean the same thing" gets 0 for (b) even if the rest is perfect.*

### C3 (6)

```cpp
struct S {
    const int c;
    int&      r;
    S(int v, int& target) : c(v), r(target) {}
};
int x = 7; S s(3, x); s.r = 99;    // x is now 99
```

A reference member cannot be assigned in the body because **a reference must be bound when it is
created and can never be rebound** — assignment to `r` writes *through* it to the referent, so there is
no syntax that would bind it later.

*Marking: 3 for the class and demonstration, 3 for the explanation. The key phrase is that assignment
writes through the reference rather than rebinding it. Accept any wording carrying that.*

---

## Part D — `const`-Correctness (16)

### D1 (6)

```cpp
void print_buffer(const CharBuffer& b) {
    std::printf("capacity=%d contents=\"%s\"\n", b.capacity(), b.c_str());
}
```

Compiles only if `capacity()` and `c_str()` are `const`.

*Marking: 3 function, 3 for having fixed the class rather than the parameter. **A student who removed
the `const` from the parameter scores 0 for the second half** even though it compiles — the sheet
explicitly forbids it, and it is the reflex the question exists to break.*

### D2 (6)

```
error: passing 'const CharBuffer' as 'this' argument discards qualifiers [-fpermissive]
note:   in call to 'int CharBuffer::capacity()'
```

The required phrase is **"as `this` argument"**. It confirms Lecture 01: the compiler is describing an
attempt to pass a `const CharBuffer*` into a parameter declared `CharBuffer*`. The hidden first
parameter is not a teaching metaphor; it is in the diagnostic.

*Marking: 2 error text, 4 explanation. Full marks require connecting "discards qualifiers" to the
pointer type of `this`. "It's const so it fails" is 1.*

### D3 (4)

```cpp
mutable int reads = 0;
char at(int i) const { ++reads; return data[i]; }
```

`mutable` relies on the distinction between **bitwise `const`** (no byte changes) and **logical
`const`** (the observable value does not change). A read counter is not part of the buffer's value.

An abuse: making `size` or `data` mutable — those *are* the object's value, and marking them mutable
turns `const` into a comment.

*Marking: 2 working demonstration, 1 the bitwise/logical distinction, 1 a defensible abuse example.
Accept any member that is part of the object's observable state.*

---

## Part E — The Cliff (16)

### E1 (8)

```
a.data = 0x502000000010
b.data = 0x502000000010   <-- same pointer
same? YES
==xxxxx==ERROR: AddressSanitizer: attempting double-free on 0x502000000010
SUMMARY: AddressSanitizer: double-free ... in operator delete[](void*)
```

The addresses vary per run; **their equality does not.**

*Marking: 4 for the two addresses and their equality, 4 for the sanitizer transcript. A student who
reports different addresses has written a copy constructor — ask them to remove it; they have solved
Week 1 early and should be told so, but this part needs the broken version.*

### E2 (8)

**(a) (3)** The **compiler generated** it, because the class declares no copy constructor. It performs a
**memberwise copy**: `size` is copied, and `data` — being a pointer — is copied *as a pointer*. Both
objects now refer to one allocation. This is a **shallow copy**.

**(b) (3)** `attempting double-free`. It happens at exit because that is when the second destructor
runs. **The copy itself is harmless**; it creates no error, corrupts nothing, and would pass any test
that did not destroy both objects. The fault is created at the copy and detonates at the second
`delete[]`.

**(c) (2)** A destructor, a copy constructor and a copy assignment operator **come as a set**: if a
class needs one, it almost certainly needs all three.

*Marking: (a) 3 — must say memberwise **and** that the pointer rather than the buffer was copied; 2 if
only one. (b) 3 — the separation of cause from symptom is the point; 1 for naming the error alone.
(c) 2 for any correct statement of the set; **students are not expected to know the name "Rule of
Three"** and should not be rewarded or penalised for it.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 20 |
| B | 28 |
| C | 20 |
| D | 16 |
| E | 16 |
| **Total** | **100** |

---

## What to Watch For

**The five recurring errors, in order of frequency:**

1. **`delete` instead of `delete[]`** (B1). ASan catches it. Flag it hard now — it recurs all semester.
2. **Removing `const` from the parameter** instead of fixing the class (D1). This is the reflex the
   course must break in Week 0, because retrofitting `const` in Week 6 is genuinely painful.
3. **Initializer list out of declaration order** (B1). Harmless here, catastrophic in C2's shape.
4. **Reporting 4 integers in C2.** Means the bug was not reproduced.
5. **Fixing Part E.** The sheet says not to. Do not award marks for a Rule of Three implementation
   here — note it approvingly and mark E as written.

---

## Feeding Into Week 1

**Week 1 Lecture 04 opens on E1's transcript.** Ask in the Monday lecture how many students saw the
double-free on their own code; the show of hands is worth more than the slide.

Students who fixed Part E have arrived at the Rule of Three independently. **Use them** — have one
present their fix in Week 1, then show them the copy-swap idiom, which is almost certainly not what
they wrote.

---

*PROG 102 · Week 0 · PS 0 Solutions · © CSE Department*
