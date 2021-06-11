"""
Ambulance GIS System - Configuration

Centralized configuration for file paths, simulation settings, and UI parameters.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Paths:
    """File path configuration."""
    DATA_DIR: str = "data"
    POINTS_FILE: str = "data/points.csv"
    ROADS_FILE: str = "data/roads.csv"


@dataclass(frozen=True)
class SimulationConfig:
    """Simulation parameters."""
    REALTIME_FACTOR: float = 0.1
    PATH_COST_WEIGHT: float = 0.5
    TRAFFIC_WEIGHT: float = 2.0


@dataclass(frozen=True)
class UIConfig:
    """User interface configuration."""
    WINDOW_TITLE: str = "Ambulance GIS System"
    WINDOW_SIZE: str = "400x500+10+10"
    BACKGROUND_COLOR: str = "light blue"
    LOCATIONS: Tuple[str, ...] = (
        "Pulchowk",
        "Baneswor",
        "Thapathali",
        "Maitighar",
        "Gwarko",
        "Patan",
        "RNAC",
        "Balaju",
        "Kapan",
        "Chabel",
    )


# Default configuration instances
paths = Paths()
simulation_config = SimulationConfig()
ui_config = UIConfig()
