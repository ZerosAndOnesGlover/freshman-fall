# PROG 102 · Lecture 07
## Function Templates and Type Deduction

**Week 2 · Tuesday · 50 minutes**
**Reading:** *C++ Primer* §16.1.1, §16.2 · **Reference:** Stroustrup Ch. 23
**Assumes:** L03 §4 (`inline`, weak symbols), Week 1 entire

**Date:** Tuesday 2 February 2027 · 10:00–10:50 · Week 2

---

## 1. The Problem

Here is `maxof` for `int`:

```cpp
int maxof(int a, int b) { return a > b ? a : b; }
```

Now you need it for `double`. And `long`. And `std::string`. In C you would write three functions, or
one macro:

```c
#define MAXOF(a,b) ((a) > (b) ? (a) : (b))
```

The macro works for every type and is a genuinely bad answer. It evaluates its arguments twice —
`MAXOF(i++, j)` increments `i` once or twice depending on which is larger — it has no type checking, it
cannot be stepped through in a debugger, and its errors are reported against the expanded text.

**C++ lets you write it once, with type checking, and no runtime cost.**

```cpp
template <typename T>
T maxof(T a, T b) { return a > b ? a : b; }
```

---

## 2. Syntax

```cpp
template <typename T>       // T is a type parameter
T maxof(T a, T b) { ... }
```

`template <typename T>` introduces a **template parameter list**. Inside the function, `T` is a type
you may use anywhere a type is allowed.

> **`typename` and `class` are interchangeable here.** `template <class T>` means exactly the same
> thing. This course writes `typename`, because `T` need not be a class — `maxof<int>` is the common
> case and `class T` reads misleadingly.

Multiple parameters are comma-separated:

```cpp
template <typename T, typename U>
void pair_up(const T& a, const U& b);
```

---

## 3. Type Deduction

You do not usually say what `T` is. The compiler works it out from the arguments:

```cpp
maxof(3, 7);        // T = int
maxof(4.2, 1.0);    // T = double
maxof('a', 'z');    // T = char
```

Verified with `typeid`:

```
T = i                                        (int)
T = d                                        (double)
T = c                                        (char)
T = NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE    (std::string)
```

*(Those are mangled type names. `nm -C` and `c++filt` demangle them, as in Lecture 01 §4.)*

**Deduction is a matching process, not a conversion process.** The compiler takes the parameter
*pattern* — here `T` and `T` — and finds the `T` that makes it fit the arguments. That distinction
matters immediately.

### 3.1 Deduction Can Fail

```cpp
maxof(3, 7.5);      // T = int? or T = double?
```

```
error: no matching function for call to 'maxof(int, double)'
```

Both parameters are declared `T`, so `T` would have to be `int` and `double` at once. **The compiler
will not pick one and convert the other** — that is what "matching, not converting" means. Ordinary
overload resolution would happily convert `3` to `3.0`; template deduction refuses.

Three ways out:

```cpp
maxof<double>(3, 7.5);            // 1. say what T is; the 3 then converts
maxof(3.0, 7.5);                  // 2. make the arguments agree
template <typename T, typename U> // 3. give them separate parameters
auto maxof(T a, U b) -> ...       //    (harder: what is the return type?)
```

**Option 1 is usually right.** Once you supply `T` explicitly, the parameters have concrete types and
normal conversion rules apply — verified: `maxof<double>(3, 7.5)` returns `7.5`.

### 3.2 Explicit Arguments Are Sometimes Required

Deduction only sees the *arguments*. A parameter that appears nowhere in the parameter list cannot be
deduced:

```cpp
template <typename Out, typename In>
Out convert(In value) { return static_cast<Out>(value); }

convert<double>(42);      // Out = double (explicit), In = int (deduced)
```

**Note the parameter order.** Explicit arguments fill the list left to right, so anything that must be
given explicitly should come **first**. Declaring `template <typename In, typename Out>` would force
callers to write `convert<int, double>(42)` and spell out the thing the compiler already knew.

---

## 4. What Actually Gets Compiled

This is the central fact of the week.

**A template is not code. It is a recipe for generating code.** Nothing is compiled until you use it,
and using it with a new type generates a new function.

