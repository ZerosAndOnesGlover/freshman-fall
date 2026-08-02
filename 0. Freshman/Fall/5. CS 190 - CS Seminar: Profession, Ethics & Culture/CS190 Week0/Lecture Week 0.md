# Lecture Week 0: What is Computer Science?
### Careers in CS, Software, and Hardware Engineering

---

## 1. The Question Nobody Asks You Before You Enroll

You almost certainly chose "Computer Science" as a major without anyone ever rigorously defining the term for you. That's not a criticism, it's a structural problem. The phrase "computer science" is a historical accident, and the field it names has split into at least three distinguishable disciplines that get casually lumped together. Before you spend four years inside this field, it's worth fifty minutes understanding what you actually signed up for.

### 1.1 Why the Name Is Misleading

Computer science is not, primarily, the science *of* computers, in the way that biology is the science of living things or chemistry is the science of matter. Computers are the instrument, not the subject. The actual subject is **computation**: the abstract study of what can be calculated, how efficiently, and by what means. You could do almost all of theoretical computer science with no computer in the room at all, the way Turing did in 1936, a full decade before a working stored-program electronic computer existed.

Edsger Dijkstra, one of the field's founding figures, put it memorably: "Computer science is no more about computers than astronomy is about telescopes." The telescope is the tool that lets you observe the stars; the computer is the tool that lets you observe computation. Neither tool *is* the discipline.

This matters for you practically: it tells you that the deep skills you're building in CS 101 (decomposition, abstraction, algorithmic thinking, proof) are not "programming skills" that will expire when today's languages and frameworks are replaced. They are modes of thought that transfer across every tool you'll ever use.

---

## 2. Three Disciplines Wearing One Name

In casual conversation, "computer science," "software engineering," and "computer engineering" get used almost interchangeably. They shouldn't be. Each is a genuinely different intellectual tradition, asking a different central question, even though all three overlap heavily in practice and a working professional typically draws on all three.

### 2.1 Computer Science: "What is computable, and how efficiently?"

Computer science, in its purest form, is a branch of mathematics. Its central objects are formal: languages, automata, algorithms, proofs. Its central questions:

- What problems can be solved by *any* computational process at all (computability)?
- For problems that can be solved, what is the minimum cost — in time, space, or other resources — to solve them (complexity)?
- How do you prove a given algorithm is correct, and how do you prove it cannot be made faster?

A pure computer scientist could spend a career never writing a line of production code, working entirely in proofs about Turing machines, complexity classes, and formal languages — the territory you'll meet formally in CS 301 (Theory of Computation) and touch in CS 101 Week 11.

### 2.2 Software Engineering: "How do you build software that works, at scale, reliably, with other people?"

Software engineering takes computability and algorithms as a *given*. It assumes you already know how to write a correct sorting function, and asks an entirely different set of questions:

- How do you design a system whose requirements will change after you ship it?
- How do you coordinate fifty engineers modifying the same codebase without it collapsing into chaos?
- How do you know a system is correct when you cannot test every possible input?
- How do you build something that survives the original author leaving the company?

This is an engineering discipline in the structural-engineering sense, not the mathematical sense: it's about managing complexity, risk, and human coordination under real-world constraints (deadlines, budgets, legacy systems, imperfect requirements). PROG 101, PROG 102, and especially CS 212 (Software Engineering) in Year 2 live here. So does almost the entirety of the `M.S. Software Engineering` curriculum if you continue to graduate study; the discipline of building systems that remain correct, maintainable, and evolvable over years.

### 2.3 Computer Engineering: "How do you build the machine that runs the computation?"

Computer engineering descends from electrical engineering. Its central question: how do you physically realize computation in silicon, in circuits, in the interaction between hardware and the lowest layers of software?

- How do logic gates compose into an arithmetic logic unit?
- How does a CPU pipeline instructions to execute more than one per clock cycle?
- How do you design a memory hierarchy that makes a slow, cheap, large memory *behave* like a fast, expensive, small one?

`ECE 110 (Digital Logic)` this year, and `CS 201 (Computer Organization & Architecture)` next year, are your entry points here. A computer engineer cares about things a pure computer scientist can safely ignore: voltage, heat dissipation, transistor count, clock skew.

### 2.4 Why the Boundaries Blur in Practice

