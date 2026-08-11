# CS 211 · Lab 1 · Solutions and Checkoff Notes
## Instructor Only

---

**Lab 1 is unmarked.** These notes exist so the checkoff is consistent and so the TA knows which failures are interesting.

> **Every number below was measured** with flex 2.6.4, gcc 13.3.0 and Python 3.14.2 against the
> reference `cyan.l` and the shipped `lexer.py`.

---

## Part 1 — Read the Hand-Written Lexer

### Q1 — The seven cases, in order

1. **Whitespace** (` \t\r\n`) — discarded
2. **Line comment** `//` — discarded to end of line
3. **Block comment** `/*` — discarded to first `*/`
4. **Identifier or keyword** — starts with a letter or `_`
5. **Integer** — starts with a digit
6. **String** — starts with `"`
7. **Operator, then punctuation** — maximal munch over the operator list, else a single punctuation character

**Why whitespace and comments come first:** they are the only cases that produce *no token*. Putting them at the top means the rest of the loop can assume it is looking at the start of a real token, and never has to re-check.

**Accept a six-case answer that merges the two comment forms.** Do not accept an answer that puts identifiers before whitespace — ask what happens to the space in `if x`.

### Q2 — Breaking the operator ordering

Sorting `OPERATORS` alphabetically gives:

```
['!', '!=', '%', '&&', '*', '+', '-', '->', '/', '<', '<=', '=', '==', '>', '>=', '||']
```

**Result: 109 tokens becomes 112.** *(Measured.)*

**First divergence is at token 19, on line 7:**

```
fn fib(n: int) -> int {
```

`->` becomes `OP(-)` then `OP(>)`, because `-` now precedes `->` in the list and `startswith` accepts the first match it finds.

**The three extra tokens** are the splits of `->` (line 7), `<=` (line 8) and `->` (line 12).

**Students often predict `<=` breaks first.** It is `->` — worth pointing out, because it shows they scanned for the operator they were thinking about rather than reading the file in order.

### Q3 — Who reads `line` and `col`

**Week 3's type checker**, and every phase after it that reports an error. If the lexer drops them, **there is no way to recover them later** — the AST has no character offsets, and the source text is long gone by the time the type checker runs.

The concrete failure: PS 3 requires an error message naming a line. A student without positions must either re-lex the source (and reconcile two token streams) or ship `type error` with no location.

**This is why PS 1 marks positions at 4 points.** Every year a few students treat them as optional and pay in Week 3.

---

## Part 2 — The flex Version

### Reference `cyan.l`

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
"//".*                  { /* line comment */ }
"/*"                    { BEGIN(COMMENT); }
<COMMENT>"*/"           { BEGIN(INITIAL); }
<COMMENT>.|\n           { /* skip */ }

"fn"|"let"|"if"|"else"|"while"|"return"|"struct"|"new"|"true"|"false"|"int"|"bool"|"string" {
                          printf("KEYWORD(%s)\n", yytext); }

{IDENT}                 { printf("IDENT(%s)\n", yytext); }
{INT}                   { printf("INT(%s)\n", yytext); }
\"([^\"\\\n]|\\.)*\"    { printf("STRING(%s)\n", yytext); }

"=="|"!="|"<="|">="|"&&"|"||"|"->"   { printf("OP(%s)\n", yytext); }
[-+*/%<>!=]             { printf("OP(%s)\n", yytext); }
[(){}\[\],;:.]          { printf("PUNCT(%s)\n", yytext); }

[ \t\r\n]+              { /* whitespace */ }
.                       { printf("ERROR(%s)\n", yytext); }
%%

