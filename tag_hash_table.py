"""
tag_hash_table.py

Implements the project's tag database using a Python dict.

CHANGED FOR INTEGRATION WITH TEAMMATE'S engine.py:
    His Note class has no `id` field, so tag_database now maps
    tag -> list of TITLES (str) instead of note IDs. This works
    because his BST already uses title as the unique lookup key
    (search(title), in_order_traversal by title order), so title is
    already the de facto primary key for the whole project.

    His Note also stores only ONE tag string (`self.tag`), not a
    list. Rather than asking him to change his class, this file packs
    multiple tags into that single string as a comma-separated value
    (e.g. "cpp,algorithms,search") and unpacks it with parse_tags().
    This keeps his Note class untouched while still letting the menu
    demonstrate multi-tag search. If you'd rather he add a real
    tags: list[str] field later, swap pack_tags/parse_tags out - the
    rest of this file's logic won't need to change.

Design decision (Hash Table implementation):
    Python's dict IS a hash table (O(1) average lookup/insert/delete
    via internal hashing). Using it directly is the standard,
    idiomatic choice for a DSA course project unless the assignment
    explicitly requires a hand-rolled hash function + collision
    handling.
"""

from typing import Dict, List


def normalize_tag(tag: str) -> str:
    """Normalize a tag: strip whitespace, drop a leading '#', lowercase."""
    tag = tag.strip()
    if tag.startswith("#"):
        tag = tag[1:]
    return tag.lower()


def pack_tags(tags: List[str]) -> str:
    """Turn a list of tags into the single comma-separated string that
    fits into engine.Note's one `tag` field. Empty/duplicate tags are
    dropped and everything is normalized first."""
    seen: List[str] = []
    for t in tags:
        clean = normalize_tag(t)
        if clean and clean not in seen:
            seen.append(clean)
    return ",".join(seen)


def parse_tags(tag_field: str) -> List[str]:
    """Reverse of pack_tags(): split engine.Note.tag back into a clean
    list of normalized tags."""
    if not tag_field:
        return []
    return [normalize_tag(t) for t in tag_field.split(",") if normalize_tag(t)]


class TagHashTable:
    """Hash table mapping normalized tags -> list of note TITLES."""

    def __init__(self) -> None:
        self.tag_database: Dict[str, List[str]] = {}

    def add_tag(self, tag: str, title: str) -> None:
        """Associate a note title with tag. Prevents duplicate mappings."""
        key = normalize_tag(tag)
        if not key:
            return
        if key not in self.tag_database:
            self.tag_database[key] = []
        if title not in self.tag_database[key]:
            self.tag_database[key].append(title)

    def add_tags(self, tags: List[str], title: str) -> None:
        """Convenience method: add several tags for one note at once."""
        for tag in tags:
            self.add_tag(tag, title)

    def remove_tag(self, tag: str, title: str) -> None:
        """Remove a note title from a single tag's mapping.

        If the tag has no titles left afterwards, the tag entry
        itself is removed from the dict to keep it clean.
        """
        key = normalize_tag(tag)
        if key not in self.tag_database:
            return
        if title in self.tag_database[key]:
            self.tag_database[key].remove(title)
        if not self.tag_database[key]:
            del self.tag_database[key]

    def remove_note(self, title: str, tags: List[str]) -> None:
        """Remove a note title from every tag it was associated with.

        Called on delete. 'tags' should be the note's tags AT THE TIME
        OF DELETION - this is exactly why the Undo Stack keeps the
        whole Note (its .tag field), so those tags can be re-parsed
        and restored on undo.
        """
        for tag in tags:
            self.remove_tag(tag, title)

    def get_titles_for_tag(self, tag: str) -> List[str]:
        """Return the list of note titles associated with a tag.
        Returns an empty list if the tag does not exist."""
        key = normalize_tag(tag)
        return list(self.tag_database.get(key, []))

    def tag_exists(self, tag: str) -> bool:
        return normalize_tag(tag) in self.tag_database
