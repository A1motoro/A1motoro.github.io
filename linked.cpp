#include <iostream>
#include <iomanip>
using namespace std;

// Linked List Simulation using 2D Array
// a[i][0] = data value
// a[i][1] = next node index (-1 for end of list)
const int MAX_SIZE = 100;
int linkedList[MAX_SIZE][2];  // The 2D array to simulate linked list
bool isUsed[MAX_SIZE];       // Track which positions are used
int head = -1;               // Head of the linked list
int freeList = 0;            // Head of free list

// Initialize the linked list
void initialize() {
    // Initialize all positions as free
    for(int i = 0; i < MAX_SIZE; i++) {
        isUsed[i] = false;
        linkedList[i][0] = 0;    // data
        linkedList[i][1] = -1;   // next pointer
    }

    // Create free list (linked list of available positions)
    for(int i = 0; i < MAX_SIZE - 1; i++) {
        linkedList[i][1] = i + 1;
    }
    linkedList[MAX_SIZE - 1][1] = -1; // Last node points to -1

    head = -1;      // Empty linked list
    freeList = 0;   // First available position
}

// Get a free node from the free list
int getFreeNode() {
    if(freeList == -1) {
        cout << "Error: No free nodes available!" << endl;
        return -1;
    }

    int node = freeList;
    freeList = linkedList[freeList][1]; // Move to next free node
    isUsed[node] = true;
    return node;
}

// Return a node to the free list
void returnNode(int node) {
    if(node < 0 || node >= MAX_SIZE) return;

    isUsed[node] = false;
    linkedList[node][0] = 0;           // Clear data
    linkedList[node][1] = freeList;    // Point to current free list head
    freeList = node;                   // This node becomes new free list head
}

// Insert a node at the beginning
void insertAtBeginning(int data) {
    int newNode = getFreeNode();
    if(newNode == -1) return;

    linkedList[newNode][0] = data;     // Store data
    linkedList[newNode][1] = head;     // Point to current head
    head = newNode;                    // Update head

    cout << "Inserted " << data << " at the beginning" << endl;
}

// Insert a node at the end
void insertAtEnd(int data) {
    int newNode = getFreeNode();
    if(newNode == -1) return;

    linkedList[newNode][0] = data;
    linkedList[newNode][1] = -1; // End of list

    if(head == -1) {
        // Empty list
        head = newNode;
    } else {
        // Find the last node
        int current = head;
        while(linkedList[current][1] != -1) {
            current = linkedList[current][1];
        }
        linkedList[current][1] = newNode; // Link last node to new node
    }

    cout << "Inserted " << data << " at the end" << endl;
}

// Insert a node after a specific value
void insertAfterValue(int searchValue, int data) {
    int current = head;

    // Find the node with searchValue
    while(current != -1) {
        if(linkedList[current][0] == searchValue) {
            int newNode = getFreeNode();
            if(newNode == -1) return;

            linkedList[newNode][0] = data;
            linkedList[newNode][1] = linkedList[current][1]; // Point to next node
            linkedList[current][1] = newNode;                // Update current node's next

            cout << "Inserted " << data << " after " << searchValue << endl;
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

            returnNode(current); // Return node to free list
            cout << "Deleted value " << value << " from the list" << endl;
            return;
        }
        previous = current;
        current = linkedList[current][1];
    }

    cout << "Value " << value << " not found in the list" << endl;
}

// Search for a value in the linked list
void searchValue(int value) {
    int current = head;
    int position = 0;

    while(current != -1) {
        position++;
        if(linkedList[current][0] == value) {
            cout << "Value " << value << " found at position " << position
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
    cout << "Array Index | Data | Next Index" << endl;
    cout << "------------|------|------------" << endl;

    int current = head;
    int count = 0;

    while(current != -1 && count < MAX_SIZE) { // Prevent infinite loop
        cout << setw(11) << current << " | "
             << setw(4) << linkedList[current][0] << " | "
             << setw(11) << linkedList[current][1] << endl;
        current = linkedList[current][1];
        count++;
    }

    cout << "\n=== TRAVERSAL (Data Values) ===" << endl;
    current = head;
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
        if(isUsed[i]) used++;
        else free++;
    }

    cout << "\n=== MEMORY STATUS ===" << endl;
    cout << "Total nodes: " << MAX_SIZE << endl;
    cout << "Used nodes: " << used << endl;
    cout << "Free nodes: " << free << endl;
    cout << "Head of list: " << head << endl;
    cout << "Head of free list: " << freeList << endl << endl;
}

// Main menu
int main() {
    initialize();
    int choice, data, searchVal;

    cout << "=== LINKED LIST SIMULATION USING 2D ARRAY ===" << endl;
    cout << "Array Structure: a[i][0] = data, a[i][1] = next index" << endl << endl;

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