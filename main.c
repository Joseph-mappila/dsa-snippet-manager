#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>

typedef struct {
    char title[256];
    char content[1024];
    char tag[256];
} Note;

typedef struct ListNode {
    Note* note;
    struct ListNode* next;
} ListNode;

typedef struct {
    ListNode* head;
    int size;
} LinkedList;

typedef struct BSTNode {
    Note* note;
    struct BSTNode* left;
    struct BSTNode* right;
} BSTNode;

typedef struct {
    BSTNode* root;
} BinarySearchTree;

typedef struct {
    Note* items[100];
    int top;
} UndoStack;

typedef struct {
    char tag[256];
    char titles[100][256];
    int title_count;
} TagEntry;

typedef struct {
    TagEntry entries[256];
    int entry_count;
} TagHashTable;

typedef struct {
    BinarySearchTree* bst;
    LinkedList* history;
} BSTNoteStorage;

typedef struct {
    BSTNoteStorage* storage;
    TagHashTable* tag_table;
    UndoStack* undo_stack;
} NoteManager;

typedef struct {
    NoteManager* manager;
} Menu;

Note* create_note(const char* title, const char* content, const char* tag) {
    Note* note = (Note*)malloc(sizeof(Note));
    strncpy(note->title, title, 255);
    note->title[255] = '\0';
    strncpy(note->content, content, 1023);
    note->content[1023] = '\0';
    strncpy(note->tag, tag, 255);
    note->tag[255] = '\0';
    return note;
}

LinkedList* create_linked_list() {
    LinkedList* ll = (LinkedList*)malloc(sizeof(LinkedList));
    ll->head = NULL;
    ll->size = 0;
    return ll;
}

void ll_append(LinkedList* ll, Note* note) {
    ListNode* new_node = (ListNode*)malloc(sizeof(ListNode));
    new_node->note = note;
    new_node->next = NULL;
    if (!ll->head) {
        ll->head = new_node;
    } else {
        ListNode* current = ll->head;
        while (current->next) {
            current = current->next;
        }
        current->next = new_node;
    }
    ll->size++;
}

BinarySearchTree* create_bst() {
    BinarySearchTree* bst = (BinarySearchTree*)malloc(sizeof(BinarySearchTree));
    bst->root = NULL;
    return bst;
}

void str_tolower(char* dest, const char* src) {
    int i = 0;
    while (src[i]) {
        dest[i] = tolower(src[i]);
        i++;
    }
    dest[i] = '\0';
}

void _bst_insert_recursive(BSTNode* current, Note* note) {
    char current_title[256], note_title[256];
    str_tolower(current_title, current->note->title);
    str_tolower(note_title, note->title);

    if (strcmp(note_title, current_title) < 0) {
        if (!current->left) {
            current->left = (BSTNode*)malloc(sizeof(BSTNode));
            current->left->note = note;
            current->left->left = NULL;
            current->left->right = NULL;
        } else {
            _bst_insert_recursive(current->left, note);
        }
    } else {
        if (!current->right) {
            current->right = (BSTNode*)malloc(sizeof(BSTNode));
            current->right->note = note;
            current->right->left = NULL;
            current->right->right = NULL;
        } else {
            _bst_insert_recursive(current->right, note);
        }
    }
}

void bst_insert(BinarySearchTree* bst, Note* note) {
    if (!bst->root) {
        bst->root = (BSTNode*)malloc(sizeof(BSTNode));
        bst->root->note = note;
        bst->root->left = NULL;
        bst->root->right = NULL;
    } else {
        _bst_insert_recursive(bst->root, note);
    }
}

Note* _bst_search_recursive(BSTNode* current, const char* target_title) {
    if (!current) return NULL;
    char current_title[256];
    str_tolower(current_title, current->note->title);
    
    if (strcmp(current_title, target_title) == 0) return current->note;
    if (strcmp(target_title, current_title) < 0) return _bst_search_recursive(current->left, target_title);
    return _bst_search_recursive(current->right, target_title);
}

Note* bst_search(BinarySearchTree* bst, const char* title) {
    char target_title[256];
    str_tolower(target_title, title);
    return _bst_search_recursive(bst->root, target_title);
}

void _bst_in_order_recursive(BSTNode* current, Note** result, int* count) {
    if (current) {
        _bst_in_order_recursive(current->left, result, count);
        result[(*count)++] = current->note;
        _bst_in_order_recursive(current->right, result, count);
    }
}

