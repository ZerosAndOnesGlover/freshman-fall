# PROG 102 · Lecture 24
## Structural Patterns

**Week 7 · Friday · 50 minutes**
**Reading:** Gang of Four Ch. 4 (Adapter, Composite, Decorator, Facade)
**Assumes:** L22, L23, Week 5 (`unique_ptr`)

---

## 1. The Problem They Share

Creational patterns are about *making* objects. **Structural patterns are about arranging objects that
already exist** — making one fit an interface it was not written for, adding behaviour without
subclassing, treating a tree like a single item, or hiding a complicated subsystem.

All four below are **composition** (L22 §3.1) in different arrangements.

---

## 2. Adapter

**Intent:** convert the interface of a class into another interface clients expect.

You have a `LegacyPrinter` you cannot change — it is in a library, or twelve other things depend on it
— and your code is written against a `Writer` interface.

```cpp
struct Writer { virtual ~Writer() = default; virtual void write(const std::string&) const = 0; };

struct LegacyAdapter : Writer {
    const LegacyPrinter& p;
    explicit LegacyAdapter(const LegacyPrinter& lp) : p(lp) {}
    void write(const std::string& s) const override { p.print_upper(s.c_str()); }
};
```

```
LEGACY: HELLO FROM A MODERN INTERFACE
```

**The adapter is a translation layer and nothing else.** It holds the adaptee, implements the target
interface, and forwards.

> **You have used one already.** `std::stack` is an adapter (L11 §7): it holds a `std::deque` and
> exposes `push`/`top`/`pop` **and deliberately not `operator[]` or iteration.** An adapter can
> *restrict* an interface as well as translate it, and restricting is often the point.

**Note the adapter holds a reference here, not a `unique_ptr`.** It does not own the printer — Week 5
§L17 §7 again. If it did own it, `unique_ptr` would be right; the type should say which.

---

## 3. Decorator

**Intent:** attach additional responsibilities to an object dynamically. A flexible alternative to
subclassing for extending functionality.

**This is the pattern with the strongest quantitative case in the book.**

### 3.1 The Problem

A data source might be **buffered**, **encrypted**, or **compressed** — and these combine freely.

By subclassing, you need a class per *combination*:

```
FileSource
BufferedFileSource
EncryptedFileSource
CompressedFileSource
BufferedEncryptedFileSource
BufferedCompressedFileSource
EncryptedCompressedFileSource
BufferedEncryptedCompressedFileSource
```

**Eight classes for three features**, and the combination is fixed at compile time.

| features | subclasses ($2^n$) | decorators ($n$) |
| --- | --- | --- |
| 1 | 2 | 1 |
| 3 | 8 | 3 |
| 5 | 32 | 5 |
| 8 | 256 | 8 |
| **10** | **1024** | **10** |

### 3.2 The Structure

A decorator **implements the same interface as the thing it wraps, and holds one of them**:

```cpp
struct DataSource {
    virtual ~DataSource() = default;
    virtual std::string read() const = 0;
};

struct Decorator : DataSource {
    std::unique_ptr<DataSource> inner;          // owns what it wraps
    explicit Decorator(std::unique_ptr<DataSource> d) : inner(std::move(d)) {}
};

struct Buffered : Decorator {
    using Decorator::Decorator;
    std::string read() const override { return "buffered<" + inner->read() + ">"; }
};
```

`Buffered` **is a** `DataSource` and **has a** `DataSource`. That is what lets it wrap another
decorator rather than only a concrete source.

Composed at run time:

```cpp
std::unique_ptr<DataSource> d = std::make_unique<FileSource>("data.bin");
d = std::make_unique<Compressed>(std::move(d));
d = std::make_unique<Encrypted>(std::move(d));
d = std::make_unique<Buffered>(std::move(d));
```

```
Buffered(Encrypted(Compressed(File(data.bin))))
buffered<decrypted<inflated<raw-bytes-of(data.bin)>>>
```

**Three classes, and the order is chosen at run time** — from a config file, if you like. The
subclassing version cannot do that at all.

> **`std::move` is doing real work here.** Each wrap *transfers ownership* of the inner source into the
> new decorator, which is exactly Week 5 §L18. Without move semantics this pattern would need
> `shared_ptr` or raw pointers, and it is a good example of a language feature making a design
> cleaner.

### 3.3 What It Costs

Every layer is one virtual call. Measured over 10,000,000 calls:

| chain depth | total per call | |
| --- | --- | --- |
| 0 (bare) | 2.06 ns | |
| 1 | 2.41 ns | |
| 2 | 2.98 ns | |
| 4 | 4.14 ns | |
| 8 | 6.70 ns | |

**Marginal cost: about 0.58 ns per layer** — $(6.70 - 2.06)/8$.

That is *less* than Week 4's ~2 ns for a virtual call, because these targets are perfectly predictable
and the branch predictor learns them; several are speculatively devirtualized (L14 §6).

> **So the trade is: $2^n$ classes and compile-time fixing, against $n$ classes, runtime composition,
> and 0.6 nanoseconds a layer.** That is unusually one-sided, and it is why this pattern is everywhere
> — Java's `BufferedInputStream(new FileInputStream(...))` is exactly this, and so is every
> middleware stack in every web framework you will ever use.

