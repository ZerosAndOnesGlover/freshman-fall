# PROG 102 · Lecture 30
## `noexcept`, Assertions, and Contracts

**Week 9 · Thursday · 50 minutes**
**Reading:** Meyers, *Effective Modern C++* Item 14 · **Assumes:** L28, L29

**Date:** Thursday 18 March 2027 · 10:00–10:50 · Week 9

---

## 1. `noexcept`

```cpp
void swap(Buffer& o) noexcept;
Buffer(Buffer&& o) noexcept;
```

**`noexcept` is a promise to the compiler and to the library**, not a request. It says: *this function
will not let an exception escape.*

### 1.1 What Happens If You Lie

```cpp
void liar() noexcept { throw std::runtime_error("I promised not to"); }
try { liar(); } catch (...) { /* does this help? */ }
```

**The compiler warns:**

```
warning: 'throw' will always call 'terminate' [-Wterminate]
```

**And at run time:**

```
terminate called after throwing an instance of 'std::runtime_error'
  what():  I promised not to
Aborted (core dumped)          exit 134
```

**The `catch (...)` did not run.** When an exception tries to escape a `noexcept` function,
`std::terminate` is called immediately — **there is no unwinding, no handler search, no chance to
recover.** Your process dies.

> **That severity is the point.** `noexcept` is not a hint the optimizer may ignore; it is a contract
> whose violation is defined to be fatal. **Do not write it hopefully.**

### 1.2 Where It Is Load-Bearing

Three places where `noexcept` changes behaviour rather than documentation:

**Move constructors.** `std::vector` growth moves elements only if the move is `noexcept`; otherwise it
copies (L18 §5). **A missing `noexcept` here silently costs you the entire benefit of move semantics**
in the place it matters most.

**`swap`.** It is the commit step of every strong-guarantee operation (L29 §4.1). If it can throw, the
commit can fail halfway and the strong guarantee is a fiction.

**Destructors.** Implicitly `noexcept` since C++11. A destructor that throws during unwinding means two
exceptions in flight, and the language's answer is `std::terminate`.

### 1.3 `noexcept` as a Query

```cpp
noexcept(1 + 1)       // 1 -- cannot throw
noexcept(new int)     // 0 -- can throw std::bad_alloc
```

and via type traits:

```
A (noexcept move)      move-ctor noexcept? yes
B (throwing move)      move-ctor noexcept? no
std::string            move-ctor noexcept? yes
std::vector<int>       move-ctor noexcept? yes
```

**This is how the library decides.** `std::vector` asks `std::is_nothrow_move_constructible` and
branches at compile time. Your type's answer is a performance decision made without your involvement.

### 1.4 Conditional `noexcept`

For a template, whether you can promise depends on `T`:

```cpp
template <typename T>
void swap(MyBox<T>& a, MyBox<T>& b) noexcept(std::is_nothrow_swappable<T>::value);
```

**Promise exactly as much as `T` lets you.** This is common in library code and rare in application
code; recognise it, and do not reach for it unless you are writing a container.

### 1.5 When to Write It

- **Always** on move constructors, move assignment, `swap` and destructors — or explain why not.
- **On simple observers** — getters, `size()`, `empty()` — where it is obviously true.
- **Not on anything that allocates**, opens a file, or calls something you do not control.

> **The failure mode is optimism.** A function that "shouldn't" throw is not `noexcept`; a function
> that **cannot** is. If you are not certain, leave it off — an unmarked function that never throws
> costs you a missed optimization, and a wrongly-marked one costs you the process.

---

## 2. Assertions Are Not Exceptions

Both report that something is wrong. **They report different kinds of wrong, to different audiences.**

| | Assertion | Exception |
| --- | --- | --- |
| Reports | **a bug in the program** | **a condition in the world** |
| Audience | the programmer | the calling code |
| Recoverable | no — the code is wrong | yes, that is the point |
| In release builds | often compiled out | always present |
| Example | index out of range on an internal array | file not found, out of memory |

```cpp
#include <cassert>

double Vector3D::operator[](int i) const {
    assert(i >= 0 && i < 3);          // a bug if false
    return e[i];
}

std::string read_config(const std::string& path) {
    std::ifstream f(path);
    if (!f) throw std::runtime_error("cannot open " + path);   // the world
    ...
}
```

### 2.1 The Test

> **Could a correct caller trigger this?**
>
> **Yes** → it is a runtime condition → **exception**.
> **No, only a buggy one could** → **assertion**.

A file being missing is not a bug; the file might be missing. An index of 7 into a three-element vector
*is* a bug, in the caller, and no amount of error handling will fix it.

### 2.2 Why It Matters That Assertions Vanish

`assert` is disabled by `NDEBUG`, which release builds usually define. **So an assertion is a
development-time check, not a runtime defence.**

Two consequences people get wrong:

- **Never put a side effect in an `assert`.** `assert(pop() == 3);` works in debug and silently stops
  popping in release. This is a real and nasty bug class.
- **Do not assert things you cannot control.** Validating user input with `assert` means your release
  build has no validation at all.

