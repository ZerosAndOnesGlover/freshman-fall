# PROG 102 · Lecture 37
## Testing and Test-Driven Development

**Week 12 · Tuesday · 50 minutes**
**Reading:** cppreference on assertions; Catch2 documentation · **Assumes:** Week 9 (Lab 9)

**Date:** Tuesday 6 April 2027 · 10:00–10:50 · Week 12

---

## 1. What a Test Is For

**A test encodes a claim about behaviour so that a machine can check it.** That is all, and it is
enough.

Three things follow, and they are the reasons to write tests rather than the slogans usually given:

- **A test is documentation that cannot go stale.** A comment saying "throws on an empty container" may
  be a lie; a test saying it is either true or failing.
- **A test lets you change code.** Week 6's containers were rewritten in Project 2; the only reason
  that is safe is a suite that says whether you broke something.
- **A test is a place to put a bug.** When you fix one, the test is what stops it coming back.

---

## 2. Unit, Integration, System

| Level | Tests | Fast? | Where the bugs are |
| --- | --- | --- | --- |
| **Unit** | one class or function, isolated | yes — milliseconds | most |
| **Integration** | several components together | seconds | the interesting ones |
| **System** | the whole program | slow | the embarrassing ones |

**Most of your tests should be unit tests**, because they are fast enough to run on every save and
precise enough to say what broke.

> **But the interesting bugs are at the boundaries.** Every component of Lab 8's event bus worked; the
> bugs were in how they combined — re-entrancy, ordering, lifetime. **Unit tests would not have found
> any of them**, and that is the standard limitation rather than a failure of the technique.

---

## 3. What Makes a Good Test

**One claim per test.** A test asserting six things fails on the first and tells you nothing about the
other five.

**A name that states the claim.** `pop_on_empty_throws` is better than `test3`, and the name is what
you read in the failure output.

**Arrange, act, assert.** Set up, do one thing, check. If you cannot see those three parts, the test is
doing too much.

**Independent of order.** A test that only passes after another has run is a trap for whoever adds a
seventh test.

**And — from Week 9 §Lab 9 A2 — a test you have watched fail.** A suite that has never failed may be
asserting nothing at all.

### 3.1 Test the Failures

**This is where most suites are thin.** You test that `push` works. Do you test:

- what happens on an **empty** container?
- what happens at **capacity**?
- what an operation does when an element's copy **throws** (Week 9)?
- what a **moved-from** object supports (Week 5)?
- what happens with a **self-assignment** (Week 1)?

**Every one of those is a documented behaviour**, and every one of them is a place this course has
shown you a bug. **Project 2 Part 2.2 requires the third.**

---

## 4. Test-Driven Development

> **Red, green, refactor.** Write a failing test. Write the least code that passes it. Clean up. Repeat.

**The honest case for TDD is not that it produces better code.** The evidence for that is weak and
much-argued. It is that:

- **You cannot write a test for code with an unusable interface**, so writing the test first forces you
  to design the interface from the caller's side. This is TDD's strongest and least-disputed benefit.
- **The test is guaranteed to be able to fail**, because you watched it fail. §3's last point, obtained
  automatically.
- **You always know where you are.** Every step is small and the suite is green or it is not.

**The honest case against:** it is poorly suited to exploratory work where you do not yet know the
design, and it can produce a suite that tests the implementation rather than the behaviour — which then
resists exactly the refactoring it was meant to enable.

> **Use it where the interface is the hard part** — a container, a parser, an API. **Do not force it**
> where you are still finding out what you are building. Both positions are defensible and the
> dogmatic version of either is not.

---

## 5. Coverage

```
g++ --coverage prog.cpp -o prog && ./prog && gcov prog.cpp
```

**Coverage tells you which lines ran. It does not tell you whether they were checked.**

```cpp
TEST_CASE("push works"){
    Stack<int> s;
    s.push(1);              // 100% coverage of push. Zero assertions.
}
```

**That test achieves full line coverage of `push` and verifies nothing.**

> **Coverage is a useful negative signal and a worthless positive one.** Zero coverage of a function
> means it is definitely untested. Full coverage means only that the lines executed.
>
> **Chase uncovered lines; do not chase a percentage.** A team targeting 90% will get 90%, and the
> tests written to reach it will be the ones with no assertions.

---

## 6. What to Do With a Bug

The discipline, in order:

1. **Reproduce it.** Reliably, with the smallest input you can find.
2. **Write a failing test.** Now it is a claim, not a story.
3. **Fix it.**
4. **Watch the test pass** — and confirm nothing else broke.
5. **Keep the test.**

**Step 2 is the one people skip**, and it is the one that stops the bug returning in six months when
somebody refactors.

> **You have done this all semester without the label.** Lab 1's four faults, Lab 5's five, Lab 10's
> five — each time you reproduced, fixed, and re-ran. **The only step missing was writing the test
> down**, and Project 2 asks for it.

---

## 7. Summary

| Idea | The point |
| --- | --- |
| A test | A claim about behaviour, checkable by a machine |
| Documentation that cannot go stale | Unlike the comment above it |
| Unit / integration / system | Most tests unit; **the interesting bugs are at boundaries** |
| One claim per test | A test asserting six things reports one |
| **Test the failures** | Empty, full, throwing, moved-from, self-assigned |
| A test you have watched fail | Otherwise it may assert nothing |
| **TDD's real benefit** | It forces the interface to be designed from the caller's side |
| Where it fits badly | Exploratory work, and when it tests the implementation |
| **Coverage** | Useful negative signal, worthless positive one |
| Bug discipline | Reproduce → **failing test** → fix → pass → keep |

---

## 8. Exercises

**1.** Take your Project 2 test suite and count: how many tests check a **failure** path? **Report the
ratio** to success-path tests.

**2.** Find one test asserting more than one claim and split it. **Which version tells you more when it
fails?**

**3.** Write a test with full line coverage of a function and **no assertions**. Run coverage and show
100%. Then say in one sentence what coverage measured.

**4.** Take one bug you hit this semester — from any lab — and write the test you should have written.
**Confirm it fails against the old code.**

**5.** Implement one small class TDD-style: failing test, minimum code, refactor, repeat, at least four
cycles. **Report whether the interface differed** from what you would have written first.

**6.** Find a behaviour in your Project 2 that is **documented but untested**. Write the test. **Did it
pass?**

**7.** Argue against TDD in four sentences. **Then argue for it in four.** Mark yourself on which was
harder.

---

## 9. Next

**Lecture 38** is profiling: how to find out where the time actually goes, which is almost never where
you thought. It also explains why the first thing to do with a slow program is **not** to optimise the
loop you are looking at.

---

*PROG 102 · Week 12 · Lecture 37 · © CSE Department*
