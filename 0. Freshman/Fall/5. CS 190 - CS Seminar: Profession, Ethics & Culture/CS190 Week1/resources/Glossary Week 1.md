# Glossary — Week 1 Additions

Terms introduced this week. Added to the cumulative semester glossary.

---

**Turing Machine**
A formal mathematical model of computation (Turing, 1936) consisting of an infinite tape divided into cells, a read/write head, a finite set of internal states, and a transition function specifying what to do for each (state, tape symbol) pair. Serves as the formal definition of "algorithm" and "computation." Not a blueprint for a physical machine — a mathematical object for reasoning about what is and isn't computable.

**Universal Turing Machine (UTM)**
A Turing Machine that takes as input the encoded description of another Turing Machine M and an input string w, and simulates M's computation on w. The theoretical model for the stored-program computer: one machine that can simulate any other.

**Halting Problem**
The problem of determining, for an arbitrary Turing Machine M and input w, whether M will eventually halt (terminate) or run forever. Proved undecidable by Turing in 1936 via diagonalization — no algorithm can solve this for all possible (M, w) pairs.

**Stored-Program Architecture (Von Neumann Architecture)**
A computer design in which program instructions and data reside in the same memory, and the CPU fetches and executes instructions sequentially from that memory. Distinguished from earlier machines where the program was encoded in physical wiring or external connections. Described by Von Neumann in the 1945 EDVAC report; the basis of virtually all general-purpose computers built since.

**Transistor**
A solid-state semiconductor device that acts as an electrically controlled switch or amplifier. Invented at Bell Labs in 1947. Replaced the vacuum tube, enabling smaller, faster, more reliable, and less power-hungry digital circuits. The fundamental physical unit of all modern digital electronics.

**Moore's Law**
Gordon Moore's 1965 empirical observation that the number of transistors on an integrated circuit doubles approximately every two years. Held approximately for ~50 years; now significantly slowing due to physical limits at nanometer scales, driving architectural responses (parallelism, specialization).

**Compiler**
A program that translates source code in a higher-level language (e.g., C, Python) into machine instructions or lower-level code executable by a CPU. Grace Hopper developed the first in 1952. Embodies the principle that abstraction can be automated — the programmer thinks in high-level constructs; the compiler handles translation to hardware-level operations.

**Packet Switching**
A network communication method in which data is broken into discrete packets, each of which is independently routed through the network and reassembled at the destination. Contrasted with circuit switching (dedicated end-to-end connection for the duration of a session). The foundational architecture of ARPANET and the modern Internet.

**End-to-End Principle**
An architectural principle stating that application-specific functions (reliability, error correction, ordering) should be implemented at the endpoints of a communication system, not within the network core. The network's job is to move packets; intelligence lives at the edges. Formalized by Saltzer, Reed, and Clark (1984); explains many of the Internet's design choices.

**Entscheidungsproblem (Decision Problem)**
Hilbert's question: is there a general mechanical procedure to determine the truth or falsity of any mathematical statement? Turing proved in 1936 (along with Alonzo Church, independently) that no such procedure exists — there are mathematical statements whose truth cannot be mechanically decided.

**Integrated Circuit (IC)**
A semiconductor device on which multiple transistors and their interconnections are fabricated on a single chip of silicon. Independently developed by Kilby (Texas Instruments) and Noyce (Fairchild) in 1958–1959. Enabled the miniaturization and mass production that drove the rest of computing history.
