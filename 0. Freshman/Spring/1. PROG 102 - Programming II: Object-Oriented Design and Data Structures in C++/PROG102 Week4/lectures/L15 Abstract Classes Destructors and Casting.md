# PROG 102 · Lecture 15
## Abstract Classes, Virtual Destructors, and Casting

**Week 4 · Thursday · 50 minutes**
**Reading:** *C++ Primer* §15.4, §15.7, §19.2 · **Reference:** Stroustrup §20.4, §22.2
**Assumes:** L13, L14

**Date:** Thursday 18 February 2027 · 10:00–10:50 · Week 4

---

## 1. Pure Virtual Functions

```cpp
struct Shape {
    virtual double area() const = 0;      // pure virtual
    virtual ~Shape() = default;
};
```

`= 0` means **there is no sensible base implementation; every derived class must supply one.**

A class with at least one pure virtual function is **abstract** and cannot be instantiated:

```
error: cannot declare variable 's' to be of abstract type 'Shape'
note:   because the following virtual functions are pure within 'Shape'
```

**Abstractness is inherited.** A derived class that does not override every pure virtual is *also*
abstract:

```cpp
struct Incomplete : Shape { };     // still abstract -- area() not overridden
```

```
error: cannot declare variable 'i' to be of abstract type 'Incomplete'
```

You can still have `Shape*` and `Shape&`. **That is the entire point** — the abstract class exists to
be pointed at.

### 1.1 An Abstract Class Is an Interface

```cpp
struct Drawable {
    virtual void draw(Canvas&) const = 0;
    virtual ~Drawable() = default;
};
```

No data, no implementations, just a contract. This is C++'s equivalent of Java's `interface`, and it is
what nearly every design pattern in **Weeks 7 and 8** is built from.

**A class may inherit from several such interfaces**, which is the well-behaved use of multiple
inheritance.

### 1.2 A Pure Virtual May Still Have a Body

Surprising and occasionally useful:

```cpp
struct Shape {
    virtual double area() const = 0;
    virtual ~Shape() = default;
};
double Shape::area() const { /* shared implementation */ return 0; }

struct Sq : Shape {
    double area() const override { Shape::area(); return s * s; }   // explicit call
};
```

```
  Shape::area() base implementation ran
  area = 9.0
```

`= 0` means "derived classes must override", **not** "there is no implementation". The body can only be
called explicitly with the `Shape::` qualification, and it is a way to share common code while still
forcing every derived class to think about the function.

**This is required for the destructor** if you want a pure virtual destructor — the base's destructor
is always called, so it must exist:

```cpp
virtual ~Shape() = 0;
Shape::~Shape() {}          // and it MUST be defined
```

---

## 2. The Virtual Destructor Rule

> **If a class may be deleted through a pointer to a base, that base's destructor must be `virtual`.**

Here is what happens when it is not. `DerNV` allocates an `int[100]`; the base's destructor is not
virtual:

```cpp
BaseNV* b = new DerNV;
delete b;
```

Measured:

```
non-virtual destructor, delete through base*:
  ~BaseNV
ERROR: AddressSanitizer: new-delete-type-mismatch
```

**`~DerNV` never ran.** The `int[100]` leaked. `delete` consulted the *static* type of the pointer —
`BaseNV` — and that type's destructor knows nothing about a derived part.

With `virtual`:

```
virtual destructor, delete through base*:
  ~DerV
  ~BaseV
```

Correct, and in the right order (L13 §4).

### 2.1 Why It Works

L14 §4 showed the destructor sitting in the vtable:

```
(gdb) p ((void***)&sq)[0][2]
$3 = (void *) 0x555555555496 <Square::~Square()>
```

A virtual destructor is dispatched like any other virtual function: `delete` loads the vptr, finds the
*derived* destructor, runs it, and it then runs the base's. Without `virtual`, there is no lookup and
the compiler calls what it can see.

### 2.2 When Your Compiler Warns, Exactly

This is worth getting precise, because the answer is "sometimes".

| Base class | `-Wall -Wextra` |
| --- | --- |
| Has a virtual function, non-virtual destructor | **Warns** |
| Has **no** virtual functions, non-virtual destructor | **Silent** |

The warning, when it fires:

```
warning: deleting object of polymorphic class type 'B2' which has non-virtual destructor
         might cause undefined behavior [-Wdelete-non-virtual-dtor]
```

