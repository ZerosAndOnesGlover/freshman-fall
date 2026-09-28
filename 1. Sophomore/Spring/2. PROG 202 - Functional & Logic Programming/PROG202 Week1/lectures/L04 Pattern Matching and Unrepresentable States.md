# PROG 202 · Functional & Logic Programming
## Week 1 · Lecture 2 of 2
### Pattern Matching, Exhaustiveness, and Making Bad States Unrepresentable

*“Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming.”* — Rob Pike, "Notes on Programming in C" (1989), rule 5

---

**Sat:** Thursday of Week 1, 11:00–12:15, TH 205 · **Reading:** Hutton §4.1–4.4, §8.5–8.6 · **Next:** Week 2 L05, higher-order functions and folds

**Coursework:** 📝 **PS 0** due Fri this week 17:00 · 📊 **Quiz 2** Tue of Week 2 · 📝 **PS 2** released Wed of Week 2, due Fri of Week 3 17:00 · 🔬 **Lab 1** Wed of Week 2 13:00–14:50

---

## 1. A Pattern Takes a Value Apart Along the Seams the Type Provides

Every `data` declaration you write is simultaneously a way to **build** values and a way to **take
them apart**. The constructors are both.

```haskell
data Booking = Pending Session
             | Confirmed Session Course
             | Cancelled Session String

status :: Booking -> String
status (Pending   _)     = "waiting"
status (Confirmed _ c)   = "confirmed for " ++ show c
status (Cancelled _ why) = "cancelled: " ++ why
```

**Three equations, one per constructor.** Each names the fields it needs and wildcards the rest. There
is no `if`, no tag field, no `instanceof`, and no possibility of asking a `Pending` for its
cancellation reason — **that question cannot be written.**

The forms you will use, all of them this week:

| Pattern | Matches | Note |
|---|---|---|
| `Tue` | that exact constructor | a nullary constructor is a pattern |
| `Just x` | a `Just`, binding its field to `x` | |
| `(a, b)` | any pair | a tuple pattern; **cannot fail** |
| `[]` / `(x:xs)` | empty / non-empty list | these two are the whole of list recursion |
| `[a, b, c]` | a list of **exactly** three | sugar for `a:b:c:[]` |
| `_` | anything, binding nothing | **"wildcard"** |
| `all@(x:xs)` | the whole value *and* its parts | **"as-pattern"**; `all` is the original list |
| `Session {day = d}` | a record, binding one field | record pattern; ignores the rest |
| `0`, `'x'`, `"LEC"` | a literal | works via `Eq`; the reason `String` matching is possible |

**Patterns nest, and this is where they earn their keep:**

```haskell
firstLecture :: [Session] -> Maybe Course
firstLecture []                            = Nothing
firstLecture (Session {kind = LEC, course = c} : _) = Just c
firstLecture (_ : rest)                    = firstLecture rest
```

Three cases, read top to bottom, **first match wins**. The middle line matches *a non-empty list whose
head is a session whose kind is LEC* — a condition three levels deep, expressed by writing the shape
of the thing you want.

### Guards, when the condition is not about shape

```haskell
lengthClass :: Session -> String
lengthClass s
  | d >= 110  = "double"
  | d >= 75   = "long"
  | d >= 50   = "standard"
  | otherwise = "short"
  where d = duration s
```

`|` here is read **"such that"**. **Guards are for questions about values; patterns are for questions
about shape**, and mixing them up is the commonest structural mistake in first-week Haskell.
`otherwise` is not a keyword — it is an ordinary library definition equal to `True`, as `:i otherwise`
will tell you (`otherwise :: Bool -- Defined in 'GHC.Base'`).

### `case … of` is the same thing as an expression

```haskell
describe :: Maybe Session -> String
describe ms = case ms of
  Nothing -> "free"
  Just s  -> show (course s) ++ " at " ++ show (start s)
```

Equations at the top level and `case` in the middle of an expression are **the same mechanism**; use
equations when you are defining a function by its argument's shape, and `case` when you need to match
something that is not an argument.

---

## 2. Exhaustiveness: What the Compiler Can and Cannot Check

Here is the measurement that justifies L03 §4's insistence on sum types over strings.

`resources/exhaustive.hs` defines the same function twice — once over a four-constructor `Kind`, once
over `String` — each missing the `SEM` case:

```haskell
data Kind = LEC | LAB | REC | SEM deriving (Show, Eq)

roomFor :: Kind -> String            roomForS :: String -> String
roomFor LEC = "TH 205"               roomForS "LEC" = "TH 205"
roomFor LAB = "BH 215"               roomForS "LAB" = "BH 215"
roomFor REC = "SSB 108"              roomForS "REC" = "SSB 108"
```

`ghc -Wall -fno-code exhaustive.hs`:

