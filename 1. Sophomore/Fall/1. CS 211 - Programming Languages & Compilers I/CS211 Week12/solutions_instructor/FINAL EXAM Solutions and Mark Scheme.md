# CS 211 · Final Examination — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** Every measured figure was verified against the lab code across Weeks 0–12.

---

## Marking Principles

1. **Reasoning carries the marks.** An approximate measured figure with a correct explanation scores full; an exact figure alone scores about half.
2. **Q7 is marked as an argument.** A student who reaches a different conclusion and defends it with course evidence scores full marks.
3. **Where a part asks to "name the week", accept the content without the number.**
4. **Do not double-penalise.** A student who mis-states the def/use rule in Q2(d) and repeats the error in Q7(a) loses it once.

---

# Section A

## Q1 · Front End (20)

**(a)** *(4)* e.g. `L → ε | I`, `I → int | int ',' I`. Unambiguity: the grammar is right-linear in `I`, so each string has one derivation. *Accept any correct grammar with a genuine argument or a genuine counterexample.*

**(b)** *(4)* **Maximal munch:** at each point take the **longest** string that forms a valid token. `>>=` lexes as one token, not `>` `>` `=`; `int x` vs `intx`.

**The second appearance is Week 5's instruction selection** — longest token, largest tile, same greedy algorithm.

**(c)** *(4)* **Left recursion**: `E → E + T` calls `E` before consuming input, so recursive descent does not terminate. Rewrite `E → T E'`, `E' → + T E' | ε` (or `T ('+' T)*`).

**Associativity is recovered in the fold/loop** — iterating left to right builds a left-associated tree. *(Week 10 §L22.4 measured this: changing the fold changes associativity without touching a production.)*

**(d)** *(4)* Any type error: `let x: int = true;` or calling with wrong arity. Message must name **line and column**.

**(e)** *(4)* `λf. λx. f (f x)` : **`∀a. (a → a) → a → a`**. Steps: `f : α`, `x : β`; `f x` forces `α = β → γ`; `f (f x)` forces `γ = β`; hence `f : β → β` and the type is `(β → β) → β → β`.

`λx. x x` requires `α = α → β`, refused by the **occurs check** — no finite type contains itself.

---

## Q2 · Intermediate Representations (20)

**(a)** *(4)*

```
    t0 = a < b
    ifz t0 goto L0
    t1 = 2 ; t2 = a * t1 ; c = t2 ; goto L1
L0: t3 = 1 ; t4 = b + t3 ; c = t4
L1:
```

**Four basic blocks.** Leaders: the first instruction; any branch target (any `label`); any instruction **following a terminator**. *(Rule 3 is the one they forget.)*

**(b)** *(5)* `c_1` and `c_2` in the branches, `c_3 = phi(c_1, c_2)` at `L1`.

**A φ records which predecessor control arrived from.** The back end **destroys** it — φ-elimination, inserting a `copy` on each incoming edge — before register allocation and code generation. *(Accept "out-of-SSA"; require some statement of *what* is inserted.)*

**(c)** *(5)*

| | direction | merge | init |
|---|---|---|---|
| liveness | backward | union | empty |
| reaching definitions | forward | union | empty |
| dominance | forward | intersection | **full** |

Union only grows, so a *may* analysis started empty converges to the **least** fixed point — the smallest set consistent with the equations, which is what "does a path exist" wants. Intersection only shrinks, so a *must* analysis must start full to reach the **greatest**. Swap them and each converges to the trivial fixed point: everything live, or nothing dominating.

**Full marks require the answer to be about which fixed point is reached.**

**(d)** *(6 — 2 the opcode, 3 the three consumers, 1 the principle)*

**`store`** (equally `setfield`) — it keeps the array in **`dst`**, which `uses` never inspected.

| consumer | symptom |
|---|---|
| dead-code elimination (W5) | the instruction computing the array is deleted; wrong answer |
| register allocation (W5) | missing interference edges — two live values may share a register |
| the GC root set (W6) | a reachable object is freed; **use-after-free** |

**The principle:** an imprecise analysis costs performance; an **unsound** one costs correctness — and *which* you get is decided by the phase that consumes it, not by the mistake.

*Award the register-allocation row generously; many will name only two.*

---

## Q3 · Optimisation and Code Generation (20)

**(a)** *(4)* Test in the header, body after it; control can leave from the header without entering the body, so the body does not dominate the exit. The defeating edge is the **header's exit edge**.

**(b)** *(4)* **Whether executing the instruction unnecessarily can be observed** — the instruction's **trap predicate**. A multiply wastes a cycle; a division can trap. Hoisting is speculation, legal only for instructions that cannot fault.

