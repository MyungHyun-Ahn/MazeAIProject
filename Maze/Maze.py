import random
import copy

# Tiletype
# 0 : empty
# 1 : WALL
# 2 : Player
# 3 : Exit

# 색깔 지정 방법
# '\033[코드m'

tiles = [0, 1, 2, 3]
colors = ['32', '31', '33', '34']

class Room:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.dir = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random.shuffle(self.dir)
    
    def get_cur_pos(self):
        return self.x, self.y
    
    def get_next_pos(self):
        return self.dir.pop()


''' Recursive Backtracking 알고리즘 기반 미로 생성 '''
class Maze:
    def __init__(self, size) -> None:
        self.maze_size = size * 2 + 1
        self.maze = self.make_maze(size)
        self.maze_back = copy.deepcopy(self.maze)

    def get_maze(self):
        return self.maze
    
    def get_enter_pos(self):
        return [1, 1]
    
    def get_exit_pos(self):
        return [self.maze_size - 2, self.maze_size - 2]
    
    def get_tile_type(self, pos):
        return self.maze[pos[0]][pos[1]]
    
    def get_maze_size(self):
        return self.maze_size

    def make_maze(self, size):
        rooms = [[Room(x, y) for x in range(size)] for y in range(size)]
        maze = [[0.0 for _ in range(size * 2 + 1)] for _ in range(size * 2 + 1)]

        visited = []

        def make(cur_room):
            cx, cy = cur_room.get_cur_pos()
            visited.append((cx, cy))
            maze[cy * 2 + 1][cx * 2 + 1] = 1.0
            while cur_room.dir:
                nx, ny = cur_room.get_next_pos()
                if 0 <= nx < size and 0 <= ny < size:
                    if (nx, ny) not in visited:
                        maze[cy + ny + 1][cx + nx + 1] = 1.0
                        make(rooms[ny][nx])

        make(rooms[0][0])

        player_pos = self.get_enter_pos()
        exit_pos = self.get_exit_pos()

        # maze[player_pos[0]][player_pos[1]] = 2
        # maze[exit_pos[0]][exit_pos[1]] = 3

        return maze
    
    def draw_maze(self):
        for y in self.maze:
            for x in y:
                if x == 1:
                    print('\033[' + colors[1] + 'm■', end=' ')
                elif x == 0:
                    print('\033[' + colors[0] + 'm■', end=' ')
                elif x == 2:
                    print('\033[' + colors[2] + 'm■', end=' ')
                elif x == 3:
                    print('\033[' + colors[3] + 'm■', end=' ')
            print()

    def reset_maze(self):
        self.maze = copy.deepcopy(self.maze_back)