#include <iostream>
#include <iomanip>
using namespace std;

// Simple Linked List Simulation using 2D Array (without Free List)
// a[i][0] = data value (-999 means free/unused)
// a[i][1] = next node index (-1 for end of list)
const int MAX_SIZE = 100;
int linkedList[MAX_SIZE][2];  // The 2D array to simulate linked list
int head = -1;                // Head of the linked list

// Initialize the linked list
void initialize() {
    // Initialize all positions as free (use -999 as free marker)
    for(int i = 0; i < MAX_SIZE; i++) {
        linkedList[i][0] = -999;  // data: -999 means free
        linkedList[i][1] = -1;    // next pointer
    }

    head = -1;  // Empty linked list
    cout << "Linked list initialized successfully!" << endl;
}

// Find the first free position in the array
int findFreePosition() {
    for(int i = 0; i < MAX_SIZE; i++) {
        if(linkedList[i][0] == -999) {  // Position is free (-999 marker)
            return i;
        }
    }
    return -1;  // No free position found
}

// Insert a node at the beginning
void insertAtBeginning(int data) {
    int freePos = findFreePosition();
    if(freePos == -1) {
        cout << "Error: No free positions available!" << endl;
        return;
    }

    // Store data and set next pointer
    linkedList[freePos][0] = data;
    linkedList[freePos][1] = head;  // Point to current head

    // Update head
    head = freePos;

    cout << "Inserted " << data << " at the beginning (position " << freePos << ")" << endl;
}

// Insert a node at the end
void insertAtEnd(int data) {
    int freePos = findFreePosition();
    if(freePos == -1) {
        cout << "Error: No free positions available!" << endl;
        return;
    }

    // Store data
    linkedList[freePos][0] = data;
    linkedList[freePos][1] = -1;  // End of list

    if(head == -1) {
        // Empty list - this becomes the head
        head = freePos;
    } else {
        // Find the last node and link to new node
        int current = head;
        while(linkedList[current][1] != -1) {
            current = linkedList[current][1];
        }
        linkedList[current][1] = freePos;
    }

    cout << "Inserted " << data << " at the end (position " << freePos << ")" << endl;
}

// Insert a node after a specific value
void insertAfterValue(int searchValue, int data) {
    if(head == -1) {
        cout << "List is empty!" << endl;
        return;
    }

    int freePos = findFreePosition();
    if(freePos == -1) {
        cout << "Error: No free positions available!" << endl;
        return;
    }

    // Find the node with searchValue
    int current = head;
    while(current != -1) {
        if(linkedList[current][0] == searchValue) {
            // Found the node - insert after it
            linkedList[freePos][0] = data;
            linkedList[freePos][1] = linkedList[current][1];  // Point to next node
            linkedList[current][1] = freePos;                 // Update current node's next

            cout << "Inserted " << data << " after " << searchValue << " (position " << freePos << ")" << endl;
            return;
        }
        current = linkedList[current][1];
    }

    cout << "Value " << searchValue << " not found in the list" << endl;
}

// Delete a node with specific value
void deleteValue(int value) {
    if(head == -1) {
        cout << "List is empty!" << endl;
        return;
    }

    int current = head;
    int previous = -1;

    // Find the node to delete
    while(current != -1) {
        if(linkedList[current][0] == value) {
            if(previous == -1) {
                // Deleting head node
                head = linkedList[current][1];
            } else {
                // Delete middle/end node
                linkedList[previous][1] = linkedList[current][1];
            }

            // Mark position as free
            linkedList[current][0] = -999;  // Mark as free
            linkedList[current][1] = -1;    // Clear next pointer

            cout << "Deleted value " << value << " from position " << current << endl;
            return;
        }
        previous = current;
        current = linkedList[current][1];
    }

    cout << "Value " << value << " not found in the list" << endl;
}

