# PROG 102 · Lecture 09
## Instantiation, Specialization, and What Templates Cost

**Week 2 · Friday · 50 minutes**
**Reading:** *C++ Primer* §16.3, §16.5 · **Reference:** Stroustrup §23.5, Ch. 25
**Assumes:** L07, L08

---

## 1. Instantiation, Precisely

**Instantiation is the compiler writing a class or function for you, on demand, from a template.**

It happens when a use of the template requires the definition — calling `maxof(3, 7)`, declaring a
`Stack<int>`, calling `s.push(...)`. It happens **once per translation unit per set of arguments**, and
the resulting weak symbols are merged by the linker (L07 §4.1).

Two properties follow, and both are useful.

### 1.1 Only What You Use Is Instantiated

For a class template, **member functions are instantiated individually.** A member you never call is
never compiled:

```cpp
template <typename T>
class Stack {
public:
    void push(const T& v) { ... }
    void print() { std::cout << data[0]; }   // requires operator<<
};

Stack<NoPrint> s;    // fine
s.push(x);           // fine
// s.print();        // only THIS would require NoPrint to have operator<<
```

**`Stack<NoPrint>` is a perfectly good type** even though one of its members could not possibly
compile. This is why the standard containers work with types that support very little — you pay only
for the operations you actually use.

### 1.2 Errors Appear at the Point of Use

The flip side. The template body is only fully checked once `T` is known, so a mistake surfaces where
the template is *used*, not where it is *written*:

```cpp
struct NoDefault { int v; explicit NoDefault(int x) : v(x) {} };
Stack<NoDefault> s;
```

```
nodefault.cpp:3:30:   required from here
stack_t.hpp:26:57: error: no matching function for call to 'NoDefault::NoDefault()'
note: candidate: 'NoDefault::NoDefault(int)'
note:   candidate expects 1 argument, 0 provided
```

The error is in **`stack_t.hpp`** — a file the student did not write — and the `required from here`
line is the only thing connecting it back to their code. Hold onto that phrase; §5 is about it.

*(The specific cause here is L08 §4: `new T[n]` default-constructs every element.)*

---

## 2. Specialization

Sometimes the generic implementation is wrong, or merely bad, for one type. **Specialization lets you
override it.**

### 2.1 Full Specialization

```cpp
template <typename T> struct Traits          { static const char* name(){ return "generic"; } };
template <>           struct Traits<int>     { static const char* name(){ return "int"; } };
```

`template <>` with the argument in the class name means: *for this exact type, use this instead.*

### 2.2 Partial Specialization

```cpp
template <typename T> struct Traits<T*>      { static const char* name(){ return "pointer"; } };
```

This matches **any pointer type**, with `T` bound to the pointee. Verified:

```
Traits<double> : generic
Traits<int>    : int (full specialization)
Traits<char*>  : pointer (partial specialization)
```

The compiler picks the **most specialized** match: `Traits<int*>` would choose the pointer version over
the generic one, and `Traits<int>` chooses the full specialization over both.

> **Partial specialization works for class templates only, not function templates.** For functions you
> use overloading instead (L07 §6), which achieves the same thing by a different mechanism. This is a
> genuine language wart and it catches people.

### 2.3 What It Is For

The standard library's most famous specialization is **`std::vector<bool>`**, which packs its elements
one per *bit* instead of one per `bool`.

It is also widely considered a mistake — `std::vector<bool>` does not behave like other vectors
(`operator[]` returns a proxy object, not a `bool&`), so generic code that works for
`std::vector<T>` can break for `T = bool`. **Week 3 returns to this.** It is the standard cautionary
example: a specialization that improves space and quietly breaks the type's contract.

**Use specialization when a type genuinely needs different logic. Do not use it to make one type
faster at the cost of behaving differently**, which is exactly what `vector<bool>` did.

---

## 3. What Instantiation Costs

Every instantiation generates its own code. So what does that cost? Three measurements.

### 3.1 Runtime: Nothing

Lecture 07 §4.2 showed `maxof<int>` byte-identical to a hand-written function. The same holds for class
templates. Comparing `TStack<int>` with a hand-written `IStack`, both compiled at `-O2`:

| Function | Result |
| --- | --- |
| `TStack<int>::push` vs `IStack::push` | **Identical**, 11 instructions |
| `TStack<int>::pop` vs `IStack::pop` | **Identical**, 8 instructions |

And end to end, pushing and popping 1024 `int`s twenty thousand times:

```
TStack<int> (template)    27.86 ms
IStack (hand-written)     27.37 ms
```

Repeated runs put the two within noise of each other. **There is no runtime cost, because there is no
template at runtime.**

