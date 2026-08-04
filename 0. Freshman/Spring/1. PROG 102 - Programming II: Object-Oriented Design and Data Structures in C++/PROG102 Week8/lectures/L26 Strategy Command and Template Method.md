# PROG 102 · Lecture 26
## Strategy, Command, and Template Method

**Week 8 · Wednesday · 50 minutes**
**Reading:** Gang of Four Ch. 5 — Strategy, Command, Template Method
**Assumes:** L25, Week 4, Week 7

---

## 1. One Question, Three Answers

All three patterns answer: **how do you make a piece of behaviour a parameter?**

| Pattern | Parameterises | Chosen |
| --- | --- | --- |
| **Strategy** | an algorithm | by the caller, at run time |
| **Command** | an action, plus the ability to undo it | stored and replayed |
| **Template Method** | *steps* of a fixed algorithm | by subclassing, at compile time |

---

## 2. Strategy

> **Define a family of algorithms, encapsulate each one, and make them interchangeable.**

The problem it replaces:

```cpp
void sort_it(std::vector<int>& v, SortKind k) {
    switch (k) {
        case ASCENDING:  /* ... */ break;
        case DESCENDING: /* ... */ break;
        case BY_ABS:     /* ... */ break;
    }
}
```

**Every new ordering edits this function** — and Week 4 §L15 §4.4 told you what a type-switch means.

```cpp
struct Compare { virtual ~Compare() = default; virtual bool less(int, int) const = 0; };
struct Ascending  : Compare { bool less(int a, int b) const override { return a < b; } };
struct ByAbsolute : Compare { bool less(int a, int b) const override { return std::abs(a) < std::abs(b); } };
```

The context stores a `Compare*` and calls it. **Adding an ordering adds a class and edits nothing.**

### 2.1 You Have Been Using It Since Week 3

```cpp
std::sort(v.begin(), v.end(), std::greater<int>());
std::sort(v.begin(), v.end(), [](const P& a, const P& b){ return a.score > b.score; });
```

**`std::sort`'s comparator is a Strategy.** So is `unique_ptr`'s deleter (L16 §4), and `std::map`'s
`Compare` template parameter (L21 §2).

### 2.2 The Open/Closed Principle

> **Open for extension, closed for modification.**

The `switch` version is closed for extension: adding an ordering means opening the function. The
Strategy version is open: adding an ordering means adding a class, and the context is never touched.

**This is the clearest example of the principle in the catalogue**, and it is worth having a name for
because it is the argument you will make in code review.

---

## 3. Four Ways to Express a Strategy — Measured

C++ gives you at least four ways to pass "the comparison". Sorting **2,000,000 integers**, three runs,
identical results:

| How | Time | vs lambda |
| --- | --- | --- |
| Classic Strategy — virtual call | 165.7–167.6 ms | 1.04× |
| **`std::function`** | **287.5–304.1 ms** | **1.85×** |
| Lambda — template parameter | 159.9–160.9 ms | 1.00× |
| Default `operator<` | 149.9–151.2 ms | 0.94× |

**`std::function` is the slowest**, by a wide margin, and it is slower than the virtual call.

### 3.1 Why

Almost everyone predicts `std::function` will be fast, because it looks modern. It is **type erasure**:
a `std::function<bool(int,int)>` can hold *any* callable with that signature, so it stores a pointer to
a type-erased wrapper and calls through it.

**That call cannot be inlined**, because the target is not known at compile time. Inside `std::sort`'s
inner loop — executed roughly $n \log n \approx 4 \times 10^7$ times — that is 40 million calls the
optimizer cannot touch.

The lambda version is a **template parameter**, so its `operator()` is a concrete type the compiler
inlines into the loop. The comparison becomes a `cmp` instruction.

> **You have seen this exact result before.** Week 3 §L12 §2 measured `qsort` at roughly **2×**
> `std::sort` for precisely this reason — a function pointer cannot be inlined. **`std::function` is
> the same mechanism wearing modern clothes**, and it produces the same factor.
>
> **The lesson generalises:** *a callable whose type is erased cannot be inlined, and in a hot loop
> that costs about 2×.* Whether the erasure is spelled `void*`, a function pointer, a virtual call or
> `std::function` barely matters.

### 3.2 So What Should You Use?

- **A template parameter (lambda)** when the callable is known at compile time and the call is hot.
  This is what the STL does and it is free.
- **`std::function`** when you must *store* callables of different types in one container, or cross an
  ABI boundary, or the call is not hot. **Its flexibility is the point and you pay for it.**
- **A virtual interface** when the strategy has state, multiple methods, or its own lifetime — a
  full-blown policy object rather than one function.

**All three are legitimate.** The mistake is reaching for `std::function` as a default because it looks
like the modern spelling of a callback.

---

## 4. Command

> **Encapsulate a request as an object**, so you can parameterise, queue, log and undo it.

