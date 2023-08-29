from time import time
from Player.Player import Player

if __name__ == '__main__':
    player = Player(10)

    print()
    print()
    print('--- 우수법 ---')
    # 오른손만 짚어서 미로를 탈출하는 기법
    start1 = time()
    player.right_hand()
    end1 = time()
    player.draw_path()
    
    print('--- 실행시간 {} ---'.format(end1 - start1))
    print()
    print('--- 우수법 최적화 ---')
    # stack 활용하여 중복 루트 제거
    start2 = time()
    player.right_hand()
    player.right_hand_optimization()
    end2 = time()
    player.draw_path()

    print('--- 실행시간 {} ---'.format(end2 - start2))
    print()
    print('--- BFS ---')
    # 넓이 우선 탐색을 이용하여 목적지까지 가는 루트를 계산
    start3 = time()
    player.bfs()
    end3 = time()
    player.draw_path()

    print('--- 실행시간 {} ---'.format(end3 - start3))
    print()
    print('--- AStar ---')
    # 다익스트라 알고리즘과 비슷한 A* 알고리즘을 활용
    start4 = time()
    player.AStar()
    end4 = time()
    player.draw_path()
    print('--- 실행시간 {} ---'.format(end4 - start4))