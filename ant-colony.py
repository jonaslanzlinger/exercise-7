import numpy as np

from environment import Environment
from ant import Ant

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""


class AntColony:
    def __init__(
        self,
        ant_population: int,
        iterations: int,
        alpha: float,
        beta: float,
        rho: float,
    ):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho)

        # Initilize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(1, ant_population + 1):

            # Initialize an ant in the environment on the vertex i % num_of_vertices
            ant = Ant(self.alpha, self.beta)

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)

            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem
    # 1. For each iteration, run all the ants to visit all the possible locations of the environment
    # 2. After each iteration, update the list of solutions and the shortest distance
    # 3. After each iteration, update the pheromone level of the environment
    # 4. After each iteration, reset the ant to the initial state
    def solve(self):

        # The solution will be a list of the visited cities
        solution = []

        # Initially, the shortest distance is set to infinite
        shortest_distance = np.inf

        # 1. For each iteration, run all the ants to visit all the possible locations of the environment
        for _ in range(self.iterations):

            for ant in self.ants:
                ant.run()
                # 2. After each iteration, update the list of solutions and the shortest distance (for each ant)
                # FOR MOPRE VERBOSE OUTPUT
                # print("Ant: distance: ", ant.travelled_distance)
                if ant.travelled_distance < shortest_distance:
                    shortest_distance = ant.travelled_distance
                    solution = ant.tour

            # 3. After each iteration, update the pheromone level of the environment
            self.environment.update_pheromone_map(self.ants)

            # 4. After each iteration, reset the ant to the initial state
            for ant in self.ants:
                ant.reset()

            # FOR MORE VERBOSE OUTPUT
            # print("Iteration: ", _, " shortest distance: ", shortest_distance)

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    # Recommended values:
    # ant_population = number of vertices
    # iterations = how many times an ant will run through the environment
    # alpha = 1.0
    # beta = 2 to 5
    # rho = 0.5
    # Determine the best alpha, beta, and rho values empirically

    # Here, I am testing the best alpha, beta, and rho values empirically
    # The best configuration will be selected based on the shortest distance
    best_solution = []
    best_solution_distance = np.Inf
    attempts = 10
    iterations = 25
    for alpha in [0.75, 1.00, 1.25]:
        for beta in [2, 2.5, 3, 3.5, 4, 4.5, 5]:
            for rho in [0.4, 0.5, 0.6]:
                print(f"Testing configuration: {alpha}, {beta}, {rho}")
                total_attempts_distance = 0
                for _ in range(attempts):
                    ant_colony = AntColony(48, iterations, alpha, beta, rho)
                    solution, distance = ant_colony.solve()
                    if distance < best_solution_distance:
                        best_solution_distance = distance
                        best_solution = solution
                        best_alpha = alpha
                        best_beta = beta
                        best_rho = rho
                    total_attempts_distance += distance
                print(
                    f"Configuration: {alpha}, {beta}, {rho} - Average distance: {total_attempts_distance / attempts}"
                )

    print(
        f"Best solution: {best_alpha}, {best_beta}, {best_rho} - {best_solution} - Shortest distance: {best_solution_distance}"
    )


if __name__ == "__main__":
    main()
