# PROG 102 · Lecture 23
## Creational Patterns

**Week 7 · Wednesday · 50 minutes**
**Reading:** Gang of Four Ch. 3 (Singleton, Factory Method, Abstract Factory, Builder)
**Assumes:** L22, Week 4 (abstract classes), Week 5 (`unique_ptr`)

**Date:** Wednesday 3 March 2027 · 10:00–10:50 · Week 7

---

## 1. The Problem They Share

A constructor names a concrete type. `Circle c(2.0);` commits, at compile time, to exactly `Circle`.

**Creational patterns are four ways of postponing or controlling that commitment** — deciding the type
later, restricting how many exist, or making a complicated construction readable.

---

## 2. Singleton

**Intent:** ensure a class has exactly one instance, and provide a global point of access to it.

The correct C++ implementation is four lines:

```cpp
class Config {
    std::string level_ = "info";
    Config() = default;
public:
    static Config& instance() { static Config c; return c; }   // the whole pattern
    Config(const Config&)            = delete;
    Config& operator=(const Config&) = delete;
};
```

- The constructor is **private**, so nobody else can make one.
- Copying is **deleted** (L05 §4.1), or you could make a second by copying the first.
- The instance is a **function-local `static`**, constructed on first call.

This is **Meyers' Singleton**, and its virtue is the last point.

### 2.1 It Is Thread-Safe, and That Is a Language Guarantee

Since C++11, initialization of a function-local `static` is guaranteed to happen **exactly once**, even
if several threads reach it simultaneously; the others block until it completes. These are informally
called **"magic statics"**.

Verified: sixteen threads racing a constructor that sleeps for 50 ms.

```
16 threads raced to initialise a 50 ms constructor
constructions = 1   (must be 1)
all threads got the same address: yes
```

**And it is not free magic — the compiler emits the lock.** Looking at the generated code:

```
__cxa_guard_acquire
__cxa_guard_release
__cxa_guard_abort
```

Those are the runtime's guard functions. **The first call takes a lock; subsequent calls test a flag
and skip it.** ThreadSanitizer confirms no race:

```
race warnings on the singleton: 0
```

*(TSan on some Linux kernels needs `setarch $(uname -m) -R ./prog` to start at all — see Lab 0's
toolchain notes.)*

> **Before C++11 this was genuinely hard.** The famous "double-checked locking" pattern was written to
> solve it and was, for years, subtly broken on most compilers. **The four-line version above is
> correct and the elaborate one is obsolete** — if you find double-checked locking in a code review,
> the fix is to delete it.

### 2.2 Why You Should Usually Not

Singleton is the most-criticised pattern in the book, and the objections are good:

- **It is a global variable with a nicer hat.** All the coupling problems of globals remain: any code
  can reach it, so any code might depend on it, and you cannot tell from a function's signature whether
  it does.
- **It makes testing hard.** You cannot substitute a fake `Config` for one test, because there is
  exactly one and it is reachable from everywhere.
- **Initialisation order across translation units is unspecified** for *namespace-scope* objects. The
  function-local form fixes this, and it is the reason to use it — but **destruction** order at exit is
  still awkward, and a singleton whose destructor uses another singleton is a real bug class.
- **"Exactly one" is rarely a requirement.** It is usually a convenience mistaken for one. The moment
  you need two — a second config for a test, a second connection pool for a second database — the
  pattern is in your way.

> **The usual better answer: make it an ordinary object and pass it in.** A `Config&` parameter says
> what a function depends on, can be substituted in tests, and permits two.
>
> **Legitimate uses exist** — a process-wide logger, a hardware resource that genuinely is unique. Use
> it deliberately, not by default.

---

## 3. Factory Method

**Intent:** define an interface for creating an object, but let the decision about which class to
instantiate be made elsewhere.

```cpp
std::unique_ptr<Shape> make_shape(const std::string& kind, double dim) {
    if (kind == "circle") return std::make_unique<Circle>(dim);
    if (kind == "square") return std::make_unique<Square>(dim);
    throw std::invalid_argument("unknown shape: " + kind);
}
```

```
Circle  area=12.5664
Square  area=4.0000
rejected: unknown shape: hexagon
```

**Note the return type.** `std::unique_ptr<Shape>` says three things at once (L16 §6): you get
ownership, the concrete type is hidden, and you cannot forget to release it. **Returning `Shape*` here
would be the Week 5 mistake.**

### 3.1 What It Buys

The caller says *what it wants* and not *which class*. Adding a `Triangle` means editing one function;
every call site is untouched.

**And it puts the failure in one place.** `make_shape("hexagon", 1)` throws from a single line rather
than from wherever somebody wrote `new Hexagon`.

### 3.2 The Honest Objection

That `if`-chain is a `switch` on a string, which L15 §4.4 called a design smell. **Here it is
legitimate**, because it is the *one* place that maps external input to concrete types — that mapping
has to exist somewhere, and confining it to a single function is the point.

**The smell is a type-switch scattered across the codebase, not a single one at the boundary.**

If the set of types is open — plugins, or types registered at run time — a registry replaces the chain:

```cpp
std::map<std::string, std::function<std::unique_ptr<Shape>(double)>> registry;
```

*(`std::function` is Week 11. The idea is that new types register themselves and the factory never
changes.)*

---

## 4. Abstract Factory

**Intent:** provide an interface for creating **families** of related objects without specifying their
concrete classes.

