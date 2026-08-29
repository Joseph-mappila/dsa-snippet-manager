"""
note_storage.py

Adapter that wraps your teammate's REAL BinarySearchTree (and
LinkedList) from engine.py, exposing the interface my Menu/NoteManager
code needs. This replaces the old placeholder SimpleNoteStorage now
that his actual classes are available.

ARCHITECTURE ASSUMPTION (confirm with your teammate):
    The BST is treated as PRIMARY storage - it's what search(),
    delete(), and get_all() operate on, since it's the only structure
    of his that supports search() and ordered traversal.

    The LinkedList is treated as an append-only INSERTION HISTORY that
    mirrors every note ever added (for demonstrating the linear data
    structure), and is NOT touched on delete/undo. If he intends the
    LinkedList to be used differently (e.g. as the actual delete-aware
    primary store, with the BST as a secondary index), this adapter
    will need to change - his code doesn't specify how the two are
    meant to combine, so this is my best guess, not a fact.

WHY DELETE IS A REBUILD (stopgap, not a permanent design):
    BinarySearchTree in engine.py has insert(), search(), and
    in_order_traversal() but no delete(). Proper BST node deletion
    (handling the 0/1/2-children cases, successor promotion, etc.) is
    a core BST operation and should be implemented by whoever owns
    the BST. Until then, delete() below works ONLY through his
    existing public methods: read out every note in order, drop the
    one being deleted, and reinsert the rest into a fresh tree. This
    is correct but O(n) instead of O(h) - fine for a small note
    collection in a class project, but flag this to your teammate as
    something to eventually replace with real BST deletion.
"""

from typing import List, Optional
from engine import Note, BinarySearchTree, LinkedList


class NoteStorage:
    """Abstract interface my Menu/NoteManager code depends on."""

    def insert(self, note: Note) -> None:
        raise NotImplementedError

    def search(self, title: str) -> Optional[Note]:
        raise NotImplementedError

    def delete(self, title: str) -> Optional[Note]:
        raise NotImplementedError

    def get_all(self) -> List[Note]:
        raise NotImplementedError

    def reinsert(self, note: Note) -> None:
        self.insert(note)


class BSTNoteStorage(NoteStorage):
    """Adapter around the teammate's real BinarySearchTree + LinkedList."""

    def __init__(self) -> None:
        self.bst = BinarySearchTree()
        self.history = LinkedList()  # append-only insertion log

    def insert(self, note: Note) -> None:
        self.bst.insert(note)
        self.history.append(note)

    def search(self, title: str) -> Optional[Note]:
        return self.bst.search(title)

    def delete(self, title: str) -> Optional[Note]:
        target = self.bst.search(title)
        if target is None:
            return None

        # Stopgap rebuild - see module docstring.
        remaining = [n for n in self.bst.in_order_traversal() if n.title != target.title]
        rebuilt = BinarySearchTree()
        for n in remaining:
            rebuilt.insert(n)
        self.bst = rebuilt
        return target

    def get_all(self) -> List[Note]:
        return self.bst.in_order_traversal()

    def reinsert(self, note: Note) -> None:
        # Undo should NOT re-append to history (it was never truly
        # removed from the insertion log), only back into the BST.
        self.bst.insert(note)
