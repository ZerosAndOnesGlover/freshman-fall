# PROG 102 · Lecture 08
## Class Templates and Generic Containers

**Week 2 · Wednesday · 50 minutes**
**Reading:** *C++ Primer* §16.1.2, §16.1.3 · **Reference:** Stroustrup Ch. 23
**Assumes:** L07, and Week 1's Rule of Three

---

## 1. Parameterising a Class

Same idea as Lecture 07, applied to a class:

```cpp
template <typename T>
class Stack {
    T*  data;
    int count;
    int cap;
public:
    explicit Stack(int c) : data(new T[c]), count(0), cap(c) {}
    ~Stack() { delete[] data; }
    void push(const T& value);
    T    pop();
};
```

`T` is usable anywhere in the class — as a member type, a parameter, a return type, a `new` argument.

**`Stack` is not a type.** You cannot declare a `Stack s;`. `Stack<int>` is a type; so is
`Stack<std::string>`; and they are **as unrelated to each other as `int` is to `std::string`**. There
is no base class in common, no shared code, and no conversion between them.

```cpp
Stack<int>    a(4);
Stack<double> b(4);
a = b;        // error: no known conversion
```

---

## 2. Defining Members Outside the Class

The syntax is verbose and there is no way around it:

```cpp
template <typename T>
void Stack<T>::push(const T& value) {
    if (count == cap) grow();
    data[count++] = value;
}
```

Three things must be right:

- **`template <typename T>` repeats** on every member definition. Each one is its own template.
- **`Stack<T>::`** — the class name carries its arguments. `Stack::push` is not a thing.
- **Inside the body, `T` is in scope**, and so are the members.

The return type is outside the class scope, so a member returning a nested type needs qualification —
and, awkwardly, `typename`:

```cpp
template <typename T>
typename Stack<T>::size_type Stack<T>::size() const { return count; }
```

> **Why `typename` there?** Because the compiler does not yet know whether `Stack<T>::size_type` is a
> type or a static member — it depends on `T`, which is not known yet. `typename` promises it is a
> type. You will meet this error in Week 6 when you write iterators, and the message
> *"need 'typename' before ... because ... is a dependent scope"* is the compiler asking for exactly
> this.

---

## 3. The Header Rule

Here is the thing that catches everyone. Put a class template's declarations in `stack.hpp` and its
definitions in `stack.cpp`, as you would for an ordinary class, and:

```
/usr/bin/ld: main.o: in function `main':
undefined reference to `Stack<int>::Stack(int)'
undefined reference to `Stack<int>::push(int const&)'
undefined reference to `Stack<int>::size() const'
undefined reference to `Stack<int>::~Stack()'
```

And `stack.o` — which compiled without error — contains **no symbols at all**.

### 3.1 Why

Lecture 07 §4: **a template is not code until it is instantiated.**

When the compiler builds `stack.cpp`, it sees the definitions and nobody asking for `Stack<int>`. So it
generates nothing. When it builds `main.cpp`, it sees the *declarations* — enough to type-check
`s.push(7)` — but not the bodies, so it cannot generate them either. It emits calls and leaves them to
the linker, and the linker finds nothing.

**Neither translation unit had both halves at once**, and instantiation needs both.

### 3.2 The Fix

**Put the definitions in the header.** That is the normal answer and it is what the entire standard
library does — `<vector>` is not a stub, it is the implementation.

```cpp
// stack.hpp
#pragma once
template <typename T> class Stack { ... };
template <typename T> void Stack<T>::push(const T& v) { ... }   // definition, in the header
```

Some codebases split it cosmetically, with the header including a `.tpp` or `.inl` file at the bottom.
That is the same thing with extra steps: the definitions still reach every translation unit.

### 3.3 The Other Fix, and When to Use It

If you know in advance every type your template will be used with, you can instantiate them explicitly
in the `.cpp`:

```cpp
// stack.cpp
template class Stack<int>;         // "generate the whole class for int, here"
template class Stack<double>;
```

That produced 8 symbols and the program linked.

**Use this when the type list is genuinely closed** — a matrix template for `float` and `double`, say.
The benefit is real: the implementation stays private, and callers do not recompile when it changes.
The cost is that a user wanting `Stack<char>` gets a link error and cannot fix it without editing your
`.cpp`.

> **This is the template trade-off in its administrative form.** Definitions in headers mean every user
> recompiles when you change an implementation detail — which is a significant part of why large C++
> projects build slowly. Lab 2 measures the compile-time side of this.

---

## 4. The Rule of Three, Written Once

Week 1's whole apparatus, now generic:

```cpp
template <typename T>
class Stack {
    T* data; int count; int cap;
public:
    Stack() : data(new T[InitialCap]), count(0), cap(InitialCap) {}

