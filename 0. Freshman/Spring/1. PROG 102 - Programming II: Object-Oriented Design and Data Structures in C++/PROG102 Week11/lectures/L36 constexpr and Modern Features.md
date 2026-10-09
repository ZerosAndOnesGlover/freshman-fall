# PROG 102 · Lecture 36
## `constexpr` and Modern Features

*“Anybody who comes to you and says he has a perfect language is either naïve or a salesman.”* — Bjarne Stroustrup, "C++0x — An Overview", University of Waterloo (2007)

**Week 11 · Thursday · 50 minutes**
**Reading:** *C++ Primer* §2.4.4, §6.5.2; cppreference on `constexpr` and structured bindings
**Assumes:** L34, L35, Week 2

**Date:** Thursday 8 April 2027 · 10:00–10:50 · Week 11

**Coursework:** 📝 **PS 10** due Fri 9 Apr 17:00 · 📝 **PS 11** released Fri 9 Apr 10:00, due Fri 16 Apr 17:00 · 🔬 **Lab 11** Mon 12 Apr 15:00–16:50 · 📕 **Final exam** Thu 22 Apr 14:00–16:30

---

## 1. `constexpr` — Computation at Compile Time

```cpp
constexpr long factorial(int n) { return n <= 1 ? 1 : n * factorial(n-1); }
constexpr long f10 = factorial(10);
static_assert(f10 == 3628800, "computed at compile time");
```

**`constexpr` says: this *may* be evaluated at compile time**, if the arguments are compile-time
constants. In a `constexpr` variable or a `static_assert`, it **must** be.

**Since C++14, `constexpr` functions can contain loops, local variables and branches:**

```cpp
constexpr int fib(int n) { int a=0,b=1; for(int i=0;i<n;++i){ int t=a+b; a=b; b=t; } return a; }
constexpr int f30 = fib(30);
static_assert(f30 == 832040, "compile-time loop");
```

Verified — both `static_assert`s hold, so **the compiler ran those loops.**

### 1.1 How You Know It Happened

**A `static_assert` is proof.** It is evaluated at compile time or it is a compile error; there is no
third option.

**So is using the result as a template argument:**

```cpp
std::array<int, factorial(5)/24> arr{};      // 5 elements -- verified
```

`std::array`'s size is a non-type template parameter (Week 2 §L08 §5). **It must be known at compile
time**, so if this compiles, the factorial was computed by the compiler.

> **`constexpr` on its own is only permission.** `long n = factorial(x)` with a runtime `x` compiles
> and runs at run time. **If you need the compile-time guarantee, ask for it** — `constexpr` variable,
> `static_assert`, or a template argument. C++20's `consteval` makes it mandatory.

### 1.2 What It Is For

- **Constants with structure** — a lookup table computed rather than typed out.
- **Sizes and dimensions** — `std::array<T, compute_size()>`.
- **Moving work off the runtime**, in embedded or hot-start systems.
- **Catching errors at compile time** rather than in a test.

**Do not `constexpr` everything.** It constrains what the function may do, the errors are harder to
read, and for anything computed once at startup the runtime cost was never the problem.

---

## 2. `if constexpr` — Choosing a Branch at Compile Time

```cpp
template <typename T>
std::string describe(const T& v) {
    if constexpr (std::is_integral_v<T>)            return "integral: " + std::to_string(v);
    else if constexpr (std::is_floating_point_v<T>) return "float: "    + std::to_string(v);
    else                                            return "other";
}
```

```
describe(42)   -> integral: 42
describe(3.5)  -> float: 3.500000
describe("hi") -> other
```

**The untaken branch is not compiled.** That is the whole feature and it is what an ordinary `if`
cannot do: with a plain `if`, `std::to_string(v)` would have to compile for `std::string` too, and it
does not.

> **This replaces a large amount of template metaprogramming.** Before C++17 you needed tag dispatch or
> SFINAE to select an implementation by type; now you write an `if`. **It is the single biggest
> readability improvement C++17 made to generic code.**

**It is `if constexpr`, not `constexpr if`** — a spelling error the compiler will not let you make
twice.

---

## 3. Structured Bindings

```cpp
std::map<std::string,int> m{{"ada",1},{"grace",2}};
for (const auto& [name, n] : m) std::printf("%-6s %d\n", name.c_str(), n);

auto [q, r] = std::make_tuple(17/5, 17%5);      // q = 3, r = 2
```

