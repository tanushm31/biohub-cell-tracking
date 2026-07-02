from dataclasses import dataclass
from math import sqrt
import matplotlib.pyplot as plt
from src.common.types import Node, Edge
from src.data.dataloader import BioHubDataset

# Physical voxel spacing (µm)
VOXEL_SIZE_X = 0.40625
VOXEL_SIZE_Y = 0.40625
VOXEL_SIZE_Z = 1.625


@dataclass(slots=True)
class MovementStatistics:
    displacements: list[float]

    @property
    def average(self) -> float:
        return sum(self.displacements) / len(self.displacements)

    @property
    def minimum(self) -> float:
        return min(self.displacements)

    @property
    def maximum(self) -> float:
        return max(self.displacements)


@dataclass(slots=True)
class MovementExample:
    distance: float

    sample_name: str

    edge: Edge

    source: Node

    target: Node

def euclidean_distance(source: Node, target: Node) -> float:
    """
    Compute physical distance (µm) between two annotated nodes.
    """

    dx = (target.x - source.x) * VOXEL_SIZE_X
    dy = (target.y - source.y) * VOXEL_SIZE_Y
    dz = (target.z - source.z) * VOXEL_SIZE_Z

    return sqrt(dx * dx + dy * dy + dz * dz)


def analyze_movement(
    dataset: BioHubDataset,
) -> MovementStatistics:
    """
    Compute movement statistics using the ground-truth tracking graph.

    Every edge represents one cell moving from one frame
    to the next.
    """

    displacements: list[float] = []

    for sample in dataset:

        node_lookup = {
            node.id: node
            for node in sample.nodes
        }

        for edge in sample.edges:

            source = node_lookup[edge.source_id]
            target = node_lookup[edge.target_id]

            distance = euclidean_distance(source, target)

            displacements.append(distance)

    return MovementStatistics(displacements)

def plot_movement_histogram(
    stats: MovementStatistics,
    bins: int = 50,
) -> None:
    """
    Plot the distribution of ground-truth cell displacements.
    """

    plt.figure(figsize=(8, 4))

    plt.hist(
        stats.displacements,
        bins=50,
        range=(0, 10),
    )

    plt.xlabel("Displacement (µm)")
    plt.ylabel("Frequency")
    plt.title("Ground Truth Cell Movement (0–10 µm)")

    plt.tight_layout()

    plt.show()

def largest_movements(
    dataset: BioHubDataset,
    top_k: int = 10,
) -> list[MovementExample]:
    """
    Return the largest ground-truth movements in the dataset.

    Useful for investigating outliers such as:
        - division events
        - annotation mistakes
        - unusually fast moving cells
    """

    movements: list[MovementExample] = []

    for sample in dataset:

        node_lookup = {
            node.id: node
            for node in sample.nodes
        }

        for edge in sample.edges:

            source = node_lookup[edge.source_id]
            target = node_lookup[edge.target_id]

            distance = euclidean_distance(source, target)

            movements.append(
                MovementExample(
                    distance=distance,
                    sample_name=sample.name,
                    edge=edge,
                    source=source,
                    target=target,
                )
            )

    movements.sort(
        key=lambda movement: movement.distance,
        reverse=True,
    )

    return movements[:top_k]

import random

def plot_movement_vectors(
    sample,
    z: int | None = None,
    max_arrows: int = 300,
):
    """
    Plot ground-truth movement vectors for one sample.
    """

    node_lookup = {
        node.id: node
        for node in sample.nodes
    }

    mip = sample.volume[0].max(axis=0)

    plt.figure(figsize=(8, 8))
    plt.imshow(mip, cmap="gray")

    count = 0
    

    edges = random.sample(
        sample.edges,
        min(max_arrows, len(sample.edges)),
    )

    for edge in edges:

        source = node_lookup[edge.source_id]
        target = node_lookup[edge.target_id]

        if z is not None and source.z != z:
            continue

        distance = euclidean_distance(source, target)
        plt.arrow(
            source.x,
            source.y,
            target.x - source.x,
            target.y - source.y,
            head_width=1.5,
            length_includes_head=True,
            alpha=0.5,
            color = plt.cm.viridis(distance / 10),
        )

        count += 1

        if count >= max_arrows:
            break

    plt.gca().invert_yaxis()

    plt.title("Ground Truth Movement Vectors")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()




def visualize_movement_example(
    dataset: BioHubDataset,
    movement: MovementExample,
    crop_size: int = 64,
) -> None:
    """
    Visualize one ground-truth movement.

    The same crop window is used for both frames so the actual
    displacement becomes visible.
    """

    sample = dataset[movement.sample_name]

    source = movement.source
    target = movement.target

    # Extract the correct z slice from each frame
    source_image = sample.volume[source.t][source.z]
    target_image = sample.volume[target.t][target.z]

    half = crop_size // 2

    # Shared crop centered between source and target
    center_x = (source.x + target.x) // 2
    center_y = (source.y + target.y) // 2

    left = max(0, center_x - half)
    right = min(source_image.shape[1], center_x + half)

    top = max(0, center_y - half)
    bottom = min(source_image.shape[0], center_y + half)

    source_crop = source_image[top:bottom, left:right]
    target_crop = target_image[top:bottom, left:right]

    # Convert global coordinates into crop coordinates
    source_x = source.x - left
    source_y = source.y - top

    target_x = target.x - left
    target_y = target.y - top

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(source_crop, cmap="gray")
    axes[0].scatter(
        source_x,
        source_y,
        s=120,
        facecolors="none",
        edgecolors="red",
        linewidths=2,
    )
    axes[0].set_title(f"Source\n t={source.t}, z={source.z}")
    axes[0].axis("off")

    axes[1].imshow(target_crop, cmap="gray")
    axes[1].scatter(
        target_x,
        target_y,
        s=120,
        facecolors="none",
        edgecolors="lime",
        linewidths=2,
    )
    axes[1].set_title(f"Target\n t={target.t}, z={target.z}")
    axes[1].axis("off")

    plt.suptitle(
        f"{movement.sample_name}\n"
        f"Movement = {movement.distance:.2f} µm"
    )

    plt.tight_layout()
    plt.show()

import numpy as np

def summarize_movement(stats: MovementStatistics) -> dict[str, float]:
    d = np.array(stats.displacements)

    return {
        "mean": float(d.mean()),
        "median": float(np.median(d)),
        "std": float(d.std()),
        "p90": float(np.percentile(d, 90)),
        "p95": float(np.percentile(d, 95)),
        "p99": float(np.percentile(d, 99)),
        "max": float(d.max()),
    }

def axis_displacement(source: Node, target: Node):
    return {
        "dx_um": abs(target.x - source.x) * VOXEL_SIZE_X,
        "dy_um": abs(target.y - source.y) * VOXEL_SIZE_Y,
        "dz_um": abs(target.z - source.z) * VOXEL_SIZE_Z,
    }