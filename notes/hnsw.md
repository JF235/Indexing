# Hierarchical Navigable Small Worlds (HNSW)

## What is HNSW?

Hierarchical Navigable Small World (HNSW) is a graph-based algorithm that performs approximate nearest neighbor (ANN) searches in vector databases.

## How does HNSW work (in a nutshell)?

At Indexing time, HNSW builds a layered graph structure from the dataset. 

At query time, it traverses from the top layer to the bottom layer until it finds the nearest neighbor.

It is based in two main ideas:
1. The SkipList data structure. Where a layered approach is used to speed up the search.
2. The Navigable Small World. Where the graph is constructed in such a way that the average path length is small.

## The SkipList

Linked List: $O(n)$ access time with $O(n)$ space complexity.

Skip List: $O(\lg n)$ access time with $O(n\lg n)$ space complexity (+ overhead for insertion and deletion).

A Skip List (SL) is a multi-level linked list where ther upper levels maintain long connections. As we move down, the connections become shorter, with the bottom level being the original linked list.

The $i$-th level of the Skip List contains on average  $p$% of the elements of the $(i-1)$-th level.
- At 0, $n$ elements.
- At $i-1$, $n \cdot p^{i-1}$ elements, on average.
- At $i$, $n \cdot p^i$ elements, on average.

The maximum height is given when $n p^{h_\text{max}}  = 1$, in this case we have

$$\log_p(p^{h_\text{max}}) = \log_p(1/n) \Rightarrow {h_\text{max}} = \log_{1/p}(n)$$

for $n, p > 0$.

## Navigable Small World

The Navigable Small World (NSW) is a graph based on the Small World network model. It is constructed in such a way that the average path length is small. It can be used to perform approximate nearest neighbor searches, where the search is performed by traversing the graph in a greedy manner (i.e., always moving to the neighbor that is closest to the query point).

## Hierarchical Navigable Small World (HNSW)

HNSW extends the NSW by adding a hierarchical structure to the graph, like the Skip List. The graph is constructed in such a way that the average path length is small, and the search is performed by traversing the graph in a greedy manner, from the top layer to the bottom layer.


### Search Layer

- Use a Heap to implement the priority queue of candidates to visit.
- Choose the entry point (EP) to start the search and populate the heap with it.
- Build a set of visited nodes.
- Build a list of nearest neighbors (nns) to keep track of the best candidates. It is ordered by distance to the query point.

1. While the heap is not empty:
    1. Pop the top element from the heap.
    2. If the element is farther from the farthest neighbor, break the loop (The best elements have been found already).
    3. For each neighbor of the element:
        1. If is not in the visited set, add it to the heap.
        2. If the neighbor is farther than the farthest, skip it.
        3. Push the neighbor to the heap.
        4. Do an insort (sorted insert) in the nns list.