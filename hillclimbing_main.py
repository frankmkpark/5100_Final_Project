
import heapq
import timeit
from sys import argv


class Node(object):

    def __init__(self, game_state, prev_state=None):
        assert len(game_state) == 9
        self.board = game_state[:]
        self.prev = prev_state
        self.step = 0

        if self.prev:
            self.step = self.step + 1



    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        parts = [self._encode_state(0, 2), self._encode_state(3, 5), self._encode_state(6, 8)]
        return sum(part * (31 ** i) for i, part in enumerate(parts))

    def _encode_state(self, start, end):
        return sum(self.state[i] << (3 * (end - i)) for i in range(start, end + 1))

    '''
        #output
        0 1 2
        3 4 5
        6 7 8
    '''

    def __str__(self):
        string_list = [str(i) for i in self.board]
        row_groups = (string_list[:3], string_list[3:6], string_list[6:])
        return "\n".join([" ".join(row) for row in row_groups])

    def manhattan_distance(self):
        distance = 0
        goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for i in range(1, 9):
            current_x, current_y = self.__i2pos(self.board.index(i))
            goal_x, goal_y = self.__i2pos(goal.index(i))
            distance += abs(current_x - goal_x) + abs(current_y - goal_y)
        return distance

    def manhattan_score(self):
        return 0

    def next(self):
        i = self.board.index(0)

        next_moves = (self.move_up(i), self.move_down(i), self.move_left(i), self.move_right(i))
        return [s for s in next_moves if s]

    def move_right(self, i):
        x, y = self.__i2pos(i)
        if y < 2:
            right_state = Node(self.board, self)
            right = self.__pos2i(x, y + 1)
            right_state.__swap(i, right)
            return right_state

    def move_left(self, i):
        x, y = self.__i2pos(i)
        if y > 0:
            left_state = Node(self.board, self)
            left = self.__pos2i(x, y - 1)
            left_state.__swap(i, left)
            return left_state

    def move_up(self, i):
        x, y = self.__i2pos(i)
        if x > 0:
            up_state = Node(self.board, self)
            up = self.__pos2i(x - 1, y)
            up_state.__swap(i, up)
            return up_state

    def move_down(self, i):
        x, y = self.__i2pos(i)
        if x < 2:
            down_state = Node(self.board, self)
            down = self.__pos2i(x + 1, y)
            down_state.__swap(i, down)
            return down_state

    def __swap(self, i, j):
        self.board[j], self.board[i] = self.board[i], self.board[j]

    def __i2pos(self, index):
        return (int(index / 3), index % 3)

    def __pos2i(self, x, y):
        return x * 3 + y

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

class Searcher(object):

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.move = 0

    def print_path(self, state):
        path = []
        while state:
            path.append(state)
            state = state.prev
        path.reverse()
        print("\n-->\n".join([str(state) for state in path]))

        if path:
            print("Total moves:", self.move)




    def hill_climbing(self):
        stack = [self.start]

        while stack:
            state = stack.pop()
            if state == self.goal:
                self.print_path(state)
                print("Find solution")
                break

            h_val = state.manhattan_distance()

            next_state = False
            for s in state.next():
                h_val_next = s.manhattan_distance()
                if h_val_next < h_val:
                    s.prev = state
                    next_state = s
                    h_val = h_val_next
                    stack.append(next_state)
                    self.move += 1
                    break

            if not next_state:
                self.print_path(state)
                print("Cannot find solution")



if __name__ == "__main__":
    script, strategy = argv

    # Experiment
    print("Search for solution\n")
    start = Node([3,1,2,0,4,5,6,7,8])
    # start = Node([3, 1, 2, 0, 4, 5, 6, 7, 8])
    # start = Node([1,4,2,3,0,5,6,7,8])
    # start = Node([2,3,6,0,7,4,5,1,8])
    # start = Node([1, 2, 3, 5, 0, 6, 4, 7, 8]) # solvable
    # start = Node([7,1,2,4,3,0,6,5,8])
    # start = Node([1,4,2,3,0,5,6,7,8])
    # start = Node([1,3,5,4,2,0,7,8,6])
    # start = Node([1,3,2,7,5,0,4,8,6])
    goal = Node([0,1,2,3,4,5,6,7,8])

    search = Searcher(start, goal)

    start_time = timeit.default_timer()
    if strategy == "hc":
        search.hill_climbing()

    else:
        print("Wrong strategy")
    end_time = timeit.default_timer()
    elapsed = end_time - start_time
    print("Search time: %s" % elapsed)

