"""
Stack ADT — provided for Lab 7.
Do not modify this file.
"""


class Stack:
    """A standard stack (LIFO) backed by a Python list."""

    def __init__(self):
        self.items = []

    def push(self, item):
        """Push an item onto the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.items.pop()

    def peek(self):
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self.items[-1]

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items on the stack."""
        return len(self.items)

    def __str__(self):
        return f"Stack (top -> bottom): {self.items[::-1]}"
