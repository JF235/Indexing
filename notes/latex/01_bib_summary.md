# Bibliografia

## Database index (wikipedia)

A database index is a data structure that improves the speed of data retrieval operations on a database table at the cost of additional writes and storage space to maintain the index data structure. Indexes are used to quickly locate data without having to search every row in a database table every time said table is accessed. Indexes can be created using one or more columns of a database table, providing the basis for both rapid random lookups and efficient access of ordered records. 

### Support for fast lookup

Most database software includes indexing technology that enables sub-linear time lookup to improve performance, as linear search is inefficient for large databases.

Suppose a database contains N data items and one must be retrieved based on the value of one of the fields. A simple implementation retrieves and examines each item according to the test. If there is only one matching item, this can stop when it finds that single item, but if there are multiple matches, it must test everything. This means that the number of operations in the average case is O(N) or linear time. Since databases may contain many objects, and since lookup is a common operation, it is often desirable to improve performance.

An index is any data structure that improves the performance of lookup. There are many different data structures used for this purpose. There are complex design trade-offs involving lookup performance, index size, and index-update performance. Many index designs exhibit logarithmic (O(log(N))) lookup performance and in some applications it is possible to achieve flat (O(1)) performance.

## B tree (wikipedia)

In computer science, a B-tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time. The B-tree generalizes the binary search tree, allowing for nodes with more than two children. Unlike other self-balancing binary search trees, the B-tree is well suited for storage systems that read and write relatively large blocks of data, such as databases and file systems.

B-trees were invented by Rudolf Bayer and Edward M. McCreight while working at Boeing Research Labs, for the purpose of efficiently managing index pages for large random-access files. The basic assumption was that indices would be so voluminous that only small chunks of the tree could fit in main memory.

Bayer and McCreight never explained what, if anything, the B stands for.

<img src="imgs/B-tree.svg">

## B+ tree (wikipedia)

A B+ tree is an m-ary tree with a variable but often large number of children per node. A B+ tree consists of a root, internal nodes and leaves. The root may be either a leaf or a node with two or more children.

A B+ tree can be viewed as a [B-tree](#b-tree-wikipedia) in which each node contains only keys (not key–value pairs), and to which an additional level is added at the bottom with linked leaves.

The primary value of a B+ tree is in storing data for efficient retrieval in a block-oriented storage context — in particular, filesystems. This is primarily because unlike binary search trees, B+ trees have very high fanout (number of pointers to child nodes in a node, typically on the order of 100 or more), which reduces the number of I/O operations required to find an element in the tree.

## Intervals in internal nodes

By definition, each value contained within the B+ tree is a key contained in exactly one leaf node. Each key is required to be directly comparable with every other key, which forms a [total order](https://en.wikipedia.org/wiki/Total_order).

> Os identificadores únicos/chaves (keys) são armazenados nos nós intermediários. Para acessar os valores associados a essa chave (ex. nome, sexo, idade) é preciso descer até as folhas.

## References

1. Navathe, Ramez Elmasri, Shamkant B. (2010). Fundamentals of database systems (6th ed.).