    Stack(const Stack& o)                                  // copy constructor
        : data(new T[o.cap]), count(o.count), cap(o.cap) {
        for (int i = 0; i < count; ++i) data[i] = o.data[i];
    }
    void swap(Stack& o) noexcept {                         // swap
        std::swap(data, o.data); std::swap(count, o.count); std::swap(cap, o.cap);
    }
    Stack& operator=(Stack o) { swap(o); return *this; }   // copy-swap
    ~Stack() { delete[] data; }
};
```

**Written once, correct for every `T`.** That is the payoff: Lab 1's `Roster` and Week 0's `IntStack`
were the same code twice, and this is that code once.

Two details specific to templates:

- **Copy the elements with `=`, not `memcpy`.** `memcpy` is correct for `int` and catastrophic for
  `std::string` — it would duplicate the string's internal pointer and produce Week 1's double free.
  `data[i] = o.data[i]` calls `T`'s own assignment operator, which is right for both.
- **`new T[n]` default-constructs every element.** So `T` must have a default constructor. That is a
  real constraint, and it is why `std::vector` does *not* do this — it allocates raw memory and
  constructs elements individually. Week 3 explains what it uses instead.

Verified working across three very different types:

```
int:    size=6 cap=8 top=36
deep:   s.size=6 t.size=5
assign: u.size=6 u.top=36
string: size=2 top=grace
double: size=3 cap=4 (started at 2)
empty:  pop from empty stack
```

Sanitizer-clean. **The `std::string` row is the one that matters** — it exercises a `T` with its own
Rule of Three, and it works because the template never assumed anything about `T` beyond assignability.

---

## 5. Non-Type Template Parameters

A template parameter can be a **value** rather than a type:

```cpp
template <typename T, int N>
struct FixedArray {
    T data[N];
    static constexpr int size() { return N; }
};

FixedArray<int, 8> fa;
```

Measured: `fa.size()` is 8 and `sizeof(fa)` is **32** — eight `int`s, with no length field stored,
because **`N` is not a member.** It is part of the *type*.

This is how `std::array<T, N>` works, and it is why `std::array` has zero overhead over a C array while
`std::vector` has a pointer and two integers.

Consequences worth stating:

- **`FixedArray<int,8>` and `FixedArray<int,9>` are different types.** You cannot assign one to the
  other, and a function taking `FixedArray<int,8>` will not accept the other.
- **`N` must be a compile-time constant.** `int n = read(); FixedArray<int, n> a;` does not compile.
- Each distinct `N` is a **separate instantiation**, with its own code. Lecture 09 measures what that
  costs.

`Stack` uses one as a default:

```cpp
template <typename T, int InitialCap = 4>
class Stack { ... };

Stack<int> s;            // InitialCap = 4
Stack<double, 2> d;      // InitialCap = 2
```

**Default template arguments** work like default function arguments: trailing only, and given once on
the declaration. Verified: `Stack<double,2>` started at capacity 2 and grew to 4.

---

## 6. `std::pair` and `std::tuple`

Two class templates from the standard library you should use rather than reinvent.

```cpp
#include <utility>
#include <tuple>

