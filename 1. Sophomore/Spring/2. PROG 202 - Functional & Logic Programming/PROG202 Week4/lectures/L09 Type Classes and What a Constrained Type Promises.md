# PROG 202 · Functional & Logic Programming
## Week 4 · Lecture 1 of 2
### Type Classes: One Function Written Once for Every Type at Once

*“From the type of a polymorphic function we can derive a theorem that it satisfies. Every function of the same type satisfies the same theorem.”* — Philip Wadler, "Theorems for free!" (1989), abstract

---

**Sat:** Tuesday of Week 4, 11:00–12:15, TH 205 · **⚠️ Quiz 4 in the first ten minutes** — covers Week 3 · **Reading:** Hutton §3.7–3.9, §8.5 · **Next:** L10, `Functor` and `Foldable`

**Coursework:** 📊 **Quiz 4** today · 📋 **Project 1** released Wed this week, due Fri of Week 7 17:00 · 📝 **PS 4** released Wed this week, due Fri of Week 5 17:00 · 🔬 **Lab 3** Wed this week 13:00–14:50 · 📝 **PS 3** due Fri this week 17:00

---

## 1. The Question Left Open in Week 0

```
ghci> :t 3
3 :: Num a => a
ghci> :t length
length :: Foldable t => t a -> Int
ghci> :t (==)
(==) :: Eq a => a -> a -> Bool
```

**Four weeks of `=>` and no explanation.** This is the lecture.

A **type class** is a set of types that support a named set of operations. `Eq` is the types you can
compare for equality; `Ord` the types you can order; `Show` the types you can print. A **constraint** —
everything left of `=>` — is a *requirement on the caller* that the type it chooses be in that set.

```haskell
class Eq a where
  (==) :: a -> a -> Bool
  (/=) :: a -> a -> Bool
  x /= y = not (x == y)          -- a default: you get this free
  x == y = not (x /= y)          -- and this
```

**That is the whole declaration of `Eq`**, and it is in a library. Three things in it are worth naming:

- `class Eq a where` introduces a **class** with one type parameter, `a`.
- The two signatures are the class's **methods** — functions whose implementation depends on the type.
- The two equations are **default methods.** An instance may define either one and get the other.

```haskell
instance Eq Day where
  Mon == Mon = True
  Tue == Tue = True
  …
  _   == _   = False
```

`instance` says *this type is in the class, and here is how.* You have been getting these from
`deriving` since Week 1; this week you write them.

---

## 2. What Really Happens: Dictionaries

`elem :: Eq a => a -> [a] -> Bool` compiles to a function of **three** arguments. The extra one is a
**dictionary**: a record of the class's methods for the chosen type.

```
elem :: Eq a => a -> [a] -> Bool

    becomes, roughly

elem :: EqDict a -> a -> [a] -> Bool
    where data EqDict a = EqDict { eq :: a -> a -> Bool, neq :: a -> a -> Bool }
```

**Every call site supplies the dictionary**, because every call site knows the type. That is why the
constraint is a caller's obligation and not a parameter you pass: the *compiler* passes it.

> **This makes the `=>`-is-not-an-argument rule exact.** `elem` takes two arguments in the source and
> three in the generated code, and the third is chosen by the compiler from the type. If you have been
> reading `Eq a =>` as an argument, you were right about the machine and wrong about the language.

### And it costs something, measured

`resources/spec.hs` is one polymorphic function compiled twice — the second time with a pragma telling
GHC to emit a dedicated `Int` version:

```haskell
sumPoly :: Num a => [a] -> a
sumPoly = foldl' (+) 0
{-# NOINLINE sumPoly #-}
{-# SPECIALISE sumPoly :: [Int] -> Int #-}   -- present in one build, absent in the other
```

*n* = 200,000,000, `-O2`, three runs each:

| | times |
|---|---|
| as written — dictionary passed, `(+)` called through it | **3.18 s, 2.97 s, 2.76 s** |
| with `{-# SPECIALISE #-}` | **2.23 s, 2.26 s, 2.18 s** |

**About 30% faster, from one pragma, with the rest of the source identical.**

**Three things to take from that number.**

