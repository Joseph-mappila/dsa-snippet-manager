"""
undo_stack.py

Implements a LIFO Stack used exclusively for the "Undo Last Delete"
feature. Works with your teammate's engine.Note unchanged - the stack
never cared about a note's internal fields, only that it can hold a
whole object and hand it back later.

Data ownership decision:
    The stack stores the COMPLETE Note object that was deleted. A
    deleted note is removed entirely from the BST, so the Stack is
    the only place left that remembers it. A note popped off the
    stack is immediately reinserted into storage and never left
    sitting in two places at once, so there's no risk of stale
    duplicate copies.
"""

from typing import List, Optional
from engine import Note


class UndoStack:
    """A simple LIFO stack of deleted Notes.

    Built on a Python list: list.append() / list.pop() are both O(1)
    amortized, which is exactly stack behavior. A manual linked-list
    stack wasn't used since the Linked List data structure is already
    separately demonstrated in engine.py.
    """

    def __init__(self) -> None:
        self._items: List[Note] = []

    def push(self, note: Note) -> None:
        """Push a deleted Note onto the stack."""
        self._items.append(note)

    def pop(self) -> Optional[Note]:
        """Remove and return the most recently deleted Note.
        Returns None if empty instead of raising."""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self) -> Optional[Note]:
        """Return the most recently deleted Note without removing it."""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)
