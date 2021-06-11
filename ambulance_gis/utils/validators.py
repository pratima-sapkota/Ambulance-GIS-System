"""
Ambulance GIS System - Input Validators

Provides validation functions for user input with descriptive error messages.
"""

from typing import Optional

from config import ui_config


class ValidationError(Exception):
    """Exception raised when validation fails."""

    def __init__(self, message: str, field_name: Optional[str] = None):
        """
        Initialize a ValidationError.

        Args:
            message: The error message describing the validation failure.
            field_name: Optional name of the field that failed validation.
        """
        self.message = message
        self.field_name = field_name
        super().__init__(self.message)


def validate_location(location: str, field_name: str) -> None:
    """
    Validate that a location is selected and valid.

    Args:
        location: The location value to validate.
        field_name: Name of the field (e.g., "Source", "Destination") for error messages.

    Raises:
        ValidationError: If the location is empty or not in the valid locations list.
    """
    if not location or location.strip() == "":
        raise ValidationError(f"{field_name} must be selected", field_name)

    if location not in ui_config.LOCATIONS:
        raise ValidationError(
            f"{field_name} must be one of the available locations",
            field_name
        )


def validate_speed(speed_str: str) -> int:
    """
    Validate and parse a speed value.

    Args:
        speed_str: The speed string to validate.

    Returns:
        The validated speed as an integer.

    Raises:
        ValidationError: If speed is empty, not a number, or out of range.
    """
    if not speed_str or speed_str.strip() == "":
        raise ValidationError("Speed must be entered", "Speed")

    try:
        speed = int(speed_str)
    except ValueError:
        raise ValidationError("Speed must be a valid number", "Speed")

    if speed <= 0:
        raise ValidationError("Speed must be a positive number", "Speed")

    if speed > 200:
        raise ValidationError("Speed must be 200 or less", "Speed")

    return speed


def validate_route(source: str, destination: str) -> None:
    """
    Validate that source and destination form a valid route.

    Args:
        source: The source location.
        destination: The destination location.

    Raises:
        ValidationError: If source and destination are the same.
    """
    if source == destination:
        raise ValidationError(
            "Source and destination cannot be the same",
            "Route"
        )
