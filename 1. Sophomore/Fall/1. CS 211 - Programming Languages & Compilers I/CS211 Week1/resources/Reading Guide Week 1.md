# CS 211 · Week 1 · Reading Guide
## Dragon Chapter 3 — the longest single reading of the term

---

**Set reading:** Aho et al., **Chapter 3** (§3.1–3.9). Skip §3.10 unless you are curious.
**Optional:** Appel, **Chapter 2**. Shorter, and better on the *implementation* than the theory.
**Reference:** `flex` manual, §"Patterns" and §"Start Conditions" — `man flex`, or `info flex`.

**Start this over the weekend.** Chapter 3 is about sixty pages and it is the most theory-dense chapter you will meet before Week 8. **The good news is that you will never need to reread it** — lexing is the one phase this course finishes completely in a single week.

---

## How to Read It

**Read §3.1–3.4 before Lecture 3, and §3.6–3.9 after Lecture 4.** The middle section, §3.5 on `lex`, is best read with a terminal open — it is a manual, not an exposition.

> **The chapter is organised backwards from how you will use it.** It builds the theory and then
> reaches the tool. If you want motivation first, read **§3.5 for ten minutes**, see what a `.l` file
> looks like, then go back to §3.1 knowing what the machinery is for.

---

## Section by Section

| § | Pages | What to take from it |
|---|---|---|
| **3.1** | The role of the lexer | Tokens, lexemes, patterns — three words the book keeps carefully distinct and most people conflate. **Learn the distinction**; L03 §1's three-field token is exactly this |
| **3.2** | Input buffering | Sentinels and the two-buffer scheme. **Skim.** It is a real technique and it is not examinable; the idea worth keeping is that the lexer touches every byte and so its inner loop is worth optimising |
| **3.3** | **Specification of tokens** | Regular expressions, formally. §3.3.3's definition is L03 §3's four operators. §3.3.4's extensions are the abbreviations |
| **3.4** | **Recognition of tokens** | Transition diagrams, and the first appearance of maximal munch. **Read §3.4.3 twice** — it is where the "longest match, then first rule" tie-break is stated properly |
| **3.5** | The `lex` tool | Read with a terminal open. Your Lab 1 `cyan.l` is this section applied |
| **3.6** | **Finite automata** | NFA and DFA defined. §3.6.4 is the simulation algorithm from L04 §2 |
| **3.7** | **Regex → automata** | §3.7.1 is the subset construction; §3.7.4 is Thompson's. **This is L04 §3–§4 in full detail** |
| **3.8** | Design of a lexer generator | How `flex` actually works, including the rewind for maximal munch |
| **3.9** | **Minimising DFAs** | §3.9.6 is partition refinement. The uniqueness result is stated here |

---

## The Three Sections That Matter Most

**§3.3.3 — the formal definition of a regular expression.** Four operators. Every time you are tempted to reach for a feature of Python's `re`, come back here and check whether it is one of the four or an abbreviation for them. **Backreferences are neither**, and Q1(d) of PS 1 asks you to prove it.

**§3.7.1 — the subset construction.** The book's presentation is cleaner than most. The two functions are $\varepsilon\text{-}closure$ and $move$, and the algorithm is "keep applying them until no new subsets appear". **If you can write these two functions you can write the whole construction**, and PS 1 Q2 asks you to run it by hand.

**§3.9.6 — minimisation.** Partition refinement, and the uniqueness theorem. **The uniqueness is the part with teeth**: it turns "are these two regular expressions the same?" from a judgement call into a decision procedure, which is PS 1 Q3(b).

---

## What the Book Does Not Emphasise Enough

**The exponential blowup.** §3.7.1 mentions that the DFA may have $2^n$ states and moves on. **L04 §5 measured it** — 58 NFA states producing a minimal DFA of exactly 512 — and the fact that *minimisation does not rescue you* is the part worth carrying. The book's brevity here is reasonable for a compiler text, because the blowup does not arise from real token sets, but it leaves the impression that the bound is loose. **It is not; it is attained exactly.**

**Why the phase split is where it is.** The book separates lexing from parsing on grounds of simplicity, efficiency and portability (§3.1.1). **Those are the practical reasons, and there is a stronger one**: tokens are regular and syntax is not, so the two jobs need different machines. Chapter 3 does not make that argument; §4.2.5 does, in the next chapter, almost in passing. L04 §7 puts them together.

---

## Questions to Read Against

Do not write these up. Several return in PS 1 and in Quiz 2.

**On §3.1 and §3.3**

1. The book distinguishes *token*, *pattern* and *lexeme*. Give all three for the text `<=` appearing in a Cyan program.
2. §3.3.4's extensions (`+`, `?`, character classes) are described as convenient. **Prove one of them adds no power** by rewriting it with the four basic operators.

**On §3.4**

3. §3.4.3 handles the keyword-versus-identifier problem. **The book's answer and Cyan's differ.** Which does `lexer.py` use, and what does the other cost?
4. Transition diagrams in §3.4 have "failure" actions that retract input. **Which Cyan token forces a retraction of more than one character**, or is there none? *(PS 1 does not ask this, but Lab 1's `x-->y` is the case to think about.)*

**On §3.6–3.7**

5. Thompson's construction adds at most two states per operator. **Why does that matter** — what would go wrong if it were quadratic?
6. The subset construction's states are sets. §3.7.1's example produces states like $\{0,1,2,4,7\}$. **What does membership of the NFA's accepting state in such a set mean?**
7. §3.7.4 builds an NFA that always has exactly one accepting state. **Where is that used** in the constructions for concatenation and star?

**On §3.9**

8. Partition refinement starts by splitting accepting from non-accepting. **Why is that the right first split**, rather than, say, splitting on out-degree?
9. The minimal DFA is unique up to renaming. **Does that mean two different regular expressions always produce different minimal DFAs?** Answer carefully.

---

## Two Things to Check on Your Own Machine

**1. What `flex` reports about your scanner.**

```bash
flex -v -o cyan_lex.c cyan.l 2>&1 | head -6
```

**Record the NFA and DFA state counts.** On the reference `cyan.l` they are **176 NFA states and 70 DFA states from 13 rules**. Yours will differ if your rules differ — the number to notice is that the DFA is *smaller* than the NFA, which is the opposite of L04 §5's worst case.

**2. That your compiler agrees about `12abc`.**

```bash
python3 -c "print(12abc)"
printf 'int main(void){int x=12abc;return 0;}\n' > n.c && gcc -c n.c
```

**Both reject it** — Python with `invalid decimal literal`, gcc with `invalid suffix "abc" on integer constant`. **Note gcc's wording**: it read `12abc` as a single malformed token, not as two tokens. That is a third design position, distinct from both of Lab 1's lexers, and worth a moment's thought about which error message is most useful.

---

*Next week's reading is Dragon Ch. 4, §4.1–4.6 — the parser. It is longer than this one but less dense, and you have already met §4.2–4.3 in Week 0's guide.*
