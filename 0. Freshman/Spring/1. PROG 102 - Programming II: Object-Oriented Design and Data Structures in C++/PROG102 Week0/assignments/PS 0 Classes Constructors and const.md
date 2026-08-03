# PROG 102 · Problem Set 0
## Classes, Constructors, and `const`

**Week 0 · Released Friday Week 0 · Due Friday Week 1, 17:00 · 100 points**
**Covers:** Lectures 00–03

---

## Before You Start

**Build with the development line, every time:**

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Submissions that do not compile cleanly under `-Wall -Wextra` lose marks on the affected part.**
Submissions that do not compile at all score zero on that part — so submit something that builds early,
then improve it.

**Deliverables:** one `.cpp` file per part where code is asked for (`a4.cpp`, `b.cpp`, `c2.cpp`, …),
plus a single `ANSWERS.md` containing every written answer, table and transcript. **Name your
collaborators and state any generative-tool use** at the top of `ANSWERS.md`.

---

## Part A — Reading the Machine (20 pts)

The point of this part is that you can always go and look. Every claim in Lecture 01 is checkable with
tools you already have.

**A1.** *(4)* Compile this file with `g++ -std=c++17 -O1 -S -masm=intel`:

```cpp
struct Counter {
    int value;
    void add(int n);
};
void Counter::add(int n) { value += n; }
void add_free(Counter* c, int n) { c->value += n; }
```

Paste **both** function bodies from the `.s` file into `ANSWERS.md`. State whether they are identical,
and name the register that carries `this`.

**A2.** *(4)* Build a table of `sizeof` for four types: a struct with `int x; double y;` and no member
functions; the same struct with five member functions added; an empty struct; and an empty struct with
two member functions.

Report the four numbers. **Explain the empty-struct result in one sentence** — why is it not 0?

**A3.** *(4)* Demangle these by hand, showing your working, then check with `c++filt`:

```
_ZN6Matrix9transposeEv
_ZNK6Matrix3getEii
```

For the second, **say what the `K` encodes** and why that means it is a genuinely different symbol
from the version without it.

**A4.** *(4)* Move `add`'s definition *inside* the `Counter` struct body and recompile to assembly.
The symbol `_ZN7Counter3addEi` disappears. **Explain why in two sentences**, using the words *inline*
and *unused*.

Then make it reappear without moving the definition back out. *(There is more than one way.)*

**A5.** *(4)* Write a two-line file defining one ordinary C++ function and one `extern "C"` function.
Show the `nm` output. **State the one thing you give up inside `extern "C"`, and why that follows from
what mangling is for.**

---

## Part B — A Class That Owns Memory (28 pts)

Build a `CharBuffer` that owns a heap allocation. This is the class Week 1 will break and then fix, so
keep it.

**B1.** *(8)* Implement `CharBuffer` with:

- a constructor taking an `int` capacity, allocating that many `char`s and zeroing them;
- a destructor releasing the allocation;
- data members `int size;` and `char* data;`.

Use `new[]`/`delete[]` — not `malloc`. Write the initializer list **in declaration order**.

**B2.** *(6)* Add these four member functions, marking `const` exactly those that should be:

```
int  capacity()          // the allocated size
char at(int i)           // the character at i
void set(int i, char c)  // write c at i
const char* c_str()      // the buffer as a C string
```

**In `ANSWERS.md`, justify each `const` decision in one line.** Two of the four are not `const`, or
should not be — say which and why.

**B3.** *(6)* Make the constructor `explicit`. Then write the one line of code that **compiles without
it and fails with it**, and paste the error.

**Explain in two sentences what bug `explicit` prevents here.** A general statement about implicit
conversion is worth 3; a statement about what would go wrong *in this class specifically* is worth 6.

**B4.** *(8)* Write a `main` that constructs a `CharBuffer`, writes `"hi"` into it, prints the capacity
and contents, and also constructs a `const CharBuffer` and calls every member function that is legal
on it.

**It must run clean under `-fsanitize=address,undefined`.** Paste the transcript, including the
sanitizer's silence.

---

## Part C — Initialization (20 pts)

**C1.** *(6)* Write one class two ways: once initializing its members in the initializer list, once
assigning them in the constructor body. Both should compile.

