# CS 201 · Week 0 · Reading Guide
## CS:APP Chapter 1, and How to Read It

---

**Set reading:** Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed., **Chapter 1** (§1.1–1.10).
**Optional:** Patterson & Hennessy, *Computer Organization and Design (RISC-V)*, **Chapter 1**.

**Read Chapter 1 in full before Week 1.** It is the only chapter of CS:APP that is a tour rather than a subject, and it is worth reading once quickly and once slowly.

---

## Why This Chapter Is Different

CS:APP Chapter 1 does something unusual: it follows a single `hello.c` program from source text through preprocessing, compilation, assembly, linking, loading and execution — and uses that one thread to name every topic the remaining eleven chapters cover.

**So it will feel like it is not teaching you anything.** It is teaching you the map. Come back to it in Week 12 and it reads completely differently.

---

## Section by Section

| § | Pages | What to take from it |
|---|---|---|
| **1.1** | Information is bits + context | The chapter's thesis. The same bytes are an integer, an instruction, or a character depending only on how they are read |
| **1.2** | The compilation system | The four stages: preprocess, compile, assemble, link. Lab 0 puts you inside stage 2's output |
| **1.3** | Why you should care | Read this properly. It is the best short argument for the course that exists |
| **1.4** | Processors read instructions | The von Neumann machine — this is Lecture 2 |
| **1.5** | Caches matter | Skim. Week 4 does it properly, but note the numbers |
| **1.6** | The memory hierarchy | Same. Lecture 3 §3 measured the real ones on the lab machine |
| **1.7** | The OS manages hardware | Processes, threads, virtual memory, files — this is PROG 201 and CS 202 in one page |
| **1.8** | Networks | Week 8 |
| **1.9** | **Concurrency and Amdahl's Law** | **Read carefully.** This is Lecture 3's power wall from CS:APP's angle |
| **1.10** | Abstractions | Lecture 1's hierarchy, stated by the authors |

---

## Questions to Read Against

Do not write answers up — these are for reading with a purpose. Several reappear in PS 0 and in Week 1.

**On §1.1**

1. The book says information is "bits + context". Give an eight-byte sequence and two different, both-sensible interpretations of it.
2. Why does the same byte value mean something different in a text file and in the `.text` section of an executable?

**On §1.2**

3. Name the four stages of compilation and the file each one produces. Which stage does `gcc -S` stop after? Which does `gcc -c` stop after?
4. Lab 0 uses `objdump` on the *linked* binary. Which stages have already run by then?

**On §1.4**

5. The book lists the CPU's components: PC, register file, ALU, main memory. Map each onto the diagram in Lecture 2 §1.
6. §1.4.2 traces `hello` running. At which point does the *program's* first instruction execute, as opposed to the shell's or the loader's?

**On §1.5–1.6**

7. The book gives cache access times in cycles. Compare them with the measured geometry in Lecture 3 §3. Do the *sizes* match the lab machine? Do the *ratios* between levels?
8. Why does the hierarchy have several levels rather than exactly two — fast and slow?

**On §1.9 — the important one**

9. State Amdahl's Law. If 90% of a program parallelises perfectly, what is the *maximum* speedup on infinite cores?
10. Lecture 3 argued that free performance ended around 2005. How does Amdahl's Law constrain the multi-core answer to that?

> **Question 9 has a number for an answer, and it is smaller than most people guess.** Work it out
> before Week 1; it reframes everything in Weeks 10 and 11.

---

## Reading Against the Machine

CS:APP's numbers are from the authors' hardware, not yours. **Check two of them.** This takes five minutes and is a better use of the time than re-reading a paragraph.

```bash
# Cache sizes, ways, and line size on the machine in front of you
lscpu -C

# Cores, threads, and clock range
lscpu | grep -E "Model name|^CPU\(s\)|Thread|Core|MHz"
```

On the lab machine these give 32 KB L1d per core / 256 KB L2 / 6 MB shared L3, 64-byte lines, four cores and eight threads at 1.6–3.4 GHz. **Compare with whatever the book says and note where it differs.** Getting into the habit of checking a textbook's numbers against the hardware you actually have is most of what "systems thinking" means in practice.

---

## Terminology You Should Own by Week 1

Not a definitions list to memorise — a checklist. If you cannot say what one of these is in a sentence, look it up before Week 1's lecture.

| | | |
|---|---|---|
| ISA | microarchitecture | abstraction layer |
| register | register file | program counter (`rip`) |
| ALU | condition flags | fetch–decode–execute |
| cache line | cache hit / miss | memory hierarchy |
| Moore's Law | Dennard scaling | the power wall |
| CISC / RISC | micro-op | variable-length encoding |
| little-endian | word size | stack frame |

---

## If You Want More

**Patterson & Hennessy Ch. 1** covers the same ground with RISC-V instead of x86-64. Reading both is genuinely useful: the contrast is what makes x86-64's irregularities visible *as* irregularities rather than as how computers simply are.

**Gordon Moore's 1965 paper**, *"Cramming more components onto integrated circuits"*, is four pages and entirely readable. Worth it to see how modest the original claim was.

**John Backus's 1977 Turing Award lecture** names the von Neumann bottleneck. Long and polemical; §1–2 are the part that matters.

---

*CS 201 · Week 0 · Reading Guide*