*Zero marks for "division is slower" or any answer about invariance.*

**(c)** *(4)* **Lower** bound — at the point where 6 values are simultaneously live, all 6 need distinct registers. **Not guaranteed**: colouring is **NP-complete** and Chaitin's is a heuristic.

**(d)** *(4)* It is trivially correct and avoids constructing SSA in the front end — dominance frontiers, φ placement, renaming — **which is what clang does too**. The pass is **`mem2reg`**, running **SSA construction via dominance frontiers** (Cytron et al., Week 4).

**(e)** *(4)* **aarch64 = 8**: hardware `sdiv`, and no remainder instruction, so `msub` computes `a − q·b`. **riscv64 = 16**: the **base RISC-V integer ISA has no divide** (it is the optional M extension), so the back end calls the runtime helper `__moddi3`.

*m* languages × *n* targets becomes *m* + *n*: front and back ends know only the IR, so a new language gets every target and a new target gets every language.

---

## Q4 · Semantics and Evaluation (20)

**(a)** *(4)* `(λf. λx. f (f x)) (λy. y+1) 3` → `(λx. (λy. y+1) ((λy. y+1) x)) 3` → … → **5**. *Award per correct step; any reduction order reaching 5 is fine (confluence).*

**(b)** *(5)* `λy′. y` is a **constant function** returning the outer free `y`; `λy. y` is **the identity**. The phenomenon is **variable capture**, an instance of **lexical scoping** (Week 3).

**Two systems:** Week 7's `subst` with `--naive`, and **Week 10's `swap-bad` macro** — plus C's preprocessor, which is not a lambda calculus and is the answer being fished for.

**(c)** *(5)* `Y g` → `(λx. g (x x)) (λx. g (x x))` → `g (Y g)`.

Under call-by-value the **argument** is reduced first, and the argument is `x x`, which produces `g (x x)` again — `g` is never entered.

**"The same function" is extensional**: for every argument both produce the same *result*. It says nothing about *when*, or whether a given strategy reaches it.

**(d)** *(6 — 1 the term, 2 the distinction, 3 the HM part)*

The term is **`λf x. x`**.

**`mult == compose` is a theorem** — multiplying Church numerals genuinely *is* composing functions, so any correct encoding reproduces it and confusing them cannot give a wrong answer. **`zero == false == nil` is a collision** — unrelated meanings sharing a shape, which a different encoding separates.

**HM separates neither**, because a **principal type is computed from the term**, and these *are* the same terms. `zero`/`false`/`nil` all get `∀a b. a → b → b`; `mult`/`compose` share theirs too.

**What separates them is a *declaration*** — `data Bool = True | False` — a **nominal** distinction grounded in a chosen name. *(Full marks require "nominal" or an unambiguous description. This is the Week 8 result that corrected the Week 7 prediction.)*

---

## Q5 · Memory and Concurrency (20)

**(a)** *(4)* Zero **proves unreachable**. Three **proves nothing** — it proves three pointers exist. Any cycle; all its members reclaimable by tracing.

**(b)** *(4)* **Live-variable analysis, Week 5, written for register allocation.** Both ask **what does the future read?** The collector cannot recompute or validate the stack map, so **a wrong entry is a memory-safety bug with no assertion anywhere**.

**(c)** *(4)* A **write barrier** filling a **remembered set**. The pointer it cannot catch is created by **promotion**: a young→young pointer becomes old→young when the parent is promoted, **with no write executing**. A write barrier fires on writes.

**(d)** *(4)* Some thread's store is first in the global order; it precedes the other thread's load, which therefore reads 1. **Store buffer**; **StoreLoad** reordering — the only one x86 permits.

**(e)** *(4)* **Loop-invariant code motion, Week 5.** The racy read is **undefined behaviour** — the standard imposes *no requirement* on the program — so the compiler may assume no other thread writes the flag, making the load loop-invariant.

*Reject "the result is unpredictable": that is precisely what the standard does not say.*

---

## Q6 · Types, Proofs and Metaprogramming (20)

**(a)** *(4)* **Sound and incomplete** — incomplete with respect to **programs that would have run without error**. Mechanism: a `let`-bound name is **generalised** (`∀`), a λ-bound name is **monomorphic**, so the body cannot use it at two types.

**(b)** *(4)* Class → **record type**; instance → **value** of it (a **function**, if it has a context); constraint → **parameter**. The nested dictionary is **built by the compiler, by recursion over the type**. Reported **at compile time, during elaboration**.

