from element import Element

class Node:
    """Node com ponteiros para o próximo e o anterior"""
    def __init__(self, data: Element):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self):
        return f"Node({str(self.data)})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.data < other.data

    def __le__(self, other):
        return self.data <= other.data

    def __gt__(self, other):
        return self.data > other.data

    def __ge__(self, other):
        return self.data >= other.data

    def __hash__(self):
        return hash(self.data)

class MultiNode(Node):
    """Node com uma lista de ponteiros"""
    def __init__(self, data: Element, size: int):
        super().__init__(data)
        self.next = [None] * (size + 1)
    
    def __str__(self):
        return f"MultiNode({str(self.data)})"