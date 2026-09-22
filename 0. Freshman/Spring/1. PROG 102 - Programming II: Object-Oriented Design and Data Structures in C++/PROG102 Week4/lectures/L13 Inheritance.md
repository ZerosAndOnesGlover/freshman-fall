# PROG 102 · Lecture 13
## Inheritance

**Week 4 · Tuesday · 50 minutes**
**Reading:** *C++ Primer* §15.1–15.3 · **Reference:** Stroustrup Ch. 20
**Assumes:** Week 0 (classes, access control, construction order)

**Date:** Tuesday 16 February 2027 · 10:00–10:50 · Week 4

---

## 1. Syntax

```cpp
class Shape {
protected:
    std::string label;
public:
    explicit Shape(std::string l) : label(std::move(l)) {}
    double area() const { return 0; }
};

class Square : public Shape {          // Square derives publicly from Shape
    double side;
public:
    Square(std::string l, double s) : Shape(std::move(l)), side(s) {}
    double area() const { return side * side; }
};
```

A `Square` **contains** a complete `Shape` sub-object, and adds `side` to it. It inherits every member
of `Shape` — data and functions — subject to access rules.

**The base is initialized in the derived constructor's initializer list**, before any derived member.
This is Lecture 02 §3 extended: the base sub-object is just another thing that must be initialized,
and it goes first.

If you do not name the base, its **default constructor** is called; if it has none, you get an error
telling you so.

---

## 2. Is-A Versus Has-A

The design question that decides whether to inherit at all.

| Relationship | Mechanism | Test |
| --- | --- | --- |
| **is-a** | inheritance | *Every* `Square` is a `Shape`, everywhere a `Shape` is expected |
| **has-a** | composition (a member) | A `Car` has an `Engine`; it is not one |

```cpp
class Car { Engine engine; };            // has-a: composition
class Square : public Shape { };          // is-a: inheritance
```

**The test is substitutability, not vocabulary.** Ask: can code written against the base, which has
never heard of your derived class, use it correctly? If not, it is not an is-a relationship however
natural the English sounds.

### 2.1 The Classic Counterexample

A `Square` is a `Rectangle` in mathematics. In code:

```cpp
class Rectangle { public: virtual void setWidth(double); virtual void setHeight(double); };
class Square : public Rectangle { ... };     // ???
```

A function taking `Rectangle&` may reasonably set the width to 3 and the height to 4 and expect an
area of 12. **A `Square` cannot honour that** — setting either dimension must change both.

The inheritance compiles and the design is wrong. This is the **Liskov Substitution Principle**, and
the practical form of it is the test above: *code written against the base must keep working.*

> **Prefer composition.** This is the Gang of Four's central advice (**Week 7**), and the reason is
> that inheritance is the tightest coupling C++ offers — the derived class depends on the base's
> interface, its protected members, and its invariants. Composition depends only on a public
> interface.
>
> Reach for inheritance when you need **runtime polymorphism**: a collection of things with a common
> interface whose concrete types are not known at the point of use. That is Lecture 14's subject and
> it is the case inheritance is genuinely for.

---

## 3. Access Specifiers, Again

Lecture 03 gave you `public`, `private` and the deferred `protected`. Now it matters.

```cpp
class Shape {
private:   double cached;      // Shape only
protected: std::string label;  // Shape AND derived classes
public:    double area() const;// anybody
};
```

**`protected` is the "derived classes may touch this" level.** It exists for the case where a derived
class genuinely needs the base's state.

> **Use it sparingly.** A `protected` member is part of your interface to every class that will ever
> derive from you, and you cannot change it later without breaking them. Many codebases treat
> `protected` *data* as a mistake and use `protected` accessor functions instead — the state stays
> private, and derived classes get a contract you can keep.

### 3.1 Inheritance Can Itself Be public, protected or private

```cpp
class D1 : public    B { };    // is-a. B's public stays public
class D2 : protected B { };    // B's public becomes protected in D2
class D3 : private   B { };    // B's public becomes private in D3
```

| | base's `public` becomes | base's `protected` becomes | Is `D*` usable as a `B`? |
| --- | --- | --- | --- |
| `public` | public | protected | **Yes** |
| `protected` | protected | protected | Only inside `D` and its derived |
| `private` | private | private | Only inside `D` |

**Use `public` inheritance.** It is the only one that means is-a, and it is what every reader assumes.

`private` inheritance means "implemented in terms of", which is a thing composition also does, more
clearly. If you catch yourself writing it, ask whether a member would do.

> **`class` defaults to `private` inheritance and `struct` defaults to `public`** — the same single
> difference from Lecture 03 §2, now applied to bases. Since forgetting the keyword silently gives you
> `private` inheritance and a baffling "cannot convert" error, **always write `public` explicitly.**

---

## 4. Construction and Destruction Order

```cpp
struct A { A(); virtual ~A(); };
struct B : A { B(); ~B(); };
struct C : B { C(); ~C(); };

{ C c; }
```

Measured:

```
  A()
  B()
  C()
  ~C()
  ~B()
  ~A()
```

**Construction runs base-first; destruction runs derived-first.** Exactly the reverse-order rule from
Lecture 02 §5.1, applied to sub-objects.

The reason is the same: `B`'s constructor may use `A`'s members, so `A` must be ready. And `B`'s
destructor may use `A`'s members, so `A` must not be gone yet.

### 4.1 Do Not Call Virtual Functions From Constructors or Destructors

