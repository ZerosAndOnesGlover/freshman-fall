# PROG 101 — Week 3
## Functions and Structured Programming

---

## This Week

Week 2 gave you expressions and control flow — enough, by Böhm–Jacopini, to compute anything. This
week is about the unit that makes that usable at scale: the **function**.

Three ideas, in order. First, **pass by value**: every argument is copied, so a function cannot
modify its caller's variables. This is the rule students fight hardest, because it makes `swap`
impossible to write with the tools you currently have — and it is the reason Week 5 exists.

Second, **the call stack**. Frames are not a metaphor. You will print addresses and watch them march
downward, 32 bytes at a time, and then see the same structure in GDB's `backtrace`. Once the stack is
concrete, storage duration, scope, and the dangling pointer all follow from it.

Third, **multi-file programs**. A header is a promise, a `.c` file is a definition, and `static` at
file scope withholds a symbol from the linker. The exercise where a program compiles cleanly and then
fails to link is the one that teaches this properly — the compiler and the linker check different
things, and finding out which stage rejected you is a skill.

| Day | Session | Topic | Duration |
|-----|---------|-------|----------|
| Tuesday | **Quiz 2** + Lecture 1 | Functions and pass-by-value | 50 min |
| Wednesday | Lecture 2 | The call stack and scope | 50 min |
| Thursday | Lecture 3 | Structured programming and multi-file discipline | 50 min |
| Monday | **Lab 3** | Functions, the call stack, and multi-file programs | 2 hours |

**Problem Set 3** released Friday, due Friday of Week 4.

---

## Contents

```
PROG101 Week3/
├── README.md
├── lectures/
│   ├── Lecture 01 Functions and Pass-by-Value.md
│   ├── Lecture 02 The Call Stack and Scope.md
│   └── Lecture 03 Structured Programming Multi-File.md
├── assignments/
│   └── Problem Set 3.md
├── lab/
│   └── LAB 3 Functions Callstack Multifile.md
├── quizzes/
│   └── QUIZ 2.md
├── resources/
│   └── Week 3 Functions and Linkage Reference.md
└── solutions_instructor/
    └── LAB 3 Solutions.md
```

---

## Learning Objectives

1. Distinguish a declaration from a definition, and say which of the compiler and the linker needs each
2. Explain pass-by-value from the **addresses** of the caller's variable and the parameter
3. Describe a stack frame's contents and demonstrate the stack's growth direction empirically
4. Separate **scope**, **storage duration**, and **linkage** — and state which of them `static` changes in each position
5. Split a program across translation units with a guarded header and correct Makefile dependencies
6. Diagnose an undefined-reference error and name the build stage that produced it
7. Write preconditions, postconditions and invariants, and enforce them with `assert`
8. State the Böhm–Jacopini theorem and rewrite `goto` code without it

---

## Key Facts

| | |
|---|---|
| Every argument is **copied** | `swap(int a, int b)` cannot work |
| Stack grows **downward** on x86-64 | verified: 32 bytes per frame in Lab 3 |
| Frame holds more than the locals | return address, saved frame pointer, alignment padding |
| Addresses differ between runs | ASLR — the *differences* do not |
| Stack is finite | ~8 MiB; unbounded recursion → SIGSEGV, exit 139 |
| `static` **in a function** | changes lifetime, **not** visibility |
| `static` **at file scope** | changes linkage — withholds the symbol from the linker |
| Missing definition | fails at **link** time, not compile time |
| Header without an include guard | breaks on the second inclusion |
| `-DNDEBUG` | deletes assertions **and their side effects** |
| `return &local` | caught by `-Wreturn-local-addr`, **on by default** |
| The same bug via a helper | caught by **nothing** static — ASan reports `stack-use-after-return` |

---

## Connections

**Back:** Week 2's control structures are what functions package up; Böhm–Jacopini is stated there
and applied here. Week 1's `sizeof` and type sizes explain the 32-byte frame spacing.

**Forward:** Week 4's arrays decay to pointers when passed, which is pass-by-value applied to an
address — the rule from this week, not an exception to it. Week 5 introduces the pointer that finally
makes `swap` writable. Week 6's heap exists precisely because the stack discipline demonstrated in
Lab 3 destroys frames on return. Week 9's recursion is this week's call stack, iterated.

**Sideways:** CS 101 covers functions, scope and the call stack in Python this week too. The stack is
the same; the difference is that Python has no linker, no header files, and no way to return a
pointer to a dead frame.

---

*PROG 101 · Week 3 · © CSE Department*
