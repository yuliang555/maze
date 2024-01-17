# <a name="_toc30313"></a><a name="_toc18589"></a>**机器人路径规划**

## <a name="_toc23612"></a><a name="_toc28316"></a>**一、实验任务**

1 设计一个有障碍物的地图，用户可以修改障碍物布局，可以指定起点和终点

2 编程实现Q-learning算法，用于机器人规划最短路径，学习算法参数可以由用户设置

3 使用可视化界面演示Q值变化过程及最短路径探测过程

## <a name="_toc2271"></a>**二、文件描述**

**maze.py：迷宫类**

**draw.py：迷宫可视化**

--draw_maze(ax, my_maze, label)：绘制迷宫

--draw_track(ax, my_maze, step)：绘制智能体运动轨迹

--draw_qtable(ax, my_maze, Q_table, step)：绘制Q-Table变化

**main.py：主程序，求解路径规划**

--q_value(self, state)：求Q(s, *)

--predict(self, state)：贪心策略求a = maxQ(s, *)

--train(self, ax1, ax2)：迭代更新Q-Table

## <a name="_toc25648"></a>**三、运行示例** 
Figure1：Q-Table的变化过程，箭头指向Q值最大的运动方向   
Figure2：智能体的运动轨迹   
<img src='https://github.com/yuliang555/maze/blob/master/images/%E5%9B%BE%E7%89%871.png'>
<img src='https://github.com/yuliang555/maze/blob/master/images/%E5%9B%BE%E7%89%872.png'>