Note** bst_in_order_traversal(BinarySearchTree* bst, int* out_size) {
    Note** result = (Note**)malloc(sizeof(Note*) * 1000); 
    *out_size = 0;
    _bst_in_order_recursive(bst->root, result, out_size);
    return result;
}

UndoStack* create_undo_stack() {
    UndoStack* stack = (UndoStack*)malloc(sizeof(UndoStack));
    stack->top = -1;
    return stack;
}

int undo_stack_is_empty(UndoStack* stack) {
    return stack->top == -1;
}

void undo_stack_push(UndoStack* stack, Note* note) {
    if (stack->top < 99) {
        stack->items[++stack->top] = note;
    }
}

Note* undo_stack_pop(UndoStack* stack) {
    if (undo_stack_is_empty(stack)) return NULL;
    return stack->items[stack->top--];
}

void normalize_tag(char* dest, const char* tag) {
    while (*tag == ' ' || *tag == '\t') tag++;
    if (*tag == '#') tag++;
    int i = 0;
    while (tag[i]) {
        dest[i] = tolower(tag[i]);
        i++;
    }
    while (i > 0 && (dest[i-1] == ' ' || dest[i-1] == '\t')) i--;
    dest[i] = '\0';
}

void pack_tags(char* dest, const char* raw_tags) {
    char temp[1024];
    strncpy(temp, raw_tags, 1023);
    temp[1023] = '\0';
    dest[0] = '\0';
    
    char* token = strtok(temp, ",");
    int first = 1;
    while (token != NULL) {
        char clean[256];
        normalize_tag(clean, token);
        if (strlen(clean) > 0) {
            if (!first) strcat(dest, ",");
            strcat(dest, clean);
            first = 0;
        }
        token = strtok(NULL, ",");
    }
}

int parse_tags(const char* tag_field, char parsed_tags[][256]) {
    if (!tag_field || strlen(tag_field) == 0) return 0;
    char temp[1024];
    strncpy(temp, tag_field, 1023);
    temp[1023] = '\0';
    
    int count = 0;
    char* token = strtok(temp, ",");
    while (token != NULL) {
        normalize_tag(parsed_tags[count], token);
        if (strlen(parsed_tags[count]) > 0) {
            count++;
        }
        token = strtok(NULL, ",");
    }
    return count;
}

TagHashTable* create_tag_hash_table() {
    TagHashTable* table = (TagHashTable*)malloc(sizeof(TagHashTable));
    table->entry_count = 0;
    return table;
}

void tag_hash_table_add_tag(TagHashTable* table, const char* tag, const char* title) {
    char key[256];
    normalize_tag(key, tag);
    if (strlen(key) == 0) return;
    
    for (int i = 0; i < table->entry_count; i++) {
        if (strcmp(table->entries[i].tag, key) == 0) {
            for (int j = 0; j < table->entries[i].title_count; j++) {
                if (strcmp(table->entries[i].titles[j], title) == 0) return;
            }
            strcpy(table->entries[i].titles[table->entries[i].title_count++], title);
            return;
        }
    }
    
    strcpy(table->entries[table->entry_count].tag, key);
    strcpy(table->entries[table->entry_count].titles[0], title);
    table->entries[table->entry_count].title_count = 1;
    table->entry_count++;
}

void tag_hash_table_add_tags(TagHashTable* table, char tags[][256], int tag_count, const char* title) {
    for (int i = 0; i < tag_count; i++) {
        tag_hash_table_add_tag(table, tags[i], title);
    }
}

void tag_hash_table_remove_tag(TagHashTable* table, const char* tag, const char* title) {
    char key[256];
    normalize_tag(key, tag);
    
    for (int i = 0; i < table->entry_count; i++) {
        if (strcmp(table->entries[i].tag, key) == 0) {
            for (int j = 0; j < table->entries[i].title_count; j++) {
                if (strcmp(table->entries[i].titles[j], title) == 0) {
                    for (int k = j; k < table->entries[i].title_count - 1; k++) {
                        strcpy(table->entries[i].titles[k], table->entries[i].titles[k+1]);
                    }
                    table->entries[i].title_count--;
                    return;
                }
            }
        }
    }
}

void tag_hash_table_remove_note(TagHashTable* table, const char* title, char tags[][256], int tag_count) {
    for (int i = 0; i < tag_count; i++) {
        tag_hash_table_remove_tag(table, tags[i], title);
    }
}