**(c)** *(4)* `λp q. p` is **`const`** — which Week 7 found is the same term as `true`.

A proof of `A ∨ B` is a **tagged value**; a proof of `A ∨ ¬A` would be a program that **decides**, for arbitrary unknown `A`, with nothing to inspect.

With LEM assumed, `lem` is a **free variable** of the proof — an assumption, not a construction, so the term is not a closed program.

**(d)** *(4)* A macro runs at **expansion time** and receives **unevaluated syntax**. The bug is **variable capture**; the fix is **`gensym`**, which corresponds to **`fresh`** in Week 7's `subst`.

**(e)** *(4)* The **occurs check is the mechanism**; **strong normalisation is the reason** — if `Y` were typeable a well-typed term would diverge and the theorem would be false. **OCaml makes `let rec` a primitive** rather than deriving recursion, giving up totality deliberately.

---

## Q7 · Synthesis (30)

### (a) *(10 — 4 symptoms, 4 ranking, 2 principle)*

Symptoms as in Q2(d). **Ranking, most to least severe: the root set (use-after-free — a memory-safety bug in a memory-safe language), then dead-code elimination (silent wrong answer), then register allocation (also a wrong answer, but caught by almost any test since it corrupts values immediately).**

**Accept any ranking with a real justification.** The strongest answers argue by *how far the failure travels* rather than by how dramatic it looks.

**Principle:** an unsound analysis's severity is set by the phase that consumes it, not by the analysis.

### (b) *(10 — 4 mechanisms, 4 instruments, 2 the habit)*

Any three mechanisms. Reference material:

- **Folder:** compiled cleanly, returned a plausible integer; every test avoiding negative division passed.
- **DCE:** the pass printed a **success** message, and the dump rendered `store` as though it *defined* its destination.
- **Root set / promotion:** the program returned the **right answer** while 97 reachable objects were freed.
- **Racy spin-wait:** `-O2` gave the correct result in 0.000 s by deleting the loop; `-O0` lost 63%.

**Instruments that agreed with the bug** (name two): Week 5's **printer**, which asserted the opposite of the truth about a def; Week 6's **peak RSS**, pinned by the collection threshold and unable to see retention; Week 7's **`0 == False`**, passing every boolean test; Week 11's **phase timer**, measuring `fork` and reporting it as code generation; Week 9's **cache-line layout**, changing a rate by 100×.

**The habit: check the property, not a sample of the outcomes.** Why more tests is insufficient — **a measured figure is required**: the store-buffer outcome appears roughly **once in 3,000–18,000 iterations**, so multiplying test runs multiplies cost linearly and confidence hardly at all. ThreadSanitizer finds it in one run because it checks **happens-before** rather than results.

*Full marks require the figure. "It's rare" is not a figure.*

### (c) *(10 — 4 the two guarantees, 3 the rejection, 3 the target)*

Any two well-argued guarantees. Strong answers: **memory safety without GC** (ownership — impossible: use-after-free and data races; cost: rejected valid programs; **paid by the programmer**); **bounds checking** (impossible: out-of-range access; cost: a compare and branch per access; **paid by the machine**, and partly recoverable by the optimiser); **no undefined behaviour** (impossible: the Week 9 spin-wait deletion; cost: fewer optimisations; **paid by the user, in performance**).

**The rejection must be concrete** — a doubly-linked list under single ownership is the canonical example, and Week 7's cycle is the same shape.

**Target:** LLVM is the defensible answer, evidenced by the Week 11 table — `wasm32` and `avr` are both in it, so one back end serves browser and embedded. *Accept a bespoke back end or WebAssembly directly if argued with the trade named.*

---

## Grade Guidance

| Marks | Reading |
|---|---|
| 130–150 | Has the through-lines. Q7 answered in terms of principles, with figures. |
| 105–129 | Strong on mechanics; Q7 thin or unevidenced. The most common strong profile. |
| 75–104 | Can execute the algorithms; cannot say why they are as they are. Q2(d), Q4(d) and Q6(a) are diagnostic. |
| < 75 | Check Section A specifically before advising; the failure is usually Weeks 4–5 rather than the whole course. |

**Cohort signals worth acting on.** Widespread failure on **Q2(d)** means the Week 5 opening did not land, and Week 6's root-set argument will not have either. Widespread failure on **Q4(d)** means the Week 7→8 correction did not land — that is the one place the course explicitly revised its own claim, and it is worth checking whether students noticed.

---

*CS 211 · Final Examination · Solutions and Mark Scheme · © CSE Department*