Factory Method makes one product. Abstract Factory makes a **matched set**.

```cpp
struct Theme {
    virtual ~Theme() = default;
    virtual std::unique_ptr<Button>   button()   const = 0;
    virtual std::unique_ptr<Checkbox> checkbox() const = 0;
};
struct DarkTheme : Theme { /* returns DarkButton and DarkCheckbox */ };
struct LightTheme : Theme { /* returns LightButton and LightCheckbox */ };

void draw_ui(const Theme& t) {
    std::printf("%s  %s\n", t.button()->render().c_str(), t.checkbox()->render().c_str());
}
```

```
[ dark button ]  [x] dark
[ light button ]  [x] light
```

**The guarantee is consistency.** `draw_ui` cannot accidentally produce a dark button beside a light
checkbox, because it never names either concrete type — it asks one factory for both, and a factory
only makes its own family.

> **The cost is rigidity in the other direction.** Adding a *product* — a `Slider` — means editing the
> `Theme` interface and **every** concrete theme. Adding a *family* is free; adding a product is
> expensive.
>
> **That asymmetry is the whole trade**, and it is exactly the question L22 §6.2 asks: which change is
> actually coming? If you will add themes, this is right. If you will add widgets, it is a tax.

---

## 5. Builder

**Intent:** separate the construction of a complex object from its representation, so the same process
can produce different results.

The problem it solves is one you have already hit:

```cpp
Request r("https://example.com", "POST", {{"Accept","json"}}, "{\"x\":1}", 5, true, false, 3);
```

**Nobody can read that.** Which `bool` is which? What is the `3`? And adding a parameter means editing
every call.

```cpp
Request r = RequestBuilder("https://example.com/api")
                .method("POST")
                .header("Accept", "json")
                .header("Auth", "token")
                .body("{\"x\":1}")
                .timeout(5)
                .build();
```

```
POST https://example.com/api timeout=5 headers=2 body=7B
```

Each setter returns `*this` by reference, which is what makes chaining work — **the same trick as
`operator+=` in Week 1 §L04 §7**.

### 5.1 Why It Is Better Than Default Arguments

C++ has default arguments, which handle *some* of this. They do not handle:

- **arguments you want to skip** — you cannot pass the seventh default and set the eighth;
- **naming at the call site** — `.timeout(5)` says what 5 is; `, 5,` does not;
- **repeated values** — `.header(...)` twice is natural; a parameter cannot be repeated;
- **validation before construction** — `build()` can check the combination and throw, so a `Request`
  never exists in an invalid state.

> **The rule of thumb: more than about four constructor parameters, or any `bool` parameter, and a
> builder is worth considering.** A `bool` parameter is almost always unreadable at the call site —
> `create(true, false)` — and it is the cheapest signal that this pattern applies.

**Builder is the creational pattern you are most likely to actually need**, and it is the least
fashionable.

---

## 6. Choosing

| You need | Pattern |
| --- | --- |
| Exactly one instance | **Singleton** — and reconsider first |
| The concrete type decided at run time from data | **Factory Method** |
| A consistent *family* of related objects | **Abstract Factory** |
| Readable construction of something with many options | **Builder** |
| None of the above | **A constructor.** This is the common case |

That last row is not a joke. **Most classes should have a constructor and no pattern**, and Lab 7 is
about a codebase that forgot it.

---

## 7. Summary

| Pattern | Intent in one line | Main cost |
| --- | --- | --- |
| **Singleton** | Exactly one instance, globally reachable | A global variable; untestable; "one" is rarely a requirement |
| **Factory Method** | Decide the concrete type elsewhere | One type-switch, which is fine at a boundary |
| **Abstract Factory** | A consistent family | Adding a *product* edits every factory |
| **Builder** | Readable construction with many options | An extra class |

| Fact | Verified |
| --- | --- |
| Function-local `static` is thread-safe | 16 threads, 50 ms constructor, **1** construction |
| The compiler emits the lock | `__cxa_guard_acquire`/`_release`/`_abort` |
| TSan finds no race in it | 0 warnings |

---

## 8. Exercises

**1.** Implement Meyers' Singleton with a constructor that prints. Call `instance()` five times and
confirm it constructs once. **Then delete the deleted copy constructor and show how to defeat the
pattern.**

**2.** Race 16 threads to `instance()` with a slow constructor. Report the construction count. Then
find `__cxa_guard_acquire` in the generated assembly.

**3.** Write `make_shape` for three shapes. Add a fourth. **Count the lines you had to change, and how
many call sites.**

**4.** Take a program that uses a singleton `Config` and rewrite it to pass a `Config&`. **Which
functions' signatures changed?** In two sentences, say what that tells you.

**5.** Implement a `Theme` abstract factory with two themes and two products. Now add a **third
product**. **Count the files you had to edit.** Then add a third *theme* and count again.

**6.** Take a constructor with six parameters, two of them `bool`, and write a builder for it. **Show
the before and after call sites** and say which you would rather read in a review.

**7.** Give a concrete situation where Singleton is the right answer. Then give the strongest argument
against your own example.

---

## 9. Next

**Lecture 24** is the structural patterns, and it contains the week's one genuinely quantitative
result: the choice between subclassing and decorating is $2^n$ against $n$, and the decorating costs
about 0.6 nanoseconds a layer.

---

*PROG 102 · Week 7 · Lecture 23 · © CSE Department*