**`-Wdelete-non-virtual-dtor` is part of `-Wall`** — so your normal build line catches the common case.

But it only fires for a class the compiler already considers **polymorphic**. A base with no virtual
functions at all, deleted through a base pointer, produces **nothing** — and that is precisely the case
where you forgot `virtual` entirely rather than forgetting it on the destructor.

> **The stricter flag is `-Wnon-virtual-dtor`**, which warns on the *class definition* rather than the
> delete site:
>
> ```
> warning: 'struct B2' has virtual functions and accessible non-virtual destructor
> ```
>
> It is not in `-Wall`. Adding it is cheap and catches the problem in the header rather than at every
> use.

### 2.3 The Rule in Practice

**Every class you intend to derive from gets a `virtual` destructor.** The cost is 8 bytes per object
(L14 §3.1) and it is not worth reasoning about whether someone might one day `delete` through a base
pointer.

The alternative, when you genuinely do not want the vptr, is to make the destructor **`protected` and
non-virtual** — then `delete b;` through a base pointer does not compile, which is a compile error
instead of a leak.

---

## 3. Object Slicing

```cpp
void by_value(Shape s);          // takes a Shape BY VALUE
void by_ref  (const Shape& s);

Sq q(3.0);
by_value(q);
by_ref(q);
```

Measured:

```
by value    : Shape area=0.00
by reference: Sq    area=9.00
```

**Passing by value copied only the `Shape` part.** The `side` member and — crucially — the *vptr* are
the derived object's; the copy is a `Shape`, with `Shape`'s vptr, and virtual dispatch now finds
`Shape::area`.

The object was **sliced**: the derived part was cut off.

### 3.1 In Containers

```cpp
std::vector<Shape>  sliced;   sliced.push_back(Sq(3.0)); sliced.push_back(Ci(1.0));
std::vector<Shape*> ptrs;     ptrs.push_back(&a);        ptrs.push_back(&b);
```

```
vector<Shape> : Shape(0.00) Shape(0.00)
vector<Shape*>: Sq(9.00)    Ci(3.14)
```

**A `std::vector<Shape>` cannot hold a `Square`.** It holds `Shape`s, so every element is sliced on the
way in. This compiles without a warning and silently discards your program's meaning.

*(It is also why the abstract version is safer: `std::vector<Shape>` where `Shape` is abstract does not
compile at all, because you cannot create a `Shape`. Making the base abstract converts this silent bug
into an error.)*

### 3.2 Avoiding It

- **Pass polymorphic types by reference or pointer, never by value.**
- **Store `std::vector<std::unique_ptr<Base>>`** (Week 5), not `std::vector<Base>`.
- **Make the base abstract** where you can — it turns the mistake into a compile error.
- If a base must not be copied at all, `= delete` its copy constructor and assignment (L05 §4.1).

---

## 4. Casting in a Hierarchy

**Upcasting** — derived to base — is implicit, always safe, and needs no cast:

```cpp
Sq q(3.0);
Shape* p = &q;              // fine
```

**Downcasting** — base to derived — is where you need to be careful.

### 4.1 `static_cast` Is Unchecked

```cpp
D2 obj;
B* p = &obj;
D1* bad = static_cast<D1*>(p);      // compiles. p does not point to a D1.
```

```
static_cast<D1*> on a D2 : 0x7fff...  -> reading it is UB, a=222
```

**`a` printed 222**, which is the value of `D2::b`. The cast reinterpreted the object, and reading
`bad->a` read `D2`'s member through `D1`'s offset. No error, no warning, plausible-looking garbage.

### 4.2 `dynamic_cast` Is Checked

```cpp
D1* good = dynamic_cast<D1*>(p);    // p points to a D2
```

```
dynamic_cast<D1*> on a D2: nullptr (correct)
```

**`dynamic_cast` consults the object's `type_info`** — reachable through the vptr, which is why it
requires a polymorphic type — and returns `nullptr` when the cast is invalid.

For references there is no null to return, so it **throws `std::bad_cast`**.

The idiomatic form:

```cpp
if (auto* sq = dynamic_cast<Square*>(shape)) {
    // definitely a Square here
}
```

### 4.3 What It Costs

Measured over 10,000,000 objects:

| | time | vs virtual call |
| --- | --- | --- |
| virtual call | 19.0–22.2 ms | 1.0× |
| `dynamic_cast` | 53.3–61.4 ms | **≈2.8×** |

