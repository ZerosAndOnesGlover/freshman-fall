# CS 190 · CS Seminar: Profession, Ethics & Culture
## Lecture · Week 1: The History of Computing
### From Babbage to Turing to Silicon Valley

*“We may say most aptly that the Analytical Engine weaves algebraical patterns just as the Jacquard-loom weaves flowers and leaves.”* — Ada Lovelace, "Notes" on Menabrea's *Sketch of the Analytical Engine* (1843)

**Date:** Wednesday 30 September 2026 · 13:00–13:50 · Week 1

**Reading:** Turing, "Computing Machinery and Intelligence" (*Mind*, 1950) · Abbate, *Inventing the Internet*, Ch. 1 · Isaacson, *The Innovators*, Ch. 1 ("Ada Lovelace") — [[CS190 Week1/resources/Reading Guide|Reading Guide]]

**Coursework:** 📝 **Prep 1** due today 12:00

---

## 1. Why History Matters in a Technical Discipline

Most engineering curricula treat history as decoration — a few names and dates before the "real" content starts. This seminar treats it differently. The history of computing is the history of *ideas*, and ideas have context. Understanding why a concept was invented, what problem it was trying to solve, and what it replaced tells you things about the concept that no formal definition can. You will understand what a Turing Machine *is* from CS 301. You will understand what it *means* from knowing what Turing was responding to.

There is also a more direct reason: the ethical and societal questions this seminar asks later in the semester — about bias, surveillance, automation, AI — are not new. Every one of them has a historical precursor. The more clearly you can see those earlier episodes, the better equipped you are to reason about the current ones.

---

## 2. The Mechanical Era: Before Electricity

### 2.1 Leibniz and Pascal — Arithmetic as Mechanism (1640s–1670s)

The first mechanical calculators were built to solve a specific, practical problem: arithmetic is tedious, error-prone, and necessary for taxation, navigation, and commerce. Blaise Pascal built the *Pascaline* (1642) to assist his father's tax work — it could add and subtract. Gottfried Wilhelm Leibniz extended this to multiplication and division with the *Stepped Reckoner* (1672).

The deeper insight from Leibniz — who was also a logician and philosopher — was more ambitious: if arithmetic could be mechanized, perhaps *reasoning itself* could be. He called this the *calculus ratiocinator*, a universal calculus of thought that could resolve any dispute by calculation. He didn't build it. The idea waited two centuries.

### 2.2 Charles Babbage and the Engines (1820s–1870s)

Charles Babbage is the figure who bridges mechanical arithmetic and the modern computer concept, though his machines were never completed in his lifetime.

The **Difference Engine** (designed 1822) was a specialized calculator for producing mathematical tables — critical for navigation, insurance, and engineering. Tables at the time were computed by human "computers" (the job title that gives us the word) and were riddled with errors. Babbage wanted to mechanize the process to eliminate mistakes.

The **Analytical Engine** (designed 1837) was something fundamentally different. It was not a specialized calculator — it was a *general-purpose* machine. It had what Babbage called a "mill" (arithmetic unit) and a "store" (memory), accepting input via punched cards (borrowed from Jacquard looms). It was, in modern terms, a mechanical computer with a CPU and RAM.

Two things make this historically important beyond the hardware:

1. **Ada Lovelace** (1843) wrote what is widely recognized as the first algorithm intended for a machine — a method to compute Bernoulli numbers on the Analytical Engine. She also wrote, more profoundly, that the Analytical Engine "has no power of originating anything. It can only do what we *know* how to order it to perform." This is the first articulation of the concept we now call the Church-Turing thesis's practical implication: the machine does exactly what it is instructed, nothing more. The question of whether modern AI has changed this is one you should carry through the semester.

2. The Analytical Engine was **general-purpose** — it was not built to solve one kind of problem. This distinction (special-purpose vs general-purpose) recurs throughout computing history and remains live in today's debates about GPUs, TPUs, and neuromorphic chips.

---

## 3. Logic Becomes Mathematics (1850s–1930s)

### 3.1 Boole and the Algebra of Thought (1854)

