from time import sleep

import intcode
import pathfinder
from collections import namedtuple
import threading
import itertools

Location = namedtuple('Location', 'x y')

def intersection(row, col):
    if (row-1,col) in scaffolding and (row+1,col) in scaffolding \
            and (row,col-1) in scaffolding and (row,col+1) in scaffolding:
        return row*col
    return None

def go_dir(loc, dir):  # dir = index('^<v>')
    new_location = Location(loc.x if dir == 0 or dir == 2 else loc.x - 1 if dir == 1 else loc.x + 1, \
                            loc.y if dir == 1 or dir == 3 else loc.y - 1 if dir == 0 else loc.y + 1)
    return new_location

def send_input(program, cmds):
    for ix, cmd in enumerate(cmds):
        program.input.put(ord(cmd))
        if ix < len(cmds)-1:
            program.input.put(ord(','))
    program.input.put(10)

if __name__ == '__main__':
    with open("input_day17.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program = intcode.Program(0, program_code)

    program.run()
    scaffolding = dict()
    loc = Location(0, 0)
    while not program.output.empty():
        reading = program.output.get()
        if reading == 10:               # LF
            loc = Location(0, loc.y+1)
        elif reading == 46:             # .
            loc = Location(loc.x+1, loc.y)
        else:
            if reading in map(ord, '^<v>'):
                robot = loc
                robot_dir = list(map(ord, '^<v>')).index(reading)
            scaffolding[loc] = chr(reading)
            loc = Location(loc.x+1, loc.y)

    alignment_numbers = 0
    for row in range(52):
        print(row, ':', end='')
        for col in range(52):
            if (col,row) in scaffolding:
                print(scaffolding[(col, row)], end='')
                if intersection(col,row):
                    alignment_numbers += intersection(col,row)
            else:
                print(' ', end = '')

        print()
    print('Sum of alignment numbers: ', alignment_numbers, ' path length:', len(scaffolding))
    print(f'Robot at {robot}, pointing {robot_dir}')

    # part 2
    # Hand-calculated: L8R10L8R8 L12R8R8 L8R10L8R8 L8R6R6R10L8 L8R6R6R10L8 L8R10L8R8 L12R8R8 L8R6R6R10L8 L12R8R8 L12R8R8
    #                  A: L8R10L8R8 B: L12R8R8 A C: L8R6R6R10L8 C A B C B B

    # Generate path
    path = []
    while True:
        straight_ahead = 0
        while go_dir(robot, robot_dir) in scaffolding:
            robot = go_dir(robot, robot_dir)
            straight_ahead += 1
        if straight_ahead != 0:
            path.append(straight_ahead)
        for turn in range(1,4,2):
            if go_dir(robot, (robot_dir+turn)%4) in scaffolding:
                robot_dir = (robot_dir + turn) % 4
                path.append('FLUR'[turn])
                break
        else:
            break

    print (f'Calculated path: {path}')
    print(f'AsString: {"".join(map(str,path))}')

    substrings = dict()
    for length_A in range(10,0,-1):
        for start_ix in range(0, len(path)-length_A):
            substring = str(path[start_ix:start_ix+length_A])
            if substring in substrings:
                substrings[substring] += 1
            else:
                substrings[substring] = 1
        print(f'Common strings of len {length_A}:', sorted(enumerate, reverse = True))

    program_code[0] = 2
    program = intcode.Program(0, program_code)
    print ('Second run.')
    print (program.print())

    robot_thread = threading.Thread(target=program.run)
    robot_thread.start()

    sleep(0.1)
    while not program.output.empty():
        reading = program.output.get()
        print (f'{reading} {chr(reading)} ', end = '')

    send_input(program, 'ABACCABCBB')
    send_input(program, 'L8R10L8R8')
    send_input(program, 'L12R8R8')
    send_input(program, 'L8R6R6R10L8')
    send_input(program, 'n')

    robot_thread.join()
    print('Getting response')

    while not program.output.empty():
        reading = program.output.get()
        print(f'{chr(reading)}', end='')
#    space_dust = program.output.get()
 #   print (f'Space dust: {space_dust}')

