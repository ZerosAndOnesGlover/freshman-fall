# PROG 102 · Lecture 03
## Encapsulation, `const`, and Namespaces

**Week 0 · Friday · 50 minutes**
**Reading:** *C++ Primer* §7.2–7.3, §18.2 · **Reference:** Stroustrup §16.2.3, Ch. 14
**Assumes:** **Lecture 00** §12 (`static_cast`, `reinterpret_cast`), §15 (`static_assert`, `decltype`)

**Date:** Friday 15 January 2027 · 10:00–10:50 · Week 0  <!-- 4th lecture in a 3-day week; see Calendar Reconciliation -->

---

## 1. Access Control

Three labels control who may name a member:

```cpp
class Account {
private:
    long balance;              // only Account's own member functions
protected:
    long overdraft_limit;      // Account, and classes derived from it (Week 4)
public:
    void deposit(long n);      // anybody
};
```

| Label | Reachable from |
| --- | --- |
| `private` | Member functions and friends of this class |
| `protected` | The above, plus derived classes — meaningless until **Week 4** |
| `public` | Anywhere |

The labels apply to everything after them until the next label, and you may repeat them freely.

### 1.1 What `private` Actually Prevents

Exactly one thing: **naming the member in code the compiler is checking.**

```cpp
class Account { long balance; public: Account(long b):balance(b){} };
int main() { Account a(10); return static_cast<int>(a.balance); }
```

```
error: 'long int Account::balance' is private within this context
note:  declared private here
```

That is the whole mechanism. It is a **compile-time name-lookup rule**, and it is worth being precise
about, because students routinely believe it is more than that.

### 1.2 It Is Not a Runtime Barrier

The object's bytes are ordinary bytes at an ordinary address. Nothing at runtime protects them:

```cpp
class Account {
    long balance;                       // private
public:
    Account(long b) : balance(b) {}
    long reported() const { return balance; }
};

Account a(4200);
long stolen;
std::memcpy(&stolen, reinterpret_cast<const char*>(&a), sizeof(long));
```

Measured output:

```
a.reported()          = 4200
raw bytes at &a       = 4200   <-- read without asking
```

**The private member was read without the compiler objecting**, because no member was *named* — bytes
were copied from an address. The access check never had anything to check.

> **Do not conclude that this is a technique.** It is undefined behaviour dressed up as a trick, it
> depends on layout the standard does not promise, and it will break. The point is what it tells you
> about the *nature* of `private`:
>
> **Encapsulation is a tool for managing complexity between programmers, not a security boundary
> against an adversary.** If you need the latter, you need a process boundary, and that is an
> operating-systems question rather than a language one.

This matters practically. `private` stops your colleague from *accidentally* depending on
`balance`, which is exactly what you want, because it means you can change `balance` later without
breaking their code. It does not stop a determined program, and it was never trying to.

---

## 2. `class` vs `struct`: Exactly One Difference

```cpp
class  C { int hidden; public: int shown; };     // members are private by default
struct S { int shown; private: int hidden; };    // members are public  by default
```

**That is the complete list of differences.** `sizeof(C) == sizeof(S) == 8`. Both can have
constructors, destructors, member functions, access labels, and can be inherited from. The only other
difference is the default inheritance access, which is the same rule applied in Week 4's context.

The convention most codebases follow, and which this course follows:

- **`struct`** for aggregates of public data with no invariant to maintain — a `Point`, a `Colour`, a
  parameter bundle.
- **`class`** when there is an invariant — anything where some combinations of member values are
  wrong and the class exists to prevent them.

`Account` is a `class` because `balance` has a meaning that arbitrary writes could violate. `Point`
is a `struct` because any pair of doubles is a valid point.

---

## 3. `const` Member Functions

A `const` after the parameter list promises the function does not modify the object:

```cpp
class Timer {
    int ticks = 0;
public:
    int  read() const { return ticks; }   // promises not to modify
    void bump()       { ++ticks; }        // may modify
};
```

