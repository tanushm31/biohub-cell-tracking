from dataclasses import dataclass

import numpy as np
from skimage.feature import peak_local_max


@dataclass(slots=True, frozen=True)
class PeakDetectionConfig:
    """
    Configuration for 3D local maxima detection.
    """

    minimum_distance: int = 3
    threshold_abs: float = 0.30
    exclude_border: bool = False


def detect_local_maxima(
    volume: np.ndarray,
    config: PeakDetectionConfig | None = None,
) -> np.ndarray:
    """
    Detect candidate cell centers in a 3D volume.

    Parameters
    ----------
    volume
        Preprocessed volume with shape (Z, Y, X).

    Returns
    -------
    ndarray
        Array of shape (N, 3) containing (z, y, x)
        coordinates of detected peaks.
    """

    if config is None:
        config = PeakDetectionConfig()

    peaks = peak_local_max(
        volume,
        min_distance=config.minimum_distance,
        threshold_abs=config.threshold_abs,
        exclude_border=config.exclude_border,
    )

    return peaks