# PROG 102 · Week 7 · Reading Guide
## The Gang of Four, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| **Gang of Four** | **Ch. 1** | What a pattern is, and the two principles. **The most valuable chapter in the book.** |
| **Gang of Four** | **Ch. 3** — Abstract Factory, Builder, Factory Method, Singleton | Read *Intent*, *Applicability*, *Consequences*. Skim the rest. |
| **Gang of Four** | **Ch. 4** — Adapter, Composite, Decorator, Facade | Same. |
| **Meyers, *Effective C++*** | **Items 32–36** | Inheritance design. Sharper than the GoF on when *not* to inherit. |
| **cppreference** | `std::stack`, `std::function` | Two patterns in the library |

> **A warning about this book.** *Design Patterns* is from **1994**. Its C++ predates templates being
> standardised, `unique_ptr`, lambdas, and move semantics. **Read it for the structure of the ideas and
> not for the code** — several examples use raw owning pointers in ways this course has spent five
> weeks teaching you not to.
>
> It is also written in a formal, catalogue style that reads badly cover-to-cover. **It is a reference
> book.** Read Chapter 1 properly, then look patterns up.

---

## Chapter 1 — The Chapter That Matters

**Guiding questions:**

1. §1.1 — the book's definition of a pattern has four parts: name, problem, solution, consequences.
   **Which of those four do people usually skip?** *(Consequences. Every time.)*
2. §1.6 — "**Favour object composition over class inheritance**". The book gives its reasoning.
   **Compare it with Lecture 13 §2's substitutability test.** Do they agree?
3. §1.6 — "**Program to an interface, not an implementation**". `std::sort` takes a template parameter
   rather than a base-class pointer. **Is that programming to an interface?** Argue it.
4. §1.8 — how to select a pattern. The book lists six approaches. **Which of the six is closest to
   Lecture 22 §6.2's test?**
5. The book says patterns make a design "more flexible". **Flexible along which axis?** Every pattern
   makes exactly one kind of change easy and usually makes another harder — find one where the book
   admits this.

---

## Chapter 3 — Creational

**Guiding questions:**

1. **Singleton.** The book's implementation uses a static pointer and lazy `new`. **Compare with
   Lecture 23 §2's four-line version.** What does the modern one fix, and what language feature made
   it possible?
2. **Factory Method vs Abstract Factory.** The names are confusingly similar. State the difference in
   one sentence. *(One product vs a family.)*
3. **Abstract Factory's Consequences** section lists a specific difficulty. **Find it** — it is the
   asymmetry from Lecture 23 §4, and the book is honest about it.
4. **Builder.** The book motivates it with a document converter. **Give a better modern example**, and
   say what makes a constructor a candidate. *(Lecture 23 §5.1 gives a rule of thumb.)*
5. The book lists **Prototype**, which this course skips. Read its Intent. **Why is it much less
   necessary in C++ than in Java?** *(Think about copy constructors.)*

---

## Chapter 4 — Structural

**Guiding questions:**

1. **Adapter.** The book distinguishes *class* adapters (inheritance) from *object* adapters
   (composition). **Which did Lecture 24 §2 use, and why?**
2. **Decorator's Consequences** section lists a specific drawback about identity. **Find it**, and
   connect it to Lab 7's debugging question.
3. **Composite.** The book explicitly discusses whether `add()` belongs on the base class.
   **Lecture 24 §4 disagrees with the book's leaning.** Read both and pick a side, with a reason.
4. **Facade.** The shortest pattern in the book. **What is the difference between a Facade and an
   Adapter?** They both wrap.
5. **Decorator vs Strategy** — the book compares them. Read the comparison now; **Week 8** implements
   Strategy and the distinction is worth having in advance.

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.** Counts are exact; timings are not.

### L23 §2.1 — The magic static

```
g++ -std=c++17 -O2 -Wall -Wextra -pthread magic.cpp -o magic && ./magic
g++ -std=c++17 -O2 -S -masm=intel guard.cpp -o guard.s && grep -oE '__cxa_guard_[a-z]+' guard.s | sort -u
```

**Expect:** 16 threads, **1** construction, all the same address; and
`__cxa_guard_acquire` / `_release` / `_abort` in the assembly.

**Under ThreadSanitizer:**

```
setarch $(uname -m) -R ./magic_tsan
```

**Expect:** zero race warnings.

> **If TSan dies with `FATAL: ThreadSanitizer: unexpected memory mapping`**, that is an ASLR problem on
> some Linux kernels, not your code. `setarch $(uname -m) -R` is the fix, and it is now recorded in
> Lab 0's toolchain notes. **Verified: TSan under `setarch` correctly finds a deliberate race and
> correctly reports none on the singleton.**

### L23 §3–5 — The creational patterns

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined creational.cpp -o c && ./c
```

### L24 §3.1, §3.3 — Decorator

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined structural.cpp -o s && ./s
g++ -std=c++17 -O2 -Wall -Wextra cost.cpp -o cost && ./cost
```

**Expect:** the $2^n$ table (10 features → **1024** vs **10**), and per-call times of 2.06 / 2.41 /
2.98 / 4.14 / 6.70 ns at depths 0 / 1 / 2 / 4 / 8 — a marginal cost of about **0.58 ns per layer**.

---

## A Change of Gear, and What Replaces Measurement

Six weeks of this course have settled questions by running something. **This week cannot**, and it is
worth being explicit about what takes its place.

There is no experiment that shows a Factory Method is right here. What there is:

- **A countable argument.** $2^n$ against $n$ is not a matter of taste, and Lecture 24 §3.1 settles the
  Decorator question the way a benchmark would settle a performance one.
- **A cost you can measure even when the benefit cannot be.** 0.58 ns a layer does not tell you whether
  to use a decorator — but it tells you the objection "it's too slow" is unavailable.
- **A named change.** Lecture 22 §6.2's test — *name the change this makes easy, and say whether it is
  coming* — converts an aesthetic argument into a factual one about your requirements.

> **Where you cannot measure, quantify what you can and be explicit about the rest.** Lab 7 Part D
> asks you to report that the refactor took 10 classes to 8 — an unimpressive number — and then to
> explain why the count is the wrong measure. **That is the skill: reporting the weak evidence you
> have rather than the strong evidence you would like.**

---

## Before Week 8

1. Lectures 22–24 read; **GoF Chapter 1 read properly.**
2. PS 7 started — it is lighter than PS 6 on purpose.
3. **Project 1's Parts 1 and 2 should be working.** It is due Week 9 and Week 9 is exception safety,
   which is not a week you want to spend writing a BST iterator.
4. Week 8 is the **behavioural** patterns, and it ends with two that C++11 made nearly obsolete — the
   clearest possible evidence that the catalogue is a field report from 1994 and not a rulebook.

---

*PROG 102 · Week 7 · Reading Guide · © CSE Department*
