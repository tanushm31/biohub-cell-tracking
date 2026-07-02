from dataclasses import dataclass

import numpy as np
from scipy.ndimage import gaussian_filter


@dataclass(slots=True, frozen=True)
class PreprocessingConfig:
    """
    Configuration for the preprocessing pipeline.
    """

    lower_percentile: float = 1.0
    upper_percentile: float = 99.0
    gaussian_sigma: float = 1.0


def normalize_percentile(
    volume: np.ndarray,
    lower_percentile: float = 1.0,
    upper_percentile: float = 99.0,
) -> np.ndarray:
    """
    Normalize a volume into the range [0, 1] using robust percentiles.
    """

    low = np.percentile(volume, lower_percentile)
    high = np.percentile(volume, upper_percentile)

    volume = np.clip(volume, low, high)

    volume = (volume - low) / (high - low + 1e-8)

    return volume.astype(np.float32)


def gaussian_blur(
    volume: np.ndarray,
    sigma: float = 1.0,
) -> np.ndarray:
    """
    Apply Gaussian smoothing.
    """

    return gaussian_filter(volume, sigma=sigma)


def maximum_intensity_projection(
    volume: np.ndarray,
) -> np.ndarray:
    """
    Compute the Maximum Intensity Projection (MIP)
    over the Z dimension.

    Input:
        (Z, Y, X)

    Output:
        (Y, X)
    """

    return volume.max(axis=0)


def preprocess(
    volume: np.ndarray,
    config: PreprocessingConfig | None = None,
) -> np.ndarray:
    """
    Complete preprocessing pipeline.
    """

    if config is None:
        config = PreprocessingConfig()

    volume = normalize_percentile(
        volume,
        config.lower_percentile,
        config.upper_percentile,
    )

    volume = gaussian_blur(
        volume,
        config.gaussian_sigma,
    )

    return volume