# CS 211 · Lab 1
## Two Lexers, and Where They Disagree

---

**Week 1 · Friday 14:00–15:50 · BH 220** — after both of this week's lectures.
**Unmarked.** The TA checks your work off in the session.
**Starter files:** `lexer.py` (a working hand-written lexer), `sample.cy`, `compare.sh`.

> **You are given the hand-written lexer today and asked to write one yourself in PS 1.** That is
> deliberate: the lab is about the *comparison*, and you cannot compare two things when you have
> not yet built either. In PS 1 you will diff your own lexer against both of today's.

---

## Why This Lab Exists

L04 claimed that a regular expression can always be turned into a table, that `flex` does exactly that, and that the result is equivalent to a lexer you write by hand.

**"Equivalent" is a strong word and you should not take it on trust.** Today you build the `flex` version, run both on the same input, and diff the token streams. On valid programs they agree exactly. **Then you go looking for inputs where they do not** — and every one you find will be about error handling, not about tokenising.

---

## Part 1 — Read the Hand-Written Lexer (15 minutes)

Open `lexer.py`. It implements `The Cyan Language Reference` §2 directly.

```bash
python3 lexer.py sample.cy | head -20
python3 lexer.py sample.cy | wc -l
```

**You should see 109 tokens.**

**Q1.** The main loop dispatches on the first character of each token. **List the seven cases it distinguishes**, in the order it tries them, and say why whitespace and comments come first.

**Q2.** Find `OPERATORS` near the top. **The list is ordered longest-first.** Delete that ordering — sort it alphabetically — and rerun on `sample.cy`. What breaks, and which line of `sample.cy` shows it first? **Restore the ordering afterwards.**

**Q3.** `tokenize` records `line` and `col` on every token, and nothing in this lab reads them. **Name the phase that will**, and say what breaks in Week 3 if the lexer drops them.

---

## Part 2 — Write the flex Version (35 minutes)

Create `cyan.l`. The skeleton below is the structure; **the rules are yours to write.**

```
%{
#include <stdio.h>
%}
%option noyywrap
%option yylineno

DIGIT   [0-9]
LETTER  [A-Za-z_]
IDENT   {LETTER}({LETTER}|{DIGIT})*
INT     {DIGIT}+

%x COMMENT

%%
    /* --- comments: one line rule, three COMMENT-state rules --- */

    /* --- keywords: one alternation rule, printing KEYWORD(...) --- */

    /* --- IDENT, INT, STRING --- */

    /* --- operators: two rules, and the ORDER MATTERS --- */

    /* --- punctuation --- */

    /* --- whitespace, then a catch-all --- */
%%

int main(void) { yylex(); return 0; }
```

**Output format must match `lexer.py` exactly**, or the diff is useless:

```
KEYWORD(fn)
IDENT(fib)
PUNCT(()
OP(<=)
INT(2)
STRING("hi\n")
```

Build and compare:

```bash
./compare.sh sample.cy
```

**Target: `IDENTICAL -- 109 tokens`.**

> **Three things that will bite you, in the order they usually do:**
>
> **1. The keyword rule must come before `{IDENT}`.** Both match `fn`, both at length 2, so the
> tie-break is rule order — L03 §4. Put `{IDENT}` first and every keyword becomes an identifier.
>
> **2. Two-character operators must come before one-character operators.** flex prefers the longest
> match, so this is usually forgiven — but not when your character class accidentally matches
> first. Write `"=="|"!="|...` above `[-+*/%<>!=]`.
>
> **3. Escaping inside `[...]`.** The punctuation class needs `[(){}\[\],;:.]` — the brackets and
> the backslash are the awkward ones. If flex reports "unrecognized rule", this is why.

**Q4.** Get `IDENTICAL -- 109 tokens` and show the TA.