### 3.1 What It Actually Does

Recall Lecture 01: every member function takes a hidden `this`. **`const` changes the type of
`this`.** Verified by `static_assert`:

```cpp
struct T {
    int v;
    void plain()       { static_assert(std::is_same_v<decltype(this), T*>,       "plain"); }
    void konst() const { static_assert(std::is_same_v<decltype(this), const T*>, "const"); }
};
```

Both assertions hold. So:

| Member function | Type of `this` | The C equivalent |
| --- | --- | --- |
| `void plain()` | `T*` | `void plain(T* this)` |
| `void konst() const` | `const T*` | `void konst(const T* this)` |

**`const` on a member function is `const` on a pointer parameter**, and you already know exactly what
that means from PROG 101. There is nothing new here except the syntax putting it at the end.

This is also why the mangled name changes — `_ZNK...` versus `_ZN...` in Lecture 01 §4. A different
parameter type is a different function.

### 3.2 The Two Errors, and What They Reveal

**Modifying a member inside a `const` member function:**

```cpp
void bump() const { ticks++; }
```

```
error: increment of member 'Timer::ticks' in read-only object
```

Through a `const T*`, every member is `const`. "Read-only object" is the compiler describing exactly
that.

**Calling a non-`const` member on a `const` object:**

```cpp
struct Timer { int ticks = 0; int read() { return ticks; } };   // read() is NOT const
const Timer t;
t.read();
```

```
error: passing 'const Timer' as 'this' argument discards qualifiers [-fpermissive]
note:   in call to 'int Timer::read()'
```

**Read that error again.** The compiler says `this` argument — out loud, in a message you will see
dozens of times this semester. It is telling you it tried to pass a `const Timer*` into a parameter
declared `Timer*`, which would throw away the `const`.

If Lecture 01's claim about the hidden first parameter ever felt like a metaphor, this is the compiler
confirming it is not.

### 3.3 `const`-Correctness Is a Discipline, Not a Decoration

**Mark every member function `const` that does not modify the object.** The reason is that `const`
propagates, and one missing `const` blocks a whole call chain:

```cpp
void print_report(const Account& a) {
    std::cout << a.report();      // requires report() to be const
}
```

If `report()` is not `const`, this function will not compile, and the usual reaction is to delete the
`const` from the parameter — which then breaks *its* callers, and so on outward. **Retrofitting
`const` into a codebase that did not start with it is genuinely painful**, which is why the habit is
worth building in Week 0 rather than Week 6.

The STL assumes it throughout. In Week 3 you will find that algorithms taking `const` containers
simply do not accept types whose accessors forgot the keyword.

### 3.4 `mutable`: The Documented Exception

Occasionally a member is not part of the object's *logical* value — a cache, a hit counter, a mutex
(Week 10). `mutable` exempts it:

```cpp
class Cache {
    int value;
    mutable int reads = 0;                       // mutable
public:
    explicit Cache(int v) : value(v) {}
    int get()  const { ++reads; return value; }  // legal: reads is mutable
    int hits() const { return reads; }
};

const Cache c(42);
c.get(); c.get(); c.get();
```

```
value reads: 3 (object was const the whole time)
```

The distinction being drawn is between **bitwise `const`** (no byte changes) and **logical `const`**
(the observable value does not change). `mutable` says: this member is not part of the value.

**Use it sparingly and only for that.** `mutable` on a member that *is* part of the object's value
turns `const` into a comment.

---

## 4. `inline` Is About Linking, Not Speed

The name is a historical accident and it misleads nearly everyone.

### 4.1 The Problem It Solves

Put a function *definition* in a header, include it from two `.cpp` files, and link:

```cpp
// util.hpp
#pragma once
int square(int x) { return x * x; }     // definition in a header
```

```
/usr/bin/ld: b.o: in function `square(int)':
b.cpp:(.text+0x0): multiple definition of `square(int)';
                   a.o:a.cpp:(.text+0x0): first defined here
collect2: error: ld returned 1 exit status
```