```
ada    1
grace  2
17/5 = 3 remainder 2
```

Works on **`pair`, `tuple`, arrays, and any struct with public members**. You met it in Week 2 §L08
§6.1 and have used it since.

**The map loop is the case that matters.** Before C++17:

```cpp
for (const auto& kv : m) { ... kv.first ... kv.second ... }
```

`kv.first` says nothing; `name` says everything. **It is a readability feature and that is enough of a
justification.**

---

## 4. A Preview: Ranges (C++20)

**You may not use these — this course is C++17.** You should know they exist, because they change how
everything in Week 3 is written.

```cpp
// C++17, this course
std::vector<int> evens;
std::copy_if(v.begin(), v.end(), std::back_inserter(evens), [](int x){ return x%2==0; });
std::sort(evens.begin(), evens.end());

// C++20
auto result = v | std::views::filter([](int x){ return x%2==0; })
                | std::views::transform([](int x){ return x*x; });
```

Three improvements, and they are real:

- **No iterator pairs.** `ranges::sort(v)` instead of `sort(v.begin(), v.end())` — and the
  begin/end-from-different-containers bug (which bit this course's own test code in Week 6) becomes
  impossible.
- **Composition without temporaries.** The `filter | transform` pipeline is **lazy**; no intermediate
  vector is created.
- **Concepts give readable errors.** Week 2 §L09 §5's 78-line message becomes a statement about which
  requirement was not met.

> **Ranges are the biggest change to everyday C++ since C++11.** When you next pick up the language
> after this course, that is where to start.

---

## 5. Perfect Forwarding — A Signpost

```cpp
template <typename... Args>
std::unique_ptr<T> make(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

`Args&&` in a **deduced** context is a **forwarding reference**, not an rvalue reference: it binds to
lvalues and rvalues alike, and `std::forward` preserves which it was.

**This is how `make_unique`, `make_shared` and `emplace_back` work** — they take your arguments and
pass them to a constructor without copying.

**You are not required to write forwarding code in this course.** Recognise `Args&&...` plus
`std::forward`, and know it means *pass these through unchanged*. Meyers Items 24–30 cover it properly
and are the right next reading.

---

## 6. Summary

| Idea | The point |
| --- | --- |
| `constexpr` | *May* run at compile time — loops allowed since C++14 |
| Proving it did | `static_assert`, or use it as a template argument |
| It is only permission | `consteval` (C++20) makes it mandatory |
| `if constexpr` | **The untaken branch is not compiled** |
| It replaces | Tag dispatch and much SFINAE |
| Structured bindings | `for (const auto& [k,v] : map)` — readability, and that is enough |
| Ranges (C++20) | No iterator pairs, lazy composition, readable errors |
| Forwarding references | `Args&&` deduced + `std::forward` = pass through unchanged |

---

## 7. Exercises

**1.** Write a `constexpr` factorial and prove with a `static_assert` that it ran at compile time.
**Then call it with a runtime value** and confirm it still compiles.

**2.** Write a `constexpr` function containing a loop that builds a lookup table into a
`std::array<int, N>`. **Use the result as an array size** to prove compile-time evaluation.

**3.** Write `describe<T>` with `if constexpr` for three type categories. **Then rewrite it with a
plain `if`** and report the error.

**4.** Rewrite three loops over a `std::map` in your Project 1 code using structured bindings.
**Which reads better, and is that worth a language feature?**

**5.** Take one algorithm chain from PS 3 and **write out what it would look like with C++20 ranges.**
You cannot compile it; write it anyway and say what it would save.

**6.** Look up `std::make_unique`'s signature on cppreference. **Identify the forwarding reference**
and say what would break if it took `Args...` by value.

**7.** Find one place in your own code where `constexpr` would genuinely help and one where it would be
pointless. **Justify both.**

---

## 8. Next

**Week 12** is the last: testing, profiling with `perf`, cache-aware programming, and the architecture
of a medium-sized system. It measures the thing that has been lurking behind Week 3's container
results and Week 10's contention figure — **the memory hierarchy** — and it is where the course's
running argument about abstraction and cost is settled.

**Project 2 is due Friday 16 April; Lab 12, your project demo, is Monday 19 April; the final exam is
Thursday 22 April.**

---

*PROG 102 · Week 11 · Lecture 36 · © CSE Department*
