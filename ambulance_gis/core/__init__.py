"""
Core modules for the Ambulance GIS System.

Contains the main business logic components:
- ambulance: Ambulance movement and pathfinding
- road_map: Road network graph management
- simulation: Simulation environment setup
"""

from ambulance_gis.core.ambulance import Ambulance
from ambulance_gis.core.road_map import RoadMap

__all__ = ["Ambulance", "RoadMap"]