Almost no working professional sits in exactly one of these three boxes. A back-end engineer at a tech company writes software (SE), but needs to reason about algorithmic complexity when choosing a data structure (CS), and increasingly needs to understand cache behavior and memory layout to write fast code (CE-adjacent, as you saw in CS 101's discussion of structure-of-arrays vs array-of-structures performance). The CSE degree you're pursuing is explicitly designed to give you fluency across all three, because the boundaries are porous in real engineering work.

| | Central Question | Core Tools | Where You'll Meet It |
| --- | --- | --- | --- |
| **Computer Science** | What is computable, and at what cost? | Proofs, automata, asymptotic analysis | CS 101, CS 102, CS 301 |
| **Software Engineering** | How do you build correct, maintainable systems at scale? | Design patterns, testing, version control, process | PROG 101/102, CS 212 |
| **Computer Engineering** | How do you physically realize computation? | Logic design, architecture, signal processing | ECE 110, CS 201 |

---

## 3. The Career Landscape: What Does a CSE Graduate Actually Become?

Part of why CS 190 exists is that the career landscape downstream of a CSE degree is far wider than most incoming students realize. "Software engineer at a tech company" is the default mental image, but it's one career path among many, and it's worth seeing the others now, partly so your later course selections (especially electives in Year 3 and 4) are informed choices rather than defaults.

### 3.1 Software Engineering Roles

The largest employment category. Sub-specializations include back-end (servers, databases, APIs), front-end (user interfaces), full-stack, mobile, infrastructure/platform engineering, and embedded software. The unifying skill: translating requirements into correct, maintainable code, usually within a team and a codebase that outlives any individual contributor.

### 3.2 Systems & Infrastructure Engineering

Building the substrate other software runs on: operating systems, databases, distributed systems, networking stacks, compilers. Demands deep CS 201/202/211/321 -style knowledge. Often the highest-leverage, most technically demanding roles — and the ones where a shaky understanding of computer architecture or OS internals shows up immediately as production incidents.

### 3.3 Data Science, Machine Learning, and AI Engineering

Sits at the intersection of CS, statistics (MATH 251), and linear algebra (MATH 241). Two distinct sub-roles worth separating: **ML researchers** (push the boundary of what models can do, often PhD-track) and **ML/AI engineers** (deploy, scale, and maintain ML systems in production — closer to software engineering with a statistics specialization).

### 3.4 Security Engineering

Adversarial by nature, you'll meet this properly in CS 341 (Year 3). Security engineers think like attackers to build defenses: penetration testing, vulnerability research, secure system design, incident response. Demands deep systems knowledge (CS 201, PROG 201) plus a specific adversarial mindset that most coursework doesn't naturally teach.

### 3.5 Hardware & Embedded Systems Engineering

Closer to the Computer Engineering tradition: designing chips, embedded firmware, robotics control systems, IoT devices. Demands ECE 110, CS 201, and often a physics/EE-heavy elective path.

### 3.6 Engineering Management & Technical Leadership

Not a separate skill set bolted onto engineering but a continuation of it. Staff engineers, principal engineers, and engineering managers still need deep technical judgment; what changes is the scope of what they're responsible for (a team's output and a system's evolution, not just their own code). This path is explored in depth at the graduate level (see the M.S. Software Engineering curriculum, especially SE 506).

### 3.7 Research (Academic or Industrial)

For students drawn to the "what is computable" questions of pure CS, a research career, typically requiring graduate study, pushes the boundary of the field itself rather than applying it. Industrial research labs (at large tech companies) and academic institutions both hire here, usually requiring a PhD.

### 3.8 Entrepreneurship / Technical Founder

The CSE skill set is also the foundation for building and launching your own products. This path trades depth-in-one-area for breadth-across-everything: you'll touch architecture, product, infrastructure, and business simultaneously.

---

## 4. Why Does a Technical Curriculum Need an Ethics Seminar?

This is worth answering directly, because skepticism about this course is common and reasonable. Here's the case for CS 190.

### 4.1 The Argument From Consequence

Software is no longer a niche technical artifact, it is infrastructure for human decision-making at civilizational scale. Algorithms now influence who gets a loan, who gets released on bail, who sees what news, who gets hired, what content a billion people see on any given day. The engineers who build these systems make consequential decisions; sometimes explicitly, sometimes by default, sometimes by simply not thinking about a trade-off at all. "I just wrote the code" is not a defense available to an engineer whose code determines real outcomes for real people.

### 4.2 The Argument From Technical Neutrality Being a Myth

A common reflex is: "I just build the tool; how it's used isn't my responsibility." This claim doesn't survive contact with how engineering decisions actually work. Every non-trivial system embeds choices: what data to collect, what to optimize for, what edge cases to handle, what failure modes to tolerate; and those choices are not value-neutral. A recommendation algorithm optimized purely for engagement *will* tend toward addictive and polarizing content, not because anyone wrote a line of code that said "polarize the users," but because that's what the optimization target produces as an emergent consequence. Understanding this is itself a technical skill, not just a moral one, and it's a skill this seminar exists to build.

### 4.3 The Argument From Professional Identity

Engineering disciplines that came before computing: civil, mechanical, aerospace; all developed codes of professional ethics and licensure specifically because their failures kill people, and the profession needed mechanisms to internalize that responsibility. Computer science is a younger field, and its norms are still being established in real time, partly through bodies like the ACM (whose Code of Ethics you'll read this semester) and partly through hard lessons from real incidents (which you'll study across the semester: algorithmic bias cases, surveillance controversies, security failures).

### 4.4 The Argument From Self-Interest

Practically: understanding the ethical and societal dimensions of your work makes you a better engineer, not a distracted one. Engineers who think about failure modes, edge cases, and unintended consequences write more robust systems. The habit of asking "what could go wrong, and for whom?" is the same habit that makes you good at writing test cases and reasoning about loop invariants. This seminar is training a muscle you will use constantly, including in purely technical contexts.

---

## 5. Looking Ahead: The Shape of the Semester

This week sets the frame. Over the coming weeks, CS 190 will move from history (Week 1: Babbage to Turing to Silicon Valley) through process (Week 2: how software actually gets built) into the substantive ethical content: the ACM Code of Ethics (Week 3, where position papers begin), algorithmic bias (Week 4), privacy and surveillance (Week 5), AI and society (Week 6), intellectual property (Week 7), cybersecurity ethics (Week 8), industry culture (Week 9), the future of work (Week 10), before culminating in student presentations and a guest speaker.

Each week builds on a shared vocabulary and set of frameworks established here in Week 0. Come to Week 1 having actually done the reading, this seminar only works if everyone has something to say.

---

## 6. Key Terms Introduced This Week

See [[Glossary]] for full definitions. New terms: *computability*, *computer science / software engineering / computer engineering* (as distinct disciplines), *technical neutrality (myth of)*, *professional ethics / code of ethics*, *emergent consequence*.
