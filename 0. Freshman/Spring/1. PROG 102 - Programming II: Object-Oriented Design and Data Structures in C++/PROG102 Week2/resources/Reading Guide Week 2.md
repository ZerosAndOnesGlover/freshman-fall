# PROG 102 · Week 2 · Reading Guide
## *C++ Primer* Chapter 16, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| ***C++ Primer*** | **§16.1.1–16.1.3** | Function and class templates. The core reading. |
| ***C++ Primer*** | **§16.2.1–16.2.3** | Type deduction. Read carefully. |
| ***C++ Primer*** | **§16.3, §16.5** | Overloading with templates; specialization. |
| **Stroustrup** | **Ch. 23** | The designer's account of why templates exist. Reference, not cover-to-cover. |
| **cppreference** | *template argument deduction*, *class template* | More precise than either book |

**Skip for now:** §16.1.4 (member templates), §16.2.5–16.2.7 (`std::move`, forwarding, reference
collapsing). Those are **Week 5** and will make far more sense after move semantics.

> ***C++ Primer* is from 2012**, which for this chapter matters in two places. It has no coverage of
> **C++17 class template argument deduction** (`std::pair p{1, 2.0}` without the angle brackets), and
> its account of variadic templates is thinner than what you will meet in Week 11. Neither affects this
> week's work.

---

## §16.1.1 — Function Templates

**Guiding questions:**

1. The book uses `template <typename T>` and `template <class T>` interchangeably. **Is there any
   difference?** *(No — but say why the course prefers one.)*
2. §16.1.1 introduces **instantiation**. Write down, in one sentence, what the compiler does when it
   instantiates a template. Then check it against Lecture 07 §4.
3. The book notes that `inline` and `constexpr` go *after* the template parameter list. **Why is the
   position significant?**
4. **The most important question in the chapter:** the book says template code should "minimise the
   requirements placed on the argument types". Given Lecture 07 §5, where are those requirements
   *written down*? What does that mean for someone reading your template?

---

## §16.1.2 — Class Templates

**Guiding questions:**

1. The book states that each instantiation of a class template is an **independent class**. What does
   that mean for `Stack<int>` and `Stack<double>` — is there any relationship at all?
2. §16.1.2 covers defining members outside the class. **Write the signature for `Stack<T>::push` from
   memory**, then check. The three things people get wrong are listed in Lecture 08 §2.
3. Find where the book explains why template definitions go in headers. **Compare its explanation with
   the experiment in Lecture 08 §3** — the book asserts it, the lecture shows you the empty object file.
4. The book introduces `typename` for dependent types. **You will not fully appreciate this until Week
   6**; for now, just be able to recognise the error message.

---

## §16.2 — Template Argument Deduction

The section that repays slow reading.

**Guiding questions:**

1. §16.2.1 — the book explains that deduction permits only very limited conversions. **Which ones?**
   Then explain why `maxof(3, 7.5)` fails but `maxof<double>(3, 7.5)` succeeds.
2. §16.2.2 — explicit template arguments. **Why must non-deducible parameters come first?**
3. §16.2.3 — trailing return types. Skim; the `decltype` machinery is Week 11.
4. The book discusses `std::max` returning a reference. **Does it warn about the dangling-reference
   trap?** Compare with Lecture 07 §7, and note that your compiler now catches it.

---

## §16.5 — Template Specialization

**Guiding questions:**

1. The book stresses that a specialization is **not** an overload. What is the practical difference?
2. Why can class templates be *partially* specialized but function templates cannot? What do you use
   instead for functions?
3. §16.5 mentions that specializations must be declared before use. **What goes wrong if a
   specialization is declared after the generic version has already been instantiated for that type?**
   *(This is a real and nasty bug class — one-definition-rule violations that link fine and misbehave.)*
4. Look up `std::vector<bool>` on cppreference. **List two ways it does not behave like
   `std::vector<T>`.**

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux, `-std=c++17`.** Sizes, symbol names and line counts should match. Timings
will not, and the §L09 §3.2 garbage-free numbers are deterministic.

### L07 §4 — One template, several symbols

```
g++ -std=c++17 -O2 -c inst2.cpp -o inst2.o
nm -C inst2.o | grep maxof
nm    inst2.o | grep -i maxof
```

**Expect:** three `W` symbols, `_Z5maxofIiET_S0_S0_` / `Id` / `Il`.

> **If you see nothing**, your instantiations were inlined and discarded — add explicit instantiation
> (`template int maxof<int>(int,int);`) as the lecture does. This is the same disappearing-symbol trap
> as Lecture 01 §2.1, and it will catch you again in Lab 2 Part A.

### L07 §4.2 — Zero runtime cost

```
g++ -std=c++17 -O2 -S -masm=intel inst2.cpp -o inst2.s
sed -n '/^_Z5maxofIiET_S0_S0_:/,/ret/p' inst2.s
sed -n '/^_Z9maxof_intii:/,/ret/p'      inst2.s
```

**Expect:** identical bodies, `cmp / mov / cmovge / ret`.

### L08 §3 — The header rule

```
g++ -std=c++17 -c stack.cpp -o stack.o
g++ -std=c++17 -c main.cpp  -o main.o
g++ main.o stack.o -o prog          # 4 undefined references
nm -C stack.o                       # empty
```

Then append `template class Stack<int>;` to `stack.cpp` and repeat. **Expect:** it links, and `nm`
shows 8 symbols.

### L09 §3.2–3.3 — The cost, and the myth

```
python3 gen.py 100 > bloat_100.cpp
/usr/bin/time -f "%e" g++ -std=c++17 -O2 bloat_100.cpp -o bloat_100
size bloat_100
```

**Expect:** text 43,993 bytes. Then generate the hand-written equivalent and compare — **the same
43,993**.

### L09 §5 — Error message lengths

```
g++ -std=c++17 -c err_plain.cpp  -o /dev/null 2>&1 | wc -l     # 6
g++ -std=c++17 -c err_simple.cpp -o /dev/null 2>&1 | wc -l     # 5
g++ -std=c++17 -c err_stl.cpp    -o /dev/null 2>&1 | wc -l     # 78
```

---

## The Habit, Extended

Week 0: *do not believe a claim about C++ you have not seen a compiler make.* Week 1 applied it to
advice that was fifteen years out of date.

**Week 2 extends it one step further, and this is the harder version:**

> **A correct measurement can carry a wrong explanation.**

Lecture 09 §3.2's table is right. Code size *does* grow linearly with instantiations. The explanation
attached to it everywhere — "templates cause code bloat" — is wrong, and it takes one extra experiment
to find that out: write the same classes by hand and compare. **The same 43,993 bytes.**

Nobody would have caught that by reading more carefully. It needed a control.

**When you measure something this semester, ask what else would produce the same number.** That
question is the difference between data and evidence, and it is the one Lab 2 Part C exists to make you
ask.

---

## Before Week 3

1. Lectures 07–09 read.
2. *C++ Primer* §16.1–16.2 worked through; §16.5 skimmed.
3. **PS 2 Part B started** — the `Stack<T>` is the week's substance and Part B4 takes longer than it
   looks.
4. **Look up `std::vector` on cppreference before Monday.** Week 3 opens by comparing it to the
   `Stack<T>` you just wrote, and the comparison is much sharper if you have already noticed how many
   members it has.

---

*PROG 102 · Week 2 · Reading Guide · © CSE Department*
