# Vector Database

Reference: 
- Vector Database 101: Everything You Need to Know
  - https://zilliz.com/learn/introduction-to-unstructured-data
- The Evolution of Milvus: A Cloud-Native Vector Database - Frank Liu, Zilliz: 
  - https://youtu.be/4yQjsY5iD9Q
- Code examples - Frank Liu
  - https://github.com/fzliu/vector-search

## Introduction to Unstructured Data

International Data Corporation predicts that the global datasphere - a measure of the total amount of new data created and stored on persistent storage all around the world - will grow to 400 zettabytes ($400\times 10^{21}$ bytes) by 2028. At that time, over 30% of said data will be generated in real-time, while 80% of all generated data will be unstructured data.

### Structured/ semi-structured/ unstructured data definition

- Unstructured data is data that does not have a predefined data model or is not organized in a predefined manner. Examples include text, images, audio, and video files.
- Structured data: relational databases, spreadsheets, etc. (MySQL, PostgreSQL, etc.)
- Semi-structured data: XML, JSON, etc. (MongoDB, Cassandra, Redis, etc.)

### A crash course on embeddings

The vast majority of neural network models are capable of turning a single piece of unstructured data into a list of floating point values, also known more commonly as an embeddings or embedding vectors. As it turns out, a properly trained neural network can output embeddings that represent the semantic content of the image. With the preeminent ResNet-50 convolutional neural network, an image can be represented as a vector of length 2048.

### Unstructured data processing

Querying MongoDB for the first book from a particular author can be done with the following code snippet (using pymongo):

```python
# pymongo
document = collection.find_one({'Author': 'Bill Bryson'})
```

For SQL databases, the equivalent query would be:

```sql
SELECT * FROM books WHERE Author = 'Bill Bryson' LIMIT 1;
```

Both are deterministic queries, meaning that the result is always the same.

Vector databases, on the other hand, work by querying the database with a vector, that is, the embedding representation of the unstructured data. 

```python
# pymilvus
results = collection.search(embedding, 'embedding', params, limit=10)
```

Internally, queries across large collections of unstructured data are performed using a suite of algorithms collectively known as approximate nearest neighbor search, or ANN search for short. In a nutshell, ANN search is a form of optimization that attempts to find the "closest" point or set of points to a given query vector. Note the "approximate" in ANN. By utilizing clever indexing methods, vector databases have a clear accuracy/performance tradeoff: increasing search runtimes will result in a more consistent database that performs closer to a deterministic system, always returning the absolute nearest neighbors given a query value. Conversely, reducing query times will improve throughput but may result in capturing fewer of a query's true nearest values. In this sense, unstructured data processing is a probabilistic process.

### Conclusion

- Structured/semi-structured data are limited to numeric, string, or time data types. Through the power of modern machine learning, unstructured data is represented as high-dimensional vectors of numerical values.
- These vectors, more commonly known as embeddings, are great for representing the semantic content of the unstructured data. Structured/semi-structured data, on the other hand, is semantically as-is, i.e. the content itself is equivalent to the semantics.
- Searching and analyzing unstructured data is done through ANN search, a process that is inherently probabilistic. Querying across structured/semi-structured data, on the other hand, is deterministic.
- Unstructured data processing is very different from semi-structured data processing, and requires a complete paradigm shift. This naturally necessitates a new type of database - the vector database.

## What is a Vector Database and How Does It Work?

- A vector database is a new database system that stores, indexes, and searches through high dimensional vector embeddings for fast semantic information retrieval and vector semantic search.
- Vector databases are a key infrastructure component of the modern AI stack: Retrieval Augmented Generation (RAG), which augments the output of large language models (LLM) and addresses AI hallucinations by providing the LLM with external knowledge. Vector databases store this external knowledge and find and retrieve contextual information for the LLM to generate more accurate answers.
- Vector databases are widely used for use cases and applications such as chatbots, recommendation systems, image/video/audio search, semantic search, and RAG.
- Mainstream purpose-built vector databases include Milvus, Zilliz Cloud (fully managed Milvus), Qdrant, Weaviate, Pinecone, and Chroma.
- Besides specialized vector databases, many traditional relational databases add a vector plugin capable of performing small-scale vector searches. Such databases include Cassandra, MongoDB, and Pgvector.
- Most vector databases support mainstream indexes such as hierarchical navigable small world (HNSW), locality-sensitive hashing (LSH), and Product Quantization (PQ).

## Compare Vector Databases, Vector Search Libraries, and Vector Search Plugins

...

## Introduction to Milvus Vector Database

...

## Introduction to Vector Similarity Search

Vector search, also known as vector similarity search or nearest neighbor search or semantic search, is a technique used in data retrieval systems to find items that are similar to a given query vector. Unlike traditional keyword search which matches exact words, semantic search understands the intent and contextual meaning behind a query, allowing it to return more relevant results even when the exact keywords are not present in the content. In vector search, we represent data points as vectors in a high-dimensional space. 

