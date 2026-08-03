# PROG 102 · Quiz 1
## Week 1 · Monday, start of lecture · 15 minutes · 20 points

**Covers Week 0** — Lectures 00–03: C++ syntax, classes and `this`, constructors and destructors,
encapsulation, `const`, `inline`, namespaces.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* This member function and this free function compile to byte-identical assembly:

```cpp
void Counter::add(int n) { value += n; }
void add_free(Counter* c, int n) { c->value += n; }
```

**(a)** What is the name of the hidden first parameter the member function receives?

**(b)** On x86-64, which register carries it?

**(c)** In one sentence, what does this tell you a member function *is*?

<br><br><br>

---

**Q2.** *(3)* Given:

```cpp
struct A { int x; double y; };
struct B { int x; double y; void f(); void g(); void h(); };
struct C { };
```

**(a)** `sizeof(A)` is 16. What is `sizeof(B)`?

**(b)** What is `sizeof(C)`?

**(c)** Why is your answer to (b) not 0?

<br><br><br>

---

**Q3.** *(3)* What does this print? Write the output exactly.

```cpp
struct N { const char* s; N(const char* n):s(n){ std::printf("+%s ", s); }
                          ~N(){ std::printf("-%s ", s); } };
int main() { N a("a"); { N b("b"); } N c("c"); }
```

<br><br><br>

---

**Q4.** *(3)* Consider:

```cpp
struct Timer { int ticks = 0; int read() { return ticks; } };
const Timer t;
int x = t.read();
```

This does not compile. The error says *"passing `const Timer` as `this` argument discards qualifiers"*.

**(a)** *(1)* What one-word change to `read()` fixes it?

**(b)** *(2)* What is the **type** of `this` inside `read()` before and after that change?

<br><br><br>

---

**Q5.** *(4)* Given:

```cpp
struct Wrong {
    int* data;
    int  size;
    Wrong(int n) : size(n), data(new int[size]) {}
};
```

**(a)** *(2)* In what order are `data` and `size` actually initialized, and why?

**(b)** *(2)* There is a bug. State it in one sentence, and give the one-line fix that works
regardless of how the members are declared.

<br><br><br>

---

**Q6.** *(2)* Putting `int square(int x) { return x*x; }` in a header and including it from two `.cpp`
files gives a linker error. Adding `inline` fixes it.

**In one sentence, what does `inline` change?** *(A statement about speed scores 0.)*

<br><br><br>

---

**Q7.** *(2)* Name the **only** difference between `class` and `struct` in C++.

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 1 · Quiz 1 · © CSE Department*
