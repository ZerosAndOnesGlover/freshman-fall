# PROG 102 · Lab 9
## Testing for Failure

**Week 9 · 2-hour lab session · 40 points**
**Deliverable:** `tests.cpp`, `RESULTS.md`. In-lab checkoff.

> **Project 1 is due today.** This lab is short and directly useful to it — Part D asks you to
> determine your own container's guarantee, which is Project 1 Part 3.3.

---

## Purpose

Every test you have written so far checks that code works when nothing goes wrong.

**This lab is about the other half.** You will build a test suite that checks what happens when things
*fail* — when a copy throws, when an allocation fails, when a precondition is violated — and use it to
determine, empirically, which exception guarantee your own code provides.

**That is the deliverable of Week 9.** A guarantee you have not tested is a guess.

---

## The Framework

The curriculum names **Catch2**, and it is the right thing to learn. **If you have it installed, use
it** — everything below is spelled the same way and your tests should compile against either unchanged.

If you do not, use the header below. It is deliberately Catch2-compatible in its spellings:
`TEST_CASE`, `SECTION`, `REQUIRE`, `CHECK`, `REQUIRE_THROWS_AS`, `REQUIRE_NOTHROW`.

Save as `microtest.hpp`:

```cpp
// microtest.hpp -- a minimal, dependency-free test framework.
#pragma once
#include <cstdio>
#include <string>
#include <vector>
#include <functional>
#include <exception>

namespace mt {
struct Case { std::string name, tags; std::function<void()> fn; };
inline std::vector<Case>& registry(){ static std::vector<Case> r; return r; }
inline int& checks(){ static int c=0; return c; }
inline int& failures(){ static int f=0; return f; }
inline std::string& section(){ static std::string s; return s; }

struct Registrar { Registrar(std::string n, std::string t, std::function<void()> f){
    registry().push_back({std::move(n), std::move(t), std::move(f)}); } };

struct Fail : std::exception { const char* what() const noexcept override { return "REQUIRE failed"; } };

inline void report(bool ok, const char* expr, const char* file, int line, bool fatal){
    ++checks();
    if (ok) return;
    ++failures();
    std::printf("  FAILED: %s\n    at %s:%d\n", expr, file, line);
    if (!section().empty()) std::printf("    in section: %s\n", section().c_str());
    if (fatal) throw Fail{};
}
inline int run(){
    int passed=0;
    for (auto& c : registry()){
        checks()=0; int before=failures(); section().clear();
        std::printf("%s\n", c.name.c_str());
        try { c.fn(); }
        catch (const Fail&) { }
        catch (const std::exception& e){ ++failures(); std::printf("  FAILED: unexpected exception: %s\n", e.what()); }
        catch (...) { ++failures(); std::printf("  FAILED: unexpected unknown exception\n"); }
        bool ok = (failures()==before);
        std::printf("  %s (%d assertions)\n", ok?"passed":"FAILED", checks());
        if (ok) ++passed;
    }
    std::printf("\n%d/%zu test cases passed, %d assertion failures\n",
                passed, registry().size(), failures());
    return failures()==0 ? 0 : 1;
}
} // namespace mt

#define MT_CAT2(a,b) a##b
#define MT_CAT(a,b) MT_CAT2(a,b)
// Catch2 spells this TEST_CASE("name", "[tags]"); tags are optional there and absent here.
#define TEST_CASE(name) \
    static void MT_CAT(mt_test_,__LINE__)(); \
    static mt::Registrar MT_CAT(mt_reg_,__LINE__){name, "", MT_CAT(mt_test_,__LINE__)}; \
    static void MT_CAT(mt_test_,__LINE__)()
#define SECTION(name) mt::section() = (name);
#define REQUIRE(expr) mt::report((expr), #expr, __FILE__, __LINE__, true)
#define CHECK(expr)   mt::report((expr), #expr, __FILE__, __LINE__, false)
#define REQUIRE_THROWS_AS(expr, ex) \
    do { bool thrown=false; try { (void)(expr); } catch(const ex&){ thrown=true; } catch(...){} \
         mt::report(thrown, #expr " throws " #ex, __FILE__, __LINE__, true); } while(0)
#define REQUIRE_NOTHROW(expr) \
    do { bool ok=true; try { (void)(expr); } catch(...){ ok=false; } \
         mt::report(ok, #expr " does not throw", __FILE__, __LINE__, true); } while(0)
#define MICROTEST_MAIN int main(){ return mt::run(); }
```

**It builds clean under `-Wall -Wextra -pedantic`** and returns a non-zero exit code on failure, so it
works in a build script.

