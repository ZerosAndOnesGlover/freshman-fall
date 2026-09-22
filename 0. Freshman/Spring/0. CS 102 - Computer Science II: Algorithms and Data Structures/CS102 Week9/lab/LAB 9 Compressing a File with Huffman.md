# CS 102 · Lab 9
## Compressing a File with Huffman

**Date:** Tuesday 30 March 2027 · 15:00–16:50 · Lab section (Week 10) — covers Week 9 (L28–L30)
*2-hour lab · 40 points · in-lab checkoff*
**Deliverable:** `lab9.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 13 labs to pass the course.** See the syllabus.
> **PROJECT 1 is due Friday of this week.**

---

## Purpose

Lecture 30 proved Huffman optimal. This lab builds a real codec — bits packed into bytes, a code table
that has to be stored, a round trip that must be lossless — and then measures what it actually
achieves.

The measurements include three that the theory does not prepare you for: **`gzip` beats it by 2×**,
**a short file gets bigger**, and **random data does not compress at all**. Each has a one-sentence
explanation, and finding them is Part D.

---

## Part A — The Codec (14 pts)

**A1.** *(4)* `build_corpus(n=200000, seed=42)` exactly as specified, so your figures are comparable:

- word list, in this order: `the of and to a in is it you that he was for on are as with his they I
  at be this have from or one had by word`
- weights $3/(i+1)$ for the $i$-th word, 0-indexed;
- `random.seed(seed)` once, then repeatedly `random.choices(words, weights=w)[0]`, accumulating
  `len(word) + 1` per pick until the total reaches `n`;
- join with single spaces and truncate to exactly `n` characters.

Report the length and the number of distinct symbols.

**A2.** *(5)* `huffman_codes(freq)` using `heapq`, returning a dict from symbol to code string.
Handle the **single-symbol** case (assign it `'0'`).

**A3.** *(5)* `encode(text, code)` returning `(bytes, padding_bits)`, and `decode(data, pad, code)`.

The bits must be **packed into bytes**, not stored as a string of `'0'` and `'1'`.

Verify a lossless round trip on the corpus **and** on: the empty string, a single character, and a
string of one repeated character.

---

## Part B — Measure It (10 pts)

**B1.** *(4)* For the corpus, report: raw bytes, encoded bytes, compression ratio, and space saved as
a percentage.

**B2.** *(3)* Report the **entropy** of the character distribution and Huffman's **average code
length**, both in bits per character. Give the overhead.

**B3.** *(3)* Report the six most frequent symbols with their counts and code lengths, plus the longest
and shortest code lengths.

Confirm the ordering is what the algorithm promises, in one sentence.

---

## Part C — The Code Table (6 pts)

**C1.** *(3)* A decoder cannot invent the code. Design a minimal table format, state its size in bytes
for your corpus, and report the compression ratio **including** the table.

**C2.** *(3)* Now compress a **short** string — `"hello world"` will do. Report the payload size, the
table size, and the total.

State the net change in bytes, and the general condition under which Huffman makes a file **larger**.

---

## Part D — Three Uncomfortable Measurements (10 pts)

**D1.** *(4)* Compress the corpus with `zlib.compress(data, 9)` and compare with your Huffman output.

`zlib` implements DEFLATE, which is **LZ77 followed by Huffman**. Report both sizes and the ratio
between them, and explain in two sentences **what LZ77 sees that Huffman cannot**.

**D2.** *(3)* Generate 50,000 uniformly random symbols over a 256-symbol alphabet and compress them.

Report the entropy, Huffman's average length, and the ratio. Explain the result in one sentence.

**D3.** *(3)* Your Part B result is within a few hundredths of a bit of the entropy floor, and
Lecture 30 showed a case where Huffman uses **12× the entropy**.

State what is different about that case, and what the fix is called.

---

## Submission

- `lab9.py` — runnable end to end, producing every figure.
- `RESULTS.md` — all tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 14 | A correct codec with real bit packing |
| B | 10 | Measuring compression and the entropy gap |
| C | 6 | The table, and when compression backfires |
| D | 10 | Three results the theory does not predict |
| **Total** | **40** | |

---

## Reference Numbers

`build_corpus(200000, 42)`, Python 3.14 on x86-64 Linux. **All deterministic** — if your generator
follows A1, these should match exactly.

**A1 / B1**

| quantity | value |
| --- | --- |
| corpus length | 200,000 characters |
| distinct symbols | **19** |
| round trip lossless | yes |
| encoded payload | **86,136 bytes** (padding 0 bits) |
| compression ratio | **2.322×** |
| space saved | **56.9%** |

**B2**

| quantity | bits/char |
| --- | --- |
| raw | 8.0000 |
| fixed-length $\lceil\log_2 19\rceil$ | 5.0000 |
| **Huffman** | **3.4454** |
| **entropy floor** | **3.4161** |
| overhead | **0.0293** |

**B3**

| symbol | count | code length |
| --- | --- | --- |
| space | 55,960 | **2** |
| `t` | 24,656 | 3 |
| `h` | 20,606 | 3 |
| `e` | 18,674 | 3 |
| `o` | 16,271 | 4 |
| `a` | 13,573 | 4 |

Longest code **9** bits, shortest **2** bits.

**C1** — a naive table of (symbol byte, code-length byte) per symbol is **38 bytes**; total 86,174
bytes, ratio **2.321×**.

**C2** — `"hello world"`: 11 bytes in, **4 bytes** payload + **16 bytes** table = 20 bytes.
**Net change +9 bytes.**

**D1**

| method | size | ratio |
| --- | --- | --- |
| Huffman alone | 86,136 bytes | 2.32× |
| `zlib` level 9 | **44,208 bytes** | **4.52×** |

`zlib` is **1.95×** smaller.

**D2** — 50,000 uniform random symbols over 256: entropy **7.9965** bits, Huffman **8.0000** bits,
ratio **1.0000×**.

---

## A Note on What This Lab Is Really Testing

Part B is the good news, and it is genuinely good: Huffman lands **0.029 bits per character** above
the entropy floor — an overhead of under 1%, far better than the guaranteed "+1". The algorithm found
that assignment knowing nothing about English.

**Part D is the calibration.**

`zlib` is nearly twice as good, and not because its Huffman is better — it uses the same algorithm.
It wins because **LZ77 runs first and replaces repeated word occurrences with back-references**.
Huffman treats characters as independent and cannot see that `the` appears fifty thousand times; it
can only give `t`, `h` and `e` short codes. **An optimal algorithm for the wrong model loses to a
decent algorithm for the right one**, and that sentence is worth more than the compression ratio.

Random data does not compress, and cannot: if it did, some other input would have to get longer —
there is no injection from $2^n$ strings into fewer than $2^n$ strings. **Compression is not a
property of an algorithm; it is a bet about the input distribution.**

And the eleven-byte file got bigger. Every real format has a threshold below which it stores data
uncompressed, and knowing why is the difference between using a library and understanding it.

---

*CS 102 · Week 9 · Lab 9 · © CSE Department*
