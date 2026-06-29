# BioHub Cell Tracking During Development

> A modular research framework for 3D cell detection, multi-object tracking, and lineage reconstruction using volumetric microscopy data.

---

## Overview

This repository contains our solution for the Kaggle **BioHub Cell Tracking During Development** competition.

The objective is to reconstruct the life history of cells in a developing zebrafish embryo by:

- Detecting cells in 3D microscopy volumes
- Tracking cells across time
- Identifying cell division (mitosis)
- Producing a lineage graph representing the developmental history of each cell

Rather than treating this as a standard computer vision competition, we approach it as a **spatio-temporal graph reconstruction problem**.

---

## Project Philosophy

This repository is designed as a research project, not a collection of Kaggle notebooks.

Our guiding principles are:

- Build the simplest working baseline first.
- Understand the data before building complex models.
- Keep every component modular and replaceable.
- Improve through error analysis, not random experimentation.
- Every architectural decision should be evidence-driven.

---

## High-Level Architecture

```
3D Microscopy Volume
          │
          ▼
   Cell Detection
          │
          ▼
 Cell Association
 (Tracking)
          │
          ▼
 Lineage Graph
          │
          ▼
 Evaluation
```

Each stage is intentionally independent so individual components can be improved without rewriting the rest of the pipeline.

---

## Repository Structure

```
src/
├── data/          # Dataset loading (.zarr / .geff)
├── detector/      # Cell detection models
├── tracker/       # Cell association & lineage reconstruction
├── evaluator/     # Metric implementation & diagnostics
├── analysis/      # Dataset exploration and statistics
└── utils/         # Shared utilities

docs/              # Design docs and research handoffs
notebooks/         # Exploratory analysis
configs/           # Experiment configuration
outputs/           # Models, predictions and logs
```

---

## Development Roadmap

### Phase 1 — Foundation

- [x] Repository structure
- [x] Initial documentation
- [ ] Development environment
- [ ] Dataset loading
- [ ] Data visualization

### Phase 2 — Baseline

- [ ] Read `.zarr` volumes
- [ ] Read `.geff` annotations
- [ ] Visualize volumes and tracks
- [ ] Build dataset abstraction
- [ ] Implement baseline detector
- [ ] Implement nearest-neighbor tracker
- [ ] Generate first valid submission

### Phase 3 — Research

- [ ] Local evaluation pipeline
- [ ] Error analysis framework
- [ ] Improved tracking algorithms
- [ ] Learned appearance embeddings
- [ ] Motion models
- [ ] Temporal models
- [ ] Ensemble methods

---

## Current Status

**Current milestone:** Foundation

The immediate objective is **not** leaderboard performance.

The goal is to fully understand the dataset and build a clean, modular baseline that future research can build upon.

---

## Documentation

| Document                          | Description                              |
| --------------------------------- | ---------------------------------------- |
| `handoff-1-problem-statement.md`  | Competition overview and research goals  |
| `handoff-2-data-understanding.md` | Dataset exploration notes                |
| `handoff-3-baseline-design.md`    | Baseline architecture                    |
| `handoff-4-evaluation-metric.md`  | Evaluation metric analysis               |
| `handoff-5-error-analysis.md`     | Failure analysis and future improvements |

---

## Long-Term Vision

The objective is not simply to obtain a competitive Kaggle score.

The goal is to build a reusable, modular framework for 3D biological cell tracking that can serve as a foundation for future research and experimentation.
