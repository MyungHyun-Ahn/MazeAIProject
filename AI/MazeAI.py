from __future__ import print_function
import os, sys, time, datetime, json, random
import numpy as np
from keras.models import Sequential
from keras.src.layers.core import Dense, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.src.layers.activation.prelu import PReLU
import matplotlib.pyplot as plt

from Maze.Maze import Maze

maze_class = Maze(10)
maze = np.array(maze_class.maze)

visited_mark = 0.8
player_mark = 0.5
LEFT    = 0
UP      = 1
RIGHT   = 2
DOWN    = 3
epsilon = 0.1

actions_dict = {
    LEFT    : 'left',
    UP      : 'up',
    RIGHT   : 'right',
    DOWN    : 'down',
}

num_actions = len(actions_dict)

class Qmaze(object):
    def __init__(self, maze) -> None:
        self._maze = np.array(maze)
        nrows, ncols = self._maze.shape
        self.player = maze_class.get_enter_pos()
        self.dest = maze_class.get_exit_pos()
        self.free_cells = [(r, c) for r in range(nrows) for c in range(ncols) if self.maze[r, c] == 1.0]
        self.free_cells.remove(self.dest)
        if self.maze[self.dest] == 0.0:
            raise Exception("Invalid maze : destination is blocked!")
        if not self.player in self.free_cells:
            raise Exception("Invalid Player Location")
        self.reset()

    def reset(self):
        self.maze = np.copy(self._maze)
        nrows, ncols = self.maze.shape
        row, col = self.player
        self.maze[row, col] = player_mark
        self.state = (row, col, 'start')
        self.min_reward = -0.5 * self.maze.size
        self.total_reward = 0
        self.visited = set()

    def update_state(self, action):
        nrows, ncols = self.maze.shape
        nrow, ncol, nmode = player_row, player_col, mode = self.state

        if self.maze[player_row, player_col] > 0.0:
            self.visited.add((player_row, player_col))  # mark visited cell

        valid_actions = self.valid_actions()
                
        if not valid_actions:
            nmode = 'blocked'
        elif action in valid_actions:
            nmode = 'valid'
            if action == LEFT:
                ncol -= 1
            elif action == UP:
                nrow -= 1
            if action == RIGHT:
                ncol += 1
            elif action == DOWN:
                nrow += 1
        else:                  # invalid action, no change in player position
            mode = 'invalid'

        # new state
        self.state = (nrow, ncol, nmode)

    def get_reward(self):
        player_row, player_col, mode = self.state
        nrows, ncols = self.maze.shape
        if player_row == nrows-1 and player_col == ncols-1:
            return 1.0
        if mode == 'blocked':
            return self.min_reward - 1
        if (player_row, player_col) in self.visited:
            return -0.25
        if mode == 'invalid':
            return -0.75
        if mode == 'valid':
            return -0.04

    def act(self, action):
        self.update_state(action)
        reward = self.get_reward()
        self.total_reward += reward
        status = self.game_status()
        envstate = self.observe()
        return envstate, reward, status

    def observe(self):
        canvas = self.draw_env()
        envstate = canvas.reshape((1, -1))
        return envstate

    def draw_env(self):
        canvas = np.copy(self.maze)
        nrows, ncols = self.maze.shape
        # clear all visual marks
        for r in range(nrows):
            for c in range(ncols):
                if canvas[r,c] > 0.0:
                    canvas[r,c] = 1.0
        # draw the rat
        row, col, valid = self.state
        canvas[row, col] = player_mark
        return canvas

    def game_status(self):
        if self.total_reward < self.min_reward:
            return 'lose'
        rat_row, rat_col, mode = self.state
        nrows, ncols = self.maze.shape
        if rat_row == nrows-1 and rat_col == ncols-1:
            return 'win'

        return 'not_over'


    def valid_actions(self, cell=None):
        if cell is None:
            row, col, mode = self.state
        else:
            row, col = cell
        actions = [0, 1, 2, 3]
        nrows, ncols = self.maze.shape
        if row == 0:
            actions.remove(1)
        elif row == nrows-1:
            actions.remove(3)

        if col == 0:
            actions.remove(0)
        elif col == ncols-1:
            actions.remove(2)

        if row>0 and self.maze[row-1,col] == 0.0:
            actions.remove(1)
        if row<nrows-1 and self.maze[row+1,col] == 0.0:
            actions.remove(3)

        if col>0 and self.maze[row,col-1] == 0.0:
            actions.remove(0)
        if col<ncols-1 and self.maze[row,col+1] == 0.0:
            actions.remove(2)

        return actions
        