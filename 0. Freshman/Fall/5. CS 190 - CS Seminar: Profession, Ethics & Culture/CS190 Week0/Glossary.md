# Glossary: Week 0

Precise definitions of terms introduced this week. CS 190 will build a cumulative glossary across the semester; this is the first installment.

---

**Computability**
The study of which problems can, in principle, be solved by *any* mechanical/algorithmic process at all, independent of how much time or memory is available. A problem can be "incomputable" even if we had infinite time to work on it; the Halting Problem (which you'll meet formally in CS 101 Week 11 and rigorously in CS 301) is the canonical example.

**Computer Science**
The formal/mathematical study of computation: what is computable, at what cost (complexity), and how do we prove algorithms correct. Distinguished in this course from Software Engineering and Computer Engineering as a matter of *central question*, not job title.

**Software Engineering**
The engineering discipline concerned with building correct, maintainable, scalable software systems, especially under real-world constraints: changing requirements, team coordination, legacy code, imperfect specifications. Takes computability and algorithms as a given and asks how to build reliable systems on top of them.

**Computer Engineering**
The engineering discipline concerned with the physical realization of computation: logic circuits, processor architecture, memory systems, the hardware/software boundary. Descends from electrical engineering.

**Technical Neutrality (Myth of)**
The claim, addressed critically in this week's lecture, that a technical artifact (an algorithm, a system, a tool) is inherently free of values or political consequence, and that responsibility for its effects lies entirely with whoever uses it rather than partly with whoever designed it. This course takes the position that this claim does not survive scrutiny: design choices (what to optimize for, what data to collect, what edge cases to handle) embed values whether or not the engineer intended them to.

**Emergent Consequence**
An outcome of a system that was not explicitly programmed or intended by any individual design decision, but arises from the interaction of the system's components and its optimization target with the real world. Example discussed in lecture: an engagement-maximizing recommendation algorithm tending toward polarizing content, without any line of code that says to do so.

**Professional Ethics / Code of Ethics**
A codified set of professional obligations and conduct standards adopted by a discipline's professional body (e.g., the ACM Code of Ethics and Professional Conduct, which CS 190 reads in full in Week 3). Distinguished from personal ethics by being a *shared, institutional* standard rather than an individual's private values.

**ACM**
Association for Computing Machinery — the largest professional and educational society for computing, founded 1947. Publishes the Code of Ethics this course reads in Week 3, among many other standards and curricular guidelines (including the Computing Curricula reports referenced in this week's reading).

**Turing Machine**
A formal mathematical model of computation introduced by Alan Turing in 1936, consisting of an infinite tape, a read/write head, and a finite set of states and transition rules. Referenced this week as the historical anchor for the claim that computer science predates the existence of physical computers by roughly a decade. Studied formally in CS 101 Week 0 and rigorously in CS 301.

---

*This glossary will grow each week. Terms introduced in later weeks build on these definitions — review them periodically rather than treating them as one-time reading.*
