# PROG 102 · Lecture 34
## Lambdas and Closures

**Week 11 · Monday · 50 minutes**
**Reading:** Meyers, *Effective Modern C++* Items 31–33 · **Assumes:** Week 1 (`operator()`), Week 2

---

## 1. A Lambda Is a Class

```cpp
[x](int y) { return x + y; }
```

**The compiler writes this for you:**

```cpp
class __anonymous {
    int x;                                              // the capture, as a data member
public:
    int operator()(int y) const { return x + y; }       // the body, as a call operator
};
```

You met that class in **Week 1 §L04 §5** under the name **functor**. A lambda is the same thing with
the boilerplate removed.

**And it is exactly the same size.** Comparing a hand-written class against the lambda it corresponds
to:

| | `sizeof` |
| --- | --- |
| `struct Manual { int x; ... }` | **4** |
| `[x](int y){ return x+y; }` | **4** |

### 1.1 `sizeof` Follows the Capture List

| Lambda | `sizeof` | Why |
| --- | --- | --- |
| `[](int y){...}` | **1** | Captures nothing — an **empty class**, and Week 0 §L01 §3.1 said those are 1 byte |
| `[x](int y){...}` | **4** | one `int` |
| `[x,d](int y){...}` | **16** | `int` + `double` + padding |
| `[&x](int y){...}` | **8** | a reference — stored as a pointer |
| `[s](int y){...}` with `std::string s` | **32** | **the whole string object** |

> **A lambda's size is the sum of what it captured.** That is not a metaphor — you can measure it, and
> Lab 11 asks you to predict it before you do.
>
> **Note the last row.** Capturing a `std::string` by value copies the entire object, including a heap
> allocation if the string is long. **Capturing is construction**, and it obeys every rule from Weeks
> 1 and 5.

### 1.2 What Kind of Class

Verified with type traits:

```
is a class type?        yes
copy-constructible?     yes
default-constructible?  no
each lambda a distinct type? yes -- distinct
```

**Every lambda expression has its own unique, unnamable type.** Two lambdas with identical bodies are
different types. That is why you write `auto`, and why storing one in a container requires either a
template parameter or `std::function` (Lecture 35).

**Not default-constructible** in C++17 — which matters if you try to make one a member of a class you
want to default-construct. *(C++20 relaxed this for captureless lambdas.)*

---

## 2. Capture

```cpp
int x = 1; double d = 2.0;

[ ]        // capture nothing
[x]        // x by value (a copy, made when the lambda is created)
[&x]       // x by reference
[=]        // everything used, by value
[&]        // everything used, by reference
[=, &x]    // by value, except x
[&, x]     // by reference, except x
[this]     // the enclosing object's `this` pointer -- by reference to the object
[x = compute()]   // init-capture (C++14): a new member, initialised from anything
```

### 2.1 By Value Is a Copy Made *Then*

```cpp
int x = 1;
auto f = [x]{ return x; };
x = 99;
f();                 // 1, not 99
```

**The copy happened when the lambda was constructed.** This surprises people who expect it to behave
like a closure in a garbage-collected language, where captures are usually by reference.

**And the captured member is `const` by default** — the call operator is `const`. To modify it:

```cpp
auto counter = [n = 0]() mutable { return ++n; };    // mutable: operator() is non-const
```

### 2.2 `[=]` and `[&]` Are Convenient and Worth Avoiding

`[=]` copies **everything the body uses**, which may include a `std::string` or a whole container you
did not think about. `[&]` references everything, which is fine until the lambda outlives the scope.

> **Prefer an explicit capture list.** It is a few more characters, it documents what the lambda
> depends on, and it makes §3's bug visible at the capture site rather than in a stack trace.
>
> **`[this]` deserves special suspicion**: it captures a *pointer*, so the lambda is only valid while
> the object is. In **Week 10**'s threads and **Week 8**'s observers, that is exactly the lifetime you
> cannot guarantee. C++17's `[*this]` copies the object instead.

---

## 3. The Dangling Capture

```cpp
std::function<int()> make_bad() {
    int local = 42;
    return [&local]{ return local; };      // returns a reference to a dead stack frame
}
```

