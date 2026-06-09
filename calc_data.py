import sys
import os
import time
import mmap
import numpy as np
import multiprocessing as mp

CHUNK_BYTES = 256 * 1024 * 1024

def process_chunk(args):
    filepath, offset, size = args

    with open(filepath, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        chunk = mm[offset:offset + size]

        data = np.frombuffer(chunk, dtype=">u4")

        chunk_sum = int(data.sum(dtype=np.uint64))
        chunk_min = int(data.min())
        chunk_max = int(data.max())

        return chunk_sum, chunk_min, chunk_max
    
def main():
    if len(sys.argv) != 2:
        print("help: python calc_data.py <path_to_file>")
        sys.exit(1)

    t_start = time.perf_counter()

    filepath = sys.argv[1]
    file_size = os.path.getsize(filepath)

    tasks = []
    offset = 0

    while offset < file_size:
        size = min(CHUNK_BYTES, file_size - offset)

        tasks.append((filepath, offset, size))
        offset += size

    workers = min(mp.cpu_count(), len(tasks))

    with mp.Pool(processes=workers) as pool:
        results = pool.map(process_chunk, tasks)

    total_sum = sum(r[0] for r in results)
    total_min = min(r[1] for r in results)
    total_max = max(r[2] for r in results)

    t_end = time.perf_counter()

    # print(f"Total time: {t_end - t_start:.2f}s", file=sys.stderr)
    print(f"sum={total_sum}")
    print(f"min={total_min}")
    print(f"max={total_max}")

if __name__ == "__main__":
    main()