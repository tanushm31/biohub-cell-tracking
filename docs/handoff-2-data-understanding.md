# Initial Dataset Observations

## Observation 1

Cells appear as diffuse fluorescent blobs rather than sharp point sources.

Implication:
Detection will likely require local spatial context instead of simple peak finding.

---

## Observation 2

The majority of the volume is low intensity, with a relatively small fraction of bright pixels.

Implication:
Intensity normalization and contrast enhancement may improve detection robustness.

---

## Observation 3

The embryo occupies only a subset of the image volume.

Open Question:
Is this consistent across all embryos, and is cropping beneficial?

## Observation 4 — Cells are densely packed

Maximum intensity projections reveal that neighboring cells are frequently in close proximity and often appear to overlap visually.

### Implication

Cell separation is likely to be one of the primary challenges for the detector. Detection errors in dense regions may propagate into tracking errors.

---

## Observation 5 — Temporal motion appears smooth

Across sampled timepoints, the overall embryo morphology remains stable while cells exhibit relatively small continuous movements.

### Implication

A simple nearest-neighbor tracker may provide a surprisingly strong baseline due to the apparent temporal continuity.

This hypothesis should be validated after implementing the annotation reader.

---

## Observation 6 — Cell morphology appears relatively consistent

Most visible cells exhibit similar apparent size and shape throughout the sequence.

### Implication

Detection architectures may not require extensive multi-scale reasoning during the baseline stage.
