#!/usr/bin/env python3
"""Summarise a JVM `-Xlog:gc` stream: pause distribution, not pause total.

    java -XX:+UseG1GC -Xlog:gc -Xmx256m Churn 40000000 7 2>&1 | python3 pauses.py G1

Why percentiles and not a mean.  A collector that stops the world for 200 ms
once per minute and one that stops it for 0.5 ms four hundred times per
minute can report the same "3% of time spent in GC".  For a batch job they
are equivalent.  For anything a person is waiting on -- a request, a frame, a
keystroke -- they are not remotely equivalent, and the difference does not
appear in the mean.  It appears in the maximum, and in p99.

**Read the occupancy numbers too.**  `33M->1M(117M)` says the heap held 33 MB
before this collection and 1 MB after: 97% of what was there was garbage.
That figure is the generational hypothesis, measured, on somebody else's
runtime -- and it is why the young collection was cheap despite the heap
being large.
"""
import re
import sys

# [0.410s][info][gc] GC(64) Pause Young (Allocation Failure) 33M->1M(117M) 0.342ms
PAUSE = re.compile(r'\]\s*GC\(\d+\)\s+(?P<what>.*?)\s+'
                   r'(?:(?P<before>\d+)M->(?P<after>\d+)M\((?P<cap>\d+)M\)\s+)?'
                   r'(?P<t>[\d.]+)(?P<unit>ms|s)\s*$')

KINDS = (('Full', 'full'), ('Major', 'major'), ('Minor', 'minor'),
         ('Young', 'young'), ('Concurrent', 'concurrent'), ('Pause', 'pause'))


def classify(what):
    for needle, name in KINDS:
        if needle in what:
            return name
    return 'other'


def pct(xs, p):
    if not xs:
        return 0.0
    s = sorted(xs)
    i = min(len(s) - 1, int(round((p / 100) * (len(s) - 1))))
    return s[i]


def main(argv):
    label = argv[1] if len(argv) > 1 else 'gc'
    events, reclaimed = [], []
    for line in sys.stdin:
        m = PAUSE.search(line.rstrip())
        if not m:
            continue
        ms = float(m['t']) * (1000 if m['unit'] == 's' else 1)
        events.append((classify(m['what']), ms))
        if m['before'] is not None:
            b, a = int(m['before']), int(m['after'])
            if b:
                reclaimed.append((b - a) / b)

    if not events:
        print(f"{label}: no GC events found -- was -Xlog:gc passed?")
        return 1

    allms = [ms for _, ms in events]
    print(f"; ---- {label} ----")
    print(f"  events   {len(events):>6}      total {sum(allms):>8.1f} ms")
    print(f"  mean     {sum(allms) / len(allms):>6.3f} ms   "
          f"p50 {pct(allms, 50):>6.3f}   p99 {pct(allms, 99):>7.3f}   "
          f"max {max(allms):>7.3f}")
    by = {}
    for kind, ms in events:
        by.setdefault(kind, []).append(ms)
    for kind in sorted(by):
        v = by[kind]
        print(f"    {kind:<11} {len(v):>5}   mean {sum(v) / len(v):>7.3f} ms"
              f"   max {max(v):>8.3f} ms")
    if reclaimed:
        print(f"  reclaimed per collection: "
              f"mean {100 * sum(reclaimed) / len(reclaimed):.1f}% of the "
              f"occupied heap, worst {100 * min(reclaimed):.1f}%")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
