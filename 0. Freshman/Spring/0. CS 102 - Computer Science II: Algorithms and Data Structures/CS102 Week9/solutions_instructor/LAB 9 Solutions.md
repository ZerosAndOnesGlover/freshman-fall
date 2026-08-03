# CS 102 · Lab 9 — Solutions and Checkoff Notes
## Compressing a File with Huffman

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Project 1 is due Friday.** Expect students to be distracted and behind. The lab is self-contained and
takes about an hour for a prepared student; let those who finish A–C early leave to work on the
project.

**Put the A1 corpus figures on the board**: 200,000 characters, **19** distinct symbols, encoded to
**86,136 bytes**. Everything downstream depends on the generator matching, and the spec pins the word
list, the weights, the seeding, and the truncation for exactly that reason.

The most common divergence is the accumulation rule — it is `len(word) + 1` per pick, counting the
separating space, and the join-then-truncate happens afterwards. A student whose corpus is 200,000
characters but has a different symbol count has a different generator.

---

## Part A — The Codec (14)

### A1 (4), A2 (5), A3 (5) — deterministic

| quantity | value |
| --- | --- |
| corpus | 200,000 characters, **19** distinct symbols |
| round trip | lossless, including all three edge cases |
| payload | **86,136 bytes**, padding **0** bits |

**Three bugs to check for specifically**, all of which pass on the main corpus:

1. **No padding length recorded.** Corrupts exactly the final symbol. The corpus happens to encode to a
   whole number of bytes (padding 0), **so this bug is invisible on the corpus** and only shows on the
   edge cases. This is why A3 requires them.
2. **Single-symbol input.** The tree has one node and the natural codeword is the empty string, which
   encodes to zero bits and cannot be decoded. Must be assigned `'0'`.
3. **Bits stored as a string** of `'0'`/`'1'` rather than packed. Round-trips fine and reports a
   "compressed" size eight times too large. Check the type of what `encode` returns.

*The padding-zero coincidence is worth mentioning aloud — it is a good illustration of a test that
passes for a reason unrelated to correctness.*

---

## Part B — Measure It (10)

### B1 (4) — deterministic

| quantity | value |
| --- | --- |
| raw | 200,000 bytes |
| encoded | **86,136 bytes** |
| ratio | **2.322×** |
| space saved | **56.9%** |

### B2 (3) — deterministic

| | bits/char |
| --- | --- |
| raw | 8.0000 |
| fixed-length $\lceil\log_2 19\rceil = 5$ | 5.0000 |
| **Huffman** | **3.4454** |
| **entropy** | **3.4161** |
| overhead | **0.0293** |

Worth drawing out: the theoretical guarantee is "+1 bit", and Huffman achieves **+0.03**. The bound is
worst-case and pessimistic for a 19-symbol alphabet.

### B3 (3) — deterministic

| symbol | count | code length |
| --- | --- | --- |
| space | 55,960 | **2** |
| `t` | 24,656 | 3 |
| `h` | 20,606 | 3 |
| `e` | 18,674 | 3 |
| `o` | 16,271 | 4 |
| `a` | 13,573 | 4 |

Longest **9** bits, shortest **2**.

Expected sentence: code length is non-increasing in frequency — a more frequent symbol never gets a
longer code. *That is a property of any optimal prefix code, not just Huffman's, and a student who says
so has understood the lemma from D5 on the problem set.*

---

## Part C — The Code Table (6)

### C1 (3) — deterministic

A naive (symbol, code-length) table is **38 bytes** for 19 symbols; total **86,174 bytes**, ratio
**2.321×** — a negligible change here.

*Accept any sensible format. A student who stores the full codeword strings will get a larger table and
should be asked why code **lengths** suffice — the canonical-Huffman point from Lecture 30 §5.*

### C2 (3) — deterministic

`"hello world"`: 11 bytes in, **4 bytes** payload, **16 bytes** table, **20 bytes** total. **Net +9
bytes.**

Expected general condition: **when the table costs more than the payload saves** — i.e. for short
inputs, or inputs with a large alphabet relative to their length. Every real format has a
stored-uncompressed fallback for exactly this.

---

## Part D — Three Uncomfortable Measurements (10)

### D1 (4) — deterministic

| method | size | ratio |
| --- | --- | --- |
| Huffman alone | 86,136 bytes | 2.32× |
| `zlib` level 9 | **44,208 bytes** | **4.52×** |

`zlib` is **1.95×** smaller.

Expected explanation: DEFLATE runs **LZ77 first**, replacing repeated substrings with
(distance, length) back-references, and only then applies Huffman. The corpus is built from 30 repeated
words, so `the` occurs tens of thousands of times — **LZ77 encodes each recurrence in a few bits, while
Huffman can only give `t`, `h`, `e` short codes individually.**

The deeper point, worth saying at checkoff: **Huffman is optimal for its model** — independent symbols,
integer bits — **and the model is wrong for text.** An optimal algorithm for the wrong model loses to a
decent algorithm for the right one.

*4 requires naming repeated substrings / back-references. "zlib is better optimised" is 1.*

### D2 (3) — deterministic

50,000 uniform random symbols over 256: entropy **7.9965** bits, Huffman **8.0000** bits, ratio
**1.0000×**.

Expected: uniform data has maximal entropy, so there is nothing to exploit. Stronger answer — and
give credit for it — **no lossless compressor can shrink all inputs**, since there is no injection
from $2^n$ strings into fewer than $2^n$ strings. Compression is a bet on the input distribution.

### D3 (3)

The 12× case is a **two-symbol** alphabet at $P = 0.99$: entropy 0.0808 bits, Huffman 1 bit. The
difference is that Huffman must spend **a whole number of bits per symbol**, and with two symbols the
minimum is 1.

The fix is **arithmetic coding** (or range coding), which encodes the whole message as a single number
and is not constrained to integer bits per symbol.

*3 requires both the cause (integer bits, tiny alphabet) and the name of the fix.*

---

## Checkoff Checklist

1. Corpus has **19** distinct symbols and encodes to **86,136 bytes**.
2. Round trip verified on the **empty string** and a **single character** — not just the corpus.
3. `encode` returns **bytes**, not a string of `'0'`/`'1'`.
4. C2 reports a **net increase** for the short string.
5. D1 explains LZ77 in terms of repeated substrings.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 14 |
| B | 10 |
| C | 6 |
| D | 10 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of 13 required.** This is Lab 9 of 13; a student who has
missed three already cannot afford to miss this one, and it is worth telling them individually.

---

## Note for the Week 10 Lecture

**MIDTERM 2 is in Week 10**, covering Weeks 5–9.

This lab is a good closing image for the greedy half of the course, and worth two minutes in the
Monday lecture. Huffman is **provably optimal**, the proof is two lemmas, and it still loses by 2× to a
method that is not optimal for anything in particular — because it makes a better assumption about the
input.

**Optimality is always relative to a model.** Week 5's Dijkstra is optimal given non-negative weights.
Week 6's Kruskal is optimal given the cut property. Huffman is optimal given independent symbols and
integer bits. **The exam will ask what a proof assumed**, not only what it concluded, and this lab is
where that becomes concrete rather than a slogan.

---

*CS 102 · Week 9 · Lab 9 Solutions · © CSE Department*
