# CS 211 · Programming Languages & Compilers I
## Week 0 · Lecture 1 of 2
### What a Language Is — and Why There Are So Many

---

**Reading:** SICP §1.1 · Dragon §1.1–1.2 · **Next:** L02, grammars and the shape of a program

---

## 1. The Question

You have written a year of programs in Python, C and C++. In all that time, something decided what you were *allowed to write* — which words were keywords, where a semicolon was required, whether `x + y` meant anything when `x` was a string and `y` was a number.

**Somebody decided all of that.** Not a committee of nature. People, in rooms, making trade-offs, mostly between 1957 and 1995, and mostly for reasons that are still legible if you know where to look.

This course is about those decisions and about the machinery that enforces them. By Week 11 you will have written the machinery yourself.

---

## 2. Syntax Is Not Semantics — and the Difference Costs Money

Here is the whole distinction in two lines of arithmetic.

```c
#include <stdio.h>
int main(void) { printf("C:      -7 / 2 = %d,  -7 %% 2 = %d\n", -7 / 2, -7 % 2); return 0; }
```

```python
print(f'Python: -7 // 2 = {-7 // 2}, -7 %  2 = {-7 % 2}')
```

```
C:      -7 / 2 = -3,  -7 % 2 = -1
Python: -7 // 2 = -4, -7 %  2 = 1
```

*(Measured. gcc 13.3.0 `-O2`, Python 3.14.2.)*

**Same operation, same operands, different answers.** And neither language is wrong. Both preserve the division identity that any sane definition must:

| | quotient | remainder | $q \times b + r$ |
|---|---:|---:|---:|
| **C** — truncate toward zero | $-3$ | $-1$ | $-3 \times 2 + (-1) = -7$ ✓ |
| **Python** — floor toward $-\infty$ | $-4$ | $+1$ | $-4 \times 2 + 1 = -7$ ✓ |

Two self-consistent designs. **The syntax is identical and the semantics are not**, which is the single most important distinction in this course. Syntax is what a program *looks like*. Semantics is what it *means*. A parser checks the first. Nothing but careful specification checks the second.

### Why each chose what it chose

Compile C's division and look:

```
$ gcc -O2 -c divf.c && objdump -d -M intel --no-show-raw-insn divf.o
```

```
0000000000000000 <cdiv>:
   0:   endbr64
   4:   mov    eax,edi
   6:   cdq
   7:   idiv   esi
   9:   ret
```

**One instruction.** `idiv` truncates toward zero because that is what the x86-64 hardware does, and C's rule *is* the hardware's rule. C's designers picked the semantics that cost nothing.

Python picked the semantics that mathematicians expect — where `a % b` always has the sign of `b`, so `-7 % 2` is a legitimate index into a 2-element list and `-3 % 2` is too. That rule cannot be one `idiv`; it needs a correction step. **Python paid instructions to buy an invariant.**

> **This is habit 2 from the syllabus, in its smallest possible form.** C refused to deviate from the
> ISA and bought speed. Python refused to surprise a mathematician and bought a modulo you can index
> with. Neither is free. Every language decision in the next twelve weeks has this shape, and part
> of what you are learning is to see the trade before somebody points at it.

---

## 3. One Problem, Four Paradigms

*"Give me the names of everyone over thirty, alphabetically."*

The answer is the same three-element list every time. **What differs is how much of the *how* you were required to supply.**

**Imperative** — you supply all of it. State, iteration order, accumulation, sorting.

```python
people = [('Ada', 36), ('Alan', 24), ('Grace', 45)]
out = []
for n, a in people:
    if a > 30:
        out.append(n)
out = sorted(out)
```

**Functional** — you supply the transformation, not the loop. No mutable accumulator, no index.

```python
out = sorted(n for n, a in people if a > 30)
```

**Declarative** — you supply the *shape of the answer*. Nothing about how to find it.

```sql
SELECT name FROM person WHERE age > 30 ORDER BY name;
```

**Logic** — you supply facts and a rule, and ask a question.

```prolog
person(ada, 36).  person(alan, 24).  person(grace, 45).
older_than(N, X) :- person(N, A), A > X.
?- older_than(N, 30).
```

All four produce `Ada, Grace`. *(Python 3.14.2 and SQLite 3.45.1 measured; you run all four yourself, Prolog included, in Lab 0 Part 1.)*

**Read down that list and one thing is monotonically decreasing: how much you had to say.** Read it the other way and something else is decreasing: how much you get to control. The SQL query does not tell you whether the database scanned the table or used an index — and on ten rows you do not care, and on ten billion rows it is the only thing you care about.

> **A paradigm is not a language feature.** Python wrote two of those four. Paradigms are *styles of
> saying what you want*, and modern languages are nearly all multi-paradigm — which is Week 12's
> subject, and the reason the word "functional language" is less useful in 2026 than it was in 1990.

---

## 4. A Program Is a Tree

Here is the idea the rest of the course rests on.

**A program is not a string of characters.** It is written down as one, and that is an encoding accident. What a program *is* — the thing the compiler manipulates, the thing that has meaning — is a **tree**.

Python will show you its own:

```python
>>> import ast
>>> print(ast.dump(ast.parse("1 + 2 * 3", mode="eval"), indent=2))
```

```
Expression(
  body=BinOp(
    left=Constant(value=1),
    op=Add(),
    right=BinOp(
      left=Constant(value=2),
      op=Mult(),
      right=Constant(value=3))))
```