// Search for a value in the linked list
void searchValue(int value) {
    if(head == -1) {
        cout << "List is empty!" << endl;
        return;
    }

    int current = head;
    int position = 0;

    while(current != -1) {
        position++;
        if(linkedList[current][0] == value) {
            cout << "Value " << value << " found at logical position " << position
                 << " (array index " << current << ")" << endl;
            return;
        }
        current = linkedList[current][1];
    }

    cout << "Value " << value << " not found in the list" << endl;
}

// Display the linked list
void displayList() {
    if(head == -1) {
        cout << "Linked List is empty!" << endl;
        return;
    }

    cout << "\n=== LINKED LIST CONTENT ===" << endl;
    cout << "Array Index | Data | Next | Status" << endl;
    cout << "------------|------|------|--------" << endl;

    for(int i = 0; i < MAX_SIZE; i++) {
        if(linkedList[i][0] != -999) {  // Only show used positions (not marked as free)
            cout << setw(11) << i << " | "
                 << setw(4) << linkedList[i][0] << " | "
                 << setw(4) << linkedList[i][1] << " | "
                 << setw(6) << "USED" << endl;
        }
    }

    cout << "\n=== TRAVERSAL (Data Values) ===" << endl;
    int current = head;
    cout << "Head -> ";
    while(current != -1) {
        cout << linkedList[current][0];
        current = linkedList[current][1];
        if(current != -1) cout << " -> ";
        else cout << " -> NULL";
    }
    cout << endl << endl;
}

// Display memory usage
void displayMemoryStatus() {
    int used = 0;
    int free = 0;

    for(int i = 0; i < MAX_SIZE; i++) {
        if(linkedList[i][0] != -999) used++;  // Not marked as free
        else free++;
    }

    cout << "\n=== MEMORY STATUS ===" << endl;
    cout << "Total positions: " << MAX_SIZE << endl;
    cout << "Used positions: " << used << endl;
    cout << "Free positions: " << free << endl;
    cout << "Head of list: " << head << endl;

    cout << "\nFree positions: ";
    for(int i = 0; i < MAX_SIZE; i++) {
        if(linkedList[i][0] == -999) {  // Marked as free
            cout << i << " ";
        }
    }
    cout << endl << endl;
}

// Main menu
int main() {
    initialize();
    int choice, data, searchVal;

    cout << "\n=== SIMPLE LINKED LIST SIMULATION ===" << endl;
    cout << "Array Structure: a[i][0] = data, a[i][1] = next index, a[i][2] = status" << endl;
    cout << "No Free List optimization - simple array traversal" << endl << endl;

    while(true) {
        cout << "\n=== MENU ===" << endl;
        cout << "1. Insert at Beginning" << endl;
        cout << "2. Insert at End" << endl;
        cout << "3. Insert After Value" << endl;
        cout << "4. Delete Value" << endl;
        cout << "5. Search Value" << endl;
        cout << "6. Display List" << endl;
        cout << "7. Display Memory Status" << endl;
        cout << "8. Exit" << endl;
        cout << "Enter your choice: ";
        cin >> choice;

        switch(choice) {
            case 1:
                cout << "Enter data to insert: ";
                cin >> data;
                insertAtBeginning(data);
                break;

            case 2:
                cout << "Enter data to insert: ";
                cin >> data;
                insertAtEnd(data);
                break;

            case 3:
                cout << "Enter value to search for: ";
                cin >> searchVal;
                cout << "Enter data to insert: ";
                cin >> data;
                insertAfterValue(searchVal, data);
                break;

            case 4:
                cout << "Enter value to delete: ";
                cin >> data;
                deleteValue(data);
                break;

            case 5:
                cout << "Enter value to search: ";
                cin >> data;
                searchValue(data);
                break;

            case 6:
                displayList();
                break;

            case 7:
                displayMemoryStatus();
                break;

            case 8:
                cout << "Exiting program..." << endl;
                return 0;

            default:
                cout << "Invalid choice! Please try again." << endl;
        }
    }

    return 0;
}
