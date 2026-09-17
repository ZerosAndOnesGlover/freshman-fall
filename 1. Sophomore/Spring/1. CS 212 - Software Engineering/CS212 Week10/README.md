# CS 212 · Software Engineering
## Week 10: API Design

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 9 due Friday 10 April 17:00 · **A 10 released Wednesday** · **📊 Quiz 10 Tuesday** (covers Week 9)

> **MATH 251's Midterm 2 is Monday 6 April and ECE 211's is Tuesday 7 April.** A 9 is due this Friday.
> **A 10 is due Friday 17 April — the same day as CS 202's Project 1, Problem Set 10 in every course,
> and CS 290's Position Paper 2.** Do A 10's Q1–Q3 in the first week.

---

### Why This Week Exists

Because Week 9 defined refactoring as change that preserves **observable behaviour**, and this week observable stops meaning *your tests* and starts meaning *other people's code.*

**Renaming a private function is a refactoring. Renaming a field in a JSON response is a breaking change** — and the difference is not the size of the edit, it is that **you cannot enumerate the observers.** Inside your codebase the test suite lists every caller; across an API boundary the callers are unknown, unreachable, and running code you cannot edit.

**Hyrum's law is the sharpest statement of the consequence:** *with a sufficient number of users, all observable behaviours of your system will be depended on by somebody* — including key order, error wording, latency, and bugs. **`roomsvc`'s `GET /bookings` has always returned insertion order, because nothing in the query said otherwise. The timetable generator depends on it. Adding an index broke the timetable in 2023.** The contract said nothing about order; the behaviour did.

**And the week's one formal result is a friend from Week 2.** *Is this change breaking?* has a precise answer, and it is **Liskov substitution**: weaken preconditions, strengthen postconditions. Add optional request fields and response fields; never add a required field, remove a response field, tighten a validation rule, or change a status code. **W2 L08 §3 said Liskov was the one letter with actual formal content — this is where it pays.**

---

### Learning Objectives

By the end of Week 10, you should be able to:

1. Say why an API boundary changes what "observable behaviour" means, and **state Hyrum's law** with two examples from your own API.
2. **Classify any change as breaking or not, from Liskov**, and name the three traps that look safe — including the required field with a default that lets round-tripping clients overwrite user data.
3. List **REST's six constraints**, say which one earns its keep and why, and explain why **HATEOAS is almost never implemented** and where it genuinely pays.
4. Place an API on the **Richardson Maturity Model**, and say "level 2" instead of "RESTful".
5. Use status codes correctly — **409 for the conflict, 403 against 401, and never a 5xx for a client's mistake.**
6. **Model state transitions as named endpoints** rather than an assignable `state` field, and say why.
7. Explain why **`POST` is not idempotent**, and what an `Idempotency-Key` protects that the unique index does not.
8. Treat **error bodies as contract**: `application/problem+json`, a stable `type`, and documentation saying which fields are promised.
9. Say what **GraphQL buys** and name its **five costs**, including the N+1 moving into your resolvers and errors returning 200.
10. Say what **gRPC buys**, and state Protobuf's rule — **the field number is the contract, the name is not** — and why JSON chooses the opposite.
11. Choose a **versioning strategy** and defend it; explain **Stripe's transformer chain** and the principle it generalises.
12. Run **expand-and-contract**, and explain why **phase 3 — measurement — is the phase that makes removal possible at all.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L31 Interfaces as Contracts and REST Properly]] | Why an API boundary changes the meaning of observable; **Hyrum's law, and `roomsvc`'s unpromised ordering**; **Liskov as the formal compatibility rule**, with three traps that look safe; **REST's six constraints** and why statelessness earns its keep; **HATEOAS, honestly** — and where it pays for `slot`; level 2 done properly; **idempotency keys**; **error bodies as contract** |
| [[L32 GraphQL and gRPC]] | The one problem GraphQL solves, with `slot`'s 32-request week view; **its five costs**, including the N+1 moving into your resolvers and **errors returning 200 so every HTTP tool sees success**; what gRPC buys and costs; **Protobuf's field-number rule, and why JSON chooses the opposite**; the choice table; **and why a machine-readable schema is the transferable idea** |
| [[L33 Versioning and Backward Compatibility]] | **Removal is the hard part** — `roomsvc`'s seventeen deprecated endpoints, oldest from March 2021, all still live; the five strategies; **Stripe's transformer chain and the principle it generalises**; **expand-and-contract, where phase 3 is measurement**; the four things a deprecation needs; **SemVer, and why it fails for services** |
| [[CS212 Week10/assignments/QUIZ 10 Week 10 Tuesday\|QUIZ 10]] | Seven questions on Week 9, ten minutes, with its own answer key |
| [[CS212 Week10/assignments/A 10 Design and Version a REST API\|A 10]] | Five questions, 100 points, due Friday 17 April. **Three deliverables go in the repository**; two automatic caps |
| [[CS212 Week10/resources/Reading Guide Week 10\|Reading Guide Week 10]] | **Fielding Ch. 5 only**, and what to notice in it; **and an honest note that this week has almost no empirical evidence** — except the one part that is a theorem |
| `resources/slot-openapi-v1.yaml` | A worked OpenAPI document with the reasoning in comments — including which fields are contract and which are prose |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A deprecation with a metric and a date is a plan. Without them, it is a wish.**

