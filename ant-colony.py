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
                if ant.travelled_distance < shortest_distance:
                    shortest_distance = ant.travelled_distance
                    solution = ant.tour

            # 3. After each iteration, update the pheromone level of the environment
            self.environment.update_pheromone_map(self.ants)

            # 4. After each iteration, reset the ant to the initial state
            for ant in self.ants:
                ant.reset()

            # print(
            #     "Iteration: ",
            #     _ + 1,
            #     "/",
            #     self.iterations,
            #     " shortest_distance: ",
            #     shortest_distance,
            #     " solution: ",
            #     solution,
            # )

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    # Recommended values:
    # ant_population = number of vertices
    # iterations = how many times an ant will run through the environment (I try values [1, 5, 20, 100])
    # alpha = 1 (I try values [0.9, 1.0, 1.1])
    # beta = 2 to 5 (I try values between 2.0 to 5.0 in steps of 0.5)
    # rho = 0.5 (I try values [0.4, 0.5, 0.6])
    # Determine the best alpha, beta, and rho values empirically
    best_solution = []
    best_solution_distance = np.Inf
    for iterations in [200]:
        for alpha in [0.5, 0.8, 1.2, 1.5]:
            for beta in [2, 2.5, 3, 3.5, 4, 4.5, 5]:
                for rho in [0.5, 0.6]:
                    print("Testing values: ", alpha, beta, rho)
                    ant_colony = AntColony(48, iterations, alpha, beta, rho)
                    solution, distance = ant_colony.solve()
                    if distance < best_solution_distance:
                        best_solution_distance = distance
                        best_solution = solution
                        print(
                            "New best solution: ",
                            best_solution,
                            " shortest distance: ",
                            best_solution_distance,
                        )

    print(
        "Best solution: ", best_solution, " shortest distance: ", best_solution_distance
    )


if __name__ == "__main__":
    main()
