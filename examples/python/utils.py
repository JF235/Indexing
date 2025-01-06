import torch
import hashlib

def gen_data(dimensions, database_size, queries_size):
    DB = torch.randn(database_size, dimensions, dtype=torch.float32)
    Q = torch.randn(queries_size, dimensions, dtype=torch.float32)
    return DB, Q

def get_data(s, options=None):
    if s == 'gen':
        return gen_data(**options)
    else:
        raise NotImplementedError(f"Unknown data source: {s}")

def format_time(seconds):
    units = [
        ("hr", 3600),
        ("min", 60),
        ("s", 1),
        ("ms", 1e-3),
        ("us", 1e-6),
        ("ns", 1e-9)
    ]
    
    for unit, factor in units:
        if seconds >= factor:
            value = seconds / factor
            return f"{value:.2f} {unit}"
    return f"{seconds:.2f} s"

def h(s):
    return hashlib.md5(s).hexdigest()