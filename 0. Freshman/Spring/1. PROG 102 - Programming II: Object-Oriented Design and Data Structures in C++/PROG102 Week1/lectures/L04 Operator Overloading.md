# PROG 102 · Lecture 04
## Operator Overloading

**Week 1 · Monday · 50 minutes**
**Reading:** *C++ Primer* Ch. 14 · **Reference:** Stroustrup Ch. 18
**Assumes:** Week 0 entire — especially L01 (`this`), L03 (`const` member functions)

---

## 1. An Operator Is a Function

That is the whole idea. When you write `a + b` and `a` is a class type, the compiler looks for a
function named `operator+` and calls it:

```cpp
a + b        // becomes  operator+(a, b)      if a free function exists
             // or       a.operator+(b)       if a member exists
```

You can write that function. Nothing else about operators changes — **precedence, associativity and
arity are fixed by the grammar** and you cannot alter them. `*` binds tighter than `+` for your type
because it binds tighter for `int`, and that is not negotiable.

```cpp
struct V { double x; };
V operator+(const V& a, const V& b) { return V{a.x + b.x}; }

V p{1}, q{2};
V r = p + q;          // r.x == 3
```

**This is syntax, not semantics.** The compiler will happily let `operator+` launch a missile. Section
9 is about why you should not.

---

## 2. Member or Free Function?

Most operators can be written either way:

```cpp
class V {
    double x;
public:
    V operator+(const V& o) const { return V{x + o.x}; }   // member
};

V operator+(const V& a, const V& b);                       // free
```

For a member, **the left operand is `this`**. That single fact decides most of the design.

### 2.1 Members Break Symmetry

Write `operator*` as a member and scaling works one way only:

```cpp
struct V { double x;
    V operator*(double s) const { return V{x*s}; }   // member
};
V v{2.0};
V a = v * 3.0;      // fine:  v.operator*(3.0)
V b = 3.0 * v;      // ???
```

```
error: no match for 'operator*' (operand types are 'double' and 'V')
```

`3.0 * v` would need `double::operator*(V)`, and you cannot add members to `double`. **A member
function can never be selected when the left operand is a built-in type.**

Free functions have no such problem:

```cpp
V operator*(const V& v, double s) { return V{v.x*s}; }
V operator*(double s, const V& v) { return V{v.x*s}; }
```

```
v*3=6.0  3*v=6.0
```

> **Rule: binary operators that treat their operands symmetrically should be free functions.** That
> covers `+ - * / == != < > <= >=`. Anything else produces a type where `2 * v` fails and `v * 2`
> works, which users will regard as a bug and will be right to.

### 2.2 Some Operators *Must* Be Members

`=`, `[]`, `()`, and `->` must be member functions. The standard requires it.

The reason is that these have a distinguished left operand that must be the class itself, and allowing
free-function versions would let anyone redefine assignment for a type they do not own.

### 2.3 Some Operators Cannot Be Members of *Your* Class

Anything whose left operand is not your type. The important case is stream output.

---

## 3. `operator<<`: Why It Must Be Free

To write `std::cout << v`, you need a function whose **left operand is `std::ostream`**. A member of
`V` cannot be that, because a member's left operand is always `V`.

Try it anyway:

```cpp
struct V { double x;
    std::ostream& operator<<(std::ostream& os) const { return os << x; }   // member
};
std::cout << v;
```

```
error: no match for 'operator<<' (operand types are 'std::ostream' and 'V')
```

**The member is not ignored — it is simply the wrong function.** It works perfectly if you call it the
way you actually declared it:

```cpp
v << std::cout;      // prints: 1
```

That compiles and runs. It is also useless, and it is the clearest possible demonstration of the rule:
**the left operand decides.**

### 3.1 The Correct Form

```cpp
class V {
    double x, y;
public:
    V(double a, double b) : x(a), y(b) {}
    friend std::ostream& operator<<(std::ostream& os, const V& v);
};

std::ostream& operator<<(std::ostream& os, const V& v) {
    return os << "(" << v.x << ", " << v.y << ")";
}
```

```
v = (1.5, 2.5)
```

Three details, all load-bearing:

- **Takes `std::ostream&`, returns `std::ostream&`.** Returning the stream is what makes chaining
  work: `os << a << b` is `(os << a) << b`, and the left part must evaluate to the stream.
- **Takes the object by `const V&`.** No copy, and it cannot modify what it prints.
- **`friend`** grants access to the private members. If your class has public accessors, you do not
  need it — and not needing it is better. Prefer accessors; use `friend` when the alternative is
  exposing state you did not want public.

> **Do not print a newline inside `operator<<`.** The caller decides. A type that always emits `"\n"`
> cannot be used mid-line, and there is no way for the caller to opt out.

---

## 4. `operator[]`: Always Provide Both

Subscript comes in a pair:

```cpp
struct Arr {
    int a[3] = {10, 20, 30};
    int&       operator[](int i)       { return a[i]; }   // non-const: assignable
    const int& operator[](int i) const { return a[i]; }   // const: read-only
};
```

