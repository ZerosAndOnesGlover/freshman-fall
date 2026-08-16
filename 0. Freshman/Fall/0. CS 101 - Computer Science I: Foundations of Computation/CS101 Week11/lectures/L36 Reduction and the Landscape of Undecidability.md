# CS 101 · Lecture 36 (Week 11, Lecture 3)
## Reduction and the Landscape of Undecidability

**Date:** Friday 6 November 2026 · 09:00–09:50 · Week 11

---

## 0. One Theorem Is Not Enough

Thursday proved a single problem undecidable, and the proof was a custom-built contradiction. If
every undecidable problem needed its own `paradox`, the theory would be a curiosity.

It does not. **Reduction** is a technique that converts one impossibility proof into thousands. Once
HALT is known to be undecidable, you never have to diagonalize again — you show that solving your
problem would let you solve HALT, and you are done.

Today: the technique, several applications, one theorem that settles a whole class at once, and an
honest account of what all of this means for the software you are going to write.

---

## 1. The Idea

You already reason this way. "If I could solve X, I could solve Y. Y is impossible. So X is
impossible."

> **Definition.** Problem A **reduces to** problem B (written **A ≤ B**) if a solution to B can be
> mechanically converted into a solution to A.

Read it as **"A is no harder than B"** — because any B-solver gives you an A-solver for free.

The contrapositive is what we use:

> If **A ≤ B** and **A is undecidable**, then **B is undecidable**.
>
> *Proof.* If B were decidable, the reduction would make A decidable. But A is not. So B is not. ∎

### The direction is the whole game

This is where nearly everyone slips the first time:

| | Reduction | What it proves |
|---|---|---|
| ✅ **Correct** | HALT ≤ NEW | NEW is **at least as hard** as HALT ⟹ **NEW is undecidable** |
| ❌ **Wrong** | NEW ≤ HALT | NEW is no *harder* than HALT — proves nothing about NEW |

**Reduce the known-hard problem *to* the new one.** You assume a solver for the new problem and use
it to build a solver for HALT. If you find yourself using `halts` to solve your new problem, you
have written the arrow backwards and proved nothing.

A mnemonic: *the known-impossible thing must come out as a consequence.* HALT is the conclusion of
your construction, never the tool.

---

## 2. A Worked Reduction

> **PRINTS-HELLO** = { ⟨M, w⟩ : M ever prints `hello` when run on w }

Surely this is easier than halting — just watch the output? No.

**Claim.** PRINTS-HELLO is undecidable.

**Proof.** Suppose `prints_hello(f, x)` exists and always correctly decides this. Then build:

```python
def halts(f, x):
    def wrapper(_):
        f(x)                 # run the original computation
        print("hello")       # reached ONLY if f(x) finished
    return prints_hello(wrapper, None)
```

Now check the equivalence in both directions:

- If **f(x) halts** — control reaches the `print`, so `wrapper` prints `hello`, so `prints_hello`
  returns `True`, so `halts` returns `True`. ✅
- If **f(x) runs forever** — control never reaches the `print`. `wrapper` prints `hello` never, so
  `prints_hello` returns `False`, so `halts` returns `False`. ✅

*(Verified by construction: with `f` a terminating function the wrapper's output is `['hello']`;
with `f` an infinite loop the print is unreachable.)*

So `halts` is correct on every input — but `halts` cannot exist (L35). The only assumption was
`prints_hello`. Therefore **`prints_hello` cannot exist.** ∎

Notice how little work that was. No diagonalization, no self-application — just a five-line wrapper.
That is the leverage reduction buys, and every proof below has the same shape.

### The pattern

1. Assume a decider for the new problem B exists.
2. Write a **transformation** that turns an arbitrary HALT instance ⟨M, w⟩ into a B instance.
3. Show the B-answer is correct **iff** the HALT-answer is — both directions.
4. Conclude B's decider would decide HALT. Contradiction.

Step 3 is where marks are lost. Both directions must be argued; showing only "if it halts then…"
leaves the proof half-done.

---

## 3. The Landscape

Everything below is undecidable, essentially all by reduction from HALT:

| Problem | Why you might want it |
|---|---|
| Does M halt on input w? | The original |
| Does M halt on **every** input? | Guaranteed-termination checker |
| Does M ever print `hello`? | Output analysis |
| Do M₁ and M₂ compute the same function? | **Compiler optimisation correctness** |
| Is M's language empty? | Dead-code / unreachable-branch detection |
| Is this line of code ever executed? | Coverage analysis, dead-code elimination |
| Does M ever dereference a null pointer? | Static bug detection |
| Is this variable ever used after being freed? | Memory-safety analysis |
| Does this program leak memory? | The thing Valgrind approximates |
| Is this program a virus? | Perfect malware detection |

