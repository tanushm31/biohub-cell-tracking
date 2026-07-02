from pathlib import Path

import zarr


class ZarrReader:
    """
    Lightweight reader for BioHub Zarr microscopy volumes.
    """

    def __init__(self, path: str | Path):

        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(path)

        self.root = zarr.open_group(self.path, mode="r")

        # Competition stores image volume under key "0"
        self.array = self.root["0"]

    @property
    def shape(self):
        return self.array.shape

    @property
    def dtype(self):
        return self.array.dtype

    @property
    def metadata(self):
        return dict(self.array.attrs)

    def __len__(self):
        return self.shape[0]

    def __getitem__(self, idx):
        return self.array[idx]

    def __repr__(self):

        return (
            "ZarrReader("
            f"path='{self.path.name}', "
            f"shape={self.shape}, "
            f"dtype={self.dtype})"
        )