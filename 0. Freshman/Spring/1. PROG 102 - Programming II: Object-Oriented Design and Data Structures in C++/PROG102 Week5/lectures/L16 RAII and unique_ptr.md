# PROG 102 · Lecture 16
## RAII and `unique_ptr`

**Week 5 · Monday · 50 minutes**
**Reading:** *C++ Primer* §12.1.1–12.1.5 · **Reference:** Meyers, *Effective Modern C++* Items 18, 21
**Assumes:** L02 (destructors), Week 1 (Rule of Three), Week 4 (virtual destructors)

---

## 1. The Idiom, Named

**RAII — Resource Acquisition Is Initialization.** You met it in Lecture 02 §5 and have been using it
since:

> **Tie a resource to an object's lifetime.** Acquire it in the constructor, release it in the
> destructor, and the language will release it on every exit path — including ones you did not write.

The name is unhelpful; the mechanism is not. **The destructor is the whole feature**, and everything
this week adds is pre-written classes that use it.

The resource need not be memory. A file handle, a lock (**Week 10**), a database connection, a socket
— anything with an acquire/release pair belongs in a class whose destructor does the release.

---

## 2. The Problem With Doing It By Hand

You have written this correctly several times now:

```cpp
class Buffer {
    char* data;
public:
    explicit Buffer(int n) : data(new char[n]) {}
    ~Buffer() { delete[] data; }
    Buffer(const Buffer&);              // and the copy constructor
    Buffer& operator=(Buffer);          // and the assignment
};
```

**That is four functions of boilerplate per resource-owning class**, and Lab 1 showed what happens when
one of them is wrong. Writing it once per class, correctly, forever, is not a plan.

`std::unique_ptr` is that class, written for you and correct.

---

## 3. `unique_ptr`

```cpp
#include <memory>

auto p = std::make_unique<Widget>(args...);   // allocate and own
p->method();                                  // use like a pointer
(*p).field;
if (p) { }                                    // contextually convertible to bool
```

**No `delete`.** When `p` goes out of scope — by any route, including an exception — the destructor
runs `delete`.

### 3.1 It Cannot Be Copied

```cpp
auto a = std::make_unique<Widget>();
auto b = a;                    // error: use of deleted function
```

**This is the design, not a limitation.** `unique_ptr` means *exclusive* ownership. Two `unique_ptr`s
to one object would both delete it — the double free from Week 1 — so the copy constructor is
`= delete`d (L00 §14).

Ownership can be **transferred**:

```cpp
auto b = std::move(a);         // b owns it now; a is null
```

That is Lecture 18's subject. For now: `std::move` is how you say "take this from me".

### 3.2 Always `make_unique`

```cpp
auto p = std::make_unique<Widget>(1, 2);        // prefer
std::unique_ptr<Widget> q(new Widget(1, 2));    // works, but
```

Reasons: it says the type once instead of twice, there is no naked `new` to mismatch, and — for
`shared_ptr` — it halves the allocations (L17 §3).

### 3.3 Arrays

```cpp
auto arr = std::make_unique<int[]>(100);        // note the [ ]
arr[0] = 1;
```

The `[]` specialization calls `delete[]`, so the `new`/`delete[]` mismatch from Lab 1's first bug
becomes impossible.

> **In practice, use `std::vector<int>` instead.** `unique_ptr<int[]>` knows the pointer and not the
> size; a vector knows both and gives you iterators. Reach for the array form only at a C API boundary.

---

## 4. Custom Deleters

Not all resources are freed with `delete`:

```cpp
auto closer = [](std::FILE* f){ if (f) std::fclose(f); };
std::unique_ptr<std::FILE, decltype(closer)> fp(std::fopen("data.txt", "r"), closer);
```

Now the file closes on every exit path. **This is how you RAII-wrap a C API** — and there are a great
many C APIs.

Note that the deleter is part of the **type**, which is why `sizeof(unique_ptr)` stays 8 only for the
default deleter. A stateful deleter makes the object bigger, which is a real trade-off and a good
reason to prefer a stateless lambda.

---

## 5. What It Costs

"Zero-overhead abstraction" is the claim. Here is the check, in three parts, because the honest answer
is not one number.

### 5.1 Size

```
sizeof(int*)                 =  8
sizeof(std::unique_ptr<int>) =  8      <- identical
sizeof(std::shared_ptr<int>) = 16
sizeof(std::weak_ptr<int>)   = 16
```

