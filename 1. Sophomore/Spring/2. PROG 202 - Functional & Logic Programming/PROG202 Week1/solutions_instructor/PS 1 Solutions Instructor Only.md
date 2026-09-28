# PROG 202 · Problem Set 1 · Solutions
## Algebraic Data Types, Pattern Matching, and Type Inference
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 1 Wednesday · **Due:** Week 2 Friday 17:00 · **100 points** · **15 parts, ~3 hours**

**What this paper is testing.** Q1 tests whether they can count a type, which is the skill behind every
design decision in Q2. Q2 is the design question and carries the most marks. Q3 is what the compiler
can and cannot see. Q4 is inference, and Q4(b) is the one that separates students who ran the
experiment from students who repeated the lecture. Q5 is `sched`.

**Timing:** Q1 25 min, Q2 50 min, Q3 30 min, Q4 40 min, Q5 35 min.

**Marking note carried from PS 0:** a stated prediction that turns out wrong, honestly reported and
explained, is full marks. A bare right answer with no prediction is half.

---

## Q1: Counting Types (18)

### (a) [8]

| Type | Count | Working |
|---|---:|---|
| `Maybe (Bool, Bool)` | **5** | 1 + (2 × 2) |
| `Either Bool (Maybe Bool)` | **5** | 2 + (1 + 2) |
| `Bool -> Maybe Bool` | **9** | 3² |
| `(Bool, ())` | **2** | 2 × 1 |
| `Maybe Bool -> Bool` | **8** | 2³ |
| `() -> ()` | **1** | 1¹ |

**The rules:** `|(a, b)| = |a| × |b|` · `|Either a b| = |a| + |b|` · `|a -> b| = |b|^|a|`.

**One mark per row, two for the rules.** The two that catch people:

- **`Bool -> Maybe Bool` is 9, not 6.** A function must choose a result *for each* argument, so it is
  `|result|^|argument|`, not the product. Students who write 6 have multiplied.
- **`() -> ()` is 1.** There is exactly one function, and it is `id`. A surprising number write 0,
  reasoning that there is "nothing to return"; there is — `()`.

*A student who notices that rows 1 and 2 are both 5 and asks whether the types are therefore "the same"
has found Week 12's subject. They are **isomorphic**, not equal. Say so and move on.*

### (b) [5]

```haskell
id            -- True -> True,  False -> False
not           -- True -> False, False -> True
const True    -- both to True
const False   -- both to False
```

**There is no fifth.** [3]

**`Bool -> Bool -> Bool` has 16** — it is `|Bool -> Bool|^|Bool|` = 4². [1] Three by name: `(&&)`,
`(||)`, `(/=)` *(which is `xor`)*, `const id`, `const not`, `\_ _ -> True`. [1]

*Do not accept "4 × 2 = 8". The reasoning matters more than the number here.*

### (c) [5]

```haskell
data Slot = Slot { taken :: Bool, takenBy :: Maybe String, freeFrom :: Maybe Int }
```

**States:** 2 × (1 + *s*) × (1 + *n*). [1]

**Meaningful:** *s* + *n* — either taken by somebody, or free from some time. [1] **The invariant the
type does not enforce:** `taken` is `True` **iff** `takenBy` is a `Just`, and `freeFrom` is a `Just`
**iff** `taken` is `False`. Three fields, two of them redundant, and nothing checks the agreement. [1]

**The replacement:** [2]

```haskell
data Slot = Taken String | Free Int
```

`2 × (1 + s) × (1 + n)` becomes `s + n`. **Accept `Either String Int`**, which is the same type with
worse names — but require them to notice that `Left`/`Right` says nothing about which is which, and
that this is exactly why you declare your own type rather than reaching for `Either`.

---

## Q2: Designing the Type (22)

### (a) [8]

Many correct answers. The shape being marked:

```haskell
data Assessment
  = ProblemSet Int Int          -- number, due week
  | Lab Int                     -- number; covers week N, sat in week N+1
  | Quiz Int                    -- number; sat week N, covers week N-1
  | Midterm                     -- Week 6, Weeks 0-5
  | Project Int Int             -- number, due week
  | Final
  deriving (Show, Eq)

weight :: Assessment -> Double
weight (ProblemSet _ _) = 0.40 / 13   -- 40% over PS 0-12
weight (Project _ _)    = 0.15        -- 15% each, two of them
weight Midterm          = 0.15
weight Final            = 0.15
weight (Lab _)          = 0.0         -- required, unweighted
weight (Quiz _)         = 0.0
```

**Mark scheme [8]:**