int tag_hash_table_get_titles(TagHashTable* table, const char* tag, char out_titles[][256]) {
    char key[256];
    normalize_tag(key, tag);
    for (int i = 0; i < table->entry_count; i++) {
        if (strcmp(table->entries[i].tag, key) == 0) {
            for (int j = 0; j < table->entries[i].title_count; j++) {
                strcpy(out_titles[j], table->entries[i].titles[j]);
            }
            return table->entries[i].title_count;
        }
    }
    return 0;
}

BSTNoteStorage* create_bst_note_storage() {
    BSTNoteStorage* storage = (BSTNoteStorage*)malloc(sizeof(BSTNoteStorage));
    storage->bst = create_bst();
    storage->history = create_linked_list();
    return storage;
}

void bst_storage_insert(BSTNoteStorage* storage, Note* note) {
    bst_insert(storage->bst, note);
    ll_append(storage->history, note);
}

Note* bst_storage_search(BSTNoteStorage* storage, const char* title) {
    return bst_search(storage->bst, title);
}

Note* bst_storage_delete(BSTNoteStorage* storage, const char* title) {
    Note* target = bst_search(storage->bst, title);
    if (!target) return NULL;
    
    int size;
    Note** all_notes = bst_in_order_traversal(storage->bst, &size);
    
    BinarySearchTree* rebuilt = create_bst();
    for (int i = 0; i < size; i++) {
        if (strcmp(all_notes[i]->title, target->title) != 0) {
            bst_insert(rebuilt, all_notes[i]);
        }
    }
    
    free(storage->bst);
    storage->bst = rebuilt;
    free(all_notes);
    return target;
}

Note** bst_storage_get_all(BSTNoteStorage* storage, int* out_size) {
    return bst_in_order_traversal(storage->bst, out_size);
}

void bst_storage_reinsert(BSTNoteStorage* storage, Note* note) {
    bst_insert(storage->bst, note);
}

NoteManager* create_note_manager(BSTNoteStorage* storage, TagHashTable* tag_table, UndoStack* undo_stack) {
    NoteManager* manager = (NoteManager*)malloc(sizeof(NoteManager));
    manager->storage = storage;
    manager->tag_table = tag_table;
    manager->undo_stack = undo_stack;
    return manager;
}

Note* manager_add_note(NoteManager* manager, const char* title, const char* content, const char* raw_tags) {
    char tag_field[256];
    pack_tags(tag_field, raw_tags);
    Note* note = create_note(title, content, tag_field);
    bst_storage_insert(manager->storage, note);
    
    char parsed_tags[10][256];
    int count = parse_tags(note->tag, parsed_tags);
    tag_hash_table_add_tags(manager->tag_table, parsed_tags, count, note->title);
    return note;
}

Note* manager_search_note(NoteManager* manager, const char* title) {
    return bst_storage_search(manager->storage, title);
}

int manager_delete_note(NoteManager* manager, const char* title) {
    Note* note = bst_storage_delete(manager->storage, title);
    if (!note) return 0;
    
    char parsed_tags[10][256];
    int count = parse_tags(note->tag, parsed_tags);
    tag_hash_table_remove_note(manager->tag_table, note->title, parsed_tags, count);
    undo_stack_push(manager->undo_stack, note);
    return 1;
}

Note* manager_undo_last_delete(NoteManager* manager) {
    Note* note = undo_stack_pop(manager->undo_stack);
    if (!note) return NULL;
    
    bst_storage_reinsert(manager->storage, note);
    char parsed_tags[10][256];
    int count = parse_tags(note->tag, parsed_tags);
    tag_hash_table_add_tags(manager->tag_table, parsed_tags, count, note->title);
    return note;
}

Note** manager_display_all_notes(NoteManager* manager, int* out_size) {
    return bst_storage_get_all(manager->storage, out_size);
}

Note** manager_search_by_tag(NoteManager* manager, const char* tag, int* out_size) {
    char titles[100][256];
    int count = tag_hash_table_get_titles(manager->tag_table, tag, titles);
    
    Note** notes = (Note**)malloc(sizeof(Note*) * count);
    *out_size = 0;
    for (int i = 0; i < count; i++) {
        Note* note = bst_storage_search(manager->storage, titles[i]);
        if (note) {
            notes[(*out_size)++] = note;
        }
    }
    return notes;
}

Menu* create_menu(NoteManager* manager) {
    Menu* menu = (Menu*)malloc(sizeof(Menu));
    menu->manager = manager;
    return menu;
}

void trim_newline(char* str) {
    int len = strlen(str);
    if (len > 0 && str[len-1] == '\n') str[len-1] = '\0';
}

