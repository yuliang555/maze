import matplotlib.pyplot as plt
import numpy as np

from maze import RIGHT, UP, LEFT, DOWN, ACTIONS


def draw_maze(ax, my_maze, label):
    nrow, ncol = my_maze.maze.shape
    start = my_maze.start
    aim = my_maze.aim
    size_factor = 7.0 / my_maze.maze.shape[0]
    
    ax.clear()
    ax.set_xticks(np.arange(0.5, nrow+1, step=1))
    ax.set_xticklabels([])
    ax.set_yticks(np.arange(0.5, ncol, step=1))
    ax.set_yticklabels([])
    ax.grid(True)
    
    ax.imshow(1-my_maze.maze, cmap="binary")   
    ax.plot(aim[1], aim[0], color='green', marker='s', markersize=int(20*size_factor))
    ax.text(aim[1], aim[0], "Exit", fontdict={'fontsize': 6}, ha="center", va="center", color="white")
    ax.plot(start[1], start[0], color='blue', marker='s', markersize=int(20*size_factor))
    ax.text(start[1], start[0], "Start", fontdict={'fontsize': 6}, ha="center", va="center", color="white")
    ax.text(0, my_maze.maze.shape[0], label, fontdict={'fontsize': 8}, ha="center", va="center", color="black")
    
    return size_factor


def draw_qtable(ax, my_maze, Q_table, step):
    label = 'Q_Table    step: ' + str(step)
    draw_maze(ax, my_maze, label)
    for cell in my_maze.free_cells:
        if cell != my_maze.aim:
            q = []
            for action in ACTIONS:
                if (cell, action) not in Q_table.keys():
                    q.append(0.0)
                else:
                    q.append(Q_table[(cell, action)])
            a = np.nonzero(q == np.max(q))[0]
            for action in a:
                dx, dy = 0, 0
                if action == LEFT:
                    dx = -0.2
                elif action == RIGHT:
                    dx = 0.2
                elif action == UP:
                    dy = -0.2
                elif action == DOWN:
                    dy = 0.2
                color = (q[action] - -1) / (1 - -1)
                color = max(min(1, color), 0)
                ax.arrow(cell[1], cell[0], dx, dy, color=(1 - color, color, 0), head_width=0.2, head_length=0.1)
    ax.get_figure().canvas.draw()


def draw_track(ax, my_maze, step):
    label = "Track     step: " + str(step)
    size_factor = draw_maze(ax, my_maze, label)

    for i, cell in enumerate(my_maze.visited):
        if i + 1 >= step and step > 0:
            ax.plot(cell[1], cell[0], color='red', marker='H', markersize=int(15*size_factor))
            ax.text(cell[1], cell[0], "Rat", fontdict={'fontsize': 6}, ha="center", va="center", color="white")
            break
        ax.plot(cell[1], cell[0], color='yellow', marker='o', markersize=int(10*size_factor))

    ax.get_figure().canvas.draw()



        