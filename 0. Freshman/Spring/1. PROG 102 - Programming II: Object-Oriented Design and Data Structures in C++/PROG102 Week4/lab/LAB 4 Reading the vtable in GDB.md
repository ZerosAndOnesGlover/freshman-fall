# PROG 102 · Lab 4
## Reading the vtable in GDB

**Date:** Monday 22 February 2027 · 15:00–16:50 · Lab section (Week 5) — covers Week 4 (L13–L15)
*2-hour lab · 40 points · in-lab checkoff · part of the Labs component (20%)*
**Deliverable:** `shapes_gdb.cpp`, `RESULTS.md` with your GDB transcripts. In-lab checkoff.

---

## Purpose

Lecture 14 described the vtable. **This session is you finding it in memory.**

Everything in that lecture — the vptr, the fixed slot order, the destructor being dispatched, the
reason slicing destroys polymorphism — is visible in a debugger in about ninety minutes. After this
lab, "virtual dispatch" should be a thing you have *looked at*, not a diagram you were shown.

You will also watch the vptr **change during construction**, which is the single most convincing
demonstration of why you must not call virtual functions from a constructor.

> **Build everything in this lab at `-O0 -g`.** At `-O2` the compiler devirtualizes, inlines, and
> optimizes away the objects you are trying to inspect. This is the one lab where optimization is the
> enemy.

---

## Setup

Write `shapes_gdb.cpp` with:

```cpp
struct Shape {
    virtual double area() const { return 0; }
    virtual const char* name() const { return "Shape"; }
    virtual ~Shape() = default;
};
struct Square : Shape {
    double s;
    explicit Square(double v) : s(v) {}
    double area() const override { return s * s; }
    const char* name() const override { return "Square"; }
};
struct Circle : Shape { /* r_, area, name, same shape */ };

int main() {
    Square sq(3.0);
    Circle ci(2.0);
    Shape* shapes[2] = { &sq, &ci };
    for (Shape* s : shapes) std::printf("%s %.4f\n", s->name(), s->area());
    return 0;                     // put your breakpoint here
}
```

```
g++ -std=c++17 -O0 -g shapes_gdb.cpp -o shapes_gdb
gdb ./shapes_gdb
```

If GDB offers to download debuginfo, decline — or `set debuginfod enabled off`.

---

## Part A — Find the vptr (12 pts)

**A1.** *(4)* Break at the `return 0;` line and run. Report `sizeof(Shape)`, `sizeof(Square)` and
`sizeof(Circle)`:

```
(gdb) p sizeof(Shape)
(gdb) p sizeof(Square)
```

**Account for every byte of `Square`.** It has one `double`. Where does the rest come from?

**A2.** *(4)* Print the first 8 bytes of each object, interpreted as a pointer:

```
(gdb) p *(void**)&sq
(gdb) p *(void**)&ci
```

Report both. **They differ. Say what each one is.**

**A3.** *(4)* Your output for `sq` should end in something like `<vtable for Square+16>`.

**Explain the `+16`.** *(Hint: Lecture 14 §4. The vptr does not point at the start of the table.)*

---

## Part B — Walk the Table (12 pts)

**B1.** *(4)* Dump both vtables:

```
(gdb) info vtbl sq
(gdb) info vtbl ci
```

Paste both. **Confirm slot 0 holds the same function *name* in each**, and state why the index is the
same for both classes.

**B2.** *(4)* `info vtbl` does not show everything. Read the slots as raw pointers:

```
(gdb) p ((void***)&sq)[0][0]
(gdb) p ((void***)&sq)[0][1]
(gdb) p ((void***)&sq)[0][2]
```

**Report all three.** Slot 2 is not in the `info vtbl` output — **what is it, and why does its presence
there matter?** *(This is the mechanism behind Lecture 15 §2.)*

**B3.** *(4)* Swap the declaration order of `area` and `name` **in `Shape`**, rebuild, and dump the
vtables again.