That list is not exotic edge cases. It is **the job description of a compiler, a linter, a debugger,
and an antivirus** — all provably impossible to do perfectly.

> **"Do M₁ and M₂ compute the same function?"** deserves a moment. That is exactly what a compiler
> claims when it optimises your code. Since program equivalence is undecidable, no optimiser can
> verify its own transformations in general. Real compilers apply a fixed catalogue of
> transformations each *individually proved* sound in advance — they never check equivalence at
> compile time. The undecidability is dodged by never asking the question.

---

## 4. Rice's Theorem: The Whole Class at Once

The list above suggests a pattern, and there is a theorem behind it.

> **Rice's theorem (1951).** Every **non-trivial semantic** property of programs is undecidable.

Two words carry the weight:

- **Semantic** — about *what the program does* (its input/output behaviour), not how it is written.
- **Non-trivial** — true of some programs and false of others. (A property true of *all* programs,
  or of none, is trivially decidable: always answer yes, or always no.)

So the answer to "is this behavioural property of programs decidable?" is essentially always **no**,
and you do not need a fresh reduction to know it.

### Where the escape hatches are

| Question | Kind | Decidable? | Why |
|---|---|---|---|
| Does M ever print `hello`? | semantic, non-trivial | ❌ | Rice |
| Does M halt on all inputs? | semantic, non-trivial | ❌ | Rice |
| Is M's language empty? | semantic, non-trivial | ❌ | Rice |
| Does M's source contain `while`? | **syntactic** | ✅ | Read the text |
| Does M have more than 50 states? | **syntactic** | ✅ | Count them |
| Does M halt within **100 steps** on w? | **resource-bounded** | ✅ | Run it 100 steps and look |
| Does M accept *some* language? | semantic, **trivial** | ✅ | Always yes |

The two practical escapes are exactly the ones your tools take:

- **Ask about syntax instead of behaviour.** A linter checking "is there an unused variable?" reads
  structure, not semantics. Decidable.
- **Bound the resources.** "Does it halt in 100 steps?" is decidable because you can just *run* it
  for 100 steps. Every timeout in every test suite is this escape hatch.

Notice `-Werror` sits in the first category and every CI timeout sits in the second.

---

## 5. What This Actually Means for You

It is easy to take undecidability as gloomy. It is better read as a **map of where effort pays off**.

**1. Impossible ≠ useless.** `gcc -Wall` catches real bugs every day while being provably incapable
of catching them all. "Handles the common cases and admits when it is stuck" is the correct design
for a tool in an undecidable domain — not a compromise, the *only* option.

**2. "Don't know" is a legitimate answer.** L35's sound/complete/total triangle is the design space.
Choosing which to drop is an engineering decision, and stating it honestly is what separates a good
tool from a frustrating one.

**3. Testing has a theoretical ceiling.** Week 7 said tests show the presence of bugs, not their
absence. You now know it is a theorem, not a shortcoming of your test suite. Which is why we also
teach invariants, assertions, and types — different attacks on a problem no single attack can win.

**4. Restricted languages can be decidable.** Regular expressions cannot count (L34) — and *because*
they are limited, questions about them are decidable. Total languages like Coq's guarantee
termination by construction, buying decidability at the price of expressiveness. **This trade-off is
a design lever**, and recognising it is the practical payoff of the week: SQL, regex, and type
systems are all deliberately weakened so that questions about them can be answered.

**5. Know the boundary.** The most useful thing you take from today is the reflex to ask *is this
even possible?* before spending a month on it. "Detect all infinite loops in submitted code" is a
request to be pushed back on, and now you can say precisely why, and propose the timeout instead.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| A ≤ B | A solution to B converts into a solution to A: "A is no harder than B" |
| The lever | A undecidable **and** A ≤ B ⟹ B undecidable |
| **Direction** | Reduce **HALT to your problem**. Backwards proves nothing |
| Proof shape | Assume B's decider → transform → argue **both** directions → contradiction |
| PRINTS-HELLO | Wrap the computation, print after it; printing ⟺ halting |
| Rice's theorem | Every non-trivial **semantic** property is undecidable |
| Escape 1 | Ask about **syntax** — decidable |
| Escape 2 | **Bound resources** — "halts in 100 steps?" is decidable |
| Program equivalence | Undecidable — why optimisers use pre-proved transformations |
| The lesson | Undecidability is a map of where to spend effort, not a counsel of despair |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** A student proves EMPTY-LANGUAGE undecidable by writing: "Assume `is_empty(M)` exists.
Given ⟨M, w⟩, use `halts(M, w)` to decide whether M's language is empty." State what is wrong, in one
sentence, and name the error.

