# CS 212 · Quiz 5
## Administered: Tuesday, Week 5 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 4** — design patterns: the catalogue, what survives in Python, and refactoring toward a pattern.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Alexander's definition has three clauses. Give the one about *problems*, and say what it rules out.

&nbsp;

&nbsp;

---

**Q2.** State Norvig's 1996 claim, and give three patterns it applies to with what each becomes in Python.

&nbsp;

&nbsp;

---

**Q3.** Adapter, Facade, Decorator and Proxy all wrap an object. What distinguishes them?

&nbsp;

&nbsp;

---

**Q4.** Why is Singleton a mistake, and what is the alternative?

&nbsp;

&nbsp;

---

**Q5.** L15 calls inheritance "very strong coupling". Name the form of connascence, and why it is worse than most.

&nbsp;

&nbsp;

---

**Q6.** Name two of the four things that bite a team adopting an event bus. One of them is Week 0's bug — which?

&nbsp;

&nbsp;

---

**Q7.** Give the three tests from L13 §5 against pattern-oriented programming.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** *"Each pattern describes **a problem which occurs over and over again** in our environment…"*

**It rules out naming a pattern for its structure.** A pattern is named for its problem — which is why **Decorator and Proxy have identical structure and are two different patterns.** If you cannot state the problem, you do not have a pattern.

---

**Q2.** **16 of the 23 GoF patterns are "invisible or simpler" in a dynamic language.**

Any three: **Strategy** → a function argument. **Command** → a closure or `functools.partial`. **Iterator** → `yield`. **Singleton** → a module. **Factory Method** → a function. **Visitor** → `singledispatch`. **Prototype** → `copy.deepcopy`.

*The structures dissolve; the problems do not.*

---

**Q3.** **Intent, and only intent.**

| | Wrapper's interface | Intent |
|---|---|---|
| **Adapter** | Different | Make an incompatible thing fit |
| **Facade** | New, simpler, over several | Hide complexity |
| **Decorator** | Same | Add behaviour transparently |
| **Proxy** | Same | Control access — cache, defer, authorise, go remote |

**Decorator and Proxy are structurally identical.** That is the clearest demonstration that a pattern is named for its problem.

---

**Q4.** **It is a global variable with a nicer name**: untestable (tests share state and fail by order), a hidden dependency (the signature lies about what the function needs), almost always the wrong lifetime (per-process, when you wanted per-request), and needs a lock if lazily initialised.

**The alternative: pass it as an argument.** Three extra characters at the call site, and the function tells the truth about its dependencies. **In Python it is also unnecessary — modules are already singletons.**

---

**Q5.** **Connascence of execution order**, across a class boundary.

Worse than most because **it appears in no signature.** A subclass depends on the order in which the base class calls its hooks, and nothing states that order. `roomsvc`'s `BaseReport` has **two subclasses that override `generate()` itself**, which defeats the pattern and is invisible unless you read all five.

---

**Q6.** Any two of: **a raising handler kills the rest of them**; **order is not guaranteed and will be relied on anyway**; **you cannot answer "what happens next?" by reading**; **publishing inside a transaction** means emailing about a booking that then rolls back.

**The last one is Week 0's bug with the arrow reversed** — `roomsvc` had the side effect inside the transaction; here the transaction rolls back under a completed side effect. **Publish after commit, or use the outbox.**

---

**Q7.** **1. Name the problem**, not the pattern. **2. Name the second case** — a Strategy with one strategy is a function with extra steps. **3. Count the files a reader must open** to answer one behavioural question, before and after. If it went up and nothing else got better, revert.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L13 §1, §3 |
| **Q3** | **L14 §7** — the table is one of the two most likely midterm short questions |
| Q4 | L14 §4 |
| Q5 | L15 §1 |
| **Q6** | **L15 §2** — and check whether your own event bus publishes inside a transaction |
| **Q7** | **L13 §5** — A 4 Q1(c) is marked on exactly these three |

**Q6 and Q7 are the ones that recur.** Q6 is a bug you can still introduce into your own project this fortnight; Q7 is the judgement Week 9 formalises and the final report is marked on.

---

*CS 212 · Week 5 · Quiz 5 · covers Week 4 · ungraded*
