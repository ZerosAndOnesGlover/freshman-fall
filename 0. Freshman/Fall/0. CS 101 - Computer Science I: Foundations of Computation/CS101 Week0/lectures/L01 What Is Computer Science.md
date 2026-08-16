# CS 101 · Lecture 1
## What Is Computer Science?

**Week 0 · Lecture 1 of 3**
*"The question of whether a machine can think is no more interesting than the question of whether a submarine can swim." — Edsger Dijkstra*

**Date:** Wednesday 19 August 2026 · 09:00–09:50 · Week 0

---

## 0. Before We Begin

This course is not about learning Python.

Python is the **vehicle**. The destination is **computational thinking**: a precise, powerful way of breaking down problems, expressing solutions, and reasoning about whether those solutions are correct and efficient.

By the end of Week 12, you will be able to take a problem you have never seen before, decompose it systematically, design a solution, implement it correctly, and prove how fast it runs. That ability transfers to any language, any system, any domain.

---

## 1. What Is Computer Science, Actually?

Most people think CS = programming. This is like saying biology = pipettes. Programming is a **tool** CS uses, not the thing itself.

CS is the **science of computation**:
- What problems can be **solved** by a machine?
- What problems are **unsolvable** — provably, forever?
- Of the solvable problems, how do we solve them **efficiently**?
- How do we **reason rigorously** about our solutions?

These questions existed before modern computers. Alan Turing asked them in 1936: 10 years before the first electronic computer was built.

---

## 2. The Three Pillars

### 2.1 Theory of Computation
What *can* and *cannot* be computed? This gives us the Turing Machine model, decidability, and complexity classes like P and NP.

### 2.2 Algorithms & Data Structures
Given a computable problem, how do we solve it efficiently? This gives us sorting algorithms, graph algorithms, dynamic programming, and the mathematical tools to analyze them.

### 2.3 Systems
How do we build real, working, large-scale systems? This gives us operating systems, compilers, networks, databases, distributed systems.

**This course (CS 101) sits at the intersection of pillars 1 and 2.**

---

## 3. CS vs. Software Engineering vs. Computer Engineering

These three are related but distinct.

| | **Computer Science** | **Software Engineering** | **Computer Engineering** |
|---|---|---|---|
| **Core Question** | What can be computed? How? | How do we build reliable software? | How do we build computing hardware? |
| **Primary Output** | Algorithms, proofs, theory | Systems, applications, processes | Chips, circuits, embedded systems |
| **Mathematical Core** | Discrete math, logic, complexity | Probability, statistics, formal methods | Electronics, signal processing |
| **Examples** | Designing a new sorting algorithm | Building a web application at scale | Designing a CPU pipeline |

In a CSE (Computer Science & Engineering) degree, you get **all three**. They reinforce each other deeply.

---

## 4. What Is an Algorithm?

**Definition:** An algorithm is a **finite**, **unambiguous**, **executable** sequence of instructions that takes **input** and produces a defined **output** to solve a **class of problems**.

Every word in that definition matters:
- **Finite**: it must terminate (eventually produce an answer)
- **Unambiguous/ Definiteness**: each step must have exactly one interpretation
- **Executable/Effectiveness**: a machine (or person) must be able to carry out each step
- **Input**: it must be able to accept valid data or information to process
- **Output**: it must produce a defined result or answer
- **Class of problems**: it must work for *all* valid inputs, not just specific examples

**Example: Making Toast (informal algorithm):**
```
1. Get bread
2. Put bread in toaster
3. Set timer to 2 minutes
4. Press down lever
5. Wait until bread pops up
6. Remove bread
```

**Why this is imprecise:** Step 1 doesn't specify what kind of bread. Step 5 doesn't say what to do if the toaster breaks. Step 3 assumes a specific toaster model. A *real* algorithm would handle all these cases.

This is why programming is harder than it looks: computers have no common sense to fill in the gaps. They do *exactly* what you say.

---

## 5. The Turing Machine: The Model of All Computation

In 1936, Alan Turing asked a deceptively simple question: **Is there a single "universal" procedure for computing anything that can be computed?**

His answer was the **Turing Machine**: not a physical device, but a mathematical model:

```
┌─────────────────────────────────────────────────┐
│  Infinite tape: [ B ][ 1 ][ 0 ][ 1 ][ B ][ B ]  │
│                              ↑                  │
│                         Read/Write Head         │
│                                                 │
│ Finite State Control: (State, Symbol) → (State, │
│ Symbol, Move)                                   │
└─────────────────────────────────────────────────┘
```

