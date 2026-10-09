# CS 212 · Software Engineering
## Week 10 · Lecture 1 of 3
### Interfaces as Contracts, and REST Properly Understood

*“In general, an implementation must be conservative in its sending behavior, and liberal in its receiving behavior.”* — Jon Postel, RFC 791, *Internet Protocol* (1981)

---

**Sat:** Tuesday of Week 10, 10:00–10:50, TH 200 · **⚠️ Quiz 10 in the first ten minutes** — covers Week 9 · **Reading:** Fielding (2000), Ch. 5; Richardson & Ruby, *RESTful Web Services*, Ch. 4 · **Next:** L32, GraphQL and gRPC

**Coursework:** 📊 **Quiz 10** today · 📝 **Assignment 10** released Wed this week 17:00, due Fri of Week 11 17:00 · 📝 **Assignment 9** due Fri this week 17:00

---

## 1. An API Is a Promise You Cannot Take Back

Week 9 defined refactoring as change that preserves **observable behaviour**, and the operational test was *"if a test had to change, it was not a refactoring."*

**This week, "observable" stops meaning your tests and starts meaning other people's code.**

| Change | Refactoring? |
|---|---|
| Rename a private function | **Yes.** Nothing outside observes it |
| Rename a module-level function used by three call sites in your repository | **Yes.** All observers are in your diff |
| Rename a field in a JSON response | **No. A breaking change** — and you cannot see the observers |

**The asymmetry is the whole subject.** Inside your codebase, the compiler or the test suite enumerates every caller. **Across an API boundary, the callers are unknown, unreachable, and running code you cannot edit.**

> **Hyrum's Law**, and it is the most useful thing in this lecture:
>
> *"With a sufficient number of users of an API, it does not matter what you promise in the contract:
> all observable behaviours of your system will be depended on by somebody."*
>
> **Which includes** the order of keys in a JSON object, the exact wording of an error message, the
> fact that an id happens to be sequential, the latency, and **a bug.**

**`roomsvc` has a live instance of this.** Its `GET /bookings` has always returned results ordered by insertion, because nothing in the query says otherwise. **The timetable generator depends on that order.** Nobody documented it, nobody intended it, and adding an index that changed the plan broke the timetable in 2023. **The contract said nothing about order; the behaviour did.**

---

## 2. Liskov, Again, and This Time It Is Load-Bearing

W2 L08 §3 rated Liskov Substitution the only SOLID letter with formal content: **a subtype may weaken preconditions and strengthen postconditions, never the reverse, and must preserve invariants.**

**That is exactly the rule for a backward-compatible API version.** Version 2 is a subtype of version 1 if v1 clients still work:

| Allowed — weaken what you demand, strengthen what you deliver | Forbidden — demand more, deliver less |
|---|---|
| **Add an optional** request field | **Add a required** request field |
| **Accept** a wider range of input | **Reject** input you used to accept |
| **Add** a response field | **Remove** a response field |
| **Add** a new endpoint | **Remove or rename** an endpoint |
| Make an error **more** specific in its body | **Change a status code** |
| Relax a validation rule | **Tighten** a validation rule |

**So "is this change breaking?" has a formal answer**, and it is the same rule you learned in Week 2 about class hierarchies. **The vocabulary transfers exactly**, which is why L08 §3 said this was the letter to learn properly.

**Three traps that look non-breaking and are not:**

1. **Adding a required field with a default.** The server is fine. **A client that round-trips the object — reads, modifies one field, writes back — now sends your default and overwrites the user's value.** This is a real and common outage.
2. **Making an optional field required "because everyone sends it".** Everyone you know about.
3. **Adding a response field with a name a client already uses internally.** Rare, and it happens with loosely-typed clients that merge objects.

---

## 3. REST, Properly

**Roy Fielding's 2000 dissertation defines REST as an architectural *style* — a set of constraints — not as "HTTP with JSON".** Almost everything called REST is not, and the gap is worth knowing precisely because it tells you which parts are load-bearing.

**Six constraints:**

| Constraint | What it requires | Do you have it? |
|---|---|---|
| **Client–server** | Separation of concerns | Yes |
| **Stateless** | **Every request carries everything needed to understand it.** No server-side session | **Usually yes, and it is the most valuable one** |
| **Cacheable** | Responses say whether they may be cached | Usually ignored |
| **Layered system** | Proxies and gateways can sit in between | Yes, by accident |
| **Uniform interface** | Resources, representations, self-descriptive messages, **and HATEOAS** | **Almost never** |
| Code-on-demand *(optional)* | | No |

**Statelessness is the one that earns its keep**, and the reason is operational rather than aesthetic: **a stateless service can be scaled by adding instances and load-balanced with no session affinity**, and any instance can serve any request. That is why the constraint survived and the others mostly did not.

**HATEOAS is the one nobody implements.** *Hypermedia As The Engine Of Application State*: responses carry links telling the client what it may do next, so the client discovers the API at runtime rather than hard-coding URLs.

```json
{
  "id": "b1f3...", "resource": "TH200", "state": "HELD",
  "_links": {
    "self":    {"href": "/bookings/b1f3..."},
    "confirm": {"href": "/bookings/b1f3.../confirm", "method": "POST"},
    "cancel":  {"href": "/bookings/b1f3.../cancel",  "method": "POST"}
  }
}
```

**Why it is mostly absent, honestly:** the benefit — clients that survive URL changes — requires clients that *actually* follow links, and almost none do. **Developers read documentation and hard-code paths.** So the cost is paid and the benefit is not collected.

