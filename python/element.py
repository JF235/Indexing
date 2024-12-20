class Element:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)
    
    def __format__(self, format_spec):
        return format(self.data, format_spec)

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

    def dump(self):
        print(self)