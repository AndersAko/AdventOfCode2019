import pathfinder
from intcode import Program
from collections import namedtuple
from queue import Queue

Location = namedtuple('Location', 'x y content')        # 0 = wall, 1 = free, 2 = oxygen

class State:
    def __init__(self, program, loc):
        self.program = program
        self.loc = loc

    def find_adjacent_rooms(self):
        result = list()
#        print(f'Locking for adjoining rooms to {self}')
        for dir in range (1,5):
            next_room_computer = self.program.copy()
            next_room_computer.input.put(dir)
            next_room_computer.step()
            coord = (self.loc.x if dir == 1 or dir == 2 else self.loc.x - 1 if dir == 3 else self.loc.x + 1, \
                     self.loc.y if dir == 3 or dir == 4 else self.loc.y - 1 if dir == 1 else self.loc.y + 1)
            found_space = next_room_computer.output.get()
            assert (0 <= found_space <=2)
            if found_space == 0:
                continue
            new_room = State(next_room_computer, Location(coord[0], coord[1], found_space))
#            print(f'  found {new_room}')
            result.append((new_room, 1))
        return result

    def found_oxygen(self):
        return self.loc.content == 2

    def __repr__(self):
        return f'Loc: {self.loc}'

    def __hash__(self):
        return hash(self.loc)

    def __eq__(self, other):
        return self.loc == other.loc

if __name__ == '__main__':
    with open("input_day15.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    initial_program = Program(1, program_code, Queue())
    initial_state = State(initial_program, Location(0, 0, 1))
    finder = pathfinder.Pathfinder(lambda x: x.find_adjacent_rooms(), lambda y: y.found_oxygen())

    print ('Initial state: ', initial_state)
    oxygen = finder.find_path(initial_state)
    print (f'Oxygen found at: {oxygen}')

    mapper = pathfinder.Pathfinder(lambda x: x.find_adjacent_rooms(), lambda y: False)
    foo = mapper.find_path(initial_state)

    print(f'Mapped out the area ({foo}): {mapper.visited}')
    room_map = {l.loc for l in mapper.visited}
    for y in range (-20,20):
        for x in range (-30,40):
            print('#' if Location(x,y,1) in room_map else 'O' if Location(x,y,2) in room_map else ' ', end='')
        print('|')

    minute = 0
    oxygenated = set()
    oxygenated.add(oxygen[0].loc)
    while True:
        newly_oxygenated = set()
        for loc in oxygenated:
            for dir in range(1, 5):
                new_location = Location(loc.x if dir == 1 or dir == 2 else loc.x - 1 if dir == 3 else loc.x + 1, \
                                loc.y if dir == 3 or dir == 4 else loc.y - 1 if dir == 1 else loc.y + 1, 1)
                if new_location in oxygenated or new_location not in room_map:
                    continue
                # print(f'Oxygenating {new_location}')
                newly_oxygenated.add(new_location)
        if not newly_oxygenated:
            break
        oxygenated.update(newly_oxygenated)
        minute += 1
        print(f'Minute {minute}: Filled {len(newly_oxygenated)} new tiles. {len(oxygenated)} / {len(room_map)}')

