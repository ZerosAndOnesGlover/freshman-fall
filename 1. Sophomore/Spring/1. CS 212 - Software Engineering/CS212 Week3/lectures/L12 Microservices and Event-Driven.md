# CS 212 · Software Engineering
## Week 3 · Lecture 3 of 3
### Microservices and Event-Driven — What They Buy, and the Bill

---

**Sat:** Thursday of Week 3, 10:00–10:50, TH 200 · **Reading:** Fowler & Lewis, *"Microservices"* (2014); Fowler, *"MicroservicePremium"* (2015) · **Next:** Week 4, design patterns

---

## 1. What Microservices Actually Buy

One thing, and it is worth a lot in the right organisation:

> **Independent deployability.** A team can ship its service without coordinating with any other
> team, on its own schedule, with its own release cadence, and without a shared release train.

**Everything else attributed to microservices is either a consequence of that or is obtainable without them.** In particular:

| Claimed benefit | Do you need microservices? |
|---|---|
| Modularity, clear boundaries | **No.** A modular monolith with an enforced import rule (L11 §4) |
| Independent scaling of one hot component | **Rarely.** Usually you scale the whole monolith horizontally, which is cheap and simple. Real when one component is genuinely resource-shaped differently — video transcoding next to a web app |
| Technology diversity | **Yes, genuinely** — but ask whether you want it. Five languages means five build systems and no shared libraries |
| Fault isolation | **Partly.** You also acquire *new* failure modes that a monolith does not have (§2) |
| **Independent deployment by separate teams** | **Yes. This is the one.** |

**Conway's law is the real argument** (L10 §7). Microservices are an *organisational* technology: they let twelve teams stop blocking each other. **They are a solution to a communication problem, and you should ask whether you have one.**

**`slot` has five people in one room, one timetable, and a WhatsApp group.** You do not have a communication problem that costs more than a network hop.

---

## 2. The Bill, Itemised

Every one of these is a problem you do not have today and would acquire on the day you split.

### 2.1 You lose the transaction

**This is the big one and it is not recoverable.**

```python
# monolith: one transaction, the database guarantees it
with uow:
    booking = repo.confirm(hold_id)      # unique index protects the invariant
    ledger.charge(booking.owner, price)  # same transaction
# both, or neither.
```

Split `bookings` and `billing` into two services with two databases and this becomes two network calls that can each fail independently. **There is no distributed transaction available to you** — two-phase commit exists, is slow, and takes an availability hit that defeats the purpose.

**What you do instead is the saga pattern**: a sequence of local transactions, each with a compensating action. And compensation is not undo:

| Step | Compensation | Is it really undo? |
|---|---|---|
| Confirm booking | Cancel booking | **No** — the confirmation email has been sent |
| Charge the account | Refund | **No** — it appears on a statement |

**Your system is now eventually consistent, and someone has to decide what a user sees in the meantime.** That is a design question per operation, and it is the question CS 202's Week 11 is about from the other end.

### 2.2 You acquire partial failure

In a monolith, a function call either returns or raises. **Over a network there is a third outcome: you do not find out.** A timeout does not tell you whether the other side did the work.

Which forces, on every call:

- **Retries** — and therefore **idempotency**, which every receiver must now implement, which means an idempotency key on every mutating request.
- **Timeouts** with sensible values, which nobody tunes until an incident.
- **Circuit breakers**, or one slow service takes down everything that calls it.
- **Correlation IDs**, or you cannot reconstruct what happened from seven logs.

**Each of those is a week of work and a permanent maintenance burden**, and a term project has twelve weeks.

### 2.3 Debugging gets much harder

**One stack trace becomes seven logs.** You need centralised logging and distributed tracing before you can answer *"why was this request slow?"* — and you need them **before** the incident, because you cannot add tracing retrospectively to a request that already failed.

### 2.4 Local development gets much harder

*"Run the system on your laptop"* goes from `docker compose up` with two containers to eight containers, or to a per-developer cloud environment, or to a nest of mocks that drift from reality. **Every previous cohort that split `slot` lost more time to this than to any design problem.**

### 2.5 Refactoring across the boundary becomes a project

**This is the cost that decides it, and it is the least discussed.**

In a monolith, moving a responsibility from one module to another is a refactoring: an afternoon, with the compiler or the tests to catch you. **Across a service boundary it is a migration**: a new endpoint, a deprecation, two deploys in the right order, a data move, and a period where both exist.

**So microservices demand that you got the boundaries right**, and W1 L06 §5 says your domain model will be wrong. **You are being asked to make an expensive-to-reverse decision precisely where your information is worst** — which is the definition of a bad bet.

> **Fowler's *MicroservicePremium* is the honest summary:** *"don't even consider microservices
> unless you have a system that's too complex to manage as a monolith"* — and his stronger
> recommendation, **monolith first**, follows directly: build the monolith, learn where the seams
> actually are from twelve months of changing it, and extract services along seams you have
> evidence for.

---

## 3. When They Are Right

So you can say it in a viva, and because the answer is not "never":

1. **Multiple teams blocking each other on a shared release.** The organisational case, and the real one.
2. **A component with genuinely different resource needs** — transcoding, ML inference, a crawler.
3. **A component with a different compliance boundary** — card data, where keeping PCI scope small is worth real money.
4. **A component with a different availability requirement** — the thing that must stay up when the rest is down.
5. **Strangling a legacy system** (Week 9): a new service in front of the old one, taking over route by route. **`roomsvc` → `slot` is genuinely this shape in the real world**, and if the department ran both at once it would be the right pattern.