| | |
|---|---:|
| a sum type with one constructor per kind, **no `Maybe`, no `Bool`** | 3 |
| each constructor carries exactly the fields that kind has, and no others | 2 |
| `weight` exhaustive, `-Wall` silent | 1 |
| the figures agree with the syllabus and **sum to 1.0** | 2 |

**The check:** 13 × (0.40/13) + 2 × 0.15 + 0.15 + 0.15 = 0.40 + 0.30 + 0.30 = **1.00** ✓. A student
whose weights do not sum to 1 has not read the syllabus; deduct both marks and say which table.

**Two traps.** *"Lowest problem set dropped"* makes the per-PS weight arguably 0.40/12; accept either
with a stated assumption. And **a `Weighted Bool` field, or `marks :: Maybe Int`, loses 3 marks** —
that is precisely the thing the question forbids, and a few will do it anyway.

### (b) [8]

```haskell
eval :: Expr -> Int
eval (Lit n)   = n
eval (Add a b) = eval a + eval b
eval (Mul a b) = eval a * eval b
eval (Neg a)   = negate (eval a)
```

**`render` with no redundant brackets [4]** needs a precedence argument. The standard solution:

```haskell
render :: Expr -> String
render = go 0
  where
    go _ (Lit n)   = show n
    go p (Add a b) = paren (p > 6) (go 6 a ++ " + " ++ go 7 b)
    go p (Mul a b) = paren (p > 7) (go 7 a ++ " * " ++ go 8 b)
    go p (Neg a)   = paren (p > 9) ("-" ++ go 10 a)
    paren True  s  = "(" ++ s ++ ")"
    paren False s  = s
```

Accept any scheme that gets `Add (Lit 2) (Mul (Lit 3) (Lit 4))` → `2 + 3 * 4` **and**
`Mul (Add (Lit 2) (Lit 3)) (Lit 4)` → `(2 + 3) * 4`. A student who brackets everything gets **2 of the
4** — it is correct output and it is not what was asked.

**Adding `Sub` [2].** The exact warnings:

```
Pattern match(es) are non-exhaustive
In an equation for ‘eval’: Patterns of type ‘Expr’ not matched: Sub _ _
```

and the same for `render`'s `go`. **Require the quoted text**, including `Sub _ _` — the wildcards are
the detail that shows they ran it.

**The associativity question [2].** `render (Sub (Lit 1) (Sub (Lit 2) (Lit 3)))` must **not** be
`1 - 2 - 3`, because that reads as `(1 - 2) - 3` = −4 and the expression is `1 - (2 - 3)` = 2.
Subtraction is left-associative, so a right-nested `Sub` **needs the brackets**: `1 - (2 - 3)`.

**In the scheme above this falls out of the asymmetry** `go 6 a ++ … ++ go 7 b` — the right operand is
asked at one level higher than the left. **Full marks require noticing that `Add` and `Mul` did not need
this and `Sub` does**, and saying why: they are associative and it does not matter.

### (c) [6]

- **Declaration order**, left to right, in the `data` declaration. [2]
- **A type where it is a bug** [2] — anything whose natural order differs from the typed order, e.g.
  `data Severity = Debug | Error | Info | Warning`, where `Error < Info` is now true and every log
  filter silently mis-ranks. Full marks also for *a type with no meaningful order at all*
  (`data Colour = Red | Green | Blue`): deriving `Ord` there does not give a wrong order, it invites
  code that depends on one that means nothing. **That is the better answer.**
- **`Priority = Low | Medium | High | Critical`: yes, deriving `Ord` is right** [2] — the declaration
  order *is* the semantic order, which is the only condition. Accept a "no" that argues the ordering
  should be written explicitly so that reordering the constructors cannot change behaviour; that is a
  defensible engineering position and the reasoning is what is marked.

---

## Q3: Pattern Matching (20)

### (a) [7]

| | Compiles? | Matches |
|---|---|---|
| 1. `f (Just x : rest) = x` | **yes** | a non-empty list whose head is a `Just`. Non-exhaustive: `[]` and `Nothing : _` |
| 2. `g all@(x:_) = (all, x)` | **yes** | any non-empty list, binding the whole list *and* its head. Shadows `Prelude.all`, so `-Wall` gives `-Wname-shadowing` |
| 3. `h (Session {day = d}) = d` | **yes** | any `Session`, binding one field |
| 4. `k [a, b] = a + b` | **yes** | a list of **exactly** two. Non-exhaustive for every other length |
| 5. `m (x:x:rest) = x` | **NO** | — |

