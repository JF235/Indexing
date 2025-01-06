import faiss
import torch
import numpy as np
import time
from utils import get_data, format_time, h

DEV = 'cuda' if torch.cuda.is_available() else 'cpu'

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

def main(d = 128, nd = 1000000, nq = 100, K = 10):
    

    # Generate data
    torch.manual_seed(42)

    DB, Q = get_data('gen', options = dict(
        dimensions=d, database_size=nd, queries_size=nq
        ))
    

    print(f"DB.shape: {tuple(DB.shape)}, Q.shape: {tuple(Q.shape)}")

    # Build the index
    Qnp, DBnp = Q.cpu().numpy(), DB.cpu().numpy()
    res = faiss.StandardGpuResources()  # use a single GPU
    index_flat = faiss.IndexFlatL2(d)  # build a flat (CPU) index
    gpu_index_flat = faiss.index_cpu_to_gpu(res, 0, index_flat)
    gpu_index_flat.add(DBnp)
    index_flat.add(DBnp)

    start = time.perf_counter()
    distances, indexes = index_flat.search(Qnp, K)
    end = time.perf_counter()
    print(f"IndexFlatL2 CPU: {format_time(end - start)}")

    start = time.perf_counter()
    distances, indexes = gpu_index_flat.search(Qnp, K)
    end = time.perf_counter()
    print(f"IndexFlatL2 GPU: {format_time(end - start)}")


    distances_naive, indexes_naive = naive_search(DB, Q, k=K, logTime=True)
    distances_naive = distances_naive.cpu().numpy()
    indexes_naive = indexes_naive.cpu().numpy()

    assert np.array_equal(indexes, indexes_naive)
    assert np.allclose(np.sqrt(distances), distances_naive)


    print(f"Hash(indexes): {h(indexes.tobytes())}")
    print(f"Hash(indexes_naive): {h(indexes_naive.tobytes())}")

    print("Ok")

if __name__ == "__main__":

    main()