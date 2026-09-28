# PROG 202 · Functional & Logic Programming
## Week 4 · Lecture 2 of 2
### `Functor`, `Foldable`, and Laws the Compiler Does Not Check

*“Simplicity does not precede complexity, but follows it.”* — Alan Perlis, "Epigrams on Programming" (1982), #31

---

**Sat:** Thursday of Week 4, 11:00–12:15, TH 205 · **Reading:** Hutton §12.1, §14.1–14.4 · **Next:** Week 5 L11, monads

**Coursework:** 📝 **PS 3** due Fri this week 17:00 · 📊 **Quiz 5** Tue of Week 5 · 📝 **PS 5** released Wed of Week 5, due Fri of Week 6 17:00 · 🔬 **Lab 4** Wed of Week 5 13:00–14:50

---

## 1. `fmap` — the Pattern Behind `map`

You have written this shape a dozen times:

```haskell
map      :: (a -> b) -> [a]       -> [b]
mapMaybe :: (a -> b) -> Maybe a   -> Maybe b      -- if you wrote it
mapTree  :: (a -> b) -> Tree a    -> Tree b       -- L04's Expr, nearly
```

**One argument changes and the container does not.** So make the container the class parameter:

```haskell
class Functor f where
  fmap :: (a -> b) -> f a -> f b
```

**Note what kind of thing `f` is.** In `Eq a`, `a` was a type — `Int`, `Day`. In `Functor f`, `f` is a
**type constructor**: `Maybe`, `[]`, `Either String`. `Maybe Int` is a type; `Maybe` is a function from
types to types, and it is `Maybe` that is the `Functor`.

```
ghci> fmap (*2) (Just 3)
Just 6
ghci> fmap (*2) [1,2,3]
[2,4,6]
ghci> fmap (*2) (Right 5 :: Either String Int)
Right 10
ghci> fmap (*2) (Left "boom" :: Either String Int)
Left "boom"
```

**`<$>` is `fmap` infix**, and you will read it far more often than you read `fmap`:

```haskell
(+1) <$> Just 2          -- Just 3
show <$> [1,2,3]         -- ["1","2","3"]
```

**Perlis's epigram at the top is the point of this lecture.** Nobody invents `Functor` first. You write
`map`, then `mapMaybe`, then `mapTree`, and only then is the simple thing visible — and it was not
available before you had written the complicated things.

---

## 2. The Laws, and the Fact That GHC Does Not Check Them

`Functor` requires two:

```
fmap id      == id                    -- identity
fmap (f . g) == fmap f . fmap g        -- composition
```

**GHC checks neither.** This compiles:

```haskell
data Pair a = Pair a a
instance Functor Pair where
  fmap f (Pair x y) = Pair (f y) (f x)      -- swaps.  Accepted.
```

`fmap id (Pair 1 2)` is `Pair 2 1`, which is not `Pair 1 2`. **The instance is legal Haskell and wrong**,
and everything built on top of it — every library function that assumes the law — is now quietly broken.

**This is the strongest argument this course can make for Week 11.** The contract of an instance is a
set of *laws*, laws are statements about all inputs, and a test that checks one example cannot check a
law. **Property-based testing exists for exactly this** and Week 11's tester takes `fmap id == id` as its
first example.

> **Wadler's quote at the top of L09 is the other half.** For a *parametrically* polymorphic function
> the type alone forces the law: `fmap`'s type says nothing about `a`, so an implementation cannot
> inspect the elements, and the only things it can do are rearrange the structure. **`Pair`'s bad
> instance is exactly a rearrangement**, which is why the type could not rule it out and the law has to.

### The laws people actually rely on

| Class | Law | What breaks if you violate it |
|---|---|---|
| `Eq` | `==` is reflexive, symmetric, transitive | `nub`, `lookup`, `Data.Map` keys |
| `Ord` | a total order, consistent with `Eq` | **`Data.Map` and `Data.Set` corrupt silently** — the tree's invariant is the order |
| `Functor` | the two above | any generic code over `f` |
| `Semigroup` | `<>` associative | `mconcat`, and any parallel reduction |
| `Monoid` | `mempty` an identity | `foldMap` on an empty container |

**The `Ord` row is the one with teeth.** A `Data.Map` built with an inconsistent `compare` does not throw
— it *loses* keys, because the lookup walks a tree whose shape assumed something false. That is the cost
of laws the compiler does not check, and it is the reason `Ord` is usually derived.

---

## 3. `Foldable` — Four Weeks of `Foldable t =>` Explained

Since Week 0, `:t length` has said `Foldable t => t a -> Int`, and Week 2 asked you to ignore it.

```haskell
class Foldable t where
  foldr   :: (a -> b -> b) -> b -> t a -> b
  foldMap :: Monoid m => (a -> m) -> t a -> m
  -- and about twenty more, all with defaults
```

**Either method alone is enough** — everything else has a default written in terms of it. So making a
container foldable is one function, and in exchange you get `length`, `sum`, `product`, `maximum`, `elem`,
`null`, `toList`, `any`, `all`, `concatMap`, `traverse_` and the rest.

```haskell
data Tree a = Leaf | Node (Tree a) a (Tree a)

instance Foldable Tree where
  foldr _ z Leaf         = z
  foldr f z (Node l x r) = foldr f (f x (foldr f z r)) l
```

**That is the whole instance, and `sum`, `length`, `maximum` and `elem` on a `Tree` now exist.** Lab 4
writes it.

### And now the surprises, all measured