Strategy parameterises *how*; Command parameterises *what*, and makes it a value you can store.

```cpp
struct Command {
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo()    = 0;
};

class History {
    std::vector<std::unique_ptr<Command>> done;
public:
    void run(std::unique_ptr<Command> c) { c->execute(); done.push_back(std::move(c)); }
    bool undo() { if (done.empty()) return false; done.back()->undo(); done.pop_back(); return true; }
};
```

Verified:

```
text = "Hello, world"  history=2
after undo: "Hello"  history=1
after undo: ""  more to undo? no
```

**Undo is the feature that justifies the pattern.** Without it, a Command is a Strategy with a worse
name. With it you get, from the same structure: undo/redo, a macro recorder, a job queue, a
transaction log, and remote execution — because the action is now a *value* rather than a call.

> **`std::unique_ptr<Command>` is doing the ownership work.** The history owns the commands; `run`
> takes ownership by value (L16 §7). This is Week 5 applied without comment, which is how it should be
> by Week 8.

---

## 5. Template Method

> **Define the skeleton of an algorithm, deferring some steps to subclasses.**

The one pattern here that uses **inheritance rather than composition** — and the Gang of Four are
explicit that it is the exception.

```cpp
class Report {
public:
    std::string render() const {                       // the skeleton: FIXED
        return header() + " | " + body() + " | " + footer();
    }
protected:
    virtual std::string header() const { return "REPORT"; }   // default, overridable
    virtual std::string body()   const = 0;                   // subclass MUST supply
    virtual std::string footer() const { return "end"; }      // default
};
```

```
SALES | sales=1200 | end          // overrode header and body
REPORT | audit=ok | end           // overrode body only
```

**`render()` is not virtual.** That is the point: the *sequence* is fixed and the subclass cannot
change it, only fill in steps. The pure virtual says which step is mandatory; the others have defaults.

### 5.1 The Hollywood Principle

> **"Don't call us, we'll call you."**

The base class calls down into the subclass, not the other way round. That inverts the usual direction
and is why Template Method is the odd one out — it is the only pattern here where the framework is the
base class.

**You have used it:** `std::sort` is a template method whose varying step is the comparison. So is any
test framework's `setUp`/`test`/`tearDown`.

### 5.2 Template Method vs Strategy

They solve almost the same problem, and choosing between them is a real decision:

| | Template Method | Strategy |
| --- | --- | --- |
| Mechanism | inheritance | composition |
| Varies | *steps within* one algorithm | the *whole* algorithm |
| Chosen | at compile time, by subclassing | at run time |
| Can vary per instance | no — it is the type | yes |
| Coupling | tight (L13 §2) | loose |

**Prefer Strategy** unless you genuinely need the base class to control the sequence. That is Week 7
§L22 §3.1 once more: composition over inheritance, and this is a case where the book itself provides
both options and tells you which is which.

---

## 6. Summary

| Pattern | Intent | Note |
| --- | --- | --- |
| **Strategy** | Interchangeable algorithms | `std::sort`'s comparator. Open/Closed in its clearest form |
| **Command** | An action as an object | **Undo** is what justifies it |
| **Template Method** | Fixed skeleton, variable steps | The one that uses inheritance; prefer Strategy |

| Measured, 2M ints | |
| --- | --- |
| virtual Strategy | 165.7–167.6 ms |
| **`std::function`** | **287.5–304.1 ms — the slowest** |
| lambda / template | 159.9–160.9 ms |
| default `operator<` | 149.9–151.2 ms |
| Why | Type erasure blocks inlining — **Week 3's `qsort` result again** |

---

## 7. Exercises

**1.** Write a sort with a `switch` over three orderings, then convert it to Strategy. **Add a fourth
ordering to each** and report the lines changed.

**2.** Reproduce §3's benchmark: all four ways, 2,000,000 elements, three runs. **Predict the ranking
before you run it**, then report your prediction and the result.

**3.** Explain your §3 result in terms of inlining. Then find Week 3 §L12 §2's `qsort` figure and
**state the ratio in both experiments.** Are they close?

**4.** Give a concrete situation where `std::function` is the right choice **despite** the benchmark.
Be specific about what a template parameter could not do there.

**5.** Implement Command with undo for a text buffer supporting append and delete. Then add **redo**.
**How much new structure did redo need?**

**6.** Write a Template Method with one mandatory and two optional steps. Then rewrite the same thing
as Strategy. **Which is shorter, and which would you rather extend?**

**7.** `std::sort` is described here as both a Template Method and as taking a Strategy. **Is that a
contradiction?** Answer in three sentences.

---

## 8. Next

**Lecture 27** covers State and MVC, and then makes the week's real argument: **two of the patterns you
have just implemented are largely obsolete**, and the evidence is a line count and the benchmark you
have already seen.

---

*PROG 102 · Week 8 · Lecture 26 · © CSE Department*