```cpp
template <typename T>
T maxof(T a, T b) { return a > b ? a : b; }

template int    maxof<int>(int, int);          // explicit instantiation
template double maxof<double>(double, double);
template long   maxof<long>(long, long);
```

One definition, three functions. `nm` on the object file:

```
W int    maxof<int>(int, int)          _Z5maxofIiET_S0_S0_
W double maxof<double>(double, double) _Z5maxofIdET_S0_S0_
W long   maxof<long>(long, long)       _Z5maxofIlET_S0_S0_
```

Read the mangled names: `_Z5maxof` then **`Ii`**, **`Id`**, **`Il`** — the template argument is encoded
in the symbol. These are three unrelated functions that happen to have been written by the same recipe.

### 4.1 The Symbols Are Weak

Look at the `W` column. Lecture 03 §4 established that `T` is a strong symbol and `W` is weak, and that
`inline` is what produces a weak symbol.

**Template instantiations are weak for exactly the same reason.** A template lives in a header,
included by many translation units, each of which instantiates its own copy of `maxof<int>`. If those
were strong symbols the linker would reject the duplicates, as it did for the non-`inline` function in
Lecture 03 §4.1. Weak symbols let it merge them.

> **Templates obey the One Definition Rule by being exempt from it in the same way `inline` is.** This
> is not a special case bolted on for templates; it is the mechanism you already met, reused.

### 4.2 The Cost Is Zero

Compare the template instantiation with a hand-written function:

```cpp
template <typename T> T maxof(T a, T b) { return a > b ? a : b; }
int maxof_int(int a, int b) { return a > b ? a : b; }
```

At `-O2`:

```asm
maxof<int>(int, int):          maxof_int(int, int):
        endbr64                        endbr64
        cmp     edi, esi               cmp     edi, esi
        mov     eax, esi               mov     eax, esi
        cmovge  eax, edi               cmovge  eax, edi
        ret                            ret
```

**Byte for byte identical.** This is what "zero-overhead abstraction" means, and it is checkable in
thirty seconds rather than taken on faith.

The reason is structural: by the time the optimizer runs, there is no template left. There is a
function taking two `int`s. **The genericity was consumed at compile time.**

---

## 5. What `T` Must Support

`maxof` uses `>`. So `T` must have `operator>`:

```cpp
struct NoLess { int x; };
NoLess a{1}, b{2};
maxof(a, b);
```

```
error: no match for 'operator>' (operand types are 'NoLess' and 'NoLess')
```

**This is the whole type system of templates, and it is unusual.** The template does not declare what
`T` needs. It just uses `T`, and the requirements are whatever the body happens to do. If the body
compiles for your type, your type qualifies.

This is often called **duck typing at compile time**, and it is genuinely both:

- Like Python's duck typing, the requirement is implicit and structural — *"has `>`"*, not *"implements
  interface Comparable"*.
- Unlike Python, it is checked **at compile time**, for every instantiation, before the program runs.

The cost is that the requirement is undocumented and the error appears at the point of *use* rather
than the point of *definition*. Lecture 09 §5 measures what that does to error messages.

> **C++20 added `concepts`**, which let you state the requirement:
> `template <std::totally_ordered T> T maxof(T, T);` — and the error then names the unmet requirement
> instead of unwinding the template. **This course is C++17 and you cannot use them**, but this is the
> single biggest improvement to templates since they were introduced, and it is worth knowing what the
> problem was.

---

## 6. Templates and Overloads Together

A template and an ordinary function can share a name. The rule, simplified to what you need this week:

> **An exact match with a non-template function wins. Otherwise the template is used.**

```cpp
template <typename T> void f(T)      { /* template */ }
                      void f(int)    { /* non-template */ }

f(42);     // the non-template: exact match
f(4.2);    // the template, T = double
```

The reasoning is that a non-template function is a deliberate, specific choice by a programmer, and a
template is a fallback for everything else. If you write a specific version, you meant it.

This is how you provide a fast path for one type while keeping the generic version:

```cpp
template <typename T> void swap_them(T& a, T& b) { T t = a; a = b; b = t; }
                      void swap_them(BigThing& a, BigThing& b) { a.swap(b); }
```

