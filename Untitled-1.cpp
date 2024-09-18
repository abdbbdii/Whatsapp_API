#include <string>
#include <iostream>

using namespace std;

class Node {
public:
    int data;
    Node* next;
    Node(int data) {
        this->data = data;
        this->next = nullptr;
    }
};

class SinglyLinkedList {
private:
    Node* _head;

public:
    SinglyLinkedList() {
        _head = nullptr;
    }
    void insertAtHead(Node* node) {
        node->next = _head;
        _head = node;
    }
    void insertAtTail(Node* node) {
        if (_head == nullptr) {
            _head = node;
            return;
        }
        Node* temp = _head;
        while (temp->next != nullptr) {
            temp = temp->next;
        }
        temp->next = node;
    }
    int search(Node *node) {
        Node* temp = _head;
        int index = 0;
        while (temp != nullptr) {
            if (temp->data == node->data) {
                return index;
            }
            temp = temp->next;
            index++;
        }
        return -1;
    }
    Node operator[](int index) {
        Node* temp = _head;
        for (int i = 0; i < index; i++) {
            temp = temp->next;
        }
        return *temp;
    }
    void display() {
        Node* temp = _head;
        while (temp->next != nullptr) {
            cout << temp->data << ', ';
            temp = temp->next;
        }
        cout << endl;
    }
};

