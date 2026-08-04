# PROG 102 · Week 5 · Reading Guide
## *C++ Primer* Chapters 12–13, Meyers Items 18–25, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| ***C++ Primer*** | **§12.1.1–12.1.6** | Smart pointers. The core reading. |
| ***C++ Primer*** | **§13.6** | Rvalue references and move. |
| **Meyers, *Effective Modern C++*** | **Items 18–22** | Smart pointers. **The best treatment of this week anywhere.** |
| **Meyers** | **Items 23–25, 29** | `std::move`, forwarding, move-aware containers. |
| **cppreference** | `unique_ptr`, `shared_ptr`, `weak_ptr` | For the exact guarantees |

> **This is the week Meyers becomes the primary text.** *C++ Primer* covers smart pointers correctly
> but treats them as library types; Meyers treats them as design decisions, which is what they are.
> **Item 18** (`unique_ptr` for exclusive ownership), **Item 19** (`shared_ptr`), **Item 20**
> (`weak_ptr`) and **Item 21** (prefer `make_unique`/`make_shared`) are four short chapters and are
> the single highest-value reading of the semester so far.

---

## §12.1 — Dynamic Memory and Smart Pointers

**Guiding questions:**

1. §12.1.1 — the book introduces `shared_ptr` **first**. Lecture 17 argues `unique_ptr` should be your
   default. **Which do you agree with, and why?** *(This is a real disagreement, not a trick.)*
2. §12.1.3 — `unique_ptr` cannot be copied. **Is that a limitation or the point?** Answer in terms of
   what two owners would do.
3. §12.1.4 — `weak_ptr`. The book explains `lock()`. **Why can you not simply check `expired()` and
   then dereference?**
4. §12.1.5 — dynamic arrays. The book covers `unique_ptr<T[]>`. **When should you use it instead of
   `std::vector`?** *(The honest answer is "almost never" — say why.)*
5. The book does **not** cover reference cycles in depth. Read Lecture 17 §5 and Meyers Item 20
   alongside.

---

## §13.6 — Move Semantics

**Guiding questions:**

1. §13.6.1 — rvalue references. **What does `&&` bind to that `&` does not, and why does that make
   stealing safe?**
2. §13.6.2 — the move constructor. The book stresses leaving the source in a valid state. **What
   exactly does "valid but unspecified" permit you to do?** Give one legal and one undefined operation.
3. §13.6.2 — `noexcept` on move operations. The book explains why `vector` needs it. **Restate the
   argument in terms of the strong exception guarantee** from Week 1.
4. §13.6.3 — the book's `Message` class. **Could it have been written under the Rule of Zero?** What
   would you have changed?

---

## Meyers Items 18–25 — The Reading That Matters

- **Item 18** — `unique_ptr` for exclusive ownership. Note his point about factory functions returning
  `unique_ptr`, which is Lecture 16 §6.
- **Item 19** — `shared_ptr`. **Read the control-block section carefully**; it explains why
  `shared_ptr<T>(new T)` and `make_shared<T>()` differ in allocations.
- **Item 20** — `weak_ptr`. His caching example is worth working through.
- **Item 21** — prefer `make_unique`/`make_shared`. **He gives the exception where you should not**,
  which Lecture 17 §3 also flags. Make sure you can state it.
- **Item 23** — `std::move` and `std::forward`. His framing: *`std::move` performs an unconditional
  cast to an rvalue and does not move.* That is Lecture 18 §4 in one sentence.
- **Item 25** — use `std::move` on rvalue references and `std::forward` on universal references.
  Skim; Week 11 returns to forwarding.

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.** `sizeof` and allocation counts are exact; timings are not.

### L16 §5.1–5.2 — `unique_ptr` costs nothing

```
g++ -std=c++17 -Wall -Wextra sizes.cpp -o sizes && ./sizes
g++ -std=c++17 -O2 -S -masm=intel zero2.cpp -o zero2.s
```

**Expect:** `unique_ptr` 8 bytes; `raw_param(Widget*)` and `uniq_param(Widget&)` **byte-identical**.

### L16 §5.3–5.4 — …except that it also works