Overload resolution picks by the **constness of the object**, verified:

```
m[0] (mutable object):
  non-const []
c[0] (const object):
  const []
```

**Why the non-`const` version returns a reference:** so `m[0] = 99` works. Returning `int` by value
would make `m[0]` an rvalue and the assignment would not compile.

**Why the `const` version exists at all:** without it, a `const Arr` has no `operator[]`, and every
function taking `const Arr&` becomes unable to read the container. That is the `const`-propagation
problem from L03 §3.3, and it is the most common reason a beginner's container is unusable with STL
algorithms in Week 3.

### 4.1 Bounds Checking

`operator[]` conventionally does **not** bounds-check, matching built-in arrays and `std::vector`.
Providing a checked `at()` alongside is the STL's convention and a good one.

This course's assignments ask you to throw from `operator[]` anyway, because the alternative in a
teaching context is a silent memory error. **Real containers do not**, and Week 3 explains the
trade-off properly.

---

## 5. `operator()`: The Function Call Operator

A class with `operator()` can be called like a function. Such an object is a **functor**.

```cpp
class Scaler {
    double factor;
public:
    explicit Scaler(double f) : factor(f) {}
    double operator()(double x) const { return x * factor; }
};

Scaler triple(3.0);
triple(5.0);          // 15.0
```

The point, which arrives properly in **Week 3**, is that a functor **carries state** in a way a plain
function pointer cannot. `std::sort` can take a comparison functor that holds a sort key; it cannot
take a function pointer that does.

`operator()` is also the only operator that may take **any number of arguments**, which is why it is
the natural spelling for a multi-dimensional subscript: `m(row, col)`, since `m[row][col]` requires
returning a proxy object.

In **Week 11** you will learn that a lambda is exactly a class with `operator()` that the compiler
wrote for you.

---

## 6. Comparison Operators

```cpp
bool operator==(const V& a, const V& b) { return a.x==b.x && a.y==b.y; }
bool operator!=(const V& a, const V& b) { return !(a == b); }
bool operator< (const V& a, const V& b) { return a.norm() < b.norm(); }
```

**Define `!=` in terms of `==`, and `>`, `<=`, `>=` in terms of `<`.** Two reasons: less code, and it
is impossible for them to disagree.

> **C++20 has `operator<=>`** — the "spaceship" operator, which generates all six from one definition.
> **This course is C++17 and you may not use it.** It is worth knowing it exists, because it is the
> first thing you will meet in a modern codebase and it makes this section obsolete.

### 6.1 `operator<` Carries an Obligation

`std::sort` and `std::map` (Week 3) require a **strict weak ordering**:

1. Irreflexive: `!(a < a)`.
2. Asymmetric: `a < b` implies `!(b < a)`.
3. Transitive: `a < b` and `b < c` implies `a < c`.
4. Transitivity of equivalence: if neither `a < b` nor `b < a`, they are equivalent, and equivalence
   must be transitive.

**Violating these is undefined behaviour, not a wrong answer.** `std::sort` with an inconsistent
comparator can read past the end of your array and crash — this is a real and frequently-reported
failure, not a theoretical one.

Note the ordering above compares by `norm()`, so two different vectors of equal length are
*equivalent* but not *equal*. That is legal and consistent. It also means `std::map<V,...>` would treat
them as the same key, which may not be what you want — an example of a comparison that is correct and
still a poor design choice.

---

## 7. The Canonical Arithmetic Pattern

Write the compound assignments as members, then the binary operators in terms of them:

```cpp
class Vector3D {
    double e[3];
public:
    Vector3D& operator+=(const Vector3D& o) {
        for (int i = 0; i < 3; ++i) e[i] += o.e[i];
        return *this;                                   // return by reference
    }
};

Vector3D operator+(Vector3D a, const Vector3D& b) {     // left operand BY VALUE
    a += b;
    return a;
}
```

Three deliberate choices:

- **`operator+=` is a member returning `Vector3D&`.** Its left operand is genuinely privileged — it is
  being modified — so a member is right. Returning a reference allows `(a += b) += c`.
- **`operator+` is free, taking its left operand *by value*.** The by-value parameter is the copy you
  needed anyway, so you add to it and return it. Writing `const Vector3D& a` would force you to make a
  copy inside the body, which is the same work spelled longer.
- **Every binary operator is one line.** There is exactly one implementation of vector addition, in
  `+=`, and `+` cannot drift out of step with it.

**Do not return a reference from `operator+`.** It would have to refer to a local, which is destroyed
on return. `-Wall` catches the obvious form of this mistake.

---

## 8. What You Cannot Do

| Cannot | Why |
| --- | --- |
| Invent new operators (`**`) | The grammar is fixed |
| Change precedence or associativity | Also fixed. `a + b * c` is always `a + (b * c)` |
| Change arity | `/` is always binary |
| Overload `::`, `.`, `.*`, `?:`, `sizeof` | Reserved by the standard |
| Overload for built-ins only | At least one operand must be a class or enum type |

