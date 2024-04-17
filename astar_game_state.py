import numpy as np

class GameState:
    def __init__(self, current, target, depth, parent=None):
        self.current = current
        self.target = target
        self.depth = depth
        self.score = depth
        self.parent = parent
        self.compute_fitness()

    def __hash__(self):
        return hash(str(self.current))
    
    def __gt__(self, other):
        return self.score > other.score

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

    def get_state(self):
        return self.current

    def get_score(self):
        return self.score

    def get_depth(self):
        return self.depth

    def get_parent(self):
        return self.parent

    def compute_fitness(self):
        size = int(np.sqrt(len(self.current)))
        for idx, tile in enumerate(self.current):
            if tile != 0:
                target_idx = self.target.index(tile)
                current_i, current_j = divmod(idx, size)
                target_i, target_j = divmod(target_idx, size)
                self.score += self.manhattan_distance(current_i, current_j, target_i, target_j)

    def manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)