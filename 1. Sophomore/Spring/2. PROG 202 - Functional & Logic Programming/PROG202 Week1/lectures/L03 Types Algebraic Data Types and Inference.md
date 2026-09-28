# PROG 202 · Functional & Logic Programming
## Week 1 · Lecture 1 of 2
### Types as Sets, Algebraic Data Types, and Why the Compiler Knows the Type You Did Not Write

*“A type system is a tractable syntactic method for proving the absence of certain program behaviors by classifying phrases according to the kinds of values they compute.”* — Benjamin C. Pierce, *Types and Programming Languages* (2002), §1.1

---

**Sat:** Tuesday of Week 1, 11:00–12:15, TH 205 · **⚠️ Quiz 1 in the first ten minutes** — covers Week 0 · **Reading:** Hutton §3, §8.1–8.4 · **Next:** L04, pattern matching and unrepresentable states

**Coursework:** 📊 **Quiz 1** today · 📝 **PS 1** released Wed this week, due Fri of Week 2 17:00 · 📝 **PS 0** due Fri this week 17:00

---

## 1. A Type Is a Set of Values, and the Set Size Is the Point

`Bool` has two values. `()` has one. `Char` has 1,114,112. `Integer` has infinitely many, and `Int` has exactly 2⁶⁴.

**Counting is not a curiosity; it is the design tool this whole week is about.** A type with fewer
values is a type in which fewer things can go wrong, and the number is often easy to work out:

| Type | Values | Why |
|---|---:|---|
| `()` | 1 | the unit type |
| `Bool` | 2 | `False`, `True` |
| `(Bool, Bool)` | **4** | 2 × 2 — a *product* |
| `Either Bool Bool` | **4** | 2 + 2 — a *sum* |
| `Maybe Bool` | **3** | 1 + 2 — `Nothing`, `Just False`, `Just True` |
| `Bool -> Bool` | **4** | 2² — one choice of result per argument |
| `Maybe (Bool, Bool)` | 5 | 1 + (2 × 2) |

**The arithmetic is not an analogy.** `(a, b)` has `|a| × |b|` values and `Either a b` has
`|a| + |b|`, which is exactly why Haskell calls them *algebraic* data types, and why `a -> b` has
`|b|^|a|`. Week 12 comes back to this and gives it its other name.

> **`Bool -> Bool` has four values, and you can name all four:** `id`, `not`, `const True`,
> `const False`. There is no fifth. Lab 1 asks you to write them down and then asks how many values
> `Bool -> Bool -> Bool` has. *(Sixteen.)*

---

## 2. `data` — Sums and Products, and Nothing Is Built In

```haskell
data Bool = False | True                     -- a sum of two things with no fields
data Day  = Mon | Tue | Wed | Thu | Fri      -- a sum of five
```

The `|` is read **"or"**. Each alternative is a **constructor**: a value, or a function that makes
one. `Mon` *is* a `Day`; there are no others.

```haskell
data Session = Session Course Kind Day Minutes Minutes     -- one constructor, five fields
```

Here `Session` is a *product*: one alternative carrying five things at once. The name `Session`
appears twice and means two different things — **on the left it is the type, on the right it is the
constructor** — and Haskell keeps type names and value names in separate namespaces precisely so this
reads naturally. They need not match; `data Session = MkSession …` is equally legal and sometimes
clearer.

**And you can have both at once**, which is where the power is:

```haskell
data Booking
  = Confirmed Session Course        -- a Session, booked by a Course
  | Pending   Session               -- requested, not yet approved
  | Cancelled Session String        -- and why
```

A `Booking` is *one of three shapes*, and each shape carries different fields. **There is no
arrangement of `Booking` that has a cancellation reason and is confirmed**, because the type does not
provide one. That sentence is the whole of L04.

### Records give the fields names

```haskell
data Session = Session
  { course :: Course
  , kind   :: Kind
  , day    :: Day
  , start  :: Minutes
  , end    :: Minutes
  } deriving (Eq, Show)
```

This defines the same type *and* five accessor functions — `course :: Session -> Course` and so on —
and lets you construct by name, in any order:

```haskell
Session { day = Tue, kind = LEC, course = Course "PROG 202", start = hm 11 0, end = hm 12 15 }
```

**Two things to know before you rely on it.** Record *update* syntax, `s { day = Wed }`, builds a new
`Session` differing in one field and is the closest Haskell comes to assignment — it is not one; `s`
is unchanged.

**And a record accessor is a partial function when the type has several constructors.** If only one
of three constructors carries a `why` field, `why` crashes on the other two:

```
$ ghc -Wall -O0 -o rec rec2.hs && ./rec
rec2: No match in record selector why
```

**`-Wall` does not warn about this on GHC 9.4.7.** There is no `-Wincomplete-record-selectors` here —
passing it gets you `unrecognised warning flag` — so **this is one hole in the type system's fence that
the compiler on these machines will not point at.** Do not spread one record's fields across a sum;
give each constructor its own fields and pattern-match, which is L04.

### `type`, `newtype`, `data` — three different things

| Keyword | What it makes | Runtime cost | Can you confuse it with the original? |
|---|---|---|---|
| `type Session = (…)` | **a synonym.** No new type at all | none | **Yes** — it *is* the tuple |
| `newtype Minutes = Minutes Int` | **a new type**, one constructor, one field | **none** — erased at compile time | **No** |
| `data Minutes = Minutes Int` | a new type, one constructor, one field | a heap box | No |

**`type` is the one Week 0 used, and it bought nothing.** `type Session = (String, String, String,
Int, Int)` is *documentation with a keyword in front of it*: every tuple of that shape is a `Session`
and every `Session` is that tuple, so nothing is checked. §4 measures exactly what that cost.

**Prefer `newtype` to `data` for a single wrapped field.** It is free: GHC erases it, so a
`[Minutes]` has the identical machine representation to an `[Int]`.

---

## 3. `Maybe` and `Either` Are Ordinary Data Types

```haskell
data Maybe a    = Nothing | Just a
data Either a b = Left a  | Right b
```

**That is the complete definition of each**, and everything else about them is library functions over
those constructors. Both are polymorphic — the lower-case `a` is a *type variable*, and `Maybe` is
not a type until you give it one. `Maybe Int` is a type; `Maybe` alone is a **type constructor**, and
Week 4 is about what you can say about those.

**`Maybe` is how a Haskell function says "possibly no answer".**

```haskell
lookup :: Eq a => a -> [(a, b)] -> Maybe b
```

There is no null. There is no sentinel. There is no exception in the ordinary case. The *type* says
the answer may be absent, so **every caller is forced by the compiler to say what it does then** —
which is the entire content of what Hoare later called his billion-dollar mistake, undone by three
words of a data declaration.

**`Either` is `Maybe` that also carries a reason.** The convention — `Left` for failure, `Right` for
success, "right is right" — is a convention and nothing in the type enforces it, but every library
follows it and Week 6 depends on it.

```haskell
mkSession :: Course -> Kind -> Day -> Minutes -> Minutes -> Either String Session
```

This is the constructor Lab 1 writes, and its type is a promise: **you cannot get a `Session` out of
it without handling the case where it refuses.**

---

## 4. What Week 0's Tuple Actually Cost: 120 Files, Compiled

Week 0's `Session` was `(String, String, String, Int, Int)`. Three strings in a row, then two `Int`s.
**How bad is that?** It is measurable, so measure it.

`resources/orderings.py` generates all **120** permutations of the five field values, writes each as a
one-line Haskell file, and compiles every one with `ghc -fno-code`:

```
$ python3 orderings.py
orderings tried      : 120
accepted by the type : 12
intended order       : True
wrong but accepted   : 11
```

**Twelve of the 120 orderings type-check.** One is right. **Eleven are wrong and the compiler accepts
them**, because any permutation that leaves the three `String`s among themselves and the two `Int`s
among themselves is indistinguishable to a type synonym: 3! × 2! = 12.

Now the same experiment on two redesigns:

