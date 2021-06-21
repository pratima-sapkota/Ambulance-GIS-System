"""
Ambulance GIS System - Map Renderer

Handles all matplotlib visualization for the road map and ambulance movement.
"""

from typing import Tuple, Dict, List, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PathCollection
import networkx as nx
from collections import defaultdict
from matplotlib.lines import Line2D
import numpy as np


# Color palette for the map (light theme)
COLORS = {
    'background': '#f8f9fa',
    'road': '#adb5bd',
    'road_edge': '#dee2e6',
    'node': '#4a90d9',
    'node_edge': '#2171b5',
    'path': '#e63946',
    'path_glow': '#e63946',
    'ambulance': '#e63946',
    'ambulance_glow': '#ff6b6b',
    'start': '#2d9a4e',
    'text': '#212529',
    'text_shadow': '#adb5bd',
    'legend_bg': '#ffffff',
    'legend_edge': '#dee2e6',
}


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
        self._setup_style()

    def _setup_style(self) -> None:
        """Configure matplotlib style for a modern light theme."""
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams.update({
            'figure.facecolor': COLORS['background'],
            'axes.facecolor': COLORS['background'],
            'axes.edgecolor': COLORS['road'],
            'axes.labelcolor': COLORS['text'],
            'text.color': COLORS['text'],
            'xtick.color': COLORS['text'],
            'ytick.color': COLORS['text'],
            'grid.color': COLORS['road'],
            'grid.alpha': 0.3,
            'font.family': 'sans-serif',
            'font.size': 10,
        })

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
        """Draw a styled map legend."""
        legend_elements = [
            Line2D([0], [0], color=COLORS['path'], alpha=0.8, lw=4,
                   label='Optimal Route', linestyle='-'),
            Line2D([0], [0], marker='o', color='none',
                   markerfacecolor=COLORS['ambulance'], markeredgecolor=COLORS['ambulance_glow'],
                   markersize=12, markeredgewidth=2, label='Ambulance'),
            Line2D([0], [0], marker='o', color='none',
                   markerfacecolor=COLORS['start'], markeredgecolor='white',
                   markersize=10, markeredgewidth=1, label='Start Point'),
        ]
        legend = plt.legend(
            handles=legend_elements,
            loc='upper right',
            facecolor=COLORS['legend_bg'],
            edgecolor=COLORS['legend_edge'],
            framealpha=0.9,
            fontsize=9,
            labelcolor=COLORS['text'],
        )
        legend.get_frame().set_linewidth(1.5)

    def draw_initial_map(self) -> None:
        """
        Draw the initial road map visualization.

        Displays all nodes with their names and traffic congestion levels,
        and all edges representing roads. Sets up matplotlib interactive mode.
        """
        positions = self.get_node_positions()

        plt.clf()
        fig = plt.gcf()
        fig.set_facecolor(COLORS['background'])
        ax = plt.gca()
        ax.set_facecolor(COLORS['background'])

        try:
            plt.get_current_fig_manager().window.state('zoomed')
        except (AttributeError, tk.TclError):
            # Window maximization not supported on all platforms
            pass

        my_labels = self._get_node_labels()

        # Draw edges with styled appearance
        nx.draw_networkx_edges(
            self.road_map.graph,
            pos=positions,
            edge_color=COLORS['road'],
            width=2.5,
            alpha=0.7,
            style='solid',
        )

        # Draw nodes with gradient-like effect (outer glow)
        nx.draw_networkx_nodes(
            self.road_map.graph,
            pos=positions,
            node_color=COLORS['node'],
            node_size=400,
            edgecolors=COLORS['node_edge'],
            linewidths=2,
            alpha=0.9,
        )

        # Draw labels with better styling
        nx.draw_networkx_labels(
            self.road_map.graph,
            pos=positions,
            labels=my_labels,
            font_color=COLORS['text'],
            font_size=8,
            font_weight='bold',
        )

        # Add title
        plt.title(
            'Ambulance GIS - Real-time Navigation',
            fontsize=14,
            fontweight='bold',
            color=COLORS['text'],
            pad=15,
        )

        self._draw_legend()

        # Remove axis clutter
        ax.set_axis_off()

        # Add subtle padding
        ax.margins(0.1)

        plt.ion()
        plt.tight_layout()
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

        # Map color shortcuts to our palette
        marker_color = COLORS['start'] if color == 'g' else COLORS['ambulance']
        glow_color = COLORS['start'] if color == 'g' else COLORS['ambulance_glow']

        # Draw outer glow effect
        glow = plt.plot(
            position[0], position[1],
            marker='o', color=glow_color, markersize=20,
            alpha=0.3, zorder=5
        )

        # Draw main ambulance marker
        main = plt.plot(
            position[0], position[1],
            marker='o', color=marker_color, markersize=14,
            markeredgecolor='white', markeredgewidth=2,
            zorder=6
        )

        # Draw inner highlight
        inner = plt.plot(
            position[0], position[1],
            marker='o', color='white', markersize=5,
            alpha=0.8, zorder=7
        )

        self.current_position_artist = glow + main + inner
        plt.pause(0.1)

    def draw_best_path(
        self,
        path: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> Any:
        """
        Draw the current best path on the map with a glowing effect.

        Args:
            path: List of edge tuples representing the path.

        Returns:
            The matplotlib path object that can be removed later.
        """
        positions = self.get_node_positions()

        # Draw outer glow layer
        glow_artist = nx.draw_networkx_edges(
            self.road_map.graph,
            pos=positions,
            edgelist=path,
            width=14,
            alpha=0.15,
            edge_color=COLORS['path_glow'],
            style='solid',
        )

        # Draw middle glow layer
        mid_glow_artist = nx.draw_networkx_edges(
            self.road_map.graph,
            pos=positions,
            edgelist=path,
            width=10,
            alpha=0.3,
            edge_color=COLORS['path_glow'],
            style='solid',
        )

        # Draw main path
        path_artist = nx.draw_networkx_edges(
            self.road_map.graph,
            pos=positions,
            edgelist=path,
            width=5,
            alpha=0.9,
            edge_color=COLORS['path'],
            style='solid',
        )

        plt.pause(0.1)

        # Store all artists for removal
        self.current_path_artist = (glow_artist, mid_glow_artist, path_artist)
        return path_artist

    def clear_current_path(self) -> None:
        """Remove the current path highlight from the map."""
        if self.current_path_artist:
            # Handle tuple of artists (glow layers + main path)
            if isinstance(self.current_path_artist, tuple):
                for artist in self.current_path_artist:
                    if artist is not None:
                        artist.remove()
            else:
                self.current_path_artist.remove()
            self.current_path_artist = None

    def refresh_map(self) -> None:
        """
        Refresh the map display after traffic congestion updates.

        Clears and redraws the entire map with updated congestion values.
        """
        plt.clf()
        fig = plt.gcf()
        fig.set_facecolor(COLORS['background'])
        ax = plt.gca()
        ax.set_facecolor(COLORS['background'])

        positions = self.get_node_positions()
        my_labels = self._get_node_labels()

        # Draw edges with styled appearance
        nx.draw_networkx_edges(
            self.road_map.graph,
            pos=positions,
            edge_color=COLORS['road'],
            width=2.5,
            alpha=0.7,
            style='solid',
        )

        # Draw nodes with gradient-like effect
        nx.draw_networkx_nodes(
            self.road_map.graph,
            pos=positions,
            node_color=COLORS['node'],
            node_size=400,
            edgecolors=COLORS['node_edge'],
            linewidths=2,
            alpha=0.9,
        )

        # Draw labels
        nx.draw_networkx_labels(
            self.road_map.graph,
            pos=positions,
            labels=my_labels,
            font_color=COLORS['text'],
            font_size=8,
            font_weight='bold',
        )

        # Add title
        plt.title(
            'Ambulance GIS - Real-time Navigation',
            fontsize=14,
            fontweight='bold',
            color=COLORS['text'],
            pad=15,
        )

        self._draw_legend()

        # Remove axis clutter
        ax.set_axis_off()
        ax.margins(0.1)

        plt.tight_layout()


# Import for exception handling in draw_initial_map
try:
    import tkinter as tk
except ImportError:
    tk = None
