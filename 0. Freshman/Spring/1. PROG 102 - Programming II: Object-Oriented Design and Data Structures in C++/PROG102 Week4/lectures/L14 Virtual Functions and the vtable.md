# PROG 102 · Lecture 14
## Virtual Functions and the vtable

**Week 4 · Wednesday · 50 minutes**
**Reading:** *C++ Primer* §15.3, §15.5 · **Reference:** Stroustrup §20.3
**Assumes:** L13, and L01 (`this`)

**Date:** Wednesday 17 February 2027 · 10:00–10:50 · Week 4

---

## 1. Without `virtual`, the Pointer Decides

```cpp
struct ShapeNV { double area() const { return 0; } };
struct SqNV : ShapeNV { double s; double area() const { return s*s; } };

SqNV a(3.0);
ShapeNV* p = &a;
```

Measured:

```
non-virtual: a.area()=9.0   but p->area()=0.0   <- static type wins
```

**The same object gave two different answers.** Called through `SqNV`, you got 9. Called through
`ShapeNV*`, you got 0 — because the compiler chose the function from the *declared type of the
pointer*, at compile time. It never looked at the object.

That is **static dispatch**, and it is what C does. It is also almost never what you want from a
hierarchy: a `std::vector<Shape*>` full of squares would report every area as zero.

## 2. With `virtual`, the Object Decides

```cpp
struct ShapeV { virtual double area() const { return 0; } virtual ~ShapeV() = default; };
struct SqV : ShapeV { double s; double area() const override { return s*s; } };
```

```
virtual    : b.area()=9.0   and p->area()=9.0    <- object decides
```

**`virtual` moves the decision from the pointer to the object**, and from compile time to run time.
That is the whole feature. Everything else in this lecture is how.

> **`virtual` is written once, in the base.** A function that is virtual in the base is virtual in every
> derived class whether or not you repeat the keyword. Write `override` instead (L13 §6) — it says the
> same thing and checks it.

---

## 3. The Mechanism

For the object to decide, **the object must carry the answer.** It does:

- Each **class** with virtual functions gets one **vtable** — a static array of function pointers, one
  per virtual function, shared by every object of that class.
- Each **object** gets one hidden **vptr**, pointing at its class's vtable.

A virtual call is then:

1. load the vptr from the object,
2. load slot *k* from the vtable,
3. call it.

Where *k* is a constant the compiler knows, because the slot order is fixed by declaration order in the
base.

### 3.1 What It Costs in Space

```cpp
struct Plain      { int x; void f(){} };
struct OneVirtual { int x; virtual void f(){} virtual ~OneVirtual()=default; };
struct TenVirtual { int x; virtual void a(){} /* ...ten of them... */ virtual ~TenVirtual()=default; };
```

Measured:

| Type | `sizeof` |
| --- | --- |
| `Plain` | **4** |
| `OneVirtual` | **16** |
| `TenVirtual` | **16** |
| `void*` | 8 |

Two things to read from this.

**The first virtual function costs 8 bytes per object** — the vptr — plus 4 bytes of padding here, so
`4` becomes `16`.

**The tenth costs nothing.** One vptr regardless of how many virtual functions, because the vtable is
per *class*, not per object. A hierarchy with fifty virtual functions has objects the same size as one
with a single virtual function.

> **This is why `sizeof` is a reliable test for "does this class have virtual functions".** And it is
> why adding one virtual function to a small, heavily-allocated type — a `Point`, a graph node — can
> be a genuine memory decision: an 8-byte `Point` becomes 24.

---

## 4. Looking At It

`Square` and `Circle` both override `area()` and `name()`. In GDB:

```
(gdb) info vtbl sq
vtable for 'Square' @ 0x555555557d00 (subobject @ 0x7fffffffd2b0):
[0]: 0x5555555553d6 <Square::area() const>
[1]: 0x5555555553fa <Square::name() const>

(gdb) info vtbl ci
vtable for 'Circle' @ 0x555555557cd0 (subobject @ 0x7fffffffd2c0):
[0]: 0x555555555450 <Circle::area() const>
[1]: 0x555555555480 <Circle::name() const>
```

**Two different tables, same slot layout.** Slot 0 is `area` for both, because `area` was declared
first in `Shape`. That fixed index is what makes the call a constant offset rather than a search.

Reading the vptr directly:

```
(gdb) p *(void**)&sq
$1 = (void *) 0x555555557d00 <vtable for Square+16>
```

**Note the `+16`.** The vptr does not point at the start of the vtable; it points 16 bytes in, past two
housekeeping words (an offset-to-top and a pointer to the `type_info` used by `dynamic_cast`). Slot 0
is at the vptr, slot 1 at vptr+8.

And walking the slots as raw pointers shows one `info vtbl` does not print:

```
(gdb) p ((void***)&sq)[0][2]
$3 = (void *) 0x555555555496 <Square::~Square()>
```

**The destructor is in the vtable too** — which is exactly what makes Lecture 15's virtual destructor
rule work.

**Lab 4 is this, done by you.**

---

## 5. What It Costs in Time

The textbook claim is "one extra indirection, negligible in most cases". Let us get a number.

### 5.1 Getting It Wrong Twice First

This is worth showing, because the first two attempts both produced plausible numbers that were
measuring something else.

**Attempt 1** — `std::vector<std::unique_ptr<Shape>>` against `std::vector<PlainSq>`:

```
non-virtual 5.4 ms    virtual 15.1 ms    ~2.8x
```

That comparison includes the vtable indirection, **plus** chasing a pointer to each object, **plus**
those objects being separate heap allocations scattered in memory. Three costs, one number.

**Attempt 2** — both stored contiguously by value, dispatching through a base reference:

```
non-virtual 5.5 ms    virtual 12.0 ms    ~2.2x
```

Better, and still wrong: `sizeof(Sq)` is 16 and `sizeof(PlainSq)` is 8, so **the virtual loop read
twice as many bytes.** Part of the gap is memory traffic, not dispatch.

**Attempt 3** — pad the plain type to 16 bytes so both loops touch identical memory:

| run | non-virtual | virtual | ratio |
| --- | --- | --- | --- |
| 1 | 6.95 ms | 15.91 ms | 2.29× |
| 2 | 10.86 ms | 13.30 ms | 1.23× |
| 3 | 8.02 ms | 23.16 ms | 2.89× |
| 4 | 7.75 ms | 16.11 ms | 2.08× |
| 5 | 9.92 ms | 17.32 ms | 1.74× |
| **mean** | **8.70 ms** | **17.16 ms** | **1.97×** |

Per call: **2.175 ns non-virtual, 4.290 ns virtual — a difference of about 2.1 ns.**

> **Each control changed the answer**, and the first version overstated the dispatch cost by roughly
> 40%. Note also the spread in attempt 3 — individual ratios range from 1.23× to 2.89×, which is why
> the mean of five runs is quoted rather than any single run.
>
> This is Lab 2's lesson from the other side. There, a correct measurement carried a wrong
> explanation. Here, three correct measurements answered three different questions, and only the third
> answered *"what does dispatch cost"*.

### 5.2 What the Number Means

**About 2 nanoseconds per call.** In a loop whose body is a single multiply, that doubles the runtime.
In a loop that does anything real — touches a string, allocates, reads a file — it disappears.

**The honest summary:** virtual dispatch is free in almost all code and matters in tight numeric loops,
which is exactly where you should not be using runtime polymorphism anyway.

---

## 6. The Compiler Is Cleverer Than the Model

Now look at what GCC actually emits for a virtual call at `-O2`:

```asm
_Z8via_baseRK5Shape:                     ; double via_base(const Shape& s) { return s.area(); }
        endbr64
        mov     rax, QWORD PTR [rdi]     ; load the vptr
        lea     rdx, _ZNK2Sq4areaEv[rip] ; address of Sq::area
        mov     rax, QWORD PTR [rax]     ; load vtable slot 0
        cmp     rax, rdx                 ; is it Sq::area?
        jne     .L8                      ; no  -> fall back to an indirect call
        movsd   xmm0, QWORD PTR 8[rdi]   ; yes -> the INLINED body
        mulsd   xmm0, xmm0
        ret
```

**That is not the three-step dispatch from §3.** GCC noticed that `Sq` is the only class deriving from
`Shape` in this translation unit, guessed that the target is `Sq::area`, and emitted a **guarded
inline copy** of it: compare the vtable slot against the expected function, and if it matches, run the
inlined body with no call at all.

This is **speculative devirtualization**. The branch is almost always taken and the predictor learns
it, so the real cost becomes a load, a compare, and a well-predicted branch — not an indirect call.

**It explains the measurement.** A true indirect call with an unpredictable target costs far more than
2 ns; 2 ns is about what a load-compare-predicted-branch costs.

### 6.1 What This Tells You

Three things worth carrying:

- **The model in §3 is what the language guarantees, not what the machine does.** Both matter, and they
  are different.
- **The optimization depends on the compiler being able to see all the derived classes.** Add another
  `Shape` subclass in another translation unit and the guess becomes unprofitable. **Your benchmark's
  answer depends on how much of the program the compiler can see** — which is why link-time
  optimization (`-flto`) exists.
- **`final` makes it certain.** Marking a class or function `final` tells the compiler no further
  override is possible, so it can devirtualize without a guard.

> **Do not conclude "virtual calls are free".** Conclude that your measurement measured *this program*,
> compiled *this way*, with *this many* derived classes visible. That is what a benchmark is.

---

