from pathlib import Path

from src.data.zarr_reader import ZarrReader

sample = next(Path("data/raw/train").glob("*.zarr"))

reader = ZarrReader(sample)

print(reader)

print("Shape:", reader.shape)

print("Dtype:", reader.dtype)

print("Frames:", len(reader))

print("Frame 0:", reader[0].shape)