void menu_print_note(Note* note) {
    char parsed_tags[10][256];
    int count = parse_tags(note->tag, parsed_tags);
    printf("Title: %s\n", note->title);
    printf("Content: %s\n", note->content);
    printf("Tags: ");
    if (count == 0) {
        printf("(none)\n");
    } else {
        for (int i = 0; i < count; i++) {
            printf("%s%s", parsed_tags[i], (i < count - 1) ? ", " : "");
        }
        printf("\n");
    }
}

void menu_run(Menu* menu) {
    char choice[256];
    while (1) {
        printf("========================================\n");
        printf("    DEVELOPER SNIPPET & NOTES MANAGER\n");
        printf("========================================\n");
        printf("1. Add Note / Code Snippet\n");
        printf("2. Search Note\n");
        printf("3. Delete Note\n");
        printf("4. Undo Last Delete\n");
        printf("5. Display All Notes\n");
        printf("6. Search Notes by Tag\n");
        printf("0. Exit\n\n");
        printf("Enter choice: ");
        fgets(choice, 256, stdin);
        trim_newline(choice);

        if (strcmp(choice, "0") == 0) {
            printf("Goodbye!\n");
            break;
        } else if (strcmp(choice, "1") == 0) {
            char title[256], content[1024], raw_tags[256];
            printf("Title: ");
            fgets(title, 256, stdin); trim_newline(title);
            if (strlen(title) == 0) {
                printf("Title cannot be empty.\n\n");
                continue;
            }
            printf("Content: ");
            fgets(content, 1024, stdin); trim_newline(content);
            printf("Tags (comma-separated): ");
            fgets(raw_tags, 256, stdin); trim_newline(raw_tags);
            
            Note* note = manager_add_note(menu->manager, title, content, raw_tags);
            printf("\nNote added:\n");
            menu_print_note(note);
            printf("\n");
        } else if (strcmp(choice, "2") == 0) {
            char title[256];
            printf("Enter title to search: ");
            fgets(title, 256, stdin); trim_newline(title);
            Note* note = manager_search_note(menu->manager, title);
            if (!note) {
                printf("Note not found.\n\n");
            } else {
                printf("\n");
                menu_print_note(note);
                printf("\n");
            }
        } else if (strcmp(choice, "3") == 0) {
            char title[256];
            printf("Enter title to delete: ");
            fgets(title, 256, stdin); trim_newline(title);
            if (manager_delete_note(menu->manager, title)) {
                printf("'%s' deleted.\n\n", title);
            } else {
                printf("Note not found.\n\n");
            }
        } else if (strcmp(choice, "4") == 0) {
            Note* note = manager_undo_last_delete(menu->manager);
            if (!note) {
                printf("Nothing to undo.\n\n");
            } else {
                printf("\n%s restored successfully.\n\n", note->title);
            }
        } else if (strcmp(choice, "5") == 0) {
            int size;
            Note** notes = manager_display_all_notes(menu->manager, &size);
            if (size == 0) {
                printf("No notes stored yet.\n\n");
            } else {
                for (int i = 0; i < size; i++) {
                    menu_print_note(notes[i]);
                    printf("----------------------------------------\n");
                }
                printf("\n");
            }
            free(notes);
        } else if (strcmp(choice, "6") == 0) {
            char tag[256];
            printf("Enter tag: ");
            fgets(tag, 256, stdin); trim_newline(tag);
            if (strlen(tag) == 0) {
                printf("Tag cannot be empty.\n\n");
                continue;
            }
            int size;
            Note** notes = manager_search_by_tag(menu->manager, tag, &size);
            char clean[256];
            normalize_tag(clean, tag);
            if (size == 0) {
                printf("No notes found for #%s.\n\n", clean);
            } else {
                printf("\nNotes tagged #%s:\n\n", clean);
                for (int i = 0; i < size; i++) {
                    printf("%d. %s\n", i + 1, notes[i]->title);
                }
                printf("\n");
            }
            free(notes);
        } else {
            printf("Invalid choice. Please try again.\n\n");
        }
    }
}

int main() {
    BSTNoteStorage* storage = create_bst_note_storage();
    TagHashTable* tag_table = create_tag_hash_table();
    UndoStack* undo_stack = create_undo_stack();

    NoteManager* manager = create_note_manager(storage, tag_table, undo_stack);
    Menu* menu = create_menu(manager);
    
    menu_run(menu);

    return 0;
}