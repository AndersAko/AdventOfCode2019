import intcode
import pathfinder
from collections import namedtuple

Location = namedtuple('Location', 'x y')

def intersection(row, col):
    if (row-1,col) in scaffolding and (row+1,col) in scaffolding \
            and (row,col-1) in scaffolding and (row,col+1) in scaffolding:
        return row*col
    return None

if __name__ == '__main__':
    with open("input_day17.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program = intcode.Program(0, program_code)

    program.run()
    scaffolding = dict()
    loc = Location(0, 0)
    while not program.output.empty():
        reading = program.output.get()
        if reading == 10:
            loc = Location(0, loc.y+1)
        elif reading == 46:
            loc = Location(loc.x+1, loc.y)
        elif reading == 35:
            scaffolding[loc] = '#'
            loc = Location(loc.x+1, loc.y)
        else:
            scaffolding[loc] = chr(reading)
            loc = Location(loc.x+1, loc.y)

    alignment_numbers = 0
    for row in range(52):
        for col in range(52):
            if (row,col) in scaffolding:
                print(scaffolding[(row,col)], end='')
                if intersection(row,col):
                    alignment_numbers += intersection(row,col)
            else:
                print(' ', end = '')

        print()

    print ('Sum of alignment numbers: ', alignment_numbers)
#    print (program.print())






'''
                new_location = Location(loc.x if dir == 1 or dir == 2 else loc.x - 1 if dir == 3 else loc.x + 1, \
                                loc.y if dir == 3 or dir == 4 else loc.y - 1 if dir == 1 else loc.y + 1, 1)
'''