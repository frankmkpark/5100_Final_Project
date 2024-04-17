from queue import PriorityQueue
from ex_game_state import GameState
import numpy as np

class Solver:
    def __init__(self, initial_state, goal_state, max_iterations=2500):
        self.initial_state = np.ravel(initial_state).tolist()
        self.goal_state = np.ravel(goal_state).tolist()
        self.max_iterations = max_iterations
        self.path = []
        self.summary = ""
        self.queue = PriorityQueue()

    def solve(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        size = int(np.sqrt(len(self.initial_state)))
        visited = set()
        self.queue.put(GameState(self.initial_state, self.goal_state, 0))

        while not self.queue.empty() and len(self.path) <= self.max_iterations:
            current_node = self.queue.get()
            current_state = current_node.get_state()
            state_id = str(current_state)
            
            if state_id in visited:
                continue
            visited.add(state_id)

            # Check if the current state is the goal state
            if current_state == self.goal_state:
                self.trace_path(current_node)
                self.get_summary()
                return self.path

            empty_idx = current_state.index(0)
            x, y = divmod(empty_idx, size)

            # Generate all possible states by moving the empty tile
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    # Swap the empty tile with the adjacent tile
                    swapped_state = self.swap_tiles(current_state, x * size + y, nx * size + ny, size)
                    if str(swapped_state) not in visited:
                        self.queue.put(GameState(swapped_state, self.goal_state, current_node.get_depth() + 1, current_node))

        if len(self.path) > self.max_iterations:
            print("This grid setting is not solvable")

    def swap_tiles(self, state, idx1, idx2, size):
        state = state[:]
        state[idx1], state[idx2] = state[idx2], state[idx1]
        return state

    # Trace the path from the goal state to the initial state
    def trace_path(self, node):
        while node:
            self.path.append(node)
            node = node.get_parent()

    # Get the summary of the solution
    def get_summary(self):
        if self.path:
            steps = self.path[0].get_depth()
            self.summary = f"Required {steps} steps, visited {len(self.path)} nodes."
        else:
            self.summary = "No solution found within the given constraints."
        return self.summary