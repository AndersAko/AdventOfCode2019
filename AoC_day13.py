import threading
from collections import defaultdict
from queue import Queue
import queue
from intcode import Program
from os import system

def draw_board(board, x_size, y_size):
    system('clear')
    score = board[(-1,0)] if (-1,0) in board else 0
    print (f'Score: {score}     Blocks: {sum(1 for t in board if board[t] == 2 )}')
    for y in range(y_size):
        for x in range(x_size):
            if (x,y) not in board or board[(x,y)] == 0:
                tile = ' '
            elif board[(x,y)] == 1:
                tile = '|'
            elif board[(x, y)] == 2:
                tile = '#'
            elif board[(x,y)] == 3:
                tile = '='
            elif board[(x,y)] == 4:
                tile = 'o'
            print (tile, end='')
        print()
    print()

if __name__ == '__main__':
    with open("input_day13.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program_code[0] = 2
    breakout_input = Queue()
    breakout = Program(1, program_code, breakout_input)
    breakout_thread = threading.Thread(target=breakout.run)

    breakout_thread.start()
    board = dict()
    while breakout_thread.is_alive():
        try:
            x = breakout.output.get(0.1)
            y = breakout.output.get()
            tile = breakout.output.get()
            print (f'({x},{y}): {tile}')
        except queue.Empty:
            break
        board[(x, y)] = tile
        draw_board(board, 70, 30)


    # wait for finish
    breakout_thread.join()

    while not breakout.output.empty():
        x = breakout.output.get()
        y = breakout.output.get()
        tile = breakout.output.get()
        board[(x, y)] = tile
        draw_board(board, 70, 30)
        

    num_blocks = 0
    for tile in board:
        print (tile)
        if board[tile] == 2:
            num_blocks+=1

    alt_num = sum(1 for t in board if board[t] == 2 )
    print (f"Total of {num_blocks} blocks on screen")