| `Session` is… | accepted of 120 | **wrong but accepted** |
|---|---:|---:|
| `type Session = (String, String, String, Int, Int)` | 12 | **11** |
| a record with `Day`/`Kind` as sums and `Course`/`Minutes` as newtypes | 2 | **1** |
| a record with a distinct `newtype` per field | 1 | **0** |

**Read the middle row, not the last one.** The last row is achievable and nobody writes it — five
newtypes for five fields is a tax you will stop paying by Thursday. The middle row is **the design a
working Haskell programmer actually produces**, and it leaves *exactly one* hole:

```
wrong but accepted : 1 -> [(0, 1, 2, 4, 3)]
```

That permutation is **`start` and `end` swapped** — the only pair still sharing a type, because both
are `Minutes`.

**So: types took eleven bugs down to one, and the one that is left is not a type error.** A session
that ends before it begins is a *value* problem, and §3's `mkSession` is where it is caught. **Knowing
which hole each tool closes is the skill this week is actually teaching.**

> **Why `Day` and `Kind` as sums rather than newtypes over `String`.** Two reasons, and the second is
> bigger. A `newtype Day = Day String` stops you passing a `Course` where a `Day` goes, but it does
> not stop `Day "Tuesady"`. A **sum type has five values and typos are not among them.** And because
> the set is finite and known, the compiler can check that you handled all of it — which is L04.

---

## 5. Type Inference: the Compiler Already Knows

You have been writing signatures since Week 0 and GHC has not needed any of them.

```haskell
pairUp x y = (y, x)
```

```
ghci> :t pairUp
pairUp :: b -> a -> (a, b)
```

**Nothing was declared and the answer is exactly right** — and it is more general than most people
would have written by hand. The algorithm is **Hindley–Milner**, it is the thing CS 211 Week 3
described, and it is three ideas:

1. **Give every unknown a fresh type variable.** `x` gets one, `y` gets another.
2. **Walk the expression, collecting equations** that the variables must satisfy. `(y, x)` forces the
   result to be the pair of them, in that order. A use of `x + 1` would add a `Num` constraint on
   `x`'s variable; `length x` would force it to be `Foldable f => f a`.
3. **Solve the equations by unification** — repeatedly substitute until either everything is
   consistent or two constructors clash, which is your type error.

**And the type it finds is *principal*: the most general one that works.** That is the theorem, and it
is why inference is trustworthy rather than merely convenient. If GHC infers `t1 -> t2 -> (t2, t1)`,
no more general type exists, and every more specific one you might have wanted is an instance of it.

### So why write signatures at all?

Three reasons, in increasing order of how much they will matter to you this term.

**One: they are the documentation that cannot rot.** A comment saying what a function takes can be
wrong. A signature cannot be.

**Two: they let you be *less* general on purpose.** `sumInts :: [Int] -> Int` is narrower than the
inferred `Num a => [a] -> a`, and narrowing is often what you want — it pins down the numeric type so
nothing downstream has to.

**Three, and this is the one with evidence: a signature is a firewall.**

Take Week 0's `Shape.hs` and make one mistake — `fst` where `snd` was meant. **With** the signature
on `busiest`:

```
Shape.hs:19:35: error:
    • Couldn't match type ‘Int’ with ‘[Char]’
   |
19 | busiest = fst . last . sort . map swap
```

Line 19. The line with the mistake. Now **delete the signature** and compile the identical mistake:

```
Shape.hs:23:29: error:
    • No instance for (Num String) arising from the literal ‘150’
   |
23 |   where table = [("CS 202", 150), ("PROG 202", 260), ("CS 290", 50)]
   |                             ^^^
```

**GHC blames the number 150**, four lines away, inside a different function, in data that is entirely
correct.

Nothing is broken here. Inference is *global*: with no signature to stop it, the wrong type
propagated out of `busiest`, through `main`, into the table, and the first thing that could not be
reconciled was an innocent literal. **The line an error is reported on is where the contradiction
became unavoidable, not where the mistake was made.**

