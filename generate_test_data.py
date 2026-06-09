import struct
import random
import os
import numpy as np

MAX_U32 = 4294967295

def test_basic():
    nums = [0, 1, 100, MAX_U32]
    with open("t1_basic.bin", "wb") as f:
        f.write(struct.pack(">4I", *nums))
    print(
        f"t1_basic.bin:"
        f"sum={sum(nums)} "
        f"min={min(nums)} "
        f"max={max(nums)}"
    )
    print(f"  Size: {os.path.getsize('t1_basic.bin')} bytes")
 
def test_endian():
    nums = [1, 256, 65536, 16777216,]
    with open("t2_endian.bin", "wb") as f:
        f.write(struct.pack(">4I", *nums))
    print(
        f"t2_endian.bin: "
        f"sum={sum(nums)} "
        f"min={min(nums)} "
        f"max={max(nums)}"
    )
    print(f"  Size: {os.path.getsize('t2_endian.bin')} bytes")
 
def test_large_sum():
    count = 10_000_000
    value = MAX_U32
    block_size = 100_000
    block = struct.pack(">I", value) * block_size
    with open("t3_large_sum.bin", "wb") as f:
        for _ in range(count // block_size):
            f.write(block)
    print(
        f"t3_large_sum.bin:"
        f"sum={value * count} "
        f"min={value} "
        f"max={value}"
    )
    print(f"  Size: {os.path.getsize('t3_large_sum.bin') / 1024 / 1024:.1f} MB")
 
def test_random():
    random.seed(42)
    count = 1_000_000
    total_sum = 0
    total_min = MAX_U32
    total_max = 0

    with open("t4_random.bin", "wb") as f:
        for _ in range(count):
            x = random.randint(0, MAX_U32)
            total_sum += x
            total_min = min(total_min, x)
            total_max = max(total_max, x)
            f.write(struct.pack(">I", x))

    print(
        f"t4_random.bin:"
        f"sum={total_sum} "
        f"min={total_min} "
        f"max={total_max}"
    )
    print(f"  Size: {os.path.getsize('t4_random.bin') / 1024 / 1024:.1f} MB")

def generate_2gb_file():
    count = 536_870_912
    chunk_size = 10_000_000
    rng = np.random.default_rng(42)

    with open("t5_2gb.bin", "wb") as f:
        for start in range(0, count, chunk_size):

            size = min(chunk_size, count - start)

            arr = rng.integers(
                0,
                2**32,
                size=size,
                dtype=np.uint32
            )

            arr.byteswap().tofile(f)

            print(
                f"\rWritten {(start + size) * 4 / 1024 / 1024:.0f} MB",
                end=""
            )

    print("\nt5_2gb.bin created")

if __name__ == "__main__":
    test_basic()
    test_endian()
    test_large_sum()
    test_random()

    # generate_2gb_file()