```
exhaustive.hs:5:1: warning: [-Wincomplete-patterns]
    Pattern match(es) are non-exhaustive
    In an equation for ‘roomFor’:
        Patterns of type ‘Kind’ not matched: SEM
```

```
exhaustive.hs:11:1: warning: [-Wincomplete-patterns]
    Pattern match(es) are non-exhaustive
    In an equation for ‘roomForS’:
        Patterns of type ‘String’ not matched:
            []
            (p:_) where p is not one of {'L', 'R'}
            ['L']
            ('L':p:_) where p is not one of {'E', 'A'}
            ...
```

**Both warn. Only one of them tells you anything.**

For `Kind`, GHC names the missing case: **`SEM`**. You fix it in five seconds. For `String`, GHC tries
to describe the uncovered part of an infinite set, produces four clauses about individual characters,
and **gives up with an ellipsis.** The warning is technically correct and operationally useless.

**This is the real argument for sum types, and it is not "types are good".** It is: *a type with a
finite, known set of values lets the compiler tell you which case you forgot, by name.* A `String`
cannot, ever, no matter how good the compiler gets.

Run either one and you get the same failure, at the same cost:

```
$ ./exhaustive
exhaustive: exhaustive.hs:(7,1)-(9,26): Non-exhaustive patterns in function roomForS
```

**A `Non-exhaustive patterns` crash is the one runtime error this course wants you never to ship**, and
`-Wall` is how. It is Haskell's null-pointer exception: the case you did not think about, discovered
by a user.

> **`-Wall` on GHC 9.4.7 covers more than people expect, and two things it does not cover at all.**
>
> It *does* include `-Wincomplete-uni-patterns`, so `let Just x = lookup k m` is caught — checked, not
> assumed; older advice that you must add that flag yourself is out of date, it joined `-Wall` in 9.2.
>
> **What nothing here catches:** a **partial record selector** (L03 §2 — there is no
> `-Wincomplete-record-selectors` on this GHC at all) and **`head`/`tail`/`fromJust` on an empty
> value**. Measured: `print (head ([] :: [Int]))` compiles with **zero warnings** under `-Wall` and
> dies with `Prelude.head: empty list`. `-Wx-partial`, which would catch it, is not recognised here
> either.
>
> **So two of the three ways to crash on a case you did not consider are invisible to this
> compiler.** The defence is the same for both and it is this lecture's subject: **do not have a case
> you did not consider** — return a `Maybe` instead of calling `head`, and give each constructor its
> own fields instead of sharing a selector. Lab 1 §3 has you find one of each.

---

## 3. Making Bad States Unrepresentable

Pattern matching is what you *do* with a good data type. This section is about getting one.

**The design rule, and it is the most transferable thing in this course:** when a combination of
fields is meaningless, **arrange the type so that the combination cannot be written**, rather than
checking for it at every use.

### The `Booking` example, done badly and then well

Here is the shape a first draft usually takes — and it is what you would write in any language with
records and no sum types:

```haskell
data Booking = Booking
  { bSession   :: Session
  , bConfirmed :: Bool
  , bBookedBy  :: Maybe Course     -- set iff confirmed
  , bCancelled :: Bool
  , bReason    :: Maybe String     -- set iff cancelled
  }
```

**Count the states.** Ignoring the `Session`, there are 2 × (1 + |Course|) × 2 × (1 + |String|)
combinations, and **almost all of them are nonsense**: confirmed *and* cancelled; confirmed with no
booker; cancelled with a reason *and* `bCancelled = False`. Every function that touches a `Booking`
must now either check these or hope.

The sum type has **exactly three** states, all of them meaningful:

```haskell
data Booking = Pending   Session
             | Confirmed Session Course
             | Cancelled Session String
```

**The `Maybe`s are gone**, because the field's presence is now carried by *which constructor it is*,
and so is every `Bool` that existed to say which case you were in. `-Wall` will also now tell you
whenever you forget one of the three.

> **The test for whether you have this right:** can you write down a value of your type that a code
> reviewer would call impossible? If yes, the type is too big. `bConfirmed = True, bCancelled = True`
> is that value, and it is unwriteable in the second version.

### Where the types stop: `mkSession`

L03 §4 measured that the redesigned `Session` leaves exactly one wrong field ordering acceptable —
`start` and `end` swapped, because both are `Minutes`. **A type cannot close that**, short of a
`newtype` per field that nobody sustains.

So close it with a **smart constructor**: one function that is the only way to build the value, which
checks what the type cannot.

```haskell
mkSession :: Course -> Kind -> Day -> Minutes -> Minutes -> Either String Session
mkSession c k d s e
  | s >= e    = Left (show c ++ " " ++ show k ++ " " ++ show d ++
                      ": starts at " ++ show s ++ " and ends at " ++ show e)
  | otherwise = Right (Session c k d s e)
```

**Two things make this work, and neither is the `if`.**

