from maze import Maze, ACTIONS
from draw import draw_maze, draw_qtable, draw_track

import random
import numpy as np
import matplotlib.pyplot as plt



epoch_num = 30000

class QTable():
    def __init__(self, my_maze, epsilon=0.1, lr=0.1, gamma=0.9):
        self.Q_table = dict()
        self.my_maze = my_maze
        self.epsilon = epsilon
        self.hsize = my_maze.maze.size // 2
        self.lr = lr
        self.gamma = gamma

    # 求Q(s, *)
    def q_value(self, state):
        return np.array([self.Q_table.get((state, action), 0.0) for action in ACTIONS])

    # greedy：a = maxQ(s, *)
    def predict(self, state):
        return ACTIONS[np.argmax(self.q_value(state))]

    # 迭代更新QTable
    def train(self, ax1, ax2):
        win_history = []
        win_rate = 0.0
        for epoch in range(epoch_num):
            self.my_maze.reset((0, 0))
            game_over = False
            state = (0, 0)
            step = 0          
            while not game_over:
                valid_actions = self.my_maze.valid_actions()
                if not valid_actions: break
                # epsilon-greedy
                if np.random.rand() < self.epsilon:
                    action = random.choice(valid_actions)
                else:
                    action = self.predict(state)
                # 实施action
                state_next, reward, game_status = self.my_maze.act(action)
                # 更新Q_table
                if (state, action) not in self.Q_table.keys():
                    self.Q_table[(state, action)] = 0.0
                max_next_Q = max(self.q_value(state_next))
                self.Q_table[(state, action)] += self.lr * (reward + self.gamma * max_next_Q - self.Q_table[(state, action)])

                if game_status == 'win':
                    win_history.append(1)
                    game_over = True
                elif game_status == 'lose':
                    win_history.append(0)
                    game_over = True
                else:
                    game_over = False
                state = state_next
                step += 1
                # 数据可视化
                if (epoch + 1) % 20 == 0:
                    if action == 0:
                        a = 'RIGHT'
                    elif action == 1:
                        a = 'UP'
                    elif action == 2:
                        a = 'LEFT'
                    else:
                        a = 'DOWN'
                    print("epoch: %3d      step: %3d       action: %7s       score: %8.3f       status: %6s" % (epoch+1, step, a, self.my_maze.score, game_status))
                    draw_qtable(ax1, self.my_maze, self.Q_table, step)
                    draw_track(ax2, self.my_maze, step)
                    plt.pause(0.01)
                    
            # 测试是否训练成熟
            if len(win_history) > self.hsize:
                win_rate = sum(win_history[-self.hsize:]) / self.hsize           
            if win_rate > 0.9: 
                self.epsilon = 0.05
            if sum(win_history[-self.hsize:]) == self.hsize and self.play_game((0,0)):
                print(f"Reached 100% win rate at epoch: {epoch + 1}")
                break

    def play_game(self, rat_cell):
        self.my_maze.reset(rat_cell)
        envstate = rat_cell
        while True:
            action = self.predict(envstate)
            envstate, reward, game_status = self.my_maze.act(action)
            if game_status == 'win':
                return True
            elif game_status == 'lose':
                return False
            
            

if __name__=="__main__":
    maze_map = np.array([
        [1, 0, 1, 1, 1,  1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1,  0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1,  0, 1, 1, 1, 1],
        [0, 0, 1, 0, 0,  1, 0, 1, 1, 1],
        [1, 1, 0, 1, 0,  1, 0, 0, 0, 1],

        [1, 1, 0, 1, 0,  1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1,  1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0,  0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1,  1, 1, 0, 1, 1],
    ])
    my_maze = Maze(maze_map=maze_map)
    
    fig1, ax1 = plt.subplots(1, 1, tight_layout=True)
    draw_maze(ax1, my_maze, "Train   step: 0")
    fig2, ax2 = plt.subplots(1, 1, tight_layout=True)
    draw_maze(ax2, my_maze, "Test    step: 0")
    
    model = QTable(my_maze)
    model.train(ax1, ax2)
    plt.show()
    