from element import Element
from ds.lists import LinkedList, SkipList
from random import randint, seed, choice
from inedxing import HNSW
import numpy as np

def create_linked_list(range_min: int, range_max: int,
                       size: int, sorted: bool = True) -> LinkedList:
    random_list = [randint(range_min, range_max) for _ in range(size)]
    
    if sorted:
        random_list.sort()

    linked_list = LinkedList()
    for element in random_list:
        linked_list.append(Element(element))
    
    return linked_list

def create_skiplist(p: float, max_level: int,
    range_min: int, range_max: int, size: int) -> SkipList:
    random_list = [randint(range_min, range_max) for _ in range(size)]
    
    skip_list = SkipList(p, max_level)
    for e in random_list:
        skip_list.insert(Element(e))
    
    return skip_list

def test_linked_list():
    linked_list = create_linked_list(0, 100, 10)
    
    print("Linked list:")
    print(linked_list)
    print("Data:")
    print(f"len(linked_list) = {len(linked_list)}")
    print(f"linked_list.head, linked_list.tail = {linked_list.head}, {linked_list.tail}")

def test_skiplist():
    skip_list = create_skiplist(0.5, 5, 0, 200, 20)
    
    skip_list.print_structure()
    
    e = Element(71)
    r = skip_list.search(e, log = True)
    if r:
        print(f"Found: {r.data}")
    else:
        print(f"Not found.")
    

def test_hnsw():
    dataset = np.random.normal(size=(1000, 32))
    

if __name__ == "__main__":
    seed(42)
    #test_linked_list()
    #test_skiplist()
    test_hnsw()