Each translation unit compiled its own copy, and the linker found two definitions of one symbol. This
is the **One Definition Rule**, and you met the C version of it in PROG 101.

Add `inline`:

```cpp
inline int square(int x) { return x * x; }
```

```
LINKED OK
```

### 4.2 What Changed

The symbol's binding:

| Header says | `nm` output |
| --- | --- |
| `int square(int x)` | `0000000000000000 T _Z6squarei` |
| `inline int square(int x)` | `0000000000000000 W _Z6squarei` |

**`T` is a strong global symbol; `W` is weak.** The linker rejects duplicate strong symbols and
silently merges duplicate weak ones, keeping one.

**That is what `inline` means: "this symbol may be defined in more than one translation unit; merge
them."** It is a linkage rule.

### 4.3 It Does Not Mean "Please Inline This"

The optimizer decides that independently, and does not need the keyword:

```cpp
static int plain(int x) { return x * 3; }   // no 'inline' keyword anywhere
int caller(int x) { return plain(x); }
```

At `-O2`:

```asm
_Z6calleri:
        endbr64
        lea     eax, [rdi+rdi*2]     ; x*3, computed in place
        ret
```

**No `call` instruction.** The function was inlined without being marked `inline`. Conversely, marking
a large function `inline` will not make the optimizer expand it if it judges that unprofitable.

> **The keyword is advice the compiler is free to ignore, and a linkage rule it is not.** Use it for
> the linkage, and let `-O2` handle the optimization — it has better information than you do about
> register pressure and code size.

### 4.4 Which Brings Back Lecture 01

A function defined inside a class body is **implicitly `inline`**:

```cpp
struct Counter {
    int value;
    void add(int n) { value += n; }    // implicitly inline
};
```

This is *necessary*: class definitions live in headers and get included many times, so without the
implicit `inline` every non-trivial class would break the One Definition Rule.

And it explains the disappearing symbol from Lecture 01 §2.1 — the function was weak *and* unused, so
nothing was emitted at all.

---

## 5. Namespaces

C's answer to name collisions is prefixes: `account_deposit`, `customer_deposit`. C++ scopes the names
instead:

```cpp
namespace physics { double energy(double m) { return m * 8.98755e16; } }
namespace finance { double energy(double m) { return m * 0.5; } }

physics::energy(1.0);   // 8.98755e+16
finance::energy(1.0);   // 0.50000
```

Two functions, identical signatures, no conflict. The namespace is part of the mangled symbol:

```
_ZN7physics6energyEd     ->  physics::energy(double)
_ZN7finance6energyEd     ->  finance::energy(double)
```

**The prefix did not go away; the compiler now writes it for you** — which is the same trade Lecture 01
described for `this`.

### 5.1 Three Ways to Shorten a Name

```cpp
std::cout << std::setw(4) << x;        // 1. fully qualified -- always fine

using std::cout;                       // 2. using-declaration: one name
cout << x;

using namespace std;                   // 3. using-directive: everything
cout << x;
```

**Prefer 1 in headers, 1 or 2 in source files.**

`using namespace std;` at the top of a **header** is a genuine defect: every file that includes it
inherits the entire standard library into its global scope, and cannot opt out. The collisions this
produces are remote from their cause and unpleasant to diagnose — a `count` or `distance` or `data` in
your own code suddenly becoming ambiguous because a header three levels down did this.

In a **`.cpp` file**, after the includes, it is a defensible convenience. This course writes `std::`
explicitly in all materials, because in teaching code it matters that you can see which names come
from the library.

### 5.2 Nested and Anonymous Namespaces

```cpp
namespace app { namespace detail { void helper(); } }   // C++03 style
namespace app::detail { void helper(); }                // C++17 -- use this
```

The **anonymous namespace** gives a name internal linkage — visible within its translation unit and
invisible to the linker:

```cpp
namespace { int scratch_counter = 0; }    // this file only
```