```
g++ -std=c++17 -O0 exc3.cpp -o e0 && ./e0 && ./e0 x
g++ -std=c++17 -O2 exc3.cpp -o e2 && ./e2 && ./e2 x
```

**Expect:** raw `allocs=2 frees=1` (**leaked**), `unique_ptr` balanced, at **both** levels.

**Then the trap.** Change the throw to be unconditional and rerun the raw version at `-O2`:

```
g++ -std=c++17 -O2 exc2.cpp -o e2u && ./e2u
```

**Expect:** it reports *balanced* — because GCC deleted the allocation as dead code. **The benchmark
measured a program that no longer allocated.**

### L16 §8 — RAII does not fix the virtual destructor

```
g++ -std=c++17 -Wall -Wextra -c uniqdtor.cpp -o /dev/null                  # 0 warnings
g++ -std=c++17 -Wall -Wextra -Wnon-virtual-dtor -c uniqdtor.cpp -o /dev/null   # 3 warnings
g++ -std=c++17 -g -fsanitize=address uniqdtor.cpp -o u && ./u
```

**Expect:** `new-delete-type-mismatch`, and **no warning** from `-Wall -Wextra` — the `delete` is
inside the library.

### L17 §3–4 — What sharing costs

```
g++ -std=c++17 -O2 shared.cpp    -o shared    && ./shared        # allocation counts
g++ -std=c++17 -O2 copycost2.cpp -o copycost2 && ./copycost2     # per-operation times
g++ -std=c++17 -O2 -S -masm=intel atomic2.cpp -o atomic2.s
grep -c 'lock ' atomic2.s          # compare with and without -pthread
```

**Expect:** 2 / 1 / 1 allocations; copy overhead ≈4 ns; **the same lock count with and without
`-pthread`.**

### L17 §5–6 — The cycle

```
g++ -std=c++17 -O2 -g -fsanitize=address cycle.cpp -o cycle
./cycle && ./cycle x
```

**Expect:** 80 bytes leaked in 2 allocations and **no destructors**, then both destructors and no leak.

### L18 §3.1, §8 — Moves

```
g++ -std=c++17 -O2 move3.cpp -o move3 && ./move3       # 1 MB buffers
g++ -std=c++17 -O2 move2.cpp -o move2 && ./move2       # push_back, both orders
```

**Expect:** copy ~1 ms per 1 MB, move ~0.1 µs. And `push_back(std::move(s))` **1.13–1.18× faster —
with `reserve`.** Without it, the move version measures *slower*.

---

## The Habit, in Its Fifth Form

The instruction has been sharpened once a week:

- **W0:** do not believe a claim you have not seen a compiler make.
- **W1:** advice can be fifteen years out of date.
- **W2:** a correct measurement can carry a wrong explanation. *Run a control.*
- **W3:** a correct theory can answer a different question. *Measure what you do.*
- **W4:** your benchmark may be measuring something other than what you named it.

**Week 5 adds the one that is hardest to defend against:** *the optimizer can delete the thing you are
measuring.*

Lecture 16 §5.4's raw-pointer leak vanished at `-O2` — not because the leak was fixed, but because GCC
proved the allocation was unreachable and removed it. The program under test stopped existing and the
benchmark reported success.

**There is no general defence.** The specific ones — consume every result, make conditions
non-constant, check the assembly when a number looks too good — are what this week's exercises drill.
And the general instinct is the one this course keeps returning to:

> **When a measurement agrees with what you wanted, that is when to check it hardest.**

---

## Before Week 6

1. Lectures 16–18 read.
2. **Meyers Items 18–21.** Four short chapters; do not skip them.
3. *C++ Primer* §12.1 and §13.6.
4. **PS 5 started — after the midterm, not before.**
5. Week 6 builds a templated linked list and BST with `unique_ptr` nodes and real iterators, and
   **Project 1 is assigned.** It is the first assignment that gives you an interface to satisfy rather
   than a class to write, and Lecture 18's **Rule of Zero** is exactly what it will test you on
   knowing when *not* to apply.

---

*PROG 102 · Week 5 · Reading Guide · © CSE Department*
