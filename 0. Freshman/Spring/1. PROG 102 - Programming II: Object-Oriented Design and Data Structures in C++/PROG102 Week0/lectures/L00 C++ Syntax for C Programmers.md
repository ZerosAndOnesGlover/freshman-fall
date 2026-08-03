# PROG 102 · Lecture 00
## C++ Syntax for C Programmers

**Week 0 · Orientation session · 50 minutes**
**Reading:** *C++ Primer* Ch. 1, §2.3, §2.5, §6.2 · **Reference:** [cppreference.com](https://en.cppreference.com)

---

## 0. What This Lecture Is

**This is a syntax primer, not a concepts lecture.** Lectures 01–03 are the three timetabled lectures
of Week 0 and they teach what classes *mean*. This one teaches the notation they are written in.

C++ is very nearly a superset of C, so most of your PROG 101 syntax carries over untouched: `if`,
`while`, `for`, `switch`, arrays, pointers, `struct`, `sizeof`, the preprocessor, and the whole
operator set all behave as you expect. **This lecture covers only the constructs that are new**, and
which Lectures 01–03 use without stopping to explain.

**How to use it:** skim it now, write the exercises, then keep it open as a reference for the first
fortnight. Nothing here is deep. All of it is assumed from Lecture 01 onward.

> **One genuinely new idea.** Everything in this lecture is notation you can look up — except
> **references** (§5), which are a new kind of thing with no C equivalent. If you are short of time,
> read §5 properly and skim the rest.

---

## 1. Headers and the `std::` Prefix

C++ has its own spelling of the C standard headers:

```cpp
#include <cstdio>      // C++ spelling of <stdio.h>
#include <cstdlib>     // <stdlib.h>
#include <cstring>     // <string.h>
#include <cmath>       // <math.h>
```

The difference: the `c`-prefixed versions put their names in the **`std` namespace**.

```cpp
#include <cstdio>
std::printf("hello\n");     // qualified
```

The old spellings still work, and `<cstdio>` in practice also puts the names in the global namespace,
so plain `printf` usually compiles too. **This course writes `std::` explicitly**, because in teaching
code it should be visible which names come from the library.

C++ also has headers with no C equivalent, which have no `.h` and no `c` prefix:

```cpp
#include <iostream>    // streams
#include <string>      // std::string
#include <vector>      // std::vector
```

---

## 2. `::` — The Scope Resolution Operator

`::` means "look this name up inside that scope". Three uses, all of which appear in Lecture 01:

```cpp
std::printf(...);          // printf inside namespace std
Account::deposit(...);     // deposit inside class Account
::global_thing;            // the global scope explicitly
```

It is not the same as `.` or `->`. **`.` and `->` reach into an object; `::` reaches into a scope** —
a namespace or a class. `std` is not an object and you cannot write `std.printf`.

---

## 3. Output: Streams

C's `printf` works and this course uses it where format control matters. But C++'s own idiom is the
stream:

```cpp
#include <iostream>

int x = 42;
std::cout << "x is " << x << "\n";
```

`<<` is an operator applied to `std::cout`, chained left to right. It is **type-aware** — you do not
write `%d` or `%s`, and you cannot get the specifier wrong. Week 1 shows you how to make it work with
your own types, which is the actual reason it is designed this way.

| Stream | Purpose |
| --- | --- |
| `std::cout` | Standard output |
| `std::cerr` | Standard error, unbuffered |
| `std::cin` | Standard input, used with `>>` |

### `std::endl` versus `"\n"`

```cpp
std::cout << "line\n";          // newline
std::cout << "line" << std::endl;   // newline AND flush the buffer
```

**`std::endl` flushes; `"\n"` does not.** Flushing in a loop is a real performance cost. **Prefer
`"\n"`** and use `std::endl` only when you genuinely need the output to appear immediately — for
example, just before a crash you are trying to locate.

---

## 4. `bool` and `nullptr`

```cpp
bool flag = true;       // a real built-in type
int* p = nullptr;       // the null pointer literal
```

Measured: `sizeof(bool) == 1`, `true` converts to `1`, `false` to `0`.

C's `NULL` is a macro for `0`, which creates a genuine ambiguity when a function is overloaded on
`int` and `T*` (§6). **`nullptr` has pointer type and cannot be mistaken for an integer.** Use it
everywhere; there is no reason to write `NULL` in C++.

---

## 5. References — The One Genuinely New Thing

A reference is an **alias**: another name for an existing object.

```cpp
int x = 5;
int& r = x;     // r is not a copy of x, and not a pointer to x. r IS x.
r = 7;          // x is now 7
```

Verified: after that code, `x == 7` and **`&x == &r`** — the same address. There is one object with
two names.

### 5.1 Why It Exists

Compare three ways to let a function modify its caller's variable:

```cpp
void by_value(int x)     { x = 99; }   // modifies a copy
void by_pointer(int* p)  { *p = 99; }  // modifies the caller's variable
void by_reference(int& r){ r = 99; }   // modifies the caller's variable
```

```cpp
int a = 1, b = 1, c = 1;
by_value(a); by_pointer(&b); by_reference(c);
```

Measured result: **`a` is 1, `b` is 99, `c` is 99.**

`by_pointer` and `by_reference` do the same job. The reference version needs no `&` at the call site
and no `*` in the body, so it cannot be passed null and cannot be arithmetic'd off the end.

### 5.2 References Versus Pointers

| | Pointer | Reference |
| --- | --- | --- |
| Can be null | Yes | **No** |
| Can be reseated | Yes | **No** — bound once, at birth |
| Must be initialized | No | **Yes** |
| Syntax to use | `*p`, `p->m` | `r`, `r.m` |
| Own address | Yes, `&p` differs from `p` | `&r == &referent` |

The two "no"s are the point. A reference is a promise that there is a real object there. This is why
Lecture 02's `const int&` and `int&` members must be set in the initializer list — there is no such
thing as an unbound reference to fix up later.

### 5.3 `const` References: The Workhorse

```cpp
void print(const std::string& s);   // no copy, and cannot modify
```

This is the **default way to pass anything bigger than a pointer** in C++. It avoids copying a
potentially large object, and the `const` documents and enforces that the function only reads it.

You will see `const T&` in every week of this course. When in doubt about how to take a parameter,
this is the answer.

---

## 6. Function Overloading

C++ allows several functions with the same name, distinguished by parameter types:

```cpp
int    area(int s)    { return s * s; }
double area(double r) { return 3.14159 * r * r; }
```

```
area(3)   -> 9
area(3.0) -> 28.27431
```

The compiler picks by argument types. This is why symbols are mangled (Lecture 01 §4) — the linker
needs a distinct name for each.

**Return type alone is not enough.** Two functions differing only in return type do not compile, since
a call like `f(1);` would be ambiguous.

---

## 7. Default Arguments

```cpp
int scaled(int x, int factor = 10) { return x * factor; }

scaled(5)      // 50
scaled(5, 2)   // 10
```

Defaults must be the trailing parameters, and are written on the **declaration** (the header), not
repeated on the definition.

---

## 8. `new` and `delete`

C++'s allocation operators, replacing `malloc`/`free`:

```cpp
S*  a   = new S;          // allocate AND construct
delete a;                 // destruct AND deallocate

S*  arr = new S[2];       // allocate and construct 2
delete[] arr;             // destruct all 2, then deallocate
```

**The difference from `malloc` is that constructors and destructors run.** Demonstrated with a struct
whose constructor sets `v = 7` and prints:

```
new / delete:
    S() ran
    a->v = 7
    ~S() ran
malloc / free (no constructor, no destructor):
    b->v = -853058783  <- never initialised
new[] / delete[]:
    S() ran
    S() ran
    ~S() ran
    ~S() ran
```

The `malloc` version produced garbage because **`malloc` allocates bytes; it does not make an
object.**

Two rules, both absolute:

- **`new` pairs with `delete`; `new[]` pairs with `delete[]`.** Mixing them is undefined behaviour.
- **Never `free` something from `new`, and never `delete` something from `malloc`.**

> By Week 5 you will barely write `new` at all — `unique_ptr` will write it for you. Until then, every
> `new` you write is a `delete` you owe.

---

## 9. `auto`

`auto` asks the compiler to deduce the type from the initializer:

```cpp
auto i = 42;                    // int
auto d = 4.2;                   // double
auto s = std::string("hi");     // std::string
```

It is not dynamic typing — the type is fixed at compile time, and `i` is exactly as much an `int` as
if you had written it. It saves you from spelling out types that are long and mechanical, which in
Week 3 becomes essential:

```cpp
std::vector<int>::const_iterator it = v.begin();   // the long way
auto it = v.begin();                               // the same type
```

**Use `auto` when the type is obvious from the right-hand side or too long to be useful. Write the
type out when it is the informative part of the line.**

---

## 10. Range-Based `for`

```cpp
std::vector<int> v{4, 5, 6};
for (int e : v) std::printf("%d ", e);        // 4 5 6
```

To modify the elements, take a reference (§5) — otherwise you are assigning to a copy:

```cpp
for (int& e : v) e *= 2;                      // v is now 8 10 12
```

The three forms you will use constantly:

| Form | Meaning |
| --- | --- |
| `for (T e : c)` | A copy of each element |
| `for (T& e : c)` | The element itself; may modify |
| `for (const T& e : c)` | The element itself, read-only. **The default choice.** |

---

## 11. Brace Initialization

C++11 added `{}` initialization, usable almost everywhere:

```cpp
int   x{5};
P     p{3, 4};
std::vector<int> v{1, 2, 3};
```

Its advantage over `=` is that it **objects to narrowing conversions**:

```cpp
double d = 3.9;
int a = d;      // no diagnostic at all -- silently truncates to 3
int b{d};       // warning: narrowing conversion of 'd' from 'double' to 'int'
```

Only the brace form is flagged. Under this course's build line (`-pedantic`) that is a **warning**;
with `-pedantic-errors` it becomes an error. Both were verified.

> **A caution for Week 3.** Braces interact awkwardly with `std::vector`: `std::vector<int> v{5}` is
> a vector containing the single element 5, while `std::vector<int> v(5)` is a vector of five zeros.
> This is a real trap and Week 3 returns to it.

---

## 12. Casts

C's cast syntax `(T)x` still compiles, and you should stop using it. C++ has four named casts; two
matter in Week 0:

```cpp
static_cast<int>(some_double);      // checked, related-type conversions
reinterpret_cast<char*>(&obj);      // "treat these bytes as", unchecked
```

The gain is that **`static_cast` refuses conversions that are not meaningful**:

```cpp
struct A { int x; }; struct B { double y; };
A a{1};
B* p = (B*)&a;                  // C cast: compiles. Meaningless.
B* q = static_cast<B*>(&a);     // error: invalid 'static_cast' from 'A*' to 'B*'
```

The C cast silently did something dangerous. `static_cast` refused. The other two,
`const_cast` and `dynamic_cast`, arrive in Weeks 3 and 4.

**Named casts are also greppable**, which is the other real reason to prefer them: you can find every
questionable conversion in a codebase, and you cannot grep for `(B*)`.

---

## 13. Class Syntax at a Glance

Lectures 01–03 explain all of this. Here it is purely as notation, so the code reads:

```cpp
class Account {          // 'class' -- members private by default
    long balance;        // a data member

public:                  // everything after this is public
    Account(long b) : balance(b) {}   // constructor: class name, no return type
                                      // ': balance(b)' is the initializer list
    ~Account() {}                     // destructor: ~ClassName, no arguments

    void deposit(long n);             // member function, declared
    long report() const;              // 'const' = does not modify the object
};

void Account::deposit(long n) { balance += n; }   // defined out of class: Account::
```

Using it:

```cpp
Account  a(100);      // construct
a.deposit(50);        // call on an object
Account* p = &a;
p->deposit(50);       // call through a pointer -- same as (*p).deposit(50)
```

`.` and `->` work exactly as they did for C structs. **The only new thing is that the right-hand side
can now be a function.**

---

## 14. `= default` and `= delete`

Two ways to control the functions the compiler writes for you:

```cpp
struct P {
    int x, y;
    P() = default;                 // "generate the default constructor you would have generated"
    P(int a, int b) : x(a), y(b) {}
};

struct NoCopy {
    NoCopy() = default;
    NoCopy(const NoCopy&) = delete;   // copying this type is forbidden
};
```

`= delete` is enforced at compile time:

```
error: use of deleted function 'NoCopy::NoCopy(const NoCopy&)'
note:  declared here
```

Lecture 02 §2.1 explains when you need `= default`. Week 1 explains when you want `= delete`, and
Week 5 uses it heavily — `unique_ptr` is non-copyable precisely this way.

---

## 15. `static_assert` and `decltype`

Used in Lecture 03 to prove a claim about `this`, so they need a mention:

```cpp
static_assert(sizeof(P) == 2 * sizeof(int), "P should be two ints");
```

**`static_assert` is checked at compile time** and fails the build with your message. It is the right
tool for assumptions about types and sizes, because a runtime assert would be too late.

`decltype(expr)` yields the *type* of an expression without evaluating it:

```cpp
static_assert(std::is_same_v<decltype(p.x), int>, "x is int");
```

You will not write much `decltype` this semester. You need to recognise it in Lecture 03.

---

## 16. `#pragma once`

```cpp
#pragma once     // replaces the #ifndef / #define / #endif include guard
```

Not standard C++, but supported by every compiler you will meet, and used throughout this course.
Traditional include guards remain perfectly correct.

---

## 17. C to C++ Quick Reference

| C | C++ | Section |
| --- | --- | --- |
| `#include <stdio.h>` | `#include <cstdio>`, names in `std::` | §1 |
| `printf("%d", x)` | `std::cout << x` | §3 |
| `NULL` | `nullptr` | §4 |
| `int` used as a flag | `bool`, `true`, `false` | §4 |
| `void f(int* p)` for output params | `void f(int& r)` | §5 |
| `void f(const big_t* p)` | `void f(const big_t& r)` | §5.3 |
| `area_int`, `area_dbl` | `area` overloaded | §6 |
| `malloc` / `free` | `new` / `delete` | §8 |
| Spelling out the type | `auto` | §9 |
| `for (i = 0; i < n; ++i) a[i]` | `for (const auto& e : c)` | §10 |
| `(T)x` | `static_cast<T>(x)` | §12 |
| `struct S` + `s_init`, `s_free` | `class S` + constructor, destructor | §13 |
| `#ifndef GUARD_H` | `#pragma once` | §16 |

---

## 18. Not Yet

Deliberately absent, so you do not think you are missing something:

| Construct | Arrives in |
| --- | --- |
| `operator+`, `operator<<` overloading | **Week 1** |
| `template<typename T>` | **Week 2** |
| `std::vector`, `std::map`, iterators, algorithms | **Week 3** |
| `virtual`, `override`, abstract base classes | **Week 4** |
| `unique_ptr`, `shared_ptr`, `std::move`, `&&` | **Week 5** |
| `try` / `catch` / `throw`, `noexcept` | **Week 9** |
| `std::thread`, `std::mutex`, `std::atomic` | **Week 10** |
| Lambdas `[](){}`, `std::function`, `constexpr` | **Week 11** |

---

## 19. Exercises

**1.** Write a program that declares `int x = 5;` and `int& r = x;`, then prints `x`, `r`, `&x` and
`&r`. **Explain the output in one sentence.**

**2.** Write `swap_ptr(int*, int*)` and `swap_ref(int&, int&)` that both swap their arguments. Call
each. Which call site is easier to misuse, and how?

**3.** Take a C program you wrote for PROG 101 that uses `printf` and convert its output to
`std::cout`. Which lines got clearer, and which got worse?

**4.** Write two overloads of `describe` — one taking `int`, one taking `double`. Call it with `5`,
`5.0`, and `5.0f`. **Predict each result before compiling**, then explain any surprise.

**5.** Demonstrate that `int b{3.9};` warns and `int a = 3.9;` does not. Then compile with
`-pedantic-errors` and report what changes.

**6.** Allocate a struct with `malloc` and one with `new`, where the struct has a constructor that
prints. Show that only one of them constructs. **Then explain why `free` on the `new`'d object is
wrong even though both came from the heap.**

**7.** Write a function taking `const std::string&` and one taking `std::string` by value. Add a print
to a copy constructor to count copies. *(You will not be able to do this properly until Week 1 — try
it now, and come back in a week.)*

---

## 20. Next

**Lecture 01** starts the course proper, with the claim that a class is a struct whose functions take
the object as a hidden first argument — and proves it by reading the generated assembly.

Everything in this lecture is notation in service of that.

---

*PROG 102 · Week 0 · Lecture 00 · © CSE Department*
