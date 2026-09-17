# CS 212 · Quiz 11
## Administered: Tuesday, Week 11 (first 10 minutes of lecture)
### **The last quiz.**

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 10** — interfaces as contracts, REST, GraphQL and gRPC, versioning.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **This is Quiz 11, and there is no Quiz 12.** Nothing covers Week 11 or Week 12 — **those are
> examined only on the final**, Friday 8 May, 09:00–11:30. The eleven quizzes you have sat are, between
> them, a reasonable map of what the final asks about Weeks 0–10; **the table at the end of each is
> the revision list.**

---

**Q1.** State Hyrum's law, and give the `roomsvc` instance.

&nbsp;

&nbsp;

---

**Q2.** Which SOLID principle decides whether an API change is breaking? State the rule in its API form.

&nbsp;

&nbsp;

---

**Q3.** Why is "add a required field with a default" a breaking change?

&nbsp;

&nbsp;

---

**Q4.** Which of REST's six constraints earns its keep, and why? Which is almost never implemented?

&nbsp;

&nbsp;

---

**Q5.** `POST /bookings` is protected by a unique index. What does an `Idempotency-Key` protect that the index does not?

&nbsp;

&nbsp;

---

**Q6.** Name three of GraphQL's five costs.

&nbsp;

&nbsp;

---

**Q7.** In expand-and-contract, which phase do teams skip, and what does `roomsvc` look like as a result?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** *"With a sufficient number of users of an API, it does not matter what you promise in the contract: **all observable behaviours of your system will be depended on by somebody.**"*

**`roomsvc`:** `GET /bookings` has always returned **insertion order**, because nothing in the query said otherwise. The timetable generator depends on it. **Adding an index changed the plan and broke the timetable in 2023.** The contract said nothing about order; the behaviour did.

---

**Q2.** **Liskov substitution.** In API form: **v2 is compatible with v1 if it weakens preconditions and strengthens postconditions** — accept more, demand less, return more, remove nothing.

*Which is why W2 L08 §3 called it the only letter with actual formal content: this is a theorem, not a preference.*

---

**Q3.** **The server is fine; the clients are not.** A client that **round-trips** an object — reads it, changes one field, writes it back — now sends your default in a field the user never set, **overwriting their value.**

*It is L31 §2's first trap and a real, common outage pattern.*

---

**Q4.** **Statelessness earns its keep**: every request carries everything needed to understand it, so **a service can be scaled by adding instances and load-balanced with no session affinity.** Operational, not aesthetic — which is why this constraint survived and the others mostly did not.

**HATEOAS is almost never implemented**, because clients read documentation and hard-code paths, so the cost is paid and the benefit is not collected. **It does pay where the available transitions depend on state** — as in `slot`, where it saves a client from re-implementing your state machine.

---

**Q5.** **The unique index protects the data. The idempotency key protects the user's experience of it.**

`POST` is not idempotent, so a retry — a mobile network, a load-balancer timeout, a double-click — sends the request twice. **The index correctly rejects the second as a 409**, which is the right outcome and the wrong error for a user who clicked once. With the key, the server returns **the original result.**

---

**Q6.** Any three of: **HTTP caching is gone** (no URL to key on, and `POST` is not cacheable); **the N+1 moves into your resolvers** — you moved the thirty requests, you did not remove them; **query cost is unbounded**, so you need depth and complexity limits; **errors return 200**, so every HTTP-level monitor, alert and load-balancer check sees success; **authorisation is per field**, which is where the bugs are.

---

**Q7.** **Phase 3 — measurement.** Teams expand, deprecate, and never instrument, so they never find out whether anyone still uses the old form.

**`roomsvc` has seventeen deprecated endpoints, the oldest marked in March 2021**, all still live, still in the test suite, still in the security surface. **"Deprecated" without a usage metric is a comment.**

*Four lines fix it — and the caller tag turns an impossible removal into three emails.*

---

### What to Do With Your Score — and With the Eleven Quizzes

There is no score. For this one:

| If you missed | Reread |
|---|---|
| **Q1, Q3** | **L31 §1–2** — Hyrum's law appears three times in A 10 and is the kind of cross-week connection the final rewards |
| Q2 | L31 §2, and W2 L08 §3 |
| Q4 | L31 §3 |
| Q5 | L31 §4 |
| Q6 | L32 §2 |
| **Q7** | **L33 §4** — A 10 caps at 75 without the metric |

**And for the final, on 8 May:** the eleven quizzes cover Weeks 0–10, and **their answer keys are the most compact revision material in the course.** Weeks 11 and 12 have no quiz, so **the final is the only place L34–L36 and Week 12 are examined** — the debt quadrant, hotspots, Goodhart's five appearances, and documentation a machine checks.

**The most reliable revision exercise available:** work back through the eleven *"what to reread"* tables and list every entry you were sent to more than once. **Those are the course's load-bearing sections**, and the final's essay questions are built on the connections between them.

---

*CS 212 · Week 11 · Quiz 11 · covers Week 10 · ungraded · the last quiz*