Now add a `const int` member to both. **One of them stops compiling.** Paste the error and explain in
one sentence why the constructor body is too late.

**C2.** *(8)* Reproduce the declaration-order bug from Lecture 02 §4:

```cpp
struct Wrong {
    int* data;
    int  size;
    Wrong(int n) : size(n), data(new int[size]) {}
    ~Wrong() { delete[] data; }
};
```

Overload `operator new[]` so it prints the byte count it is asked for. Run `Wrong w(4);` and report
**how many integers were actually allocated on your machine.**

Then answer both:

- **(a)** *(2)* Which of `-Wreorder` and `-Wuninitialized` fires? Quote both messages.
- **(b)** *(3)* Swap the two member declarations, changing nothing else. **One warning still fires and
  the bug goes away.** Explain what that tells you about what `-Wreorder` actually means.

**C3.** *(6)* Write a class with a `const int` member and an `int&` member, both initialized from
constructor parameters. Demonstrate that writing through the reference member modifies the caller's
variable.

**Then explain in one sentence why a reference member cannot be assigned in the constructor body**,
referring to Lecture 00 §5.2.

---

## Part D — `const`-Correctness (16 pts)

**D1.** *(6)* Take your `CharBuffer` from Part B. Write a free function:

```cpp
void print_buffer(const CharBuffer& b);
```

that prints the capacity and contents. **If it does not compile, do not remove the `const` from the
parameter** — fix the class instead, and say in `ANSWERS.md` what you changed.

**D2.** *(6)* Deliberately remove `const` from `capacity()`. Recompile `print_buffer` and paste the
error.

**The error names `this`.** Quote the exact phrase, and explain in two sentences how it confirms
Lecture 01's claim about the hidden first parameter.

**D3.** *(4)* Add a `mutable` member to `CharBuffer` that counts how many times `at()` has been
called. Show it incrementing on a `const CharBuffer`.

**In one sentence, state the distinction `mutable` relies on**, and give one example of a member for
which using `mutable` would be an abuse.

---

## Part E — The Cliff (16 pts)

**Do not fix anything in this part.** It sets up Week 1. Marks are for demonstrating and explaining the
failure, not for repairing it.

**E1.** *(8)* Add a `char* raw() const { return data; }` accessor to `CharBuffer` temporarily, then run:

```cpp
CharBuffer a(8);
std::strcpy(a.raw(), "hi");
CharBuffer b = a;            // you did not write a copy constructor
std::fprintf(stderr, "a.data = %p\n", (void*)a.raw());
std::fprintf(stderr, "b.data = %p\n", (void*)b.raw());
```

Report the two addresses and whether they are equal. Then let the program exit and paste the
sanitizer's report.

> **Print to `stderr`, not `stdout`.** When the sanitizer aborts, buffered `stdout` can be lost and
> your output disappears. This is worth knowing generally.

**E2.** *(8)* Answer all three:

- **(a)** *(3)* You never wrote a copy constructor. **Where did the one that ran come from, and what
  exactly did it copy?**
- **(b)** *(3)* Name the sanitizer error precisely, and explain why it happens at *exit* rather than at
  the point of copying.
- **(c)** *(2)* `CharBuffer` has a correct constructor and a correct destructor, and is still broken.
  **State the rule this suggests** about which functions come as a set. You are not expected to know
  its name yet.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 20 | The tools: assembly, `sizeof`, `nm`, `c++filt` |
| B | 28 | A correct owning class, `const`-marked and sanitizer-clean |
| C | 20 | Initializer lists and the declaration-order rule |
| D | 16 | `const`-correctness as a propagating discipline |
| E | 16 | Demonstrating the double-free, and explaining it |
| **Total** | **100** | |

**Where the marks actually are:** Parts A and E carry 36 points between them and neither asks you to
design anything. They ask you to *look at what the compiler did* and *say what you saw*. That is the
habit this course is built on, and it is the cheapest 36 points on this problem set.

---

## Submission Checklist

1. Every `.cpp` compiles under `-Wall -Wextra -pedantic` with **no warnings** except the ones C2
   deliberately provokes.
2. `ANSWERS.md` contains every transcript, table and written answer, in order.
3. Part B4 runs clean under `-fsanitize=address,undefined`.
4. Part E is **not** fixed.
5. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 0 · Problem Set 0 · © CSE Department*
