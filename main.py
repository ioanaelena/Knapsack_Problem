import random
import time


def read_input(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            nr_object = lines[0]
            values = []
            weights = []
            for line in lines[1:-1]:
                parts = line.split()
                values.append(int(parts[1]))
                weights.append(int(parts[2]))
            knapsack_weight = int(lines[-1])
        return nr_object, values, weights, knapsack_weight
    except FileNotFoundError:
        print("File not found.")
        return None


def calculate_fitness_or_weights(solution, used_list):
    return sum(solution[i] * used_list[i] for i in range(len(used_list)))


def generate_random_solution(length):
    return [random.randint(0, 1) for _ in range(length)]


def is_valid_solution(solution, weights, capacity):
    return sum(solution[i] * weights[i] for i in range(len(weights))) <= capacity


def find_best_solution(solutions, values, weights, capacity):
    valid_solutions = [(sol, calculate_fitness_or_weights(sol, values)) for sol in solutions
                       if is_valid_solution(sol, weights, capacity)]
    return max(valid_solutions, key=lambda x: x[1], default=(None, -1))


def random_search(weights, values, capacity, num_iterations):
    solutions = [generate_random_solution(len(weights)) for _ in range(num_iterations)]
    return find_best_solution(solutions, values, weights, capacity)


def flip_switch(solution, position):
    new_solution = solution[:]
    new_solution[position] = 1 - new_solution[position]
    return new_solution


def steepest_ascent_hill_climbing_alg(weights, values, capacity, num_iterations):
    best_sol = []
    best_fit = -1
    while num_iterations >= 0:
        while True:
            random_solution = generate_random_solution(len(weights))
            if calculate_fitness_or_weights(random_solution, weights) <= capacity:
                initial_solution = random_solution
                initial_fitness = calculate_fitness_or_weights(initial_solution, values)
                break
        while True:
            neighbor_fitness = initial_fitness
            best_neighbor = []
            find = False
            for i in range(len(initial_solution)):
                new_state = flip_switch(initial_solution, i)
                if calculate_fitness_or_weights(new_state, weights) <= capacity \
                        and calculate_fitness_or_weights(new_state, values) > neighbor_fitness:
                    best_neighbor = new_state
                    neighbor_fitness = calculate_fitness_or_weights(new_state, values)
                    find = True
            if find is False:
                num_iterations -= 1
                if initial_fitness > best_fit:
                    best_fit = initial_fitness
                    best_sol = initial_solution
                break
            else:
                initial_solution = best_neighbor
                initial_fitness = neighbor_fitness
    return best_sol, best_fit


def run_experiment(values, weights, knapsack_weight, num_iterations, num_runs):
    results = {"Random_search": [], "Sahc": []}
    for _ in range(num_runs):
        start_time = time.time()
        best_solution, best_fitness = random_search(weights, values, knapsack_weight, num_iterations)
        results["Random_search"].append((best_solution, best_fitness, time.time() - start_time))

        start_time = time.time()
        sahc_solution, sahc_fitness = steepest_ascent_hill_climbing_alg(weights, values, knapsack_weight,
                                                                        num_iterations)
        results["Sahc"].append((sahc_solution, sahc_fitness, time.time() - start_time))

    return results


def print_results(results):
    for key in results:
        print(f"{key} Results:")
        for i, (solution, fitness, exec_time) in enumerate(results[key], 1):
            print(f"Run {i}: Best solution - {solution}, Maximum knapsack value - {fitness},"
                  f" Execution time - {exec_time:.4f} seconds")
        best_fitness = max(results[key], key=lambda x: x[1])[1]
        avg_fitness = sum(x[1] for x in results[key]) / len(results[key])
        avg_time = sum(x[2] for x in results[key]) / len(results[key])
        print(f"Best value: {best_fitness}\nAverage value: {avg_fitness}\nAverage execution time:"
              f" {avg_time:.4f} seconds\n")


def main():
    file_path = input("Enter the path to the input file or leave it empty to use test data: ")
    if file_path:
        input_data = read_input(file_path)
        if input_data is None:
            return
        nr_object, values, weights, knapsack_weight = input_data
    else:
        values, weights, knapsack_weight = [10, 20, 30, 40, 50], [1, 2, 3, 4, 5], 10

    num_iterations = int(input("Enter the number of iterations you want to use for algorithms: "))
    num_runs = 10
    results = run_experiment(values, weights, knapsack_weight, num_iterations, num_runs)
    print_results(results)


if __name__ == "__main__":
    main()

