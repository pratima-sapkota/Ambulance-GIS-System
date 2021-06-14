"""
Ambulance GIS System - Map Renderer

Handles all matplotlib visualization for the road map and ambulance movement.
"""

from typing import Tuple, Dict, List, Any, Optional
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from matplotlib.lines import Line2D


class MapRenderer:
    """
    Renders the road map and ambulance position using matplotlib.

    Separates visualization concerns from business logic, allowing
    the Ambulance class to focus on pathfinding and movement.

    Attributes:
        road_map: The RoadMap instance containing the graph data.
        current_path_artist: The matplotlib artist for the current path highlight.
        current_position_artist: The matplotlib artist for ambulance position.
    """

    def __init__(self, road_map: Any) -> None:
        """
        Initialize the MapRenderer.

        Args:
            road_map: RoadMap instance containing the road network graph.
        """
        self.road_map = road_map
        self.current_path_artist: Optional[Any] = None
        self.current_position_artist: Optional[List[Any]] = None

    def get_node_positions(self) -> Dict[Tuple[int, int], Tuple[int, int]]:
        """
        Get the positions of all nodes in the graph.

        For this road map, node positions are the same as their coordinate keys.

        Returns:
            Dictionary mapping node coordinates to their display positions.
        """
        positions = dict()
        for node in self.road_map.graph.nodes:
            positions[node] = node
        return positions

    def _get_node_labels(self) -> Dict[Tuple[int, int], List[Any]]:
        """
        Get combined labels (name and congestion) for all nodes.

        Returns:
            Dictionary mapping node coordinates to [name, congestion] lists.
        """
        my_labels = defaultdict(list)
        node_congestion = nx.get_node_attributes(self.road_map.graph, 'traffic_cong')
        node_names = nx.get_node_attributes(self.road_map.graph, 'name')

        for d in (node_names, node_congestion):
            for key, value in d.items():
                my_labels[key].append(value)

        return my_labels

    def _draw_legend(self) -> None:
        """Draw the map legend."""
        legend_elements = [
            Line2D([0], [0], color='b', alpha=0.5, lw=4, label='Best Path'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='r',
                   markersize=12, label='Ambulance Position')
        ]
        plt.legend(handles=legend_elements, loc='upper right')

    def draw_initial_map(self) -> None:
        """
        Draw the initial road map visualization.

        Displays all nodes with their names and traffic congestion levels,
        and all edges representing roads. Sets up matplotlib interactive mode.
        """
        positions = self.get_node_positions()

        plt.clf()

        try:
            plt.get_current_fig_manager().window.state('zoomed')
        except (AttributeError, tk.TclError):
            # Window maximization not supported on all platforms
            pass

        my_labels = self._get_node_labels()

        nx.draw(self.road_map.graph, with_labels=False, pos=positions)
        nx.draw_networkx_labels(
            self.road_map.graph.nodes,
            pos=positions,
            labels=my_labels,
            font_color='black',
            font_size=10
        )

        self._draw_legend()

        plt.ion()
        plt.show()
        plt.pause(0.1)

    def update_ambulance_position(
        self,
        position: Tuple[float, float],
        color: str = 'r'
    ) -> None:
        """
        Update the ambulance position marker on the map.

        Args:
            position: Current (x, y) coordinates of the ambulance.
            color: Color for the marker ('g' for start, 'r' for moving).
        """
        # Hide previous position marker
        if self.current_position_artist:
            for p in self.current_position_artist:
                p.set_visible(False)

        # Draw new position
        self.current_position_artist = plt.plot(
            position[0], position[1],
            marker='o', color=color, markersize=12
        )
        plt.pause(0.1)

    def draw_best_path(
        self,
        path: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> Any:
        """
        Draw the current best path on the map.

        Args:
            path: List of edge tuples representing the path.

        Returns:
            The matplotlib path object that can be removed later.
        """
        positions = self.get_node_positions()

        path_artist = nx.draw_networkx_edges(
            self.road_map.graph,
            pos=positions,
            edgelist=path,
            width=8,
            alpha=0.4,
            edge_color='blue'
        )
        plt.pause(0.1)

        self.current_path_artist = path_artist
        return path_artist

    def clear_current_path(self) -> None:
        """Remove the current path highlight from the map."""
        if self.current_path_artist:
            self.current_path_artist.remove()
            self.current_path_artist = None

    def refresh_map(self) -> None:
        """
        Refresh the map display after traffic congestion updates.

        Clears and redraws the entire map with updated congestion values.
        """
        plt.clf()

        positions = self.get_node_positions()
        my_labels = self._get_node_labels()

        nx.draw(self.road_map.graph, pos=positions)
        nx.draw_networkx_labels(
            self.road_map.graph.nodes,
            pos=positions,
            labels=my_labels,
            font_color='black',
            font_size=10
        )

        self._draw_legend()


# Import for exception handling in draw_initial_map
try:
    import tkinter as tk
except ImportError:
    tk = None