**The multiplication is nested inside the addition.** That is precedence — not a rule applied afterwards by the evaluator, but a fact about the shape of the tree, decided when the string was parsed. By the time anything runs, "precedence" no longer exists as a concept. There is only a tree, and you evaluate a tree bottom-up.

Now parenthesise it:

```python
>>> print(ast.dump(ast.parse("(1 + 2) * 3", mode="eval"), indent=2))
```

```
Expression(
  body=BinOp(
    left=BinOp(
      left=Constant(value=1),
      op=Add(),
      right=Constant(value=2)),
    op=Mult(),
    right=Constant(value=3)))
```

**The tree flipped, and the parentheses are gone.** There is no `Paren` node. There never was one — parentheses are an instruction to the parser about what tree to build, and once it is built they have done their job and evaporated.

**That is what an Abstract Syntax Tree is**, and the word doing the work is *abstract*: it keeps the structure and discards the notation. Semicolons, parentheses, whitespace, the choice between `and` and `&&` — all gone. Two programs that differ only in notation produce the identical AST, which is exactly what you want, because they mean the identical thing.

---

## 5. The Eight Translations

A compiler is not one transformation. It is a chain of them, each with a named input and a named output, and **at every moment in this course you should know which link you are holding.**

| # | Phase | In | Out | Week |
|---|---|---|---|---|
| 1 | **Lexer** | source text | tokens | 1 |
| 2 | **Parser** | tokens | parse tree | 2 |
| 3 | **AST build** | parse tree | AST | 2 |
| 4 | **Semantic analysis** | AST | typed AST + symbol table | 3 |
| 5 | **IR generation** | typed AST | three-address code | 4 |
| 6 | **Optimisation** | TAC / SSA | better TAC / SSA | 5 |
| 7 | **Code generation** | IR | LLVM IR | 11 |
| 8 | **Back end** | LLVM IR | machine code | 11 *(LLVM's job)* |

**Every one of those intermediate forms can be printed.** That is not incidental — it is the entire debugging methodology of this course, and it is why `cyanc` will grow a `--dump` flag in Week 1 and never lose it.

> **When your compiler produces a wrong answer, do not read the Cyan program.** The Cyan program is
> fine. Dump each representation in order and find the first one that is not what you expected; the
> bug is in the phase that produced it. This sounds obvious written down and is astonishingly hard
> to do under time pressure in Week 11, which is why you start practising it in Week 1.

**The front end is phases 1–4** — everything that depends on the source language. **The back end is 7–8** — everything that depends on the target machine. The IR in the middle is what lets them be separated, and that separation is why LLVM exists, why Rust and Swift and Clang all got x86, ARM and WebAssembly back ends without writing three each, and why Week 11 is a short week rather than a catastrophic one.

---

## 6. Compiler or Interpreter? The Line Is Blurrier Than You Were Told

The tidy version: a compiler translates the whole program to machine code ahead of time; an interpreter walks the AST and executes as it goes.

**The tidy version describes almost nothing in current use.**

- **CPython** compiles your source to bytecode — a real IR, phases 1 through 5 — then interprets the bytecode. It is both.
- **Java** compiles to bytecode ahead of time, then the JVM *compiles the hot parts to machine code while running*. That is a JIT, and it can beat an ahead-of-time compiler because it knows which branch actually gets taken.
- **JavaScript engines** interpret first and compile the functions that turn out to matter, sometimes several times at increasing optimisation levels, and de-optimise back when an assumption breaks.

**What is genuinely fixed is the pipeline, not the timing.** Phases 1–4 happen for every language that has ever run, whether at build time or a microsecond before execution. What varies is *when* — and Week 11 shows you a JIT doing phases 5–8 at runtime, on your own compiler.

---

## 7. What to Take Away

1. **Syntax is form; semantics is meaning.** `-7 / 2` is one syntax with at least two defensible meanings, and languages differ on which they picked.
2. **Every language decision is a trade**, and the trade is usually legible — C's division is one `idiv` because C chose the hardware's answer.
3. **A paradigm is a choice about how much of the "how" you must supply**, not a property of a language. Python did two of the four.
4. **A program is a tree.** Parentheses and precedence are instructions for *building* the tree and do not survive into it.
5. **A compiler is eight named translations**, each with a printable output. Debugging is finding the first one that is wrong.

---

## Exercises

1. Python's `-7 % 2` is `1`; C's is `-1`. Give a concrete programming task where Python's answer is clearly the more useful one, and one where C's is. *(Hint for the first: circular buffers.)*
2. C's `/` compiles to a single `idiv`. Write, in C, what Python's `//` would have to do on top of `idiv` to get $-4$ instead of $-3$. How many extra instructions is that, and does the correction ever fire for positive operands?
3. The SQL query says nothing about *how* to find the rows. Name one thing the database can therefore do that the Python `for` loop cannot, and one thing that becomes harder for the programmer as a direct result.
4. `ast.parse("(1 + 2) * 3")` produces no node representing the parentheses. If the parentheses leave no trace, how does the tree still record that they were there? Answer in one sentence.
5. A JIT can outperform an ahead-of-time compiler on the same source. Give the reason, in terms of information one of them has and the other does not.

---

*Next: L02 — grammars. How a finite set of rules decides which of the infinitely many strings are programs, and what goes wrong when the rules admit more than one answer.*
