# PROG 102 · Lab 4 — Solutions and Checkoff Notes
## Reading the vtable in GDB

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Three things, said before anyone opens a debugger:**

1. **`-O0 -g`, always, in this lab.** At `-O2` the compiler devirtualizes (L14 §6), inlines, and elides
   the objects. Students who build optimized will find `info vtbl` reporting nothing useful and will
   spend forty minutes on it.
2. **Decline the debuginfod prompt**, or `set debuginfod enabled off`. It stalls the session on a slow
   network for no benefit.
3. **Addresses will differ from the reference and from each other.** ASLR. Mark the *structure*.

**Part C is the highlight** — watching the vptr change mid-construction — and it is the one most likely
to be cut for time. **Protect it.** Budget A 25 min, B 30 min, C 30 min, D 15 min, 20 min slack.

**GDB familiarity varies enormously.** Have the four commands on the board from the start:

```
break <line>     run     p <expr>     info vtbl <obj>
```

That is the entire command set this lab needs.

---

## Part A — Find the vptr (12)

### A1 (4)

`sizeof(Shape)` = **8**, `sizeof(Square)` = **16**.

`Square` has one `double` (8 bytes) plus the vptr (8) = 16. **`Shape` has no data members at all** and
is still 8, because it has virtual functions and therefore a vptr — the empty-class-is-1 rule from L01
§3.1 does not apply once there is a vptr to store.

*Marking: 2 the numbers, 2 accounting for the bytes. **A student who says `Shape` is 8 "because it's
empty" has it backwards** — an empty class is 1; this one is 8 because of the vptr.*

### A2 (4)

```
$1 = (void *) 0x555555557d00 <vtable for Square+16>
$2 = (void *) 0x555555557cd0 <vtable for Circle+16>
```

The first eight bytes of each object are the **vptr**, pointing at that class's vtable.

*Marking: 2 both values, 2 identifying them as vptrs pointing to per-class tables.*

### A3 (4)

The vptr points **16 bytes past the start** of the vtable, skipping two housekeeping words: the
offset-to-top (for multiple inheritance) and a pointer to the `type_info` used by `dynamic_cast`.
Slot 0 sits at the vptr itself.

*Marking: 4. **Accept "two words of metadata before the function pointers"** without naming both — the
key idea is that the vptr does not point at the table's start. Naming `type_info` and connecting it to
`dynamic_cast` (L15 §4.2) is worth a commendation.*

---

## Part B — Walk the Table (12)

### B1 (4)

```
vtable for 'Square' @ 0x555555557d00 (subobject @ 0x7fffffffd2b0):
[0]: 0x5555555553d6 <Square::area() const>
[1]: 0x5555555553fa <Square::name() const>

vtable for 'Circle' @ 0x555555557cd0 (subobject @ 0x7fffffffd2c0):
[0]: 0x555555555450 <Circle::area() const>
[1]: 0x555555555480 <Circle::name() const>
```

Slot 0 is `area` in both because **the index is assigned by declaration order in the base**. That fixed
index is what lets the call site use a constant offset instead of searching.

*Marking: 2 both dumps, 2 the reason including the constant-offset consequence.*

### B2 (4)

```
$1 = (void *) 0x5555555553d6 <Square::area() const>
$2 = (void *) 0x5555555553fa <Square::name() const>
$3 = (void *) 0x555555555496 <Square::~Square()>
```

**Slot 2 is the destructor.** Its presence in the table is exactly what makes a virtual destructor
work — `delete` through a base pointer looks it up like any other virtual function and finds the
derived one.

*Marking: 2 the three values, 2 identifying slot 2 and connecting it to L15 §2. **The connection is the
assessed half.***

*(Students may see two destructor entries — the complete and deleting destructors. Accept either; if
they ask, the second is the one that also calls `operator delete`.)*

### B3 (4)

Swapping the base's declarations swaps the slots in every derived vtable.

The library question: **a base class that adds or reorders a virtual function changes every derived
class's slot indices.** Derived classes compiled against the old header call the wrong slot — no
compile error, no link error, wrong function at run time.

*Marking: 2 the observation, 2 the consequence. **This is the binary-compatibility problem** and a
student who names it should be told they have found the reason mature C++ libraries almost never touch
a published base class.*

---

## Part C — Watch It Change (10)

The best ten minutes of the session.

### C1 (6)

Printing `*(void**)this` at both breakpoints:

```
  in Shape():  vptr = 0x5f8b1b8d6d50
  in Square(): vptr = 0x5f8b1b8d6d28
  after ctor:  vptr = 0x5f8b1b8d6d28
```

**Two different values.** During `Shape`'s constructor the object's vptr points at **`Shape`'s**
vtable; by the time `Square`'s constructor body runs it points at `Square`'s.

*Marking: 4 both values captured, 2 noting they differ. Addresses are irrelevant; the difference is
everything.*

### C2 (4)

The vptr is set **per stage of construction**: while a base constructor runs, the derived part is not
yet initialized, so the object is treated as being of the base's type. A virtual call therefore
dispatches to the **base's** implementation.

Demonstrated:

```
  in Shape():  ... report() says: Shape
  in Square(): ... report() says: Square
  after ctor:  ... report() says: Square
```

**`Shape::report()` ran even though the object was going to be a `Square`.** No warning, no error.

*Marking: 2 the explanation, 2 the demonstration. **A student who predicted "Square" and was surprised
has learned the thing**; note it approvingly. The rule from L13 §4.1 is now something they have watched
rather than been told.*

---

## Part D — Slicing, in Memory (6)

### D1 (4)

```
(gdb) p *(void**)&sq
$1 = <vtable for Square+16>
(gdb) p *(void**)&base
$2 = <vtable for Shape+16>
```

**The copy has `Shape`'s vptr.**

*Marking: 4 both values with the observation.*

### D2 (2)

Expected: *slicing copies only the base sub-object, and the base sub-object's vptr is the base's — so
the copy is genuinely a `Shape` and virtual dispatch on it finds `Shape`'s functions.*

*Marking: 2. **The answer must be in terms of the vptr**, as the question demands. "The derived part is
lost" is the textbook phrasing and scores 1 — true, and not what was asked.*

---

## Checkoff Checklist

1. Built at **`-O0 -g`**.
2. A1 accounts for `Shape` being 8 bytes **because of the vptr**, not because it is empty.
3. B2 identifies slot 2 as the destructor and connects it to the virtual destructor rule.
4. **Part C completed** — both vptr values captured.
5. D2 phrased in terms of the vptr.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 12 |
| B | 12 |
| C | 10 |
| D | 6 |
| **Total** | **40** |

---

## Note for the Lab

Close on the general point, not on the mechanism.

> **Everything in this course has a representation you can print.** The `this` pointer was a register
> in Week 0. A template instantiation was a symbol in Week 2. An iterator category was a tag type in
> Week 3. Today the vtable was an array at an address, and the vptr was the first eight bytes of your
> object.

Then the honest part, which is worth saying in midterm week:

> **None of this is advanced.** It is `sizeof`, `nm`, `-S` and four GDB commands. What separates a
> programmer who knows what their code does from one who believes what they were told is not talent —
> it is the habit of going and looking, and you have now done it four times.

If there is time, connect Part C to Part D out loud: **both are the same fact.** The vptr says what the
object currently is. During base construction it says "base". After a slicing copy it says "base". In
both cases virtual dispatch is telling you the truth about an object that is not what you thought it
was.

**Midterm 1 is next week.** Point at the revision guide's Section D table before they leave.

---

*PROG 102 · Week 4 · Lab 4 Solutions · © CSE Department*