That last one is what stops anyone redefining `int + int`, and it is why `operator+(double, V)` is
legal while `operator+(double, double)` is not.

---

## 9. When Not to Overload

Overloading is easy, which is the problem. The test is simple:

> **Would a reader who has never seen your class guess what the operator does?**

`+` on a vector, a matrix, a complex number, a string: yes. `+` on an `Employee`: no. Write
`promote(e)` and let the reader see what happens.

Some specific traps:

- **`operator+` on a container meaning "insert"** — reads as concatenation. Prefer `push_back`.
- **`operator<` on something with no natural order** — you will get a consistent-looking sort that
  means nothing.
- **`operator bool`** — makes `if (obj)` compile, and makes `obj + 1` compile too, via the implicit
  conversion to `int`. Use `explicit operator bool()`, which permits the first and forbids the second.
- **Operators with side effects the reader cannot see.** `a == b` that logs to a file will eventually
  be called from inside `std::find` a million times.

**The good rule:** overload an operator when your type is modelling a thing that already *has* that
operator in its own domain — numbers, sets, strings, matrices. Otherwise write a named function.

`Vector3D` earns `+`, `-`, `*`, `/`, `==` and `<<` because vectors have all of them in mathematics.
It does **not** get `*` for the dot product, because mathematics writes that `a · b` and there are two
different products competing for one symbol. `dot(a, b)` and `cross(a, b)` say which one you meant.

---

## 10. A Complete Example

Reference output from the `Vector3D` you will build in PS 1:

```
a       = (1, 2, 3)
b       = (4, 5, 6)
a+b     = (5, 7, 9)
b-a     = (3, 3, 3)
a*2     = (2, 4, 6)
2*a     = (2, 4, 6)
-a      = (-1, -2, -3)
a/2     = (0.5, 1, 1.5)
dot     = 32
cross   = (-3, 6, -3)
|a|     = 3.74166
a==a    = 1   a!=b = 1   a<b = 1
```

$|a| = \sqrt{1 + 4 + 9} = \sqrt{14} = 3.74166$.

> **Note what `Vector3D` does *not* need.** Its only member is `double e[3]` — an array of built-ins.
> The compiler-generated copy constructor copies it element by element, which is exactly right.
> **`Vector3D` needs no destructor, no copy constructor and no copy assignment operator.**
>
> That is not because operators are safe. It is because it **owns no resource**. Lecture 05 takes a
> class that does, and the same generated copy constructor becomes a double free.

---

## 11. Summary

| Idea | The point |
| --- | --- |
| An operator is a function | `a + b` → `operator+(a, b)` |
| Member's left operand is `this` | Which is why members break symmetry |
| Symmetric binary ops → free functions | `3.0 * v` fails otherwise — verified |
| `= [] () ->` must be members | Required by the standard |
| `operator<<` must be free | A member gives you `v << cout`, which compiles and is useless |
| `operator[]` comes in pairs | Non-`const` returns `T&`; `const` version keeps `const` objects usable |
| `operator()` | A functor carries state; a function pointer does not |
| Define `!=` from `==`, rest from `<` | They cannot then disagree |
| `operator<` must be a strict weak ordering | Violating it is UB in `std::sort`, not a wrong answer |
| Canonical arithmetic | `+=` member; `+` free, taking the left operand by value |
| When not to | If a stranger cannot guess it, use a named function |

---

## 12. Exercises

**1.** Write `operator*` for a `Money` class as a **member**, then show the exact line that fails.
Convert it to a free function and show that line compiling.

**2.** Write `operator<<` for a class as a member, then call it the way you declared it. **Paste the
output.** In one sentence, say why the member is not merely broken but *backwards*.

**3.** Give a class only a non-`const` `operator[]`. Now write `void print(const Arr&)` that reads
`a[0]`. Paste the error and connect it to L03 §3.3.

**4.** Implement `Fraction` with `+ - * /`, `==`, `<` and `<<`, always in lowest terms. **Does your
`operator<` satisfy the four strict-weak-ordering conditions?** Argue for each.

**5.** Write a functor `Between(lo, hi)` whose `operator()(int)` returns whether its argument lies in
range. Explain in one sentence what it can do that a function pointer cannot.

**6.** Someone proposes `operator+` on a `Logger` meaning "append a message". Give two concrete
reasons to reject it, one about readability and one about §6.1 or §9.

**7.** Implement `operator+` returning a reference to a local and compile with `-Wall`. **Quote the
warning**, then explain what would happen at runtime if you ignored it.

---

## 13. Next

**Lecture 05** returns to `CharBuffer`. It has a correct constructor, a correct destructor and correct
operators — and copying it destroys the program. We find out which function did it, where it came
from, and what the Rule of Three actually says.

---

*PROG 102 · Week 1 · Lecture 04 · © CSE Department*
