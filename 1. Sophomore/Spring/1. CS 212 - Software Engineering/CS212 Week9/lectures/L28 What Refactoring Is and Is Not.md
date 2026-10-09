# CS 212 · Software Engineering
## Week 9 · Lecture 1 of 3
### What Refactoring Is, and What It Is Not

*“When you find you have to add a feature to a program, and the program's code is not structured in a convenient way to add the feature, first refactor the program to make it easy to add the feature, then add the feature.”* — Martin Fowler, *Refactoring* (1999)

---

**Sat:** Tuesday of Week 9, 10:00–10:50, TH 200 · **⚠️ Quiz 9 in the first ten minutes** — covers Week 8 · **Reading:** Fowler, *Refactoring*, 2nd ed., Ch. 1–2 · **Next:** L29, the catalogue

**Coursework:** 📊 **Quiz 9** today · 📝 **Assignment 9** released Wed this week 17:00, due Fri of Week 10 17:00 · 📝 **Assignment 8** due Fri this week 17:00

---

## 1. The Definition, and Why the Precision Matters

**Fowler's, and every word of it is load-bearing:**

> **Refactoring** *(noun)*: a change made to the internal structure of software to make it easier to
> understand and cheaper to modify **without changing its observable behaviour.**
>
> **Refactor** *(verb)*: to restructure software by applying a series of refactorings **without
> changing its observable behaviour.**

**"Without changing observable behaviour" is not a guideline. It is the definition**, and it is what makes refactoring safe enough to do continuously.

**So three things people call refactoring are not:**

| What people say | What it actually is | Why the distinction matters |
|---|---|---|
| *"I'm refactoring the booking module"* — and fixing two bugs | **Refactoring plus behaviour change** | If a test fails you cannot tell which half broke it |
| *"We're refactoring to the new architecture"* — six weeks, one branch | **A rewrite** | It carries a rewrite's risk and has none of a refactoring's safety |
| *"Refactoring the CSS"* — making it prettier | **Tidying** | Harmless, but not a technique with a safety property |

> **The operational test, and it is the one to use in review:** **if a test had to change, it was not
> a refactoring.** Tests encode observable behaviour. A change that requires editing a test has
> changed what the system does, and it needs the argument and the care that a behaviour change needs.

**This is why A 2 and A 4 both said "the tests must pass unchanged".** It was not a marking convenience; it is the definition being enforced.

---

## 2. Refactoring Requires Tests, and Therefore Is Often Impossible

**The awkward fact at the centre of the week.**

Refactoring is safe because the tests tell you when you broke something. **`confirm_booking` has 47% branch coverage, 31.8% with branches counted, and eleven tests against ninety-four independent paths.** You cannot refactor it safely, because nothing will tell you when you have broken it.

**Feathers' definition is the honest one:**

> *"Legacy code is code without tests."*
> — Feathers, *Working Effectively with Legacy Code* (2004)

**Deliberately unkind and operationally exact.** What makes code legacy is not age — it is that **you cannot change it safely**, and tests are the mechanism that makes change safe.

**Which produces the deadlock that every real codebase has:**

> **To refactor safely you need tests. To write tests you need seams. To create seams you must
> refactor.**

**The way out is the characterisation test**, and it is the most useful technique in this lecture.

---

## 3. Characterisation Tests: Pinning Behaviour You Do Not Understand

**A characterisation test does not assert what the code *should* do. It asserts what it *does* do.**

The procedure, on `roomsvc`'s pricing:

**Step 1. Write a test that asserts something obviously wrong.**

```python
def test_characterise_external_partner_price():
    assert price_for(booking(kind="external_partner", hours=2)) == Decimal("0")
```

**Step 2. Run it, and read the failure.**

```
E   assert Decimal('86.40') == Decimal('0')
```

**Step 3. Put the actual value in.**

```python
def test_characterise_external_partner_price():
    # Characterisation only. NOT a statement that 86.40 is correct --
    # a statement that 86.40 is what this code returns today.
    assert price_for(booking(kind="external_partner", hours=2)) == Decimal("86.40")
```

**Now you have a test.** It may be pinning a bug — and if so, **you want it pinned**, because the point is to detect *change*, not to validate correctness. **Correctness is a separate conversation with the finance office.**

**Do this for every branch you are about to touch.** For `price_for` that is seven tests and about twenty minutes, and afterwards the open/closed refactoring from A 2 is safe rather than hopeful.

> **The comment is mandatory.** A characterisation test that looks like a normal test will be read as
> a specification by the next person, and they will defend the bug. **Say in the test that it records
> behaviour rather than endorsing it.**

**Two tools make this cheaper:**

- **Approval testing** (`pytest-approvaltests`, or a hand-rolled snapshot): capture the whole output, commit it, and diff subsequent runs. **Good for `render_week`**, whose output is 40 lines of HTML that nobody wants to assert by hand.
- **Coverage as a checklist.** Run coverage over your characterisation tests. **The uncovered branches are the ones you have not pinned**, and they are exactly the ones your refactoring can silently break (W6 L19 §3).

---

## 4. The Two Hats

**Fowler's discipline, and it is the single most practical idea in the week.**

