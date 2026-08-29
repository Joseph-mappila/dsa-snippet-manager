

from typing import List, Optional
from engine import Note


class UndoStack:
    

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
