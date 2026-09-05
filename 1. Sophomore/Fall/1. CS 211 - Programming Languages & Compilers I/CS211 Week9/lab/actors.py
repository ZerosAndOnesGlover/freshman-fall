#!/usr/bin/env python3
"""A mini actor system, and the point it exists to make.

Every bug in `litmus.c`, `orders.c` and `hoist.c` has one precondition:
**two threads reach the same memory.** Remove that and the whole category
goes with it.

An actor owns its state, and nothing else may touch it. Actors communicate
by sending immutable messages to each other's mailboxes. There is no shared
mutable state, so there is nothing to race on, no lock to forget, no barrier
to place, and no memory model to reason about.

    python3 actors.py

That is the trade Erlang, Elixir and Akka make, and it is what Go means by
"do not communicate by sharing memory; share memory by communicating".
**The cost is real and it is measured below**: a message send is far more
expensive than a shared-memory write, and the model only pays when the work
per message is large enough to hide it.

This implementation uses real OS threads and a locked queue, so the locking
has not gone away -- it has been *moved into the mailbox*, written once,
by someone whose job it was. That relocation is the entire engineering
argument, and it is worth being honest that it is a relocation.
"""
import queue
import sys
import threading
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """Immutable. An actor may keep a reference without copying, and no
    sender can mutate a message after it has been posted."""
    tag: str
    body: object = None
    reply_to: 'Actor' = None


STOP = Message('stop')


class Actor:
    """State, a mailbox, and a thread. Nothing else may touch the state."""

    def __init__(self, name):
        self.name = name
        self.inbox = queue.Queue()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self.received = 0

    def start(self):
        self._thread.start()
        return self

    def send(self, msg):
        self.inbox.put(msg)

    def join(self, timeout=None):
        self._thread.join(timeout)

    def _run(self):
        while True:
            msg = self.inbox.get()
            self.received += 1
            if msg.tag == 'stop':
                return
            self.on(msg)

    def on(self, msg):
        raise NotImplementedError


class Counter(Actor):
    """The shared counter from `orders.c`, as an actor.

    `self.count` is touched by exactly one thread -- this actor's own. There
    is no race here, and there is no lock in this class either.
    """

    def __init__(self, name):
        super().__init__(name)
        self.count = 0

    def on(self, msg):
        if msg.tag == 'inc':
            self.count += 1
        elif msg.tag == 'get':
            msg.reply_to.send(Message('value', self.count))


class Collector(Actor):
    def __init__(self, name, expect):
        super().__init__(name)
        self.values, self.expect = [], expect
        self.done = threading.Event()

    def on(self, msg):
        self.values.append(msg.body)
        if len(self.values) >= self.expect:
            self.done.set()


def bench_actors(n_senders, per_sender):
    c = Counter('counter').start()
    col = Collector('collector', 1).start()

    def sender():
        inc = Message('inc')
        for _ in range(per_sender):
            c.send(inc)

    t0 = time.perf_counter()
    ts = [threading.Thread(target=sender) for _ in range(n_senders)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    c.send(Message('get', reply_to=col))
    col.done.wait(30)
    dt = time.perf_counter() - t0
    got = col.values[0] if col.values else None
    c.send(STOP)
    col.send(STOP)
    return got, dt


def bench_lock(n_senders, per_sender):
    """The same total work with a shared counter and a lock."""
    lock = threading.Lock()
    box = [0]

    def worker():
        for _ in range(per_sender):
            with lock:
                box[0] += 1

    t0 = time.perf_counter()
    ts = [threading.Thread(target=worker) for _ in range(n_senders)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return box[0], time.perf_counter() - t0


def bench_racy(n_senders, per_sender):
    """No lock at all. In CPython the GIL usually hides the race; the point
    is that "usually" is not a guarantee and is not portable."""
    box = [0]

    def worker():
        for _ in range(per_sender):
            box[0] += 1

    t0 = time.perf_counter()
    ts = [threading.Thread(target=worker) for _ in range(n_senders)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return box[0], time.perf_counter() - t0


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    per = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    want = n * per

    print(f"; ---- {n} senders x {per} increments; correct answer {want} ----")
    print(f"  {'model':<22} {'answer':>10} {'time':>9}  {'msgs/s':>10}")
    for label, fn in (("actor (no shared state)", bench_actors),
                      ("shared + lock", bench_lock),
                      ("shared, no lock", bench_racy)):
        got, dt = fn(n, per)
        mark = '' if got == want else '   <- WRONG'
        print(f"  {label:<22} {got:>10} {dt:>8.3f}s  {want/dt:>10,.0f}{mark}")

    print()
    print("  The actor answer is always right and it is not the fastest.")
    print("  Read the ratio, not the ranking: what you are buying is that")
    print("  `self.count += 1` in Counter.on cannot be raced, by anyone,")
    print("  ever -- without a lock appearing anywhere in that class.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