### 2.3 `static_assert` Is Better When Possible

```cpp
static_assert(sizeof(Node) <= 64, "Node must fit in a cache line");
```

**Checked at compile time, cannot be disabled, costs nothing.** Whenever a condition is about types or
constants rather than values, this is strictly better. You met it in L03 §3.1.

---

## 3. Contracts

A **contract** is what a function promises and requires. Three parts:

| | Who guarantees it |
| --- | --- |
| **Precondition** | the **caller** |
| **Postcondition** | the **function** |
| **Invariant** | the class, between every public call |

```cpp
/// Removes the top element.
/// @pre  !empty()
/// @post size() == old size() - 1
/// Invariant: size() <= capacity()
T pop();
```

C++ has no language support for these — **a contracts proposal has been repeatedly deferred** — so they
live in documentation, assertions and tests.

### 3.1 Who Checks What

**A precondition violation is the caller's bug**, so: **document it, assert it, and do not throw.**

```cpp
T pop() {
    assert(!empty());              // caller's bug; catch it in development
    return data[--count];
}
```

**Unless the caller cannot reasonably check it first** — then throwing is kinder:

```cpp
T at(std::size_t i) const {
    if (i >= count) throw std::out_of_range("at");   // checkable, but throwing is the contract
    return data[i];
}
```

> **This is exactly the `operator[]` / `at()` split in the standard library** (L11 §2.3), and now you
> can see it is a contract decision rather than an inconsistency. **`operator[]` puts the precondition
> on the caller and does not check. `at()` takes responsibility and throws.** Two functions, two
> contracts, deliberately.

### 3.2 What This Course Has Been Doing

Every assignment in this course has stated a contract without using the word:

- Week 1's `operator<` must be a **strict weak ordering** — a precondition, and violating it is UB.
- Week 6's iterator must satisfy **`LegacyBidirectionalIterator`** — a contract you were marked against.
- Week 9's containers must state **which guarantee** they provide — a postcondition about failure.

**Naming the guarantee (L29) is writing down half your contract.** The other half is what you require
of the caller.

---

## 4. Putting It Together

```cpp
template <typename T>
class Stack {
    std::vector<T> data;
public:
    /// @pre  none
    /// @post size() == old size() + 1
    /// Strong guarantee.
    void push(const T& v) { data.push_back(v); }

    /// @pre  !empty()
    /// @post size() == old size() - 1
    /// Nothrow, given a nothrow-movable T.
    void pop() noexcept { assert(!empty()); data.pop_back(); }

    /// Nothrow.
    bool empty() const noexcept { return data.empty(); }

    /// Nothrow.
    void swap(Stack& o) noexcept { data.swap(o.data); }
};
```

**Every public function states its guarantee.** That is the deliverable of this week, and it is what
Project 1 Part 3.3 asks for.

---

## 5. Summary

| Idea | The point |
| --- | --- |
| `noexcept` is a contract | Violating it calls `std::terminate` — **the `catch` does not run** |
| The compiler warns | `-Wterminate` |
| Load-bearing on | move constructors, `swap`, destructors |
| A missing `noexcept` on a move | Silently makes `vector` **copy** |
| `noexcept` as a query | How the library decides, at compile time |
| Write it when it **cannot** throw | Not when it "shouldn't" |
| **Assertion** | A bug, reported to the programmer, gone in release |
| **Exception** | A condition, reported to the caller, always present |
| The test | *Could a correct caller trigger this?* |
| Never a side effect in `assert` | It vanishes under `NDEBUG` |
| `operator[]` vs `at()` | Two contracts, deliberately — not an inconsistency |
| Contracts | Precondition (caller), postcondition (function), invariant (class) |

---

## 6. Exercises

**1.** Write a `noexcept` function that throws. **Paste the compiler warning and the runtime output.**
Confirm that a surrounding `catch (...)` does not run, and explain why.

**2.** Take a class with a move constructor. Measure `vector` growth **with and without** `noexcept` on
it, counting moves and copies. **Report both.**

**3.** Print `noexcept(expr)` for five expressions of your choosing, at least two of which surprise you.

**4.** Find three functions in your Project 1 code that should be `noexcept` and are not. **Add it, and
justify each in one line.**

**5.** For each of these, decide **assertion or exception**, and justify in one sentence: an index past
the end of an internal buffer; a config file that will not parse; a null pointer passed to a private
helper; a network timeout; a negative size passed to your container's constructor.

**6.** Write an `assert` with a side effect. **Show it behaving differently with and without
`-DNDEBUG`.**

**7.** Take one class from Project 1 and write the full contract for every public function —
precondition, postcondition, guarantee. **Then find one function whose contract you could not state**,
and say what that tells you.

---

## 7. Next

**Week 10** is concurrency, and it makes all of this harder in a specific way: **an exception that
escapes a thread's function calls `std::terminate` immediately** — there is no other thread to catch
it. Everything you have learned this week has to be rebuilt for that.

**Midterm 2 is in Week 10** and covers Weeks 5–9.

---

*PROG 102 · Week 9 · Lecture 30 · © CSE Department*