**Where it does pay:** when the available *transitions* depend on state. Here, `_links` tells a client that a `HELD` booking can be confirmed and a `CONFIRMED` one cannot — **which means the client does not have to re-implement your state machine.** That is a real benefit and it is worth considering for `slot`, because your state machine is exactly the thing a client would otherwise duplicate and get wrong.

> **The Richardson Maturity Model** is the useful ladder: **level 0**, one endpoint, everything POSTed;
> **level 1**, resources; **level 2**, HTTP verbs and status codes used correctly; **level 3**, HATEOAS.
> **Most good APIs are level 2 and that is a defensible destination.** Say "level 2" rather than
> "RESTful" and you will be both more accurate and more credible.

---

## 4. Getting Level 2 Right

**Level 2 is where the marks are**, and most of it is mechanical.

**Resources are nouns; verbs are HTTP methods:**

```
GET    /resources                 list
GET    /resources/TH200           one
GET    /resources/TH200/bookings  a sub-collection
POST   /bookings                  create
GET    /bookings/{id}             read
POST   /bookings/{id}/confirm     ← a state transition, not a resource
DELETE /bookings/{id}             ✗ don't — cancellation is not deletion (I5)
POST   /bookings/{id}/cancel      ✓
```

**The `confirm` line deserves a note.** Strict REST would model this as `PATCH /bookings/{id}` with `{"state": "CONFIRMED"}`. **In practice, naming the transition is better**, because it is the thing that has permissions, an invariant and a failure mode — and because `PATCH` with a state field invites a client to attempt `HELD → HELD`. **State machines are better expressed as named transitions than as assignable fields**, which is L15 §3's point arriving at the API boundary.

**Status codes that actually matter:**

| Code | Use |
|---|---|
| **200 / 201 / 204** | OK / created / no content |
| **400** | Malformed — you cannot parse it |
| **401 / 403** | Not authenticated / authenticated but not permitted. **Different things** |
| **404** | No such resource |
| **409** | **Conflict.** `AlreadyBooked` lands here. **The single most important code in `slot`** |
| **422** | Well-formed but semantically invalid — a slot outside opening hours |
| **429** | Rate limited |
| **5xx** | **Your fault.** A 500 for a client's bad input is a defect |

**Idempotency, which is not optional** (W3 L12 §2): `GET`, `PUT` and `DELETE` are idempotent by specification; **`POST` is not**, so a retried booking creates two.

```
POST /bookings
Idempotency-Key: 8f14e45f-...
```

**The server stores the key with the result and returns the same result for a repeat.** Without this, any client retry — a mobile network, a load balancer timeout, a user double-clicking — **is a duplicate booking**, and the constraint will reject it as a conflict, which is the *right* outcome but the *wrong* error for the user. **Your invariant protects the data; the idempotency key protects the user's experience of it.**

---

## 5. Error Bodies Are Part of the Contract

**A status code is not enough**, and an error body assembled ad hoc becomes a contract by accident (Hyrum's law).

**RFC 9457, `application/problem+json`** — use it, because it already exists and it is stable:

```json
{
  "type": "https://slot.cse.example/problems/slot-unavailable",
  "title": "The requested slot is unavailable",
  "status": 409,
  "detail": "TH200 already has a confirmed booking at 2026-03-04T10:00Z",
  "instance": "/bookings/req-8f14e45f",
  "conflicting_booking": "b1f3c9a2"
}
```

**Three properties make this worth adopting:**

- **`type` is a stable identifier.** A client branches on it. **`detail` is prose and may change; `type` may not** — which gives you a way to improve error wording without breaking anybody.
- **It is extensible.** `conflicting_booking` is yours; the standard says extra members are allowed.
- **It is uniform.** One shape for every error, so a client writes one handler.

> **And say in your documentation which parts are contract.** *"`type` and `status` are stable;
> `title` and `detail` are human-readable and may change"* — **which is the only defence against
> Hyrum's law available to you: state what is promised, and make the unpromised parts visibly
> unstable.** It does not fully work. It helps.

---

## 6. Summary

- **Across an API boundary, observable behaviour means other people's code** — unknown, unreachable, uneditable. Renaming a private function is a refactoring; renaming a JSON field is a breaking change.
- **Hyrum's law: with enough users, everything observable will be depended on**, including key order, error wording, latency, and bugs. **`roomsvc`'s `GET /bookings` order was never promised and the timetable generator depends on it.**
- **Liskov is the formal rule for compatibility**: weaken preconditions, strengthen postconditions. **Add optional request fields and response fields; never add a required field, remove a response field, tighten validation, or change a status code.**
- **Three traps that look safe:** a required field with a default (**round-tripping clients overwrite user data**), making an optional field required "because everyone sends it", and colliding with a client's internal name.
- **REST is six constraints, and statelessness is the one that earns its keep** — it is what makes horizontal scaling and load balancing work. **HATEOAS is almost never implemented**, because clients hard-code paths; **it does pay where the available transitions depend on state**, which is exactly `slot`.
- **Say "Richardson level 2"**, not "RESTful". It is more accurate and more credible.
- **Name state transitions as endpoints** rather than exposing an assignable `state` field. **409 is the most important code in `slot`.** **`POST` is not idempotent, so an `Idempotency-Key` protects the user where the constraint protects the data.**
- **Error bodies are contract.** Use `application/problem+json`, branch on a stable `type`, and **say in the documentation which fields are promised.**

**Next:** L32 — GraphQL and gRPC: what each actually buys, what each costs, and the question to ask before adopting either.

---

*CS 212 · Week 10 · L31 · © CSE Department*