**Components:**
1. **Infinite tape**: cells that each hold one symbol (0, 1, or blank)
2. **Read/write head**: can read the current cell, write a symbol, and move left or right
3. **Finite state control**: a set of rules: "If in state Q and I see symbol S, write symbol S', move direction D, go to state Q'"

**Why does this matter?** Because Turing proved that **any computation that can be done by any mechanical process can be done by a Turing Machine.** This is the **Church-Turing Thesis**: the foundational claim of all computer science.

Your laptop, your phone, the world's fastest supercomputer: they are all, in a precise mathematical sense, equivalent to a Turing Machine with faster access to more memory.

---

## 6. What Cannot Be Computed?

This is one of the most profound results in mathematics.

**The Halting Problem:** Given an arbitrary program P and an input I, will P ever terminate, or will it run forever?

Turing proved in 1936 that **no algorithm can solve the Halting Problem for all programs.** The proof is a diagonalization argument we will study in Week 11.

This means there are well-defined questions with no algorithmic answer: forever, by mathematical proof, regardless of how fast or powerful computers become.

This is computer science at its most philosophical and most rigorous.

---

## 7. A Brief History: The People Who Built This Field

Understanding who created this field, and why, helps you see it as a *human* endeavor, not a fixed collection of facts.

| **Year** | **Person** | **Contribution** |
|---|---|---|
| 1843 | Ada Lovelace | Wrote the first algorithm intended for mechanical execution (for Babbage's Analytical Engine) |
| 1936 | Alan Turing | Formalized computation with the Turing Machine; proved the Halting Problem undecidable |
| 1936 | Alonzo Church | Developed lambda calculus (equivalent to Turing Machines; foundation of functional programming) |
| 1948 | Claude Shannon | Invented information theory; proved all information can be encoded in bits |
| 1945 | John von Neumann | Proposed the stored-program computer architecture (still the basis of all CPUs) |
| 1956 | John McCarthy | Coined "Artificial Intelligence"; invented LISP |
| 1968 | Edsger Dijkstra | Invented structured programming; shortest path algorithm; semaphores |
| 1972 | Dennis Ritchie | Invented C and co-invented Unix |
| 1983 | Linus Torvalds | Created the Linux kernel |

> **Reflection:** Every algorithm you write stands on 80+ years of foundational work by these people and thousands of others. Your job now is to understand their ideas deeply enough to extend them.

---

## 8. The Von Neumann Architecture: What Your Computer Actually Is

Every modern computer follows this design:

```
┌──────────────┐     ┌────────────────────────────────────┐
│    Input     │────▶│              CPU                   │
│  (keyboard,  │     │  ┌────────── ┐   ┌───────────────┐ │
│   network)   │     │  │   ALU     │   │    Control    │ │
└──────────────┘     │  │(Arithmetic│   │      Unit     │ │
                     │  │  Logic    │   │               │ │
┌──────────────┐     │  │  Unit)    │   └───────────────┘ │
│    Output    │◀────│  └────────── ┘         │           │
│  (screen,    │     │         │              │           │
│   network)   │     │    Registers ◀─────────┘           │
└──────────────┘     └────────────────────────────────────┘  
                              │        ▲                  
                              ▼        │                  
                         ┌──────────────────┐                
                         │     Memory       │                
                         │  (Programs AND   │                
                         │      Data)       │                
                         └──────────────────┘                
```

**Key insight:** Programs and data live in the **same memory**. This is Von Neumann's revolutionary idea: a program is just data that the CPU interprets. You can write programs that write programs. This is how compilers, operating systems, and virtual machines work.

---

## 9. What This Course Will Do To How You Think

After CS 101, you will look at problems differently. Concretely:

**Before:** "I need to find if the name 'Alice' is in a list of 1 million names."
**After:** "Is the list sorted? If yes, binary search: O(log n), done in 20 comparisons. If no, hash table lookup: O(1). If neither is available, linear scan: O(n), worst case 1 million comparisons. The algorithmic choice matters enormously."

**Before:** "My code is slow."
**After:** "There's a nested loop, this is O(n²). For n = 10,000, that's 100 million operations. I need an O(n log n) or O(n) approach."

This is the transformation this course delivers. You will start thinking in **complexity classes**, **data structures**, and **algorithmic patterns**, not just code.

---

## 10. Summary

| Concept | One-Line Summary |
|---|---|
| Computer Science | The science of what can be computed and how efficiently |
| Algorithm | A finite, unambiguous, executable solution to a class of problems |
| Turing Machine | The mathematical model of universal computation |
| Church-Turing Thesis | Any mechanical computation can be done by a Turing Machine |
| Halting Problem | Some well-defined problems have no algorithmic solution |
| Von Neumann Architecture | Programs and data share memory; the basis of all modern computers |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Here is a procedure for finding a person's name in a phone book:

```
1. Open the book somewhere near the middle.
2. If the name is on this page, stop.
3. If the name comes alphabetically before this page, repeat from step 1 using the left half.
4. Otherwise repeat from step 1 using the right half.
```

Test each of the five properties of an algorithm from §4 against this procedure. Exactly one property is violated. Which, and what single word would you change to fix it?

**2. (Explain.)** The halting problem proves that no program can decide, for every possible program and input, whether that program halts. Yet compilers routinely warn about infinite loops, and static analysers ship in industry. Explain precisely why these tools do not contradict the theorem.

**3. (Build.)** Design a Turing machine that decides whether a binary string contains an even number of `1`s. Give the state set, the transition table, and the accepting state. Then trace it on the input `1011`.

**4. (Stretch.)** §8 describes the von Neumann architecture, in which instructions and data share one memory and one bus to the CPU. This is the *von Neumann bottleneck*. Name one concrete hardware mechanism modern processors use to mitigate it, and explain what property of real programs makes that mechanism work.


### Answers

**1.** **Definiteness** is violated: "somewhere near the middle" is not a precisely specified step — two people following it could open different pages. Replace *near* with *at* (the exact midpoint of the remaining range) and the procedure becomes definite. The other four hold: it has clear input (the book and the name) and output (the entry or a failure), each step is effective, and it terminates because the range halves each pass and cannot halve below one page.

**2.** **`Undecidability`** is a statement about a **total** decision procedure — one that answers correctly for *every* input. Real `analysers` evade it in one of two ways. They may be *partial*: allowed to answer "halts", "does not halt", or "don't know", and the third answer is always available. Or they may be *unsound in one direction*: conservative, reporting a possible non-termination that may never actually occur (a false positive), or missing some real ones (a false negative). The theorem forbids a tool that is total, sound, and complete simultaneously; it forbids nothing about tools that give up two of the three. This is the general escape from undecidability results, and you will meet it again in CS 320.

**3.** Two states suffice, since the only thing worth remembering is the parity seen so far.

| State | Read | Write | Move | Next |
|---|---|---|---|---|
| q_even | 0 | 0 | R | q_even |
| q_even | 1 | 1 | R | q_odd |
| q_even | ␣ | ␣ | — | **accept** |
| q_odd | 0 | 0 | R | q_odd |
| q_odd | 1 | 1 | R | q_even |
| q_odd | ␣ | ␣ | — | **reject** |

Start in q_even. On `1011`: q_even→(1)→q_odd→(0)→q_odd→(1)→q_even→(1)→q_odd, then blank ⇒ **reject**, which is right — `1011` has three `1`s. Note the machine never writes anything different from what it read; all of its memory is in the state, which is why two states is the whole answer.

**4.** Caches are the central answer (separate L1 instruction and data caches are also a partial return to the competing Harvard architecture). A cache works because real programs exhibit **locality of reference**: *temporal* locality, where a recently used address is likely to be used again soon, and *spatial* locality, where addresses near a recently used one are likely to be used soon. Neither is guaranteed by the architecture — they are empirical facts about how people write code, which is why a deliberately cache-hostile access pattern can still run an order of magnitude slower than a friendly one on identical hardware. Other valid answers: instruction pipelining, speculative execution, or wider/multiple buses.



---

## Reading Assignments

- **`Guttag`, Ch. 1**: "Getting Started" (read tonight before Lab 0)
- **Optional but rewarding:** Alan Turing's original 1936 paper *"On Computable Numbers"* — the first 10 pages are accessible and historically stunning

---

## What's Next

**Lecture 2:** [[L02 Python Environment and REPL]]
**Lecture 3:** [[L03 Values Types and Expressions]]
**Lab 0 (Tue):** [[LAB 0 Environment Setup]]

---

*CS 101 · Week 0 · Lecture 1 · © CSE Department*