**Note that four of the five are about something other than code quality.** That is the tell.

---

## 4. Event-Driven Architecture

**Components communicate by publishing facts rather than calling each other.** Orthogonal to microservices — you can do this inside a monolith, and for `slot` that is the interesting version.

```python
# instead of: confirm() calls notify(), audit(), sync_calendar()
def confirm(hold_id, repo, events):
    booking = repo.confirm(hold_id)
    events.publish(BookingConfirmed(booking.id, booking.owner_id, booking.slot))
    return booking

# elsewhere, subscribing:
#   send_confirmation_email
#   write_audit_entry
#   push_to_calendar
```

**What it buys:**

- **Extension without modification** — genuinely open/closed, and here the axis of change is real: `roomsvc` has added a subscriber-shaped concern to `confirm_booking` **five times in six years** (email, audit, calendar, cache, exam webhook).
- **Temporal decoupling** — the calendar service being down does not fail the booking. **This is L06's extension 6a, solved structurally.**
- **A natural audit trail** — the events *are* the log.

**What it costs**, and the first one is severe:

| Cost | |
|---|---|
| **You cannot follow the control flow by reading** | *"What happens when a booking is confirmed?"* has no answer visible at the call site. You must search for subscribers. **In a 4,000-line project this is a real loss of comprehensibility for a benefit you may not need** |
| **Ordering and delivery guarantees** | At-least-once means duplicate emails unless every handler is idempotent. Exactly-once does not exist |
| **Debugging is indirect** | The stack trace stops at `publish` |
| **Testing needs a strategy** | "Did the right event get published?" is a different assertion from "did the email get sent?", and you need both |

**The transactional outbox.** If you publish events and write to a database, you have the two-systems problem from §2.1 in miniature: commit the row, then publish — and if the process dies between, the event is lost. **The standard fix is to write the event to an `outbox` table in the same transaction, and have a separate process publish from it.** This is the pattern W1 L06 §1's extension 6a was pointing at, and it is worth knowing the name.

> **The honest recommendation for `slot`:** an **in-process event bus is a reasonable choice** if
> you have three or more subscribers to one domain event, and **over-engineering if you have one.**
> Most teams have one — the confirmation email — and should call the function. **If you adopt it,
> the ADR must name the third subscriber.**

---

## 5. The Two Questions

Ask these of anyone proposing either architecture, including yourself. They are the only two you need.

> **1. What are you buying, and who is the customer?**
> Microservices buy independent deployability for *teams*. **Name the teams.** If the answer is
> "us, all five of us, in one room", you have named the problem.
>
> **2. What is the cost of being wrong about the boundary?**
> In a monolith: an afternoon. Across services: a migration with two deploys and a dual-write
> period. **And you are at the point of the project where your domain model is least reliable.**

**A third, for event-driven specifically:** *how many subscribers does this event have?* **One is a function call wearing a costume.**

---

## 6. What This Means for Your Phase 1

**You will be asked, in the viva, what shape you chose and why.** The marks are for the reasoning, not the shape.

| Answer | Mark |
|---|---|
| *"Modular monolith. We ranked testability first, we enforce the domain-import rule in CI, ADR 0003 records the alternative we rejected and why."* | **Full marks** |
| *"Hexagonal. Here is the port, here are the two adapters — Postgres and the test fake — and here is the 9-second container startup we avoided."* | **Full marks** |
| *"Microservices, because it's better architecture."* | **Poor** — cannot name the customer |
| *"Microservices, because we want the bulk importer to run on its own schedule without blocking the API deploy, and we accepted eventual consistency for the import."* | **Full marks.** A real reason, a named cost |
| *"We didn't really decide."* | **Poor, and honest** — which is better than the third row, and should be said |

**The last row is worth more than it looks.** A team that says *"we did not decide, it accreted, and here is the ADR we are writing now"* has done the thing this week teaches. **A team that retro-fits a justification is doing the thing `roomsvc` did.**

---

## 7. Summary

- **Microservices buy exactly one thing: independent deployability by separate teams.** It is an organisational technology and Conway's law is the real argument. **Everything else attributed to them is obtainable without them, or is a consequence of that one thing.**
- **The bill:** you lose the transaction (sagas, compensations that are not undo, eventual consistency); you acquire partial failure (retries, idempotency, timeouts, circuit breakers, correlation IDs); debugging becomes seven logs; local development becomes eight containers; **and refactoring across a boundary stops being an afternoon and becomes a migration.**
- **That last cost decides it**, because you must get the boundaries right at the moment your domain model is least reliable. **Monolith first.**
- **They are right** when teams block each other, when resource needs genuinely differ, for a compliance or availability boundary, or when strangling a legacy system — and four of those five are not about code quality.
- **Event-driven buys extension without modification and temporal decoupling** — `roomsvc` added a subscriber-shaped concern to one function five times — **and costs you the ability to answer "what happens next?" by reading.** The transactional outbox is the pattern for publishing and persisting atomically.
- **Two questions: what are you buying and who is the customer; and what does being wrong about the boundary cost?** For event-driven, a third: **how many subscribers? One is a function call wearing a costume.**
- **Phase 1 marks the reasoning, not the shape** — and *"we did not decide, and here is the ADR we are writing now"* scores above a retro-fitted justification.

**Next:** Week 4 — design patterns: a vocabulary that is thirty years old, which parts of it became language features, and which of the twenty-three are still worth the name.

---

*CS 212 · Week 3 · L12 · © CSE Department*
