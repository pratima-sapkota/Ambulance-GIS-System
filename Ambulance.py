"""
Ambulance GIS System - Ambulance Module

Defines the Ambulance class which handles ambulance movement simulation,
pathfinding, and visualization of the ambulance on the road map.
"""

from typing import Tuple, Dict, List, Any, Generator
from sympy import symbols, Eq, solve  # for solving equations
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from matplotlib.lines import Line2D

from utils import calculate_distance
from logger import app_logger


class Ambulance:
    """
    Represents an ambulance navigating through a road network.

    The ambulance finds optimal paths based on distance and traffic,
    moves along the road network, and visualizes its progress.

    Attributes:
        speed: Movement speed of the ambulance in simulation units.
        source: Starting position as (x, y) coordinates.
        destination: Target position as (x, y) coordinates.
        position: Current position as (x, y) coordinates.
        env: SimPy simulation environment.
        road_map: RoadMap instance containing the road network graph.
        best_path: Current best path to destination.
    """

    def __init__(self, env: Any, road_map: Any, speed: int,
                 source: Tuple[int, int], destination: Tuple[int, int]) -> None:
        """
        Initialize an Ambulance instance.

        Args:
            env: SimPy simulation environment.
            road_map: RoadMap instance containing the road network.
            speed: Movement speed of the ambulance.
            source: Starting coordinates as (x, y) tuple.
            destination: Target coordinates as (x, y) tuple.
        """
        self.speed = speed
        self.source = source
        self.destination = destination
        self.position = source
        self.env = env
        self.road_map = road_map
        self.draw_road_map()

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
            self.best_path = self.road_map.select_best_path(self.position, self.destination)
            path = self.draw_best_path_edge()

            next_node = self.best_path[1]
            final_best_path.append(next_node)

            x, y = symbols('x y')
            coeff1 = next_node[1] - self.position[1]
            coeff2 = next_node[0] - self.position[0]
            eq1 = Eq(coeff1 * x - coeff2 * y, coeff1 * self.position[0] - coeff2 * self.position[1])

            point = plt.plot(self.position[0], self.position[1], marker='o', color='g',markersize=12)

            while not self.position == next_node:
                for p in point:
                    p.set_visible(False)

                dist_from_next_node = calculate_distance(self.position, next_node)
                if dist_from_next_node <= self.speed:
                    time_to_reach_dest = dist_from_next_node / self.speed

                    # hold time to reach next node from current position
                    yield self.env.timeout(time_to_reach_dest)
                    self.position = next_node

                else:
                    eq2 = Eq((x - self.position[0]) ** 2 + (y - self.position[1]) ** 2, self.speed ** 2)
                    sol = solve((eq1, eq2), (x, y))
                    dist_with_next_node = {}
                    for (x_val, y_val) in sol:
                        # x, y have already been used as symbols above!
                        x1 = x_val.evalf()
                        y1 = y_val.evalf()
                        dist_with_next_node[(x1, y1)] = calculate_distance((x1, y1), next_node)
                    yield self.env.timeout(1)

                    # the above two equations solve for two co-ordinate pairs,
                    # finding which point moves the ambulance towards next node
                    self.position = min(dist_with_next_node.items(), key=lambda k: k[1])[0]

                point = plt.plot(self.position[0], self.position[1], marker='o', color='r',markersize=12)
                plt.pause(0.1)

            path.remove()

            plt.clf()
            self.road_map.update_congestion()
            my_labels = defaultdict(list)
            updated_node_labels = nx.get_node_attributes(self.road_map.graph, 'traffic_cong')
            node_names=nx.get_node_attributes(self.road_map.graph,'name')

            for d in (node_names,updated_node_labels): # you can list as many input dicts as you want here
                for key, value in d.items():
                    my_labels[key].append(value)
            nx.draw(self.road_map.graph, pos=self.get_node_positions())
            nx.draw_networkx_labels(self.road_map.graph.nodes, pos=self.get_node_positions(),
                                    labels=my_labels, font_color='black', font_size=10)

            legend_elements = [Line2D([0], [0], color='b',alpha=0.5, lw=4, label='Best Path'),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='r', markersize=12,label='Ambuance Position')]
            plt.legend(handles=legend_elements, loc='upper right')
        app_logger.info(f"Journey complete. Path taken: {final_best_path}")

    def draw_road_map(self) -> None:
        """
        Draw the initial road map visualization.

        Displays all nodes with their names and traffic congestion levels,
        and all edges representing roads. Sets up the matplotlib interactive mode.
        """
        positions = self.get_node_positions()

        plt.clf()

        plt.get_current_fig_manager().window.state('zoomed')

        my_labels = defaultdict(list)
        node_congestion = nx.get_node_attributes(self.road_map.graph, 'traffic_cong')
        node_names = nx.get_node_attributes(self.road_map.graph, 'name')

        for d in (node_names, node_congestion): # you can list as many input dicts as you want here
            for key, value in d.items():
                my_labels[key].append(value)
        nx.draw(self.road_map.graph, with_labels=False, pos=positions)
        nx.draw_networkx_labels(self.road_map.graph.nodes, pos=positions,
                                labels=my_labels, font_color='black', font_size=10)

        legend_elements = [Line2D([0], [0], color='b',alpha=0.5, lw=4, label='Best Path'),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='r', markersize=12, label='Ambulance Position')]
        plt.legend(handles=legend_elements, loc='upper right')

        plt.ion()
        plt.show()
        plt.pause(0.1)

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

    def get_edge_list_from_path(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Convert the best path to a list of edges.

        Returns:
            List of edge tuples, where each edge is a pair of node coordinates.
        """
        best_path_edge = list()
        for i in range((len(self.best_path) - 1)):
            temp_edge = (self.best_path[i], self.best_path[i + 1])
            best_path_edge.append(temp_edge)

        return best_path_edge

    def draw_best_path_edge(self) -> Any:
        """
        Draw the current best path on the map.

        Highlights the optimal route with a thick blue line.

        Returns:
            The matplotlib path object that can be removed later.
        """
        best_path_edge = self.get_edge_list_from_path()

        path = nx.draw_networkx_edges(self.road_map.graph, pos=self.get_node_positions(),
                                      edgelist=best_path_edge,
                                      width=8, alpha=0.4, edge_color='blue')
        plt.pause(0.1)
        return path
