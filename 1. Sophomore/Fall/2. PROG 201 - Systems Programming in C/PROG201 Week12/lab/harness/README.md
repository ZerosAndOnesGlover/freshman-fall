# Project 2 Test Harness

Provided tools for exercising your daemon. Build with `make` (warning-clean under `-Wall -Wextra`).

## `bench` — load client (because `ab` is not installed)

```
bench PORT [CONNS] [PER_CONN] [PATH]
bench 8080 50 200            # 50 connections, 200 requests each, to "/"
bench 8080 10 4 /slow        # exercise a blocking endpoint
```

Opens `CONNS` connections in parallel, each firing `PER_CONN` sequential `GET PATH` requests
(HTTP/1.0, connection: close). Reports throughput and mean / p50 / **p99** / max latency. It sorts
every latency, so the percentiles are real — the p99 is the number your SLA is written on, not the
mean. Loopback throughput is an upper bound; treat it as a ceiling, not a forecast.

## `rudeclient` — the client that hangs up

```
rudeclient PORT [rst|fin]    # default: fin
```

Connects, sends a request, then disconnects before reading the reply:
- `fin` (default): a graceful close (FIN). A later server write provokes a RST from the peer, and the
  write *after that* raises `SIGPIPE`/`EPIPE` — the case that kills a server which does not ignore
  `SIGPIPE`.
- `rst`: an abrupt close (RST via `SO_LINGER 0`). The server's write gets `ECONNRESET`.

Use it to prove your daemon survives a mid-response disconnect (Project 2, Part 2). Run one against a
`/slow` request in flight, then confirm a normal `bench` request still succeeds against the same pid.

## A note on ports

Pick a **high, free** port for testing (e.g. `39117`). Other services may hold common ports like
`8080` on a shared machine — if `bench` reports throughput but your daemon logged a `bind` error,
you are measuring someone else's server. Check with `ss -ltn | grep :PORT` first.