```
ghci> length (Just 3)                  1
ghci> length Nothing                   0
ghci> length ('x', 5)                  1
ghci> sum ('x', 5)                     5
ghci> maximum ("hello", 3)             3
ghci> length (Right 5)                 1
ghci> length (Left "boom")             0
ghci> null (Just undefined)            False
ghci> fmap (*2) ('x', 5)               ('x',10)
```

**A tuple is `Foldable` in its second component only, and a `Maybe` is a container of zero or one.**
Those are consistent, defensible, and a menace:

- `length someTuple` is **always 1** and compiles silently.
- `maximum ("hello", 3)` **ignores the string**, because `(,) a` is the functor and `a` is not an element.
- `sum` over a `Maybe` treats `Nothing` as 0, which is sometimes what you want and never obviously so.

**`null (Just undefined)` being `False` is the pleasant one** — `null` asks about structure, not contents,
so it never forces the element. That is Week 3's WHNF being useful rather than expensive.

> **This is a real and ongoing argument in the Haskell community, not a curiosity.** Generalising
> `length` from `[a] -> Int` to `Foldable t => t a -> Int` made a whole family of type errors into
> silently-wrong programs, and the standard library did it anyway because the generality is worth more.
> **You should know the trap and you should also know why the trade was made.** PS 4 asks you to argue
> it, and there is no expected answer.

### `foldMap`, which is the interesting method

```haskell
foldMap :: Monoid m => (a -> m) -> t a -> m
```

**Map every element into a monoid and combine.** Given L09 §4's `Stats` monoid:

```haskell
foldMap statsOf ts        -- one traversal, all the statistics
```

and because `<>` is associative *by law*, **the combining can happen in any order** — which is how a
parallel reduction over a tree is possible at all, and it is Week 7's first example.

---

## 4. `Traversable`, and Lab 1's `traverse id`

In Lab 1 you wrote `traverse id` and were told it was Week 6. It is `Traversable`, and it is the third
class in this family:

```haskell
class (Functor t, Foldable t) => Traversable t where
  traverse :: Applicative f => (a -> f b) -> t a -> f (t b)
```

**Read the type slowly and it is exactly what Lab 1 needed.** With `t = []` and `f = Either String`:

```haskell
traverse :: (a -> Either String b) -> [a] -> Either String [b]
```

*"Apply a function that might fail to every element, and give me either all the results or the first
failure."* And `traverse id` is that with the function already applied — a list of `Either`s becoming an
`Either` of a list.

**`Applicative` is Week 6** and until then this is the honest summary: `Traversable` is `Functor` plus
`Foldable` plus the ability to do it *effectfully*, and the three classes together are why
`Data.Traversable` has sixteen functions and you have to write one.

---

## 5. When Not to Generalise

The lecture has been an argument for abstraction, so here is the other side, because it is examinable.

**Three costs, all real:**

1. **Error messages get worse.** A mistake in a `Foldable t =>` function reports a missing instance for
   an inferred `t` rather than "you gave a `Maybe` where a list goes". You have already met this in
   L03 §5 without the constraints; add classes and it compounds.
2. **`length someTuple == 1`.** Generalisation turns type errors into wrong answers, and §3 is the
   list.
3. **It costs a dictionary** unless GHC specialises — measured in L09 §2 at 30%, and **40× if you also
   block inlining**, which is what `NOINLINE` in that experiment was simulating.

**The rule this course asks for:**

> **Generalise when you have written the specific version at least twice and the laws hold.** Not
> before — Perlis's epigram is about the order — and not when you cannot say what the laws are. An
> instance without laws is a name for a coincidence.

---

## 6. What to Take Away

1. **`Functor f` has a type *constructor* as its parameter**, not a type. `Maybe` is the functor, not
   `Maybe Int`.
2. **`<$>` is `fmap` infix**, and you will read it more often than `fmap`.
3. **`Functor` has two laws and GHC checks neither.** A swapping `Pair` instance compiles and breaks
   `fmap id == id`. **That is what Week 11 is for.**
4. **Violating `Ord`'s laws corrupts `Data.Map` silently** rather than throwing. Derive `Ord` unless you
   have a reason.
5. **`Foldable` needs one method** — `foldr` or `foldMap` — and gives you twenty, which is why
   `Foldable t =>` has been in every `:t` since Week 0.
6. **`length (Just 3) == 1`, `length ('x', 5) == 1`, `maximum ("hello", 3) == 3`.** Consistent,
   defensible, and a menace, and the trade was made deliberately.
7. **`foldMap` needs `<>` to be associative by law**, which is what makes a parallel reduction legal —
   Week 7.
8. **`traverse` is Lab 1's `traverse id`**, and it is `Functor` + `Foldable` + effects.
9. **Generalise after writing the specific version twice, and only when you can state the laws.**

---

## Exercises

*(Not assessed. PS 4 is the assessed work.)*

1. Write `instance Functor Tree` for `data Tree a = Leaf | Node (Tree a) a (Tree a)`, then check both laws
   on a three-node tree by hand.
2. Write the swapping `Functor Pair` from §2, compile it with `-Wall`, and confirm GHC accepts it. Then
   find a *library* function whose behaviour it breaks.
3. Predict, then check: `length (Just [1,2,3])`, `sum (Just 4)`, `concat (Just [1,2])`,
   `maximum (Left "x" :: Either String Int)`. One of the four throws; say which and why.
4. Write `instance Foldable Tree` with **`foldMap`** rather than `foldr`, and check that `sum`, `length`
   and `toList` all work. Which of the two methods was easier, and which would you write in a library?
5. `foldMap Sum [1,2,3]` and `foldMap Product [1,2,3]`. Why are `Sum` and `Product` `newtype`s rather
   than two `Monoid Int` instances? *(L09 §5.)*

---

*PROG 202 · Week 4 · L10 · © CSE Department*
