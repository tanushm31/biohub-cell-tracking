from dataclasses import dataclass
from typing import Any
from src.data.zarr_reader import ZarrReader

@dataclass(frozen=True, slots=True)
class Node:

    id: int

    t: int

    z: float

    y: float

    x: float

    confidence: float = 1.0

@dataclass
class Edge:

    source_id: int

    target_id: int

@dataclass(slots=True, frozen=True)
class Sample:
    """
    One annotated microscopy sample.

    Consists of:
        - A 4D microscopy volume
        - Annotated cell detections
        - Annotated temporal edges
    """

    name: str
    volume: ZarrReader 
    nodes: tuple[Node, ...]
    edges: tuple[Edge, ...]