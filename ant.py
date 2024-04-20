
# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.travelled_distance = 0
        self.tour = [initial_location]

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        pass

    # Select the next path based on the random proportional rule of the ACO algorithm
    # 1. Get all possible paths that are reachable and have not been visited
    # 2. Calculate numerator for each path based on the pheromone level and distance, alpha and beta
    # 3. Calculate the denominator (which is the sum of the numerators)
    # 4. Calculate the probability of each path
    # 5. Return the next path based on the highest probability
    def select_path(self):

        print(self.tour)
        # 1. Get all possible paths that are reachable and have not been visited
        all_paths = self.environment.get_possible_locations(self.current_location)
        paths = {key: value for key, value in all_paths.items() if key not in self.tour}

        # 2. Calculate numerator for each path based on the pheromone level and distance, alpha and beta
        for path in paths:
            paths[path]["numerator"] = (paths[path]["pheromone_level"] ** self.alpha) * (1 / paths[path]["weight"] ** self.beta)

        # 3. Calculate the denominator (which is the sum of the numerators)
        denominator = sum([path["numerator"] for path in paths.values()])

        # 4. Calculate the probability of each path
        for path in paths:
            paths[path]["probability"] = paths[path]["numerator"] / denominator

        # 5. Return the next path based on the highest probability
        next_path = max(paths, key=lambda x: paths[x]["probability"])

        # print(next_path)
        # for key, value in paths.items():
        #     print(key, value)
        return next_path

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment

    # Get the pseudo-euclidean distance between current location and the destination vertex
    def get_distance(self, destination_vertex: int):
        return self.environment.get_distance(self.current_location, destination_vertex)
