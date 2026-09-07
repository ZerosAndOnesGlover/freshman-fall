# CS 211 · Quiz 5

**Sat:** Tuesday of **Week 5**, first 10 minutes of lecture · TH 205
**Covers:** **Week 4** — three-address code, basic blocks, the CFG, SSA, dataflow analysis
**Unmarked.** Recorded in [[_CS 211 Lab and Quiz Record]].

**The answer key is printed below the questions.** Do not look at it until you have written something for all six. The point of this quiz is to tell *you* what you do not know, twenty minutes before Week 5 starts assuming it.

---

## Questions

**1.** *(1 min)* Lower this Cyan statement to three-address code. Use as many temporaries as you need.

```cyan
return (a + b) * (a - 1);
```

---

**2.** *(2 min)* Three rules define a **leader**. State all three.

---

**3.** *(2 min)* Here is a fragment of TAC:

```
    t0 = x < y
    ifz t0 goto L2
    t1 = 1
    goto L3
L2:
    t1 = 2
L3:
    ret t1
```

Rewrite it in **SSA form**, inserting a φ-function where one is needed. State in one sentence what the φ records.

---

**4.** *(2 min)* Why must `&&` be lowered to **branches** rather than to a single instruction? Give a Cyan expression that computes the wrong answer — or crashes — if you get this wrong.

---

**5.** *(2 min)* Dataflow analysis is one algorithm with two knobs. Name them, and give their settings for **reaching definitions**.

---

**6.** *(1 min)* Changing the constant folder's `/` from truncating division to Python's floor division makes `-7 / 2 * 100 + -7 % 2` fold to `-401` instead of `-301`.

**Why is that worse than a folder that crashes on the same input?**

---
---

## Answer Key

**1.**

```
    t0 = a + b
    t1 = 1
    t2 = a - t1
    t3 = t0 * t2
    ret t3
```

Any order that computes both operands before the multiply is correct. **Four temporaries is typical; three is possible; one is not.** Note `t1 = 1` — Cyan has no negative literals and no immediate operands in our IR, so every constant gets its own instruction.

---

**2.** A leader is:

1. the **first** instruction of the program,
2. any instruction that is the **target of a branch** (in our IR, any `label`),
3. any instruction **immediately following** a terminator.

*(Dragon §8.4. Rule 3 is the one people forget, and it is the one that puts the code after a `goto` into its own block.)*

---

**3.**

```
    t0 = x < y
    ifz t0 goto L2
    t1_1 = 1
    goto L3
L2:
    t1_2 = 2
L3:
    t1_3 = phi(t1_1, t1_2)
    ret t1_3
```

**The φ records which predecessor control arrived from.** It is not an instruction the machine executes — it is a note to the compiler that `t1_3` takes `t1_1`'s value on the fall-through edge and `t1_2`'s value on the edge from `L2`.

*The "static" in Static Single Assignment means each name is assigned once in the **program text**. A name inside a loop is still assigned once statically and many times dynamically.*

---

**4.** Because `&&` **must not evaluate its right operand** when the left is false.

```cyan
b != 0 && a / b > 1
```

Evaluate both operands unconditionally and this divides by zero whenever `b` is zero — precisely the case the guard was written to prevent. **A single instruction cannot express "do not compute this" — only a branch can.**

*Full credit for any example where the right operand faults, divides by zero, or has a side effect.*

---

**5.** The knobs are **direction** (forward or backward) and **merge operator** (union or intersection).

**Reaching definitions: forward, union.** Union because it is a *may* analysis — a definition reaches if it arrives along *some* path.

*(Liveness: backward, union. Available expressions: forward, intersection. Those three are the standard set, and Week 5 adds dominators — forward, intersection.)*

---

**6.** Because **a crash tells you immediately, and a wrong constant tells whoever is unlucky, months later, in production.**

The compiler reports no error. The program runs. It computes something the source never asked for, and **every test that avoids negative division still passes.**

*An optimisation that produces a different answer is not a slow compiler. It is a wrong one.*

---

## How You Did

**6 correct** — you are ready for Week 5.
**4–5** — reread the section you missed before Thursday; this week builds directly on all six.
**0–3** — L09 and L10, properly, this week. **Week 5's register allocator is built on the def/use model from Q1 and the dataflow framework from Q5**, and it will not make sense without them.

---

*CS 211 · Week 5 · Quiz 5 · © CSE Department*
