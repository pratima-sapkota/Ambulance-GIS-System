"""
Ambulance GIS System - Geometry Utilities

Provides geometric calculations for the application.
"""

import math
from typing import Tuple, Union


def calculate_distance(
    point1: Tuple[Union[int, float], Union[int, float]],
    point2: Tuple[Union[int, float], Union[int, float]]
) -> float:
    """
    Calculate the Euclidean distance between two points.

    Args:
        point1: First point as (x, y) tuple.
        point2: Second point as (x, y) tuple.

    Returns:
        The Euclidean distance between the two points.
    """
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
