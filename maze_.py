import random
import copy
from queue import PriorityQueue
import time


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
        maze = [[1 for _ in range(size * 2 + 1)] for _ in range(size * 2 + 1)]

        visited = []

        def make(cur_room):
            cx, cy = cur_room.get_cur_pos()
            visited.append((cx, cy))
            maze[cy * 2 + 1][cx * 2 + 1] = 0
            while cur_room.dir:
                nx, ny = cur_room.get_next_pos()
                if 0 <= nx < size and 0 <= ny < size:
                    if (nx, ny) not in visited:
                        maze[cy + ny + 1][cx + nx + 1] = 0
                        make(rooms[ny][nx])

        make(rooms[0][0])

        player_pos = self.get_enter_pos()
        exit_pos = self.get_exit_pos()

        maze[player_pos[0]][player_pos[1]] = 2
        maze[exit_pos[0]][exit_pos[1]] = 3

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

class Player:
    dir_list = [0, 1, 2, 3]
    dir_list_count = 4
    INT32_MAX = 2147483647

    def __init__(self, size) -> None:
        self.maze = Maze(size)
        self.maze.draw_maze()
        self.path = []
        self.pathIndex = 0
        self.dir = self.dir_list[0]
        self.pos = self.maze.get_enter_pos()

    def reset(self):
        self.path = []
        self.pathIndex = 0
        self.dir = self.dir_list[0]
        self.pos = self.maze.get_enter_pos()
        self.maze.reset_maze()

    def can_go(self, pos):
        return self.maze.get_tile_type(pos) == 0 or self.maze.get_tile_type(pos) == 3
    
    ''' 우수법 오른손만 짚어서 탈출하는 방법 '''
    def right_hand(self):
        self.reset()
        pos = self.pos
        self.path.clear()
        self.path.append(list(pos))

        dest = self.maze.get_exit_pos()

        front = [[-1, 0], [0, -1], [1, 0], [0, 1]]

        while pos != dest:
            new_dir = (self.dir_list[self.dir] - 1 + self.dir_list_count) % self.dir_list_count
            new_pos1 = [pos[0] + front[new_dir][0], pos[1] + front[new_dir][1]]
            new_pos2 = [pos[0] + front[self.dir][0], pos[1] + front[self.dir][1]]
            
            # print(pos, dest)

            if (self.can_go(new_pos1)):
                self.dir = new_dir
                pos[0] += front[self.dir][0]
                pos[1] += front[self.dir][1]
                self.path.append(list(pos))
            elif(self.can_go(new_pos2)):
                pos[0] += front[self.dir][0]
                pos[1] += front[self.dir][1]
                self.path.append(list(pos))
            else:
                self.dir = (self.dir + 1) % self.dir_list_count

        # print(self.path)

    def right_hand_optimization(self):
        stack = []

        for i in range(len(self.path) - 1):
            if (len(stack) != 0 and stack[-1] == self.path[i + 1]):
                stack.pop()
            else:
                stack.append(self.path[i])
        
        # 목적지 도착
        if (len(stack) != 0):
            stack.append(self.path[-1])

        path = []
        while (len(stack) != 0):
            path.append(stack[-1])
            stack.pop()

        path.reverse()
        self.path = path

    def draw_path(self):
        self.maze.reset_maze()

        for pos in self.path:
            self.maze.maze[pos[0]][pos[1]] = 2
        self.maze.draw_maze()

    ''' 넓이 우선 탐색(BFS)을 이용한 길찾기 '''
    def bfs(self):
        self.reset()

        pos = self.pos

        self.path.clear()
        self.path.append(list(pos))

        dest = self.maze.get_exit_pos()

        front = [[-1, 0], [0, -1], [1, 0], [0, 1]]

        size = self.maze.get_maze_size()
        discovered = [[False for _ in range(size)] for _ in range(size)]
        
        parent = {}

        q = list()
        q.append(pos)
        discovered[pos[0]][pos[1]] = True
        
        hash_pos = "y" + str(pos[0]) + "x" + str(pos[1])

        parent[hash_pos] = pos

        while (len(q) != 0):
            pos = q[0]
            q.pop(0)

            # 방문
            if (pos == dest):
                break

            for dir in range(4):
                next_pos = [pos[0] + front[dir][0], pos[1] + front[dir][1]]

                if (self.can_go(next_pos) == False):
                    continue

                if (discovered[next_pos[0]][next_pos[1]]):
                    continue

                q.append(next_pos)
                discovered[next_pos[0]][next_pos[1]] = True
                next_hash_pos = "y" + str(next_pos[0]) + "x" + str(next_pos[1])
                parent[next_hash_pos] = pos
        
        self.path.clear()

        pos = dest

        while (True):
            self.path.append(pos)

            hash_pos = "y" + str(pos[0]) + "x" + str(pos[1])

            if (pos == parent[hash_pos]):
                break
        
            pos = parent[hash_pos]

        self.path.reverse()
        self.path.append(pos)

    ''' AStar 알고리즘 길찾기 '''
    def AStar(self):
        # 각 경로의 점수를 매겨 길을 찾는 알고리즘
        # F = G + H
        # F : 최종 점수 (작을 수록 좋음, 경로에 따라 달라짐)
        # G : 시작점에서 해당 좌표까지 이동하는데 드는 비용
        # H : 목적지에서 얼마나 가까운지 (고정)
        self.reset()

        start = list(self.pos)
        dest = self.maze.get_exit_pos()

        front = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        cost = [10, 10, 10, 10]

        size = self.maze.get_maze_size()

        # close[y][x] -> 방문여부 체크
        closed = [[False for _ in range(size)] for _ in range(size)]

        # 지금까지 (y, x)에 대한 가장 좋은 비용
        best = [[self.INT32_MAX for _ in range(size)] for _ in range(size)]

        # 부모 추적 용도
        parent = {}

        pq = PriorityQueue()

        # 1) 예약(발견) 시스템 구현 : 우선순위 큐
        # 2) 뒤늦게 더 좋은 경로가 발견될 수 있음 -> 예외처리 필수
        g = 0
        h = 10 * (abs(dest[0] - start[0]) + abs(dest[1] - start[1]))
        pq.put(PQNode(g + h, g, start))
        best[start[0]][start[1]] = g + h
        hash_start = 'y' + str(start[0]) + 'x' + str(start[1])
        parent[hash_start] = start

        while (pq.empty() == False):
            node = pq.get()

            # 동일한 좌표를 여러 경로로 찾아서, 더 빠른 경로로 인해 이미 방문된 경우라면 스킵

            if (closed[node.pos[0]][node.pos[1]]):
                continue

            if (best[node.pos[0]][node.pos[1]] < node.f):
                continue
            
            # 방문처리
            closed[node.pos[0]][node.pos[1]] = True

            # 목적지에 도착했으면 바로 종료
            if (node.pos == dest):
                break

            for dir in range(self.dir_list_count):
                nextPos = [node.pos[0] + front[dir][0], node.pos[1] + front[dir][1]]

                # 갈 수 있는 지역은 맞는지 확인
                if (self.can_go(nextPos) == False):
                    continue

                # 이미 방문한 곳이면 스킵
                if (closed[nextPos[0]][nextPos[1]]):
                    continue
                
                # 비용 계산
                g = node.g + cost[dir]
                h = 10 * (abs(dest[0] - start[0]) + abs(dest[1] - start[1]))

                # 다른 경로에서 더 빠른 길을 찾았으면 스킵
                if (best[nextPos[0]][nextPos[1]] <= g + h):
                    continue

                # 예약 진행
                best[nextPos[0]][nextPos[1]] = g + h
                pq.put(PQNode(g + h, g, nextPos))
                hash_next = 'y' + str(nextPos[0]) + 'x' + str(nextPos[1])
                parent[hash_next] = node.pos

        # 거슬러 올라가기
        pos = dest
        self.path.clear()
        self.pathIndex = 0

        while (True):
            self.path.append(list(pos))
            hash_pos = 'y' + str(pos[0]) + 'x' + str(pos[1])
            if (pos == parent[hash_pos]):
                break

            pos = parent[hash_pos]

        self.path.reverse()

class PQNode:
    def __init__(self, f, g, pos) -> None:
        self.f = f
        self.g = g
        self.pos = pos

    def __lt__(self, other):
        return self.f < other.f
    
    def __gt__(self, other):
        return self.f < other.f






if __name__ == '__main__':
    player = Player(7)

    print()
    print()
    print('--- 우수법 ---')
    start1 = time.time()
    player.right_hand()
    end1 = time.time()
    player.draw_path()
    
    print('--- 실행시간 {} ---'.format(end1 - start1))
    print()
    print('--- 우수법 최적화 ---')

    start2 = time.time()
    player.right_hand()
    player.right_hand_optimization()
    end2 = time.time()
    player.draw_path()

    print('--- 실행시간 {} ---'.format(end2 - start2))
    print()
    print('--- BFS ---')

    start3 = time.time()
    player.bfs()
    end3 = time.time()
    player.draw_path()

    print('--- 실행시간 {} ---'.format(end3 - start3))
    print()
    print('--- AStar ---')
    
    start4 = time.time()
    player.AStar()
    end4 = time.time()
    player.draw_path()
    print('--- 실행시간 {} ---'.format(end4 - start4))