> **You are either adding functionality or refactoring. You are never doing both. You may swap hats
> often — several times an hour — but you wear one at a time.**

| Hat | You may | You may not |
|---|---|---|
| **Adding functionality** | Add tests, add code, make tests pass | Restructure existing code |
| **Refactoring** | Restructure, move, rename, extract | **Add a test, or change one** |

**Why the discipline pays, concretely.** When a test goes red while you are refactoring, **you know it was your restructuring**, because nothing else changed. The diagnosis is immediate. Mixing the hats means every red test has two possible causes and you bisect by hand.

**This maps directly onto your commits**, which is why A 4 asked for a `refactor:` commit with no behaviour change and A 2 asked for formatting separated from logic:

```
test:     characterise existing pricing behaviour   (7 tests, all passing)
refactor: extract PricingPolicy per booking kind    (tests unchanged, green)
refactor: replace kind switch with registry lookup  (tests unchanged, green)
feat:     add external_partner_charity kind         (1 new test)
```

**Four commits, and each one is independently reviewable and independently revertable.** That is the property W7 L22 §4's size evidence says you want, arrived at from a different direction.

---

## 5. When to Refactor

**Not "as a project".** Fowler's own guidance, and it is deliberately opportunistic:

| Trigger | |
|---|---|
| **The rule of three** | Third time you see the same thing, restructure it (W2 L09 §2) |
| **Preparatory refactoring** | *"I need to add a feature here, and it would be easier if the code looked like this first."* **The most valuable kind** |
| **Comprehension refactoring** | You are reading code to understand it; as you understand, you rename and extract so the next reader does not have to. **Your understanding goes into the code rather than into your head** |
| **Litter-pickup refactoring** | You notice something small and wrong; you fix it because you are here |

**Preparatory refactoring is the one that changes how you work.** The instinct is to add the feature to the code as it is, in whatever shape that forces. **The better move is: make the change easy, then make the easy change** — two commits, the first behaviour-preserving.

**And the honest note on "a refactoring sprint":**

> **A fortnight of pure refactoring with no feature delivered is almost always a mistake**, for two
> reasons. It produces a large, hard-to-review, hard-to-revert change — every property W7 says makes
> review fail. And **it optimises code whose future you are guessing at**, rather than code you are
> about to change, so you have no evidence about which axis matters (W2 L08 §2).
>
> **Refactor along the path of work you are actually doing.** The `git log` tells you where that is.

---

## 6. Where Refactoring Is Genuinely Dangerous

Four cases where the safety property weakens, and you should know them before Week 11's debt register asks you to prioritise.

| Case | Why | What to do |
|---|---|---|
| **No tests** | The safety property is gone entirely | Characterisation tests first. §3 |
| **Concurrency** | A restructuring can change *timing*, and timing is observable in ways your tests are not watching. **Moving a database call outside a lock preserves every unit test and introduces a race** | Treat as a behaviour change. Reason explicitly about the critical section |
| **Performance-sensitive code** | Extracting a function, adding a layer, replacing a loop with a comprehension — **all preserve behaviour and can change latency by an order of magnitude** | **Measure before and after.** Keep the slow obvious version as an oracle (W6 L20 §3) |
| **A public interface** | Observable behaviour includes what *other people's code* observes. Renaming a private method is a refactoring; renaming an API field is a **breaking change** | Week 10. Expand and contract |

**The concurrency row is the one relevant to `slot` right now.** Your booking confirmation has a critical section; **a well-intentioned "extract method" that moves the `INSERT` away from its guard reproduces the VNC 101 bug**, passes every unit test, and is invisible in review. **Ask the L23 pass-3 question of your own refactorings: can two of these run at once?**

---

## 7. Summary

- **Refactoring is a change to internal structure that does not change observable behaviour.** The clause is the definition, not a guideline. **The operational test: if a test had to change, it was not a refactoring.**
- **Three things are not refactoring**: restructuring plus a bug fix, a six-week rewrite on a branch, and tidying.
- **Refactoring requires tests, so it is often impossible** — `confirm_booking` has eleven tests for ninety-four paths. ***"Legacy code is code without tests"*** is unkind and exact: what makes code legacy is that you cannot change it safely.
- **The deadlock — tests need seams, seams need refactoring — is broken by characterisation tests**, which assert what the code *does*, not what it should. **Write the wrong assertion, read the failure, paste the value in, and comment that it records rather than endorses.** Use coverage over them as a checklist for what you have not pinned.
- **The two hats: adding functionality or refactoring, never both.** Then a red test has exactly one possible cause, and your commits are independently revertable.
- **Refactor opportunistically**: rule of three, **preparatory** (*make the change easy, then make the easy change*), comprehension, litter-pickup. **A pure refactoring fortnight is usually a mistake** — unreviewable, unrevertable, and optimising code whose future you are guessing at.
- **Four dangerous cases**: no tests, **concurrency** (an extract-method can move an `INSERT` out of its critical section and reproduce VNC 101 while every unit test passes), performance-sensitive code, and **a public interface** — which is Week 10.

**Next:** L29 — the smell catalogue, applied to `roomsvc`, and the moment the bug this course opened with gets removed.

---

*CS 212 · Week 9 · L28 · © CSE Department*
