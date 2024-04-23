import math
import tsplib95
import numpy as np

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""


class Environment:
    def __init__(self, rho):

        self.rho = rho

        # Initialize the environment topology
        self.graph = tsplib95.load_problem("att48-specs/att48.tsp").get_graph()

        # Remove all edges that lead to themselfs (weight == 0)
        for edge in self.graph.edges():
            if self.graph[edge[0]][edge[1]]["weight"] == 0:
                self.graph.remove_edge(edge[0], edge[1])

        # Intialize the pheromone map in the environment
        self.initialize_pheromone_map()

    # Intialize the pheromone trails in the environment by this procedure
    # 1. Pick random start vertex
    # 2. Find the nearest neighbor tour length: nnDistance
    # 3. Initial pheormone level: m / nnDistance, where m = #ants
    def initialize_pheromone_map(self):
        # 1. Pick random start vertex from the graph self.graph
        start_vertex = np.random.randint(1, self.graph.number_of_nodes() + 1)

        # 2. Find the nearest neighbor tour length: nnDistance
        num_vertices = self.graph.number_of_nodes()
        nnDistance = 0
        current_vertex = start_vertex
        nnTour = [current_vertex]

        for _ in range(1, num_vertices):
            next_vertex = None
            next_vertex_distance = np.Inf
            for vertex in range(1, num_vertices + 1):
                if (
                    vertex not in nnTour
                    and self.graph[current_vertex][vertex]["weight"]
                    < next_vertex_distance
                ):
                    next_vertex = vertex
                    next_vertex_distance = self.graph[current_vertex][next_vertex][
                        "weight"
                    ]
            nnTour.append(next_vertex)
            nnDistance += next_vertex_distance
            current_vertex = next_vertex

        # Return to the start vertex
        nnTour.append(start_vertex)
        nnDistance += self.graph[current_vertex][start_vertex]["weight"]

        # print("Nearest neighbor tour: ", nnTour)
        # print("Nearest neighbor tour length: ", nnDistance)

        # 3. Initial pheormone level: m / nnDistance, where m = #ants
        for edge in self.graph.edges():
            self.graph[edge[0]][edge[1]]["pheromone_level"] = 48 / nnDistance

    # Update the pheromone trails in the environment
    # 1. Evaporate the pheromone trails in the environment
    # 2. Deposit pheromone trails in the environment
    def update_pheromone_map(self, ants: list):

        # 1. Evaporate the pheromone trails in the environment
        for edge in self.graph.edges():
            self.graph[edge[0]][edge[1]]["pheromone_level"] *= 1 - self.rho

        # 2. Deposit pheromone trails in the environment
        for ant in ants:
            for i, edge_end in enumerate(ant.tour[1:]):
                self.graph[ant.tour[i]][edge_end]["pheromone_level"] += (
                    1 / ant.travelled_distance
                )

    # Get reachable vertices from the current location
    def get_reachable_locations(self, current_location: int):
        return self.graph[current_location]

    # Get the pseudo-euclidean distance between two vertices
    def get_distance(self, vertex1: int, vertex2: int):
        return self.graph[vertex1][vertex2]["weight"]