1. **The cost is real.** A dictionary call is an indirect jump, and it blocks the inlining and unboxing
   that would otherwise turn `(+)` into one machine instruction.
2. **The cost is usually not paid**, because at `-O2` GHC specialises automatically whenever it can see
   both the polymorphic function and the concrete call. `NOINLINE` in the measurement above is there
   precisely to stop it, which is the only reason there is anything to measure.
3. **`SPECIALISE` is the escape hatch** for when it cannot — across a module boundary, most often. It is
   the one pragma in this course worth knowing by name, and Week 7 needs it again.

---

## 3. The Standard Classes, and What Each Promises

**A class is a promise about what you may do, and — via Wadler's quote at the top — about what a
function *cannot* do.**

| Class | Methods you get | What it promises | Derivable? |
|---|---|---|---|
| `Eq` | `==`, `/=` | equality. Nothing about order | ✔ |
| `Ord` | `compare`, `<`, `max`, … | a **total** order. **Superclass `Eq`** | ✔ |
| `Show` | `show`, `showsPrec` | a `String` for *programmers* | ✔ |
| `Read` | `read`, `readsPrec` | parse back from that `String` | ✔ |
| `Enum` | `succ`, `[x ..]` | successor and ranges | ✔ |
| `Bounded` | `minBound`, `maxBound` | **a finite type** | ✔ |
| `Num` | `+`, `*`, `negate`, `fromInteger`, `abs`, `signum` | ring-ish arithmetic and integer literals | ✘ |
| `Semigroup` | `<>` | an associative combine | ✘ |
| `Monoid` | `mempty` | `<>` with an identity. **Superclass `Semigroup`** | ✘ |
| `Functor` | `fmap`, `<$>` | a structure you can map over | ✘ *(but see L10)* |
| `Foldable` | `foldr`, `foldMap`, and 20 more | a structure with elements in some order | ✘ |

### Superclasses

```haskell
class Eq a => Ord a where …
```

**Read `Eq a =>` on a *class* declaration as "you cannot be `Ord` without being `Eq` first".** So a
function with `Ord a =>` may also use `==` for free, and the constraint `(Eq a, Ord a) =>` is redundant
— write `Ord a =>` and `-Wall` will not complain either way, but reviewers will.

### `Num` is the one that explains `:t 3`

**Every integer literal in Haskell is `fromInteger` applied to a literal.** `3` means
`fromInteger (3 :: Integer)`, and `fromInteger :: Num a => Integer -> a` is a method of `Num`. So `3`
works at any type in `Num`, which is exactly what `3 :: Num a => a` says.

**Two consequences you have already met.**

`length xs / 2` fails because `length` gives `Int`, `(/)` needs `Fractional`, and `Int` is not
`Fractional` — a *separate* class for types with division. That is not pedantry: it is the language
refusing to pick between truncating and true division on your behalf, and **C, Java and Python make
three different silent choices there** (PS 0 Q1d).

And **defaulting**: at a GHCi prompt, `3 + 4` has type `Num a => a` with nothing to fix `a`, so the
prompt would be unable to print it. GHC applies the *defaulting rules* and picks `Integer`. **In a
compiled module the same ambiguity is usually an error**, which is why `-Wall`'s `-Wtype-defaults`
exists and why you have seen it.

---

## 4. Writing an Instance

`Sched.hs` has two hand-written `Show` instances already. Here is one with more in it — a `Monoid` for
combining timetable statistics:

```haskell
data Stats = Stats { nSessions :: !Int, nMinutes :: !Int, longest :: !Int }

instance Semigroup Stats where
  a <> b = Stats (nSessions a + nSessions b)
                 (nMinutes  a + nMinutes  b)
                 (max (longest a) (longest b))

instance Monoid Stats where
  mempty = Stats 0 0 0
```

**And now `mconcat`, `foldMap` and every other `Monoid` function work on it**, with no further code.
That is the pay-off and it is why the classes are worth the ceremony.

**But an instance carries obligations the compiler does not check.** `Semigroup` requires `<>` to be
**associative**; `Monoid` requires `mempty` to be an **identity**. GHC will accept an instance that
violates both. **The laws are the contract, and they are enforced by review and by testing** — which is
Week 11, and it is the clearest answer to *why would you test a law rather than an example*.

