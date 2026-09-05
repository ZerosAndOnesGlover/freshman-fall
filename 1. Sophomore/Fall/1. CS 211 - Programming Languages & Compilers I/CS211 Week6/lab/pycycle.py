#!/usr/bin/env python3
"""Lab 6 Part C.  cycle.cy, but in a language you did not write.

CPython is a reference-counted runtime.  It has exactly the incompleteness
L13 section 8 describes, and it ships a second collector -- a tracing one --
purely to clean up after the first.  This script shows both facts on the
interpreter you have been using all term.

    python3 pycycle.py
"""
import gc
import sys


class Node:
    __slots__ = ('name', 'link')

    def __init__(self, name):
        self.name = name
        self.link = None


def make_acyclic():
    a = Node('a')
    b = Node('b')
    a.link = b          # a -> b, and nothing points back
    return None


def make_cycle():
    a = Node('a')
    b = Node('b')
    a.link = b
    b.link = a          # the back edge is the whole difference
    return None


def count_nodes():
    return sum(1 for o in gc.get_objects() if isinstance(o, Node))


def trial(label, build, n):
    gc.collect()
    before = count_nodes()
    for _ in range(n):
        build()
    leaked = count_nodes() - before
    freed = gc.collect()
    after = count_nodes() - before
    print(f"  {label:<22} built {2 * n:>4} nodes   "
          f"refcounting left {leaked:>4} alive   "
          f"gc.collect() then freed {leaked - after:>4}")


def main():
    print(f"; ---- CPython {sys.version.split()[0]} ----")
    print("; reference counting is the primary collector; gc is the backup")
    print()

    gc.disable()        # turn OFF the tracing collector; refcounting remains
    print("; with gc DISABLED -- reference counting alone")
    trial("no cycle", make_acyclic, 100)
    trial("cycle", make_cycle, 100)
    print()

    gc.enable()
    print("; with gc ENABLED -- the cycle collector runs on its own schedule")
    gc.collect()
    before = count_nodes()
    for _ in range(10_000):
        make_cycle()
    print(f"  10000 cycles built     {count_nodes() - before:>5} nodes still "
          f"alive without an explicit collect")
    freed = gc.collect()
    print(f"  gc.collect() freed     {freed:>5} objects; "
          f"{count_nodes() - before:>4} nodes remain")
    print()
    print("; thresholds -- how many net allocations trigger each generation")
    print(f"  gc.get_threshold() = {gc.get_threshold()}")
    print(f"  gc.get_count()     = {gc.get_count()}")


if __name__ == '__main__':
    main()