**Q5.** Your `COMMENT` start condition is a **second DFA** (L04 §8). Delete the `%x COMMENT` machinery and try to handle `/* ... */` with a single regular expression instead. **Either get it working or explain precisely what defeats you** — and if you get it working, say what it does to `a/* /* */ */b`.

---

## Part 3 — Make Them Disagree (35 minutes)

Both lexers now agree on `sample.cy`. **Find inputs where they do not.**

For each input below, run both and record the two outputs.

```
a<=b
a< =b
x-->y
a<<=b
ifx
if x
x/**/y
a/* /* */ */b
12abc
"unterminated
a&b
```

**Q6.** **Eight of the eleven agree. Which three do not?** Fill in a table:

| Input | flex | hand-written | Same? |
|---|---|---|---|

**Q7.** `x-->y` produces four tokens in both. **Write them down.** Then explain, using maximal munch, why the first `-` does not become part of a `->`.

**Q8.** `a/* /* */ */b` produces `IDENT(a) OP(*) OP(/) IDENT(b)` in both. **Trace it.** Where exactly does the comment end, and what is `*/b` being read as?

**Q9.** The three disagreements are all on **invalid** input. State the general pattern in one sentence — what does flex do that the hand-written lexer does not?

**Q10.** `12abc` is the sharpest case. flex gives `INT(12) IDENT(abc)`; `lexer.py` raises an error.

- **Which one is applying maximal munch faithfully?**
- **Which behaviour do C and Python have?** Check:
  ```bash
  python3 -c "print(12abc)"
  printf 'int main(void){int x=12abc;return 0;}\n' > n.c && gcc -c n.c
  ```
- The hand-written lexer has a rule flex was never given. **Find it in `lexer.py`** and quote the two lines.

---

## Part 4 — Measure the Table (15 minutes)

L04 §5 claimed the subset construction can blow up exponentially, but that real token sets do not.

```bash
flex -o cyan_lex.c cyan.l
grep -c '' cyan_lex.c
grep -m1 -A3 'yy_nxt\[\]' cyan_lex.c
```

**Q11.** How many lines is the generated C? **How much of it did you write?** Find `yy_nxt` and look at it — that array is the table from L04 §2, and the reason the file is unreadable is that it is a data structure rather than a program.

**Q12.** `flex -v` prints the machine's real size:

```bash
flex -v -o cyan_lex.c cyan.l 2>&1 | head -6
```

**Record the NFA and DFA state counts.** On the reference solution they are **176 NFA states and 70 DFA states, from 13 rules.**

**Now compare that against L04 §5.** There, an NFA of **58** states produced a minimal DFA of **512**. Here an NFA of **176** states produces a DFA of **70** — *fewer* states than the NFA it came from. **Explain the difference in one or two sentences.** What is it about a token set that keeps the subset construction from blowing up?

---

## Before You Leave

The TA checks:

- [ ] **Part 1** — Q1's seven cases; Q2's break demonstrated and then reverted
- [ ] **Part 2** — `./compare.sh sample.cy` printing `IDENTICAL -- 109 tokens`
- [ ] **Part 3** — the eleven-row table filled in, with the three disagreements identified
- [ ] **Part 4** — the generated line count and the DFA state count recorded

**Keep `cyan.l` and your notes.** PS 1 asks you to write the hand-written lexer yourself and diff it against *both* of today's, and Week 2's Lab 2 does the same thing one phase up — bison against recursive descent.

---

## If You Finish Early

**Add a token class.** Cyan has no floating-point literals and no hexadecimal. Add `HEX ::= 0x[0-9a-fA-F]+` to both lexers and get them agreeing again.

**Then break it deliberately:** what does your `HEX` rule do to the input `0x`? To `0xg`? To `12x34`? Get the two lexers to *disagree* on one of those, and say which behaviour you would ship.

---

*Next: Week 2 — the parser. Lab 2 builds Cyan's parser twice as well, once by recursive descent and once with bison, and the disagreement there is not about error handling.*
