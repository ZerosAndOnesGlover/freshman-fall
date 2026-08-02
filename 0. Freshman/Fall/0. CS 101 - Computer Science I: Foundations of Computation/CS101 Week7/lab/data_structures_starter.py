#!/usr/bin/env python3
"""
data_structures.py
CS 101 — Week 7, Lab 7 Starter

Complete implementations: Node, LinkedList, DoublyLinkedList, Stack, Queue.
Fill in every TODO, then run this file to check your work.

Student: ____________________________
Date: ______________________________
"""

from collections import deque


class Node:
    """A node in a singly linked list."""
    __slots__ = ("data", "next")

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    """
    Singly linked list with head AND tail pointers (enables O(1) append).
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def append(self, data):
        """
        Insert data at the end. O(1) thanks to the tail pointer.

        Cases to handle:
        - Empty list: new node becomes both head and tail
        - Non-empty list: link old tail's .next to the new node, update tail
        """
        # TODO
        pass

    def prepend(self, data):
        """
        Insert data at the front. O(1).

        Cases to handle:
        - Empty list: new node becomes both head and tail
        - Non-empty list: new node's .next = old head, update head
        """
        # TODO
        pass

    def find(self, target):
        """
        Return True if target is anywhere in the list. O(n).
        """
        # TODO: traverse from head, compare .data at each node
        pass

    def remove(self, target):
        """
        Remove the FIRST occurrence of target. Return True if removed,
        False if not found. O(n).

        Special cases to handle:
        - target is at the head (update self.head)
        - target is at the tail (update self.tail!)
        - list becomes empty after removal (both head and tail become None)
        """
        # TODO
        pass

    def get(self, index):
        """
        Return the data at position index (0-based). O(n).
        Raises IndexError if index is out of range.
        """
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        # TODO: traverse from head, counting positions until you reach index
        pass

    def to_list(self):
        """Convert to a Python list. O(n)."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __repr__(self):
        return " -> ".join(str(x) for x in self.to_list()) + " -> None"


class DNode:
    """A node in a doubly linked list."""
    __slots__ = ("data", "prev", "next")

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    """
    Doubly linked list with head and tail pointers.
    Enables O(1) removal from EITHER end.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, data):
        """
        Insert at the end. O(1).

        new_node.prev should point to the OLD tail.
        Update the old tail's .next to point to new_node (if list wasn't empty).
        Update self.tail to new_node. Update self.head too if list was empty.
        """
        # TODO
        pass

    def prepend(self, data):
        """
        Insert at the front. O(1). Mirror image of append().
        """
        # TODO
        pass

    def remove_last(self):
        """
        Remove and return the last element. O(1).
        Raises IndexError if empty.

        Key step: self.tail = self.tail.prev
        Then: if the new tail is None, the list is now empty (update self.head too)
              else: the new tail's .next must be set to None
        """
        if self.tail is None:
            raise IndexError("remove from empty list")
        # TODO
        pass

    def remove_first(self):
        """
        Remove and return the first element. O(1). Mirror image of remove_last().
        """
        if self.head is None:
            raise IndexError("remove from empty list")
        # TODO
        pass

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_list_reversed(self):
        """Traverse backward from the tail."""
        result = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result


class Stack:
    """
    Stack ADT backed by a Python list.
    Design choice: the END of the list is the "top" (both O(1) operations).
    """

    def __init__(self):
        self._data = []

    def push(self, x):
        """Add x to the top. O(1) amortized."""
        # TODO
        pass

    def pop(self):
        """
        Remove and return the top element. O(1).
        Raise IndexError("pop from empty stack") if empty.
        """
        # TODO
        pass

    def peek(self):
        """
        Return the top element without removing it. O(1).
        Raise IndexError("peek from empty stack") if empty.
        """
        # TODO
        pass

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack({self._data})"


class Queue:
    """
    Queue ADT backed by collections.deque.
    Design choice: enqueue at the RIGHT end, dequeue from the LEFT end
    — both O(1) thanks to deque's internal doubly-linked-block structure.
    """

    def __init__(self):
        self._data = deque()

    def enqueue(self, x):
        """Add to the back. O(1)."""
        # TODO
        pass

    def dequeue(self):
        """
        Remove and return from the front. O(1).
        Raise IndexError("dequeue from empty queue") if empty.
        """
        # TODO
        pass

    def peek(self):
        """
        Return the front element without removing it. O(1).
        Raise IndexError("peek from empty queue") if empty.
        """
        # TODO
        pass

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


def run_tests():
    """Verify all implementations are correct."""

    # ── LinkedList tests ──────────────────────────────────────────────────
    ll = LinkedList()
    assert ll.is_empty()
    ll.append(10); ll.append(20); ll.append(30)
    assert ll.to_list() == [10, 20, 30], f"got {ll.to_list()}"
    ll.prepend(5)
    assert ll.to_list() == [5, 10, 20, 30]
    assert ll.find(20) == True
    assert ll.find(99) == False
    assert ll.get(0) == 5
    assert ll.get(2) == 20
    assert len(ll) == 4
    ll.remove(20)
    assert ll.to_list() == [5, 10, 30]
    assert len(ll) == 3
    # Test removing the tail correctly updates self.tail:
    ll.remove(30)
    assert ll.to_list() == [5, 10]
    ll.append(99)   # this MUST work correctly — tests that .tail was updated!
    assert ll.to_list() == [5, 10, 99], "tail pointer wasn't updated after removing old tail!"
    print("✓ LinkedList")

    # ── DoublyLinkedList tests ────────────────────────────────────────────
    dll = DoublyLinkedList()
    dll.append(1); dll.append(2); dll.append(3)
    assert dll.to_list() == [1, 2, 3]
    assert dll.to_list_reversed() == [3, 2, 1]
    assert dll.remove_last() == 3
    assert dll.to_list() == [1, 2]
    assert dll.remove_first() == 1
    assert dll.to_list() == [2]
    dll.prepend(0)
    assert dll.to_list() == [0, 2]
    print("✓ DoublyLinkedList")

    # ── Stack tests ────────────────────────────────────────────────────────
    s = Stack()
    assert s.is_empty()
    s.push(1); s.push(2); s.push(3)
    assert s.pop() == 3
    assert s.peek() == 2
    assert s.size() == 2
    try:
        empty_stack = Stack()
        empty_stack.pop()
        assert False, "should have raised IndexError"
    except IndexError:
        pass
    print("✓ Stack")

    # ── Queue tests ────────────────────────────────────────────────────────
    q = Queue()
    assert q.is_empty()
    q.enqueue(1); q.enqueue(2); q.enqueue(3)
    assert q.dequeue() == 1
    assert q.peek() == 2
    assert q.size() == 2
    try:
        empty_queue = Queue()
        empty_queue.dequeue()
        assert False, "should have raised IndexError"
    except IndexError:
        pass
    print("✓ Queue")

    print("\n🎉 All data structure tests passed!")


if __name__ == "__main__":
    run_tests()