**Check yours by hand, now:** is `Stats` `<>` associative? Is `Stats 0 0 0` an identity? *(One of the
three fields makes the second question interesting if any duration could be negative — which
`mkSession` prevents, and that is the connection between Week 1 and Week 11 in one sentence.)*

---

## 5. A Type Class Is Not an Interface

Students arriving from Java or C++ map "type class" onto "interface" and then get stuck. The mapping is
close and it fails in four places, each of which matters this term.

| | Java interface | Haskell type class |
|---|---|---|
| Declared where? | **inside the class** that implements it | **anywhere**, including in a module that owns neither the class nor the type |
| Dispatch on | the **receiver** — one value | **any position in the signature**, including the *return* type |
| Retrofit an existing type? | no — you cannot add `implements` to someone else's class | **yes** — `instance Eq TheirType` is legal wherever you can see both |
| How many instances per type? | many interfaces, one implementation each | **exactly one** instance of a class for a type, program-wide |

**The second row is the important one.** `mempty :: Monoid a => a` has the class variable *only in the
return type*, so there is no receiver to dispatch on — the *caller's expected type* chooses the
instance. `read :: Read a => String -> a` is the same, which is why `read "42"` alone is ambiguous and
`read "42" :: Int` is not. **No OO interface can express `mempty`**, and that is the sharpest way to see
that classes are not interfaces.

**The fourth row is called *coherence*** and it is why there is no `instance Monoid Int`: addition and
multiplication are both monoids on `Int`, and the language will not let you have two. The library's
answer is `newtype Sum Int` and `newtype Product Int` — **Week 1's free `newtype`, doing real work.**

> **The cost of coherence is the *orphan instance*.** An instance declared in a module that defines
> neither the class nor the type is legal, and GHC will warn, because two libraries can then define
> incompatible instances and the meaning of your program depends on what you imported. **If you need an
> instance for someone else's type, wrap it in your own `newtype`** — the same answer as `Sum` and
> `Product`.

---

## 6. What to Take Away

1. **A class is a set of types with named operations; a constraint is a requirement on the caller.**
2. **`=>` compiles to a dictionary argument the compiler supplies.** Two arguments in the source, three
   in the code.
3. **Measured: dictionary passing cost 30%** — 2.9 s against 2.2 s — and `-O2` usually removes it by
   specialising. `{-# SPECIALISE #-}` is the escape hatch when it cannot.
4. **`Ord` has `Eq` as a superclass**, so `Ord a =>` gives you `==` free, and `(Eq a, Ord a) =>` is
   redundant.
5. **`Num` explains `:t 3`:** every integer literal is `fromInteger`, so a literal has a constraint and
   not a type. `length xs / 2` fails for a good reason.
6. **Instances carry laws the compiler does not check.** `<>` must be associative; `mempty` must be an
   identity. That is what Week 11 tests.
7. **A class is not an interface**, in four ways — and `mempty :: Monoid a => a`, which dispatches on the
   *return* type, is the one no interface can express.
8. **One instance per type, program-wide.** That is *coherence*, it is why `Sum` and `Product` exist,
   and the price of it is the orphan-instance warning.

---

## Exercises

*(Not assessed. PS 4 is the assessed work.)*

1. `:i Eq`, `:i Ord`, `:i Num`, `:i Monoid`. For each, note the superclass and count the methods. One of
   the four has a method you cannot usefully write for most types; which, and why?
2. Write `instance Eq Session` by hand, so that two sessions are equal when they are the same course on
   the same day at the same time — **ignoring `kind`.** Then say why `deriving Eq` would have been wrong,
   and what breaks if `Ord` is still derived.
3. `mempty` has its class variable only in the return type. Write an expression where GHC cannot work out
   which `mempty` you meant, and then the annotation that fixes it.
4. Define `newtype MaxMinutes = MaxMinutes Int` with a `Semigroup` instance taking the larger. Is it a
   `Monoid`? Find the identity or prove there is none.
5. Build `resources/spec.hs` both ways and reproduce the 30%. Then remove the `NOINLINE` from
   `sumPoly` and measure again. **Explain what happened to the difference.**

---

*PROG 202 · Week 4 · L09 · © CSE Department*
