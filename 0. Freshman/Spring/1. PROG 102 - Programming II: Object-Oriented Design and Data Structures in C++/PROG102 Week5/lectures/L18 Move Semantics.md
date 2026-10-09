# PROG 102 · Lecture 18
## Move Semantics

*“Software is under a constant tension. Being symbolic it is arbitrarily perfectible; but also it is arbitrarily changeable.”* — Alan Perlis, "Epigrams on Programming" (1982), #56

**Week 5 · Thursday · 50 minutes**
**Reading:** *C++ Primer* §13.6 · **Reference:** Meyers Items 23–25, 29
**Assumes:** Week 1 (Rule of Three, copy elision), L16, L17

**Date:** Thursday 25 February 2027 · 10:00–10:50 · Week 5

**Coursework:** 📝 **PS 4** due Fri 26 Feb 17:00 · 📝 **PS 5** released Fri 26 Feb 10:00, due Fri 5 Mar 17:00 · 🔬 **Lab 5** Mon 1 Mar 15:00–16:50 · 📊 **Quiz 6** Tue 2 Mar 10:00–10:15 · 📋 **Project 1** released Tue 2 Mar 10:00, due Fri 26 Mar 17:00 · 📘 **Midterm 1** Tue 2 Mar 18:00–19:30

---

## 1. The Problem

```cpp
auto p = std::make_unique<Widget>();
v.push_back(p);              // error: unique_ptr is not copyable
v.push_back(std::move(p));   // fine
```

`unique_ptr` cannot be copied (L16 §3.1). Yet it can be put into a vector, returned from a function,
and passed around. **Something other than copying is happening**, and this lecture is that something.

The other half of the problem is efficiency. Copying a 1 MB buffer to hand it to someone who is going
to keep it, when you were about to destroy your copy anyway, is pure waste.

---

## 2. Lvalues and Rvalues

An **lvalue** has a name and an address you can take. An **rvalue** is a temporary — the result of an
expression, about to disappear.

```cpp
std::string a = "hello";     // a is an lvalue
a + "!"                      // an rvalue: nothing else refers to it
std::string("hi")            // an rvalue
```

**The distinction matters because of what you may do to a temporary.** If nobody else can refer to it,
you may take its contents apart — nobody will notice.

C++11 added a reference type that binds only to rvalues:

```cpp
void f(const std::string& s);   // binds to anything
void f(std::string&& s);        // binds only to rvalues -- "I may gut this"
```

`&&` is an **rvalue reference**. Overload resolution prefers it for temporaries, which is how a class
can provide two implementations: an expensive-but-safe one for lvalues and a cheap one for things about
to die.

---

## 3. The Move Constructor

```cpp
struct Buf {
    std::size_t n; char* d;

    Buf(const Buf& o)                                   // COPY: allocate and duplicate
        : n(o.n), d(new char[o.n]) { std::copy(o.d, o.d + n, d); }

    Buf(Buf&& o) noexcept                               // MOVE: steal
        : n(o.n), d(o.d) { o.d = nullptr; o.n = 0; }

    ~Buf() { delete[] d; }
};
```

**The move constructor takes the pointer and nulls the source.** No allocation, no copying — three
assignments.

Nulling the source is not optional. **The source's destructor will still run**, and `delete[]` on a
pointer the new object now owns is the Week 1 double free.

### 3.1 What It Is Worth

Moving against copying **2,000 pre-built 1 MB buffers**, three runs:

| | per operation |
| --- | --- |
| copy | **941–1036 µs** |
| move | **0.055–0.156 µs** |

Roughly **four orders of magnitude**, and the ratio is noisy precisely because the move is close to
free — it is three stores against a megabyte of allocation and copying.

> **Read the absolute numbers, not the ratio.** A ratio of "17,000×" is a fact about how big the buffer
> was. The useful statement is: *a copy costs time proportional to the data; a move costs a constant
> few nanoseconds.*

---

## 4. `std::move` Does Not Move Anything

The most misleadingly named function in the standard library.

> **`std::move(x)` is a cast.** It converts `x` to an rvalue reference so that overload resolution
> picks the move constructor. It generates **no code** and moves **nothing**.