int main(void) { yylex(); return 0; }
```

### Q4 — The target

```
$ ./compare.sh sample.cy
IDENTICAL -- 109 tokens
```

**Common failures, in the order they occur:**

| Symptom | Cause |
|---|---|
| Every keyword prints as `IDENT` | `{IDENT}` rule placed above the keyword rule |
| `unrecognized rule` from flex | `[(){}\[\],;:.]` mis-escaped — the `[` and `]` are the usual culprits |
| `->` splits into two tokens | The one-character operator class placed above the two-character alternation |
| Trailing token count off by one | Missing `[ \t\r\n]+` rule, so newlines hit the catch-all and print `ERROR` |
| Comments produce tokens | `%x COMMENT` declared but `BEGIN(COMMENT)` never called |

**A student whose count is 109 but whose diff is non-empty** has an output-format mismatch — usually `PUNCT` versus `OP` for one character. Point at `delta.txt`.

### Q5 — Block comments without a start condition

**It can be done**, and the regex is the awkward part:

```
"/*"([^*]|\*+[^*/])*\*+"/"     { /* block comment */ }
```

**This works and produces identical output on `sample.cy`.** The pattern says: `/*`, then any run of non-`*` characters or `*`s not followed by `/`, then a final run of `*`s and a `/`.

**On `a/* /* */ */b` it gives the same answer** — `IDENT(a) OP(*) OP(/) IDENT(b)` — because it is still non-greedy about the *first* `*/`.

**Students who fail to get it working** should be credited for a correct account of *why* it is hard: the naive `"/*".*"*/"` is greedy and swallows everything to the **last** `*/` on the line, and `.` does not match newline so multi-line comments fail entirely. **Either outcome is a pass**; the question is diagnostic.

**Worth saying aloud:** the start-condition version is what you would ship, because it is readable. The single-regex version is a party trick that demonstrates the theory — both are finite state, and L04 §8's claim that start conditions are "still finite state" is exactly this equivalence.

---

## Part 3 — Making Them Disagree

### Q6 — The table

| Input | flex | hand-written | Same? |
|---|---|---|---|
| `a<=b` | `IDENT(a) OP(<=) IDENT(b)` | same | ✅ |
| `a< =b` | `IDENT(a) OP(<) OP(=) IDENT(b)` | same | ✅ |
| `x-->y` | `IDENT(x) OP(-) OP(->) IDENT(y)` | same | ✅ |
| `a<<=b` | `IDENT(a) OP(<) OP(<=) IDENT(b)` | same | ✅ |
| `ifx` | `IDENT(ifx)` | same | ✅ |
| `if x` | `KEYWORD(if) IDENT(x)` | same | ✅ |
| `x/**/y` | `IDENT(x) IDENT(y)` | same | ✅ |
| `a/* /* */ */b` | `IDENT(a) OP(*) OP(/) IDENT(b)` | same | ✅ |
| **`12abc`** | `INT(12) IDENT(abc)` | **error:** malformed number | ❌ |
| **`"unterminated`** | `ERROR(") IDENT(unterminated)` | **error:** newline in string | ❌ |
| **`a&b`** | `IDENT(a) ERROR(&) IDENT(b)` | **error:** unexpected `&` | ❌ |

*(All eleven measured.)*

### Q7 — `x-->y`

**Four tokens: `IDENT(x)` `OP(-)` `OP(->)` `IDENT(y)`.**

At the first `-`, the lexer tries the longest operator that matches. `--` is not a Cyan operator, and `->` requires the next character to be `>` — it is `-`. **So the longest match at that position is the single `-`.** At the second `-`, the next character *is* `>`, so `->` matches and wins.

**The lexer is not confused.** It produced the longest legal token at each position, which is all maximal munch promises. The result is a syntax error in Week 2, not a lex error here — and that division is the design working.

### Q8 — `a/* /* */ */b`

```
a          -> IDENT(a)
/*         -> comment opens
 /*        -> inside a comment; the second /* is just characters
 */        -> comment CLOSES here (comments do not nest)
 */b       -> live code again
   *       -> OP(*)
   /       -> OP(/)
   b       -> IDENT(b)
```

**The comment ends at the first `*/`.** Everything after it is code, and ` */b` lexes as `*`, `/`, `b`.

**If a student expects `IDENT(a) IDENT(b)`**, they have assumed nesting. `The Cyan Language Reference` §2 says "not nested", and this is what that sentence buys.

### Q9 — The pattern

**flex recovers and continues; the hand-written lexer stops at the first error.**

Accept any phrasing of that. The stronger answers add *why it matters*: recovering reports every error in one compile, stopping gives a better message for the first and avoids a cascade of bogus follow-on errors.

### Q10 — `12abc`

**Which applies maximal munch faithfully?** **flex.** No rule matches `12abc`; the longest match at position 0 is `12`; then `abc` matches `IDENT`. flex did exactly what it was told.

**What do C and Python do?** Both reject it:

```
$ python3 -c "print(12abc)"
SyntaxError: invalid decimal literal

$ gcc -c n.c
error: invalid suffix "abc" on integer constant
```

**Note gcc's wording** — it read `12abc` as *one* malformed token, not two. **That is a third position**, distinct from both lab lexers, and the best answers notice it.

**The two lines in `lexer.py`:**

```python
# An identifier may not start immediately after a digit: 12abc
if j < n and is_letter(src[j]):
    raise LexError(f"line {line}: malformed number '{src[i:j+1]}'")
```

**This rule is an addition to the specification**, not a consequence of it. It exists because `12abc` is almost always a typo, and reporting it here gives a better message than letting the parser fail on two adjacent tokens it cannot combine.

---

## Part 4 — Measuring the Table

### Q11

**1,906 lines of generated C** from a 35-line `cyan.l`. *(Measured.)*

`yy_nxt` is the transition table from L04 §2. **The file is unreadable because it is a data structure**, and that is the point worth making — nobody wrote those numbers, the subset construction did.

### Q12

```
$ flex -v -o cyan_lex.c cyan.l 2>&1 | head -6
  176/2000 NFA states
  70/1000 DFA states (367 words)
  13 rules
```

**176 NFA states → 70 DFA states.** *(Measured.)*

**The DFA is smaller than the NFA.** Against L04 §5, where 58 NFA states produced 512.

**The explanation to draw out:** a token set is a *union of short, mostly disjoint patterns*. After the first character or two, the machine has usually committed to one token class, so the reachable subsets are few and small. **The blowup needs patterns that force the machine to track a sliding window** — "the character $n$ from the end was an `a`" — and nothing in a token specification does that, because tokens are recognised left to right with no lookbehind.

**Accept:** "the alternatives are disjoint so the subsets stay small". **Push for more** from a student who says only "token sets are simple".

---

## Checkoff Summary

| Part | Minimum to pass |
|---|---|
| **1** | Seven cases listed; Q2's break demonstrated live and reverted; Q3 names Week 3 |
| **2** | `IDENTICAL -- 109 tokens` shown running |
| **3** | Eleven-row table with the three disagreements correctly identified; Q10's two lines quoted |
| **4** | 1,906 and 176/70 recorded, with an attempt at the explanation |

**If a student is short on time, cut Part 4's Q11.** Do not cut Q10 — it is the only place the lab makes the error-recovery choice concrete, and PS 1 asks them to defend their own version of it.

---

*CS 211 · Lab 1 Solutions · Instructor Only*
