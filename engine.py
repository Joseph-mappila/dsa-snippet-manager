class Note:
    def __init__(self, title: str, content: str, tag: str):
        self.title = title
        self.content = content
        self.tag = tag

    def __repr__(self):
        return f"Note(title='{self.title}', tag='{self.tag}')"


# ---------------------------------------------------------
# LINEAR DATA STRUCTURE: Custom Singly Linked List
# ---------------------------------------------------------
class ListNode:
    def __init__(self, note: Note):
        self.note = note
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, note: Note) -> None:
        new_node = ListNode(note)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def to_list(self) -> list[Note]:
        notes = []
        current = self.head
        while current:
            notes.append(current.note)
            current = current.next
        return notes


# ---------------------------------------------------------
# NON-LINEAR DATA STRUCTURE: Binary Search Tree (BST)
# ---------------------------------------------------------
class BSTNode:
    def __init__(self, note: Note):
        self.note = note
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, note: Note) -> None:
        if self.root is None:
            self.root = BSTNode(note)
        else:
            self._insert_recursive(self.root, note)

    def _insert_recursive(self, current: BSTNode, note: Note) -> None:
        if note.title.lower() < current.note.title.lower():
            if current.left is None:
                current.left = BSTNode(note)
            else:
                self._insert_recursive(current.left, note)
        else:
            if current.right is None:
                current.right = BSTNode(note)
            else:
                self._insert_recursive(current.right, note)

    def search(self, title: str) -> Note | None:
        return self._search_recursive(self.root, title.lower())

    def _search_recursive(self, current: BSTNode, target_title: str) -> Note | None:
        if current is None:
            return None
        if current.note.title.lower() == target_title:
            return current.note
        if target_title < current.note.title.lower():
            return self._search_recursive(current.left, target_title)
        return self._search_recursive(current.right, target_title)

    def in_order_traversal(self) -> list[Note]:
        result = []
        self._in_order_recursive(self.root, result)
        return result

    def _in_order_recursive(self, current: BSTNode, result: list[Note]) -> None:
        if current:
            self._in_order_recursive(current.left, result)
            result.append(current.note)
            self._in_order_recursive(current.right, result)