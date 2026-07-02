from pathlib import Path

from src.common.types import Sample
from src.data.geff_reader import GEFFReader
from src.data.zarr_reader import ZarrReader


class BioHubDataset:

    def __init__(self, root):

        self.root = Path(root)

        self.samples = sorted(
            p.stem
            for p in self.root.glob("*.zarr")
        )

    def __len__(self):

        return len(self.samples)

    def __getitem__(self, idx):
        
        if isinstance(idx, str):
            name = idx
        else:
            name = self.samples[idx]

        volume = ZarrReader(
            self.root / f"{name}.zarr"
        )

        annotations = GEFFReader(
            self.root / f"{name}.geff"
        )

        return Sample(
            name=name,
            volume=volume.array,
            nodes=annotations.nodes,
            edges=annotations.edges,
        )