## 7. When Virtual Costs More Than the Indirection

The 2 ns is not the whole story, and in real code it is usually the smaller part.

**A virtual call is an optimization barrier.** The compiler generally cannot:

- **inline** the callee — it does not know which one it is;
- **vectorize** a loop containing it, since it cannot batch calls to an unknown function;
- propagate constants across it, or reorder around it.

The vectorization part is directly observable. At `-O3`, GCC reports:

```
vecloop.cpp:6:80: optimized: loop vectorized using 16 byte vectors
```

Line 6 is the **non-virtual** loop. The virtual loop on line 7 is not in the report, and its assembly
contains one packed instruction against the non-virtual loop's three.

### 7.1 And Yet It Did Not Widen the Gap

Here is where the honest version diverges from the tidy one. If blocked vectorization dominated, the
ratio should be much worse at `-O3` — where the non-virtual loop vectorizes — than at `-O2`, where
neither does. Measured:

| | non-virtual | virtual | ratio |
| --- | --- | --- | --- |
| `-O2` *(no vectorization)* | 6.23 ms | 13.70 ms | **2.20×** |
| `-O3` *(non-virtual vectorizes)* | 5.61 ms | 12.49 ms | **2.23×** |

**Essentially unchanged.** Vectorizing made the non-virtual loop faster, and the virtual loop got
faster too, and the ratio did not move.

So for *this* kernel the barrier effect is not what the gap is made of. **The tidy claim that blocked
optimization dominates the indirection is a real mechanism and is not what these numbers show**, and
the difference between those two sentences is the point of this course.

The guidance survives, with its justification narrowed to what was measured:

> **Do not put a virtual call in the innermost loop of a numeric kernel.** Everywhere else, use it
> freely — the cost is not what stops your program being fast.

A kernel with a heavier, more vectorizable body than `s*s` would likely show the barrier effect
clearly. **Exercise 7 asks you to build one**, and it is the hardest exercise this week because you
have to make the mechanism visible rather than take it on trust.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| Without `virtual` | The **pointer's type** decides — same object gave 9.0 and 0.0 |
| With `virtual` | The **object** decides, at run time |
| Mechanism | vptr per object, vtable per class, fixed slot index |
| Space cost | First virtual function: **+8 bytes**. Tenth: **0** |
| The vtable in GDB | `info vtbl`; slot 0 = first declared virtual; destructor is in there too |
| vptr points to vtable **+16** | Past offset-to-top and `type_info` |
| Time cost | **≈2.1 ns per call**, ratio ≈1.97× on a loop that does nothing else |
| The measurement took three tries | Pointer-chasing, then object size, then the actual answer |
| Speculative devirtualization | GCC guards-and-inlines; the model is not the machine |
| Optimization barrier | Real and observable — the non-virtual loop vectorizes at `-O3`, the virtual one does not |
| …but it did not dominate here | Ratio 2.20× at `-O2`, 2.23× at `-O3`. **A mechanism being real is not the same as it explaining your number** |

---

## 9. Exercises

**1.** Measure `sizeof` for a class with 0, 1, 2 and 10 virtual functions. **Explain the pattern in one
sentence.** Then add a second data member and explain the new numbers.

**2.** Reproduce the three attempts in §5.1 — pointers, then contiguous-but-unequal-size, then
contiguous-and-equal. **Report all three ratios** and say what each one was measuring.

**3.** Compile a virtual call at `-O2 -S` and look for the `cmp`/`jne` pattern from §6. **Did your
compiler devirtualize?** Now add a second derived class and recompile. **Did it stop?**

**4.** Mark the derived class `final` and compare the assembly with and without. What changed?

**5.** Use GDB's `info vtbl` on two sibling classes. Confirm slot 0 is the same *function* in both.
Then swap the declaration order of two virtual functions in the **base** and show the slots move.

**6.** Write a hierarchy where the base declares `area()` non-virtual, store objects in a
`std::vector<Base*>`, and print each area. **Report the wrong answers**, then fix it with one keyword.

**7.** *(Hard, and open-ended.)* §7.1 found the ratio unchanged between `-O2` and `-O3`, so the
vectorization barrier did not dominate there. **Build a kernel where it does** — a loop body heavy
enough to vectorize well, run it both ways at both optimization levels, and show the ratio widening.

Report your numbers **even if you cannot make it happen.** A well-documented failure here is worth full
marks; the claim in §7 is a mechanism, and whether it dominates is an empirical question about your
loop.

---

## 10. Next

**Lecture 15** finishes the mechanism with the rules you cannot afford to get wrong: **pure virtual
functions** and abstract base classes, the **virtual destructor requirement** — which leaks memory
silently and which your build line only sometimes warns about — **object slicing**, and
`dynamic_cast`.

---

*PROG 102 · Week 4 · Lecture 14 · © CSE Department*
