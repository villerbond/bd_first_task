import sys
import os
import time
import numpy as np

CHUNK_BYTES = 256 * 1024 * 1024

def main():
    if len(sys.argv) != 2:
        print("help: python calc_data.py <path_to_file>")
        sys.exit(1)

    t_start = time.perf_counter()

    filepath = sys.argv[1]

    total_sum = 0
    total_min = 4294967295
    total_max = 0

    with open(filepath, "rb") as f:
        while True:
            raw = f.read(CHUNK_BYTES)
            if not raw:
                break
            data = np.frombuffer(raw, dtype=">u4")
            total_sum += int(np.sum(data.astype(np.uint64)))
            total_min = min(total_min, int(data.min()))
            total_max = max(total_max, int(data.max()))

    t_end = time.perf_counter()

    print(f"Total time: {t_end - t_start:.2f}s", file=sys.stderr)
    print(f"sum={total_sum}")
    print(f"min={total_min}")
    print(f"max={total_max}")

if __name__ == "__main__":
    main()