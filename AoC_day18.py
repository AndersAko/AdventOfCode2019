import pathfinder
from collections import namedtuple
import cProfile

Location = namedtuple('Location', 'x y')

class State:
    def __init__(self, loc, keys):
        self.loc = loc
        self.keys = keys

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
        return hash((self.loc, str(sorted(self.keys))))

    def __eq__(self, other):
        return (self.loc, self.keys) == (other.loc, other.keys)

    def __repr__(self):
        return f'{self.loc} {self.keys}'


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
    cProfile.run('finder.find_path(starting_location)')
    #    print("Route: ", finder.find_path(starting_location))
    # print("Visited: ", len(finder.visited))

    # part 2
    '''
    sx = starting_location.loc.x
    sy = starting_location.loc.y
    maze[Location(sx-1, sy-1)] = '@'
    maze[Location(sx, sy-1)] = '@'
    maze[Location(sx+1, sy-1)] = '@'
    '''