During `A`'s constructor, the object **is not yet a `C`** — `C`'s members are uninitialized. So the
language says a virtual call inside `A::A()` dispatches to `A`'s version, not `C`'s.

```cpp
struct A { A() { init(); }  virtual void init() { /* A's version runs */ } };
struct C : A { void init() override { /* NEVER called from A::A() */ } };
```

This compiles, runs, and does the wrong thing silently. **The rule: no virtual calls from constructors
or destructors.** If you need derived-specific setup, do it in the derived constructor or in a separate
`initialize()` the caller invokes.

---

## 5. Name Hiding

A trap that catches everyone once.

```cpp
struct Base { void f(int)    { /* Base::f(int) */ } };
struct Der : Base { void f(double) { /* Der::f(double) */ } };

Der d;
d.f(1);        // which one?
```

Measured:

```
  d.f(1) with an int argument ->  Der::f(double)
```

**`Der::f(double)` runs**, and the `int` is converted. `Base::f(int)` — an exact match — was not
considered at all.

**Declaring *any* `f` in the derived class hides *every* `f` from the base.** Name lookup finds the
derived scope, stops, and only then does overload resolution among what it found.

The fix:

```cpp
struct Der2 : Base { using Base::f; void f(double) { } };
```

```
  e.f(1) with 'using Base::f'  ->  Base::f(int)
```

**`using Base::f;` pulls the base's overloads into scope**, and then normal overload resolution picks
the exact match.

Your build line catches this:

```
warning: 'virtual void Base::draw(int) const' was hidden [-Woverloaded-virtual=]
```

---

## 6. `override` and `final`

```cpp
struct Base { virtual void draw(int) const; virtual void scale(double); };

struct D1 : Base { void draw(int) {} };                  // forgot const
struct D2 : Base { void draw(int) const override {} };   // correct
struct D3 : Base { void scale(int) override {} };        // wrong parameter type
```

`D1` looks like an override and is not — the missing `const` makes it a *different function* (Lecture
03 §3.1: `const` is part of the signature). Without `override` this compiles silently and your
function is never called through a base pointer.

`D3` is marked `override` and does not override:

```
error: 'void D3::scale(int)' marked 'override', but does not override
```

> **Write `override` on every override.** It costs one word and converts a silent behavioural bug into
> a compile error. It also documents intent — a reader can see at a glance that a function is part of
> a hierarchy's interface.

**`final`** stops further overriding, or further derivation:

```cpp
struct Leaf final : Base { void draw(int) const final; };
```

Besides expressing intent, `final` lets the compiler **devirtualize**: if a class is `final`, a call
through a pointer to it cannot dispatch anywhere else. Lecture 14 §5 shows the compiler doing this even
without the keyword.

---

## 7. What Derived Classes Do Not Inherit

Worth knowing, because each one surprises somebody:

- **Constructors** are not inherited by default. Use `using Base::Base;` to inherit them.
- **The destructor** is not inherited; the derived one calls the base's automatically.
- **`operator=`** is not inherited — the derived class gets its own generated one, which calls the
  base's.
- **Friendship** is not inherited or transitive.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| Derived contains a complete base sub-object | Initialized first, in the derived constructor's list |
| **is-a** vs **has-a** | Test substitutability, not English |
| Square/Rectangle | Compiles, and violates the base's contract |
| `protected` | Derived classes may touch it — so it is part of your interface forever |
| Use **`public`** inheritance | The only kind that means is-a; `class` defaults to `private` |
| Order | Construct base-first, destroy derived-first — measured |
| No virtual calls in constructors | The derived part does not exist yet |
| Name hiding | Any `f` in derived hides **all** `f` in base — `d.f(1)` called `f(double)` |
| `using Base::f;` | The fix |
| `override` | Turns a silent bug into a compile error. Always write it |
| `final` | Expresses intent and enables devirtualization |

---

## 9. Exercises

**1.** Build a three-level hierarchy whose constructors and destructors print. **Predict the output
for a stack object, then verify.** Now allocate one with `new` and delete it through a base pointer —
predict again. *(Lecture 15 explains what you see.)*

**2.** Write the `Square`/`Rectangle` hierarchy from §2.1 and a function
`void resize(Rectangle&, double w, double h)` that sets both and asserts the area. **Pass it a
`Square`.** Report what happens, and state which principle was violated.

**3.** Reproduce the name-hiding result: `Base::f(int)`, `Der::f(double)`, then call `d.f(1)`. Report
which runs and quote the warning. Fix it with `using`.

**4.** Take a correct override and delete the `const`. **Does it still compile?** Does the base-pointer
call still reach your function? Now add `override` and report the error.

**5.** Write a class hierarchy where `protected` data leads to a change in the base breaking a derived
class. Then rewrite it with a `protected` accessor and show that the same change is now safe.

**6.** Try `class D : B { };` without `public`, then use a `D*` where a `B*` is expected. Paste the
error and explain it.

**7.** Write a base whose constructor calls a virtual function overridden in the derived class. Print
from both. **Which runs?** Explain in one sentence.

---

## 10. Next

**Lecture 14** answers the question this lecture has avoided: `Square::area()` and `Shape::area()` both
exist — **which one runs when you call through a `Shape*`?** Without `virtual`, the answer is decided
at compile time and is usually not what you want. With it, the object decides, and we go and look at
how.

---

*PROG 102 · Week 4 · Lecture 13 · © CSE Department*
