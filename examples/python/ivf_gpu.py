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

def main(d = 128, nd = 1000000, nq = 100, K = 10, nlist = 1000, nprobe = 500):

    # Generate data
    torch.manual_seed(42)

    DB, Q = get_data('gen', options = dict(
        dimensions=d, database_size=nd, queries_size=nq
        ))

    print(f"DB.shape: {tuple(DB.shape)}, Q.shape: {tuple(Q.shape)}")

    res = faiss.StandardGpuResources()  # use a single GPU
    quantizer = faiss.IndexFlatL2(d)  # the other index
    index_ivf = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
    # here we specify METRIC_L2, by default it performs inner-product search
    DBnp, Qnp = DB.cpu().numpy(), Q.cpu().numpy()

    # make it an IVF GPU index
    gpu_index_ivf = faiss.index_cpu_to_gpu(res, 0, index_ivf)

    assert not gpu_index_ivf.is_trained
    gpu_index_ivf.train(DBnp)        # add vectors to the index
    assert gpu_index_ivf.is_trained

    gpu_index_ivf.add(DBnp)          # add vectors to the index

    gpu_index_ivf.nprobe = nprobe
    start = time.perf_counter()
    distances, indexes = gpu_index_ivf.search(Qnp, K)  # actual search
    end = time.perf_counter()
    print(f"IVF GPU: {format_time(end - start)}")

    # Naive Search for comparison
    distances_naive, indexes_naive = naive_search(DB, Q, k = K, logTime=True)
    distances_naive = distances_naive.cpu().numpy()
    indexes_naive = indexes_naive.cpu().numpy()

    p = []
    for i in range(nq):
        # Count collision percentage between distances[i] and distances_naive[i]
        bool_mask = np.isin(indexes[0], indexes_naive[0])
        p.append( sum(bool_mask) / len(bool_mask) )

    print(f"Recall: {np.mean(p) * 100:.2f}%")

if __name__ == "__main__":

    main()