---

## 7. A Practical Point About Parameters

`maxof(T a, T b)` takes its parameters **by value**. Week 1 §L06 measured what that costs: two copy
constructions and two destructions per call for a class type.

The generic version should usually take `const T&`:

```cpp
template <typename T>
const T& maxof(const T& a, const T& b) { return a > b ? a : b; }
```

**And that introduces a bug**, which is worth seeing now:

```cpp
const int& r = maxof(3, 7);      // both arguments are temporaries
                                 // r dangles the moment the statement ends
```

Returning `const T&` is correct when the arguments outlive the call and dangerous when they do not. The
standard library's `std::max` has exactly this signature and exactly this trap.

**This time the tools do catch it.** Under the course build line:

```
warning: possibly dangling reference to a temporary [-Wdangling-reference]
note: the temporary was destroyed at the end of the full expression 'maxof<int>(3, 7)'
```

and at runtime:

```
ERROR: AddressSanitizer: stack-use-after-scope
```

> **Contrast this with Week 1 §L05 §9**, where `-Wall -Wextra` compiled a Rule of Three violation in
> total silence. Here the same flags name the bug, the temporary, and the expression that destroyed it.
>
> **The difference is not that one bug is worse.** It is that a dangling reference to a temporary is a
> *local, syntactic* pattern the compiler can recognise in one expression, whereas "this class owns
> something" is a fact about intent that appears nowhere in the source. **The compiler catches what is
> visible in the code, and ownership is not.** That is the whole argument for Week 5.
>
> *(`-Wdangling-reference` is new in GCC 13. On an older compiler you will get silence here, which is
> worth checking on your own machine.)*

**For this week, take by value for small types and `const T&` for large ones, and return by value.**
Week 5's move semantics gives the general answer.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| `template <typename T>` | Introduces a type parameter |
| `typename` vs `class` | Identical here; this course uses `typename` |
| Deduction | The compiler matches the parameter pattern against the arguments |
| Deduction **matches**, does not convert | `maxof(3, 7.5)` is an error, not a promotion |
| Explicit arguments | `maxof<double>(3, 7.5)`; put non-deducible parameters first |
| Instantiation | One template, one symbol **per type used** — `Ii`, `Id`, `Il` |
| Instantiations are **weak** symbols | Same mechanism as `inline`, from L03 §4 |
| Zero runtime cost | `maxof<int>` is byte-identical to the hand-written function |
| Requirements on `T` are implicit | Whatever the body uses. Compile-time duck typing |
| Template vs overload | An exact non-template match wins |

---

## 9. Exercises

**1.** Write `template <typename T> T sum(const T* arr, int n)`. Instantiate it for `int` and `double`
using explicit instantiation, and show with `nm` that you produced two symbols. **Identify the type
argument in each mangled name.**

**2.** Compile your `sum<int>` alongside a hand-written `sum_int` at `-O2` and compare the assembly.
**Report whether they are identical**, and if not, exactly how they differ.

**3.** Call `maxof(3, 7.5)` and paste the error. Then fix it three different ways, and say in one
sentence which you would use in real code and why.

**4.** Write a `struct` with no comparison operators and pass it to `maxof`. Paste the error. Now add
**only** `operator>` and show it compiles. **What does this tell you about how template requirements
are declared?**

**5.** Write `template <typename Out, typename In> Out convert(In)`. Call it as `convert<double>(42)`.
Now swap the two template parameters in the declaration and show what callers must write instead.

**6.** Given both `template <typename T> void f(T)` and `void f(int)`, predict which is called for
`f(42)`, `f(42L)`, `f('a')` and `f(4.2)`. **Verify with a print in each.**

**7.** Write the `const T&` version of `maxof` from §7 and demonstrate the dangling reference. Run it
under `-fsanitize=address` and paste what it says.

---

## 10. Next

**Lecture 08** applies all of this to classes: `Stack<T>`, with the full Rule of Three written once.
Along the way it answers the question that catches everyone — **why must a template's definitions live
in the header?** — and the answer follows directly from §4 of this lecture.

---

*PROG 102 · Week 2 · Lecture 07 · © CSE Department*