This is C++'s replacement for file-scope `static` in C, and it works for types as well as functions
and variables, which `static` never did.

---

## 6. Putting the Week Together

```cpp
// account.hpp
#pragma once
#include <stdexcept>

namespace bank {

class Account {
    long balance;                  // private: an invariant to protect
public:
    explicit Account(long opening) : balance(opening) {}   // explicit; init list

    void deposit(long amount) {                            // implicitly inline
        if (amount < 0) throw std::invalid_argument("negative deposit");
        balance += amount;
    }

    long report() const { return balance; }                // const: does not modify
};

}  // namespace bank
```

Every choice here comes from this week:

| Choice | Lecture |
| --- | --- |
| `namespace bank` | L03 §5 — scoping instead of an `account_` prefix |
| `class`, `balance` private | L03 §1–2 — there is an invariant |
| `explicit` | L02 §2.2 — no silent `long` → `Account` |
| `: balance(opening)` | L02 §3 — initializer list |
| `report() const` | L03 §3 — does not modify, so callable on a `const Account&` |
| Defined in the header | L03 §4 — implicitly `inline`, so it links |
| No destructor | L02 §5 — nothing is owned, so nothing needs releasing |

**That last row is the one to remember.** `Account` needs no destructor because it holds no resource.
The moment it holds a pointer, it needs a destructor — and then, as Lecture 02 §6 showed, it needs a
copy constructor and a copy assignment operator too, or copying it will double-free.

That is the Rule of Three, and it is Week 1.

---

## 7. Summary

| Idea | The point |
| --- | --- |
| `private` | A compile-time name-lookup rule, nothing more |
| Not a security boundary | Bytes were read via `memcpy` with no complaint |
| `class` vs `struct` | Default access. That is the entire difference |
| `const` member function | Makes `this` a `const T*` — verified by `static_assert` |
| "discards qualifiers" | The compiler naming `this` in an error message |
| `const`-correctness | Propagates outward; retrofitting is painful |
| `mutable` | Logical `const` vs bitwise `const`. Use sparingly |
| `inline` | A **linkage** rule: weak symbol, `T` → `W` |
| Optimizer inlining | Happens without the keyword; verified at `-O2` |
| Namespaces | The `account_` prefix, written by the compiler |

---

## 8. Exercises

**1.** Add a `private` member to a class, then read it from `main` two ways: by naming it, and by
`memcpy` from the object's address. Which does the compiler reject? **In one sentence, say what that
tells you about what `private` is for.**

**2.** Write a class where `sizeof` is the same whether you use `class` or `struct`, and where
changing the keyword alone changes whether the program compiles.

**3.** Take a class with five member functions and mark `const` every one that should be. Now write a
function taking `const YourClass&` that calls all five. **Which ones fail, and is the fix to remove
the `const` from the parameter?**

**4.** Reproduce the multiple-definition link error from §4.1, then fix it with `inline`. Confirm the
symbol changed from `T` to `W` using `nm`.

**5.** Compile a small function at `-O2` without the `inline` keyword and confirm from the assembly
that it was inlined anyway. Then explain in two sentences why the keyword still exists.

**6.** Two libraries both define `Logger` in the global namespace and you must use both. Fix it
without editing either library. *(There is more than one answer.)*

**7.** Why is `using namespace std;` acceptable in a `.cpp` file and a defect in a `.hpp` file? Answer
in terms of who is affected and whether they can opt out.

---

## 9. Next

Week 0 built a class that owns nothing. **Week 1** builds one that owns memory, and discovers that the
copy constructor the compiler wrote for you copies the *pointer* rather than the data — so two objects
free the same allocation and the program dies at a `delete` that looks correct.

The fix is the **Rule of Three**, and the elegant form of it is the **copy-swap idiom**. Bring
Lecture 02's destruction-order material with you; it is what makes copy-swap work.

---

*PROG 102 · Week 0 · Lecture 03 · © CSE Department*
