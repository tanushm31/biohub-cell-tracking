from dataclasses import dataclass
    
from src.data.dataloader import BioHubDataset

@dataclass(slots=True)
class CellCountStatistics:
    cells_per_frame: list[int]

    @property
    def average(self) -> float:
        return sum(self.cells_per_frame) / len(self.cells_per_frame)

    @property
    def minimum(self) -> int:
        return min(self.cells_per_frame)

    @property
    def maximum(self) -> int:
        return max(self.cells_per_frame)

@dataclass(slots=True)
class ZDistributionStatistics:
    z_coordinates: list[int]

    @property
    def average(self):
        return sum(self.z_coordinates) / len(self.z_coordinates)

    @property
    def minimum(self):
        return min(self.z_coordinates)

    @property
    def maximum(self):
        return max(self.z_coordinates)
@dataclass
class SampleNodeStatistics:
    nodes_per_sample: list[int]

def analyze_cell_counts(dataset: BioHubDataset) -> CellCountStatistics:
    """
    Compute the number of annotated cells in every frame
    across the entire training dataset.
    """

    cells_per_frame: list[int] = []

    for sample in dataset:
        for t in range(sample.volume.shape[0]):
            count = sum(
                1
                for node in sample.nodes
                if node.t == t
            )

            cells_per_frame.append(count)

    return CellCountStatistics(cells_per_frame)

# def analyze_nodes_per_sample(dataset):

def analyze_z_distribution(
    dataset: BioHubDataset,
) -> ZDistributionStatistics:
    """
    Compute the distribution of z coordinates across all annotated cells
    in the entire training dataset.
    """
    
    z_coordinates = []

    for sample in dataset:
        for node in sample.nodes:
            z_coordinates.append(node.z)

    return ZDistributionStatistics(z_coordinates)