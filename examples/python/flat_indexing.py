import faiss
import torch
import numpy as np
import time
from utils import get_data, format_time, h


def naive_search(DB: torch.Tensor, Q: torch.Tensor, k: int = 10, logTime: bool = False) -> tuple[torch.Tensor, torch.Tensor]:
    """ Naive search using `torch.cdist` """
    distances = []
    indexes = []

    # Move to device
    DB = DB.to(DEV)
    Q = Q.to(DEV)

    start = time.perf_counter()

    distances, indexes = torch.cdist(Q, DB, p=2).topk(k, dim=1, largest=False)

    end = time.perf_counter()

    if logTime:
        print(f"naive search ({DEV}): {format_time(end - start)}")
    
    return distances, indexes

def main():
    d = 128
    nd = 1000000
    nq = 100

    # Generate data
    torch.manual_seed(42)

    DB, Q = get_data('gen', options = dict(
        dimensions=d, database_size=nd, queries_size=nq
        ))
    

    print(f"DB.shape: {tuple(DB.shape)}, Q.shape: {tuple(Q.shape)}")

    # Build the index
    flat_index = faiss.IndexFlatL2(d)
    flat_index.add(DB)

    # Flat indexing 
    start = time.perf_counter()
    distances, indexes = flat_index.search(Q, 10)
    end = time.perf_counter()
    print(f"IndexFlatL2: {format_time(end - start)}")


    distances_naive, indexes_naive = naive_search(DB, Q, k=10, logTime=True)
    indexes_naive = indexes_naive.numpy()

    assert np.array_equal(indexes, indexes_naive)
    assert np.allclose(np.sqrt(distances), distances_naive)


    print(f"Hash(indexes): {h(indexes.tobytes())}")
    print(f"Hash(indexes_naive): {h(indexes_naive.tobytes())}")

    print("Ok")

if __name__ == "__main__":
    DEV = 'cuda' if torch.cuda.is_available() else 'cpu'

    main()