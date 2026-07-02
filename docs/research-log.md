# BioHub Cell Tracking - Research Log

This document records every verified observation, assumption, experiment and conclusion throughout the competition.

Unlike the handoff documents, this file evolves continuously.

---

# Project Timeline

## Phase 1 - Understanding the Competition

### Status

✅ Completed

### Summary

- Read and understood the competition objective.
- Task consists of two coupled problems:
  1. Detect cells in each frame.
  2. Link detections across time into cell tracks.
- Final prediction is a graph composed of nodes (detections) and edges (temporal links).

---

## Phase 2 - Understanding the Evaluation Metric

### Status

✅ Completed

### Summary

Final score:

score = adjusted_edge_jaccard + 0.1 × division_jaccard

### Important Takeaways

- Edge accuracy contributes almost all of the score.
- Cell division contributes an additional bonus.
- Nodes are matched using centroid distance.
- Over-predicting cells is penalized.
- Ground truth annotations are sparse.

---

## Phase 3 - Understanding the Dataset

### Status

✅ Completed

### Dataset

Image Volume

- Shape: (100, 64, 256, 256)
- Format: Zarr v3
- Dtype: uint16

Annotation Format

- GEFF graph
- Nodes
  - id
  - t
  - z
  - y
  - x
- Edges
  - source_id
  - target_id

Important

Each sample contains:

Image Volume
↓

Annotated Cell Centers
↓

Temporal Graph

---

## Phase 4 - Data Infrastructure

### Status

✅ Completed

Implemented

- Node
- Edge
- Sample
- ZarrReader
- GEFFReader
- BioHubDataset

Validation

- Successfully loaded Zarr volumes.
- Successfully parsed GEFF annotations.
- Successfully created dataset abstraction.

---

## Phase 5 - Coordinate Validation

### Status

✅ Completed

Experiment

Overlayed GEFF centroids on microscopy images.

Result

✅ Annotation coordinates align correctly with fluorescent cells.

Conclusion

Coordinate system is validated.

No axis flips or indexing issues detected.

---

# Verified Observations

## Dataset

### Observation 1

Ground truth annotations are sparse.

Evidence

Competition documentation explicitly states that not every visible cell is annotated.

Implication

Statistics computed from the annotations describe annotated cells, not the total biological cell population.

---

### Observation 2

The data loading pipeline is validated.

Evidence

Overlay visualization matches annotated centroids to fluorescent cells.

Confidence

High

---

### Observation 3

## Z Distribution

### Results

- Average annotated Z coordinate: 30.95
- Minimum annotated Z coordinate: 0
- Maximum annotated Z coordinate: 63

### Observations

- Annotated cells span nearly the full depth of the image volume.
- No strong global bias toward shallow or deep Z slices.
- Distribution is not perfectly uniform and contains several peaks.
- Current evidence does not justify cropping the Z dimension based solely on annotations.

# Dataset Statistics

## Annotated Cell Counts

Current Results

- Samples: 199
- Average annotated cells per frame: 6.70
- Minimum annotated cells per frame: 0
- Maximum annotated cells per frame: 33

Observations

- Annotation density varies significantly.
- Empty annotated frames exist.
- These statistics describe annotated cells only.

---

# Assumptions

These are hypotheses, not verified facts.

## A1

Average visible cells are significantly higher than average annotated cells.

Status

Unverified

Planned Experiment

Estimate visible cell count using simple blob detection.

---

## A2

Cell movement between consecutive frames is relatively small.

Status

Unverified

Planned Experiment

Movement statistics.

---

## A3

Only part of the Z volume contains cells.

Status

Unverified

Planned Experiment

Z-distribution analysis.

---

# Open Questions

- Average cell displacement?
- Distribution of track lengths?
- Number of division events?
- Typical nearest-neighbor distance?
- Annotation density versus actual density?
- Which Z slices contain most cells?

---

# Future Experiments

Priority 1

- Dataset statistics
- Z-distribution
- Nodes per sample

Priority 2

- Movement statistics
- Track statistics
- Division analysis

Priority 3

- Baseline detector
- Baseline tracker

---

# Lessons Learned

## Lesson 1

Validate every assumption with data before designing algorithms.

## Lesson 2

Infrastructure should stabilize early.

## Lesson 3

The dataset should determine algorithmic choices—not intuition.