**This compiles with no warning under `-Wall -Wextra -pedantic`.**

Under AddressSanitizer:

```
ERROR: AddressSanitizer: stack-use-after-return
    ... in operator()  dangle.cpp:3
```

The by-value version is fine:

```
capture by value    : 42
```

> **The compiler is silent, and this is worth pausing on.** Week 2 §L07 §7 found that
> `-Wdangling-reference` catches a dangling reference from a function *call*. Here the reference is
> captured into an object that outlives its referent, and the analysis needed to see that is
> interprocedural — so nothing warns.
>
> **This is the single most common lambda bug**, and it is the reason `[&]` is dangerous rather than
> merely untidy. **It appears whenever a lambda outlives its scope**: returned from a function, stored
> in a container, registered as a callback (**Week 8**), or handed to a thread (**Week 10**).
>
> **Rule: if the lambda might outlive the enclosing scope, capture by value.** For a thread or a
> callback, that is always.

---

## 4. Lambdas Are Why the STL Works the Way It Does

```cpp
std::count_if(v.begin(), v.end(), [](int x){ return x % 2 == 0; });
std::sort(v.begin(), v.end(), [](const P& a, const P& b){ return a.score > b.score; });
v.erase(std::remove_if(v.begin(), v.end(), [k](int x){ return x < k; }), v.end());
```

**Week 3 §L12 §7 said "prefer algorithms to loops" and every example needed a lambda.** Before C++11
you would have written a functor class — five lines, in a different part of the file, for a predicate
used once.

**And the captured state is the point.** `[k]` above carries a value into the algorithm. A function
pointer cannot do that (**Week 8 §L26 §3**), which is why `qsort` needs a global or an extra parameter
and `std::sort` does not.

### 4.1 Generic Lambdas

```cpp
auto print = [](const auto& x) { std::cout << x << "\n"; };   // C++14
```

`auto` in a parameter makes `operator()` a **template**. One lambda, any type — which is Week 2's
machinery, applied without the syntax.

---

## 5. Summary

| Idea | The point |
| --- | --- |
| A lambda **is a class** | Captures are members; the body is `operator()` |
| Same size as the hand-written version | 4 bytes for `[x]`, verified |
| Empty lambda is **1 byte** | Week 0's empty-class rule |
| `[s]` with a `std::string` is **32** | Capturing is construction |
| Every lambda has a unique type | Hence `auto`, hence `std::function` |
| Not default-constructible | In C++17 |
| `[x]` copies **at creation** | Not at call |
| `mutable` | Makes `operator()` non-`const` |
| Prefer explicit captures | `[=]`/`[&]` hide what you depend on |
| **Dangling capture** | `stack-use-after-return`, and **no compiler warning** |
| The rule | If it may outlive the scope, capture **by value** |

---

## 6. Exercises

**1.** Write a hand-written functor and the equivalent lambda. **Confirm they are the same `sizeof`**
and that both work with `std::count_if`.

**2.** Predict `sizeof` for six lambdas with different captures — including one capturing a
`std::string` and one capturing nothing. **Then measure.** Report predictions and results.

**3.** Show that `[x]` copies at creation: capture, modify the original, call. **Then make it
`mutable`** and show the lambda's own copy changing across calls.

**4.** Reproduce §3's dangling capture. Confirm **no warning** under `-Wall -Wextra -pedantic`, then
catch it with AddressSanitizer. **Then fix it** and explain the fix in one sentence.

**5.** Write a lambda capturing `[this]` inside a class, store it, destroy the object, and call it.
**Report what ASan says.** Then fix it with `[*this]`.

**6.** Take three raw loops from your Project 1 code and rewrite them with algorithms and lambdas.
**Nominate one where the loop was better** and defend it.

**7.** Write a generic lambda that prints anything streamable. Call it with three different types.
**What is `operator()` in the generated class?**

---

## 7. Next

**Lecture 35** answers the question §1.2 raises: if every lambda has a unique type, how do you store
one in a `vector`, or return one from a function whose signature is fixed? The answer is
`std::function`, and Week 8 already measured what it costs.

---

*PROG 102 · Week 11 · Lecture 34 · © CSE Department*
