"""
Utility modules for the Ambulance GIS System.

Contains shared utilities:
- geometry: Distance calculations
- validators: Input validation
- logger: Logging configuration
"""

from ambulance_gis.utils.geometry import calculate_distance
from ambulance_gis.utils.validators import ValidationError, validate_location, validate_speed, validate_route
from ambulance_gis.utils.logger import app_logger, setup_logger

__all__ = [
    "calculate_distance",
    "ValidationError",
    "validate_location",
    "validate_speed",
    "validate_route",
    "app_logger",
    "setup_logger",
]
