# PROG 202 · Haskell Syntax and Symbols
## The punctuation, what each mark is called, and what it means

---

**Haskell's reputation for being unreadable is almost entirely about its punctuation.** The language
has few keywords and a lot of symbols, most of which are ordinary functions rather than syntax — and
you cannot look up an ordinary function if you do not know how to say its name.

**This file is the lookup table.** Everything used anywhere in PROG 202 is here, in the week it first
appears, with what it is called out loud. Keep it open in a second window for the first three weeks.

> **How to read the "Week" column.** A row marked **W0** is in use from the first lecture; a row
> marked **W5** is here so that you can recognise it, and the week named is where it is taught. You
> are not expected to understand `>>=` in Week 0. You *are* expected, from Week 0, to be able to say
> *"that's bind"* rather than *"that's the weird arrow thing"*.

---

## 1. Layout: the rules with no symbols at all

Before any punctuation, the thing that surprises people most: **indentation is syntax.**

```haskell
f x = a + b
  where a = x * 2        -- indented under f, so it belongs to f
        b = x + 1        -- lined up with a, so it is a sibling, not part of a
```

Three rules cover it:

1. **A block's items all start in the same column.** The first item after `where`, `let`, `do` or
   `of` sets the column; everything in the same column is a new item; anything further right is a
   continuation of the previous one; anything further left ends the block.
2. **Tabs are a mistake.** Use spaces. GHC warns with `-Wtabs`, which `-Wall` turns on.
3. **You can always write the braces instead** — `where { a = 1; b = 2 }` is legal — and nobody does,
   except on one line at a GHCi prompt.

**The commonest beginner error in this course** is an equation continued at the wrong column:

```haskell
total = sum xs
+ sum ys          -- ERROR: `+ sum ys` starts at column 1, so it is a new declaration
```

---

## 2. Types

| Symbol | Said out loud | Means | Week |
|---|---|---|---|
| `::` | **"has type"** | `x :: Int` — a type signature or annotation. **Not** C++'s scope operator | **W0** |
| `->` | **"to"** or **"arrow"** | `Int -> Bool` is a function from `Int` to `Bool` | **W0** |
| `=>` | **"implies"** or **"such that"** | `Num a => a -> a` — a *constraint* on the left, the type on the right. Everything before `=>` is a requirement, not an argument | **W0** |
| `[a]` | **"list of a"** | The list type. `[Int]`, `[[Char]]` | **W0** |
| `(a, b)` | **"pair of a and b"** | Tuple type. `(a,b,c)` is a triple; there is no "tuple of n" | **W0** |
| `()` | **"unit"** | The type with exactly one value, also written `()`. Haskell's `void` | **W0** |
| `a`, `b`, `t` | **"type variable"** | Lower case in a type means *any type*. Upper case (`Int`, `Maybe`) is a concrete type or constructor | **W0** |
| `Maybe a` | — | A type *constructor* applied to a type. `Maybe` alone is not a type | **W1** |
| `\|` | **"or"** | In a `data` declaration, separates constructors | **W1** |
| `forall a.` | **"for all a"** | Explicit quantification. Implicit in every signature you write | W6 |

**`=>` is the one that trips everyone.** In `elem :: Eq a => a -> [a] -> Bool`, the function takes
**two** arguments, not three. `Eq a` is a promise the caller must be able to keep, not a value.

---

## 3. Definitions and bindings

| Symbol | Said out loud | Means | Week |
|---|---|---|---|
| `=` | **"is defined as"** | An equation. **Never assignment.** `x = x + 1` is a lie, not a command | **W0** |
| `_` | **"wildcard"** or **"don't care"** | A pattern that matches anything and binds nothing | **W0** |
| `where` | — | Definitions local to one equation, *after* it. Can see the equation's arguments | **W0** |
| `let … in …` | — | Definitions local to one *expression*. `let x = 1 in x + x` | **W0** |
| `case … of` | — | Pattern match on a value, anywhere an expression is allowed | **W1** |
| `\|` (in an equation) | **"guard"** or **"such that"** | `f x \| x > 0 = 1 \| otherwise = 0` — a boolean condition on a clause | **W0** |
| `@` | **"as-pattern"** | `all@(x:xs)` binds the whole list to `all` *and* matches its parts | **W1** |
| `~` | **"lazy pattern"** or **"irrefutable"** | Match without forcing. Rare, and Week 3's | W3 |
| `!` | **"bang pattern"** | Force this argument. Needs `{-# LANGUAGE BangPatterns #-}` | W3 |