George Boole published *An Investigation of the Laws of Thought* in 1854, showing that logical reasoning could be formalized as an algebraic system — what we now call Boolean algebra. AND, OR, NOT as mathematical operations on 0 and 1. This was a step toward Leibniz's dream of mechanized reasoning, though Boole himself didn't connect it to physical machines.

Claude Shannon closed that gap in his 1937 master's thesis, showing that Boolean algebra and electronic relay circuits were the same thing. A circuit either conducts or doesn't — 1 or 0. AND, OR, NOT could be built from physical switches. This is the foundational insight of digital electronics: *logic is physical*.

### 3.2 Hilbert's Program and Its Destruction (1900–1931)

David Hilbert, the greatest mathematician of his era, posed in 1900 a program for mathematics: prove that all of mathematics is *consistent* (no contradictions), *complete* (every true statement is provable), and *decidable* (there exists a mechanical procedure to determine if any given statement is true). This was Leibniz's dream in rigorous form.

All three goals were destroyed within 31 years.

**Kurt Gödel** (1931) proved the Incompleteness Theorems: in any sufficiently expressive formal system, there are true statements that cannot be proven within that system (incompleteness), and the system cannot prove its own consistency. Mathematics is irreducibly incomplete.

**Alan Turing** (1936) addressed the decidability question. To even state "there is a mechanical procedure to decide X," you need a precise definition of "mechanical procedure." Turing provided one: the Turing Machine.

### 3.3 Turing and the Universal Machine (1936)

Alan Turing's paper "On Computable Numbers, with an Application to the Entscheidungsproblem" (1936) is the founding document of computer science. Its primary goal was to prove that Hilbert's *Entscheidungsproblem* (decision problem) had no solution — there is no general mechanical procedure to decide mathematical truth. But to prove this, Turing had to first define precisely what a "mechanical procedure" even was.

His answer was the **Turing Machine**: an abstract machine with an infinite tape, a read/write head, and a finite set of rules governing transitions between states. Simple enough to reason about mathematically; expressive enough to compute anything computable.

The critical contribution beyond this was the **Universal Turing Machine**: a Turing Machine that takes, as its input, a description of another Turing Machine plus that machine's input, and simulates it. This is the theoretical model of the stored-program computer — a machine that can be programmed to be any other machine. Every computer you will ever use is, in a mathematically precise sense, a physical Universal Turing Machine.

Turing then proved the **Halting Problem** is undecidable: no Turing Machine can determine, for all possible inputs, whether an arbitrary Turing Machine will halt or run forever. You will prove this yourself in CS 101 Week 11 and again more rigorously in CS 301. The proof is a diagonalization argument — beautiful, short, and devastating.

---

## 4. The First Machines (1940s)

### 4.1 Wartime Computation

World War II created urgent computational needs that accelerated the transition from theory to hardware.

**Colossus** (UK, 1943–1944): Built at Bletchley Park, where Turing worked, to assist in breaking Lorenz cipher messages from the German high command. Colossus was a special-purpose electronic machine — not a stored-program computer in the modern sense, but the first large-scale programmable electronic device.

**ENIAC** (US, 1945): The first general-purpose electronic digital computer in the sense of being fully Turing-complete and electronic (rather than electromechanical). Built at the University of Pennsylvania, ENIAC used 18,000 vacuum tubes, weighed 30 tons, and consumed 150 kilowatts. Programming it meant physically reconnecting wires and setting switches — it had no stored program.

### 4.2 Von Neumann and the Stored Program (1945)

John von Neumann's "First Draft of a Report on the EDVAC" (1945) — whether or not he deserves sole credit for the idea, a historical controversy — described what we now call the **Von Neumann architecture**: a machine with a processor, memory that holds both data *and* program instructions, and I/O. The stored program is the critical innovation: you can change what the machine does by changing what is in memory, not by rewiring it. This is the architecture of virtually every general-purpose computer built in the 80 years since.

---

## 5. The Transistor and the Semiconductor Era (1947–1970s)

### 5.1 The Transistor (1947)

