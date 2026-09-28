# PROG 202 · Functional & Logic Programming
## Week 2 · Lecture 1 of 2
### Higher-Order Functions: What Is Left of a Loop When You Take the Variable Away

*“The ways in which one can divide up the original problem depend directly on the ways in which one can glue solutions together. Therefore, to increase one's ability to modularize a problem conceptually, one must provide new kinds of glue in the programming language.”* — John Hughes, "Why Functional Programming Matters" (1989), §2

---

**Sat:** Tuesday of Week 2, 11:00–12:15, TH 205 · **⚠️ Quiz 2 in the first ten minutes** — covers Week 1 · **Reading:** Hutton §6, §7.1–7.3 · **Next:** L06, the two folds and which to use

**Coursework:** 📊 **Quiz 2** today · 📝 **PS 2** released Wed this week, due Fri of Week 3 17:00 · 🔬 **Lab 1** Wed this week 13:00–14:50 · 📝 **PS 1** due Fri this week 17:00

---

## 1. A Function Is a Value, and That Is the Whole Idea

You have been using this since Week 0 without it being named.

```haskell
map     :: (a -> b) -> [a] -> [b]
filter  :: (a -> Bool) -> [a] -> [a]
sortOn  :: Ord b => (a -> b) -> [a] -> [a]
```

**Each takes a function as its first argument.** That is all "higher-order" means. There is no special
syntax for passing one, no function pointer, no delegate, no `Comparator` interface — a function is a
value and you pass it the way you pass an `Int`.

And functions come *back*, too:

```
ghci> :t (.)
(.) :: (b -> c) -> (a -> b) -> a -> c
ghci> :t map
map :: (a -> b) -> [a] -> [b]
ghci> :t map duration
map duration :: [Session] -> [Int]
```

**`map duration` is a function you did not define.** It is `map` with one of two arguments supplied,
and it has a type and a name and can be passed around. Week 1's `orderings.py` had to compile 120
files; this lecture is about the fact that `map duration` costs nothing to make.

---

## 2. Currying: Why `f x y` Is Not `f(x, y)`

```haskell
add :: Int -> Int -> Int
add x y = x + y
```

**That type is `Int -> (Int -> Int)`.** `->` is right-associative, and it is not a cosmetic detail:
`add` is a function of **one** argument that returns a function of one argument.

```
ghci> :t add 3
add 3 :: Int -> Int
```

So `add 3 4` is `(add 3) 4`: apply `add` to `3`, get a function, apply that to `4`. **Application is
left-associative and types are right-associative**, and those two facts together are currying.

**What it buys is that partial application is free.** Every one of these is a function, made by
supplying some arguments and stopping:

```haskell
map (add 3)          -- add 3 to everything
filter (> 100)       -- keep the big ones
takeWhile (/= Fri)   -- up to Friday
replicate 3          -- three of whatever you give me
```

> **The alternative is worth seeing to appreciate the difference.** In a language where `f(x, y)` is
> primitive, `add3 = partial(add, 3)` needs a library function, a closure object, or a lambda —
> `lambda y: add(3, y)`. In Haskell `add 3` *is already* that, with no machinery, because `add` never
> took two arguments in the first place.

**And the uncurried version exists if you want it:**

```
ghci> :t uncurry add
uncurry add :: (Int, Int) -> Int
ghci> :t curry
curry :: ((a, b) -> c) -> a -> b -> c
```

`uncurry` is how you apply a two-argument function to a pair, which is what you need when `zip` has
handed you pairs. Lab 2 uses it once and it is the only time this term.

---

## 3. `map`, `filter`, and the Loop They Replace

Here is Week 1's `sched` asking three questions. Each is a loop in any other language and none of them
is a loop here.

```haskell
sum (map duration ts)                             -- total contact minutes
filter ((== LEC) . kind) ts                       -- just the lectures
map course (filter ((== Wed) . day) ts)           -- what meets on Wednesday
```

**`map` changes each element and keeps the shape. `filter` keeps the shape's *elements* and changes
the length.** Between them they cover most of what a `for` loop was for, and they say which one you
meant in the first word.

| Loop written as | Means |
|---|---|
| `map f xs` | same length, each element transformed |
| `filter p xs` | same elements, some dropped |
| `takeWhile p xs` | a prefix, stopping at the first failure |
| `zipWith f xs ys` | two lists walked in step |
| `concatMap f xs` | each element becomes *several*, flattened |
| `foldr`/`foldl` | **everything else** — L06 |

**The one to notice is `zipWith`.** `zipWith (*) prices quantities` is the line from Week 0 L01 §1,
and it is the loop with two index variables that nobody writes correctly the first time.

### List comprehensions are `map` and `filter` in different clothing

```haskell
[ course t | t <- ts, day t == Wed ]
map course (filter ((== Wed) . day) ts)
```

**The same computation.** The comprehension is usually more readable when there are two generators or
a nontrivial guard; the combinators are more readable when you want to *name* the transformation or
pass it on. Both compile to the same thing, which you can check with `-ddump-simpl` and will not.

---

## 4. Composition, and the Point-Free Style

```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
(f . g) x = f (g x)
```

**Right to left, as in mathematics.** `(negate . abs) 3` is `-3`.