**`where` versus `let`.** `where` attaches to an *equation* and can be shared by all its guards;
`let` is an *expression* and can appear in the middle of one. When either works, Haskell style
prefers `where`, because it puts the main definition first and the helpers after.

---

## 4. Lists and strings

| Symbol | Said out loud | Means | Week |
|---|---|---|---|
| `[]` | **"nil"** or **"empty list"** | Both the empty list and its type constructor | **W0** |
| `:` | **"cons"** | `1 : [2,3]` is `[1,2,3]`. **Right-associative**, so `1:2:3:[]` works. The *only* list constructor | **W0** |
| `++` | **"append"** | `[1,2] ++ [3]`. **O(n) in its left argument** — Week 2 measures what that costs | **W0** |
| `!!` | **"index"** | `xs !! 2`. O(n). If you are reaching for it, you probably want a different type | **W0** |
| `..` | **"range"** or **"enum from to"** | `[1..10]`, `[1,3..9]`, `[1..]` (infinite) | **W0** |
| `[ e \| q, … ]` | **"list comprehension"** | `[ x*2 \| x <- xs, x > 0 ]` — "the `x*2` for each `x` drawn from `xs` such that `x > 0`" | **W0** |
| `<-` (in a comprehension) | **"drawn from"** | The generator. Not the same `<-` as in `do` — see §7 | **W0** |
| `"abc"` | — | A `String`, which *is* `[Char]`. Not a distinct type | **W0** |
| `'a'` | — | A single `Char`. Single quotes and double quotes mean different types | **W0** |

**`String = [Char]` is a real type synonym**, which is why `reverse`, `map`, `filter` and `++` all
work on strings with no string-specific function needed — and why `String` is a slow way to hold a
megabyte of text. `Data.Text` exists for that, and Week 2 says when to reach for it.

---

## 5. Functions and application

| Symbol | Said out loud | Means | Week |
|---|---|---|---|
| *(a space)* | **"applied to"** | `f x y` is `f` applied to `x`, then applied to `y`. **Binds tighter than every operator** | **W0** |
| `.` | **"compose"** | `(f . g) x` = `f (g x)`. Right to left, like in maths | **W0** |
| `$` | **"apply"** | `f $ x + 1` = `f (x + 1)`. Lowest precedence, right-associative — **it exists to delete brackets** | **W0** |
| `\x -> e` | **"lambda"** | An anonymous function. The `\` is meant to look like a λ | **W0** |
| `` `f` `` | **"infix"** | Backticks make a named function infix: ``x `div` y`` is `div x y` | **W0** |
| `(+ 1)`, `(1 +)` | **"section"** | A partly applied operator. `(+1)` adds one; `(subtract 1)` is how you write `(-1)`, which would be negative one | **W0** |
| `(,)` | — | The pair constructor as a function. `(,) 1 2` is `(1,2)` | W2 |
| `flip`, `const`, `id` | — | Not symbols, but the three functions whose names you must know before Week 2 | **W0** |

**`f x y` is not `f(x, y)`.** It is `(f x) y`: `f` applied to `x` gives back a *function*, which is
then applied to `y`. This is **currying** and it is the reason every Haskell type is written with
arrows all the way down. Week 2 depends on it completely.

**`$` deserves its own line.** These three are the same expression:

```haskell
print (sum (map (*2) [1..10]))
print $ sum $ map (*2) [1..10]
print . sum . map (*2) $ [1..10]
```

**Do not become the person who writes the third one everywhere.** Use `$` to remove a bracket that
spans a long line; keep the brackets when they are short.

**`-` is the one genuinely irregular symbol in the language.** It is both subtraction and negation,
so `(-1)` is the number minus one, *not* the "subtract one" section, and `f -1` parses as
`f - 1`. Write `subtract 1`, or `(+ (-1))`, and move on.

---

## 6. Operators you will meet as characters before you meet as ideas

| Symbol | Said out loud | Means | Week |
|---|---|---|---|
| `<$>` | **"fmap"** | Infix `fmap`. `(+1) <$> Just 2` is `Just 3` | W4 |
| `<*>` | **"ap"** or **"apply"** | Applicative application | W6 |
| `>>=` | **"bind"** | Monadic sequencing. `m >>= f` | W5 |
| `>>` | **"then"** | Sequence, discarding the first result | W5 |
| `=<<` | **"reverse bind"** | `>>=` with the arguments swapped | W5 |
| `<>` | **"mappend"** | Semigroup combine. For lists it is `++` | W4 |
| `<\|>` | **"alternative"** or **"or else"** | First success of two. Parsec, and Week 6 | W6 |
| `&&`, `\|\|`, `not` | — | Boolean. `&&` and `\|\|` are lazy in the right argument | **W0** |
| `==`, `/=` | **"equals", "not equals"** | Note `/=`, not `!=` | **W0** |
| `<`, `<=`, `>`, `>=` | — | From `Ord`. Work on anything comparable, including lists and tuples | **W0** |

**`/=` is not a typo.** `!` is not a special character in Haskell operator names, and `!=` would be a
perfectly legal operator someone could define to mean something else.

---

## 7. `do`, and the `<-` that is not a generator

| Symbol | Said out loud | Means | Week |
|---|---|---|---|
| `do` | — | Sequences actions in a monad. **W0 uses it only for `IO`** | **W0** |
| `<-` (in a `do`) | **"bind"** or **"get"** | `line <- getLine` — perform the action, name its result. **Not assignment**: `line` never changes | **W0** |
| `let` (in a `do`) | — | An ordinary definition inside a `do` block. **No `in`** | **W0** |
| `return` / `pure` | **"return"** / **"pure"** | Wrap a value as an action that does nothing. **Not C's `return`** — it does not exit anything | **W0** |

```haskell
main :: IO ()
main = do
  putStrLn "name?"
  name <- getLine            -- <- : perform, then bind the String
  let greeting = "hi " ++ name   -- let : ordinary definition, no `in`
  putStrLn greeting