**`unique_ptr` is exactly a pointer.** The deleter is stateless and occupies no space (empty base
optimization).

### 5.2 Generated Code, Where the Comparison Is Fair

The right comparison is *how you pass it to a function that does not take ownership*:

```cpp
int raw_param (Widget* w) { w->poke(); return w->v; }
int uniq_param(Widget& w) { w.poke();  return w.v;  }
```

At `-O2`:

```asm
raw_param:                    uniq_param:
        endbr64                       endbr64
        push    rbx                   push    rbx
        mov     rbx, rdi              mov     rbx, rdi
        call    Widget::poke()        call    Widget::poke()
        mov     eax, DWORD PTR [rbx]  mov     eax, DWORD PTR [rbx]
        pop     rbx                   pop     rbx
        ret                           ret
```

**Byte for byte identical.**

> **The wrong comparison is instructive too.** Passing `const std::unique_ptr<Widget>&` instead is
> *not* identical — it adds a load, because you are passing a pointer *to the smart pointer* and must
> dereference twice. **That is both slower and worse style**, and §7 explains why.

### 5.3 The Ownership Case: Not Identical, and Not Overhead

```cpp
int raw_own()  { Widget* w = new Widget{7}; w->poke(); int r = w->v; delete w; return r; }
int uniq_own() { auto w = std::make_unique<Widget>(Widget{7}); w->poke(); return w->v; }
```

Here the generated code **does** differ: the `unique_ptr` version carries exception-handling landing
pads (`.LEHB0`, `.LEHE0`) that the raw version does not.

**That is not overhead. It is the extra thing it does.** Make `poke()` throw, and count allocations:

| | allocations | frees | |
| --- | --- | --- | --- |
| raw `new`/`delete` | 2 | 1 | **LEAKED** |
| `make_unique` | 2 | 2 | balanced |

Verified at **both `-O0` and `-O2`**. The raw version's `delete w;` is skipped when `poke()` throws —
the failure Lecture 02 §1 described, still there, still silent.

> **So `unique_ptr` is not free. It is cheaper than free**, because the code it replaces was wrong on
> a path nobody tests.

### 5.4 A Benchmarking Trap Found While Measuring This

The first version of the experiment had `poke()` throw *unconditionally*. At `-O2` the raw version
reported **balanced**, apparently contradicting the whole point.

It was not. GCC inlined `poke()`, saw that the throw dominated, and **deleted the allocation entirely**
as dead code — allocation elision is permitted. The benchmark was measuring a program that no longer
allocated.

Making the throw conditional restored the leak at both optimization levels.

**Add this to the list from Weeks 2–4.** A benchmark can measure the wrong thing (W4), carry a wrong
explanation (W2), answer a different question (W3) — **or be optimized out from under you.**

---

## 6. Ownership in the Type System

The real argument for `unique_ptr` is not performance and not even safety. It is that **the code now
says who owns what**, and the compiler checks it.

```cpp
Widget* find_widget();                    // ??? do I delete this?
std::unique_ptr<Widget> make_widget();    // yours; you must handle it
Widget* borrow_widget();                  // not yours; do not delete
Widget& get_widget();                     // not yours, and never null
```

**The first line is a documentation problem.** The others are not, because the type answers the
question. That is the whole of modern C++ memory management: not "be careful", but "make the careful
thing the only thing that compiles".

---

## 7. Passing Smart Pointers to Functions

This follows directly and it is worth memorising, because it is the most common thing beginners get
wrong.

| Signature | Means | Use when |
| --- | --- | --- |
| `void f(std::unique_ptr<W> p)` | **takes ownership** | The function will keep or destroy it |
| `void f(W* p)` | borrows, may be null | It only uses it, and null is meaningful |
| `void f(W& r)` | borrows, never null | It only uses it. **The default** |
| `void f(const std::unique_ptr<W>&)` | **almost always wrong** | — |

The last row is the one to avoid. It says "I need a `unique_ptr` specifically", which means the
function cannot be called with a `shared_ptr`, a stack object, or a raw pointer — **and it does not
take ownership anyway**, so the restriction buys nothing. Take `W&` and let the caller keep the
ownership question to itself.

> **Rule: pass ownership by value, and everything else by reference to the pointee.** Your signature
> then documents itself.

---

