# CS 211 · Midterm Examination 2 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** Every count in this scheme was verified against the Week 4–7 lab code. Where a question asks for a measured figure, **the reasoning carries the marks and the figure does not** — students sat this without machines.

---

## Marking Principles

1. **Explanation marks are separate from answer marks** and are stated per part. A correct answer with no reasoning takes roughly half of the part.
2. **Approximate measured figures score full marks with correct reasoning.** "About ten thousand reductions, because normal order re-reduces `pred n` at every level" is worth more than "10384" alone.
3. **Q5 is marked as an argument, not as a checklist.** A student who reaches a different conclusion from this scheme and defends it with evidence from the course scores full marks.
4. Where a part says *name the week*, accept the content without the week number. Do not award the week number alone.

---

## Q1 · Intermediate Representations (15)

**(a)** *(3 — 2 the code, 1 the store)*

```
    t0 = b.count
    t1 = 2
    t2 = t0 * t1
    t3 = 1
    t4 = i + t3
    a[t4] = t2
```

**Five temporaries.** The instruction whose destination is *read* is the **store**, `a[t4] = t2` — `a` is in the `dst` slot and is read, not written.

*Accept any consistent ordering: `tac.py` happens to evaluate the right-hand side before the index (`gen_stmt`'s `Assign` case calls `gen_expr(s.value)` first), but a student who computes the index first has not made an error. Accept 4–6 temporaries with consistent code. **Do not accept an answer that treats `a` as defined by the store** — that is the exact error Q2(a) is about, and a student who makes it here should lose the mark in both places.*

**(b)** *(3 — 2 the rules, 1 the count)*

A leader is: the **first** instruction; any instruction that is the **target of a branch** (in our IR, any `label`); any instruction **immediately following a terminator**.

**Four basic blocks.**

```
B0  t0 = x < y ; ifz t0 goto L2      -> L2, B1
B1  t1 = 1 ; goto L3                 -> L3
L2  t1 = 2                           -> L3
L3  ret t1                           (preds: B1, L2)
```

*Three is the common wrong answer, from forgetting that the instruction after the `goto` starts a block. Here that instruction is also a label, so the two rules coincide at `L2` — award the count mark only if four blocks are named.*

**(c)** *(4 — 2 the SSA, 2 the φ explanation)*

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

**A φ records which predecessor control arrived from** — `t1_3` takes `t1_1`'s value on the edge from `B1` and `t1_2`'s on the edge from `L2`.

The back end must **destroy** it: replace the φ with a `copy` on each incoming edge, so that both predecessors write the same location. *(Accept "φ-elimination", "out-of-SSA", or a description of inserting moves in the predecessors. Do not accept "the register allocator handles it" without saying what it does.)*

**(d)** *(5 — 3 the table, 2 the initialisation argument)*

| analysis | direction | merge | init |
|---|---|---|---|
| liveness | backward | union | empty |
| reaching definitions | forward | union | empty |
| dominance | forward | **intersection** | **full** |

**Dominance is the *must* analysis.** A block dominates another if **every** path passes through it. Intersection only ever shrinks a set, so the iteration must start from the largest candidate — every block — and remove what the equations refuse.

Initialise it empty and intersection can never add anything: every set stays empty, the iteration reaches a fixed point immediately, and the analysis concludes that **nothing dominates anything**. That is a fixed point of the equations; it is just the wrong one. *May* analyses want the **least** fixed point and start empty; *must* analyses want the **greatest** and start full.

*Full marks require the answer to be about which fixed point is reached, not about the code.*

---

## Q2 · Optimisation (15)

**(a)** *(4 — 1 unsound, 1 conservative, 2 which is worse)*

- **Unsound: `store`** (equally `setfield`). `uses` inspected only the `a` and `b` slots, and `store` keeps the array in **`dst`** — so the array looked dead and the instruction computing it was deleted.
- **Conservative: `getfield`** (equally `alloc`). It carries a **field name** (or a **type name**) in an operand slot; the name is an identifier, so a variable that does not exist was reported live.

**The unsound one is worse.** A conservative analysis keeps code that could have gone — it costs performance. An unsound one removes code the program needs — it costs correctness.

*Full marks require both words used correctly. The frequent error is calling the `getfield` case "unsound because it's wrong": it is wrong, but in the safe direction, and that distinction is the question.*

**(b)** *(4 — 2 the diagram, 2 the edge)*

```
   header:  if cond goto exit      <- the loop exit is HERE
      |
   body:    t = k * 2              <- and this is what you want to hoist
      |
   goto header
```

Control can leave the loop **from the header**, without ever entering the body. So the body does not dominate the exit, and condition (1) fails for every instruction in it.

The defeating edge is the **header's exit edge** — the branch out of the loop, taken before the body runs.

*Accept any drawing that puts the test in the header and identifies that edge.*

**(c)** *(3)*

**Whether executing the instruction unnecessarily can be observed.** A multiply that did not need to happen wastes a cycle; a division that did not need to happen can **trap** — divide by zero — turning a program that returns a value into one that dies.

Hoisting is **speculation**: it executes an instruction on a path where the source would not have. Legal for instructions that cannot fault, illegal for those that can.

*It is a rule about the instruction's **trap predicate**. Zero marks for "because division is slower", "because the loop might not run" alone, or any answer about invariance.*

**(d)** *(4 — 2 the guarantee, 2 the bound)*

**No, it is not guaranteed.** Graph colouring is **NP-complete**, and Chaitin's algorithm is a *heuristic*: remove nodes of degree < k, and when none exists, choose one to spill. Achieving zero spills at exactly peak liveness is a good result on that graph, not a theorem. Briggs' optimistic colouring improves on it precisely because Chaitin spills graphs that are k-colourable.

Peak liveness is a **lower** bound: at the point where 7 values are simultaneously live, all 7 need distinct registers, so no allocator can use fewer. Chaitin matching it means the bound was **tight** here.

*The common error is calling it an upper bound. Award the first two marks independently of the second two.*

---

## Q3 · Runtime Systems (15)

**(a)** *(3 — 1 zero, 1 three, 1 the heap)*

**Zero proves the object is unreachable**, so it is safe to free. **Three proves nothing** — it proves three pointers exist, not that anything can reach them.

```
        a ---> [b] ---> b ---> [a] ---> a
```

Four objects, each holding the next's count at one, none reachable from outside. **A tracing collector reclaims all four.**

*Accept any cycle. A two-object cycle is fine if the student says so and adjusts the count.*

**(b)** *(4 — 1 analysis+week, 2 purpose and shared question, 1 consequence)*

**Live-variable analysis, Week 5.** Written for **register allocation** — to decide when a register may be reused.

Both consumers ask: **what does the future read?** A register may be reused when nothing will read its occupant again; an object may be freed when nothing will read the pointer to it again.

The consequence: **the compiler is the only thing that can be right about it.** The collector receives a stack map it cannot recompute and cannot validate, so a wrong entry is a memory-safety bug with no assertion anywhere to catch it.

**(c)** *(4 — 2 the explanation, 2 the measurement)*

Peak live is fixed by **whatever triggers a collection** — an object count or a heap size. A retaining collector does not exceed that trigger; it reaches it **sooner**. So retention appears as *more frequent collections and more marking*, never as a higher peak.

The measurement is **residency** — live bytes immediately *after* a collection — or equivalently objects scanned. On `loiter.cy`: 16 B against 216 B, 17 collections against 22, 17 objects scanned against 132, **with peak live 504 B in both**.

*Approximate figures fine. Full marks require naming a post-collection measurement; "measure it for longer" scores nothing.*

**(d)** *(4 — 2 barrier and set, 2 promotion)*

A **write barrier** on every heap pointer write, recording old-to-young pointers in the **remembered set**, which minor collections treat as extra roots.

The one it cannot catch is created by **promotion**. A young object pointing at another young object is correctly *not* recorded — a minor collection scans both. Promote the parent and that same pointer becomes old-to-young, **without any write executing**. A write barrier fires on writes; nothing wrote.

*This is the discriminating part of Q3. Accept any answer that identifies promotion as a re-classification rather than an assignment. Removing the fix-up freed 97 reachable objects while still printing the right answer — a student who cites that scores the full four.*

---

## Q4 · The Lambda Calculus (15)

**(a)** *(3 — one per step)*

```
(λx y. y x) a (λz. z)
→  (λy. y a) (λz. z)
→  (λz. z) a
→  a
```

Three beta-reductions; normal form **`a`**.

*Award per correct step. A student who reduces the argument first reaches the same answer and should not be penalised — the term is confluent.*

**(b)** *(4 — 2 the two functions, 1 the naming, 1 the danger)*

- `λy′. y` is a **constant function**: it ignores its argument and returns the outer free `y`.
- `λy. y` is **the identity function**: it returns its argument.

The phenomenon is **variable capture**. It is an instance of **lexical scoping** — Week 3's symbol table, and the rule that an occurrence binds to the nearest enclosing binder of that name.

Why worse than a crash: **nothing reports an error.** The result is a well-formed term with a normal form, so the program runs and computes something the source never asked for — and every test that does not exercise the capturing case passes.

*Accept "hygiene" as the name. Full marks need the two functions described by behaviour, not appearance.*

**(c)** *(4 — 1 the step, 1 the equation, 1 CBV, 1 "same function")*

`Y g` → `(λx. g (x x)) (λx. g (x x))` → `g ((λx. g (x x)) (λx. g (x x)))`, so

$$Y\,g \;=\; g\,(Y\,g)$$

**Under call-by-value the argument must be reduced before the application.** The argument is `(λx. g (x x))` applied to itself, which produces `g (x x)` again — so `g` is never entered and the base case is never consulted. The repeatedly-evaluated subterm is **`x x`**.

**"The same function" is extensional**: for every argument both produce the same result. It is a claim about *results*, and says nothing about *when*, how many steps, or whether a given strategy reaches them. So one may terminate and the other not, without contradiction.

*The last mark is the one that separates the top of the cohort. Accept any answer that locates the claim at "results" and denies it covers evaluation.*

**(d)** *(4 — 1 the term, 1 the return, 2 the difference)*

The term is **`λf x. x`** (equivalently `λt f. f`, `λc n. n` — the same term up to alpha).

A program returning it has returned the numeral zero **and** the boolean false **and** the empty list, and **there is no fact of the matter about which** — nothing in the term records an intention.

**`mult == compose` is a different kind of fact.** It is a **theorem**: multiplying Church numerals genuinely *is* composing functions, so any correct encoding of numerals reproduces it, and confusing the two cannot produce a wrong answer. `zero == false` is a **collision**: two unrelated meanings that happen to need the same shape, and a different encoding separates them.

*Two marks for the theorem/collision distinction, however phrased. "One is a coincidence and one is not" with a reason is full marks. A student who claims both are coincidences loses both.*

---

## Q5 · Synthesis (15)

Marked as an argument. The scheme below is a strong answer, not the only one.

**(a)** *(5 — 2.5 per mechanism, capped at 5)*

Any two of:

- **Week 4's folder.** The compiler reported no error and the program ran; `−7 / 2 * 100 + −7 % 2` folded to `−401`. The developer saw a passing build and a plausible integer. They did not see that **every test avoiding negative division still passed** — the defect is in a case tests rarely cover.
- **Week 5's DCE.** `opt.py` reported `round 1: dce changed the code` — a *success* message. The developer saw 8 instructions become 6, which is what an optimiser is supposed to do. They did not see that the surviving `store` wrote through a register nothing had loaded, **because the printer rendered `store` as though it defined its destination**.
- **Week 6's collector.** The program returned the right answer. Under `--no-fixup`, `chain 120` freed 97 reachable objects and still printed 119, because the corrupted tail was never dereferenced. The developer saw a correct result; they did not see the heap.
- **Week 7's substitution.** One beta-step, no error, a well-formed term with a normal form. The developer saw a result; they did not see that it was the identity rather than a constant function.

*Award for the mechanism of invisibility, not for restating the bug. "It gave the wrong answer" is not a mechanism; "the pass reported success and the dump asserted the opposite of the truth" is.*

**(b)** *(5 — 2 the table, 1 the entry, 2 the severity argument)*

The table is the **def/use model** — `Instr.uses` in Week 4, replaced by `SLOTS` in `live.py` in Week 5.

The wrong entry: **`store` (and `setfield`) read their `dst` slot**, and `uses` never inspected `dst`.

Severity changed with the consumer, and the table did not change at all:

| consumed by | result |
|---|---|
| dead-code elimination (W5) | an instruction deleted; a wrong answer |
| the **root set** (W6) | `#2` freed and written through — a **use-after-free** |

**An imprecise analysis makes a slow program; an unsound one makes an exploitable one**, and which you get is decided by the phase downstream rather than by the mistake itself.

*Three of the four is the intended reading — W4's folder is a different root cause (the semantics of division), and a student who says so and argues only three belong scores full marks. A student who forces all four into one cause should lose a mark unless the argument is good.*

**(c)** *(5)*

Both conclusions are defensible. Award on engagement with *why each defect evaded observation*.

**Against the colleague** (the stronger case, and the one the course argues):

- Several defects were invisible **to the instruments**, not merely untested. Week 5's dump asserted `t2` was defined by the `store`; a developer reading it would have confirmed the deletion as correct. **More tests do not help when the tool agrees with the bug.**
- Week 6's collector bug needs sustained allocation *and* long-lived structure *and* a reader that traverses — `walk 32` passes and `walk 33` crashes. That is a description of production, not of a test suite.
- Week 7's `church.py` **had** a test for every boolean case and reported 23/23, because `0 == False` in Python. The suite was weak precisely on the property it existed to check.

**What would have been more effective:** differential testing (`--gc=none` against `--gc=mark`); an assertion in the tool rather than a test of the program (`check_coverage` raising on an unknown opcode); fixing the *printer* before trusting the dump; and choosing a representation where the error cannot be expressed (de Bruijn indices, `Ref` as a distinct class).

**For the colleague:** a property-based or differential suite *is* a test suite, so the disagreement is partly about what counts as one. That is a legitimate reading and scores full marks if argued.

*Zero marks for "yes, always write more tests" with no engagement. Full marks require at least two concrete Week 4–7 examples and a named alternative.*

---

## Grade Guidance

| Marks | Reading |
|---|---|
| 65–75 | Has the through-line. Q5(b) and Q4(c) answered in terms of the underlying principle. |
| 50–64 | Solid mechanics; Q5 thin. The most common profile. |
| 35–49 | Can execute the algorithms, cannot say why they are the way they are. Q1(d), Q2(a) and Q3(d) are the diagnostic parts. |
| < 35 | Weeks 4–5 not consolidated. Check Q1 and Q2 specifically before advising. |

**Two parts to watch across the cohort.** If **Q2(a)** is widely wrong, the Week 5 opening did not land and Week 6's root-set argument will not either — worth ten minutes in the Week 9 lecture. If **Q3(d)** is widely wrong, it is the promotion hole, which is genuinely hard and may simply need re-teaching rather than remediation.

---

*CS 211 · Midterm Examination 2 · Solutions and Mark Scheme · © CSE Department*
