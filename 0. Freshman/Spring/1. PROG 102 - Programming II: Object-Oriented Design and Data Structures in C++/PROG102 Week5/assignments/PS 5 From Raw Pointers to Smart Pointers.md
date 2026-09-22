# PROG 102 · Problem Set 5
## From Raw Pointers to Smart Pointers

**Released:** Friday 26 February 2027, 10:00 · Week 5 (after Thursday's L18)
**Due:** Friday 5 March 2027, 17:00 · Week 6 — late penalty from 17:01
**Points:** 100 · counts toward the Problem Sets component (30%, lowest one dropped)
**Expected time:** about 4–5 hours

## What this problem set uses

Weeks 0–5: your PS 4 hierarchy, throwing and catching (L04 §4.2) and the counting harness (L06 §1),
RAII, `unique_ptr`, `make_unique` and passing smart pointers (L16), `shared_ptr`, `make_shared`,
`weak_ptr` and cycles (L17), move semantics, `noexcept` on moves and the Rule of Five/Zero (L18).

**Not needed and not expected:** exception guarantees by name (Week 9), threads (Week 10). Comparing
assembly and timing smart pointers are measured in Lectures 16–18; this set does not repeat them.

> **Midterm 1 is Tuesday 2 March, 18:00**, and covers Weeks 0–4 — nothing on this set is on it.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `shapes2.cpp`, `costs.cpp`, `cycle.cpp`, `moves.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

---

## Part A — Rewrite Week 4's Hierarchy (26 pts)

**A1.** *(8)* Take your PS 4 `Shape` hierarchy and rewrite it so that:

- the container is `std::vector<std::unique_ptr<Shape>>`;
- there is **no `new`** anywhere — use `make_unique`;
- there is **no `delete`** anywhere;
- `Shape` keeps its **virtual destructor**.

It must produce the same output as PS 4 A4 and be sanitizer-clean.

**A2.** *(6)* Remove the `virtual` from `Shape`'s destructor and rerun under
`-fsanitize=address`.

**Report what happens.** Then answer in two sentences: **does `unique_ptr` protect you from Week 4's
virtual destructor rule?**

**A3.** *(6)* Write these four functions over your hierarchy and say in one line what each **signature**
promises the caller:

```cpp
double total_area(const std::vector<std::unique_ptr<Shape>>& shapes);
void   describe(const Shape& s);
std::unique_ptr<Shape> make_circle(double r);
void   absorb(std::unique_ptr<Shape> s);
```

**A4.** *(6)* Now write `void bad(const std::unique_ptr<Shape>& s)` that only calls `s->area()`.

Try to call it with (a) a `Shape` on the stack and (b) a `shared_ptr<Shape>`. **Paste both errors.**
Then fix the signature and show both calls working.

**State the rule in one sentence.**

---

## Part B — What It Costs (16 pts)

**B1.** *(8)* Report `sizeof` for `int*`, `unique_ptr<int>`, `shared_ptr<int>` and `weak_ptr<int>`.
**Explain why two of them are 16.**

Then give `unique_ptr` a **stateful** deleter and report `sizeof` again.

**B2.** *(8)* Instrument `operator new` — the single-object form, written the same way as Lecture 06's
`operator new[]` harness — and count allocations for `shared_ptr<W>(new W)`,
`make_shared<W>()` and `make_unique<W>()`. Report all three and explain the difference.

---

## Part C — Exception Safety and the Benchmark Trap (24 pts)

**C1.** *(10)* Write two functions that allocate a `Widget`, call a method that **conditionally throws**,
and return a value — one using raw `new`/`delete`, one using `make_unique`.

Count with your B2 instrumentation, plus a matching `operator delete`. Trigger the throw and report allocations and
frees for **both**, at **`-O0` and `-O2`**.

**C2.** *(8)* Now change the method to throw **unconditionally** and rerun the raw version at `-O2`.

**Report what changes.** Explain it in two sentences.

*(This is Lecture 16 §5.4. It is the most instructive part of this problem set and it is worth reading
that section before you start.)*

**C3.** *(6)* In three sentences: **is `unique_ptr` zero-overhead?** Your answer must distinguish size,
generated code for borrowing, and generated code for owning.

---

## Part D — Cycles and Moves (34 pts)

**D1.** *(10)* Build two `shared_ptr` nodes pointing at each other. Report `use_count()` for both,
whether the destructors run, and the sanitizer's leak figure.

Then convert one link to `weak_ptr` and show both destructors running.

**Explain in one sentence why reference counting cannot solve this in general.**

**D2.** *(10)* Demonstrate `weak_ptr`'s lifecycle: `expired()` and `use_count()` before the object
exists, while it is alive, inside a `lock()`, and after it is destroyed.

**Why must you use `lock()` rather than `expired()` followed by access?**

**D3.** *(14)* Answer all three, with code and output:

- **(a)** *(5)* `std::string b = std::move(a);` — print `a` afterwards. What may you legally do with
  `a` now? Give one legal and one undefined operation.
- **(b)** *(5)* Write `Buf make()` as `return b;` and as `return std::move(b);` with counting
  constructors. **Report both counts** and say which is correct.
- **(c)** *(4)* Remove `noexcept` from your move constructor, then `push_back` into a `vector` without
  `reserve`. **Report whether moves or copies were used**, and put the `noexcept` back.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 26 | Ownership expressed in types and signatures |
| B | 16 | Size and allocation counts |
| C | 24 | Exception safety, and a benchmark that optimized itself away |
| D | 34 | Cycles, `weak_ptr`, and move semantics |
| **Total** | **100** | |

---

## Submission Checklist

1. Part A contains **no `new` and no `delete`** (except where A2 deliberately breaks the destructor).
2. Sanitizer-clean except where A2, C1 and D1 provoke reports.
3. Part C reports **both** optimization levels, and C2's unconditional-throw result.
4. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 5 · Problem Set 5 · © CSE Department*
