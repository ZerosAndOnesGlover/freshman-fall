# CS 212 · Software Engineering
## Week 10 · Lecture 2 of 3
### GraphQL and gRPC — What Each Buys, and What Each Costs

---

**Sat:** Wednesday of Week 10, 10:00–10:50, TH 200 · **Reading:** GraphQL spec overview; gRPC "Introduction"; Protobuf "Proto3 language guide" §Updating **Next:** L33, versioning
**A 10 is released after this lecture**, Wednesday 17:00.

---

## 1. GraphQL Solves One Problem

**The problem is real and specific:** a client needs data from several resources, and a resource-shaped API forces it to make many round trips or to accept a large response it mostly discards.

**`slot`'s week view is exactly this.** To render one week for one room:

```
GET /resources/TH200                    1 request
GET /resources/TH200/bookings?week=...  1 request
GET /users/{id}   × 30 bookings         30 requests    ← the problem
```

**Thirty-two requests, or one endpoint that returns everything and is 40 KB when you needed 3.** GraphQL's answer is that the client states its shape:

```graphql
query WeekView($resource: ID!, $week: Week!) {
  resource(id: $resource) {
    code
    bookings(week: $week) {
      slot
      state
      owner { displayName }     # ← the 30 requests, in the same round trip
    }
  }
}
```

**One request, exactly the fields asked for.** That is what it buys, and for a mobile client on a slow network it is a substantial win.

**Two more real benefits:**

- **A strongly-typed, introspectable schema.** The schema is machine-readable, so tooling — client code generation, editor completion, validation — is unusually good. **This is under-rated.**
- **Field-level deprecation.** `@deprecated(reason: "...")` on a field, plus per-field usage metrics, means **you can find out who still uses something before you remove it** — which L33 shows is the hard part of versioning.

---

## 2. What GraphQL Costs

**Five costs, and the first two are severe enough to decide the question for a project like yours.**

### 1. Caching is much harder

**HTTP caching works on URLs.** `GET /resources/TH200` is cacheable by any proxy, any CDN, and the browser, for free.

**GraphQL is typically one `POST /graphql` with a body.** No URL to key on, and `POST` is not cacheable. **You lose the entire HTTP caching layer** and must rebuild it inside your application — persisted queries, normalised client caches, dataloaders. **All of that is work you did not have to do before.**

### 2. The N+1 problem moves into your resolvers

The query above looks like one request. **On the server, a naive implementation issues:**

```
1  query for the resource
1  query for its bookings
30 queries, one per booking, for the owner        ← N+1, now on your side
```

**You have not removed the thirty requests; you have moved them behind your own API.** The fix is batching — `DataLoader` — which you must implement per field, and which is exactly the proxy-shaped surprise W3 L11 §1 warned about.

### 3. Query cost is unbounded

A client can ask for something expensive:

```graphql
{ resources { bookings { owner { bookings { owner { bookings { ... } } } } } } }
```

**Unbounded depth, unbounded breadth, and one request can cost you a minute of database time.** So you need query depth limits, complexity analysis, and timeouts — **three mechanisms that REST gets for free because each endpoint's cost is bounded by its code.**

### 4. Errors and status codes

GraphQL returns **200 with an `errors` array**, including for a partial failure. **Which means every HTTP-level tool you have — monitoring, alerting, load balancer health, log-based error rates — sees success.** Your observability must be GraphQL-aware, and W8 L27 §6's four numbers need redefining.

### 5. Authorisation is per-field

**A REST endpoint has one permission check.** In GraphQL, `owner { email }` may be visible to an admin and not to a student — **so the check is per field, per path, in every resolver.** This is where GraphQL authorisation bugs come from, and they are common.

> **For `slot`: no.** Your week view's N+1 is solved by **one endpoint that joins**, which is twenty
> lines of SQL, keeps HTTP caching, keeps bounded cost, keeps one permission check, and keeps your
> status codes meaningful. **GraphQL earns its costs when you have many diverse clients you do not
> control** — a public API, several mobile apps on different release cycles, a partner integration.
> **You have one client and you wrote it.**

---

## 3. gRPC Solves a Different Problem

**Service-to-service calls, at volume, where latency and CPU matter.**

```protobuf
syntax = "proto3";

service Bookings {
  rpc Confirm(ConfirmRequest) returns (Booking);
  rpc WatchResource(WatchRequest) returns (stream BookingEvent);   // streaming
}

message ConfirmRequest {
  string hold_id = 1;              // ← field NUMBERS are the contract, not names
  string idempotency_key = 2;
}
```

**What it buys:**

| | |
|---|---|
| **Binary serialisation** | Protobuf is compact and fast to parse — typically **3–10× smaller and faster than JSON** |
| **HTTP/2 multiplexing** | Many concurrent calls on one connection, no head-of-line blocking |
| **Generated clients** | For a dozen languages, from the same `.proto`. **Genuinely excellent tooling** |
| **Streaming** | Server-, client- and bidirectional streaming as first-class. **REST has no good answer to this** |
| **A schema that is enforced** | Not documentation — the wire format |

**What it costs:**

