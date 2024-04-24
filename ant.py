import random
import time
import numpy as np

# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""


class Ant:
    def __init__(self, alpha: float, beta: float):
        self.alpha = alpha
        self.beta = beta
        self.reset()

    # Reset the ant to the initial state after each iteration
    def reset(self):
        self.current_location = random.randint(1, 48)
        self.tour = [self.current_location]
        self.travelled_distance = 0

    # The ant runs to visit all the possible locations of the environment
    def run(self):
        while len(self.tour) < self.environment.graph.number_of_nodes():
            next_location = self.select_path()
            self.travelled_distance += self.get_distance(next_location)
            self.tour.append(next_location)
            self.current_location = next_location

        # Return to the start vertex
        self.tour.append(self.tour[0])
        self.travelled_distance += self.get_distance(self.tour[0])
        self.current_location = self.tour[0]

    # Select the next path based on the random proportional rule of the ACO algorithm
    # 1. Get all possible paths that are reachable and have not been visited
    # 2. Calculate numerator for each path based on the pheromone level and distance, alpha and beta
    # 3. Calculate the denominator (which is the sum of the numerators)
    # 4. Calculate the probability of each path
    # 5. Return the next path based on the highest probability
    def select_path(self):

        # 1. Get all possible paths that are reachable and have not been visited
        possible_locations = self.environment.get_reachable_locations(
            self.current_location
        )

        paths = {
            key: value
            for key, value in possible_locations.items()
            if key not in self.tour
        }

        # 2. Calculate numerator for each path based on the pheromone level and distance, alpha and beta
        for path in paths:
            pheromone_level = paths[path]["pheromone_level"]
            distance = paths[path]["weight"]
            paths[path]["numerator"] = (pheromone_level**self.alpha) * (
                (1 / distance) ** self.beta
            )

        # 3. Calculate the denominator (which is the sum of the numerators)
        denominator = sum([path["numerator"] for path in paths.values()])

        # 4. Calculate the probability of each path
        for path in paths:
            paths[path]["probability"] = paths[path]["numerator"] / denominator

        # 5. Return the next path based on the highest probability
        # store probabilities in 1-D array
        probabilities = [path["probability"] for path in paths.values()]

        # choose the next path based on the probabilities
        return np.random.choice(list(paths.keys()), p=probabilities)

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment

    # Get the pseudo-euclidean distance between current location and the destination vertex
    def get_distance(self, destination_vertex: int):
        return self.environment.get_distance(self.current_location, destination_vertex)
