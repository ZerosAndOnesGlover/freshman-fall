#!/usr/bin/env python3
"""
hash_table_starter.py
CS 101 — Week 8, Lab 8 Starter

Two complete hash table implementations: chaining and open addressing.
Fill in every TODO.

Student: ____________________________
Date: ______________________________
"""


class ChainedHashTable:
    """
    Hash table using separate chaining for collision resolution.
    Automatically resizes (doubles) when load factor exceeds 0.75.
    """

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._buckets = [[] for _ in range(self._size)]
        self._count = 0
        self._max_load_factor = 0.75

        # Instrumentation for this lab:
        self.total_comparisons = 0
        self.resize_count = 0

    def _index(self, key, size=None):
        size = size if size is not None else self._size
        return hash(key) % size

    def load_factor(self):
        return self._count / self._size

    def _resize(self):
        """
        Double the bucket array and re-insert every element. O(n).

        CRITICAL: you cannot just copy the old buckets — every key's
        index must be RECOMPUTED using the new size, since
        hash(key) % new_size generally differs from hash(key) % old_size.
        """
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [[] for _ in range(self._size)]
        self.resize_count += 1

        # TODO: for each chain in old_buckets, for each (key, value) in
        # that chain, compute the NEW index and append to self._buckets
        pass

    def put(self, key, value):
        """
        Insert or update key -> value. Resize if load factor exceeds threshold.
        """
        idx = self._index(key)
        chain = self._buckets[idx]

        # TODO: scan the chain for an existing key (update case).
        # Increment self.total_comparisons for EACH key comparison made.
        # If found: update its value and return.

        # TODO: not found — append new (key, value) entry, increment
        # self._count, then check if load_factor() exceeds threshold
        # and call self._resize() if so.
        pass

    def get(self, key):
        """Retrieve value for key. Raise KeyError if not found."""
        idx = self._index(key)
        chain = self._buckets[idx]

        # TODO: scan the chain, incrementing self.total_comparisons
        # for each comparison. Return the value if found.

        raise KeyError(key)

    def contains(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def __len__(self):
        return self._count

    def max_chain_length(self):
        """Return the length of the longest chain — a diagnostic tool."""
        return max(len(chain) for chain in self._buckets)


class OpenAddressingHashTable:
    """
    Hash table using linear probing for collision resolution.
    Automatically resizes (doubles) when load factor exceeds 0.5.
    """

    _EMPTY = object()
    _DELETED = object()

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._keys = [self._EMPTY] * self._size
        self._values = [None] * self._size
        self._count = 0
        self._max_load_factor = 0.5

        self.total_probes = 0
        self.resize_count = 0

    def _index(self, key, size=None):
        size = size if size is not None else self._size
        return hash(key) % size

    def load_factor(self):
        return self._count / self._size

    def _resize(self):
        """Double the table and re-insert every valid element."""
        old_keys = self._keys
        old_values = self._values
        self._size *= 2
        self._keys = [self._EMPTY] * self._size
        self._values = [None] * self._size
        self._count = 0
        self.resize_count += 1

        # TODO: for each (k, v) in zip(old_keys, old_values), if k is
        # not _EMPTY and not _DELETED, re-insert via self.put(k, v)
        pass

    def put(self, key, value):
        """
        Insert or update key -> value using linear probing.

        Check load factor and resize BEFORE inserting (so the new
        element is inserted into the resized table if a resize occurs).
        """
        if self.load_factor() >= self._max_load_factor:
            self._resize()

        idx = self._index(key)
        start_idx = idx

        # TODO: probe (linear: idx = (idx+1) % self._size) until you find
        # either the existing key (update case) or an _EMPTY/_DELETED slot
        # (insert case). Increment self.total_probes for each slot examined.
        # Guard against an infinite loop if the table is somehow full
        # (shouldn't happen given the resize check above, but check
        # `if idx == start_idx: raise Exception("Hash table is full!")`
        # after each probe step, just in case).

        pass

    def get(self, key):
        """Retrieve value for key using linear probing. Raise KeyError if absent."""
        idx = self._index(key)
        start_idx = idx

        # TODO: probe until finding the key (return its value) or an
        # _EMPTY slot (meaning: definitely not present, raise KeyError).
        # Skip over _DELETED slots without stopping (that's the whole
        # point of tombstones!). Increment self.total_probes each step.

        raise KeyError(key)

    def contains(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def remove(self, key):
        """Mark the slot containing key as _DELETED (a tombstone)."""
        idx = self._index(key)
        start_idx = idx

        # TODO: probe until finding the key (mark _DELETED, decrement
        # count, return) or hitting an _EMPTY slot (raise KeyError)

        raise KeyError(key)

    def __len__(self):
        return self._count


def run_tests():
    """Verify both implementations are correct."""

    # ── ChainedHashTable ──────────────────────────────────────────────────
    cht = ChainedHashTable(initial_size=4)
    cht.put("apple", 1)
    cht.put("banana", 2)
    cht.put("cherry", 3)
    assert cht.get("apple") == 1
    assert cht.get("banana") == 2
    assert cht.contains("date") == False
    assert len(cht) == 3
    cht.put("apple", 100)   # update, not new
    assert cht.get("apple") == 100
    assert len(cht) == 3
    print("✓ ChainedHashTable basic operations")

    cht2 = ChainedHashTable(initial_size=4)
    for i in range(50):
        cht2.put(f"key{i}", i)
    assert len(cht2) == 50
    assert cht2.resize_count > 0, "Should have resized at least once by n=50"
    for i in range(50):
        assert cht2.get(f"key{i}") == i, f"Lost data for key{i} after resize!"
    print(f"✓ ChainedHashTable resize integrity (resized {cht2.resize_count} times)")

    # ── OpenAddressingHashTable ───────────────────────────────────────────
    oht = OpenAddressingHashTable(initial_size=8)
    oht.put("apple", 1)
    oht.put("banana", 2)
    oht.put("cherry", 3)
    assert oht.get("apple") == 1
    assert oht.contains("date") == False
    oht.remove("banana")
    assert len(oht) == 2
    try:
        oht.get("banana")
        assert False, "should have raised KeyError"
    except KeyError:
        pass
    print("✓ OpenAddressingHashTable basic operations + tombstone removal")

    oht2 = OpenAddressingHashTable(initial_size=4)
    for i in range(50):
        oht2.put(f"key{i}", i)
    assert len(oht2) == 50
    for i in range(50):
        assert oht2.get(f"key{i}") == i, f"Lost data for key{i} after resize!"
    print(f"✓ OpenAddressingHashTable resize integrity (resized {oht2.resize_count} times)")

    print("\n🎉 All hash table tests passed!")


if __name__ == "__main__":
    run_tests()
