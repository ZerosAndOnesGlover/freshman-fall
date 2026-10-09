# PROG 102 · Lecture 02
## Constructors, Destructors, and Object Lifetime

*“In the long run every program becomes rococo - then rubble.”* — Alan Perlis, "Epigrams on Programming" (1982), #14

**Week 0 · Thursday · 50 minutes**
**Reading:** *C++ Primer* §7.1.4, §7.5 · **Reference:** Stroustrup Ch. 17
**Assumes:** **Lecture 00** §5 (references), §8 (`new`/`delete`), §14 (`= default`)

**Date:** Thursday 21 January 2027 · 10:00–10:50 · Week 0

**Coursework:** 📝 **PS 0** released Fri 22 Jan 11:00, due Fri 29 Jan 17:00 · 🔬 **Lab 0** Mon 25 Jan 15:00–16:50 · 📊 **Quiz 1** Tue 26 Jan 10:00–10:15

---

## 1. The Problem C Cannot Solve

Here is the C `Account` from Lecture 01, and here are two bugs it cannot prevent:

```c
struct Account a;
account_deposit(&a, 50);       /* bug 1: never initialised. a.balance is garbage. */
```

```c
struct Buffer* b = buffer_create(1024);
if (error) return -1;          /* bug 2: never destroyed. 1024 bytes leaked. */
buffer_destroy(b);
```

Both are the same shape of mistake: **C can express the rule but cannot enforce it.**
`account_init` exists, and the documentation says to call it, and nothing checks. `buffer_destroy`
exists, and every `return` between creation and destruction silently skips it.

You spent a semester developing the discipline to get these right by hand. That discipline is real and
you will keep using it. But it does not scale — a function with six early returns needs cleanup on all
six paths, and the seventh, added next year by someone else, will not have it.

**C++'s answer is to attach the rules to the type**, so that the compiler emits the calls rather than
trusting you to. Two mechanisms: constructors and destructors.

---

## 2. Constructors

A constructor is a member function with **the class's name and no return type**. It runs
automatically when an object comes into existence.

```cpp
class Account {
    long balance;
public:
    Account()                : balance(0)       {}   // default constructor
    explicit Account(long b) : balance(b)       {}   // one-argument constructor
};

Account a;        // calls Account()
Account b(500);   // calls Account(long)
```

**There is no way to obtain an `Account` without one of these running.** That is the entire point.
Bug 1 above is not merely discouraged; it has become inexpressible.

### 2.1 The Default Constructor Rule

If you declare **no** constructors at all, the compiler generates a default one for you. If you
declare **any** constructor, it does not.

```cpp
struct A { int x; };                            // compiler generates A()
struct B { int x; explicit B(int v):x(v){} };   // no B() exists
B b;                                            // error: no matching function
```

This trips people up because adding a constructor silently removes one. If you want both, say so:

```cpp
struct B {
    int x;
    B() = default;                 // "generate the one you would have generated"
    explicit B(int v) : x(v) {}
};
```

### 2.2 `explicit`, and Why It Is Not Decoration

A single-argument constructor doubles as an **implicit conversion** unless you forbid it:

```cpp
class Timeout { public: Timeout(int seconds); };   // no 'explicit'
void wait(Timeout t);

wait(30);          // compiles. 30 silently becomes a Timeout.
```

That may be what you want for a type like `Timeout`. It is emphatically not what you want here:

```cpp
class Buffer { public: Buffer(int capacity); };
void send(Buffer b);

send(4096);        // compiles, and allocates a 4096-byte buffer nobody asked for
```

**Write `explicit` on every single-argument constructor unless you have a specific reason to want the
conversion.** It costs one word and removes a class of bug that is genuinely hard to see in review.

---

## 3. The Member Initializer List

The part after the `:` and before the `{` is the **member initializer list**.

```cpp
Account(long b) : balance(b) {}
//                ^^^^^^^^^^ initializer list
```

It is not a stylistic alternative to assigning in the body. The two do different things:

```cpp
Account(long b) : balance(b) {}     // balance is CONSTRUCTED with the value b
Account(long b) { balance = b; }    // balance is default-constructed, THEN assigned
```

For an `int` the difference is invisible. For a member with an expensive constructor it is one
wasted construction. For two kinds of member it is **the difference between compiling and not**.

### 3.1 Two Members That Leave You No Choice

```cpp
struct S {
    const int c;      // const: can never be assigned
    int&      r;      // reference: must be bound at birth, can never be rebound
    S(int v, int& target) { c = v; r = target; }   // assignment in the body
};
```

The compiler rejects this outright:

```
error: uninitialized const member in 'const int'
note:  'const int S::c' should be initialized
error: uninitialized reference member in 'int&'
note:  'int& S::r' should be initialized
error: assignment of read-only member 'S::c'
```

Read the errors carefully — they say two separate things. By the time the constructor *body* runs,
every member has already been initialized somehow, and `c` and `r` cannot be. The body is too late.

The initializer list is the only place these can be set:

```cpp
struct S {
    const int c;
    int&      r;
    S(int v, int& target) : c(v), r(target) {}    // correct
};

int x = 7;
S s(3, x);
s.r = 99;          // writes through the reference: x is now 99
```

> **Rule: prefer the initializer list always.** It is required for `const` members, reference members
> and base classes (Week 4), it is never slower, and it is often faster. There is no case where the
> body is preferable and several where it is illegal.

---

## 4. The Trap: Initialization Order Is Declaration Order

Here is the rule that catches everybody, including people who have written C++ for years:

> **Members are initialized in the order they are *declared in the class*, not the order they appear
> in the initializer list.**

The list is not a sequence of instructions. It is a set of *values to use*, and the compiler applies
them in declaration order. Consider:

```cpp
struct Wrong {
    int* data;      // declared FIRST  -> initialized FIRST
    int  size;      // declared SECOND -> initialized SECOND

    Wrong(int n) : size(n), data(new int[size]) {}   // list says size first
    ~Wrong() { delete[] data; }
};
```

The list reads as though `size` is set before `data` uses it. It is not. `data` is declared first, so
`data(new int[size])` runs first, and it reads `size` **before `size` has been given a value**.

`-Wall -Wextra` catches this, and it is worth reading the exact wording:

```
warning: 'Wrong::size' will be initialized after [-Wreorder]
warning:   'int* Wrong::data' [-Wreorder]
warning:   when initialized here [-Wreorder]
warning: '*this.Wrong::size' is used uninitialized [-Wuninitialized]
```

### 4.1 What It Costs

This is not theoretical. Instrumenting `operator new[]` to report the size actually requested, and
running `Wrong w(4)` — asking for **four** integers:

| Build | Integers actually allocated |
| --- | --- |
| `-O0` | **99,539,950** |
| `-O2` | **1,600,677,166** |

At `-O0` the program allocated about **398 megabytes**; at `-O2`, about **6.4 gigabytes**.

The `-O0` number is not random. The test deliberately left the value `0x5EEDBEE` in the stack slot the
object would occupy, and `0x5EEDBEE` is exactly **99,539,950**. The constructor read the stale stack
bytes and passed them to `new[]`.

The assembly confirms the ordering directly:

```asm
_ZN5WrongC2Ei:
        endbr64
        push    rbp
        push    rbx
        mov     rbx, rdi
        movsx   rdi, DWORD PTR 8[rdi]     ; <-- LOAD size... before anything stored it
        ...
        call    _Znam@PLT                 ; <-- operator new[]
```

And the object afterwards looks **completely healthy** — `w.size` reports 4, because `size(n)` did
eventually run. A debugger inspecting the object tells you nothing is wrong. The damage was done and
finished during construction.

### 4.2 The Same Warning Does Not Always Mean a Bug

Now swap the two declarations **and** write the list the other way round. (Swapping the declarations
alone would make the list agree with them, and both warnings would simply disappear.)