The move happens in the constructor or assignment operator that gets selected. `std::move` only makes
that selection possible.

### 4.1 The Source Afterwards

```cpp
std::string a = "a reasonably long string that will heap-allocate";
std::string b = std::move(a);
```

```
after move: b="a reasonably long string that will heap-allocate"
after move: a=""  (size 0) -- valid but unspecified
```

**The standard says a moved-from object is in a "valid but unspecified state".** You may destroy it or
assign to it. You may **not** assume what it contains — `a` being empty here is libstdc++'s choice, not
a guarantee.

```cpp
auto b = std::move(a);
a.size();          // legal, unspecified value
a = "new value";   // legal and fine -- assignment restores it
a[0];              // UNDEFINED -- you assumed it was non-empty
```

**For `unique_ptr` the state *is* specified: it is null.** That is a stronger guarantee than the
general rule and you may rely on it.

### 4.2 Do Not Move a Return Value

```cpp
Buf make() { Buf b(1024); return std::move(b); }   // WRONG
Buf make() { Buf b(1024); return b; }              // right
```

The `std::move` **disables NRVO** (Week 1 §L06 §6.1). Without it the compiler constructs `b` directly
in the caller and there is no move at all; with it you have forced a move that was not needed.

Counted, at both `-O0` and `-O2`:

| | copies | moves |
| --- | --- | --- |
| `return b;` | 0 | **0** |
| `return std::move(b);` | 0 | **1** |

**Return the local. The language already does better than you can here.**

> **And your build line says so.** `-Wall` catches this one:
>
> ```
> warning: moving a local object in a return statement prevents copy elision [-Wpessimizing-move]
> note: remove 'std::move' call
> ```
>
> The compiler names the mistake and tells you the fix. Worth noticing after Week 4, where the
> non-virtual destructor got silence — **the diagnostics are good where the mistake is visible in one
> expression, and absent where it is a fact about design.**

---

## 5. `noexcept` Is Load-Bearing

```cpp
Buf(Buf&& o) noexcept;      // the noexcept matters
```

When a `std::vector` grows it must relocate its elements. It will **move** them only if the move
constructor is `noexcept`; otherwise it **copies**.

The reason is the strong exception guarantee (Week 1 §L06 §2.3, and Week 9). Halfway through moving
elements into new storage, a throwing move would leave the vector with some elements moved out of the
old buffer and some not — **unrecoverable**, because you cannot move them back without risking another
throw. Copying is safe: the original is untouched until the copy succeeds.

> **A move constructor that is not `noexcept` will silently not be used** in the place it matters most.
> Write `noexcept` on every move constructor and move assignment operator. If yours can genuinely
> throw, redesign it so it cannot — a move should be stealing pointers, and stealing pointers does not
> throw.

---

## 6. The Rule of Five

Week 1's Rule of Three, extended:

> **If you define any of: destructor, copy constructor, copy assignment, move constructor, move
> assignment — you probably need to consider all five.**

```cpp
struct Buf {
    ~Buf();
    Buf(const Buf&);                 Buf& operator=(const Buf&);
    Buf(Buf&&) noexcept;             Buf& operator=(Buf&&) noexcept;
};
```

**And there is a trap:** declaring a destructor, or any copy operation, **suppresses** the generated
move operations. A class with a hand-written destructor and no move constructor will be *copied*
wherever it could have been moved — silently, and often in a `std::vector` growth.

That is why the rule says *consider all five*, not *write all five*.

---

## 7. The Rule of Zero

The rule you should actually aim for.

> **Write none of the five.** Use members that manage themselves — `std::string`, `std::vector`,
> `std::unique_ptr` — and the compiler-generated versions are correct.

```cpp
class Roster {                        // Lab 1's class, done properly
    std::vector<std::string> names;
public:
    void add(std::string n) { names.push_back(std::move(n)); }
    std::size_t size() const { return names.size(); }
};
```

**No destructor. No copy constructor. No assignment. No move operations.** Copying works, moving works,
destruction works, it is exception-safe, and it cannot double-free.

