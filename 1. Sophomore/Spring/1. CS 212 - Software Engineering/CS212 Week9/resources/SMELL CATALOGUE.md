# CS 212 · Code Smells — Working Reference
## Fowler's catalogue, with where each one lives in `roomsvc`

---

> **A smell is a cheap, fallible signal that says *look here*.** Same epistemic shape as coverage
> (W6) and linter findings (W7), and the same failure mode — **treating a signal as a verdict.**
>
> **Three steps, always:** notice it; ask what it indicates *in this code, for the change you are
> making*; decide whether it is worth fixing **now**.

---

## The nine that account for `roomsvc`

| Smell | Symptom | In `roomsvc` | Refactoring |
|---|---|---|---|
| **Divergent Change** | One module changes for many unrelated reasons | **`bookings.py`: five actors, 891 of 2,173 file-touches in two years** | Split Phase; Move Function |
| **Shotgun Surgery** | One change touches many modules | Adding a booking kind touches **four** files; `7b1e4f2` missed one for eight months | Move Function; Combine Functions into Class |
| **Long Function** | It does not fit on a screen | `confirm_booking`, 487 lines, complexity 94 | Extract Function — **but it is a symptom; see below** |
| **Duplicated Code** | The same knowledge in several places | `range(8, 20)` in **four** places, three updated in 2023 | Extract Function — **after W2 L09 §1's test** |
| **Primitive Obsession** | Domain concepts as strings and numbers | `state` as `String(20)` with no constraint; `slot` as a naked `datetime` | Replace Primitive with Object; Replace Type Code with Subclasses |
| **Mysterious Name** | You cannot tell what it is | `_entry`, `s`, `do_it`, `process2` | **Rename** — cheapest refactoring, most under-used |
| **Feature Envy** | A function more interested in another object's data than its own | `reports.py` computing from `Booking`'s fields what `Booking` should know | Move Function |
| **Message Chains** | `a.b.c.d.e` | `booking.resource.building.campus.timezone` | Hide Delegate; Extract Function |
| **Speculative Generality** | Machinery for a need that never arrived | **`roomsvc/plugins/`: 380 lines, 31 commits, zero plugins** | **Remove Dead Code** |

---

## The two that get mis-ranked

**Divergent Change is the most serious and the least visible.** A file with five reasons to change
does not look ugly — it looks big. **Its damage shows up only in the `git log`, and it is the only
smell here that no linter can ever detect.** It is why a VAT change shipped a permission regression.

**Speculative Generality is the easiest to fix and the hardest to agree to.** Deleting 380 lines that
took someone a week feels wasteful. **The waste already happened; keeping it means paying forever** —
31 commits of maintenance, a node in every dependency graph, two days lost on a Python upgrade.
**Deletion is a refactoring, and nobody chooses it.**

---

## Long Function is a symptom

Extract nine functions from `confirm_booking` and **every real problem survives**: VAT in a file about
booking rules, email untestable without SMTP, the calendar POST inside the transaction.

**The right first move is Split Phase:**

| Stage | Property |
|---|---|
| **Decide** | Pure. No I/O. Testable in microseconds |
| **Act** | One transaction, one invariant, nothing else in the critical section |
| **Announce** | **After the commit.** Retriable, and cannot undo the booking |

**Nobody counts lines.** Split along *what changes for whom* (Week 2), and the line count falls out.

---

## The rest of the catalogue, briefly

| Smell | One-line cure |
|---|---|
| **Mutable Data** | Encapsulate Variable; make it a value object |
| **Global Data** | Encapsulate Variable. *(`roomsvc`'s `SETTINGS`, mutated in three places)* |
| **Long Parameter List** | Introduce Parameter Object; Preserve Whole Object |
| **Data Clumps** | Extract Class — **the same three fields travelling together everywhere** |
| **Repeated Switches** | Replace Conditional with Polymorphism *(the pricing tree — A 2)* |
| **Loops** | Replace Loop with Pipeline |
| **Lazy Element** | Inline Function / Class — **a class that does nothing** |
| **Temporary Field** | Extract Class; Introduce Special Case |
| **Refused Bequest** | Replace Subclass with Delegate *(the `Equipment.book` Liskov violation — W2 L08 §3)* |
| **Insider Trading** | Move Function; Hide Delegate |
| **Large Class** | Extract Class; Extract Superclass |
| **Alternative Classes with Different Interfaces** | Change Function Declaration; Move Function |
| **Data Class** | Move Function into it — *or accept it; an anemic model is a style, not a crime (W3 L11 §3)* |
| **Comments** | Sometimes a deodorant for a smell — **and sometimes just a good comment.** See below |

---

## On "Comments" as a smell

Fowler lists comments as a smell, and *Clean Code* goes further. **This course disagrees, and the
syllabus says so (§7.2).**

**A comment explaining *why* is a first-class artefact**, because the why is **not recoverable from
the code** and is the first thing lost when authors leave. `roomsvc` is the whole argument: nobody can
say why `confirm_booking` checks `slot.is_provisional` twice, because the reason lived in a head that
left in 2023.

**The smell is real when a comment explains *what*** — that is a naming failure wearing a costume.

---

## Before you refactor anything

- [ ] **Characterisation tests** for the behaviour you are about to change (L28 §3)
- [ ] **Coverage over those tests**, to see what you have *not* pinned
- [ ] **One hat.** `test:` and `refactor:` are never the same commit
- [ ] **Does it fit in a commit?** If not: branch by abstraction, with a visible denominator
- [ ] **Can two of these run at once?** *Have I moved anything out of a critical section?*
- [ ] **Is this a public interface?** Then it is not a refactoring — it is Week 10

---

*CS 212 · Week 9 · smell catalogue · print and keep*
