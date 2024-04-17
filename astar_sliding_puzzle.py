import numpy as np
from solver import Solver
import timeit

def perform_a_star(initial_state, goal_state, max_iterations):
    solver = Solver(initial_state, goal_state, max_iterations)
    path = solver.solve()
    
    # Print the path and the moves made
    if path:
        last_position = (None, None)
        for node in reversed(solver.path):
            current_state = np.array(node.get_state()).reshape(goal_state.shape)
            zero_index = current_state.flatten().tolist().index(0)
            current_i, current_j = divmod(zero_index, goal_state.shape[0])

            if last_position != (None, None):
                direction = {(-1, 0): 'UP', (1, 0): 'DOWN', (0, 1): 'RIGHT', (0, -1): 'LEFT'}
                move_vector = (current_i - last_position[0], current_j - last_position[1])
                move_description = direction.get(move_vector, "Unknown move")
                print(f'Moved {move_description} from {last_position} to ({current_i}, {current_j})')
        
            last_position = (current_i, current_j)

            for row in current_state:
                print(row)
            print()
    else:
        print("No solution found.")

    print(solver.get_summary())

def main():
    N = 3
    max_iterations = 5000
    # Configuration for initial and goal states
    initial_config = '1 4 2 3 0 5 6 7 8'
    goal_config = '0 1 2 3 4 5 6 7 8'

    initial_state = np.array([int(num) for num in initial_config.split()]).reshape(N, N)
    goal_state = np.array([int(num) for num in goal_config.split()]).reshape(N, N)
    
    # Perform A* and measure time elapsed
    start_time = timeit.default_timer()
    perform_a_star(initial_state, goal_state, max_iterations)
    end_time = timeit.default_timer()
    print(f'Time elapsed: {end_time - start_time} seconds')

if __name__ == "__main__":
    main()
