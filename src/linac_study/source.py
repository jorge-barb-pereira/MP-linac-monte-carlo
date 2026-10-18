"""Finite-interval Cauchy source distributions, using exact bin probabilities."""
import numpy as np


def bin_probabilities(edges, location, scale):
    """Normalize CDF differences on the provided finite interval.

    A radius distribution is a probability per dr, not an areal density.
    Location and scale have the same units as edges; scale is half the FWHM.
    """
    edges = np.asarray(edges, dtype=float)
    if (edges.ndim != 1 or len(edges) < 2 or not np.all(np.isfinite(edges))
            or np.any(np.diff(edges) <= 0) or not np.isfinite(location)
            or not np.isfinite(scale) or scale <= 0):
        raise ValueError("Need finite increasing edges, finite location and positive scale")
    masses = np.diff(np.arctan((edges-location)/scale))/np.pi
    total = masses.sum()
    if not np.isfinite(total) or total <= 0 or np.any(masses < 0):
        raise ValueError("Interval probability is numerically unresolved")
    return masses/total
