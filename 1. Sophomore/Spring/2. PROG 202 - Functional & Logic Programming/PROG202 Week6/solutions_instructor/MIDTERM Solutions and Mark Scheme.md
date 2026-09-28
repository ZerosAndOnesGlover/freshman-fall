# PROG 202 · Midterm · Solutions and Mark Scheme
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Thursday 5 March, 18:00–19:15 · 75 minutes · 100 marks · 15% of the course · Weeks 0–5**

**What this paper is for.** Three quarters of it is mechanism and one quarter is judgement. The mechanism
half is not recall — **the figures are given on the paper** so that no mark depends on memory — and every
question that quotes one asks *why*, not *what*.

**The four things the paper is really testing**, in order of how much of the rest of the course depends on
them:

1. **Weak head normal form** (A2, B1) — the single most load-bearing definition in Weeks 0–5, and the one
   the second half of the course keeps needing.
2. **That an optimisation is not a guarantee** (B1c, B3c) — the distinction between what `-O2` does and what
   the language promises.
3. **That a type stops short and something else finishes the job** (A3, B2) — types, then a smart
   constructor, then a module boundary.
4. **`>>=`** (A7, C1).

**Marking posture.** Mechanism beats numbers: a right mechanism with a wrong figure keeps most of the marks;
a figure with no mechanism keeps almost none. Say this in the pre-exam briefing, because the paper says it
too.

---

## Section A — Short Answers (30)

**A1. [4]** *Referential transparency:* **an expression can be replaced by its value without changing the
meaning of the program.** [2]

**`getLine` has it.** [1] It is a *value* of type `IO String` — the same value every time it is mentioned,
freely substitutable. What differs is what happens when the runtime **performs** it, and **performing is not
evaluating.** [1]

*Accept "equals may be substituted for equals". Do not accept "it has no side effects" as the definition — 1
of the 2. A student who says `getLine` is **not** transparent loses the 2 marks but keeps the 2 for a coherent
reason, provided they distinguish evaluating from performing somewhere.*

---

**A2. [4]** *WHNF:* **a value whose outermost constructor is known.** [2] Nothing is claimed about its
fields.

`:sprint p` shows **`p = (_,_)` — unchanged.** [1] Because `p` was **already** in WHNF: the pair constructor
was known the moment `p` was written, so `seq` had no work to do, **and it never touches the components.** [1]

*"Evaluated one level" without "outermost constructor" scores 1 of the 2. This is the definition B1 depends
on, so mark it consistently across the two.*

---

**A3. [5]** **12 accepted.** [1] **From 3! × 2! = 12** — any permutation keeping the three `String`s among
the string positions and the two `Int`s among the integer positions is indistinguishable to a type synonym,
so 11 of the 12 are wrong. [2]

After the redesign the surviving wrong ordering is **`start` and `end` exchanged**, because they are the only
pair of fields still sharing a type (`Minutes`). [2]

*Accept 12 with "3 strings and 2 ints can be permuted among themselves" and no factorials.*

---

**A4. [4]** **Two arguments.** [2] The compiler supplies a **dictionary** — a record of `Eq`'s methods for
the chosen type — so the generated code takes three. [1] **At the call site**, chosen from the type. [1]

*Deduct both of the first 2 for "three". This is the misreading L09 was written to kill and it is worth
flagging on the script.*

---

**A5. [5]** **The operator decides.** [1]

- **Strict in the accumulator → `foldl'`**, named operator: `+`, `*`, `max`. [2]
- **Lazy in its second argument → `foldr`**, named operator: `&&`, `||`, `:`, `++`. [2]

*A rule phrased in terms of the list ("use `foldl'` for long lists") scores 1. **`foldl` unprimed should not
appear in a correct answer**; note it if it does.*

---

**A6. [5]** **The one fact: a tuple is `Foldable` in its second component only**, because the functor is
`(,) a` — so `a` is part of the *structure*, not an element. [2] Generalising: **`Foldable` counts
*elements*, and which parts of a type are elements is the instance's decision.**