**Item 5 is the answer [3 of the 7].** Haskell has **no non-linear patterns**: a variable may appear at
most once in a pattern. It does *not* mean "a list whose first two elements are equal".

```
q3m.hs:1:4: error:
    • Conflicting definitions for ‘x’
      Bound at: q3m.hs:1:4
                q3m.hs:1:6
    • In an equation for ‘m’
```

**`Conflicting definitions` is not an obvious message for this mistake**, which is why it is worth
asking about. The intended meaning needs a guard: `m (x:y:_) | x == y = x`.

### (b) [7]

Both warnings, verbatim, are in L04 §2. [4]

**Why GHC can name `SEM` and not the `String` case [3].** Because `Kind` **has four values and the
compiler knows all four**, so the uncovered set is a finite list it can print. `String` is infinite,
so the uncovered set can only be described by a *pattern over characters* — GHC produces four such
clauses and then prints `...` because there is no end to them.

**This is a fact about the types, not about GHC's cleverness**, and that is the sentence being marked.
No compiler, however good, can enumerate the complement of three string literals in an infinite set.

### (c) [6]

```haskell
p :: B -> String              q :: [Int] -> Int
p = why                       q = head
```

| | crashing input | runtime message |
|---|---|---|
| `p` | `Ok 1` — any `Ok` | `No match in record selector why` |
| `q` | `[]` | `Prelude.head: empty list` |

[1 each for the input, 1 each for the message.]

**What to write instead [2]:**

- **`p`: a data-design change.** Do not spread one record's fields across a sum. Give `Cancelled` its
  own `reason` field and **pattern-match** instead of using a selector:
  `p (Bad _ w) = w; p (Ok _) = ""`. `-Wall` then checks it.
- **`q`: a type change.** `q :: [Int] -> Maybe Int`, `q = listToMaybe`. Once the type admits the empty
  case the caller must handle it.

**The remark worth writing on scripts:** *both of these compile with zero warnings under `-Wall` on this
GHC.* `-Wincomplete-record-selectors` does not exist here and neither does `-Wx-partial`. **So two of
the three ways to crash on an unconsidered case are invisible to this compiler**, and the defence is
design, not flags.

---

## Q4: Inference (20)

### (a) [7]

```
f1 :: b -> a -> (a, b)
f2 :: a -> [a]
f3 :: (t -> t) -> t -> t
f4 :: (b -> c) -> (a -> b) -> a -> c
f5 :: Num a => Bool -> a
```

[1 each for f1–f4, 3 for f5.]

**`f5` is the marked one.** It is **`Num a => Bool -> a`**, not `Bool -> Int`. The literals `1` and `0`
are overloaded — `1 :: Num a => a` — so nothing in the function forces a concrete numeric type, and
inference keeps it general. `f5 True :: Double` is legal.

*Students who wrote `Bool -> Int` have been misled by GHCi's defaulting when they printed it. Ask them
to try `f5 True + 0.5`.*

*`f3` is `(t -> t) -> t -> t`: because `f` is applied to its own result, argument and result type must
unify.*

### (b) [7]

**Experiment 1 — the `/` mistake.** With signatures: `A.hs:9:37`. Without: `B.hs:6:37` — **the same
line of the same code** (line 6 of the stripped file is line 9 of the original). **The error did not
move.**

**Experiment 2 — `Shape.hs`, `snd` → `fst`.** With the signature on `busiest`:

```
Shape.hs:19:35: error: • Couldn't match type ‘Int’ with ‘[Char]’
```

Without it:

```
Shape.hs:23:29: error:
    • No instance for (Num String) arising from the literal ‘150’
```

**Line 23, in `main`'s `where`, four lines away, blaming the number 150.** [4 for the four
line/message pairs.]

**The explanation [3], and this is the question.** In experiment 1, the wrong type is
**self-contradictory inside `average`** — `total xs` is an `Int` by `minutesOf`, `/` needs
`Fractional`, and `Int` is not, so the clash is local whether or not a signature is present.

In experiment 2, `fst . last . sort . map swap` is **perfectly consistent on its own**: without a
signature GHC happily infers `busiest :: (Ord a, Ord b) => [(a, b)] -> b`-ish, propagates that out
through `main`, and the first genuine contradiction is in the *data*.

**So the rule is not "signatures move errors closer".** It is: **a signature stops a wrong-but-coherent
type from escaping the definition that made it.** When the mistake is locally contradictory, inference
localises it perfectly well on its own.

**Deduct for "signatures always give better errors"** — their own experiment 1 disproves it and that is
why both experiments are on the paper.

### (c) [6]

