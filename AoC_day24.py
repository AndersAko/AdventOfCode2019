from enum import Enum

class Dir(Enum):
    UP = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4

def print_eris(e_stack):
    for l in e_stack:
        print(f' L:{l:-3}', end=' ')
    print()
    for r in range(5):
        for l in e_stack:
            print(''.join(['#' if c else '.' for c in e_stack[l][r*5:r*5+5]]), end='  ')
        print()
    print(diversity(e_stack[0]))


def get_adjacent(cell_index, direction, current_level):
    if cell_index == 12:
        return 0
    if direction == Dir.UP:
        if cell_index < 5:
            return 1 if eris_stack.get(current_level-1) and eris_stack[current_level-1][7] else 0
        elif cell_index == 17:
            return sum(1 for t in eris_stack[current_level+1][20:] if t) if current_level + 1 in eris_stack else 0
        else:
            return 1 if eris_stack[current_level][cell_index-5] else 0
    elif direction == Dir.LEFT:
        if cell_index % 5 == 0:
            return 1 if eris_stack.get(current_level-1) and eris_stack[current_level-1][11] else 0
        elif cell_index == 13:
            return sum(1 for t in eris_stack[current_level + 1][4::5] if t) if current_level + 1 in eris_stack else 0
        else:
            return 1 if eris_stack[current_level][cell_index-1] else 0
    elif direction == Dir.RIGHT:
        if cell_index % 5 == 4:
            return 1 if eris_stack.get(current_level-1) and eris_stack[current_level-1][13] else 0
        elif cell_index == 11:
            return sum(1 for t in eris_stack[current_level + 1][0::5] if t) if current_level + 1 in eris_stack else 0
        else:
            return 1 if eris_stack[current_level][cell_index+1] else 0
    elif direction == Dir.DOWN:
        if cell_index >= 20:
            return 1 if eris_stack.get(current_level-1) and eris_stack[current_level-1][17] else 0
        elif cell_index == 7:
            return sum(1 for t in eris_stack[current_level + 1][:5] if t) if current_level + 1 in eris_stack else 0
        else:
            return 1 if eris_stack[current_level][cell_index+5] else 0


def tick(level):
    new_state = []
    for i in range(len(eris_stack[level])):
        # up left right down
        adjacent = sum(get_adjacent(i, d, level) for d in Dir)
        new_state.append(True if adjacent == 1 or (not eris_stack[level][i] and adjacent == 2) else False)
    return new_state


def diversity(e):
    return sum(2**i for i in range(len(e)) if e[i])


with open("input_day24.txt", "r") as input_file:

    eris = []
    for line in input_file.readlines():
        eris.extend([True if c == '#' else False for c in line.strip('\n')])
    eris_stack = {0: eris, -1: [False]*len(eris), 1: [False]*len(eris), }

    print_eris(eris_stack)

    ''' passed_states = set()
    while tuple(eris_stack[0]) not in passed_states:
        passed_states.add(tuple(eris_stack[0]))
        eris_stack[0] = tick(0)
        print_eris(eris_stack)
    '''

    print(f'============  Part 2  ==============')

    for minute in range(200):
        new_state = dict()
        if [True for t in eris_stack[min(eris_stack)] if t]:
            new_level = min(eris_stack)-1
            new_state[new_level] = [False] * len(eris_stack[0])
            print(f'Added level {new_level}')
        if [True for t in eris_stack[max(eris_stack)] if t]:
            new_level = max(eris_stack)+1
            new_state[new_level] = [False] * len(eris_stack[0])
            print(f'Added level {new_level}')

        for level in eris_stack:
            new_level = tick(level)
            new_state[level] = new_level
        eris_stack = new_state
        print_eris(eris_stack)

    bug_count = 0
    for level in eris_stack:
        bug_count += sum(1 for t in eris_stack[level] if t)

    print (f'Total bugs in system: {bug_count}')