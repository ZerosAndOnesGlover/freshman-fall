# CS 212 · Software Engineering
## Week 10 · Lecture 3 of 3
### Versioning, and Backward Compatibility

*“Compatibility means deliberately repeating other people's mistakes.”* — David Wheeler

---

**Sat:** Thursday of Week 10, 10:00–10:50, TH 200 · **Reading:** Stripe's API versioning post; SemVer 2.0.0 · **Next:** Week 11, technical debt and metrics

**Coursework:** 📝 **Assignment 9** due Fri this week 17:00 · 📊 **Quiz 11** Tue of Week 11 · 📝 **Assignment 11** released Wed of Week 11 17:00, due Fri of Week 12 17:00

---

## 1. The Hard Part Is Removal, Not Addition

**Adding to an API is easy and safe.** Liskov says so (L31 §2): an optional request field and a new response field break nobody.

**The hard part is taking something away**, and the difficulty is not technical:

> **You cannot remove a field until you know nobody uses it, and you cannot know that.**

**Which is where the real work of versioning lies.** Every strategy below is an answer to *"how do I eventually get rid of v1?"*, and the ones that fail, fail there.

**`roomsvc`'s answer was to never remove anything.** The result:

```console
$ grep -c 'deprecated' roomsvc/views.py
17
$ git log -S'DEPRECATED' --format='%cd' --date=short | tail -1
2021-03-08
```

**Seventeen deprecated endpoints, the oldest marked five years ago, all still live and all still maintained.** Nobody knew who used them, so nobody could delete them, so every one of them is still in the test suite, still in the security surface, and still breaks when the schema changes. **"Deprecated" without a removal mechanism is a comment.**

---

## 2. The Strategies

| Strategy | Example | Honest assessment |
|---|---|---|
| **URL path** | `/v1/bookings`, `/v2/bookings` | **Most common, most visible, easiest to route and to reason about.** Purists object that the URL should identify the resource, not its representation. Ignore them; this is fine |
| **Header** | `Accept: application/vnd.slot.v2+json` | Theoretically cleaner. **Invisible in a browser, invisible in a log, easy to forget, and hard to test with `curl`** |
| **Query parameter** | `/bookings?version=2` | Easy, and it pollutes caching — the same resource has two cache keys |
| **Date-based, pinned per client** | `Stripe-Version: 2026-03-04` | **The most sophisticated, and the most expensive.** §3 |
| **Never version; only make compatible changes** | | **The best answer when you can manage it**, and §4 is how |

**Recommendation for `slot`, and you should be able to defend it:** **`/v1/` in the path from the first endpoint**, and then work hard to never need `/v2/`. **The prefix costs nothing now and is impossible to add later** — retrofitting a version prefix is itself a breaking change, which is a nicely circular trap.

---

## 3. Stripe's Approach, Because It Is Instructive

**Stripe has not made a breaking change since 2011**, while changing its API continuously. The mechanism is worth understanding even though you will not build it.

1. **Every client is pinned to the API version current when it first called.**
2. **Internally, there is exactly one current implementation.**
3. **Between the implementation and the client sits a chain of *version transformers*** — small, ordered, individually-tested functions, each of which converts the response from one version to the previous one.

```
current implementation
  → transform 2026-01-15 → 2025-11-02   (renames `resource_id` back to `room_id`)
  → transform 2025-11-02 → 2025-06-30   (re-adds the removed `legacy_price` field)
  → the client's pinned version
```

**What this buys:** a client written in 2014 still works, and the team maintains **one** implementation rather than fourteen.

**What it costs**, and this is why you are not doing it:

- **Every breaking change requires writing and testing a transformer**, forever. The chain only grows.
- **The test matrix is the cross product** of versions and endpoints.
- **Some changes cannot be transformed.** A new *required* concept has no representation in an older version, and then you are stuck.
- **It requires a version registry per client**, which is state you now own.

> **The transferable idea is not the machinery. It is the principle:** **make compatibility a property
> of a translation layer rather than of the core implementation.** One implementation plus N small
> translators is vastly cheaper than N implementations — and it is the same shape as the Adapter
> pattern (W4 L14 §5) applied across time instead of across systems.

---

## 4. Expand and Contract

**The technique you will actually use, and you have already met it twice** — L26 §7 for a database column, and L30 §2's branch by abstraction for a component. **Here it is for an API.**

**The problem: rename `room_id` to `resource_id` without breaking anyone.**

| Phase | Server | Clients |
|---|---|---|
| **1. Expand** | Accept **both** on input; return **both** on output. Document `room_id` as deprecated | Unchanged, still working |
| **2. Migrate** | — | Clients move to `resource_id`, at their own pace |
| **3. Measure** | **Count requests still sending or reading `room_id`** | — |
| **4. Contract** | When the count is zero and has been for long enough, **remove `room_id`** | Done |

**Phase 3 is the one that makes the whole thing work, and it is the one teams skip.**

```python
@app.post("/v1/bookings")
def create_booking(body: dict):
    if "room_id" in body:
        metrics.increment("deprecated_field_used",
                          tags={"field": "room_id",
                                "client": request.headers.get("User-Agent", "unknown")})
    resource_id = body.get("resource_id") or body.get("room_id")
    ...
```

