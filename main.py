"""
main.py

Entry point for the Developer Snippet & Notes Manager.

Run with:
    python main.py

engine.py must contain your teammate's Note / LinkedList /
BinarySearchTree classes (real file from his branch, not the copy
included here for testing).
"""

from note_storage import BSTNoteStorage
from tag_hash_table import TagHashTable
from undo_stack import UndoStack
from menu import NoteManager, Menu


def main() -> None:
    storage = BSTNoteStorage()
    tag_table = TagHashTable()
    undo_stack = UndoStack()

    manager = NoteManager(storage, tag_table, undo_stack)
    menu = Menu(manager)
    menu.run()


if __name__ == "__main__":
    main()