---

## Part A — A Test Suite That Can Fail (10 pts)

**A1.** *(4)* Write at least **eight** test cases over a container of your choice — your Week 6
`List<T>`, your BST, or Project 1's. Cover construction, insertion, removal, copying, moving,
iteration and at least one error path.

**A2.** *(3)* **Prove your tests can fail.** Deliberately break one assertion, run, and paste the
output showing the file, line and expression.

Then fix it and show the suite passing with a non-zero assertion count.

**A3.** *(3)* Confirm the suite **returns a non-zero exit code** when a test fails and zero when they
pass.

**Why does that matter?** One sentence.

---

## Part B — Testing the Error Paths (12 pts)

**B1.** *(6)* Use `REQUIRE_THROWS_AS` and `REQUIRE_NOTHROW` to test at least **four** documented error
behaviours — an out-of-range access, an invalid argument, an operation on an empty container, and one
of your choosing.

For each, **state what the contract is** before you test it.

**B2.** *(6)* Find one function in your container whose behaviour on failure you **cannot state**.

Write the test you *would* write, then answer: **is the missing thing a bug, or an undocumented
decision?** Justify in three sentences.

*(There is always at least one. If you think there is not, look at your destructor, or at what happens
when an element's copy constructor throws.)*

---

## Part C — The Throwing Element (12 pts)

**C1.** *(6)* Implement the `Fragile` element type from L29 §6 — one that throws on the *n*-th copy,
where *n* is settable.

**Verify it works**: a test that arms `throw_on_copy = 3`, copies three `Fragile`s, and requires the
third to throw.

**C2.** *(6)* Use it to determine, **by testing**, which guarantee your container's `push_back` (or
`insert`) provides.

**Sweep the failure point** across every copy the operation performs — not just the first. For each *n*:

- record the state before;
- arm the failure at *n*;
- run inside a `try`;
- check whether the state is unchanged (**strong**), merely valid (**basic**), or neither.

**Report a table of *n* against the guarantee observed.**

---

## Part D — What You Actually Provide (6 pts)

**D1.** *(4)* From your Part C table, state the guarantee your operation provides. **It is the weakest
one observed across all *n***, not the best.

Then answer: **did it match what you expected before testing?**

**D2.** *(2)* Take one operation that came out **basic** and describe — in three sentences, no code —
how you would make it strong, and what that would cost.

---

## Submission

- `tests.cpp`, `microtest.hpp` (or your Catch2 setup), and the container under test.
- `RESULTS.md` — the failing-test transcript, the Part C table, and all written answers.
- Machine, OS, compiler version at the top. **State which framework you used.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | A suite that genuinely reports failures |
| B | 12 | Testing contracts, and finding one you cannot state |
| C | 12 | The throwing element, swept across every failure point |
| D | 6 | Naming your guarantee honestly |
| **Total** | **40** | |

---

## Reference Output

The framework's own self-test, showing a deliberate failure:

```
arithmetic works
  passed (3 assertions)
exceptions are checked
  passed (3 assertions)
a deliberate failure, to prove failures are reported
  FAILED: 1 == 2
    at selftest.cpp:18
  FAILED (2 assertions)

2/3 test cases passed, 1 assertion failures
exit=1
```

**L29 §3–4's guarantee demonstration**, which Part C reproduces on your own container:

```
[BASIC]  before: size=2   caught: copy failed   after: size=4   <- valid, but CHANGED
[STRONG] before: size=2   caught: copy failed   after: size=2   <- UNCHANGED
```

---

## What This Lab Is Really Showing

**Part A2 is the part students find odd and it is the most important.** You are asked to break a test
and prove it fails.

A test suite that has never failed is not evidence of anything. It might be checking nothing —
a `REQUIRE` on a condition that is always true, a test case that never runs, an assertion inside a
branch that is never taken. **The only way to know your tests can detect a problem is to give them
one**, and doing it deliberately once is cheaper than discovering it during an incident.

**Part C is the week's real skill.** Anyone can write `try`/`catch`. Producing a table of failure points
against observed behaviour is *evidence*, and it is the difference between a container documented as
"strong" and one that is.

**And Part D1's rule — the weakest observed, not the best — is where the honesty lives.** An operation
that is strong for a failure in its first copy and basic for a failure in its third **provides basic**.
Reporting the best case is the most natural mistake in the world and it makes the documentation a lie.

That is what Project 1 Part 3.3 is asking for, and you now have the method.

---

*PROG 102 · Week 9 · Lab 9 · © CSE Department*
