"""
Ambulance GIS System - Ambulance Module

Defines the Ambulance class which handles ambulance movement simulation
and pathfinding. Visualization is delegated to the MapRenderer.
"""

from typing import Tuple, Dict, List, Any, Generator, Optional
from sympy import symbols, Eq, solve  # for solving equations

from ambulance_gis.utils.geometry import calculate_distance
from ambulance_gis.utils.logger import app_logger
from ambulance_gis.visualization.map_renderer import MapRenderer


class Ambulance:
    """
    Represents an ambulance navigating through a road network.

    The ambulance finds optimal paths based on distance and traffic,
    moves along the road network. Visualization is handled by MapRenderer.

    Attributes:
        speed: Movement speed of the ambulance in simulation units.
        source: Starting position as (x, y) coordinates.
        destination: Target position as (x, y) coordinates.
        position: Current position as (x, y) coordinates.
        env: SimPy simulation environment.
        road_map: RoadMap instance containing the road network graph.
        renderer: MapRenderer for visualization (optional).
        best_path: Current best path to destination.
    """

    def __init__(
        self,
        env: Any,
        road_map: Any,
        speed: int,
        source: Tuple[int, int],
        destination: Tuple[int, int],
        renderer: Optional[MapRenderer] = None
    ) -> None:
        """
        Initialize an Ambulance instance.

        Args:
            env: SimPy simulation environment.
            road_map: RoadMap instance containing the road network.
            speed: Movement speed of the ambulance.
            source: Starting coordinates as (x, y) tuple.
            destination: Target coordinates as (x, y) tuple.
            renderer: Optional MapRenderer for visualization. If None, creates one.
        """
        self.speed = speed
        self.source = source
        self.destination = destination
        self.position = source
        self.env = env
        self.road_map = road_map
        self.renderer = renderer or MapRenderer(road_map)
        self.best_path: Tuple[Tuple[int, int], ...] = tuple()

        # Initialize the map display
        self.renderer.draw_initial_map()

    def get_edge_list_from_path(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Convert the best path to a list of edges.

        Returns:
            List of edge tuples, where each edge is a pair of node coordinates.
        """
        best_path_edge = []
        for i in range(len(self.best_path) - 1):
            temp_edge = (self.best_path[i], self.best_path[i + 1])
            best_path_edge.append(temp_edge)
        return best_path_edge

    def drive_to_destination(self) -> Generator[Any, None, None]:
        """
        Drive the ambulance from source to destination.

        This is a SimPy generator that yields timeout events as the
        ambulance moves along the optimal path, recalculating the
        best route at each node based on current traffic conditions.

        Yields:
            SimPy timeout events representing travel time between positions.
        """
        final_best_path = [self.source]

        while not self.position == self.destination:
            # Calculate best path from current position
            self.best_path = self.road_map.select_best_path(self.position, self.destination)

            # Draw the path
            path_edges = self.get_edge_list_from_path()
            self.renderer.draw_best_path(path_edges)

            next_node = self.best_path[1]
            final_best_path.append(next_node)

            # Set up equations for movement along the edge
            x, y = symbols('x y')
            coeff1 = next_node[1] - self.position[1]
            coeff2 = next_node[0] - self.position[0]
            eq1 = Eq(coeff1 * x - coeff2 * y, coeff1 * self.position[0] - coeff2 * self.position[1])

            # Draw starting position
            self.renderer.update_ambulance_position(self.position, color='g')

            # Move towards next node
            while not self.position == next_node:
                # Hide previous position
                if self.renderer.current_position_artist:
                    for p in self.renderer.current_position_artist:
                        p.set_visible(False)

                dist_from_next_node = calculate_distance(self.position, next_node)

                if dist_from_next_node <= self.speed:
                    # Close enough to reach the node
                    time_to_reach_dest = dist_from_next_node / self.speed
                    yield self.env.timeout(time_to_reach_dest)
                    self.position = next_node
                else:
                    # Move one step towards the node
                    eq2 = Eq((x - self.position[0]) ** 2 + (y - self.position[1]) ** 2, self.speed ** 2)
                    sol = solve((eq1, eq2), (x, y))

                    # Find which solution moves us closer to the next node
                    dist_with_next_node = {}
                    for (x_val, y_val) in sol:
                        x1 = x_val.evalf()
                        y1 = y_val.evalf()
                        dist_with_next_node[(x1, y1)] = calculate_distance((x1, y1), next_node)

                    yield self.env.timeout(1)
                    self.position = min(dist_with_next_node.items(), key=lambda k: k[1])[0]

                # Update position display
                self.renderer.update_ambulance_position(self.position, color='r')

            # Reached the next node - update traffic and refresh map
            self.renderer.clear_current_path()
            self.road_map.update_congestion()
            self.renderer.refresh_map()

        app_logger.info(f"Journey complete. Path taken: {final_best_path}")
