# Modification for Chained List

**Published:** December 20, 2024
**Category:** Programming
**Read Time:** 8 min

Chainedlist is a data structure that allows for efficient insertion, deletion, and traversal of elements. It is particularly useful in scenarios where frequent modifications to the list are required.

## **Simple Model** of Chained List
### Initialization

Generally, when it comes to chained list, we talk about the one-way linked list.
Take C++ as an example, a simple implementation of a chained list can be done as follows:
''' C++
class Node {
    int data;
    Node* next;
};
'''
The block above defines the basic structure of a **node** in the list. Each node contains a data field and a pointer to the next node in the list.
You can surely simulate the same function in arrays, which could be written as follows:
```C++
int arr[100][2]; // Assuming a maximum of 100 nodes
// arr[i][0] stores the data
// arr[i][1] stores the pointer to the next node
```

Aside from the nodes, it's worth mentioning the **head** of the list, which is the first node in the list.In the case of arrays, the head could be the pointer to the first element in thechained list. Also the last node in the list usualy own a pointer of -1 or NULL to indicate the end of the list.

So clever reader, guess what it means when head = -1?
### Traversal
Traversal is an O(n) operation in the chained list. You start at the head and traverse every node until you find the node you're looking for. Here's the implementation in C++:
Say you want to find the first node with a certain value, you can do it as follows:

```C++
Node* find(int value) {
    Node* current = head;
    while (current!= NULL) {
        if (current->data == value) {
            return current;
        }
        current = current->next;
    }
    return NULL;
}
```
*Easy huh?*  

### Insertion

Insertion is highly efficient in a chained list. It work like this:

1. Create a new node with the data to be inserted.
2. Find the node that you want to insert the new node after.
3. Set the new node's next pointer to the next node of the node you found.
4. Set the next pointer of the node you found to the new node.
   
Here's the implementation in C++:
Say you want to insert a new node with a value of data after the node of a certain value, you can do it as follows using the find function from above:

```C++
void insert(int data, int value){
    Node* newNode = new Node;
    newNode->data = data;
    Node* current = find(value);
    newNode->next = current->next;
    current->next = newNode;
}
```

### Deletion

Deletion is also highly efficient in a chained list. It works like this:

1. Find the node that you want to delete.
2. Set the next pointer of the previous node to the next node of the node you found.
3. Delete the node you found.

Here's the implementation in C++, like when you want to delete a node with a certain value:
```C++
void deleteNode(int value) {
    Node* current = head;
    Node* previous = NULL;
    while (current!= NULL) {
        if (current->data == value) {
            if (previous == NULL) {
                head = current->next;
            } else {
                previous->next = current->next;
            }
            delete current;
            return;
        }
        previous = current;
        current = current->next;
    }
}
```

## **Modification** of Chained List

In the previous section, we discussed the basic model of a chained list. In this section, we will discuss the modification of a chained list.

### Ways to save memory

How do we save memory when we modify a chained list? One way is to reuse the nodes that are no longer in use. This way, we don't need to allocate new memory for the nodes that are modified.  
1. **Mark the unused**We can add a flag to each node to indicate whether it's in use or not. In some cases, say the data field is defined to be above zero, we can set the data to a negative value to indicate that the node is unused.
2. **Reuse empty nodes**We can keep track of the last node that keeps unused to save memory when adding a new node, because we don't need to allocate new memory for the last node.

For the second way, we announce a variable Node* _freelast_ to keep track of the last unused node. When we need to add a new node, we first check if there are any unused nodes. If there are, we reuse one of them. Otherwise, we allocate a new node.

We initialize _freelast_ to NULL when the list is created. When we add a new node, we check if _freelast_ is NULL. If it is, we allocate a new node and set _freelast_ to it. Otherwise, we reuse the node pointed to by _freelast_ and set _freelast_ to its next pointer. When a node is deleted, we set its next pointer to _freelast_ and set _freelast_ to the deleted node.

Here's the implementation in C++:

