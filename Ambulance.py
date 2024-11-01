import math
from sympy import symbols, Eq, solve  # for solving equations
import matplotlib.pyplot as plt
import networkx as nx


def find_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


class Ambulance(object):
    def __init__(self, env, road_map, speed, source, destination):
        self.speed = speed
        self.source = source
        self.destination = destination
        self.position = source
        self.env = env
        self.road_map = road_map
        self.draw_road_map()

    # to travel from source node to destination
    def drive_to_destination(self):
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

            point = plt.plot(self.position[0], self.position[1], marker='o', color='g')

            while not self.position == next_node:
                for p in point:
                    p.set_visible(False)

                dist_from_next_node = find_distance(self.position, next_node)
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
                        dist_with_next_node[(x1, y1)] = find_distance((x1, y1), next_node)
                    yield self.env.timeout(1)

                    # the above two equations solve for two co-ordinate pairs,
                    # finding which point moves the ambulance towards next node
                    self.position = min(dist_with_next_node.items(), key=lambda k: k[1])[0]

                point = plt.plot(self.position[0], self.position[1], marker='o', color='g')
                plt.pause(0.1)

            path.remove()

            node_labels = nx.get_node_attributes(self.road_map.graph, 'traffic_cong')
            self.road_map.update_congestion()
            updated_node_labels = nx.get_node_attributes(self.road_map.graph, 'traffic_cong')

            mapping = {}
            for key in set(node_labels.keys()) & set(updated_node_labels.keys()):
                mapping[node_labels[key]] = updated_node_labels[key]
            print(f"mapping:{mapping}")
            # nx.relabel_nodes(self.road_map.graph, mapping)
        print(final_best_path)

    def draw_road_map(self):
        positions = self.get_node_positions()

        nx.draw(self.road_map.graph, with_labels=True, pos=positions)
        node_labels = nx.get_node_attributes(self.road_map.graph, 'traffic_cong')
        nx.draw_networkx_labels(self.road_map.graph.nodes, pos=positions, labels=node_labels, font_color='w')

        plt.ion()
        plt.show()
        plt.pause(0.1)

    def get_node_positions(self):
        positions = dict()
        for node in self.road_map.graph.nodes:
            positions[node] = node

        return positions

    def get_edge_list_from_path(self):
        best_path_edge = list()
        for i in range((len(self.best_path) - 1)):
            temp_edge = (self.best_path[i], self.best_path[i + 1])
            best_path_edge.append(temp_edge)

        return best_path_edge

    def draw_best_path_edge(self):
        best_path_edge = self.get_edge_list_from_path()

        path = nx.draw_networkx_edges(self.road_map.graph, pos=self.get_node_positions(),
                                      edgelist=best_path_edge,
                                      width=10, alpha=0.5, edge_color='r')
        plt.pause(0.1)
        return path