- `length ('x', 5)` = 1 — one element. [1]
- `maximum ("hello", 3)` = 3 — `"hello"` is structure. [1]
- `maximum (Left "x")` **throws** and `length (Left "x")` is 0 — `Either a` is foldable in its `Right` only,
  so a `Left` is an **empty** container: `length` of nothing is 0 and `maximum` of nothing is an error. [1]

*Full marks require the four to come from *one* fact, as asked. Four separate correct explanations score 3.*

---

**A7. [4]** `m >>= \x -> n x >>= \y -> pure (x, y)` [2]

**`<-` is the parameter of a lambda that `>>=` is about to be given.** [2] Which is why it cannot be
reassigned and why it is not assignment.

*Accept "the binder of the function passed to `>>=`". "It extracts the value from the monad" scores 1 — it is
the intuition, not the answer.*

---

## Section B — Applied Judgement (40)

### B1. Where the memory went [14]

**(a) [5]** **`foldl'` forces its accumulator to weak head normal form, and the accumulator is a pair** — so
each step confirms the pair *constructor* and leaves both components unevaluated. [3]

**Two chains, each 10⁷ links long** — one for `s`, one for `c`. [2]

*Require "weak head normal form" (the question asks for it) and require the count to be **two** chains; "a
chain of thunks" singular scores 1 of the 2, because it suggests they have not noticed the pair has two
fields.*

**(b) [4]** Any two of: [2 for two working fixes]

```haskell
step (!s, !c) x = (s + x, c + 1)                 -- bang patterns
step (s, c) x = s `seq` c `seq` (s + x, c + 1)    -- by hand
data Acc = Acc !Int !Int                          -- strict fields
```

**Which to ship: the strict data type.** [2] Because the strictness becomes a property of the **type**, so
every construction anywhere is strict and no caller has to remember — *and* it removes the pair allocation
entirely (110 KB against 160 MB at `-O2`).

*Accept bang patterns as the shipped answer if defended on the grounds that it is local and does not change a
shared type. Do not accept a choice with no reason.*

**(c) [5]** **Strictness analysis.** [1]

**The answer to the colleague [2]:** the 44 KB is an optimisation GHC is *permitted* to make, not part of the
program's meaning — the `-O0` figure is the proof — and a small change (an accumulator only conditionally
demanded) defeats the analysis at any level while looking identical.

**The case where it does not save you [2]** — one of:

- **`Data.Map.Lazy` as a counter: 107 MB against `Strict`'s 44 KB, *both at `-O2`***. The analyser cannot see
  inside a balanced tree. **This is the best answer.**
- **The two-pass mean: 245 MB at `-O0` and 289 MB at `-O2`** — retention, which no optimisation addresses.
- **`foldr (+) 0`: 130 MB at `-O2`.**

*A measurement is required. A named case with no figure scores 1 of the 2.*

---

### B2. What the types left open [12]

**(a) [4]** **It returns `Either String Session`, so the caller cannot obtain a `Session` without handling
the failure** — the type makes the error case unskippable. [3] A `Bool`-returning validator can be ignored,
and its result is a separate value the caller may forget to consult. [1]

*Accept "it carries a reason" for 1 of the 4, but the unskippability is the point.*

**(b) [4]** **An export list that exports the type without its constructor.** [1]

```haskell
module Sched (Session, mkSession, …) where     -- not Session (..)
```
[1]

**Without it a caller uses the raw constructor.** [2] Measured in Lab 1: with `Session (..)` exported,
`./break` prints `PROG 202 LEC Tue 12:15-11:00` and **exits 0** — no crash, just a bad value that will give a
wrong answer somewhere later.

*"A validation function is a convention until a module boundary makes it a guarantee" is the sentence; accept
any phrasing with both halves.*

