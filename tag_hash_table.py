
from typing import Dict, List


def normalize_tag(tag: str) -> str:
    """Normalize a tag: strip whitespace, drop a leading '#', lowercase."""
    tag = tag.strip()
    if tag.startswith("#"):
        tag = tag[1:]
    return tag.lower()


def pack_tags(tags: List[str]) -> str:
    
    seen: List[str] = []
    for t in tags:
        clean = normalize_tag(t)
        if clean and clean not in seen:
            seen.append(clean)
    return ",".join(seen)


def parse_tags(tag_field: str) -> List[str]:
    
    if not tag_field:
        return []
    return [normalize_tag(t) for t in tag_field.split(",") if normalize_tag(t)]


class TagHashTable:
    """Hash table mapping normalized tags -> list of note TITLES."""

    def __init__(self) -> None:
        self.tag_database: Dict[str, List[str]] = {}

    def add_tag(self, tag: str, title: str) -> None:
       
        key = normalize_tag(tag)
        if not key:
            return
        if key not in self.tag_database:
            self.tag_database[key] = []
        if title not in self.tag_database[key]:
            self.tag_database[key].append(title)

    def add_tags(self, tags: List[str], title: str) -> None:
       
        for tag in tags:
            self.add_tag(tag, title)

    def remove_tag(self, tag: str, title: str) -> None:
        
        key = normalize_tag(tag)
        if key not in self.tag_database:
            return
        if title in self.tag_database[key]:
            self.tag_database[key].remove(title)
        if not self.tag_database[key]:
            del self.tag_database[key]

    def remove_note(self, title: str, tags: List[str]) -> None:
       
        for tag in tags:
            self.remove_tag(tag, title)

    def get_titles_for_tag(self, tag: str) -> List[str]:
        
        key = normalize_tag(tag)
        return list(self.tag_database.get(key, []))

    def tag_exists(self, tag: str) -> bool:
        return normalize_tag(tag) in self.tag_database
