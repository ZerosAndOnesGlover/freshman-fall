# PROG 102 · Midterm 1 · Revision Guide
## Weeks 0–4

**Sat Tuesday 2 March 2027, 18:00–19:30 (Week 6, VNC 100) · a 75-minute paper · 12.5% of the course grade**
**Closed book, closed device. One handwritten sheet of A4, one side only.**

---

## What Is Examinable

**Lectures 00–15, Problem Sets 0–4, and Labs 0–4.** Anything covered in a lecture, assessed on a
problem set, or measured in a lab.

Reading-guide material that was never lectured is **not** examinable, but the guiding questions are a
good source of revision prompts.

### The Shape of the Paper

| Section | Marks | What it asks |
| --- | --- | --- |
| **A — Short answer** | 30 | 10 questions, 3 marks each. Definitions, one-line explanations, "what does this print" |
| **B — Code reading** | 30 | Given code, say what it does, what is wrong with it, or what the compiler says |
| **C — Code writing** | 25 | Write a class or a small hierarchy correctly, by hand, on paper |
| **D — Explain a measurement** | 15 | A table of numbers from a lab; explain what it shows and what it does not |
| **Total** | **100** | |

**Section D is the one students underprepare.** It is 15 marks for explaining numbers you have already
produced, and it cannot be revised by memorising definitions.

---

## The Ten Things Most Likely to Appear

Ordered by how often they have been the difference between grades.

1. **The Rule of Three**, and the double-free it prevents. *(L05)*
2. **Why the copy-swap `operator=` needs no self-assignment guard**, and what exception guarantee it
   gives. *(L06)*
3. **What `obj.method(args)` compiles to**, and where `this` arrives. *(L01)*
4. **Member initialization order** — declaration order, not list order — and the bug it causes. *(L02)*
5. **Why a class template's definitions must be in the header.** *(L08)*
6. **Iterator categories**, and predicting whether an algorithm compiles for a container. *(L10)*
7. **The virtual destructor rule**, and what leaks without it. *(L15)*
8. **Object slicing**, explained in terms of the vptr. *(L15)*
9. **`const` member functions** and the type of `this`. *(L03)*
10. **What a virtual call costs**, and why the naive benchmark overstates it. *(L14)*

---

## Week-by-Week Checklist

### Week 0 — C to C++

- [ ] A member function takes the object as a hidden first argument; `this` arrives in `rdi` on x86-64
- [ ] Member functions cost **0 bytes** per object; an empty class is **1** byte, and why
- [ ] Reading a mangled name: namespace, class, parameters, and `K` for `const`
- [ ] `extern "C"` disables mangling, and you lose overloading
- [ ] Constructors, `explicit`, `= default`
- [ ] **Members are initialized in declaration order.** `-Wreorder` means "misleading"; `-Wuninitialized` means "wrong"
- [ ] Destruction is the reverse of construction; heap objects need `delete`
- [ ] `private` is a compile-time rule, not a runtime barrier
- [ ] `class` vs `struct`: exactly one difference
- [ ] `const` on a member function makes `this` a `const T*`
- [ ] **`inline` is a linkage rule** — weak symbol, `T` → `W` — not a speed hint

### Week 1 — Operators and Copying

- [ ] An operator is a function; the member's left operand is `this`
- [ ] Symmetric binary operators must be **free functions** — `3.0 * v` otherwise fails
- [ ] `operator<<` must be free; a member gives you `v << cout`
- [ ] `operator[]` comes in a `const`/non-`const` pair
- [ ] `operator<` must be a **strict weak ordering**; violating it is UB in `std::sort`
- [ ] **The Rule of Three**, and `= delete` as a way of satisfying it
- [ ] Shallow vs deep copy; the generated copy constructor is memberwise
- [ ] Self-assignment in the naive `operator=`: **the data is destroyed, and it is not a use-after-free**
- [ ] **Copy-swap**: by-value parameter, swap, return. No guard needed, strong guarantee
- [ ] `swap` must be `noexcept`, and why
- [ ] Guaranteed copy elision: `V3 c = a + b;` is **0** copies, and `-fno-elide-constructors` cannot change it in C++17
- [ ] Pass by value costs 2 copies per call; `const&` costs 0

### Week 2 — Templates

- [ ] A template is a recipe; `Stack` is not a type, `Stack<int>` is
- [ ] Deduction **matches**, it does not convert — `maxof(3, 7.5)` fails
- [ ] One template, one **weak** symbol per instantiation, type encoded in the name
- [ ] **Zero runtime cost** — instruction-identical to hand-written
- [ ] **Definitions in the header**, or explicit instantiation; otherwise no symbols and a link error
- [ ] `new T[n]` requires `T` to be default-constructible
- [ ] Full vs partial specialization; partial is **classes only**
- [ ] Non-type parameters: `FixedArray<int,8>` is `N * sizeof(int)`; `N` is in the type
- [ ] Cost is linear in instantiations — **and 100 hand-written classes cost exactly the same**
- [ ] Error length comes from **depth**, not from templates

