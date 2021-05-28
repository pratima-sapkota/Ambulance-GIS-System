"""
Ambulance GIS System - Simulation Module

Handles the simulation environment setup, graph generation from CSV data,
and orchestrates the ambulance navigation simulation.
"""

from Ambulance import Ambulance
from RoadMap import RoadMap
import networkx as nx
import csv
import simpy
import matplotlib.pyplot as plt
from typing import Tuple

from utils import calculate_distance
from config import paths, simulation_config

fig = plt.figure()


def main_function(source: Tuple[int, int], destination: Tuple[int, int], ambulance_speed: int) -> None:
    """
    Main entry point for the ambulance simulation.

    Creates the road network graph from CSV files, initializes the simulation
    environment, and runs the ambulance navigation.

    Args:
        source: Starting coordinates as (x, y) tuple.
        destination: Target coordinates as (x, y) tuple.
        ambulance_speed: Speed of the ambulance in simulation units.
    """
    def generate_graph() -> nx.Graph:
        """
        Generate a NetworkX graph from CSV data files.

        Reads points.csv for nodes (with traffic congestion data) and
        roads.csv for edges (with distance weights).

        Returns:
            A NetworkX Graph representing the road network.
        """
        myGraph = nx.Graph()

        # context manager, so that when we are done reading the file, it is closed
        with open(paths.POINTS_FILE, "r") as f:
            points = csv.reader(f)

            # to skip the first row containing headers
            next(points)

            for row in points:
                myGraph.add_node((int(row[0]), int(row[1])), traffic_cong=int(row[2]), name=row[6])

        with open(paths.ROADS_FILE, "r") as f:
            roads = csv.reader(f)
            next(roads)
            for row in roads:
                p1 = (int(row[1]), int(row[2]))
                p2 = (int(row[3]), int(row[4]))
                distance = calculate_distance(p1, p2)
                myGraph.add_edge(p1, p2, weight=distance)
        return myGraph

    myGraph = generate_graph()

    # main execution code
    env = simpy.rt.RealtimeEnvironment(factor=simulation_config.REALTIME_FACTOR, strict=False)
    my_road = RoadMap(myGraph)
    my_ambulance = Ambulance(env, my_road, ambulance_speed, source, destination)
    my_ambulance.env.process(my_ambulance.drive_to_destination())
    my_ambulance.env.run()