The first is that its **type forces the caller to deal with failure** — you cannot get a `Session` out
of an `Either String Session` without handling the `Left`. The second is the discipline that makes it
airtight: **export `mkSession` and not the `Session` constructor**, so that within a module you build
sessions one way and outside it there is no other way. That is a one-line change to the module header:

```haskell
module Sched (Session, mkSession, course, kind, day, start, end, …) where
```

`Session` without `(..)` exports the *type* and not its constructor. Lab 1 §4 does this and then
tries to break it from another module.

**The hierarchy this week has built, in order of what each tool can promise:**

| Tool | Catches | When |
|---|---|---|
| a distinct **type** per field | passing the wrong *kind* of thing | compile time, always |
| a **sum type** instead of flags | impossible *combinations* of fields | compile time, always |
| **`-Wall` exhaustiveness** | a case you forgot | compile time, if the type is finite |
| a **smart constructor** | bad *values* of individually-fine types | run time, once, at the boundary |
| a **module boundary** | someone bypassing the smart constructor | compile time, always |

**Only the last row makes the fourth row trustworthy**, and that is the part people leave out.

---

## 4. Recursive Types, and the One You Will Build for Six Weeks

A data type may mention itself:

```haskell
data Expr = Lit Int
          | Add Expr Expr
          | Mul Expr Expr
          | Neg Expr
  deriving (Show, Eq)
```

**That is an abstract syntax tree**, the thing CS 211 spent a term producing from source text, and here
it is in five lines. `Add (Lit 2) (Mul (Lit 3) (Lit 4))` is `2 + 3 * 4`.

And the evaluator is one equation per constructor:

```haskell
eval :: Expr -> Int
eval (Lit n)   = n
eval (Add a b) = eval a + eval b
eval (Mul a b) = eval a * eval b
eval (Neg a)   = negate (eval a)
```

**Four lines, total, exhaustive, and `-Wall` will tell you if you add a constructor and forget to
handle it.** Compare the visitor pattern you would write for the same tree in Java.

> **This is Project 1.** The interpreter due in Week 7 is this type with variables, functions and
> `let` added, an `Either` for errors (Week 6) and a `State` for the environment (Week 5). Every week
> from here adds one constructor and one equation. **`Expr` and `eval` above are not a toy example;
> they are the first commit.**

**The list is a recursive type too**, and nothing more:

```haskell
data [] a = [] | a : [a]          -- roughly; the real one is built into the syntax
```

`[]` and `(:)` being constructors is why `(x:xs)` is a pattern and not a function call, and why every
list function in Week 2 has exactly two equations.

---

## 5. What to Take Away

1. **Constructors build and take apart.** A pattern is a constructor used backwards, and patterns
   nest as deep as the data does.
2. **Patterns ask about shape; guards ask about values.** `|` in an equation is "such that";
   `otherwise` is a library function, not a keyword.
3. **Equations and `case … of` are one mechanism**, differing only in where you can write them.
4. **Exhaustiveness checking is only useful on a finite type.** Measured: for `Kind`, GHC names the
   missing case — `SEM`. For `String` it emits four clauses about individual characters and **gives up
   with an ellipsis**. That is the argument for sum types.
5. **`-Wall` catches the incomplete `case` *and* the incomplete `let Just x = …`** — both, on this
   GHC. It catches **neither** a partial record selector nor `head []`, which compile silently and
   crash. **Return a `Maybe` rather than calling `head`.**
6. **Make bad states unrepresentable.** Three constructors beat two `Bool`s and two `Maybe`s, and the
   test is whether you can write down a value a reviewer would call impossible.
7. **A smart constructor catches what a type cannot** — and is only trustworthy if the module exports
   it *instead of* the real constructor.
8. **A recursive type is an AST**, and `eval` is one equation per constructor. That is Project 1's
   first commit.

---

## Exercises

*(Not assessed. PS 1 is the assessed work.)*

1. Add a `Div Expr Expr` constructor to `Expr` and compile `eval` without changing it. Which warning
   fires, and what is its exact wording? Then handle it — and notice that division can fail, which is
   Week 6's problem and not this week's.
2. Write `depth :: Expr -> Int`. Then write `countLits :: Expr -> Int`. They have the same shape;
   remember that you noticed, because Week 2 §5 is about it.
3. Take the bad `Booking` record from §3 and write `isValid :: Booking -> Bool` that rejects every
   nonsensical combination. Count the clauses. That count is what the sum type saves you.
4. `firstLecture` in §1 has three equations. Rewrite it with `case … of` and a helper, and say which
   version you would rather review.
5. Try to build a `Session` with `start` after `end` **through `mkSession`**, then **around it** by
   using the `Session` constructor directly. Then hide the constructor with an export list and try
   again from a second module.

---

*PROG 202 · Week 1 · L04 · © CSE Department*