**Four lines, and they convert "we think nobody uses it" into a number.** Without them you are in `roomsvc`'s position: seventeen deprecated endpoints and no way to decide.

**And note what the `client` tag buys.** When the count is not zero, **you know who to email** — which turns an impossible removal into a conversation with three teams.

> **The rule to take from this and from L26 §7 together: every removal is a five-step sequence, and
> step 3 is measurement.** A deprecation with no usage metric is a wish. **A deprecation with a
> metric and a date is a plan.**

---

## 5. Deprecation That Actually Ends

**A deprecation notice needs four things**, and `roomsvc`'s has one.

| | |
|---|---|
| **1. A machine-readable marker** | `Deprecation` and `Sunset` HTTP headers (RFC 8594), `@deprecated` in a schema, a field in your OpenAPI |
| **2. A date** | Not "soon". **A date, in the response headers** |
| **3. A usage metric** | §4. **Without it you cannot act on the date** |
| **4. A replacement, named** | *"Use `resource_id`"* — not *"this is deprecated"* |

```http
HTTP/1.1 200 OK
Deprecation: version="v1", date="Wed, 04 Mar 2026 00:00:00 GMT"
Sunset: Fri, 04 Sep 2026 00:00:00 GMT
Link: </v2/bookings>; rel="successor-version"
Warning: 299 - "room_id is deprecated; use resource_id. Removal 2026-09-04."
```

**Then — and this is what nobody does — put the sunset date on the board as a card**, with the metric linked. **A deprecation that is not scheduled work does not happen**, which is why `roomsvc` has seventeen of them and the oldest is from March 2021.

---

## 6. SemVer, and Where It Applies

**Semantic versioning — `MAJOR.MINOR.PATCH`** — is a promise about compatibility, and the mapping is Liskov again:

| Increment | When |
|---|---|
| **PATCH** | A bug fix that changes no interface |
| **MINOR** | Backward-compatible addition — **weakened preconditions, strengthened postconditions** |
| **MAJOR** | A breaking change |

**It works well for libraries** — one artefact, one version, a consumer who chooses when to upgrade.

**It works badly for a deployed service**, for a reason worth being precise about: **a library consumer upgrades when they choose, and a service consumer is upgraded when you deploy.** There is no `requirements.txt` pinning your API. **So a MAJOR bump on a service means "we broke you, now"** — which is why services use path versions with overlapping lifetimes rather than SemVer.

**Two honest problems with SemVer even for libraries:**

1. **"Breaking" is decided by the author and experienced by the user.** A bug fix is a MAJOR change to anyone depending on the bug — **Hyrum's law again** (L31 §1).
2. **MAJOR bumps fragment the ecosystem.** Python 2/3 took a decade; `urllib3` 2.0 broke a large fraction of the packaging world for months. **The cost of a major version is paid by everyone downstream, and it is much larger than the author's estimate.**

---

## 7. What to Do on `slot`

A 10 requires 1–4.

1. **`/v1/` in every path**, from now. It costs nothing and cannot be retrofitted.
2. **Generate OpenAPI** — FastAPI does it from your annotations — and **commit the generated document.** It is a diffable contract.
3. **Add breaking-change detection to the gate** (L32 §5): `oasdiff breaking` against `main`'s schema, failing the build. **One step, and it is the only thing here that catches a break before a client does.**
4. **Do one expand-and-contract, properly**, including the usage metric. **A 10 asks you to document a breaking change you chose to make compatibly.**
5. **Decide and record — in an ADR — what you would do if you had a real client.** The viva asks.

---

## 8. Summary

- **Addition is safe; removal is the hard part**, and it is not technical: **you cannot remove a field until you know nobody uses it, and you cannot know that.** `roomsvc` has **seventeen deprecated endpoints, the oldest from March 2021**, all still live — *"deprecated" without a removal mechanism is a comment.*
- **Strategies: URL path** (most common, visible, routable — use it), header (invisible in logs, hard to `curl`), query parameter (pollutes caching), **date-pinned per client** (sophisticated, expensive), and **only ever making compatible changes** (best when you can manage it).
- **Put `/v1/` in the path now.** Retrofitting a version prefix is itself a breaking change.
- **Stripe: one implementation plus a chain of version transformers**, so a 2014 client still works. **The transferable principle is that compatibility belongs in a translation layer, not in the core** — Adapter, across time.
- **Expand and contract, in four phases, and phase 3 is measurement.** Four lines of instrumentation convert *"we think nobody uses it"* into a number — **and the client tag tells you who to email.** A deprecation with a metric and a date is a plan; without them it is a wish.
- **A deprecation needs a machine-readable marker, a date, a usage metric and a named replacement** — and **the sunset date on the board as a card**, or it does not happen.
- **SemVer maps onto Liskov** and works for libraries, badly for services: **a library consumer upgrades when they choose; a service consumer is upgraded when you deploy.** And *"breaking"* is decided by the author, experienced by the user — **Hyrum's law again.**

**Next:** Week 11 — technical debt, metrics, maintainability and documentation. Where every number this course has produced gets read as a trend rather than a score, and where you write the debt register your final report is marked on.

---

*CS 212 · Week 10 · L33 · © CSE Department*
