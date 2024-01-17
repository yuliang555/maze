import numpy as np


# 定义动作集
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
ACTIONS = [RIGHT, UP, LEFT, DOWN]

# 定义奖励
REWARD = {"move":-0.05, "finish":1.0, "wall":-0.85, "bound":-0.85, "repeat":-0.3, "dead":-2}

# 迷宫类
class Maze(object):
    def __init__(self, maze_map=None):
        # maze_map: 0代表墙，1代表空格子
        self.maze = np.array(maze_map, dtype=int)
        self.start = (0, 0)
        self.aim = (self.maze.shape[0] - 1, self.maze.shape[1] - 1)
        self.free_cells = [(i, j) for i in range(self.maze.shape[0]) for j in range(self.maze.shape[1]) if self.maze[i, j] == 1]
        self.rat = (0, 0)
        self.score = 0
        self.min_reward = -0.5 * self.maze.shape[0] * self.maze.shape[1]
        self.visited = []
        self.reset()

    def reset(self, rat=(0, 0)):
        self.rat = rat
        self.score = 0
        self.visited = []

    def act(self, action):
        rat_i, rat_j = self.rat
        next_i, next_j = self.move(rat_i, rat_j, action)
        nrow, ncol = self.maze.shape
        if next_i >= nrow or next_j >= ncol or next_i < 0 or next_j < 0:
            award = REWARD['bound']
            next_i = rat_i
            next_j = rat_j
            self.visited.append((next_i, next_j))
            game_status = "blocked"
        elif self.maze[next_i, next_j] == 0:
            award = REWARD['wall']
            next_i = rat_i
            next_j = rat_j
            self.visited.append((next_i, next_j))
            game_status = "blocked"
        elif next_i == self.aim[0] and next_j == self.aim[1]:
            award = REWARD['finish']
            game_status = "win"
        elif (next_i, next_j) in self.visited:
            award = REWARD['repeat']
            self.visited.append((next_i, next_j))
            game_status = "normal"
        else:
            award = REWARD['move']
            self.visited.append((next_i, next_j))
            game_status = "normal"
        self.score += award
        self.rat = (next_i, next_j)
        if self.score < self.min_reward:
            game_status = "lose"
        return self.rat, award, game_status

    def move(self, i, j, action):
        if action == UP:
            next_i = i - 1
            next_j = j
        elif action == RIGHT:
            next_i = i
            next_j = j + 1
        elif action == LEFT:
            next_i = i
            next_j = j - 1
        elif action == DOWN:
            next_i = i + 1
            next_j = j
        return next_i, next_j

    def valid_actions(self, cell=None):
        if cell is None:
            row, col = self.rat
        else:
            row, col = cell
        actions = [RIGHT, UP, LEFT, DOWN]
        nrow, ncol = self.maze.shape
        if row == 0:
            actions.remove(UP)
        elif row == nrow - 1:
            actions.remove(DOWN)
        if col == 0:
            actions.remove(LEFT)
        elif col == ncol - 1:
            actions.remove(RIGHT)
        if row > 0 and self.maze[row-1, col] == 0:
            actions.remove(UP)
        if row < nrow - 1 and self.maze[row+1, col] == 0:
            actions.remove(DOWN)
        if col > 0 and self.maze[row, col-1] == 0:
            actions.remove(LEFT)
        if col < ncol - 1 and self.maze[row, col+1] == 0:
            actions.remove(RIGHT)
        return actions
    
    