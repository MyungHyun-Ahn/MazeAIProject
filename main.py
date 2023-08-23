from time import time
from Player.Player import Player

if __name__ == '__main__':
    player = Player(7)

    print()
    print()
    print('--- 우수법 ---')
    start1 = time()
    player.right_hand()
    end1 = time()
    player.draw_path()
    
    print('--- 실행시간 {} ---'.format(end1 - start1))
    print()
    print('--- 우수법 최적화 ---')

    start2 = time()
    player.right_hand()
    player.right_hand_optimization()
    end2 = time()
    player.draw_path()

    print('--- 실행시간 {} ---'.format(end2 - start2))
    print()
    print('--- BFS ---')

    start3 = time()
    player.bfs()
    end3 = time()
    player.draw_path()

    print('--- 실행시간 {} ---'.format(end3 - start3))
    print()
    print('--- AStar ---')
    
    start4 = time()
    player.AStar()
    end4 = time()
    player.draw_path()
    print('--- 실행시간 {} ---'.format(end4 - start4))