| | |
|---|---|
| **Not browser-native** | Browsers cannot speak gRPC directly. **gRPC-Web plus a proxy**, which is an extra hop and an extra thing to operate |
| **Not human-readable** | `curl` does not work. You need `grpcurl`, and debugging a wire capture is harder |
| **No HTTP caching** | Same problem as GraphQL, for the same reason |
| **Build-step coupling** | Codegen in every client's build. **A team without a build pipeline cannot consume it** |

**The one thing worth learning from Protobuf even if you never use gRPC** — and it is genuinely instructive:

> **The field *number* is the contract; the field *name* is not.**
>
> **Renaming a field is free** — the wire format carries `2`, not `idempotency_key`.
> **Reusing a number is catastrophic** — an old client sends a string for field 2 and the new server
> reads it as an int.

```protobuf
message Booking {
  reserved 3, 7;                  // numbers of deleted fields. Never reuse.
  reserved "old_room_field";      // and the name, so nobody reintroduces it
}
```

**Which is the opposite of JSON**, where the name is the contract and renaming is breaking. **Neither is better; they are different choices about what is stable** — and knowing that a protocol *chooses* this is worth more than knowing either protocol.

---

## 4. Choosing, Honestly

| | REST (level 2) | GraphQL | gRPC |
|---|---|---|---|
| **Best for** | Public and browser-facing APIs, CRUD-shaped resources | Many diverse clients you do not control, over slow networks | Service-to-service, high volume, streaming |
| **Caching** | **Free, via HTTP** | You build it | You build it |
| **Cost bounding** | **Per endpoint, free** | Depth and complexity limits required | Per method, free |
| **Browser** | Native | Native | Proxy required |
| **Debuggable with `curl`** | **Yes** | Partly | No |
| **Schema enforced** | Optional (OpenAPI) | **Yes** | **Yes** |
| **Streaming** | Poor | Subscriptions, with a WebSocket | **First-class** |
| **Renaming a field** | **Breaking** | Breaking, but deprecable per field | **Free** — the number is the contract |
| **For `slot`** | **Yes** | No — one client, and you wrote it | No — no second service |

**The question to ask, and it is L12 §5's question wearing new clothes:**

> **What are you buying, and who is the customer?**
>
> GraphQL buys **query flexibility for clients you do not control.** Name them. gRPC buys
> **efficiency and streaming between services.** Name the services. **If the answer to either is
> "us, and there is one of us", you have named the problem.**

**And the honest note about mixing them**, because real systems do: a public REST API, gRPC between internal services, and GraphQL as a gateway for a mobile client is a coherent architecture at scale. **It is also three protocols to operate, document, monitor and version.** For a five-person team it is three times the work for one client.

---

## 5. What a Schema Buys You, Whichever You Choose

**The most transferable idea in this lecture is not a protocol. It is that a machine-readable schema changes what is possible.**

| With a schema | Without |
|---|---|
| **Generated clients**, always in sync | Hand-written clients, drifting |
| **Breaking-change detection in CI** — `buf breaking`, `oasdiff` | A human reading a diff |
| **Contract tests that are generated** | Contract tests written by hand (W5 L18 §4) |
| Mock servers from the schema | Hand-written stubs |
| Documentation that cannot go stale | Documentation that does |

**So use OpenAPI if you are doing REST.** FastAPI generates it from your type annotations, so you already have it — **and the step almost nobody takes is the second row:**

```yaml
# in the gate (W8 L25 §5)
- run: oasdiff breaking openapi-main.json openapi-head.json --fail-on ERR
```

**A CI check that fails when a pull request breaks your API.** It is the API-level equivalent of W3's architecture test, it costs one step, and **it is the only mechanism in this week that catches a breaking change before a client does.** A 10 requires it.

---

## 6. Summary

- **GraphQL solves one real problem**: a client needing data from several resources without many round trips. `slot`'s week view is 32 requests. It also buys **an introspectable schema** and **per-field deprecation with usage metrics** — which is how you find out who still uses something.
- **Its five costs:** **HTTP caching is gone** (no URL, and `POST`); **the N+1 moves into your resolvers** (you moved the 30 requests, you did not remove them); **query cost is unbounded**, so you need depth and complexity limits; **errors return 200**, so every HTTP-level tool sees success; **and authorisation is per field**, which is where the bugs are.
- **gRPC buys binary serialisation, HTTP/2 multiplexing, generated clients and first-class streaming** — and costs browser support, human readability, HTTP caching and a build step in every client.
- **Protobuf's lesson transfers even if you never use it: the field *number* is the contract, the *name* is not.** Renaming is free; **reusing a number is catastrophic**, hence `reserved`. **JSON chooses the opposite** — and knowing that a protocol *chooses* is the point.
- **For `slot`: REST at Richardson level 2.** One joined endpoint solves the week view in twenty lines of SQL and keeps caching, bounded cost, one permission check and meaningful status codes.
- **Ask what you are buying and who the customer is.** If the answer is "us, and there is one of us", you have named the problem.
- **A machine-readable schema is the transferable idea**: generated clients, mock servers, generated contract tests, documentation that cannot go stale — **and breaking-change detection in CI**, which is one step and the only mechanism here that catches a break before a client does.

**Next:** L33 — versioning: the strategies, why removing something is the hard part, and expand-and-contract for an audience you cannot contact.

---

*CS 212 · Week 10 · L32 · © CSE Department*
