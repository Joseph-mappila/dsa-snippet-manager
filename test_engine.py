# test_engine.py
from engine import Note, LinkedList, BinarySearchTree

def test_engine():
    print("--- 1. Testing Linked List ---")
    ll = LinkedList()
    ll.append(Note("Bubble Sort", "O(n^2) comparison sort", "#sorting"))
    ll.append(Note("Merge Sort", "O(n log n) divide and conquer", "#sorting"))
    
    for note in ll.to_list():
        print(f"  [LL Item] {note.title} -> Tag: {note.tag}")

    print("\n--- 2. Testing Binary Search Tree ---")
    bst = BinarySearchTree()
    test_notes = [
        Note("Quick Sort", "Pivot-based sorting", "#sorting"),
        Note("Dijkstra", "Shortest path algorithm", "#graphs"),
        Note("Binary Search", "Divide-and-conquer search", "#searching"),
        Note("AVL Tree", "Self-balancing BST", "#trees"),
    ]

    for note in test_notes:
        bst.insert(note)
        print(f"  Inserted: {note.title}")

    print("\n--- 3. Testing Alphabetical In-Order Traversal ---")
    sorted_notes = bst.in_order_traversal()
    for note in sorted_notes:
        print(f"  Sorted: {note.title}")

    print("\n--- 4. Testing BST Search ---")
    query = "Dijkstra"
    found = bst.search(query)
    if found:
        print(f"  Found '{query}': {found.content}")
    else:
        print(f"  '{query}' not found.")

if __name__ == "__main__":
    test_engine()