One paragraph, marked on whether it uses their own numbers. [4]

**The case where a signature changes the *meaning* [2]:** narrowing. `sumInts :: [Int] -> Int` is a
different function from the inferred `Num a => [a] -> a` — it can be applied to fewer things, and
downstream code that would have been polymorphic is now monomorphic. Also accept **the monomorphism
restriction**: `f = (+)` at the top level with no signature gets defaulted to a single type, and adding
`f :: Num a => a -> a -> a` makes it polymorphic. Either answer is full marks; the second is better
and rarer.

---

## Q5: `sched`, Retyped (20)

### (a) [7]

```
tuple    120 tried, 12 accepted, 11 wrong
middle   120 tried,  2 accepted,  1 wrong  -> [(0, 1, 2, 4, 3)]
strict   120 tried,  1 accepted,  0 wrong
```

[3 for the table.]

- **`(0,1,2,4,3)` is `start`/`end` swapped** — positions 3 and 4 exchanged, the only remaining pair of
  fields sharing a type. [1]
- **Two costs of `strict`** [2], and a line of code is required. The two that earn it:
  `start a < end b` **does not compile** (`Couldn't match expected type ‘Start’ with actual type
  ‘End’`), so `overlaps` needs a conversion that destroys the protection; and it does not scale — five
  fields need five newtypes and five `Show` instances, and nobody keeps it up on a twelve-field record.
- **Which to ship** [1]: `middle`, with `mkSession` closing the last hole. Accept `strict` **only** if
  they have written a working `overlaps` for it.

### (b) [7]

**The 08:00–18:00 check** — a `Left`, and **no type could reasonably do it**: it is a predicate on an
`Int`, and a type that encoded it would be a `newtype` with a smart constructor, which is the same
check moved one level down. *(A student who says "a refinement type could" is right and is describing
something Haskell does not have. Give the mark.)* [3]

**The `LEC` on an untimetabled day** — also a `Left`, and here **a type could have done it**, which is
the interesting half: `data LectureDay = LMon | LTue | LWed | LThu | LFri` is no help, but making the
timetable's *structure* carry the constraint — a per-course list of its own days — removes the
possibility. Full marks require noticing that the two cases differ in this respect. [3]

Output with a bad session, for either: [1]

```
rejected: PROG 202 LEC Sat: …
```

*(Accept any correct rejection message.)*

### (c) [6]

```
Break.hs:14:7: error:
    • Illegal term-level use of the type constructor or class ‘Session’
    • imported from ‘Sched’ at Break.hs:11:1-12
    • Perhaps use variable ‘mkSession’ (imported from Sched)
```

**It does not say "not exported" [2].** It says a **type** name has been used where a **value** was
wanted — because `Session` the type *is* exported and in scope, and `Session` the constructor is not.
Types and values are separate namespaces (L03 §2) and the export list let exactly one of the two
`Session`s through.

**With `Session (..)` [2]:** it compiles, and at run time `./break` prints
`PROG 202 LEC Tue 12:15-11:00` and **exits 0**. No crash. The bad value simply exists.
*Bonus-worthy observation: `Session (..)` also re-exports the five accessors the list already names, so
GHC emits three `-Wduplicate-exports` warnings. The "fix" is not even clean.*

**The sentence [2]:** *the check in `mkSession` only helps if there is no other way to make a `Session`,
and the export list is the only thing that makes that true.* **Reject "because `mkSession` validates
its input"** — that is the belief the question disproves.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Counting types | 3 | 18 |
| 2 | Designing the type | 3 | 22 |
| 3 | Pattern matching | 3 | 20 |
| 4 | Inference | 3 | 20 |
| 5 | `sched`, retyped | 3 | 20 |
| | **Total** | **15** | **100** |

---

## What to Watch For Across the Cohort

1. **`Bool -> Maybe Bool` answered as 6.** They have multiplied where they should have exponentiated,
   and Q2(a)'s state count then comes out wrong too. Five minutes in the Week 2 tutorial.
2. **A `Maybe` or a `Bool` surviving in Q2(a).** The single most important habit this week is meant to
   install. Name it on the script.
3. **Q4(b) answered as "signatures always help".** Their own experiment 1 disproves it. This is the
   paper's best discriminator between reading and running.
4. **Q5(c) answered as "`mkSession` validates the input".** They did §5 of the lab without the point
   landing. Worth raising in the tutorial rather than in feedback, because most of the room will have
   it.

---

*PROG 202 · Week 1 · PS 1 Solutions · INSTRUCTOR ONLY · © CSE Department*
