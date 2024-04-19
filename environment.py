import math
import tsplib95

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""


class Environment:
    def __init__(self, rho):

        self.rho = rho

        # Initialize the environment topology
        problem = tsplib95.load_problem("att48-specs/att48.tsp")
        self.graph = problem.get_graph()
        # print(self.graph)

        # Intialize the pheromone map in the environment
        self.initialize_pheromone_map()
        # for edge in self.graph.edges():
        #     print(edge, self.graph[edge[0]][edge[1]]["pheromone_level"])

    # Intialize the pheromone trails in the environment by this procedure
    # 1. Pick random start vertex
    # 2. Find the nearest neighbor tour length
    # 2. Initial pheormone level => 1 / nearest neighbor tour length
    def initialize_pheromone_map(self):
        # 1. Pick random start vertex from the graph self.graph
        start_vertex = 1

        # 2. Find the nearest neighbor tour length
        num_vertices = self.graph.number_of_nodes()
        visited = [False] * num_vertices
        tour_length = 0
        current_vertex = start_vertex
        tour = [current_vertex]
        visited[current_vertex] = True

        for _ in range(1, num_vertices - 1):
            next_vertex = None
            min_distance = float("inf")
            for vertex in range(1, num_vertices):
                if (
                    not visited[vertex]
                    and self.graph[current_vertex][vertex]["weight"] < min_distance
                ):
                    min_distance = self.graph[current_vertex][vertex]["weight"]
                    next_vertex = vertex
            visited[next_vertex] = True
            tour.append(next_vertex)
            tour_length += min_distance
            current_vertex = next_vertex

        # Return to the start vertex
        tour_length += self.graph[current_vertex][start_vertex]["weight"]

        # 3. Initial pheormone level => 1 / nearest neighbor tour length
        for edge in self.graph.edges():
            self.graph[edge[0]][edge[1]]["pheromone_level"] = 1 / tour_length

        print("Nearest neighbor tour length: ", tour_length)

    # Update the pheromone trails in the environment
    def update_pheromone_map(self):
        pass

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        pass

    # Get the environment topology
    def get_possible_locations(self):
        pass
