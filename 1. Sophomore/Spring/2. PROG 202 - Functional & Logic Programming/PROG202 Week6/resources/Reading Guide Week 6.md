# PROG 202 · Reading Guide · Week 6
## The midterm is Thursday — so this week's reading is short on purpose

---

**This is the lightest reading week of the term, deliberately.** The midterm is **Thursday 18:00–19:15**,
covering Weeks 0–5, and Project 1 is due the following Friday. **Budget one hour on reading and put the rest
into the paper and the project.**

| | Now? | Why |
|---|---|---|
| **Hutton §12.2** | **Read** | `Applicative`. You skipped it in Week 4 on instruction; this is the week it has a reason |
| **Wadler §4** | **Read** | The state monad in the original. Twenty minutes, and it is L12 in better prose |
| McBride & Paterson (2008), §1–§2 | **Optional, and the best thing here** | The paper that introduced `Applicative`. §1's examples are the motivation the class is usually taught without |
| Hutton §14.5 (`Traversable`) | **Read now** | Four pages, and this is finally the week it makes sense |
| `mtl` documentation | Reference | Do not read it through. Know that `MonadState`, `MonadError`, `MonadReader` exist and that they are why you write no `lift` |

---

## Hutton §12.2 — with a reason this time

In Week 4 you were told to stop at the end of §12.1 because `Applicative` without a motivation is a list of
operators. **L13 §1 is the motivation**: `Either` reports one error out of three, and that is what `>>=`
*means*.

**Questions:**

1. Hutton gives the four applicative laws. **You will not use them directly.** The one that matters is the
   relationship law `(<*>) == ap`, which he mentions in passing. **Find where**, and note that L13 §4 breaks
   it on purpose.
2. §12.2's `Applicative` instance for lists is *not* the one you would guess. **Predict `[(+1),(*2)] <*>
   [1,2]`**, then check. *(There are four answers, not two.)*
3. Hutton presents `Applicative` as a step on the way to `Monad`. **L13 §4 argues it is not.** Decide which
   presentation you find more useful and be able to say why — it is a fair final-exam question.

---

## McBride & Paterson, "Applicative programming with effects" (2008)

**Optional, thirteen pages, and the best-written thing on this week's subject.**

§1 introduces the pattern through four examples — sequencing commands, transposing matrices, evaluating
expressions, and traversing — **before naming it**. That order is the point: the abstraction is presented as
something that kept recurring, not as a definition to memorise. *(Perlis's epigram from L10 again: simplicity
follows complexity.)*

**If you read one thing:** §2's `transpose` example. It is four lines, it uses an applicative you would never
have thought of, and it is the clearest demonstration that `<*>` is not merely weaker `>>=`.

**The paper's own summary of the thesis is the quote at the top of L13** — *"weaker than Monads and hence
more widespread"* — and the whole argument is in that clause.

---

## Hutton §14.5 — `Traversable`, at last

Four pages. You have now met `traverse` three times without being told what it was: Lab 1's `traverse id`,
Week 5's `sequence`, and L13 §5.

**Question:** `traverse`'s constraint is `Applicative f`. **Write down what would change if it were
`Monad f`** — one sentence about error reporting, one about evaluation order. The second is why Week 7 can
parallelise a traversal and is the reason the constraint is what it is.

---

## Not This Week

**Nothing about Prolog.** Week 8 changes language entirely and the syntax reference starts again from zero.
**Do not read ahead into Clocksin & Mellish** — the two halves of this course do not mix well in one head,
and seven weeks of "no mutation" is what makes "no functions either" survivable.

**Nothing more on transformers.** `mtl`'s documentation is a reference, not a text, and the `n²` instance
table is there to be looked up rather than read. **L14 §3's one rule** — the effect that must survive a
failure goes outside `ExceptT` — is 90% of what you will need for years.

---

## What to Actually Do

**Before Thursday:** write your one A4 sheet for the midterm. **It is the best revision exercise available**
and the paper explicitly permits it.

The three things worth the most space on it, in order:

1. **`State`'s three instances and `>>=`** — Section C offers this as a fifteen-mark question.
2. **The definition of weak head normal form**, and the two places it cost money (`foldl'` over a pair;
   `Data.Map.Lazy`).
3. **The fold table** — which fold for which operator, and the eight residency figures.

**The paper prints its own figures**, so do not waste sheet space on numbers. Spend it on definitions and on
the two or three code skeletons you would otherwise have to reconstruct under time pressure.

---

*PROG 202 · Week 6 · Reading Guide · © CSE Department*