## 8. `std::vector<std::unique_ptr<Base>>`

Week 4 used this in PS 4 without explanation. Now it has one.

```cpp
std::vector<std::unique_ptr<Shape>> shapes;
shapes.push_back(std::make_unique<Circle>("c1", 1.0));
shapes.push_back(std::make_unique<Square>("s1", 3.0));

for (const auto& s : shapes) std::cout << s->area() << "\n";
```

It solves **both** of Week 4's problems at once:

- `std::vector<Shape>` would **slice** (L15 §3.1). This does not — the vector holds pointers.
- `std::vector<Shape*>` would not slice, but somebody must `delete` every element, on every exit path.
  This destroys them automatically, in the vector's destructor.

**And it still needs `Shape`'s destructor to be `virtual`** (L15 §2). `unique_ptr<Shape>` calls
`delete` on a `Shape*`; if that destructor is not virtual, the derived part is never destroyed. **RAII
does not rescue you from Week 4's rule** — it only makes sure the `delete` happens.

Verified. With a non-virtual base destructor:

```
ERROR: AddressSanitizer: new-delete-type-mismatch
```

exactly as in Week 4, and clean once the destructor is `virtual`.

> **Worse: the warning disappears.** Week 4 §L15 §2.2 established that `-Wall` catches a raw
> `delete b;` through a polymorphic base. Here `-Wall -Wextra` said **nothing at all** — because the
> `delete` now happens inside `unique_ptr`'s deleter, in a library header, not at a `delete` site in
> your code.
>
> **So wrapping the pointer removed a diagnostic you used to get.** That is a genuinely uncomfortable
> result and worth carrying: smart pointers make the *leak* impossible and the *type mismatch* harder
> to see. `-Wnon-virtual-dtor`, which warns at the class definition rather than the delete, still
> catches it — which is the argument for adding that flag.

---

## 9. Summary

| Idea | The point |
| --- | --- |
| RAII | Acquire in the constructor, release in the destructor |
| `unique_ptr` | Exclusive ownership, expressed as a type |
| Not copyable | Deliberate — two owners is Week 1's double free |
| `make_unique` | Prefer it. No naked `new` |
| Custom deleters | RAII for any C API |
| `sizeof` = 8 | Identical to a raw pointer |
| Identical codegen | When you pass the **pointee**, not the smart pointer |
| The ownership case differs | Exception landing pads — **not overhead** |
| Raw `new`/`delete` **leaks on throw** | `allocs=2 frees=1`, verified at `-O0` and `-O2` |
| The benchmark trap | An unconditional throw let `-O2` delete the allocation |
| Signatures document ownership | By value = taking it; reference = borrowing |
| `const unique_ptr<T>&` | Almost always the wrong parameter type |

---

## 10. Exercises

**1.** Rewrite Lab 1's `Roster` so that `names` is a `std::vector<std::string>`. **How many of the five
special members do you now need?**

**2.** Verify `sizeof(std::unique_ptr<int>) == sizeof(int*)`. Then give it a **stateful** deleter (a
lambda capturing something) and measure `sizeof` again. Explain.

**3.** Reproduce §5.2: compile `raw_param(Widget*)` and `uniq_param(Widget&)` at `-O2 -S` and compare.
Then compare against `const std::unique_ptr<Widget>&` and report the extra instruction.

**4.** Reproduce §5.3 with an instrumented `operator new`/`operator delete` and a **conditionally**
throwing function. Report the allocation counts for both versions, at `-O0` and `-O2`.

**5.** Now make the throw **unconditional** and rerun at `-O2`. **Report what changes and explain it.**
*(This is §5.4. It is the most instructive part of the exercise.)*

**6.** Wrap `std::FILE*` in a `unique_ptr` with a custom deleter. Use it in a function with three early
returns and one `throw`. **Count the `fclose` calls you wrote.**

**7.** Write `void process(const std::unique_ptr<Widget>& w)`. Now try to call it with a stack
`Widget`, and with a `shared_ptr<Widget>`. **Report both errors**, then fix the signature.

---

## 11. Next

**Lecture 17** covers the case `unique_ptr` cannot express: **several owners, and the object dies when
the last one does.** `shared_ptr` does it by counting, which costs an allocation, an atomic, and — if
you are not careful — an entire object graph that never gets freed.

---

*PROG 102 · Week 5 · Lecture 16 · © CSE Department*