The vacuum tube computers of the 1940s were large, hot, power-hungry, and unreliable — a single vacuum tube burned out on average every few hours, and ENIAC had 18,000 of them. The transistor, invented at Bell Labs by Bardeen, Brattain, and Shockley in 1947, replaced the vacuum tube with a solid-state semiconductor device. Smaller, faster, cooler, more reliable.

The transistor is the foundation of the entire modern semiconductor industry. Every chip you will encounter in this degree — from the CPU in your laptop to the GPU in a cloud server to the microcontroller in your mouse — is made of transistors. A modern CPU contains tens of billions of them.

### 5.2 The Integrated Circuit (1958–1959)

Jack Kilby (Texas Instruments) and Robert Noyce (Fairchild Semiconductor) independently developed the integrated circuit — placing multiple transistors and their connections on a single piece of semiconductor material. This made miniaturization and mass production possible.

### 5.3 Moore's Law (1965)

Gordon Moore, co-founder of Intel, observed in 1965 that the number of transistors on an integrated circuit was doubling roughly every two years, and predicted this would continue. It did — for about 50 years. Moore's Law is why your phone has more computing power than a room-sized machine from the 1980s. It is also why Moore's Law has now significantly slowed, which is driving the architectural innovations you'll study in CS 201 and ECE 311: specialized hardware (GPUs, TPUs), parallelism, and new chip architectures.

---

## 6. Software Emerges as a Discipline (1950s–1970s)

For the first decade of computing, hardware and software were barely distinguished. A computer was programmed by writing machine code — raw binary instructions for the CPU. This is still, ultimately, what every program becomes; but it's not how anyone above the hardware layer thinks about programming.

### 6.1 Assembly Language and Compilers

**Grace Hopper** (1952) developed the first compiler — a program that translates human-readable source code into machine instructions. This was genuinely controversial at the time; many engineers believed a machine could not translate code as efficiently as a human programmer. Hopper was proven right. The compiler is now so foundational it's invisible; you will use one daily for the rest of your career.

### 6.2 FORTRAN and the First High-Level Languages (1957)

John Backus led the team that created FORTRAN (FORmula TRANslation) at IBM — the first widely used high-level programming language. FORTRAN made scientific computing accessible to people who weren't machine-code programmers. The insight it represents: *abstraction as productivity*. You pay a small efficiency cost in some cases; you gain an enormous readability and maintainability advantage. This tradeoff recurs at every layer of the computing stack.

### 6.3 NATO Software Engineering Conference (1968)

By the late 1960s, large software projects were failing systematically — overbudget, late, incorrect, impossible to maintain. The NATO Science Committee convened a conference in 1968 where the term "software engineering" was coined deliberately, to signal that programming needed to become an engineering discipline with systematic methods, not an ad-hoc craft.

This is the founding moment of software engineering as a self-conscious discipline — and the problem it was responding to (large software systems failing) has never fully gone away, which is why CS 212 in Year 2 and the entire M.S. Software Engineering program exist.

### 6.4 Unix and C (1969–1973)

Ken Thompson and Dennis Ritchie at Bell Labs created Unix (1969) and the C programming language (1972) — two artifacts whose influence on computing is difficult to overstate. Unix established the design principles (everything is a file, small tools composable by pipes, processes as the unit of execution) that underlie Linux, macOS, and Android today. C gave programmers a language close enough to the hardware to be efficient, abstract enough to be portable — the language you are learning right now in PROG 101 is the same language Ritchie designed in 1972, with modest updates.

---

## 7. The Personal Computer Revolution (1970s–1980s)

Until the mid-1970s, computers were institutional — owned by universities, governments, and large corporations, operated by specialists. The personal computer changed who had access to computation.

**Apple II** (1977), **IBM PC** (1981), and the software that ran on them — spreadsheets (VisiCalc, later Lotus 1-2-3), word processors, early databases — moved computing from institutions to individuals. **Microsoft** built its early business on MS-DOS, the operating system for the IBM PC, and later **Windows** — making the operating system the primary interface layer between users and hardware.

**Xerox PARC** (1970s) deserves special mention: researchers there developed the graphical user interface, the mouse, object-oriented programming (Smalltalk), and Ethernet. Almost none of it was commercialized by Xerox; most of it was commercialized by Apple and others. The PARC story is one of computing's most-cited examples of the gap between invention and commercialization — a recurring theme in tech industry history.

