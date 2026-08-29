
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

    
        remaining = [n for n in self.bst.in_order_traversal() if n.title != target.title]
        rebuilt = BinarySearchTree()
        for n in remaining:
            rebuilt.insert(n)
        self.bst = rebuilt
        return target

    def get_all(self) -> List[Note]:
        return self.bst.in_order_traversal()

    def reinsert(self, note: Note) -> None:

        self.bst.insert(note)
