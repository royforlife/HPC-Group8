# An instance of the class LifeGeneration takes in a matrix which represents the current frame of the game
class LifeGeneration:
    def __init__(self, state):
        self.state = state
    # get width of the game matrix
    def width(self):
        return len(self.state[0])
    # get height of the game matrix
    def height(self):
        return len(self.state)
    # check whether a certian cell is alive, wich 1 or True representing alive and vice versa
    def is_alive(self, x, y):
        return self.state[y][x]
    # according to the cell's position, get its neighbor cells
    # there are in total 9 situations to be specified
    def get_neighbors(self, x, y):
        # neighbors are returned as a list of coordinates of cells
        neighbors = []
        if x == 0 and y == 0:
            neighbors.extend([(x + 1, y), (x + 1, y + 1), (x, y + 1)])      # left-top corner
        elif x == self.width() - 1 and y == 0:
            neighbors.extend([(x - 1, y), (x - 1, y + 1), (x, y + 1)])      # right top corner
        elif x == 0 and y == self.height() - 1:
            neighbors.extend([(x, y - 1), (x + 1, y - 1), (x + 1, y)])      # left bottom corner
        elif x == self.width() - 1 and y == self.height() - 1:
            neighbors.extend([(x, y - 1), (x - 1, y - 1), (x - 1, y)])      # right bottom corner
        elif x == 0 and y != 0 and y != self.height() - 1:
            neighbors.extend([(x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1)])  # left edge
        elif x == self.width() - 1 and y != 0 and y != self.height() - 1:
            neighbors.extend([(x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1)])  # right edge
        elif y == 0 and x != 0 and x != self.width() - 1:
            neighbors.extend([(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y)])  # top edge
        elif y == self.height() - 1 and x != 0 and x != self.width() - 1:
            neighbors.extend([(x - 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y)])  # bottom edge
        else:
            neighbors.extend([(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y),   # otherwise (center)
                              (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)])
        return neighbors
    # takes in a list of neighbors, count for alive
    def count_alive(self, neighbors):
        live_counter = 0
        for i in neighbors:
            if self.is_alive(i[0], i[1]):
                live_counter += 1
        return live_counter
    # progress the game for 1 step
    def next_generation(self):
        # the frame after the game progress 1 step: initially an empty matrix with the settled width and height
        new_frame = [[None for i in range(len(self.state[0]))] for j in range(len(self.state))]
        # traverse the matrix
        for y in range(len(self.state)):
            for x in range(len(self.state[0])):
                # for every cell in the matrix, get its neighbors and check for alive neighbors
                neighbors = self.get_neighbors(x, y)
                num_alive = self.count_alive(neighbors)
                # progress the game according to the game rule
                if self.state[y][x]:
                    if num_alive == 2 or num_alive == 3:
                        new_frame[y][x] = True
                    else:
                        new_frame[y][x] = False
                else:
                    if num_alive == 3:
                        new_frame[y][x] = True
                    else:
                        new_frame[y][x] = False
        # return a new LifeGeneration instance with the new_frame
        return LifeGeneration(new_frame)
    # check whether all cells are dead
    def is_all_dead(self):
        flat_matrix = [item for sublist in self.state for item in sublist]
        return True not in flat_matrix

    # return the current matrix
    def board(self):
        return self.state

# used to store game histories for reproducing the game
class LifeHistory:
    # a list stroying LifeGeneration instances
    history = []

    def __init__(self, initial_gen):
        self.history.clear()
        # initial_gen = the initial game setting = the seed
        self.history.append(initial_gen)
    # progress 1 step
    def play_step(self):
        self.history.append(self.history[-1].next_generation())
    # return the current number of iterations
    def nr_generations(self):
        return len(self.history)
    # get the current game frame
    def get_generation(self, i):
        return self.history[i]
    # check whether all cells are dead
    def dies_out(self):
        return self.history[-1].is_all_dead()
    # check whether the iteration enters a period (infinite loop)
    def period(self):
        length = 0
        for i in range(0, len(self.history)):
            for j in range(i + 1, len(self.history)):
                if self.get_generation(i).board() == self.get_generation(j).board():
                    length += j - i
                    return length
        return None
    # give a max_steps, the function will progress the game automatically until reach the max_steps or the terminating criteria
    def play_out(self, max_steps):
        for i in range(max_steps):
            self.play_step()
            if self.dies_out() or self.period() is not None:
                break
    # return all matrics for all game frames
    def all_boards(self):
        res = []
        for i in self.history:
            res.append(i.board())
        return res


if __name__ == "__main__":
    a = LifeGeneration([[False, True, False],
                        [True, False, True],
                        [False, False, True]])
    # print(a.height())
    # print(a.get_neighbors(2, 0))
    print(a.count_alive(a.get_neighbors(1, 1)))
    print(a.next_generation())
    print(a.next_generation().board())