### 3.2 Code Size and Compile Time: Linear

Instantiating one `Stack<T>` for *N* distinct element types:

| types | compile (s) | text (bytes) |
| --- | --- | --- |
| 1 | 0.16 | 2,776 |
| 5 | 0.18 | 4,477 |
| 10 | 0.25 | 6,551 |
| 25 | 0.42 | 12,802 |
| 50 | 0.75 | 23,199 |
| 100 | 1.55 | 43,993 |

Both grow **linearly** — about **416 bytes of machine code and 14 milliseconds of compile time per
additional instantiation.** This is real, and in a large codebase it is why builds take minutes.

### 3.3 The Claim That Is Wrong

This growth is universally called **template code bloat**, with the implication that templates caused
it. So write the same 100 classes out by hand and compare:

| | compile | text |
| --- | --- | --- |
| `Stack<T>` instantiated for 100 types | 1.55 s | **43,993 bytes** |
| 100 hand-written classes, no templates | 1.84 s | **43,993 bytes** |

**Byte for byte identical.** And the hand-written version took *longer* to compile.

> **Templates did not bloat anything.** One hundred types that each need their own `push`, `pop`, copy
> constructor and destructor require one hundred copies of that code — in any language, by any
> mechanism, including copy and paste. The template is not the cause; it is the reason you could ask
> for a hundred instantiations by writing three lines and never noticing.

The engineering advice that actually follows is not "avoid templates". It is:

- **Know how many instantiations you are creating.** `Stack<int>` and `Stack<const int>` and
  `Stack<int*>` are three.
- **Do not template things that do not vary.** If a member function does not use `T`, it can live in a
  non-template base class and be shared by every instantiation. *(This is a real technique, sometimes
  called the "thin template" idiom.)*
- **Watch non-type parameters.** `FixedArray<int,8>` and `FixedArray<int,9>` are separate
  instantiations, and a template parameterised on a size can quietly produce dozens.

---

## 4. Compared With Other Languages

The docx puts it well: templates are *fundamentally different* from generics elsewhere. Precisely how:

| | When is the type known? | One implementation or many? | Cost |
| --- | --- | --- | --- |
| **C++ templates** | Compile time | **Many** — one per instantiation | Compile time and code size; **zero at runtime** |
| **Java generics** | Compile time, then **erased** | **One**, operating on `Object` | Runtime casts; no code growth |
| **Python** | Runtime (duck typing) | One | Runtime type lookup on every operation |

**Java's type erasure** means `List<String>` and `List<Integer>` are the same class at runtime, with
casts inserted. That is why Java cannot have `List<int>` (only boxed `Integer`), why you cannot write
`new T[10]`, and why generic code cannot be specialised per type. It also means no code growth and
fast compiles.

**C++ generates real code per type**, so `Stack<int>` stores actual `int`s with no boxing, `sizeof`
works, specialization is possible, and the optimizer sees concrete types. The bill arrives at compile
time.

**Python checks nothing until it runs.** `maxof(a, b)` works for anything with `>`, and finds out at
runtime — which is the same *structural* requirement as a C++ template (L07 §5), differing only in
when it is checked.

> **The C++ position is: pay at compile time, so that runtime is free.** That is a coherent choice
> rather than an obviously correct one, and the two costs it produces — build times and error messages
> — are the price. Every subsequent language has picked a different point on this trade-off.

---

## 5. Error Messages, Measured

Templates are notorious for this. Here is the actual scale, measuring the *same conceptual mistake* —
a type used where `<` is required — at three depths:

| Error | lines | characters |
| --- | --- | --- |
| Plain type error (`int x = "hello";`) | 6 | 287 |
| Direct template (`maxof` on a type with no `>`) | **5** | 380 |
| Through the STL (`std::sort` on a type with no `<`) | **78** | **10,455** |

**Note the middle row.** A one-level-deep template error is *no worse* than an ordinary one. Templates
are not intrinsically verbose.

**The 78-line message comes from depth.** `std::sort` calls `__sort`, which calls
`__introsort_loop`, which calls `__unguarded_partition_pivot`, and the error surfaces inside
`predefined_ops.h` — a header nobody wrote by hand. Each frame in that stack is another
`required from here`.

### 5.1 How to Read One

The first three lines of the 78 are:

```
In file included from /usr/include/c++/13/bits/stl_algobase.h:71,
                 from /usr/include/c++/13/vector:62,
                 from err_stl.cpp:1:
```

Pure noise. The line that matters is:

```
/usr/include/c++/13/bits/predefined_ops.h:45:23: error: no match for 'operator<'
                                                 (operand types are 'NoLess' and 'NoLess')
```

