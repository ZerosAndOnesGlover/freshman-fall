# CS 202 · Midterm 2 — Revision Guide

**Monday of Week 8, 18:00–19:15, VNC 100 · 75 minutes · 100 marks · 12.5% of the course**
**Covers Weeks 4–7.** Nothing from Week 8 is on the paper.

---

## What the Paper Looks Like

**Five questions of 20 marks, all compulsory.** One question per theme, four parts each — so **a part you cannot do costs 4–6 marks, not 20.**

| Q | Theme | Weeks |
|---|---|---|
| 1 | Deadlock: conditions, the Banker's algorithm, detection, livelock | 4 |
| 2 | Address translation: page tables, the TLB, shootdowns | 5 |
| 3 | Demand paging, copy-on-write, and page faults | 5 |
| 4 | Page replacement, working sets, thrashing, the OOM killer | 6 |
| 5 | File systems: inodes, the page cache, durability, layout | 7 |

**One handwritten sheet of A4, one side.** No calculators — **the arithmetic is designed to be done by hand**, and every number you need is either given or small.

---

## What to Practise, With Where It Is Worked

**These are the calculations the paper asks for. Do each one at least once before Monday.**

| Calculation | Practise on | Worked in |
|---|---|---|
| **Need = Max − Allocation, and a safe sequence** | PS 4 Q1, `states/textbook.txt` | L14 §4 |
| **Grant or refuse a request** — pretend, test safety, roll back | PS 4 Q1(b) | L14 §4, PS 4 solutions |
| **Detection with several instances**, and the "holds nothing" rule | PS 4 Q2 | L15 §1 |
| **Split an address** into xv6's 10/10/12 and x86-64's 9/9/9/9/12 | L16 Exercise 1 | L16 §4, §6 |
| **Page-table memory** for a layout: how many PTE/PMD pages | PS 5 Q2(c) | L16 §7 |
| **TLB reach and effective access time** | PS 5 Q3, L17 Exercise 1 | L17 §2–§3 |
| **Count page faults** for a read-then-write pattern | Lab 5 Q5 | L18 §1, §3 |
| **`fork` and copy-on-write costs**, Linux against xv6 | L18 §4–§5 | L18 §4 |
| **Decode a page-fault error code** (present / write / user) | L18 §2 | L18 §2 |
| **FIFO, LRU, OPT on a short reference string** | PS 6 Q1, `traces/textbook.txt` | L20 §1–§4 |
| **Belady's anomaly**: show it, and say why LRU cannot | PS 6 Q2 | L20 §2 |
| **Working set from a fault curve; thrashing** | PS 6 Q3, L21 §2 | L21 §1–§2 |
| **OOM badness: compare two processes** | Lab 6 Q8 | L21 §5 |
| **Inode arithmetic**: largest file, blocks for a size, reads for a path | PS 7 Q2, Q5 | L22 §3, §7 |
| **Cold against warm reads; readahead** | Lab 7 Q2–Q4 | L23 §1–§2 |
| **Durability arithmetic**: writes per second with and without `fsync` | Lab 7 Q7 | L23 §4 |

---

## The Numbers Worth Knowing Cold

You will not be asked to recall a measurement, **but the arithmetic is quicker if you know the shape of the answers**:

| | |
|---|---|
| TLB hit / L3 hit / **major fault** | ~1 ns / ~8 ns / **~90 µs** |
| demand-zero fault / copy-on-write fault | 1.9 µs / 2.7 µs |
| 4 KiB write: buffered / with `fsync` | **2.9 µs / ~3,900 µs** |
| a page table entry covers | 4 KiB; a PMD page covers 1 GiB |
| xv6: largest file / fork of a 4 MiB process | **71,680 bytes** / 1,096 pages |
| xv6 kernel mapping, per process | 65 pages |

---

## How to Prepare, in Order

1. **Rework PS 4 Q1 and PS 6 Q1 by hand**, without the programs. They are the two mechanical questions on the paper, and both are quick once the table is laid out correctly.
2. **Re-read the four "What to Take Away" lists** for L14, L17, L18 and L23. They are the examinable claims, stated as sentences.
3. **Redo your own lab answers** for Lab 5 Q4 and Lab 6 Q8 — those measurements are the ones students misremember.
4. **Write your sheet last**, from the table above: the formulas you cannot re-derive under time, and the four or five numbers you keep looking up.

---

## What Belongs on Your One Sheet

**Formulas you would waste minutes re-deriving:**

- Need = Max − Allocation; the safety-check loop in four lines.
- The detection algorithm's two differences from the safety check.
- x86-64 address fields, and the size each level covers.
- Effective access time with a hit rate.
- Badness: memory share plus `oom_score_adj`, and the direction.
- Largest file for *d* direct + one indirect; blocks for a size.
- The safe-update sequence: write, `fsync`, `rename`, `fsync` the directory.

**What does not belong:** anything you can derive in ten seconds, and long prose — **the sheet is for arithmetic, and the marks are for explanation.**

---

## In the Room

- **Answer the part you know first.** Every question has an easy part and a harder one; they are worth similar marks.
- **Show the intermediate table.** For the Banker, the replacement string and the inode arithmetic, **the working carries most of the marks** — a wrong final number with a right table loses little.
- **State your assumption and continue** if a question seems to need something you were not given. That earns the marks; a blank does not.
- **75 minutes, 100 marks**: about 14 minutes per question, with five left over.

---

*CS 202 · Week 8 · Midterm 2 Revision Guide · © CSE Department*