```cpp
struct NotABug {
    int  size;      // declared FIRST
    int* data;      // declared SECOND
    NotABug(int n) : data(new int[size]), size(n) {}
    ~NotABug() { delete[] data; }
};
```

`-Wreorder` **still fires** — the list order still disagrees with the declaration order. But there is
no bug: `size` is declared first, so it is initialized first, and by the time `data` reads it the
value is there. The assembly shows the store happening before the load:

```asm
_ZN5WrongC2Ei:
        endbr64
        push    rbx
        mov     rbx, rdi
        mov     DWORD PTR [rdi], esi      ; <-- STORE size = n, first
        movsx   rdi, esi                  ; <-- then use it
        call    _Znam@PLT
```

**So `-Wreorder` tells you the list is misleading, not that it is wrong.** `-Wuninitialized` is the
one that fires only on the genuine bug — and it fired on `Wrong` and not on `NotABug`.

Two habits follow, and they are cheap:

1. **Write the initializer list in declaration order.** Then the two can never disagree and the
   warning can never fire. This is the whole fix.
2. **Do not initialize one member from another** unless you have checked the declaration order. Use
   the constructor parameter instead: `data(new int[n])` is correct regardless of how the members are
   declared, and is what both versions above should have said.

---

## 5. Destructors

A destructor is `~ClassName()`. It takes no arguments, returns nothing, and **there is exactly one
per class**. It runs automatically when the object's lifetime ends.

```cpp
class Buffer {
    int* data;
    int  size;
public:
    explicit Buffer(int n) : data(new int[n]), size(n) {}
    ~Buffer() { delete[] data; }        // runs automatically. Always.
};
```

Bug 2 from §1 is now inexpressible for stack objects:

```cpp
void process() {
    Buffer b(1024);
    if (error) return;      // ~Buffer() runs here
    if (other) return;      // and here
    ...
}                           // and here
```

**Every exit path calls the destructor**, including paths added years later by someone who never read
this function, and including exits caused by an exception being thrown (Week 9). You did not write the
cleanup on any of them.

This is **RAII** — *Resource Acquisition Is Initialization* — and it is the most important idea in
C++. Week 5 is devoted to it. Weeks 9 and 10 depend on it entirely.

### 5.1 Lifetime and Destruction Order

Objects are destroyed in **reverse order of construction**. Demonstrated:

```cpp
{
    Noisy first("first");
    Noisy second("second");
}
```

```
    ctor first
    ctor second
    -- end of scope --
    dtor second
    dtor first
```

Reverse order is not arbitrary. If `second` was built using something `first` owns, then destroying
`first` first would leave `second` holding a dangling reference during its own destructor. Reverse
order is the only order that is always safe, and it matches the stack discipline you already know from
PROG 101.

### 5.2 Heap Objects Are Different, and This Matters

The destructor runs automatically for objects with **automatic** (scope-bound) lifetime. An object
created with `new` has **dynamic** lifetime, and nothing runs its destructor until you say `delete`:

```cpp
{ Noisy a("stack"); }                          // ctor stack / dtor stack
Noisy* p = new Noisy("heap");                  // ctor heap        -- and that is all
Noisy* q = new Noisy("heap-deleted"); delete q; // ctor + dtor heap-deleted
```

Measured output:

```
stack object:
    ctor stack
    dtor stack
heap object, never deleted:
    ctor heap
heap object, deleted:
    ctor heap-deleted
    dtor heap-deleted
end of main
```

**`dtor heap` never appears.** Under `valgrind --leak-check=full` that program reports:

```
8 bytes in 1 blocks are definitely lost in loss record 1 of 1
   definitely lost: 8 bytes in 1 blocks
   still reachable: 0 bytes in 0 blocks
```

Eight bytes, because `Noisy` holds one `const char*`. Note that valgrind separates **definitely
lost** from **still reachable** — a distinction that matters more than it looks, and one we return to
in Week 5 when leak detection becomes the lab.