**Three rules, and they will save you hours this semester:**

1. **Read the *first* error, not the last.** Later errors are usually consequences.
2. **Search for the first line naming *your* type or *your* file.** In a wall of `std::` and `__`
   symbols, `NoLess` is the signal.
3. **Look for `required from here`** — that is the instantiation backtrace, and following it upward
   takes you from the library's internals to the line you wrote.

The actual fix here is one line: give `NoLess` an `operator<`.

> **C++20 concepts largely solve this**, by letting the template state its requirement so the compiler
> can report *"`NoLess` does not satisfy `totally_ordered`"* instead of unwinding four levels of
> library internals. **You cannot use them in this C++17 course**, but you should know that the
> problem you are about to spend a semester working around has since been fixed.

---

## 6. Variadic Templates — A Preview

A template can take **any number** of arguments:

```cpp
template <typename... Args>
void print_all(const Args&... args);
```

`Args` is a **parameter pack**. This is how `std::make_tuple`, `std::vector::emplace_back` and
`printf`-style type-safe formatting are written.

You are not required to write variadic templates in this course. You should recognise the `...` and
know it means "zero or more". **Week 11** uses them for perfect forwarding.

---

## 7. Why Templates Enable the STL

This is the week's destination and Week 3's starting point.

`std::sort` does not know what it is sorting. It requires **random-access iterators** and
**`operator<`** — nothing else. `std::vector<T>` stores any `T`. `std::find` works on any container
providing forward iterators.

**None of this is possible without a mechanism that generates real, type-specific code from one
description.** With Java-style erasure you cannot sort `int`s without boxing them. With C's `void*`
you lose every type check and every optimization. **Templates are what make an algorithm library
possible that is simultaneously generic and as fast as hand-written code**, and Week 3 is about the
library that resulted.

The design has one further move, which is the genuinely brilliant part: **algorithms are separated
from containers by iterators.** `std::sort` never mentions `std::vector`. That decoupling is Lecture
10's subject.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| Instantiation | The compiler writes the function or class on demand |
| Members instantiate individually | An uncalled member need not even be compilable |
| Errors appear at the point of **use** | Reported inside headers you did not write |
| Full specialization | `template <> struct Traits<int>` |
| Partial specialization | `template <typename T> struct Traits<T*>`; **classes only** |
| `std::vector<bool>` | The cautionary example: faster, and breaks the contract |
| Runtime cost | **Zero.** Identical instructions, identical timings |
| Compile/size cost | Linear: ~416 bytes and ~14 ms per instantiation |
| **"Template bloat" is misattributed** | 100 hand-written classes: **the same 43,993 bytes** |
| vs Java | Java erases to one implementation; C++ generates many |
| vs Python | Same structural requirement, checked at compile time instead of runtime |
| Error messages | 5 lines one level deep; **78 lines** through the STL |
| Reading them | First error · first mention of your type · `required from here` |

---

## 9. Exercises

**1.** Write a class template with a member function that could not compile for your chosen `T`.
Instantiate the class, call every *other* member, and show it builds. **Then call the bad one** and
paste the error.

**2.** Write `Traits<T>` with a generic version, a full specialization for `double`, and a partial
specialization for `T*`. Predict the output for `Traits<int>`, `Traits<double>`, `Traits<double*>` and
`Traits<int**>` **before running it.**

**3.** Reproduce the table in §3.2 on your machine for at least four values of *N*. **Compute the bytes
per instantiation.** Does it grow linearly for you?

**4.** Reproduce §3.3: write out by hand the classes your template generated, and compare `size` output.
**Report both numbers.** If they differ on your machine, investigate why before concluding the lecture
is wrong.

**5.** Trigger the `std::sort` error from §5 and count the lines yourself. **Find the one line that
identifies the real problem**, and quote it. How far down is it?

**6.** Someone proposes banning templates in a project "because of code bloat". Using §3.3, write a
three-sentence reply that is fair to their concern and corrects the attribution.

**7.** Explain in two sentences why Java can have `ArrayList<Integer>` but not `ArrayList<int>`, and why
C++ has no such restriction. Refer to §4.

---

## 10. Next

**Week 3** hands you the library this week made possible: `vector`, `map`, `set`, iterators, and the
algorithms that work with all of them. You will find that `std::vector` is `Stack<T>` done properly,
and that most of what you wrote this fortnight already existed and was better.

**That is the intended order.** You now know what `vector` is doing, what it cost to build, and why its
interface looks the way it does — which is not something you could have been told.

---

*PROG 102 · Week 2 · Lecture 09 · © CSE Department*
