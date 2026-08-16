# PROG 102 · Lecture 01
## From C to C++: The Class as a Struct With Functions

**Week 0 · Wednesday · 50 minutes**
**Reading:** *C++ Primer* Ch. 1, §7.1–7.2 · **Reference:** Stroustrup Ch. 16.2
**Assumes:** **Lecture 00** — this lecture uses `::`, `std::`, `explicit`, references and
`new`/`delete` without explaining them.

**Date:** Wednesday 13 January 2027 · 10:00–10:50 · Week 0

---

## 1. What Actually Changed

You spent PROG 101 writing C. Here is a C program:

```c
/* account.c */
#include <stdio.h>

struct Account {
    long balance;
};

void account_init(struct Account* a, long opening) { a->balance = opening; }
void account_deposit(struct Account* a, long amount) { a->balance += amount; }
long account_balance(const struct Account* a) { return a->balance; }

int main(void) {
    struct Account a;
    account_init(&a, 100);
    account_deposit(&a, 50);
    printf("%ld\n", account_balance(&a));
    return 0;
}
```

Notice the shape of it. Every function that operates on an `Account` takes an `Account*` as its
**first parameter**, and every function's name begins with `account_` so it does not collide with the
`customer_` functions in the next file.

That shape is not an accident of this program. **It is the shape every C program of any size
converges on**, because it is the only way C lets you associate functions with a type. C++ takes that
convention and makes it a language feature:

```cpp
// account.cpp
#include <cstdio>

class Account {
    long balance;
public:
    Account(long opening) : balance(opening) {}
    void deposit(long amount)  { balance += amount; }
    long report() const        { return balance; }
};

int main() {
    Account a(100);
    a.deposit(50);
    std::printf("%ld\n", a.report());
    return 0;
}
```

Three things changed and only three:

1. The functions moved **inside** the struct.
2. The explicit `Account*` first parameter **disappeared from the source**.
3. The prefix `account_` disappeared, because the class name now provides it.

**The first parameter did not disappear from the program.** It disappeared from the *source*. This
lecture is about where it went.

---

## 2. The Claim, and the Proof

> **`obj.method(args)` compiles to `method(&obj, args)`.**
>
> The object's address is passed as an implicit first argument, named `this`.

You do not have to take this on trust, and you should not. Here are two functions that do the same
work, one a member and one free:

```cpp
// this_ptr.cpp
struct Counter {
    int value;
    void add(int n);        // declared here, defined below
};

void Counter::add(int n) { value += n; }              // member function

void add_free(Counter* c, int n) { c->value += n; }   // the C equivalent
```

Compile to assembly and look:

```
g++ -std=c++17 -O1 -S -masm=intel this_ptr.cpp -o this_ptr.s
```

**`Counter::add`:**

```asm
_ZN7Counter3addEi:
        endbr64
        add     DWORD PTR [rdi], esi
        ret
```

**`add_free`:**

```asm
_Z8add_freeP7Counteri:
        endbr64
        add     DWORD PTR [rdi], esi
        ret
```

**The bodies are byte-for-byte identical.** Not similar — identical.

On the x86-64 System V ABI, the first integer/pointer argument arrives in `rdi` and the second in
`esi`. Both functions do `add DWORD PTR [rdi], esi`: *add the second argument to the int at the
address in the first argument.*

For `add_free`, `rdi` holds the `Counter*` you passed. For `Counter::add`, **`rdi` holds `this`** —
which you never wrote, and which the compiler supplied.

> **This is the single most useful fact in the course.** A member function is an ordinary function
> with one extra parameter. Everything in Weeks 1–12 is built on it.

### 2.1 Try It Yourself, and the Trap You Will Hit

Run that compile now. If you write the class the natural way:

```cpp
struct Counter {
    int value;
    void add(int n) { value += n; }   // defined INSIDE the class body
};
```

…and then search the assembly for `Counter::add`, **you will find nothing at all.**

This is not a mistake in the instructions. A function defined inside a class body is **implicitly
`inline`**, and an inline function with no callers generates no symbol — there is nothing to emit.
Move the definition outside the class (as above) and the symbol appears.

Two lessons, both of which will cost someone an hour later in the semester if not learned now:

- **"My function vanished from the object file" usually means it was inline and unused**, not that
  the compiler is broken.
- **Where you write a definition changes how it is compiled**, not just where it is readable. We come
  back to this in Lecture 03.

---

## 3. What an Object Costs

If member functions were stored *in* objects, every method you added would make every object bigger.
They are not, and it does not. Compare:

```cpp
struct PlainC { int x; double y; };                 // a C struct
struct WithMethods {
    int x; double y;
    void set(int a) { x = a; }
    double get() const { return y; }
    void lots() const {} void more() const {} void evenMore() const {}
};
```

Measured with `sizeof`:

| Type | Members | Member functions | `sizeof` |
| --- | --- | --- | --- |
| `PlainC` | `int x; double y;` | 0 | **16** |
| `WithMethods` | `int x; double y;` | 5 | **16** |
| `Empty` | none | 0 | **1** |
| `EmptyWithMethods` | none | 2 | **1** |

**Adding five member functions cost zero bytes.** The functions live in the text segment, exactly like
C functions, and are shared by every object of the type. An object contains its *data members* and
nothing else.

> The 16 rather than 12 for `PlainC` is alignment padding, not a C++ effect — `double y` must sit on
> an 8-byte boundary, so the compiler inserts 4 bytes after `int x`. This is identical in C, and you
> met it in PROG 101.

### 3.1 Why Is an Empty Class 1 Byte and Not 0?

Because **two distinct objects must have distinct addresses.** If `sizeof(Empty)` were 0, an array of
them would have every element at the same address, and `&a[0] == &a[1]` would be true — which breaks
pointer arithmetic and object identity everywhere in the language.

So the standard requires a minimum of 1. The byte is padding; nothing is stored in it.

**This is the first cost-of-abstraction measurement of the course**, and it is a good one to start on,
because the answer is *zero* — with a footnote. That pattern recurs all semester.

---

## 4. Name Mangling: Why C++ Symbols Look Like That

You saw `_ZN7Counter3addEi` above. That is not noise; it is a grammar, and it exists because **C++ has
function overloading and C does not.**

In C, a function's name *is* its symbol. Two functions cannot share a name, because the linker would
not know which one a call refers to. In C++ this is legal:

```cpp
namespace app {
class Widget {
public:
    void draw();
    void draw(int layer);
    void draw(double x, double y) const;
};
}
```

Three functions, one name. The linker needs three distinct symbols, so the compiler **encodes the
namespace, class, and parameter types into the symbol name.** Compiling that file and running `nm`:

| Mangled symbol | Demangled |
| --- | --- |
| `_ZN3app6Widget4drawEv` | `app::Widget::draw()` |
| `_ZN3app6Widget4drawEi` | `app::Widget::draw(int)` |
| `_ZNK3app6Widget4drawEdd` | `app::Widget::draw(double, double) const` |

You can read these once you know the pieces:

| Piece | Meaning |
| --- | --- |
| `_Z` | "This is a mangled C++ name" |
| `N ... E` | A **n**ested name — namespace/class qualifiers, terminated by `E` |
| `3app` | An identifier: 3 characters long, `app` |
| `6Widget`, `4draw` | Same rule — length then text |
| `v`, `i`, `d`, `dd` | Parameter types: `void`, `int`, `double`, `(double,double)` |
| **`K`** after `_ZN` | The function is **`const`** |

Two details worth pausing on.

**First: `const` is part of the symbol.** `_ZNK...` differs from `_ZN...`. A `const` member function
is genuinely a *different function* at link time, not the same function with a note attached. We use
this in Lecture 03.

**Second: `this` is not in the parameter list.** Compare the two symbols from §2:

```
_ZN7Counter3addEi          Counter::add(int)         -> params: i
_Z8add_freeP7Counteri      add_free(Counter*, int)   -> params: P7Counter, i
```

The member function's mangled name records **only `int`**, even though we proved it takes two
arguments. The `this` parameter is implied by the `N7CounterE` nesting rather than listed. **Same
machine code, different symbol grammar.**

### 4.1 `extern "C"` — Turning Mangling Off

Mangling breaks linking against C libraries, whose symbols are unmangled. So C++ gives you an escape:

```cpp
extern "C" void plain_c_function(int) {}
```

That emits the symbol **`plain_c_function`**, exactly as C would. Verified with `nm`:

```
plain_c_function              <- extern "C", unmangled
_ZN3app6Widget4drawEi         <- ordinary C++
```

This is why every C header you have ever opened contains:

```c
#ifdef __cplusplus
extern "C" {
#endif
    /* ... declarations ... */
#ifdef __cplusplus
}
#endif
```

The header is announcing: *if a C++ compiler is reading this, do not mangle these names.* You have
been reading past that boilerplate for a year. Now you know what it does.

**The cost:** inside `extern "C"` you cannot overload, because there is no way to encode the
difference. One name, one function.

---

## 5. The Compilation Model Has Not Changed

Worth stating explicitly, because it is a source of confusion:

```
    .cpp ──preprocess──> .i ──compile──> .s ──assemble──> .o ──link──> executable
```

This is the same four-stage pipeline as C, with the same separate compilation, the same `#include`
textual inclusion, and the same linker. `g++` is a driver that runs the same stages `gcc` does.

What changed is **what the compiler emits**, not the shape of the process:

| Stage | New in C++ |
| --- | --- |
| Preprocess | Nothing. `#include` and `#define` behave identically. |
| Compile | Mangled names; implicit `this`; compiler-generated functions (Week 1); template instantiation (Week 2) |
| Assemble | Nothing |
| Link | Must match mangled names; may need to merge duplicate inline/template definitions |

**Every debugging technique you learned in PROG 101 still applies.** `-E` still shows you the
preprocessed source, `-S` still shows you the assembly, `nm` still lists symbols, and "undefined
reference" still means the linker could not find a definition — it is just harder to read, because
the name is mangled. Run it through `c++filt`, or use `nm -C`.

---

## 6. Header and Source, in C++ Terms

The split is the same as C's, with a new convention:

```cpp
// account.hpp  -- the interface
#pragma once

class Account {
    long balance;                       // private data
public:
    explicit Account(long opening);     // declarations only
    void deposit(long amount);
    long report() const;
};
```

```cpp
// account.cpp  -- the implementation
#include "account.hpp"

Account::Account(long opening) : balance(opening) {}
void Account::deposit(long amount) { balance += amount; }
long Account::report() const       { return balance; }
```

Three points of C++ syntax:

- **`Account::` is the scope-resolution operator.** Outside the class body, you must say which class a
  member belongs to. `void deposit(...)` alone would define an unrelated free function.
- **`#pragma once`** replaces the `#ifndef ACCOUNT_H` include-guard dance. It is not standard C++, but
  every compiler you will meet supports it. Include guards remain correct if you prefer them.
- **`const` goes at the end** of a member function, in both declaration and definition, and must
  match. Lecture 03 explains what it does.

> **Why declare in the header and define in the source?** The same reason as C: so that changing an
> implementation does not force every file that uses it to recompile. C++ complicates this in exactly
> one place — **templates**, whose definitions usually *must* be in the header. That is Week 2's
> problem, and it is a real one.

---

## 7. What This Buys You

The C and C++ versions of `Account` generate the same instructions. So what did you gain?

**1. The compiler enforces the association.** In C, nothing stops you calling
`account_deposit(&customer, 50)` if the types are loosely related, and nothing stops a colleague
writing a fourth `account_` function that forgets to maintain your invariant. In C++, `deposit` is
*part of* `Account`.

**2. You can make `balance` unreachable.** The C version's `balance` is public to the entire program.
The C++ version's is private, and code outside the class **will not compile** if it touches it. That
is Lecture 03.

**3. Cleanup becomes automatic.** The C version has no way to say "when an `Account` goes away, do
this." The C++ version does, and it is the single most important feature of the language. That is
Lecture 02.

**4. The name is scoped.** No more `account_` prefixes to avoid collisions.

**None of these are runtime features.** All four are compile-time. The generated code is the code you
would have written by hand — which is the promise C++ makes and mostly keeps, and which you will spend
this course learning to check rather than assume.

---

## 8. Summary

| Claim | How we established it |
| --- | --- |
| A member function takes the object as a hidden first argument | Identical assembly for `Counter::add` and `add_free`; both use `rdi` |
| That argument is called `this` | The ABI: first argument in `rdi`; Lecture 03 shows the compiler naming it in an error |
| Member functions cost 0 bytes per object | `sizeof(PlainC) == sizeof(WithMethods) == 16` |
| An empty class is 1 byte | Required so distinct objects have distinct addresses |
| Symbols encode namespace, class, params, and `const` | `nm` output; `_ZNK` vs `_ZN` |
| A function defined in a class body is implicitly `inline` | Its symbol is absent from the object file when unused |
| `extern "C"` disables mangling | `plain_c_function` appears unmangled |

---

## 9. Exercises

**1.** Compile the `Counter` example yourself with `-O1 -S -masm=intel`. Confirm you get identical
bodies. Now change `add` to take a `long` instead of an `int` and re-read both the assembly **and**
the mangled name. What changed in each?

**2.** Write a class with one `int` member and ten member functions. Predict `sizeof` before you
measure it.

**3.** Demangle these by hand, then check with `c++filt`:

```
_ZN6Matrix9transposeEv
_ZNK6Matrix3getEii
_Z5applyPFiiEi
```

*(The third is harder and involves a function pointer. Work out what `PFiiE` must mean.)*

**4.** Take the `account.c` program from §1 and deliberately break the link: declare
`account_deposit` in a header, call it from `main`, and never define it. Read the error. Now do the
same in the C++ version. **How does the error differ, and which is more informative?**

**5.** Why can a function inside `extern "C"` not be overloaded? Answer in one sentence, referring to
symbols.

---

## 10. Next

**Lecture 02** answers the question this lecture leaves open: the C version needs `account_init`
called before the struct is usable, and nothing enforces that. Constructors do — and destructors do
the same for cleanup, which is the feature that makes C++ worth learning.

---

*PROG 102 · Week 0 · Lecture 01 · © CSE Department*