`roomsvc` has **seventeen deprecated endpoints. The oldest was marked in March 2021.** Every one of them is still live, still in the test suite, still in the security surface, and still breaks when the schema changes — because **nobody could find out who used them, so nobody could delete them.**

**The fix is four lines:**

```python
if "room_id" in body:
    metrics.increment("deprecated_field_used",
                      tags={"field": "room_id",
                            "client": request.headers.get("User-Agent", "unknown")})
```

**Four lines convert *"we think nobody uses it"* into a number** — and the `client` tag converts an impossible removal into **a conversation with three teams.** That is the whole difference between a codebase that can shed weight and one that only accumulates it.

**And notice the shape of the idea, because you have now seen it four times.** W6: coverage is a diagnostic you *read*, not a target. W7: a linter rule everyone dismisses should be *deleted*, and the dismissal count is the evidence. W8: a nightly sweep nobody *reads* is worse than none. W10: a deprecation nobody *measures* is permanent. **Every one is the same principle — instrument the thing you intend to act on, and act on it — and every failure is the same failure: a signal generated, and never read.**

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.** Quiz *N* covers Week *N−1*, ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, with its own key printed. **Quiz 11, next week, is the last one.** Tracked in [[_CS 212 Quiz Record]].

**Assignments** released Wednesday 17:00, due Friday 17:00 of the week after; **lowest of thirteen dropped.** A 9 is due this Friday. A 10 is released Wednesday.

> **A 10's two caps.** **No breaking-change check in the gate → 70**, because it is one CI step and the
> only mechanism this week that catches a break *before a client does*. **An expand-and-contract with
> no usage metric → 75**, because phase 3 is what makes removal possible — without it you have built
> `roomsvc`'s seventeen deprecations.

---

### Connections

**Back:** **W2 L08 §3's Liskov is this week's compatibility theorem**, which is why that lecture said it was the letter to learn properly. **W9's definition of refactoring** is what breaks at the API boundary. **W8 L26 §7's expand-and-contract** for a database column is L33 §4's technique for a field, and **W4 L14 §5's Adapter** is Stripe's transformer chain applied across time instead of across systems. **W3 L12 §5's two questions** return unchanged for GraphQL and gRPC.

**Sideways:** **CS 202's Week 11 is distributed systems**, and its treatment of failure detection is the other half of L32's honesty about gRPC — you cannot distinguish a slow service from a dead one, which is why streaming and timeouts are first-class there. **CS 202's Project 1 is due the same Friday as A 10**; plan for it.

**Forward:** **Week 11 reads every number this course has produced as a trend rather than a score**, and asks you to write the debt register your final report is marked on — **an API compatibility item belongs on it, and teams never think to put one there.** **Week 12** is presentations, management and what to do next. **The final report** asks for at least one ADR you would now decide differently, and a versioning decision is a strong candidate.

---

*CS 212 · Week 10 · © CSE Department*
