# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 2: Templates and Generic Programming

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 2, Lab 2, Quiz 2 (Monday, covers Week 1)

---

### Why This Week Exists

You have now written the same class twice. Week 0's `IntStack` holds `int`s. Lab 1's `Roster` holds
`char*`s. The allocation logic, the growth logic, the Rule of Three — **identical in both**, and
copied by hand.

C is stuck there. The C answer is `void*` and a size parameter, which throws away every type check you
had. **C++'s answer is to make the type a parameter**, and the result is not merely convenient: it is
*free*.

That word is the week's subject, and it is measured rather than asserted. `TStack<int>::push` and a
hand-written `IStack::push` compile to **instruction-identical** machine code — verified, 11
instructions each. The abstraction costs nothing at runtime because it does not exist at runtime; the
compiler generated the class you would have written.

**What it does cost is compile time and code size**, and Lab 2 measures both.

### Learning Objectives

By the end of Week 2, you should be able to:

1. Write function templates and explain how `T` is deduced from the arguments.
2. Say when deduction fails and supply an explicit template argument.
3. Write a class template with a full Rule of Three, and explain why the definitions must be visible
   to every translation unit that uses them.
4. Explain what "instantiation" means, and read a mangled name to identify which instantiation a
   symbol belongs to.
5. Write full and partial specializations, and say which one applies to a given type.
6. Use non-type template parameters and explain what `FixedArray<int, 8>` costs.
7. **Measure** the compile-time and code-size cost of instantiation, and state what it is *not* caused
   by.
8. Explain how C++ templates differ from Java generics and Python duck typing, in terms of when the
   type is known.
9. Read a 78-line template error message and find the three lines that matter.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 Function Templates and Type Deduction]] | Syntax, deduction, explicit arguments, overload interaction |
| [[L08 Class Templates and Generic Containers]] | `Stack<T>`, the header rule, non-type parameters, `pair` and `tuple` |
| [[L09 Instantiation Specialization and Cost]] | Specialization, the cost measured, error messages, vs Java and Python |
| [[PS 2 A Generic Stack]] | Due Friday of Week 3 |
| [[PROG102 Week2/assignments/QUIZ 2 Week 2 Monday\|QUIZ 2 Week 2 Monday]] | 15 minutes, covers Week 1 |
| [[LAB 2 What Templates Cost]] | Measure compile time, binary size and runtime yourself |
| [[PROG102 Week2/resources/Reading Guide Week 2\|Reading Guide Week 2]] | *C++ Primer* Ch. 16, and every command to reproduce this week |
| [[PROG102 Week2/solutions_instructor/PS 2 Solutions\|PS 2 Solutions]] | Instructor only |
| [[PROG102 Week2/solutions_instructor/LAB 2 Solutions\|LAB 2 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**A template is not a class. It is instructions for writing classes.**

`Stack` is not a type and you cannot make one. `Stack<int>` is a type, and it exists only because you
asked for it somewhere in your program. `Stack<int>` and `Stack<double>` are **as unrelated as
`int` and `std::string`** — separate symbols, separate machine code, no shared implementation.

That single fact explains everything else this week: why the definitions must be in headers, why the
error messages are long, why specialization is possible at all, and why the runtime cost is zero.

### The Measurement That Corrects a Myth

You will hear that templates cause **code bloat**. Lab 2 measures it, and the honest result is worth
stating up front:

| | compile | text size |
| --- | --- | --- |
| `Stack<T>` instantiated for 100 types | 1.55 s | **43,993 bytes** |
| 100 equivalent classes written by hand | 1.84 s | **43,993 bytes** |

**Byte for byte identical**, and the hand-written version compiles *slower*.

**Templates did not cause the bloat.** Using 100 distinct types caused it, and the template is merely
the reason you could do that without noticing. That distinction is the difference between "avoid
templates" — which is wrong — and "know how many instantiations you are asking for", which is the
actual engineering advice.

### Assessment Reminder

**Quiz 2 is Monday and covers Week 1** — operator overloading, the Rule of Three, copy-swap, and copy
counting.

**Bring Lab 1's repaired `Roster`.** Lab 2 and PS 2 both build on it, and a `Roster` whose Rule of
Three is wrong becomes a *template* whose Rule of Three is wrong — which produces the 78-line error
messages of §L09 rather than the four-line ones you are used to.

### Connections

**Back:** the Rule of Three from **Week 1** is written once here and inherited by every instantiation.
`operator[]`, `operator<<` and the `const` pair from **Lecture 04** all reappear as template members.
Weak symbols and the One Definition Rule from **Lecture 03** §4 are exactly why templates behave as
they do at link time.

**Forward:** **Week 3** is the STL, which is this week applied at scale — `std::vector` is `Stack<T>`
done properly, and `std::sort` works on your types only if you gave them `operator<`. **Week 6**
implements a templated linked list and BST with iterators. **Week 11**'s lambdas are class templates
the compiler writes for you.

---

*PROG 102 · Week 2 · © CSE Department*