```C++
class Node {
    int data;
    Node* next;
    bool used;
};

Node* _freelast = NULL;

void insert(int data) {
    Node* newNode = new Node;
    newNode->data = data;
    newNode->used = true;
    if (_freelast == NULL) {
        newNode->next = NULL;
    } else {
        newNode->next = _freelast->next;
        _freelast->next = newNode;
    }
    _freelast = newNode;
}
void deleteNode(int value) {
    Node* current = head;
    Node* previous = NULL;
    while (current!= NULL) {
        if (current->data == value) {
            if (previous == NULL) {
                head = current->next;
            } else {
                previous->next = current->next;
            }
            if (current->used) {
                current->used = false;
                current->next = _freelast->next;
                _freelast->next = current;
                _freelast = current;
            } else {
                delete current;
            }
            return;
        }
        previous = current;
        current = current->next;
    }
}
```

For this scene, we use the **memory pool**
**Notice**:this is not a way to save memory, the whole memory is still allocated, but it reduces the number of allocations and frees.
### Ways to save time

In addition to saving memory, we can also save time by avoiding unnecessary traversals. One way is to use a **hash table** to store the nodes. We can use the data field of each node as the key to the hash table and the node itself as the value. When we need to find a node, we simply look it up in the hash table. When we need to insert or delete a node, we update the hash table accordingly.  
The main idea of using  the hashmap is exchange time with memory. We can avoid traversing the list to find a node, which takes O(n) time, and instead, we can look it up in the hash table in constant time.
We create a hash table mapping data to nodes. The hash table make the time varianse of searching a value from O(n) to O(1).

Here's the implementation in C++:

```C++
#include <unordered_map>

class Node {
    int data;
    Node* next;
};

std::unordered_map<int, Node*> hashmap;

void insert(int data) {
    Node* newNode = new Node;
    newNode->data = data;
    newNode->next = hashmap[data];
    hashmap[data] = newNode; // update hash table
}
void deleteNode(int value) {
    Node* current = hashmap[value];
    Node* previous = NULL;
    while (current!= NULL) {
        if (current->data == value) {
            if (previous == NULL) {
                hashmap[value] = current->next; // update hash table
            } else {
                previous->next = current->next;
            }
            delete current;
            return;
        }
        previous = current;
        current = current->next;
    }
}
```

In this implementation, we use the unordered_map from the C++ standard library. The unordered_map is a hash table that provides constant time complexity for insertions, deletions, and lookups.

There's another O(log N) way to save time by using a **Skip list**, which need the basis to be ordered. The idea is to use multiple levels of skip nodes, each of which skips over some number of nodes. When we need to find a node, we start at the top level and move down the levels until we find the node. When we need to insert or delete a node, we update the skip nodes accordingly.

Here's the implementation in C++:

```C++
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

class Node {
    int data;
    Node* next;
};

class SkipNode {
    Node* next;
    int level;
};
void insert(int data) {
    Node* newNode = new Node;
    newNode->data = data;
    newNode->next = NULL;
    SkipNode* current = head;
    int level = 0;
    while (true) {
        int skip = rand() % (1 << level);
        for (int i = 0; i < skip; i++) {
            if (current->next == NULL) {
                current->next = newNode;
                return;
            }
            current = current->next;
        }
        if (current->next == NULL) {
            current->next = newNode;
            return;
        }
        level++;
        current = current->next;
    }
}
void deleteNode(int value) {
    SkipNode* current = head;
    SkipNode* previous = NULL;
    while (current!= NULL) {
        Node* currentNode = current->next;
        while (currentNode!= NULL) {
            if (currentNode->data == value) {
                if (previous == NULL) {
                    current->next = currentNode->next;
                } else {
                    previous->next = currentNode->next;
                }
                delete currentNode;
                return;
            }
            previous = currentNode;
            currentNode = currentNode->next;
        }
        current = current->next;
    }
}
```

In this implementation, we use a SkipNode to represent a skip node. Each SkipNode has a pointer to the next node and a level. The level indicates the number of nodes to skip over when moving down the list. We use a random number to determine the number of nodes to skip over. When we need to insert or delete a node, we update the SkipNodes accordingly. In this way, we are saving the search time from O(n) to O(log N) and meanwhile not using extra memory as we are using in the hashmap way.

### Conclusion

In this article, we discussed the modification of a chained list. We discussed two ways to save memory and two ways to save time. The first way is to reuse the **unused nodes**We also discussed the **memory pool** and the **hashmap** and **skip list**.
In summary, the modification of a chained list can save memory by reusing the unused nodes, and can save time by using a hash table or a skip list. The memory pool and the hashmap and skip list are two ways to save memory and time, respectively.
More reletive practice will be shown in more passages. Wait and see!

# Love your reading!