Compare it with Lab 1's original, which had four bugs, and with your repaired version, which needed a
deep-copy constructor, a `noexcept` swap and a copy-swap assignment. **The vector was the answer the
whole time.**

> **This is the point the whole first third of the course has been building to.** You wrote the Rule of
> Three by hand so that you would understand what `std::vector` and `unique_ptr` are doing — and now
> that you do, you should almost never write it again.
>
> **Write the five only when you are implementing a resource wrapper**: a class whose entire job is to
> own something the standard library does not already own for you. That is Week 6's job, and after
> that it is rare.

---

## 8. Where Moves Show Up Without You Asking

```cpp
v.push_back(std::string(200, 'x'));            // the temporary is moved in
std::string s(200, 'x'); v.push_back(s);       // copied
std::string t(200, 'x'); v.push_back(std::move(t));   // moved
```

Measured, 200,000 strings of 200 characters, with `reserve` so growth is not a factor:

| | time | |
| --- | --- | --- |
| `push_back(s)` | 44.3–46.8 ms | copies |
| `push_back(std::move(s))` | 37.5–41.5 ms | moves |
| ratio | **1.13–1.18×** | |

Modest — because a 200-character string is a small allocation. Make it a megabyte and it is §3.1.

> **A measurement note.** The first version of this benchmark had no `reserve` and reported the *move*
> version as **slower** (0.75×). The vector was reallocating during the loop, which moves every element
> and swamped the difference. Adding `reserve` and running both orders gave the table above.
>
> **Week 3's lab lesson, again:** measure the operation you mean, not the operation plus whatever else
> the container decided to do.

---

## 9. Summary

| Idea | The point |
| --- | --- |
| Lvalue / rvalue | An rvalue is a temporary; nothing else refers to it |
| `T&&` | Binds only to rvalues — "I may gut this" |
| Move constructor | Steal the pointer, **null the source** |
| Worth | Copy 941–1036 µs per 1 MB; move 0.055–0.156 µs |
| **`std::move` is a cast** | It generates no code and moves nothing |
| Moved-from state | Valid but **unspecified** — except `unique_ptr`, which is null |
| `return std::move(x)` | Wrong — it disables NRVO |
| `noexcept` on moves | Without it `vector` growth **copies** instead |
| Rule of Five | Declaring any suppresses the generated moves |
| **Rule of Zero** | Write none. Let `vector`, `string`, `unique_ptr` do it |
| Measurement note | Without `reserve`, the move benchmark reported moves as *slower* |

---

## 10. Exercises

**1.** Add a move constructor and move assignment to your Week 1 `Buffer`. Print from copy and move.
Then run the reference `main` and **report which one each operation chose.**

**2.** Reproduce §3.1: copy against move for 1 MB buffers. Report per-operation times. **Then repeat
with a 16-byte buffer and explain the change in ratio.**

**3.** Move from a `std::string` and print the source. Then try `a[0]` on it. **Which of those is
undefined, and why is the other one fine?**

**4.** Write `Buf make()` two ways — `return b;` and `return std::move(b);` — with counting copy and
move constructors. **Report the counts for both.**

**5.** Remove `noexcept` from your move constructor, `reserve`-free `push_back` 100,000 elements into a
vector, and count moves against copies. Add `noexcept` back and count again.

**6.** Rewrite Lab 1's `Roster` under the Rule of Zero. **Count the lines you deleted**, and confirm
`a = a`, copying, and moving all work with no special members at all.

**7.** Reproduce §8's benchmark **without** `reserve` first, then with it, in both orders. **Report all
four numbers** and explain the one that disagrees with the others.

---

## 11. Next

**Week 6** puts all of this to work: a templated doubly linked list and a BST, with nodes owned by
`unique_ptr`, iterators that work with STL algorithms, and the Rule of Zero wherever it applies.

It is also the week **Project 1 is assigned**, and the week the course stops giving you the class to
write and starts giving you the interface to satisfy.

**Midterm 1 is next Tuesday, 2 March, 18:00.** Whatever it tells you about Weeks 0–4, Week 6 assumes all of it.

---

*PROG 102 · Week 5 · Lecture 18 · © CSE Department*
