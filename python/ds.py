from element import Element
from node import Node, MultiNode
from random import random

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def __contains__(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def __getitem__(self, index):
        self.check_index(index)
        
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def __setitem__(self, index, data):
        self.check_index(index)

        current = self.head
        for _ in range(index):
            current = current.next
        current.data = data

    def check_index(self, index):
        if index < 0 or index >= self.size:
            raise IndexError
    
    def append(self, data: Element):
        new_node = Node(data)
        if self.size == 0:
            self.head = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
        self.tail = new_node
        self.size += 1

    def insert(self, index, data):
        self.check_index(index)
        
        new_node = Node(data)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            if self.size == 0:
                self.tail = new_node
                new_node.next.prev = new_node
        else:
            # A -> C, to insert (B)
            current = self.head
            for _ in range(index - 1):
                current = current.next
            # (B) -> C
            new_node.next = current.next
            current.prev = new_node
            # A -> (B)
            current.next = new_node
            new_node.prev = current
            if index == self.size:
                self.tail = new_node
        self.size += 1
    
    def __str__(self):
        return "[" + " -> ".join(str(node) for node in self) + "]"

class SkipList:
    
    def __init__(self, p: float = 0.5, max_level: int = 3):
        self.p = p
        self.level = 0
        self.max_level = max_level
        self.head = MultiNode(None, max_level)
        self.size = 0
        
        
    def __len__(self):
        return self.size
    
    def insert(self, data):
        """Insert a new node in the skip list"""

        # List to store the update pointers
        update = [None] * (self.max_level + 1)
        
        current = self.head

        # Search for the position to insert the new node
        # Traverse all the levels
        for i in range(self.level, -1, -1):
            # Traverse the level i...
            while current.next[i] and current.next[i].data < data:
                current = current.next[i]
            #...finished traversing the level i
            
            # Store the last node visited
            update[i] = current

        # Coin toss to determine the level of the new node
        new_level = self.random_level()

        # If the new level is greater than the current level...
        if new_level > self.level:
            #...update the list
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.head
            self.level = new_level

        # Create the node and update the pointers
        new_node = MultiNode(data, new_level)
        
        # Inserting (B) in A -> C
        # A stores the last node visited in the level i
        for i in range(new_level + 1):
            # (B) -> C
            new_node.next[i] = update[i].next[i]
            # A -> (B)
            update[i].next[i] = new_node
        
        self.size += 1
    
    def search(self, data: Element, log: bool = False):
        """Search for a node in the skip list"""
        current = self.head
        idx = -1
        
        # Traverse all the levels
        for i in range(self.level, -1, -1):
            if log:
                print(f"Level {i}:", end = "")
            # Traverse the level i...
            while current.next[i] and current.next[i].data < data:
                if log:
                    print(f"  {current.next[i].data}", end = "")
                current = current.next[i]
                idx += 1
            #...finished traversing the level i
            if log:
                print()
            
        #...finished traversing all the levels
        current = current.next[0]
        if current and current.data == data:
            idx += 1
            return current
        
        return None
    
    def random_level(self):
        """ Returns a random level for the new node """
        level = 0
        while random() < self.p and level < self.max_level:
            level += 1
        return level

    def __str__(self):
        current = self.head.next[0]
        nodes = []
        while current:
            nodes.append(str(current))
            current = current.next[0]
        return "[" + " -> ".join(nodes) + "]"

    def print_structure(self):
        # Traverse the levels starting from the bottom and store into a
        # matrix (levels x elements)
        matrix = [[None for _ in range(self.size)] for _ in range(self.level)]
        
        current = self.head.next[0]
        i = 0
        while current:
            matrix[0][i] = current
            for j in range(len(current.next) - 1):
                if current.next[j]:
                    matrix[j][i] = current
            current = current.next[0]
            i += 1
        
        for i in range(self.level - 1, -1, -1):
            for j in range(self.size):
                print(f"{matrix[i][j].data if matrix[i][j] else '':<4}", end="")
            print()
            