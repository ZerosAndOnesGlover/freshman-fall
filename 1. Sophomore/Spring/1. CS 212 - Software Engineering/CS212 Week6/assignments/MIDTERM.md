# CS 212 · Midterm Examination
## Wednesday 4 March, 18:00–19:15 · 75 minutes · 100 marks · 15% of the course

**Name:** _________________________________ **Student ID:** ___________ **Team:** ___________

---

**Covers Weeks 0–5.** Software engineering as a discipline; requirements; design principles; architecture; design patterns; testing.

**Closed book.** No notes, no devices. **One A4 sheet of your own handwritten notes is permitted** — bring it; it is the best revision exercise available and you may keep it.

**Answer all questions.** Marks are shown. **Budget roughly 45 seconds per mark.**

> **How this paper is marked.** Every question asks for a judgement, and **a defended position that
> disagrees with the lectures scores full marks.** There are four questions in this paper where the
> lecture's own position is contested, and saying so is worth more than reciting it. Where a
> question says *"with evidence"* or *"with a number"*, an answer without one is capped at half.

---

## Section A — Short Answers (30 marks)

**A1. [4]** State the operational definition of architecture, and the test it yields.

**A2. [4]** `roomsvc`'s `bookings.py` took **891 of 2,173 file-touches in two years.** What does that measure, and why does it require no judgement?

**A3. [5]** Name the four requirement categories. Which one did the VNC 101 double-booking violate, and why does that category never appear in a user story?

**A4. [4]** A test suite has 100% line and branch coverage. Give **three** distinct classes of defect it can still ship.

**A5. [4]** Adapter, Facade, Decorator and Proxy all wrap an object. **Distinguish all four in one sentence each.**

**A6. [5]** State DRY in its original words, and give the test that separates real duplication from two fragments that merely look alike.

**A7. [4]** What is the *one* thing microservices buy? Name two items on the bill.

---

## Section B — Applied Judgement (40 marks)

**B1. Where the invariant lives [14]**

A team proposes enforcing *"a resource has at most one confirmed booking per slot"* in their domain layer:

```python
def confirm(hold_id, repo):
    hold = repo.get(hold_id)
    if repo.confirmed_exists(hold.resource, hold.slot):
        raise AlreadyBooked(hold.resource, hold.slot)
    return repo.mark_confirmed(hold_id)
```

**(a) [6]** Explain precisely why this does not enforce the invariant. Name the failure, and describe the interleaving.

**(b) [4]** State where it must be enforced instead, and **give the general rule** of which this is an instance.

**(c) [4]** The team objects: *"business rules do not belong in the database."* **Answer the objection** — and say what, if anything, is right about it.

---

**B2. The abstraction question [14]**

In 2020, `roomsvc` had two booking kinds and one place that switched on them. By 2024 it had six kinds and four switch sites, and commit `7b1e4f2` added a kind and missed one site for eight months.

**(a) [5]** A developer in **2020** proposes replacing the two-branch `if` with a policy registry. **Should they?** Answer with the principle, and with what would have to be true.

**(b) [5]** The same proposal in **2024**. Same question. **If your two answers differ, name exactly what changed** — and say where a developer would find it.

**(c) [4]** Sandi Metz: *"duplication is far cheaper than the wrong abstraction."* **Explain the asymmetry** — why is a wrong abstraction more expensive than duplication, given that both cost an edit in several places?

---

**B3. Reading a test [12]**

```python
def test_confirm_notifies_owner():
    repo, notify = Mock(), Mock()
    confirm("h1", repo, notify)
    repo.confirm.assert_called_once_with("h1")
    notify.assert_called_once_with(OWNER_ID, "Confirmed: TH200 at 10:00")
```

**(a) [6]** Give **three** distinct defects in this test. For each, describe a change to the system that would make it fail although nothing had broken, **or** a break it would not detect.

**(b) [3]** Rewrite it. State what your version asserts that this one does not.

**(c) [3]** Under mutation testing, `booking = repo.confirm(hold_id)` is mutated to `booking = None`. **Does this test kill it?** Justify, and say what the answer tells you about the relationship between coverage and mutation score.

---

## Section C — Essay (30 marks)

**Answer ONE of the following. About 500–700 words. Marked on the argument, not on length or on agreement with the lectures.**

---

**C1. "Every process innovation since 1968 has shortened the feedback loop, and nothing else about them is common."**

**Defend or attack this claim.** Use at least three of: waterfall as Royce actually wrote it, the spiral model, Scrum, Kanban, XP's technical practices, continuous integration.

**Your answer must engage with the evidence**, including the fact that the practices with the strongest empirical support are the mechanical ones and those with the weakest are the cultural ones. **Say what that asymmetry implies** — for the claim, and for how you should treat advice in this field.

---

**C2. "Coverage is a diagnostic, never a target; mutation score is the measurement that matters."**

**Defend or attack.** You must use Inozemtseva & Holmes (2014) and Just et al. (2014), and you must state what each actually controlled for.

**Then answer the harder question:** if mutation score is the better measure, **why is it not universally adopted?** Give the practical reasons and say which of them are solvable.

---

**C3. "`confirm_booking` is not bad because it is 487 lines."**

**Defend the claim, then complicate it.** Name what is actually wrong with the function, and show that the obvious fix — splitting it into nine small functions — leaves each problem standing.

**Then the complication:** *is length ever the problem?* If it is, say under what conditions and why. If it never is, explain why the correlation between long functions and bad functions is so strong — **and whether a rule of thumb that is wrong about the mechanism can still be useful advice.**

---

## Formula sheet and given facts

*Provided so that no mark depends on memorising a figure.*

| | |
|---|---|
| `roomsvc` | 11,438 lines; 2,847 commits; 5 human authors, 1 remaining; `bookings.py` 2,814 lines; `confirm_booking` 487 lines, cyclomatic complexity 94, 11 tests |
| `roomsvc` tests | 212 tests, 94 s; **61.0% line coverage**, 48.3% branch; **31.1% mutation score** (1,204 mutants, 374 killed) |
| Change data | `bookings.py`: 891 of 2,173 file-touches over two years |
| Lifetime cost | ~60% post-release; of maintenance: ~50% perfective, ~25% adaptive, **~21% corrective**, ~4% preventive |
| Feature usage | 45% never used, 19% rarely (Standish, 2002) |
| Brooks | Communication paths = $n(n-1)/2$ |
| Little's Law | $L = \lambda W$ |
| Boehm | Requirements defect found in production ≈ 100× the cost of finding it in requirements |
| Test timings | Domain test with a fake ≈ 1 ms; integration test with a session-scoped container ≈ 5–20 ms; container startup ≈ 9 s |

---

*CS 212 · Midterm · Weeks 0–5 · 100 marks · 15% of the course*