---

## 4. Composite

**Intent:** compose objects into tree structures, and let clients treat individual objects and
compositions uniformly.

```cpp
struct Node { virtual ~Node()=default; virtual std::size_t size() const = 0; };

struct FileNode : Node { std::size_t bytes; std::size_t size() const override { return bytes; } };

struct DirNode : Node {
    std::vector<std::unique_ptr<Node>> children;
    std::size_t size() const override {
        return std::accumulate(children.begin(), children.end(), std::size_t{0},
            [](std::size_t a, const std::unique_ptr<Node>& c){ return a + c->size(); });
    }
};
```

```
project/ (5400 B)
  src/ (4600 B)
    main.cpp (1200 B)
    list.hpp (3400 B)
  README.md (800 B)
total via one call: 5400 B
```

**The caller does not know whether it holds a file or a directory**, and `size()` works either way. The
recursion is in the structure rather than in the calling code.

> **The uniformity is the point and also the objection.** `DirNode` needs `add()`; `FileNode` does not.
> The Gang of Four discuss putting `add()` on the base for maximum uniformity — which means
> `file->add(...)` compiles and must fail at run time. **This course's position is the opposite:**
> keep `add()` on `DirNode` (L20 §5 — an interface should refuse what it cannot do), and let the
> caller downcast in the one place that builds trees.
>
> This is a genuine disagreement with the book, and it is worth knowing that the book's own
> "Consequences" section raises it.

---

## 5. Facade

**Intent:** provide a unified, higher-level interface to a set of interfaces in a subsystem.

The simplest pattern in the book. Sections 2–4 built a subsystem with several moving parts; a facade
hides it:

```cpp
class Archive {
    std::unique_ptr<DataSource> src;
public:
    explicit Archive(std::string file)
      : src(std::make_unique<Buffered>(std::make_unique<Encrypted>(
              std::make_unique<Compressed>(std::make_unique<FileSource>(std::move(file)))))) {}
    std::string load() const { return src->read(); }
};
```

```cpp
Archive arc("secret.dat");
arc.load();
```

```
Archive("secret.dat").load() -> buffered<decrypted<inflated<raw-bytes-of(secret.dat)>>>
```

**The caller writes two lines and never learns that decorators exist.**

> **A facade does not forbid the subsystem** — code that needs the pieces can still use them. It
> provides the easy path for the common case, which is why `Archive` here is a convenience rather than
> a wall.
>
> **The failure mode is a facade that grows into a second interface to everything** — one class with
> forty methods forwarding to five subsystems. At that point it is not simplifying anything; it is a
> phone directory.

---

## 6. Choosing

| You need | Pattern |
| --- | --- |
| An existing class to fit an interface it was not written for | **Adapter** |
| Combinable, optional behaviour composed at run time | **Decorator** |
| To treat a tree and a leaf the same way | **Composite** |
| A simple entry point to a complicated subsystem | **Facade** |

---

## 7. Summary

| Pattern | One line | Main cost |
| --- | --- | --- |
| **Adapter** | Translate (or restrict) an interface | One more indirection; a class per adaptee |
| **Decorator** | Add behaviour by wrapping | ~**0.58 ns per layer**; deep chains are hard to debug |
| **Composite** | Trees and leaves, uniformly | Uniformity tempts you into `add()` on a leaf |
| **Facade** | A simple front door | Grows into a phone directory if unwatched |

| Measured | |
| --- | --- |
| $2^n$ vs $n$ | 10 features: **1024 subclasses** or **10 decorators** |
| Decorator layer cost | 2.06 ns bare → 6.70 ns at depth 8 |
| Marginal | **~0.58 ns per layer** |

---

## 8. Exercises

**1.** Write an adapter making a C API (`FILE*`, or a C string function) satisfy a small C++ interface.
**Does your adapter own the adaptee?** Justify the pointer type you chose.

**2.** Implement three decorators over one interface and compose all **eight** combinations at run time,
printing each. **Then write out the class names the subclassing version would need.**

**3.** Reproduce §3.3: measure a decorator chain at depths 0, 1, 2, 4 and 8. **Report the marginal cost
per layer** and compare it with Week 4's virtual-call figure. Explain any difference.

**4.** Build a Composite for a filesystem tree and compute total size with one call. Then add a
`count_files()` that returns 1 for a file. **How much code did the second operation need?**

**5.** Put `add()` on the Composite base class, as the Gang of Four discuss. **Write the code that
now compiles and must fail at run time.** Then argue for or against the book's position.

**6.** Write a facade over your Week 6 container library exposing three operations. **Then name one
thing a user of the facade can no longer do**, and say whether that matters.

**7.** A colleague has a decorator chain fourteen layers deep and a bug somewhere in it. **Give two
concrete reasons this is hard to debug**, then say what you would change about the design.

---

## 9. Next

**Week 8** is the behavioural patterns — Observer, Strategy, Command, Template Method, State — and it
ends with two patterns that C++11 made nearly obsolete, which is the strongest possible reminder that
the catalogue is a 1994 field report rather than scripture.

**Project 1 is due Week 9.** Parts 1 and 2 should be working by now.

---

*PROG 102 · Week 7 · Lecture 24 · © CSE Department*
