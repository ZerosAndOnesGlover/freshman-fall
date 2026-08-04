# PROG 102 · Quiz 2
## Week 2 · Monday, start of lecture · 15 minutes · 20 points

**Covers Week 1** — Lectures 04–06: operator overloading, copy semantics, the Rule of Three,
copy-swap, and copy counting.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* This compiles:

```cpp
struct V { double x;
    V operator*(double s) const { return V{x*s}; }   // member
};
V v{2.0};
V a = v * 3.0;
```

but `V b = 3.0 * v;` does not.

**(a)** *(1)* Why not? One sentence.

**(b)** *(2)* Give the fix, as a declaration.

<br><br><br>

---

**Q2.** *(3)* A class has a destructor that calls `delete[]`, and no other special members.

**(a)** *(1)* Name the rule it violates.

**(b)** *(2)* Describe the failure that occurs, and say **when** it happens relative to the copy.

<br><br><br>

---

**Q3.** *(4)* Given this assignment operator and `a = a;`:

```cpp
Buf& operator=(const Buf& o) {
    delete[] d;
    n = o.n;
    d = new char[n];
    std::memcpy(d, o.d, n);
    return *this;
}
```

**(a)** *(2)* At the `memcpy`, what does `o.d` point to? Be precise.

**(b)** *(2)* The lecture insists this is **not** a use-after-free. Why not?

<br><br><br>

---

**Q4.** *(4)* The copy-swap operator:

```cpp
Buffer& operator=(Buffer o) { swap(o); return *this; }
```

**(a)** *(1)* Why does it need no `if (this == &o)` guard?

**(b)** *(2)* It provides the **strong** exception guarantee. Which property of the ordering gives it
that?

**(c)** *(1)* Why must `swap` be `noexcept`?

<br><br><br>

---

**Q5.** *(3)* With a `V3` that counts its copy constructor calls, compiled `-std=c++17 -O2`:

```cpp
V3 c = a + b;        // how many copy constructions?
```

**(a)** *(1)* State the number.

**(b)** *(2)* Adding `-fno-elide-constructors` does not change it. **Why not?**

<br><br><br>

---

**Q6.** *(3)* Fill in the table for a class with an `operator[]` pair:

| Called on | Which overload runs | Return type |
| --- | --- | --- |
| a non-`const` object | | |
| a `const` object | | |

**In one sentence, what breaks if you omit the `const` version?**

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 2 · Quiz 2 · © CSE Department*
