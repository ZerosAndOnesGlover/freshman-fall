# PROG 102 · Week 4 · Reading Guide
## *C++ Primer* Chapter 15, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| ***C++ Primer*** | **§15.1–15.5** | Inheritance and virtual functions. The core reading. |
| ***C++ Primer*** | **§15.7–15.8** | Containers of pointers, and text queries — a worked hierarchy. |
| ***C++ Primer*** | **§19.2** | `dynamic_cast` and `typeid`. |
| **Meyers, *Effective C++*** | **Items 7, 32–36** | Item 7 is the virtual destructor rule. 32–36 are inheritance design and are excellent. |
| **Stroustrup** | **Ch. 20** | Reference for the mechanism. |

> **Meyers Item 7 is four pages and is the best short treatment of Lecture 15 §2 anywhere.** If you
> read one thing outside the lectures this week, read that. Items 32–36 are the reading you will want
> again in Weeks 7–8.

---

## §15.1–15.2 — Base and Derived

**Guiding questions:**

1. The book stresses that a derived object **contains** a base sub-object. **Where is it in memory?**
   Lab 4 lets you answer this by printing addresses.
2. §15.2.2 — the derived constructor initializes the base. What happens if you omit it? What if the
   base has no default constructor?
3. §15.2.3 — the book covers `protected`. **Give one concrete reason to prefer a `protected` accessor
   over a `protected` data member.**
4. §15.2.4 — preventing inheritance with `final`. Besides intent, what does `final` let the compiler
   do? *(L14 §6.)*

---

## §15.3 — Virtual Functions

The chapter's core.

**Guiding questions:**

1. The book says a virtual function is virtual "all the way down" once declared. **Why is `override`
   still worth writing?**
2. §15.3 — calling a virtual function with the scope operator (`base->Shape::area()`) suppresses
   dispatch. When would you want that?
3. **The book describes the vtable only briefly.** Read Lecture 14 §3–4 alongside, and note which
   parts of the mechanism are *guaranteed by the standard* and which are *how GCC happens to do it*.
   That distinction matters and the book does not draw it.
4. §15.3 covers default arguments in virtual functions. **This is a genuine trap** — look up what
   happens when the base and derived declare different defaults, and say which one is used.

---

## §15.4–15.5 — Abstract Classes and Access

**Guiding questions:**

1. Why can you have a `Shape*` but not a `Shape`?
2. §15.5 — `public`, `protected` and `private` inheritance. **Which one means is-a?** What does
   `private` inheritance mean, and what would you use instead?
3. The book notes that friendship is not inherited. Construct an example where that surprises you.

---

## §19.2 — `dynamic_cast` and `typeid`

**Guiding questions:**

1. What must be true of a type for `dynamic_cast` to work on it?
2. What does `dynamic_cast` on a **reference** do on failure, and why is it different from the pointer
   case?
3. The book presents `typeid`. **Compare a `typeid` chain with a `dynamic_cast` chain with a virtual
   function** — three ways to do the same thing. Rank them and justify.

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.** `sizeof` values and GDB structure will match; addresses and timings will
not.

### L14 §3.1 — What a vptr costs

```
g++ -std=c++17 -Wall -Wextra vptr.cpp -o vptr && ./vptr
```

**Expect:** 4, 16, 16, 8. Ten virtuals cost the same as one.

### L14 §4 — The vtable in GDB

```
g++ -std=c++17 -O0 -g gdbdemo.cpp -o gdbdemo
gdb -q ./gdbdemo
(gdb) break 24
(gdb) run
(gdb) info vtbl sq
(gdb) p *(void**)&sq
(gdb) p ((void***)&sq)[0][2]
```

**Expect:** slot 0 is `area`, slot 1 is `name`, slot 2 is the destructor, and the vptr reads
`<vtable for Square+16>`.

**This is Lab 4.** Do it there rather than here.

### L14 §5 — The cost, in three attempts

```
g++ -std=c++17 -O2 vcost.cpp  -o vcost  && ./vcost     # attempt 1: pointers
g++ -std=c++17 -O2 vcost2.cpp -o vcost2 && ./vcost2    # attempt 2: unequal sizes
g++ -std=c++17 -O2 vcost3.cpp -o vcost3 && ./vcost3    # attempt 3: controlled
```

**Expect** each attempt to give a different answer, with the first the largest.

### L14 §6 — Speculative devirtualization

```
g++ -std=c++17 -O2 -S -masm=intel callsite.cpp -o callsite.s
sed -n '/^_Z8via_baseRK5Shape:/,/ret/p' callsite.s
```

**Expect** a `cmp` against a function address and a `jne`, followed by an inlined body.

### L14 §7 — The vectorization barrier

```
g++ -std=c++17 -O3 -fopt-info-vec vecloop.cpp -c -o /dev/null
```

**Expect** the non-virtual loop reported as vectorized and the virtual one absent. **Then check whether
that changes the ratio** — on the reference machine it did not.

### L15 §2 — The virtual destructor

```
g++ -std=c++17 -Wall -Wextra -g -fsanitize=address dtor.cpp -o dtor
./dtor        # non-virtual
./dtor x      # virtual
g++ -std=c++17 -Wall -Wextra -c warncond.cpp -o /dev/null       # when does it warn?
```

### L15 §3–4 — Slicing and casting

```
g++ -std=c++17 -O2 slice.cpp    -o slice    && ./slice
g++ -std=c++17 -O0 downcast.cpp -o downcast && ./downcast
g++ -std=c++17 -O2 dyncost.cpp  -o dyncost  && ./dyncost
```

---

## The Habit, in Its Fourth Form

Each week has sharpened the same instruction.

- **Week 0:** do not believe a claim about C++ you have not seen a compiler make.
- **Week 1:** advice can be fifteen years out of date. Measure it.
- **Week 2:** a correct measurement can carry a wrong explanation. Run a control.
- **Week 3:** a correct theory can answer a slightly different question. Measure what you actually do.

**Week 4 adds:** *your own benchmark can be measuring something other than what you named it.*

Lecture 14 §5 took three attempts to measure one thing. Attempts 1 and 2 were not sloppy — they were
reasonable programs that produced reasonable numbers, and both numbers answered a question nobody had
asked. Only the third controlled for object size.

And then §7.1 found that the mechanism everyone cites for virtual-call cost — blocked vectorization —
**was real and did not explain the gap**. Verified in both directions, and the tidy story lost.

> **The recurring skill is not measurement. It is asking what your number is a number *of*.**

Section D of Midterm 1 is fifteen marks of exactly this.

---

## Before Week 5

1. Lectures 13–15 read.
2. *C++ Primer* §15.1–15.5 worked through; Meyers Item 7 read.
3. **PS 4 Parts A and C started.**
4. **[[PROG102 Week4/resources/MIDTERM 1 Revision Guide|MIDTERM 1 Revision Guide]] read once, this week.** It tells you what is examinable
   and what Section D expects, and both are easier to act on with two weeks left than with two days.
5. Week 5 is **RAII and smart pointers**, and it is the week that retires most of the manual memory
   management you have been doing since Week 0. **The midterm is the same week.**

---

*PROG 102 · Week 4 · Reading Guide · © CSE Department*