**Report what moved.** Then answer: if a library ships a base class and you recompile only your derived
class after the library adds a virtual function in the middle, what happens?

---

## Part C — Watch It Change (10 pts)

This is the part that explains L13 §4.1.

**C1.** *(6)* Add a constructor body to `Shape` and to `Square` so you can break inside each. Set
breakpoints in both, and construct a `Square`.

At each stop, print `p *(void**)this`.

**Report the value at both breakpoints.** They are different.

**C2.** *(4)* Explain what you saw, and connect it to the rule "never call a virtual function from a
constructor".

Then *(2 of the 4)*: add a virtual function called from `Shape`'s constructor and overridden in
`Square`. **Which implementation runs?** Confirm it with a print, and say why your Part C1 observation
predicts it.

---

## Part D — Slicing, in Memory (6 pts)

**D1.** *(4)* Create a `Square sq(3.0)` and then `Shape base = sq;` (a slicing copy).

Print the vptr of both:

```
(gdb) p *(void**)&sq
(gdb) p *(void**)&base
```

**Report both and say what happened to the copy.**

**D2.** *(2)* In one sentence, explain object slicing **in terms of the vptr** rather than in terms of
"the derived part is lost".

---

## Submission

- `shapes_gdb.cpp`
- `RESULTS.md` — every GDB transcript, in order, with your written answers.
- **Machine, OS, compiler and GDB version at the top.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 12 | Finding the vptr and accounting for object size |
| B | 12 | Reading the table, including the slot `info vtbl` hides |
| C | 10 | Watching the vptr change during construction |
| D | 6 | Slicing, explained as a vptr overwrite |
| **Total** | **40** | |

---

## Reference Transcript

g++ 13.3.0, GDB 15.x, x86-64 Linux, `-O0 -g`.

**A1:** `sizeof(Shape)` = **8**, `sizeof(Square)` = **16** (vptr 8 + `double` 8).

**A2 / A3:**

```
(gdb) p *(void**)&sq
$1 = (void *) 0x555555557d00 <vtable for Square+16>
(gdb) p *(void**)&ci
$2 = (void *) 0x555555557cd0 <vtable for Circle+16>
```

**B1:**

```
vtable for 'Square' @ 0x555555557d00 (subobject @ 0x7fffffffd2b0):
[0]: 0x5555555553d6 <Square::area() const>
[1]: 0x5555555553fa <Square::name() const>

vtable for 'Circle' @ 0x555555557cd0 (subobject @ 0x7fffffffd2c0):
[0]: 0x555555555450 <Circle::area() const>
[1]: 0x555555555480 <Circle::name() const>
```

**B2:**

```
$1 = (void *) 0x5555555553d6 <Square::area() const>
$2 = (void *) 0x5555555553fa <Square::name() const>
$3 = (void *) 0x555555555496 <Square::~Square()>
```

**Addresses will differ on your machine** (ASLR, and different code layout). The *structure* will not.

---

## What This Lab Is Really Showing

Three things, and the third is the one worth keeping.

**One:** the vtable is not a metaphor. It is an array of function pointers at a real address, and the
vptr is the first eight bytes of your object. You can print both.

**Two:** the slot index is fixed by the base's declaration order, which is why the call is a constant
offset and not a search — and why B3's question about a library adding a virtual function in the middle
has an unpleasant answer. **That is the binary-compatibility problem**, and it is why mature C++
libraries are so reluctant to change a base class.

**Three, and the general one:** every abstraction in this course has a representation you can inspect.
The `this` pointer was a register in Week 0. A template instantiation was a symbol in Week 2. Iterator
categories were tag types in Week 3. The vtable is an array in memory.

**None of this is advanced technique.** It is `sizeof`, `nm`, `-S` and a debugger, and the habit of
reaching for them is most of what separates a programmer who *knows* what their code does from one who
believes what they were told about it.

---

*PROG 102 · Week 4 · Lab 4 · © CSE Department*