auto p = std::make_pair(1, std::string("one"));
auto t = std::make_tuple(2, 3.5, 'c');

p.first;  p.second;                                // pair: named members
std::get<0>(t); std::get<1>(t); std::get<2>(t);    // tuple: by index
```

```
pair  : 1 one
tuple : 2 3.5 c
```

`std::pair<A,B>` holds exactly two things and is what `std::map` stores (Week 3). `std::tuple` holds
any number.

**Note `std::get<0>(t)` uses a non-type template parameter** — the index is part of the type, which is
how the return type can differ per element. `t[0]` could not do that, which is why tuples have no
`operator[]`.

### 6.1 Structured Bindings

C++17 lets you unpack them:

```cpp
auto [a, b, c] = t;      // a=2, b=3.5, c='c'
```

```
bound : 2 3.5 c
```

Verified. This works on tuples, pairs, arrays and plain structs, and it is the single most useful small
feature in C++17. It comes back properly in **Week 11**, and in **Week 3** for iterating a `std::map`:

```cpp
for (const auto& [key, value] : my_map) { ... }
```

**Prefer `pair`/`tuple` for genuinely anonymous groupings** — a function returning two things, a map
entry. **Prefer a named `struct` when the fields mean something**, because `p.second` tells the reader
nothing and `result.distance` tells them everything.

---

## 7. Summary

| Idea | The point |
| --- | --- |
| `template <typename T> class Stack` | `Stack` is not a type; `Stack<int>` is |
| `Stack<int>` vs `Stack<double>` | Unrelated types, no shared code, no conversion |
| Out-of-class members | `template <typename T> ... Stack<T>::member` |
| `typename` on dependent types | The compiler cannot tell a type from a value until `T` is known |
| **Definitions go in the header** | Verified: otherwise no symbols, and 4 undefined references |
| Explicit instantiation | The alternative, when the type list is closed |
| Rule of Three, once | Copy elements with `=`, never `memcpy` |
| `new T[n]` needs a default constructor | A real constraint; `std::vector` avoids it |
| Non-type parameters | `FixedArray<int,8>` is 32 bytes; `N` is in the type, not the object |
| Default template arguments | Trailing only, on the declaration |
| `pair`, `tuple`, structured bindings | Use them; prefer a named struct when fields have meaning |

---

## 8. Exercises

**1.** Take Lab 1's repaired `Roster` and make it `Roster<T>`. **Keep the Rule of Three.** Verify it
works for `T = int` and `T = std::string`, and that both are sanitizer-clean.

**2.** Split your `Stack<T>` into `stack.hpp` (declarations) and `stack.cpp` (definitions) and try to
link. **Paste the errors, and paste `nm stack.o`.** Then fix it two ways — moving the definitions, and
explicit instantiation — and say when you would choose each.

**3.** In your copy constructor, replace the element-copy loop with `std::memcpy`. Show it still works
for `Stack<int>` and demonstrate what it does to `Stack<std::string>`. **Run it under
`-fsanitize=address` and paste the report.**

**4.** Write `FixedArray<T,N>` and print `sizeof` for `N` = 4, 8 and 16. **Where is `N` stored?**

**5.** Write a function taking `FixedArray<int,8>` and try to pass it a `FixedArray<int,9>`. Paste the
error and explain it in one sentence.

**6.** `new T[n]` requires `T` to be default-constructible. Write a class with **only** a
one-argument constructor and try to put it in your `Stack`. Paste the error. **How does `std::vector`
avoid this?** *(Answer from Week 3's reading if you like — one sentence.)*

**7.** Write a function returning both a quotient and a remainder, once with `std::pair` and once with
a named `struct`. **Which reads better at the call site, and why?**

---

## 9. Next

**Lecture 09** answers the question this lecture has been deferring: if every instantiation generates
its own code, **what does that cost?** The answer is measured — compile time, binary size, and the
78-line error messages — and one widely-repeated claim about it turns out to be wrong.

---

*PROG 102 · Week 2 · Lecture 08 · © CSE Department*