> **So `new` reintroduces exactly the problem destructors solved.** This is the central tension of
> Weeks 1–5, and its resolution is: *stop writing `new` in ordinary code.* Put the `new` inside a
> class whose destructor does the `delete` (Week 1), or use `unique_ptr`, which is that class already
> written for you (Week 5).

### 5.3 The Four Lifetimes

| Lifetime | Created | Destroyed | Example |
| --- | --- | --- | --- |
| **Automatic** | At its declaration | End of enclosing scope | `Buffer b(10);` inside a function |
| **Dynamic** | `new` | `delete`, and only then | `new Buffer(10)` |
| **Static** | Before `main`, or on first use | After `main` returns | A global, or `static` local |
| **Temporary** | Within an expression | End of the full expression | The result of `a + b` |

Automatic is the one to use. **Almost everything in this course is about arranging to use automatic
lifetime for things that look like they need dynamic lifetime.**

---

## 6. Putting It Together

```cpp
class Buffer {
    int  size;                              // declared first
    int* data;                              // declared second
public:
    explicit Buffer(int n)
        : size(n), data(new int[n]) {}      // list in declaration order; uses n, not size

    ~Buffer() { delete[] data; }

    int  capacity() const { return size; }
    int& operator[](int i) { return data[i]; }   // Week 1
};
```

Everything in this class is deliberate:

- `explicit` — so `Buffer b = 10;` does not compile.
- Initializer list **in declaration order** — so `-Wreorder` can never fire.
- `data(new int[n])` uses the **parameter**, not the member — correct regardless of declaration order.
- The destructor matches the constructor exactly: `new[]` pairs with `delete[]`.
- `capacity() const` — Lecture 03.

**And it is still broken.** Copy it:

```cpp
Buffer a(10);
Buffer b = a;      // compiles. Both objects now hold the SAME pointer.
```

When `a` and `b` are destroyed, `delete[]` runs twice on one allocation. That is a double free, and it
is the subject of Week 1's Rule of Three. The compiler generated a copy constructor for you, silently,
and it did the wrong thing — which is §2.1's rule biting from the other direction.

---

## 7. Summary

| Idea | The point |
| --- | --- |
| Constructor | An object cannot exist without one running |
| `= default` | Get the generated constructor back after declaring another |
| `explicit` | Stops a one-argument constructor becoming a silent conversion |
| Initializer list | Required for `const`, references and bases; never slower |
| **Declaration order rules** | The list's order is ignored — write it in declaration order |
| `-Wreorder` vs `-Wuninitialized` | The first means "misleading"; only the second means "wrong" |
| Destructor | Runs on every exit path from a scope, including exceptions |
| Reverse destruction order | The only order that is always safe |
| `new` without `delete` | The destructor never runs — verified, 8 bytes definitely lost |

---

## 8. Exercises

**1.** Write a `Noisy` class that prints in its constructor and destructor. Predict, then verify, the
output for:

```cpp
{ Noisy a("a"); { Noisy b("b"); } Noisy c("c"); }
```

**2.** Compile the `Wrong` struct from §4 with `-Wall -Wextra`. Instrument `operator new[]` to print
the byte count it receives, and report what `Wrong w(4)` actually allocates on your machine. **Does
your number match the lecture's? Should it?**

**3.** Take `NotABug` from §4.2 and explain in two sentences why `-Wreorder` fires on correct code.
Then rewrite it so the warning disappears without changing behaviour.

**4.** Add a `const int id;` member to `Buffer` and initialize it from a constructor parameter. Then
try to assign to it in the body and read the error.

**5.** Write a class holding a `FILE*` that opens in the constructor and `fclose`s in the destructor.
Use it in a function with three early `return`s. **How many `fclose` calls did you write?**

**6.** Why must destruction happen in reverse order of construction? Give a concrete two-object
example where the forward order would leave a dangling reference.

---

## 9. Next

**Lecture 03** covers the other half of a class definition: `private`, `const` member functions,
`inline` and namespaces — the features that decide who is allowed to touch what, and what the compiler
will let them do with it.

---

*PROG 102 · Week 0 · Lecture 02 · © CSE Department*
