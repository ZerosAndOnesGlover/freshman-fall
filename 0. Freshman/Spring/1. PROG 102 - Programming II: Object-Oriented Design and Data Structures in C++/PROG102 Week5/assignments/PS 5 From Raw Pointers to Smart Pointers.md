# PROG 102 · Problem Set 5
## From Raw Pointers to Smart Pointers

**Week 5 · Released Friday Week 5 · Due Friday Week 6, 17:00 · 100 points**
**Covers:** Lectures 16–18

> **Midterm 1 was this week.** This set is released after it and due in Week 6. **Do not start it
> before the exam.**

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

## Part B — What It Costs (26 pts)

**B1.** *(6)* Report `sizeof` for `int*`, `unique_ptr<int>`, `shared_ptr<int>` and `weak_ptr<int>`.
**Explain why two of them are 16.**

Then give `unique_ptr` a **stateful** deleter and report `sizeof` again.

**B2.** *(8)* Compile and compare at `-O2 -S`:

- `int raw(Widget*)` against `int uniq(Widget&)` — **report whether they are identical**;
- both against `int bad(const std::unique_ptr<Widget>&)` — **report the extra instruction.**

**B3.** *(6)* Instrument `operator new` and count allocations for `shared_ptr<W>(new W)`,
`make_shared<W>()` and `make_unique<W>()`. Report all three and explain the difference.

**B4.** *(6)* Measure, over at least 10⁶ **distinct** objects: a raw pointer, a `shared_ptr` accessed
**by reference**, and a `shared_ptr` **copied** each iteration.

Report per-operation times. Then answer: **which part of the gap is the reference count, and which part
is not?**

---

## Part C — Exception Safety and the Benchmark Trap (18 pts)

**C1.** *(8)* Write two functions that allocate a `Widget`, call a method that **conditionally throws**,
and return a value — one using raw `new`/`delete`, one using `make_unique`.

Instrument `operator new`/`operator delete` to count. Trigger the throw and report allocations and
frees for **both**, at **`-O0` and `-O2`**.

**C2.** *(6)* Now change the method to throw **unconditionally** and rerun the raw version at `-O2`.

**Report what changes.** Explain it in two sentences.

*(This is Lecture 16 §5.4. It is the most instructive part of this problem set and it is worth reading
that section before you start.)*

**C3.** *(4)* In three sentences: **is `unique_ptr` zero-overhead?** Your answer must distinguish size,
generated code for borrowing, and generated code for owning.

---

## Part D — Cycles and Moves (30 pts)

**D1.** *(8)* Build two `shared_ptr` nodes pointing at each other. Report `use_count()` for both,
whether the destructors run, and the sanitizer's leak figure.

Then convert one link to `weak_ptr` and show both destructors running.

**Explain in one sentence why reference counting cannot solve this in general.**

**D2.** *(6)* Demonstrate `weak_ptr`'s lifecycle: `expired()` and `use_count()` before the object
exists, while it is alive, inside a `lock()`, and after it is destroyed.

**Why must you use `lock()` rather than `expired()` followed by access?**

**D3.** *(8)* Add a move constructor and move assignment to a buffer class. Measure copying against
moving **2,000 pre-built 1 MB buffers**.

Report **per-operation** times, not just the ratio. Then repeat with a **16-byte** buffer and explain
the change.

**D4.** *(8)* Answer all three, with code and output:

- **(a)** *(3)* `std::string b = std::move(a);` — print `a` afterwards. What may you legally do with
  `a` now? Give one legal and one undefined operation.
- **(b)** *(3)* Write `Buf make()` as `return b;` and as `return std::move(b);` with counting
  constructors. **Report both counts** and say which is correct.
- **(c)** *(2)* Remove `noexcept` from your move constructor, then `push_back` into a `vector` without
  `reserve`. **Report whether moves or copies were used**, and put the `noexcept` back.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 26 | Ownership expressed in types and signatures |
| B | 26 | The costs, measured and separated |
| C | 18 | Exception safety, and a benchmark that optimized itself away |
| D | 30 | Cycles, `weak_ptr`, and move semantics |
| **Total** | **100** | |

---

## Submission Checklist

1. Part A contains **no `new` and no `delete`** (except where A2 deliberately breaks the destructor).
2. Sanitizer-clean except where A2, C1 and D1 provoke reports.
3. Part C reports **both** optimization levels, and C2's unconditional-throw result.
4. Part D3 reports **absolute per-operation times**, not only ratios.
5. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 5 · Problem Set 5 · © CSE Department*
