#!/bin/bash
# midterm1_check.sh: every number in Midterm 1's mark scheme, computed.
# CS 202 · INSTRUCTOR ONLY. Run from anywhere:  bash midterm1_check.sh
set -e
C="$(cd "$(dirname "$0")/../.." && pwd)"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
gcc -O2 -w -o "$T/schedsim" "$C/CS202 Week2/solutions_instructor/schedsim reference (do not distribute).c"
gcc -O2 -w -o "$T/rtsim" "$C/CS202 Week2/resources/rtsim.c" -lm

echo "== Q3(a): A 0 8, B 1 4, C 2 9, D 3 5"
printf 'A 0 8\nB 1 4\nC 2 9\nD 3 5\n' > "$T/q3.txt"
for p in fcfs srtf rr:4; do "$T/schedsim" $p < "$T/q3.txt" | sed -n '1p;3,7p'; done

echo "== Q3(d): rate-monotonic, 1/4 2/5 2/10"
"$T/rtsim" rm "1/4 2/5 2/10"
"$T/rtsim" edf "1/4 2/5 2/10" | tail -1

python3 - <<'PY'
import math
fails = 0
def check(name, got, want, tol=1e-9):
    global fails
    ok = abs(got - want) <= tol * max(1, abs(want))
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {got} (expected {want})")

# Q1(c): an 8 MiB file read at 600 ns per read() call, including the read that returns 0
size = 8 * 1024 * 1024
calls_1 = size + 1
calls_4096 = size // 4096 + 1
check("Q1(c) calls, 1-byte buffer", calls_1, 8388609)
check("Q1(c) calls, 4096-byte buffer", calls_4096, 2049)
check("Q1(c) seconds, 1-byte", round(calls_1 * 600e-9, 3), 5.033)
check("Q1(c) milliseconds, 4096-byte", round(calls_4096 * 600e-6, 2), 1.23)

# Q2(c): ping-pong -- 100,000 rounds, 0.60 s, baseline pair 1,500 ns, 200,000 switches
switch = (0.60 - 2 * 100000 * 1500e-9) / 200000
check("Q2(c) microseconds per switch", round(switch * 1e6, 3), 1.5)

# Q2(d): each process should reach 2,500,000; the pair must sum to 5,000,000
check("Q2(d) the other process", 5_000_000 - 4_212_345, 787_655)

# Q3(c): nice 0, 5, 10 -> weights 1024, 335, 110
w = [1024, 335, 110]
shares = [round(100 * x / sum(w), 1) for x in w]
check("Q3(c) nice 0 share %", shares[0], 69.7)
check("Q3(c) nice 5 share %", shares[1], 22.8)
check("Q3(c) nice 10 share %", shares[2], 7.5)

# Q3(d): response-time analysis for task 3 (C=2, P=10) against 1/4 and 2/5
R = 2
while True:
    nxt = 2 + math.ceil(R / 4) * 1 + math.ceil(R / 5) * 2
    if nxt == R: break
    R = nxt
check("Q3(d) task 3 worst-case response", R, 8)
U = 1/4 + 2/5 + 2/10
check("Q3(d) utilisation", round(U, 3), 0.85)
check("Q3(d) Liu-Layland bound n=3", round(3 * (2 ** (1/3) - 1), 3), 0.780)

# Q4(a): balance 100, deposits of 20 and 30 racing
check("Q4(a) correct final balance", 100 + 20 + 30, 150)

# Q4(b): three-state futex trace -- futex calls: two waits, three wakes
check("Q4(b) futex system calls", 2 + 3, 5)

# Q5(c): 64 processes polled every millisecond at 600 ns per call, for one second
check("Q5(c) ms of CPU per second, one call per process", round(64 * 1000 * 600e-9 * 1000, 1), 38.4)
check("Q5(c) ms of CPU per second, one call for all", round(1000 * 600e-9 * 1000, 1), 0.6)
print("ALL CHECKS PASSED" if fails == 0 else f"{fails} CHECK(S) FAILED")
raise SystemExit(fails)
PY
