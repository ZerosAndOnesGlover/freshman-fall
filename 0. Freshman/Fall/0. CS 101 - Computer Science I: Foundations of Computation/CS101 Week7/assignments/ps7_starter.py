#!/usr/bin/env python3
"""
ps7.py
CS 101 — Problem Set 7: Stacks, Queues, and Linked Structures
Due Friday 20 November 2026, 17:00

Student: ____________________________

State each method's cost in a comment. pop/peek/dequeue raise IndexError when empty.
"""
from collections import deque
import timeit


# --- B1: List-based -----------------------------------------------------------
class ArrayStack:
    """TODO: which end of the list is the top, and why?"""
    def __init__(self):
        self._items = []
    # TODO: push, pop, peek, is_empty, __len__


class ArrayQueue:
    """Queue on collections.deque."""
    def __init__(self):
        self._items = deque()
    # TODO: enqueue, dequeue, is_empty, __len__


class NaiveArrayQueue:
    """Queue on a raw list; dequeue uses pop(0)."""
    def __init__(self):
        self._items = []
    # TODO: enqueue, dequeue, is_empty, __len__


# --- B2: Linked ---------------------------------------------------------------
class _Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedStack:
    """Top = head."""
    # TODO


class LinkedQueue:
    """head and tail; enqueue at the tail, dequeue at the head. Why not the reverse?"""
    # TODO


# --- B3: LinkedList -----------------------------------------------------------
class LinkedList:
    # TODO: __init__(items=()), append, to_list, count, reverse, remove_duplicates
    pass


# --- B4: Timing ---------------------------------------------------------------
# TODO: for n in [1000, 5000, 20000, 50000], time n enqueues + n dequeues on each queue
#       with timeit (as in L24's exercise) and print both times and the ratio.


# --- B5: Two-stack evaluation -------------------------------------------------
def tokenize(expression):
    """TODO"""
    pass


def evaluate(expression):
    """TODO — operand stack + operator stack; ')' pops one operator and two operands."""
    pass
