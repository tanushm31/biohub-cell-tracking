# Data Understanding

This document summarizes our understanding of the BioHub Cell Tracking dataset after visual inspection, dataset exploration, and quantitative analysis.

---

# Dataset Overview

Each training sample consists of:

- A 4D fluorescence microscopy volume stored in Zarr format.
- A corresponding GEFF annotation graph.
- Graph nodes represent annotated cell centroids.
- Graph edges represent temporal associations between cells across consecutive frames.

Volume dimensions:

- Time (T): 100
- Depth (Z): 64
- Height (Y): 256
- Width (X): 256

Image datatype:

- uint16

---

# Visual Observations

## Observation 1 — Cells appear as diffuse fluorescent blobs

Cells appear as smooth fluorescent regions rather than sharp point sources.

### Implication

Detection will require local spatial context rather than simple peak detection.

---

## Observation 2 — Most voxels contain low intensity values

The majority of the image consists of dark background with relatively sparse bright structures.

### Implication

Intensity normalization may improve detector robustness.

---

## Observation 3 — The embryo occupies only part of the volume

The embryo does not fill the entire imaging volume.

### Status

Further quantitative analysis is required before deciding whether cropping is beneficial.

---

## Observation 4 — Cells are densely packed

Neighboring cells frequently appear close together and sometimes overlap visually.

### Implication

Cell separation will likely be one of the primary challenges for detection.

---

## Observation 5 — Cell morphology appears relatively consistent

Most cells have similar apparent size and shape throughout the sequence.

### Implication

A baseline detector may not require sophisticated multi-scale reasoning.

---

# Verified Findings

The following observations have been confirmed through quantitative analysis.

---

## Finding 1 — Ground-truth annotations are sparse

The competition provides annotations for only a subset of visible cells.

### Implication

Statistics computed from the annotations describe annotated cells rather than the complete biological cell population.

---

## Finding 2 — Annotation density is low

Measured statistics:

- Average annotated cells per frame: **6.70**
- Minimum annotated cells per frame: **0**
- Maximum annotated cells per frame: **33**

### Implication

Detection and evaluation operate on sparse annotations rather than dense segmentation.

---

## Finding 3 — Annotated cells span nearly the entire Z volume

Measured statistics:

- Average annotated Z coordinate: **30.95**
- Minimum Z: **0**
- Maximum Z: **63**

### Implication

No evidence currently supports discarding large portions of the Z dimension.

---

## Finding 4 — Tracking edges connect consecutive frames

Every ground-truth edge connects:

```
Frame t → Frame t + 1
```

No skipped-frame connections were observed.

### Implication

Baseline tracking only needs to associate detections between adjacent frames.

---

## Finding 5 — Typical cell movement is small

Measured movement statistics:

- Mean displacement: **2.13 µm**
- Median displacement: **1.82 µm**
- 95th percentile: **5.34 µm**
- 99th percentile: **8.38 µm**

### Implication

Nearest-neighbor association is well supported as a baseline tracking strategy.

---

## Finding 6 — Large motion outliers are rare

The largest measured displacement was:

- **60.76 µm**

Further investigation showed:

- The eight largest movements originated from a single sample.
- These movements were dominated by unusually large changes in the Z dimension.

### Implication

Tracker hyperparameters should be selected using the movement distribution rather than the maximum observed displacement.

---

# Current Understanding

The dataset exhibits several favorable properties for building a baseline tracker:

- Sparse annotations.
- Smooth temporal motion.
- Consecutive-frame associations.
- Small typical displacements.
- Stable cell morphology.

The primary challenge is expected to be reliable cell detection rather than temporal association.