```

**Three warnings, all of which you will hit this week:**

- **`return` is not a control-flow statement.** `return 5` in the middle of a `do` block computes a
  value and throws it away. Nothing exits.
- **`name <- getLine` is legal; `name = getLine` inside `do` is not what you meant.** The first gives
  you a `String`; the second, written `let name = getLine`, gives you an `IO String` you have not
  performed.
- **The `<-` in a `do` block and the `<-` in a list comprehension are not the same arrow**, although
  Week 5 will show you that they are more closely related than they look.

---

## 8. Comments, pragmas, and the module header

| Symbol | Means | Week |
|---|---|---|
| `--` | Line comment. **Needs a space after it** if the next character is a symbol: `-->` is an operator, not a comment | **W0** |
| `{- … -}` | Block comment. Nests properly, unlike C's | **W0** |
| `-- \|` | Haddock documentation for the thing *below* it | **W0** |
| `-- ^` | Haddock documentation for the thing *before* it | **W0** |
| `{-# … #-}` | A **pragma**: `{-# LANGUAGE BangPatterns #-}`, `{-# INLINE f #-}`, `{-# NOINLINE f #-}` | W3 |
| `module M where` | The module header. `Main` with a `main` is the executable | **W0** |
| `import D.L (sort)` | Import, with an **explicit list**. This course wants the list | **W0** |
| `import qualified D.M as M` | Qualified import; use as `M.insert`. **How you use `Data.Map`** | W2 |

---

## 9. A worked line

Every symbol in this course's most typical single line:

```haskell
busiest = snd . last . sort . map swap
  where swap (c, m) = (m, c)
```

| Piece | Reading |
|---|---|
| `busiest = …` | An *equation*: `busiest` **is** the thing on the right. No arguments are named |
| `snd . last . sort . map swap` | Four functions **composed**, applied right to left |
| `map swap` | `map` **applied to** `swap` — one argument of two, so the result is still a function |
| `where` | What follows is local to this equation |
| `swap (c, m) = (m, c)` | An equation whose argument is matched **against the shape** `(c, m)` |

Read aloud: *"busiest is snd, after last, after sort, after map swap — where swap takes a pair c-m
and gives back the pair m-c."*

**If you can do that with any line of this course's code, you can read Haskell.** The rest is
vocabulary.

---

## 10. The ten you must recognise before Week 1's first lecture

`::` `->` `=>` `=` `_` `:` `++` `.` `$` `<-`

**Say each one out loud now.** Week 1 introduces `data`, `|`, `case … of` and `@`, and it assumes
these ten are gone from your working memory as obstacles.

---

*PROG 202 · Week 0 · Reference · © CSE Department. Prolog gets its own reference of exactly this
shape — `Prolog Syntax and Symbols`, in Week 8's `resources/` — because its punctuation shares almost
nothing with this one.*