The goal of vector search is to efficiently search and retrieve the most relevant vectors that are similar or nearest to a query vector.

### Linear search

Computing the distance from a query vector to all other vectors in the vector database. Due to the lack of space complexity as well as constant space overhead associated with naïve search, this method can often outperform space partitioning even when querying across a moderate number of vectors.

### Space partitioning

K-dimensional trees (kd-trees) are perhaps the most well-known in this family, and work by continuously bisecting the search space (splitting the vectors into “left” and “right” buckets) in a manner similar to binary search trees.

Inverted file index (IVF) is also a form of space partitioning, and works by assigning each vector to its nearest centroid - searches are then conducted by first determining the query vector's closest centroid and conducting the search around there, significantly reducing the total number of vectors that need to be searched. IVF is a fairly popular indexing strategy and is commonly combined with other indexing algorithms to improve performance.

### Quantization

Quantization is a technique for reducing the total size of the database by reducing the precision of the vectors.

Scalar quantization (SQ), for example, works by multiplying high-precision floating point vectors with a scalar value, then casting the elements of the resultant vector to their nearest integers. This not only reduces the effective size of the entire database (e.g. by a factor of eight for conversion from float64_t to int8_t), but also has the positive side-effect of speeding up vector-to-vector distance computations.

Product quantization (PQ) is another quantization technique that works similar to dictionary compression. In PQ, all vectors are split into equally-sized subvectors, and each subvector is then replaced with a centroid.

### HNSW

### ANNOY

Approximate Nearest Neighbors Oh Yeah

ANNOY works by first randomly selecting two vectors in the database and bisecting the search space along the hyperplane separating those two vectors. This is done iteratively until there are fewer than some predefined parameter NUM_MAX_ELEMS per node. Since the resulting index is essentially a binary tree, this allows us to do our search on O(log n) complexity.

### Similarity Metrics

- Floating Point
  - L1: $\sum_i |a_i - b_i|$
  - L2: $\left(\sum_i (a_i - b_i)^2\right)^{1/2}$
  - Cos: $\frac{a\cdot b}{\|a\|\|b\|}$

With a bit of math, we can also show that L2 distance and cosine similarity are effectively equivalent when it comes to similarity ranking for unit norm vectors:

$$(a-b)^T(a - b) = a^Ta - 2a^T b + b^Tb = 2(1-a^Tb)$$

Essentially, for unit norm vectors, L2 distance and cosine similarity are functionally equivalent! Always remember to normalize your embeddings.

- Binary Vectors
  - Tanimoto/Jaccard: $1 - \frac{a\cdot b}{|a|^2 + |b|^2 - a\cdot b}$
  - Hamming: $\sum_i a_i \oplus b_i$

## Vector Index Basics and Inverted File Index

- hash-based indexing (e.g. locality-sensitive hashing),
- tree-based indexing (e.g. ANNOY),
- cluster-based or cluster indexing (e.g. product quantization), and
- graph-based indexing (e.g. Hierarchical navigable small world or HNSW, CAGRA).


1. an optional pre-processing step where vectors may be reduced or optimized prior to indexing,
2. a required primary step which is the core algorithm used for indexing, and
3. an optional secondary step where vectors may be quantized or hashed to further improve search speeds.

Description:

1. The first step simply prepares the raw vectors used for indexing and search without actually building any data structure. The algorithm used here often depends on the application and the upstream vector generation method, but some commonly used ones include L2 normalization, dimensionality reduction, and zero padding. Most vector databases skip this step and leave pre-processing entirely up to the user in the application layer.
2. The primary algorithm is the only mandatory component and forms the crux of the vector index. The output of this step should be a data structure which holds all information necessary to conduct an efficient vector search. Tree-based and graph-based data structures are commonly used here, but a quantization algorithm or a hash based index such as product quantization or locality-sensitive hashing works as well.
3. The secondary step reduces the total size of the index by mapping all floating point values in the dataset into lower-precision integer values, i.e. float64 -> int8 or float32 -> int8. This modification can both reduce the index size as well as improve search speeds, but generally at the cost of some precision. There are a couple different ways this can be done; we'll dive deeper into quantization and hashing in future tutorials.


### Flat Indexing

Naive search

```python
query = np.random.normal(size=(128,))
dataset = np.random.normal(size=(1000, 128))
nearest = np.argmin(np.linalg.norm(dataset - query, axis=1))
```

### Inverted File Index (IVF)

Fancy name aside, IVF is actually fairly simple. An inverted file index reduces the overall search scope by arranging vector space in the entire dataset into partitions. All partitions are associated with a centroid, and every vector in the dataset is assigned to a partition that corresponds to its nearest centroid.