### Week 3 — The STL

- [ ] An iterator is an interface: `*`, `++`, `==`, one-past-the-end
- [ ] Categories: input ⊂ forward ⊂ bidirectional ⊂ random access
- [ ] `vector`/`deque` random access; `list`/`set`/`map` bidirectional
- [ ] `std::sort` on a `list` fails on `operator-`; use `l.sort()`
- [ ] **The insertion paradox**: vector 178× faster with a search, list 128× faster without one
- [ ] `map` vs `unordered_map`: lookup ~6.5× faster unordered; ordering is what you pay for
- [ ] Member `find` beats `std::find` by ~6,000× on a set
- [ ] Iterator invalidation: `vector` `push_back` → use-after-free; `list` survives
- [ ] `std::sort` beats `qsort` ~2× — templates inline the comparison
- [ ] `accumulate`'s type comes from the **initial value**
- [ ] `std::remove` does not remove; the erase-remove idiom
- [ ] `vector<bool>` is a specialization that broke the contract

### Week 4 — Inheritance and Polymorphism

- [ ] is-a vs has-a; the Square/Rectangle counterexample
- [ ] `public` inheritance; `class` defaults to `private`
- [ ] Construct base-first, destroy derived-first
- [ ] **No virtual calls from constructors** — the vptr is not yet the derived one
- [ ] Name hiding: any `f` in derived hides **all** `f` in base; fix with `using`
- [ ] `override` turns a silent bug into a compile error
- [ ] vptr per object, vtable per class; first virtual costs **8 bytes**, tenth costs **0**
- [ ] Slot index is fixed by the base's declaration order
- [ ] Virtual dispatch ≈ **2 ns**, ratio ≈2× on a loop that does nothing else
- [ ] **Speculative devirtualization** — the model is not the machine
- [ ] Abstract classes; abstractness is inherited; a pure virtual may have a body
- [ ] **The virtual destructor rule**, and exactly when `-Wall` warns
- [ ] Slicing, and that making the base abstract turns it into a compile error
- [ ] `static_cast` down is unchecked; `dynamic_cast` is checked and costs ~2.8× a virtual call

---

## Section D: The Measurements You Should Be Able to Explain

You will be given a table and asked what it shows. **Do not memorise the numbers** — memorise what each
one demonstrates and what it does not.

| Measurement | What it shows | The trap |
| --- | --- | --- |
| `V3 c = a + b;` = 0 copies | C++17 guaranteed elision | It is **not** an optimization; the flag cannot disable it |
| 100 templates = 100 hand-written = 43,993 bytes | "Template bloat" is misattributed | The measurement was right; the *explanation* was wrong |
| vector 178× / list 128× | The insertion paradox | **Both** are correct; the table omits the search |
| `std::sort` 2× `qsort` | Templates inline; function pointers cannot | Not a better algorithm |
| virtual ≈ 2 ns, ratio ≈2× | Dispatch is cheap in absolute terms | The first two benchmarks measured something else |
| `-O2` 2.20× vs `-O3` 2.23× | Blocked vectorization is real | …and did **not** explain the gap here |

**A good Section D answer states what the number is evidence for, and names one thing it is not
evidence for.** That second half is where the marks are.

---

## How to Build the Sheet

One side of A4, handwritten. **Making it is most of the revision** — do not photograph someone else's.

What is worth the space:

- The **Rule of Three / copy-swap** skeleton, written out in full
- The **iterator category** table and which containers provide which
- The **special members the compiler generates**, and when it stops
- The declaration-order rule, and the two warnings
- `sizeof` facts: empty class 1, first virtual +8, `FixedArray<T,N>` = `N*sizeof(T)`
- The four casts, one line each

What is **not** worth the space:

- Anything you can derive in ten seconds
- Exact benchmark numbers — Section D gives you the table
- Syntax you have typed twenty times

---

## Practice Strategy

**Two weeks out (now):** work the exercises at the end of each lecture you skipped. They are the paper's
source material.

**One week out:** re-run **one** measurement from each of Labs 2, 3 and 4 without looking at your old
results. If you cannot reproduce it, you cannot explain it.

**Three days out:** write the sheet. Then do a timed 75 minutes on the lecture exercises for Weeks 0–2,
which is the half people forget.

**The night before:** stop. Re-read this checklist and sleep.

---

## Practicalities

- **75 minutes**, and the paper is written to be finishable in 65. If you are short of time you have
  been over-writing — Section A wants one or two sentences, not a paragraph.
- **Code in Section C is marked on correctness of the ideas**, not on whether you remembered a
  semicolon. Missing `#include`s cost nothing. A missing `virtual` on a destructor costs plenty.
- **Show working in Section D.** A number with no reasoning earns little; reasoning with an arithmetic
  slip earns most of the marks.
- Anything you need in order to sit the exam — extra time, a separate room — is arranged by emailing
  the instructor, **without giving a reason.** Do it this week, not the week of the paper.

---

*PROG 102 · Week 4 · Midterm 1 Revision Guide · © CSE Department*
