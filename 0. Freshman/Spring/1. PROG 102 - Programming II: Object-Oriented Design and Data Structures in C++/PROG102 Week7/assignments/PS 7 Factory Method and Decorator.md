# PROG 102 · Problem Set 7
## Factory Method and Decorator

**Week 7 · Released Friday Week 7 · Due Friday Week 8, 17:00 · 100 points**
**Covers:** Lectures 22–24

> **Project 1 is due Week 9.** This problem set is deliberately lighter than PS 6. **Use the time you
> save on Project 1**, not on this.

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `factory.cpp`, `decorator.cpp`, `singleton.cpp`, `patterns.md`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

**No raw `new`/`delete` anywhere.** Week 5 applies; every pattern here should use `unique_ptr`.

---

## Part A — Factory Method (24 pts)

**A1.** *(8)* A `Shape` hierarchy with at least three concrete types, and:

```cpp
std::unique_ptr<Shape> make_shape(const std::string& kind, double dim);
```

Unknown kinds throw `std::invalid_argument` naming the kind.

**In `ANSWERS.md`, say what the return type promises the caller** — all three things it says.

**A2.** *(6)* Add a **fourth** shape.

**Report exactly how many lines you changed and how many call sites you touched.** Then state, in one
sentence, what the factory bought.

**A3.** *(6)* The factory contains an `if`-chain on a string, which Lecture 15 §4.4 called a design
smell.

**Argue that it is acceptable here**, in three sentences. Your argument must distinguish this case from
the one L15 objected to.

**A4.** *(4)* Replace the `if`-chain with a **registry** — a `std::map` from name to a creating
function — so that adding a shape does not modify `make_shape` at all.

*(You may use `std::function`; it is Week 11 material and using it here is fine.)*

**Which version would you ship, and why?** One sentence. **Both answers can earn full marks.**

---

## Part B — Decorator (34 pts)

**B1.** *(10)* An interface with at least one concrete implementation and **three** decorators over it,
each adding an observable transformation.

Compose them at run time with `unique_ptr` and `std::move`. Print the composition **and** the result.

**B2.** *(6)* Compose and print **all eight** combinations of your three decorators.

Then **write out the class names the subclassing version would have needed**, and tabulate
$2^n$ against $n$ for n = 1, 3, 5, 8, 10.

**B3.** *(10)* Measure the cost. Build chains of depth 0, 1, 2, 4 and 8 over an interface whose base
operation is trivial, and time at least 10⁷ calls.

Report **per-call time at each depth and the marginal cost per layer.**

Then compare your marginal figure with Week 4's virtual-call measurement (~2 ns). **They will differ.
Explain why**, referring to L14 §6.

**B4.** *(8)* Answer both:

- **(a)** *(4)* Decorators wrap at run time. **Give one concrete thing this lets you do** that the
  subclassing version cannot, and show the code.
- **(b)** *(4)* Give **two** concrete disadvantages of a deep decorator chain. At least one must be
  about debugging rather than performance.

---

## Part C — Singleton, and Whether to Use It (22 pts)

**C1.** *(6)* Implement Meyers' Singleton with a constructor that prints. Call `instance()` five times
and show it constructs once.

Then **defeat it**: remove the deleted copy constructor and show how a second instance can be created.

**C2.** *(8)* Race at least 16 threads to `instance()`, with a constructor that sleeps 50 ms.

Report the construction count. Then find the guard in the generated assembly:

```
g++ -std=c++17 -O2 -S -masm=intel yourfile.cpp -o out.s
grep __cxa_guard out.s
```

**Report what you find and what it means.**

*(If ThreadSanitizer will not start, see Lab 0's toolchain note — `setarch $(uname -m) -R ./prog`.)*

**C3.** *(8)* Take a small program that uses a singleton `Config` and rewrite it to pass a `Config&`.

- **(a)** *(4)* **Which function signatures changed?** List them.
- **(b)** *(4)* In three sentences: what did the signatures reveal that the singleton hid, and what did
  you give up?

---

## Part D — Judgement (20 pts)

This part is marked as writing. `patterns.md`.

**D1.** *(8)* Find **three** patterns in the C++ standard library, not counting Iterator and
`std::stack`, which were named in lectures.

For each: name the pattern, name the class, and say **what varies** in one sentence.

**D2.** *(6)* Take any class from your PS 4, PS 6 or Project 1 code. **Identify one place where a
pattern from this week would genuinely help**, and one where applying a pattern would make it worse.

Both halves required. Be specific — name the pattern and the class.

**D3.** *(6)* A colleague proposes an `IShapeFactory` abstract interface for a program with exactly one
shape type, which has not changed in two years.

Write the **three-sentence objection**, then the **strongest three-sentence case in favour**.

**You are marked on the quality of the second one.** Arguing the position you disagree with is the
skill being assessed.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 24 | Factory Method, and when a type-switch is acceptable |
| B | 34 | Decorator, measured and argued |
| C | 22 | Singleton, its guarantee, and its cost |
| D | 20 | Judgement — including arguing against yourself |
| **Total** | **100** | |

---

## Submission Checklist

1. Clean build, sanitizer-clean, **no raw `new`/`delete`**.
2. B2 includes both the eight compositions and the $2^n$ table.
3. B3 reports the **marginal** cost per layer, not just totals.
4. C2 includes the `__cxa_guard` finding.
5. D3's case *in favour* is a real argument, not a straw man.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 7 · Problem Set 7 · © CSE Department*
