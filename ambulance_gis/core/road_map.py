"""
Ambulance GIS System - RoadMap Module

Defines the RoadMap class which manages the road network graph,
handles traffic congestion updates, and implements pathfinding algorithms.
"""

import networkx as nx
import random
from typing import Dict, List, Tuple, Optional

from config import simulation_config
from ambulance_gis.utils.logger import app_logger


class RoadMap:
    """
    Represents a road network with traffic congestion data.

    Manages the underlying graph structure, updates traffic conditions,
    and provides methods to find optimal paths based on distance and traffic.

    Attributes:
        graph: NetworkX Graph containing nodes (intersections) and edges (roads).
    """

    def __init__(self, graph: nx.Graph) -> None:
        """
        Initialize a RoadMap with the given graph.

        Args:
            graph: NetworkX Graph representing the road network.
        """
        self.graph = graph

    def update_congestion(self) -> None:
        """
        Update traffic congestion values for all nodes.

        Simulates changing traffic conditions by assigning random
        congestion values (0-100) to each node.
        """
        for node in self.graph.nodes.data():
            node[1]['traffic_cong'] = random.randint(0, 100)

    def find_path_cost(self, path: Tuple[Tuple[int, int], ...]) -> float:
        """
        Calculate the total distance cost of a path.

        Args:
            path: Tuple of node coordinates representing the path.

        Returns:
            Sum of edge weights (distances) along the path.
        """
        path_cost = 0
        for i in range(len(path) - 1):
            path_cost += (self.graph.edges[path[i], path[i + 1]])[
                'weight']  # graph.edges[path[i], path[i+1]] returns a dictionary

        return path_cost

    def find_path_traffic(self, path: Tuple[Tuple[int, int], ...]) -> int:
        """
        Calculate the total traffic congestion along a path.

        Args:
            path: Tuple of node coordinates representing the path.

        Returns:
            Sum of traffic congestion values at each node (except destination).
        """
        path_traffic = 0
        for i in range(len(path) - 1):
            path_traffic += self.graph.nodes[path[i]]['traffic_cong']
        return path_traffic

    def find_cost_of_all_path(self, source: Tuple[int, int],
                               destiny: Tuple[int, int]) -> Dict[Tuple[Tuple[int, int], ...], List[float]]:
        """
        Find all paths and their costs between source and destination.

        Args:
            source: Starting node coordinates.
            destiny: Destination node coordinates.

        Returns:
            Dictionary mapping each path (as tuple) to [distance_cost, traffic_cost].
        """
        path_costs = {}
        if nx.has_path(self.graph, source, destiny):

            # possible path is a generator object
            possible_path = nx.all_simple_paths(self.graph, source, destiny)
            path_costs = {}
            for path in possible_path:
                path_costs[tuple(path)] = [self.find_path_cost(path),
                                           self.find_path_traffic(path)]

        else:
            app_logger.warning(f"No path exists between {source} and {destiny}")
        return path_costs

    def select_best_path(self, source: Tuple[int, int],
                          destiny: Tuple[int, int]) -> Tuple[Tuple[int, int], ...]:
        """
        Select the optimal path based on distance and traffic.

        Calculates a weighted score for each path combining normalized
        distance cost and traffic congestion, then returns the path
        with the lowest total cost.

        Args:
            source: Starting node coordinates.
            destiny: Destination node coordinates.

        Returns:
            The optimal path as a tuple of node coordinates, or empty tuple if no path exists.
        """
        path_with_cost_traffic = self.find_cost_of_all_path(source, destiny)

        if len(path_with_cost_traffic):
            max_path_cost = max(path_with_cost_traffic.values(), key=lambda v: v[0])[0]

            for path, cost_traffic in path_with_cost_traffic.items():
                # normalizing path cost
                normalized_path_cost = (cost_traffic[0] / max_path_cost) * 100
                total_cost = (simulation_config.PATH_COST_WEIGHT * normalized_path_cost +
                             cost_traffic[1] * simulation_config.TRAFFIC_WEIGHT)
                cost_traffic.append(total_cost)

            # min function only returns a single value even if multiple min exists. So, no handling is done.
            min_tot_cost_path = min(path_with_cost_traffic.items(), key=lambda x: x[1][2])
            return min_tot_cost_path[0]
        else:
            app_logger.warning(f"No path exists between {source} and {destiny}")
            return tuple()
