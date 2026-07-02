from dataclasses import dataclass
@dataclass
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