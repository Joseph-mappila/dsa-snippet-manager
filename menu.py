"""
Ties together primary storage (BSTNoteStorage, wrapping your
teammate's real BST), the tag hash table, and the undo stack.
"""

from typing import List, Optional

from engine import Note
from note_storage import NoteStorage
from tag_hash_table import TagHashTable, normalize_tag, pack_tags, parse_tags
from undo_stack import UndoStack


class NoteManager:
    """Coordinates storage, tags, and undo for every note operation."""

    def __init__(self, storage: NoteStorage, tag_table: TagHashTable, undo_stack: UndoStack) -> None:
        self.storage = storage
        self.tag_table = tag_table
        self.undo_stack = undo_stack

    def add_note(self, title: str, content: str, tags: List[str]) -> Note:
        tag_field = pack_tags(tags)
        note = Note(title=title, content=content, tag=tag_field)
        self.storage.insert(note)
        self.tag_table.add_tags(parse_tags(note.tag), note.title)
        return note

    def search_note(self, title: str) -> Optional[Note]:
        return self.storage.search(title)

    def delete_note(self, title: str) -> bool:
        note = self.storage.delete(title)
        if note is None:
            return False
        self.tag_table.remove_note(note.title, parse_tags(note.tag))
        self.undo_stack.push(note)
        return True

    def undo_last_delete(self) -> Optional[Note]:
        note = self.undo_stack.pop()
        if note is None:
            return None
        self.storage.reinsert(note)
        self.tag_table.add_tags(parse_tags(note.tag), note.title)
        return note

    def display_all_notes(self) -> List[Note]:
        return self.storage.get_all()

    def search_by_tag(self, tag: str) -> List[Note]:
        titles = self.tag_table.get_titles_for_tag(tag)
        notes = []
        for title in titles:
            note = self.storage.search(title)
            if note is not None:
                notes.append(note)
        return notes


class Menu:
    """Runs the continuous terminal menu loop and handles user I/O."""

    def __init__(self, manager: NoteManager) -> None:
        self.manager = manager

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Enter choice: ").strip()

            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                self._handle_add_note()
            elif choice == "2":
                self._handle_search_note()
            elif choice == "3":
                self._handle_delete_note()
            elif choice == "4":
                self._handle_undo()
            elif choice == "5":
                self._handle_display_all()
            elif choice == "6":
                self._handle_search_by_tag()
            else:
                print("Invalid choice. Please try again.\n")

    def _print_menu(self) -> None:
        print("========================================")
        print("    DEVELOPER SNIPPET & NOTES MANAGER")
        print("========================================")
        print("1. Add Note / Code Snippet")
        print("2. Search Note")
        print("3. Delete Note")
        print("4. Undo Last Delete")
        print("5. Display All Notes")
        print("6. Search Notes by Tag")
        print("0. Exit")
        print()

    def _print_note(self, note: Note) -> None:
        tags = parse_tags(note.tag)
        tag_str = ", ".join(tags) if tags else "(none)"
        print(f"Title: {note.title}")
        print(f"Content: {note.content}")
        print(f"Tags: {tag_str}")

    def _handle_add_note(self) -> None:
        title = input("Title: ").strip()
        if not title:
            print("Title cannot be empty.\n")
            return
        content = input("Content: ").strip()
        raw_tags = input("Tags (comma-separated): ").strip()
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

        note = self.manager.add_note(title, content, tags)
        print("\nNote added:")
        self._print_note(note)
        print()

    def _handle_search_note(self) -> None:
        title = input("Enter title to search: ").strip()
        note = self.manager.search_note(title)
        if note is None:
            print("Note not found.\n")
        else:
            print()
            self._print_note(note)
            print()

    def _handle_delete_note(self) -> None:
        title = input("Enter title to delete: ").strip()
        deleted = self.manager.delete_note(title)
        if deleted:
            print(f"'{title}' deleted.\n")
        else:
            print("Note not found.\n")

    def _handle_undo(self) -> None:
        note = self.manager.undo_last_delete()
        if note is None:
            print("Nothing to undo.\n")
        else:
            print(f"\n{note.title} restored successfully.\n")

    def _handle_display_all(self) -> None:
        notes = self.manager.display_all_notes()
        if not notes:
            print("No notes stored yet.\n")
            return
        for note in notes:
            self._print_note(note)
            print("-" * 40)
        print()

    def _handle_search_by_tag(self) -> None:
        tag = input("Enter tag: ").strip()
        if not tag:
            print("Tag cannot be empty.\n")
            return
        notes = self.manager.search_by_tag(tag)
        clean = normalize_tag(tag)
        if not notes:
            print(f"No notes found for #{clean}.\n")
            return
        print(f"\nNotes tagged #{clean}:\n")
        for i, note in enumerate(notes, start=1):
            print(f"{i}. {note.title}")
        print()
