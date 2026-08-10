# CS 201 · Week 8 · Summary

**Topic —** Networks: the layered model, TCP's reliability and congestion machinery, and the cost of a round trip.
**Lectures —** L25 Layers and the Latency Ladder; L26 TCP — Reliability, Flow and Congestion; L27 The Application Layer and the Cost of a Round Trip.
**Work —** PS 8 (100, due Week 9), Lab 8 (unmarked, sat Tuesday of Week 9), Quiz 8 Monday covering Week 7 (unmarked, key in the paper). **Project 1 due Week 9.**
**Takeaway —** A flag's cost is a property of the workload, not the flag. `TCP_NODELAY` changed a send-then-receive loop by 3% (18.6 → 19.1 μs) and a write-write-read loop by 1350× (30.4 μs → 41,068 μs) on the same machine minutes apart — and 41 ms is not a slow network but Linux's delayed-ACK timer, with Nagle holding the second small write while the receiver holds its ACK, each waiting for the other. The ladder now spans 500 million: L1 at 1.2 ns to a 589 ms HTTPS page load, of which ~582 ms was three round trips and the server's own work was invisible. A loopback round trip at 84 μs is faster than an SSD read; cold DNS cost 1487 ms against 3 ms warm. And message size dominated again exactly as it did for storage — 64 B gave 6.6 MiB/s and 64 KiB gave 2436 MiB/s on the same socket.
**Next —** Week 9 — security, where Week 3's stack and this week's protocols are attacked.
