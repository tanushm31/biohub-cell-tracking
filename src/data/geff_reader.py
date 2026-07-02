"""
Read BioHub cell tracking annotations stored in GEFF format.

Responsibilities:
    - Open a GEFF annotation store
    - Read node annotations
    - Read edge annotations
    - Convert annotations into domain objects (Node, Edge)

Does NOT:
    - Perform graph analysis
    - Build tracks
    - Validate annotations
    - Compute statistics
"""

from pathlib import Path

import zarr

from src.common.types import Edge, Node


class GEFFReader:
    """Lightweight reader for BioHub GEFF annotation files."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(f"GEFF dataset not found: {self.path}")

        self.root = zarr.open_group(self.path, mode="r")

        self._nodes = self._load_nodes()
        self._edges = self._load_edges()

    def _load_nodes(self) -> tuple[Node, ...]:
        """Load all annotated nodes."""

        node_ids = self.root["nodes"]["ids"][:]

        t = self.root["nodes"]["props"]["t"]["values"][:]
        z = self.root["nodes"]["props"]["z"]["values"][:]
        y = self.root["nodes"]["props"]["y"]["values"][:]
        x = self.root["nodes"]["props"]["x"]["values"][:]

        nodes = tuple(
            Node(
                id=int(node_ids[i]),
                t=int(t[i]),
                z=int(z[i]),
                y=int(y[i]),
                x=int(x[i]),
            )
            for i in range(len(node_ids))
        )

        return nodes

    def _load_edges(self) -> tuple[Edge, ...]:
        """Load all graph edges."""

        edge_array = self.root["edges"]["ids"][:]

        edges = tuple(
            Edge(
                source_id=int(source),
                target_id=int(target),
            )
            for source, target in edge_array
        )

        return edges

    @property
    def nodes(self) -> tuple[Node, ...]:
        """Return all annotated nodes."""
        return self._nodes

    @property
    def edges(self) -> tuple[Edge, ...]:
        """Return all graph edges."""
        return self._edges

    @property
    def metadata(self) -> dict:
        """Return GEFF metadata."""
        return dict(self.root.attrs)
    #okß
    def __repr__(self) -> str:
        return (
            f"GEFFReader("
            f"path='{self.path.name}', "
            f"nodes={len(self.nodes)}, "
            f"edges={len(self.edges)})"
        )