> **Do not over-learn this.** Inference is usually *better* than that example suggests. Put the
> mistake somewhere whose wrong type contradicts something in the same function — `total xs / length
> xs` where `div` was meant — and GHC lands on the exact character with or without a signature.
> The bad case needs a wrong type that is **self-consistent within the function** and only disagrees
> with the outside world. **Signatures cost you one line and bound the blast radius to one
> definition.** Write one on every top-level binding; `-Wall` asks you to anyway.

---

## 6. `deriving` — Four Instances for Free

```haskell
data Day = Mon | Tue | Wed | Thu | Fri
  deriving (Show, Eq, Ord, Enum, Bounded)
```

| Derived | Gives you | Watch out |
|---|---|---|
| `Show` | `show Tue == "Tue"` | It is for *programmers*. A `Show` instance that produces prose is a mistake |
| `Eq` | `==`, `/=` | Structural equality, field by field |
| `Ord` | `<`, `compare`, `sort` | **Ordered by declaration order.** `Mon < Tue` because you wrote `Mon` first |
| `Enum` | `[Mon ..]`, `succ` | `[Mon .. Fri]` is the whole week |
| `Bounded` | `minBound`, `maxBound` | `[minBound .. maxBound] :: [Day]` — **every `Day`, with no list to maintain** |

**That last row is worth the price of the lecture.** Lab 1 iterates over the week as
`[minBound .. maxBound]`, and when someone adds `Sat`, every loop over the week picks it up and no
list anywhere needs editing. Week 0's `weekdays = ["Mon","Tue","Wed","Thu","Fri"]` was a list that
could disagree with the data, and now there is nothing to disagree with.

**`Ord` from declaration order is a real trap.** It is what you want for `Day`; it is not what you
want for a `Priority` you listed alphabetically. If the ordering matters, write the instance.

---

## 7. What to Take Away

1. **A type is a set of values**, and the arithmetic is literal: products multiply, sums add,
   functions exponentiate.
2. **`data` gives sums with `|` and products with several fields**, and both at once. Nothing is built
   in — `Bool` is two lines of library.
3. **`type` checks nothing, `newtype` is a free new type, `data` is a type with a box.** Week 0's
   `type` was documentation wearing a keyword.
4. **`Maybe` and `Either` are ordinary data types**, and `Maybe` is how the absence of a null is
   arranged.
5. **Measured: Week 0's tuple accepted 11 wrong field orderings out of 120; the record with sums and
   newtypes accepts 1.** The one that remains is `start`/`end`, because they share a type, and it is
   a *value* error that a smart constructor catches — not a type error.
6. **Inference finds the principal type**, so it is trustworthy. Write signatures anyway: **a
   signature is a firewall**, and without one GHC blamed the literal `150` for a mistake four lines
   away.
7. **`deriving (Eq, Ord, Enum, Bounded)`**, and `[minBound .. maxBound]` is every value of a finite
   type with no list to maintain.

---

## Exercises

*(Not assessed. PS 1 is the assessed work.)*

1. Count the values of: `Maybe (Maybe Bool)`, `Either () Bool`, `(Bool, ())`, `Bool -> ()`,
   `() -> Bool`. Two of those five are the same size and it is not the obvious pair.
2. Write out all four values of `Bool -> Bool` as Haskell expressions. Then say how many values
   `Maybe Bool -> Bool` has, and check by counting.
3. `data Foo = Foo Int | Bar` — what does `:t Foo` say, and what does `:t Bar` say? Why are they
   different kinds of thing when both are constructors?
4. Define `newtype Celsius = Celsius Double` and `newtype Fahrenheit = Fahrenheit Double`, and a
   conversion between them. Then try to add a `Celsius` to a `Fahrenheit` and read the error.
5. Run `resources/orderings.py`. Then edit it so that `Kind` is a `newtype` over `String` rather than
   a sum. Predict the count before you run it, and say which bug the change leaves open.
6. Write a two-constructor record where only one constructor has a `why` field, apply the `why`
   selector to the other, and compile it with `-Wall`. **Report what GHC says at compile time and
   what the program says at run time.** Then find the warning flag that would have caught it and
   check whether this GHC has it.

---

*PROG 202 · Week 1 · L03 · © CSE Department*