Cluster centroids are usually determined with a clustering algorithm called k-means. K-means is an interative algorithm that works by first randomly selecting a set of K points as clusters. At every iteration, all points in the dataset of vectors are assigned to its nearest centroid, and all centroids are then updated to the mean of each cluster. This process then continues until convergence - a process known as expectation-maximazation for folks familiar with statistics.

```python
import numpy as np
from scipy.cluster.vq import kmeans2
num_part = 16  # number of IVF partitions
dataset = np.random.normal(size=(1000, 128))
(centroids, assignments) = kmeans2(dataset, num_part, iter=32)
```

We'll now need to create the inverted file index by correlating each centroid with a list of vectors within the cluster:

```python
index = [[] for _ in range(num_part)]
for n, k in enumerate(assignments):
    index[k].append(n)  # the nth vector gets added to the kth c
```

With the index in place, we can now restrict the overall search space by searching only the nearest cluster:

```python
query = np.random.normal(size=(128,))
c = np.argmin(np.linalg.norm(centroids - query, axis=1))  # find the nearest partition
nearest = np.argmin(np.linalg.norm(dataset[index[c]] - query, axis=1))  # find nearest neighbor
```

## Scalar Quantization and Product Quantization

Dimensionality reduction methods such as PCA use linear algebra to project the input data into a lower dimensional space. Without getting too deep into the math here, just know that these methods generally aren't used as the primary indexing strategy because they tend to have limitations on the distribution of the data. PCA, for example, works best on data that can be separated into independent, Gaussian distributed components.

Quantization, on the other hand, makes no assumption about the distribution of the data - rather, it looks at each dimension (or group of dimensions) separately and attempts to "bin" each value into one of many discrete buckets. Instead of performing a flat search over all of the original vectors, we can instead perform flat search over the quantized vectors - this can result in reduced memory consumption as well as significant speedup.

```python
# Quantization vs. Dimensionality Reduction
vector.size  # length of our original vector
128
quantized_vector.size  # length of our quantized vector
128
reduced_vector.size  # length of our reduced vector
16

vector.dtype  # data type of our original vector
dtype('float64')
quantized_vector.dtype
dtype('int8')
reduced_vector.dtype
dtype('float64')
```

### Scalar Quantization

Scalar quantization is an important data compression technique that turns floating point values into low-dimensional integers. 

For each vector dimension, scalar quantization takes the maximum and minimum value of that particular dimension as seen across the entire database, and uniformly splits that dimension into bins across its entire range.

```python
import numpy as np
dataset = np.random.normal(size=(1000, 128))

ranges = np.vstack((np.min(dataset, axis=0), np.max(dataset, axis=0)))

starts = ranges[0,:]
steps = (ranges[1,:] - ranges[0,:]) / 255

dataset_quantized = np.uint8((dataset - starts) / steps)
dataset_quantized
array([[136,  58, 156, ..., 153, 182,  30],
       [210,  66, 175, ...,  68, 146,  33],
       [100, 136, 148, ..., 142,  86, 108],
       ...,
       [133, 146, 146, ..., 137, 209, 144],
       [ 63, 131,  96, ..., 174, 174, 105],
       [159,  78, 204, ...,  95,  87, 146]], dtype=uint8)
```

### Product Quantization

Product quantization (PQ) is another data compression technique that is much more powerful and flexible to quantize vectors when compared with scalar quantization. A major disadvantage of scalar quantization is that it does not take into consideration the distribution of values in each dimension.

The primary idea behind product quantization is to algorithmically split a high-dimensional vector into a lower dimensional subspace, with dimension of the subspace corresponding to multiple dimensions in the original high-dimensional vector. This reduction process is typically done using a special algorithm called the Lloyd's algorithm, a quantizer which is effectively equivalent to k-means clustering.

1. Given a dataset of N total vectors, we'll first divide each vector into `M` subvectors (also known as a subspace). These subvectors don't necessarily have to be the same length, but in practice they almost always are.
2. We'll then use k-means (or some other clustering algorithm) for all subvectors in the dataset. This will give us a collection of `K` centroids for each subspace, each of which will be assigned its own unique ID.
3. With all centroids computed, we'll replace all subvectors in the original dataset with the ID of its closest centroid.

```python
import numpy as np
dataset = np.random.normal(size=(1000, 128))

(M, K) = (16, 256)

sublen = dataset.shape[1] // M
subspace = dataset[:,0:sublen]  # this is the 0th subspace

from scipy.cluster.vq import kmeans2
(centroids, assignments) = kmeans2(subspace, K, iter=32)
quantized = np.uint8(assignments)
```

We can expend a bit of extra memory to compute distance tables for all centroids in each subspace.

## HNSW

[Refer to](hnsw.md)

## 