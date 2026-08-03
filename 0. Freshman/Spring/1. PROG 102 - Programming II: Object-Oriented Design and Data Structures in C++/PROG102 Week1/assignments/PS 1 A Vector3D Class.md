# PROG 102 · Problem Set 1
## A `Vector3D` Class, and a Class That Owns Memory

**Week 1 · Released Friday Week 1 · Due Friday Week 2, 17:00 · 100 points**
**Covers:** Lectures 04–06

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**No warnings.** Part D additionally requires `-O2` builds for the copy counts, and Part D3 requires
several other flag combinations, all stated there.

**Deliverables:** `vector3d.hpp`, `vector3d_test.cpp`, `buffer.hpp`, `buffer_test.cpp`, `counting.cpp`,
and `ANSWERS.md`. Name collaborators and state any generative-tool use at the top of `ANSWERS.md`.

**You may not use `std::vector`, `std::array` or `std::string` anywhere in this problem set.** Week 3
gives them to you; this week you are building the thing they replace.

---

## Part A — `Vector3D` (34 pts)

A three-component vector of `double`. Store the components however you like; `double e[3]` is
suggested.

**A1.** *(6)* Constructors: a default constructor giving the zero vector, and one taking three
`double`s. Plus:

```cpp
double  operator[](int i) const;   // read
double& operator[](int i);         // write
```

Both must `throw std::out_of_range` for an index outside 0–2.

**A2.** *(8)* The compound assignments, as **member** functions returning `Vector3D&`:

```
operator+=   operator-=   operator*=(double)   operator/=(double)
```

`operator/=` must `throw std::domain_error` on division by zero. Confirm `(a += b) += c` compiles and
does what it says.

**A3.** *(8)* The binary operators, as **free** functions implemented in terms of A2:

```
operator+   operator-   operator*(Vector3D, double)   operator*(double, Vector3D)   operator/
```

plus unary `operator-`.

**Both orderings of `operator*` are required.** In `ANSWERS.md`, paste the error you get if you
implement `operator*` as a member and then write `2.0 * v`.

**A4.** *(6)* Comparisons: `operator==`, `operator!=`, `operator<`.

Define `!=` in terms of `==`. Order by magnitude. **In `ANSWERS.md`, state whether your `operator<` is
a strict weak ordering** and justify each of the four conditions from Lecture 04 §6.1 in one line each.

**A5.** *(4)* `operator<<` printing `(x, y, z)`.

**It must be a free function.** Chaining must work: `std::cout << "v = " << v << "\n";`

**A6.** *(2)* Free functions `dot` and `cross`.

**In one sentence, say why these are named functions rather than `operator*`.**

### Reference Output

With `a = (1,2,3)` and `b = (4,5,6)`:

```
a+b     = (5, 7, 9)
b-a     = (3, 3, 3)
a*2     = (2, 4, 6)
2*a     = (2, 4, 6)
-a      = (-1, -2, -3)
a/2     = (0.5, 1, 1.5)
dot     = 32
cross   = (-3, 6, -3)
|a|     = 3.74166
```

---

## Part B — A Class That Owns Memory (30 pts)

`Vector3D` needs none of the Rule of Three. **Say why in one line in `ANSWERS.md`** *(2 of the 30)*.

Now build one that does: `Buffer`, holding a heap-allocated `double[]`.

**B1.** *(6)* Constructor taking a size, allocating and zeroing; destructor releasing. `size()` and a
`const`/non-`const` `operator[]` pair.

**B2.** *(8)* A **deep-copying copy constructor**. Demonstrate independence: copy a buffer, modify the
copy, show the original is unchanged.

**B3.** *(8)* A copy assignment operator, written the **four-step** way from Lecture 05 §6, *including*
the self-assignment guard.

**B4.** *(8)* Now break it. Remove the guard, run `b = b`, and instrument the operator to print:

- whether `this == &other`;
- the old pointer and its contents;
- the new pointer, and `other.data` **after** the reallocation;
- the resulting bytes, and whether any NUL/zero remains.

Paste the trace and the sanitizer report.

**Then answer:** *(4 of the 8)* Lecture 05 §7.1 claims this is **not** a use-after-free. **Is that true
of your trace?** Identify which line would have to change for it to become one.

---

## Part C — Copy-Swap (20 pts)

**C1.** *(6)* Add a `swap` member marked `noexcept`, and replace your `operator=` with the copy-swap
form taking its parameter **by value**.

Confirm `b = b` works with **no `this == &other` comparison anywhere in the class.**

**C2.** *(8)* Replace `operator new[]` so it throws `std::bad_alloc` on demand. Then, for **both** your
four-step operator and your copy-swap operator:

- construct `a` holding known contents and `b` holding different contents;
- arm the failure;
- attempt `a = b` and catch the exception;
- **read `a` afterwards.**

Paste both transcripts. One of them will report a sanitizer error.

**C3.** *(6)* Answer both:

- **(a)** *(3)* Name the exception guarantee copy-swap provides, and say **which property of the
  ordering** produces it.
- **(b)** *(3)* `swap` is `noexcept`. If it could throw, would the guarantee in (a) still hold?
  Explain in two sentences.

---

## Part D — Counting Copies (16 pts)

**D1.** *(6)* Build the counting harness from Lecture 06 §5 and reproduce the six-row table on your
machine at `-std=c++17 -O2`.

**D2.** *(4)* Before running anything, **write down your prediction** for the copy count of:

```cpp
Vector3D f() { Vector3D local(1,2,3); return local; }
Vector3D d = f();
Vector3D e = Vector3D(1,2,3);
```

Then measure. **Report your prediction and the measurement, even where they disagree** — the disagreement
is worth more marks than a correct guess.

**D3.** *(6)* Measure `Vector3D c = a + b;` under all five configurations:

```
-std=c++11 -O0
-std=c++11 -O0 -fno-elide-constructors
-std=c++17 -O0
-std=c++17 -O0 -fno-elide-constructors
-std=c++17 -O2
```

**Explain in three sentences why the second and fourth rows differ**, given that the flag is the same.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 34 | Operator overloading: member vs free, symmetry, `const` pairs |
| B | 30 | The Rule of Three, and the self-assignment failure traced |
| C | 20 | Copy-swap, and exception safety demonstrated rather than asserted |
| D | 16 | Copy counting and guaranteed elision |
| **Total** | **100** | |

**Where the marks actually are:** B4, C2 and D3 are 26 points for *running experiments and reporting
what happened*. None require you to invent anything. They are the cheapest marks here and they are the
ones the midterm will draw on.

---

## Submission Checklist

1. All files compile with **no warnings** under the development line.
2. `-fsanitize=address,undefined` clean, **except** where B4 and C2 deliberately provoke a report.
3. Part C contains **no** `this == &other` comparison.
4. Part D includes your predictions, including wrong ones.
5. No `std::vector`, `std::array` or `std::string`.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 1 · Problem Set 1 · © CSE Department*