**(c) [4]** `longest` is a **maximum**, so `mempty`'s third field must be the **identity of `max`** — the
smallest possible duration. **`0` is right only because no duration is ever ≤ 0, and `mkSession` is what
guarantees that** by rejecting `start >= end`. [3]

**Without it you would need `minBound :: Int`** — which works because `Int` is `Bounded`, and which is exactly
why the standard library's `Data.Semigroup.Max` requires `Bounded` for its `Monoid` instance. [1]

*This is the paper's best cross-week question and about half the cohort will miss the `mkSession` link. Note
it on the script: **the laws you can satisfy depend on the invariants you established three weeks earlier.***

---

### B3. Reading a fold [14]

**(a) [4]** `foldr (-) 0 [1,2,3]` = `1 - (2 - (3 - 0))` = **2** [2]
`foldl (-) 0 [1,2,3]` = `((0 - 1) - 2) - 3` = **−6** [2]

*Require the bracketing. A bare 2 and −6 scores 2 of the 4.*

**(b) [5]** `foldr`'s outermost application involves the **first** element: `f x₁ (foldr f z rest)`. [2]
So an operator that ignores its second argument — `||` when the first is `True` — never examines the rest. [1]

`foldl'`'s outermost application involves the **last** element, so it cannot produce anything until it has
reached the end of the list, and `[1..]` has no end. [2]

*Full marks require the word "outermost" or an equivalent structural statement about which end the fold's
top-level application comes from.*

**(c) [5]** **`-O0` [1]:** neither is repaired; `foldl` is worse because its thunk chain is one heap object
per element with an extra indirection, on top of the list.

**`-O2` [1]:** **strictness analysis** repairs `foldl` — it proves the accumulator is demanded and evaluates
as it goes — giving 44 KB.

**Why `foldr` is never repaired [3], and this is the marked part:**

| | what is held |
|---|---|
| `foldl` | a **thunk chain in the heap**, one link per element. Removable: force as you go |
| `foldr` | the **stack of suspended applications**, one frame per element |

To compute `foldr`'s outermost `+` you need its right operand, which is another `+`, and so on **to the end
of the list** — so the recursion genuinely must descend fully before any addition happens. **It is the order
of the work, not the strictness of it**, and no analysis can change the order without changing the meaning.

*A student who says "same problem, both laziness" scores 1 of the 3. The distinction is the question.*

---

## Section C — Longer Answers (30) · **any TWO, 15 each**

### C1. Write `State` from scratch [15]

```haskell
newtype State s a = State { runState :: s -> (a, s) }

instance Functor (State s) where
  fmap f (State g) = State $ \s -> let (a, s') = g s in (f a, s')

instance Applicative (State s) where
  pure a = State $ \s -> (a, s)
  State f <*> State g = State $ \s -> let (h, s') = f s; (a, s'') = g s' in (h a, s'')

instance Monad (State s) where
  State g >>= f = State $ \s -> let (a, s') = g s
                                    State h = f a
                                in  h s'

get           = State $ \s -> (s, s)
put s         = State $ \_ -> ((), s)
evalState m s = fst (runState m s)
execState m s = snd (runState m s)
```

| | |
|---|---:|
| the `newtype` | 2 |
| `Functor` | 2 |
| `Applicative` (`pure` alone earns 1 of the 2) | 2 |
| **`Monad`** | **4** |
| `get`, `put`, `evalState`, `execState` | 3 |
| the `>>=` annotation and which instances `do` uses | 2 |

**The `>>=` annotation must have three steps:** run the first computation from the incoming state; feed its
result to `f`, **which returns the next computation, not a value**; run that from the new state.

**Which instances `do` calls:** `>>=` from `Monad` and `pure` from `Applicative`. **`fmap` is never called by
`do`.** All three instances must nevertheless *exist*, because of the superclass chain — a student who
separates "what `do` calls" from "what the hierarchy requires" gets both marks.

