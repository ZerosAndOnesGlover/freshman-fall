# PROG 102 · Problem Set 1
## A `Vector3D` Class, and a Class That Owns Memory

**Released:** Friday 29 January 2027, 10:00 · Week 1 (after Thursday's L06)
**Due:** Friday 5 February 2027, 17:00 · Week 2 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 4–5 hours

## What this problem set uses

Weeks 0–1: classes and `const` from Week 0; operator overloading, member versus free, `operator<<`,
`operator[]` pairs and strict weak ordering (L04), throwing an exception (L04 §4.2), the Rule of Three
and self-assignment (L05), copy-swap, the forced-failure harness and copy counting (L06).

**Not needed and not expected:** templates (Week 2), `std::vector`/`std::string` (Week 3), move
semantics (Week 5), exception guarantees by name beyond what L06 §2.3 says (Week 9).

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**No warnings.** Part D additionally requires an `-O2` build for the copy counts.

**Deliverables:** `vector3d.hpp`, `vector3d_test.cpp`, `buffer.hpp`, `buffer_test.cpp`, `counting.cpp`,
and `ANSWERS.md`. Name collaborators and state any generative-tool use at the top of `ANSWERS.md`.

**You may not use `std::vector`, `std::array` or `std::string` anywhere in this problem set.** Week 3
gives them to you; this week you are building the thing they replace.

---

## Part A — `Vector3D` (36 pts)

A three-component vector of `double`. Store the components however you like; `double e[3]` is
suggested.

**A1.** *(6)* Constructors: a default constructor giving the zero vector, and one taking three
`double`s. Plus:

```cpp
double  operator[](int i) const;   // read
double& operator[](int i);         // write
```

Both must `throw std::out_of_range` for an index outside 0–2 (Lecture 04 §4.2).

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

**A6.** *(4)* Free functions `dot` and `cross`.

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

## Part B — A Class That Owns Memory (32 pts)

`Vector3D` needs none of the Rule of Three. **Say why in one line in `ANSWERS.md`** *(2 of the 32)*.

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

## Part C — Copy-Swap (22 pts)

**C1.** *(7)* Add a `swap` member marked `noexcept`, and replace your `operator=` with the copy-swap
form taking its parameter **by value**.

Confirm `b = b` works with **no `this == &other` comparison anywhere in the class.**

**C2.** *(8)* Add Lecture 06 §1's forced-failure harness (copy it as given). Then, for **both** your
four-step operator and your copy-swap operator:

- construct `a` holding known contents and `b` holding different contents;
- arm the failure;
- attempt `a = b` and catch the exception;
- **read `a` afterwards.**

Paste both transcripts. One of them will report a sanitizer error.

**C3.** *(7)* Answer both:

- **(a)** *(4)* Name the exception guarantee copy-swap provides, and say **which property of the
  ordering** produces it.
- **(b)** *(3)* `swap` is `noexcept`. If it could throw, would the guarantee in (a) still hold?
  Explain in two sentences.

---

## Part D — Counting Copies (10 pts)

**D1.** *(10)* Before running anything, **write down your prediction** for the copy count of:

```cpp
Vector3D f() { Vector3D local(1,2,3); return local; }
Vector3D d = f();
Vector3D e = Vector3D(1,2,3);
```

Then measure it with Lecture 06 §5's counting harness at `-std=c++17 -O2`. **Report your prediction and the measurement, even where they disagree** — the disagreement
is worth more marks than a correct guess.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 36 | Operator overloading: member vs free, symmetry, `const` pairs |
| B | 32 | The Rule of Three, and the self-assignment failure traced |
| C | 22 | Copy-swap, and exception safety demonstrated rather than asserted |
| D | 10 | Predicting and counting copies |
| **Total** | **100** | |

**Where the marks actually are:** B4, C2 and D1 are 26 points for *running experiments and reporting
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