---

## 8. The Internet and the Web (1969–1990s)

**ARPANET** (1969), the precursor to the Internet, was initially a US Department of Defense-funded research network. Its key architectural decision — packet switching, where messages are broken into independent packets routed independently across the network — was designed by Paul Baran partly with nuclear-attack resilience in mind. The end-to-end principle (intelligence at the edges, not the core) that you will study in CS 302 (Networks) emerged from this design tradition.

**TCP/IP** (Cerf and Kahn, 1974) provided the protocol suite that allowed diverse networks to interconnect — the "internet of networks" that gives the Internet its name.

**The World Wide Web** (Tim Berners-Lee, 1989–1991) was built at CERN as a document-sharing system for physicists. HTTP, HTML, and URLs were designed for academic hypertext, not for what the Web became. The gap between the Web's original design assumptions and its current use at civilizational scale is itself an ethical and engineering story worth understanding.

---

## 9. Silicon Valley as a Cultural Phenomenon (1970s–present)

"Silicon Valley" is both a physical place (the San Francisco Bay Area) and a cultural mode — a specific set of norms, incentives, and narratives about how technology should be developed and by whom.

Key features of Silicon Valley culture as it actually operates (not as it narrates itself):
- **Venture capital as the dominant funding model**, which selects for hyper-growth and rapid exit over long-term sustainability or public benefit.
- **"Move fast and break things"** (the Facebook internal motto, later quietly retired) as an operational philosophy — a view that iteration speed dominates caution, with externalities to be handled later.
- **Network effects and winner-take-all dynamics** — the tendency of technology markets to produce dominant platforms (one search engine, one social network, one ride-hailing app per market) rather than competitive markets.
- **The myth of the lone genius founder** — a narrative that distorts both how innovation actually works (it is almost always collaborative and evolutionary) and who gets credit and resources.

Understanding Silicon Valley's cultural dynamics is prerequisite for reasoning clearly about the ethical questions this seminar raises in Weeks 4–11. Many of the algorithmic bias cases, privacy controversies, and content moderation failures we will examine are not accidental technical failures — they are predictable products of a specific incentive structure.

---

## 10. Where This Leaves You

The arc from Babbage's gears to today's neural networks is not a story of inevitable progress — it is a story of human choices, constrained by physics, economics, war, and institutions, made by people who often did not foresee the consequences of what they built. Turing did not foresee the internet. Berners-Lee did not foresee social media. The designers of TCP/IP did not foresee spam, DDoS attacks, or BGP hijacking.

This is not a counsel of pessimism — it is a counsel of humility and foresight. You are entering a field that has a history of building things faster than it thinks through what those things will do. CS 190 exists to build the habit of thinking a step ahead.

---

## Key Figures Timeline

| Year | Person / Event | Significance |
| --- | --- | --- |
| 1642 | Pascal — Pascaline | First mechanical calculator |
| 1837 | Babbage — Analytical Engine | First general-purpose computer concept |
| 1843 | Lovelace — First algorithm | Algorithm as distinct from machine |
| 1854 | Boole — Laws of Thought | Logic as algebra |
| 1931 | Gödel — Incompleteness Theorems | Mathematics is irreducibly incomplete |
| 1936 | Turing — Computable Numbers | Definition of computation; Halting Problem |
| 1945 | Von Neumann — EDVAC report | Stored-program architecture |
| 1947 | Bardeen, Brattain, Shockley — Transistor | Foundation of semiconductor industry |
| 1952 | Hopper — First compiler | Abstraction layer above machine code |
| 1957 | Backus — FORTRAN | First widely used high-level language |
| 1965 | Moore's Law | Transistor density doubling ~every 2 years |
| 1968 | NATO SE Conference | "Software engineering" as discipline coined |
| 1969 | Thompson & Ritchie — Unix | Foundational OS design |
| 1969 | ARPANET | Precursor to the Internet |
| 1972 | Ritchie — C | Language still in active use today |
| 1989 | Berners-Lee — WWW | Hypertext as global infrastructure |
