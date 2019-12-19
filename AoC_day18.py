import pathfinder
from collections import namedtuple
import cProfile

Location = namedtuple('Location', 'x y')

class State:
    def __init__(self, loc, keys):
        self.loc = loc
        self.keys = keys
        self.sortedkeys = str(sorted(keys))


    def possible_moves(self):            # dir = index('^<v>')
        moves = []
        for dir in range(4):
            new_location = Location(self.loc.x if dir == 0 or dir == 2 else self.loc.x - 1 if dir == 1 else self.loc.x + 1,\
                                self.loc.y if dir == 1 or dir == 3 else self.loc.y - 1 if dir == 0 else self.loc.y + 1)
            if maze[new_location] == '.' or maze[new_location] == '@' \
                    or maze[new_location].islower() or maze[new_location].lower() in self.keys:
                keys = set(self.keys)
                if maze[new_location].islower():
                    keys.add(maze[new_location])
                moves.append((State(new_location, keys), 1))
        #print(f'Possible moves from {self} = {moves}')
        return moves

    def all_keys(self):
        return len(self.keys) == number_of_keys

    def key_reward(self):
        return -len(self.keys)*50

    def __hash__(self):
        return hash((self.loc, self.sortedkeys))

    def __eq__(self, other):
        return (self.loc, self.keys) == (other.loc, other.keys)

    def __repr__(self):
        return f'{self.loc} {self.keys}'

class State2:
    def __init__(self, locs, keys):
        self.locs = locs
        self.keys = keys
        self.sortedkeys = str(sorted(keys))

    def possible_moves(self):            # dir = index('^<v>')
        moves = []
        for loc_ix,loc in enumerate(self.locs):
            for dir in range(4):
                new_location = Location(loc.x if dir == 0 or dir == 2 else loc.x - 1 if dir == 1 else loc.x + 1,\
                                        loc.y if dir == 1 or dir == 3 else loc.y - 1 if dir == 0 else loc.y + 1)
                if maze[new_location] == '.' or maze[new_location] == '@' \
                        or maze[new_location].islower() or maze[new_location].lower() in self.keys:
                    keys = set(self.keys)
                    reward = 0
                    if maze[new_location].islower():
                        if maze[new_location] in keys:
                            #print(f'Found a key that I already had: {maze[new_location]} at {list((l.x,l.y) for l in self.locs)}')
                            break
                        keys.add(maze[new_location])
                        reward = 1000
                    new_locs = list(self.locs)
                    new_locs[loc_ix] = new_location
                    moves.append((State2(new_locs, keys), 1))


        #print(f'Possible moves from {self} = {moves}')
        return moves

    def all_keys(self):
        return len(self.keys) == number_of_keys

    def __hash__(self):
        to_hash = tuple(sorted([(l.x,l.y) for l in self.locs])) + tuple(sorted(self.keys))
        return hash(to_hash)

    def __eq__(self, other):
        return (self.locs, self.keys) == (other.locs, other.keys)

    def __repr__(self):
        return f'{self.locs} {self.keys}'

if __name__ == '__main__':
    with open("input_day18.txt", "r") as input_file:
        maze = dict()
        number_of_keys = 0
        row = 0
        for line in input_file.readlines():
            for col in range(len(line)):
                maze[Location(col, row)] = line[col]
                if line[col] == '@':
                    starting_location = State(Location(col, row), set())
                if line[col].islower():
                    number_of_keys += 1
                size_x = col+1
            row += 1
        size_y = row

    print ('Maze:\n')
    for row in range(size_y):
        for col in range(size_x):
            print(maze[(col, row)], end='')
        print()

    print(starting_location)
    finder = pathfinder.Pathfinder(lambda x: x.possible_moves(), lambda y: y.all_keys())
   # cProfile.run('finder.find_path(starting_location)')
    #    print("Route: ", finder.find_path(starting_location))
    print("Visited: ", len(finder.visited))

    # part 2

    sx = starting_location.loc.x
    sy = starting_location.loc.y
    maze[Location(sx-1, sy-1)] = '@'
    maze[Location(sx, sy-1)] = '#'
    maze[Location(sx+1, sy-1)] = '@'
    maze[Location(sx-1, sy)] = '#'
    maze[Location(sx, sy)] = '#'
    maze[Location(sx+1, sy)] = '#'
    maze[Location(sx-1, sy+1)] = '@'
    maze[Location(sx, sy+1)] = '#'
    maze[Location(sx+1, sy+1)] = '@'

    print('Maze:\n')
    for row in range(size_y):
        for col in range(size_x):
            print(maze[(col, row)], end='')
        print()

    starting_locations = [Location(sx-1, sy-1), Location(sx+1, sy-1), Location(sx-1, sy+1), Location(sx+1, sy+1)]
    print ('Starting locations part 2: ', starting_locations)
    finder_part2 = pathfinder.Pathfinder(lambda x: x.possible_moves(), lambda y: y.all_keys())
    result = finder_part2.find_path(State2(starting_locations, set()))
    print(result)
    print(finder_part2.visited)