**2. (Explain.)** For each, say decidable or undecidable and give the one-line reason:
(a) Does this Python file contain the word `eval`?
(b) Does this program ever call `eval`?
(c) Does this program terminate within 10 seconds on input `x`?
(d) Does this program terminate on every input?

**3. (Build.)** Prove **ALL-HALT** = { ⟨M⟩ : M halts on every input } is undecidable, by reduction
from HALT. Give the wrapper and argue both directions.

**4. (Stretch.)** Your manager asks for a tool that flags every submitted program that will infinite-loop,
with no false positives. Explain why it cannot be built, then propose something buildable and say
which of sound/complete/total you gave up.

### Answers

**1.** The reduction runs **backwards**: it uses `halts` to solve the new problem, when it must use
the new problem's decider to build `halts`.

The error is the **direction of the reduction**. As written, the student has shown
EMPTY-LANGUAGE ≤ HALT, which says only that the new problem is *no harder* than halting — entirely
consistent with it being easy, or even decidable. A correct proof assumes `is_empty` and constructs
a working `halts` from it.

**2.**

| | Verdict | Reason |
|---|---|---|
| **(a)** contains the word `eval` | **Decidable** | Purely **syntactic** — search the source text. Trivially computable. |
| **(b)** ever *calls* `eval` | **Undecidable** | **Semantic** and non-trivial: it is about runtime behaviour. Rice's theorem. (Also directly reducible: wrap `f(x)` and put `eval("1")` after it.) |
| **(c)** terminates within 10 seconds | **Decidable** | **Resource-bounded** — run it for 10 seconds and look. The bound makes it a finite check. |
| **(d)** terminates on every input | **Undecidable** | Semantic, non-trivial — Rice. This is ALL-HALT, proved in Ex 3. |

The (a)/(b) pair is the whole point of §4: nearly identical English, opposite verdicts, because one
asks about **text** and the other about **behaviour**.

**3.** Suppose `all_halt(f)` exists, deciding whether `f` halts on every input. Given an arbitrary
⟨M, w⟩, build:

```python
def halts(M, w):
    def wrapper(anything):   # ignores its own input entirely
        return M(w)          # always runs M on the fixed w
    return all_halt(wrapper)
```

`wrapper` discards its argument and does the same thing regardless — it runs `M` on `w`. So its
behaviour is identical on **every** input, which collapses "halts on all inputs" to "halts on this
one computation."

- **If M(w) halts** — then `wrapper(a)` halts for every `a` (they all just run M on w). So `wrapper`
  halts on all inputs, `all_halt` returns `True`, and `halts` returns `True`. ✅
- **If M(w) runs forever** — then `wrapper(a)` runs forever for every `a`. So `wrapper` does *not*
  halt on all inputs (indeed on none), `all_halt` returns `False`, and `halts` returns `False`. ✅

`halts` is correct on every input, contradicting L35. Therefore `all_halt` does not exist. ∎

*(The trick — an input-ignoring wrapper — is worth remembering. It converts "for all inputs"
questions into "for this one input" questions and shows up in many reductions.)*

**4. Why it cannot be built.** The request is for a decider that is **total** (answers on every
submission), **sound** (no false positives — never flags a program that actually terminates), and
**complete** (flags *every* looping program). That is precisely a decider for the complement of
HALT, which L35 proved impossible. No amount of engineering effort changes this; it is not a hard
problem, it is a nonexistent one.

**What to build instead** — three defensible options, each dropping a different property:

- **A timeout.** Run each submission for 10 seconds; flag whatever is still running. This is
  **total** and **complete** (every genuinely infinite loop gets flagged), and drops **soundness**:
  a correct-but-slow program is flagged too. Simple, and almost always the right answer.
- **A conservative static analyser.** Prove termination where the structure allows it — bounded
  `for` loops, recursion on a decreasing measure — and report `loops` / `terminates` / **`don't know`**.
  This is **sound** and **complete** on what it answers, and drops **totality** by having a third
  answer.
- **Both.** Static analysis to catch the obvious cases instantly, timeouts as the backstop. This is
  what real autograders do.

**What to tell the manager:** not "impossible", but *"perfect detection is provably impossible — here
are three approximations, and here is exactly what each one gets wrong."* That reframing is the
professional skill this week is really teaching.

---

## Reading

- **Sipser, Ch. 5.1, 5.3** — reducibility and mapping reductions (primary)
- **Sipser, Ch. 6.3** — Rice's theorem
- **Regehr, "Undefined Behavior" series** — optional; undecidability's fingerprints in real compilers

---

*CS 101 · Week 11 · Lecture 36 (Fri) · © CSE Department*