This is Hughes's "glue" in the quote at the top of this lecture, and it is why Week 1's `busiest` had
no arguments:

```haskell
busiest = snd . last . sort . map swap
```

**Read it right to left:** map, then sort, then take the last, then take the second component. There is
no variable naming the list because the function never needs to mention it — it is a *pipeline*, and
writing it this way is called **point-free** style, "point" being an old word for an argument.

### `$`, and what it is for

```haskell
print (sum (map duration ts))
print $ sum $ map duration ts
```

`$` is function application with the lowest possible precedence, so it **deletes a closing bracket you
would otherwise have to find the match for.** That is its entire purpose.

### When point-free style stops helping

```haskell
-- (a) readable
lectureMinutes ts = sum [ duration t | t <- ts, kind t == LEC ]

-- (b) still readable
lectureMinutes = sum . map duration . filter ((== LEC) . kind)

-- (c) not yet, and arguably not ever -- this is the mean duration, point-free
meanDuration = (/) <$> (fromIntegral . sum . map duration) <*> (fromIntegral . length)
```

**(b) is the target and (c) is the failure mode.** (c) works — it really does give `78.33` for a 50,
a 75 and a 110, and people write it — but you cannot see where the list went, and it went to **both**
branches, which is something `<$>` and `<*>` are doing on your behalf. Note also that the first
`fromIntegral` is not decoration: without it `Int` would have to be `Fractional` and the whole thing
does not compile. That is Week 6, and until then the honest version has a name in it:

```haskell
meanDuration ts = fromIntegral (sum (map duration ts)) / fromIntegral (length ts)
```

The rule this course asks for:

> **Point-free is right when the pipeline reads as a sentence in the order the data flows, and wrong
> when you have to work out where the arguments went.** If you need `flip`, or nested `(.)` sections,
> or the argument has to reach two places at once, you have passed the point. Name it.

**`(== LEC) . kind` deserves one line of explanation** because it is the idiom you will use fifty times
this term: `kind` gets the field out, `(== LEC)` compares it, and `.` glues them into a single
predicate you can hand to `filter`. In an imperative language that is `lambda t: t.kind == LEC`, and
the Haskell version is shorter because both halves already exist.

---

## 5. Two Functions With the Same Shape

L04's exercises had you write these, and asked you to remember that you noticed:

```haskell
depth :: Expr -> Int                    countLits :: Expr -> Int
depth (Lit _)   = 1                     countLits (Lit _)   = 1
depth (Add a b) = 1 + max (depth a) (depth b)
                                        countLits (Add a b) = countLits a + countLits b
depth (Mul a b) = 1 + max (depth a) (depth b)
                                        countLits (Mul a b) = countLits a + countLits b
depth (Neg a)   = 1 + depth a           countLits (Neg a)   = countLits a
```

**Everything except the combining operation is the same.** Both walk the tree; one takes a `max` and
adds one, the other adds. And `eval` from L04 §4 has that shape too, and so does `render`.

**When four functions differ only in an operator, the operator is the argument.** That is the whole
observation behind `foldr`, and L06 makes it precise:

```haskell
foldExpr :: (Int -> r) -> (r -> r -> r) -> (r -> r -> r) -> (r -> r) -> Expr -> r
```

You will write that in Lab 2 and then write `eval`, `depth`, `countLits` and `render` in terms of it,
each in one line. **That is the payoff of this week** and it is also the point at which some people
decide the abstraction costs more than it saves. PS 2 asks you which, and there is no expected answer.

---

## 6. What to Take Away

1. **A function is a value.** Higher-order means nothing more than that, and there is no syntax for it.
2. **`f x y` is `(f x) y`** because `->` is right-associative. **Partial application is therefore
   free**, and `map (add 3)` needs no machinery.
3. **`map` keeps the length, `filter` keeps the elements.** Between them, most `for` loops.
4. **`zipWith` is the two-index loop** and it is the one people get wrong by hand.
5. **Comprehensions and combinators are the same computation.** Prefer whichever names the idea
   better.
6. **`.` is right-to-left glue and `$` deletes a bracket.** `(== LEC) . kind` is the idiom of the
   term.
7. **Point-free is right up to the point where you cannot see the arguments.** If you reach for
   `flip`, stop and name them.
8. **Four functions that differ only in an operator have one function's worth of content.** L06 names
   it.

---

## Exercises

*(Not assessed. PS 2 is the assessed work.)*

1. `:t` these and say what each is: `map map`, `(.) . (.)`, `zipWith const`, `filter . (==)`,
   `uncurry (+)`. Two of them are useful and three are puzzles.
2. Write `lectureMinutes` three ways — a comprehension, a combinator pipeline, and explicit recursion —
   and say which you would put in a code review.
3. `takeWhile (< 100) [1..]` terminates. `filter (< 100) [1..]` does not. Explain the difference in
   one sentence, then check both. *(This is Week 3 arriving early.)*
4. Without running it, say what `map (map (* 2)) [[1,2],[3]]` is, then what
   `(map . map) (* 2) [[1,2],[3]]` is. They are the same. Why?
5. Rewrite `pairs` from Lab 1 without a list comprehension, using only `zip`, `concatMap` and
   `drop`. Which version would you rather maintain?

---

*PROG 202 · Week 2 · L05 · © CSE Department*