`dynamic_cast` walks a run-time type hierarchy; a virtual call indexes an array. **Roughly three times
the cost of a virtual call**, which is still small in absolute terms — but it is not free, and it
scales with the depth of the hierarchy.

### 4.4 Needing It Is Usually a Design Smell

```cpp
if (auto* s = dynamic_cast<Square*>(shape))      { /* ... */ }
else if (auto* c = dynamic_cast<Circle*>(shape)) { /* ... */ }
```

**That chain is a `switch` on type, which is what virtual functions exist to replace.** Every time you
add a shape you must find and edit every chain. The virtual version needs no edit at all.

> **Ask first: could this be a virtual function?** Usually it can, and the answer is to add one to the
> base rather than to interrogate the type at the call site.
>
> **Legitimate uses exist:** recovering a concrete type at a boundary you do not control, implementing
> a `visit`-like dispatch, or safe downcasting in a plugin system. In Week 8 the **Visitor pattern**
> is the principled solution to genuinely needing per-type behaviour that does not belong in the class.

### 4.5 The Four Casts, Summarised

| Cast | Use | Checked? |
| --- | --- | --- |
| `static_cast` | Related types, upcasts, numeric conversions | **No** |
| `dynamic_cast` | Downcast in a polymorphic hierarchy | **Yes** — `nullptr` or `bad_cast` |
| `const_cast` | Add or remove `const` | No. Removing `const` from a genuinely `const` object is UB |
| `reinterpret_cast` | Bit reinterpretation | No. Almost always wrong outside systems code |

---

## 5. Summary

| Idea | The point |
| --- | --- |
| `= 0` | Abstract; cannot be instantiated. Abstractness is inherited |
| A pure virtual may have a body | Callable only with explicit qualification |
| Abstract class = interface | The basis of nearly every pattern in Weeks 7–8 |
| **Virtual destructor rule** | Verified: without it, `~DerNV` never runs and ASan reports `new-delete-type-mismatch` |
| The warning | `-Wall` catches it **only if the base is already polymorphic**; otherwise silence |
| `-Wnon-virtual-dtor` | Stricter, not in `-Wall`, warns at the class rather than the delete |
| Slicing | `by_value` gave `Shape area=0.00`; `vector<Shape>` sliced every element |
| Making the base abstract | Turns the slicing bug into a compile error |
| `static_cast` down | Unchecked — read `D2::b` as `D1::a` and printed 222 |
| `dynamic_cast` | Checked, `nullptr` on failure, **≈2.8×** a virtual call |
| A `dynamic_cast` chain | A `switch` on type. Usually wants to be a virtual function |

---

## 6. Exercises

**1.** Make `Shape::area()` pure virtual and try to create a `Shape`. Paste the error. Then derive a
class that does *not* override it and try to create that. **Paste that error too.**

**2.** Give a pure virtual function a body and call it from an override. Show the base implementation
running.

**3.** Reproduce the virtual destructor leak. Report what runs, what ASan says, and how many bytes
leak. **Then determine, on your compiler, exactly when the warning fires** — try both a base with a
virtual function and a base without.

**4.** Write a `Base` whose destructor is `protected` and non-virtual, and show that `delete b;`
through a base pointer does not compile. **When would you want this?**

**5.** Demonstrate slicing three ways: by-value parameter, assignment to a base variable, and
`std::vector<Base>`. Then make the base abstract and show which of the three now fail to compile.

**6.** Downcast a `D2*` to a `D1*` with `static_cast` and read a member. **Report the garbage value and
explain where it came from.** Then do it with `dynamic_cast`.

**7.** Write a `dynamic_cast` chain over three shape types, then rewrite it as a virtual function.
**Count the lines that must change when you add a fourth shape**, for each version.

---

## 7. Next

**Week 5** is memory management and RAII — `unique_ptr`, `shared_ptr`, `weak_ptr` and move semantics.
It answers the question §3.2 raised: `std::vector<Base*>` avoids slicing but leaves you deleting
everything by hand. `std::vector<std::unique_ptr<Base>>` does not.

**MIDTERM 1 is Tuesday 2 March, 18:00** (Week 6) and covers Weeks 0–4. The revision guide is in `resources/` — start now, not
next Sunday.

---

*PROG 102 · Week 4 · Lecture 15 · © CSE Department*
