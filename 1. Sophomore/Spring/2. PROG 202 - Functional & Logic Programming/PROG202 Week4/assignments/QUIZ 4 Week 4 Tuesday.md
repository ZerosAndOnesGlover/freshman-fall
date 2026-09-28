# PROG 202 · Quiz 4
## Administered: Tuesday, Week 4 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 3** — thunks, weak head normal form, strictness, space leaks, infinite lists.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then mark it yourself before you leave the room.

---

**Q1.** Define *weak head normal form* in one sentence.

&nbsp;

&nbsp;

---

**Q2.** `let p = (1+1, 2+2)`. After `p `seq` ()`, `:sprint p` shows `(_,_)`. Why did `seq` do nothing?

&nbsp;

&nbsp;

---

**Q3.** A one-pass mean written with `foldl'` held **727 MB**. `foldl'` is the strict fold. What leaked?

&nbsp;

&nbsp;

---

**Q4.** The two-pass version leaked at `-O0` **and** `-O2`, and no `seq` fixes it. What is that problem
called, and why is `seq` no help?

&nbsp;

&nbsp;

---

**Q5.** `foldl (+) 0 [1..10⁷]` was 619 MB at `-O0` and 44 KB at `-O2`. Name the pass, and say why
`foldl'` is the rule anyway.

&nbsp;

&nbsp;

---

**Q6.** `fibs = 0 : 1 : zipWith (+) fibs (tail fibs)` works; `bad = zipWith (+) bad (tail bad)` is
`<<loop>>`. One word for the difference, and one sentence.

&nbsp;

&nbsp;

---

**Q7.** `Data.Map.Lazy` as a counter held **107 MB** where `Data.Map.Strict` held 44 KB — at `-O2`, where
the lazy *pair* was repaired. Why could the optimiser not repair this one?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **A value is in weak head normal form when its outermost constructor is known.** Nothing is said
about its fields.

*Do not accept "evaluated one level" on its own — the vaguer phrasing is what produces Q3's 727 MB.*

---

**Q2.** Because `p` was **already** in WHNF: the pair constructor was known the moment `p` was written, so
`seq` had no work to do — **and it never touches the components.**

---

**Q3.** **The accumulator's two components.** `foldl'` forces the accumulator to WHNF, the accumulator is a
pair, and the WHNF of a pair is the pair constructor — so `(s + x, c + 1)` is confirmed to be a pair and
both fields stay thunks. **Two chains, ten million links each.**

*The fixes: bang the components, or `data Acc = Acc !Int !Int` — which also removes the allocation,
110 KB against 160 MB.*

---

**Q4.** **Retention.** `xs` is named and two traversals need it, so already-evaluated cells stay
**reachable**. `seq` forces unevaluated things; here nothing is unevaluated. The only fix is to stop
holding the reference — which is what the one-pass version is for.

---

**Q5.** **Strictness analysis**, which proves that if the result is demanded then the accumulator is
demanded, so it may be evaluated as the fold goes.

**`foldl'` is the rule because it says `seq` out loud** — it is 44 KB at *every* optimisation level, and
does not depend on an analysis succeeding. The `-O0` column is the proof that the 44 KB is not part of the
program's meaning.

---

**Q6.** **Productive.** `fibs`' first cell is the literal `0 :`, available without consulting the
recursive part, so `zipWith` always has cells already produced; `bad`'s outermost cons is not available
until `zipWith` produces one, and `zipWith` needs it first.

---

**Q7.** **The thunks are values inside a balanced tree**, and the strictness analyser cannot see through a
data structure to prove that every value in it will be demanded. `insertWith (+)` on a lazy map forces the
**map** to WHNF — the tree node — and stores the *unapplied addition* as the value.

**It is Q2's pair, one level deeper and out of the optimiser's reach** — which is why `Data.Map.Strict`
exists as a separate module rather than as a compiler flag.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| **Q1, Q2** | **L07 §3** — today's lecture is about constraints on types, and this is the definition the *rest of the course* keeps needing |
| Q3, Q4 | L07 §5 and §6 |
| **Q5** | **L07 §4** — on the midterm |
| Q6 | L08 §2 |
| **Q7** | **L07 §6's last paragraph, and PS 3 Q5(b)** |

**Q1 and Q4 are the two that recur.** The midterm is in Week 6 and covers Weeks 0–5; the distinction
between *retention* and *not-yet-evaluated* is the single most examinable thing in Weeks 0–3.

---

*PROG 202 · Week 4 · Quiz 4 · covers Week 3 · ungraded*