*Verified reference: `OwnState.hs` in Week 5's `solutions_instructor/`. Order of the instances matters only
in that all three must be present; do not deduct for declaration order in the script.*

---

### C2. "Laziness is a feature, and the space cost is the price of it." [15]

**No expected conclusion. A defended "against" is worth full marks.**

| | |
|---|---:|
| **three** measurements from the course, correctly attributed | 6 |
| one case where laziness bought what strictness could not | 3 |
| one case where the cost was **not visible in the source** | 3 |
| a position, defended, that engages with its own counter-evidence | 3 |

**Bought what strictness could not:** `foldr` answering `True` over `[1..]` where `foldl'` never terminates ·
`take 10 fibs` and knot-tying · `sqrts`/`within` computing **six** approximations out of infinitely many ·
`null (Just undefined)` not forcing · generate-and-test over an infinite space returning `(3,4,5)`.

**Cost not visible in the source:** 44 KB against 273 MB for the same answer, the difference being whether
the list is *named* · the one-pass mean's 727 MB *using the strict fold* · the two-line `primes` being 19×
slower than a real sieve with nothing in its shape to say so · `Data.Map.Lazy` at 107 MB.

**The strongest "against" answers** argue that "price" is the wrong word because the cost is **not
predictable from the text** — you cannot budget for a price you cannot read — and cite the `primes` sieve or
the two-pass mean. **Reward that.**

*Deduct for an answer that lists measurements without taking a position, and for a position with fewer than
three measurements. Do not reward length.*

---

### C3. "A type class is just an interface." [15]

| | |
|---|---:|
| three differences, each with what it lets you write | 9 |
| one involving a class variable **only in the return type** | 3 |
| *coherence*, and the cost this course showed | 3 |

**The four available differences** (any three):

1. **Declared anywhere**, including in a module owning neither the class nor the type — so you can retrofit
   `instance Eq TheirType`. Java cannot add `implements` to someone else's class.
2. **Dispatch on any position, including the return type.** `mempty :: Monoid a => a` has no receiver at all;
   `read :: Read a => String -> a`; `pure`. **No OO interface can express `mempty`** — this is the required
   one, and 3 of the 15 depend on it.
3. **Exactly one instance per type, program-wide** (coherence), against many-interfaces-one-implementation.
4. **Dictionaries are passed at the call site**, so the same value can be used at several instances in one
   expression; a Java object's vtable is fixed at construction.

**Coherence [3]:** one instance of a class for a type across the whole program. **The cost this course
showed:** there is **no `instance Monoid Int`**, because `+`/0 and `*`/1 are equally canonical and the
language declines to choose — hence the `newtype`s `Sum` and `Product`. *Accept the orphan-instance warning as
the cost instead.*

*A student who answers only "Haskell's are more flexible" with no mechanism scores 3 of the 15.*

---

## Marks

| Section | | Marks |
|---|---|---:|
| **A** | Short answers, A1–A7 | **30** |
| **B** | B1 14 · B2 12 · B3 14 | **40** |
| **C** | any two of three, 15 each | **30** |
| | **Total** | **100** |

---

## After Marking

**Two figures to compute before the Week 7 tutorial:**

1. **The A2/B1a pair.** How many students defined WHNF correctly in A2 *and* then failed to apply it in B1a?
   That gap is the one to spend Week 7's tutorial on, and it is the definition Weeks 6–12 keep needing.
2. **B3(c) answered "same problem".** This predicts trouble in Week 7, where `par` on a thunk nobody forces
   is a 1.0× speed-up for exactly this reason.

**One thing to say when handing the paper back:** the figures were printed on the paper, so nobody lost a mark
to memory — **every mark lost was a mechanism.** That is the point of giving them, and it is worth making
explicit before the final, where the same policy applies.

**Grade release:** two weeks, per [[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]].

---

*PROG 202 · Week 6 · Midterm Solutions and Mark Scheme · INSTRUCTOR ONLY · © CSE Department*
