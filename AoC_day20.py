import pathfinder
from collections import namedtuple
import cProfile

Location = namedtuple('Location', 'x y')


class State:
    call_count = 0

    def __init__(self, loc, level=0, route=[]):
        self.loc = loc
        self.route = route
        self.level = level

    def possible_moves(self):  # dir = index('^<v>')
        State.call_count += 1
        if State.call_count%10000 == 0:
            print(f'{self} {len(self.route)}')
        moves = []
        for dir in range(4):
            jump = False
            new_level = self.level
            new_location = Location(self.loc.x if dir == 0 or dir == 2 else self.loc.x - 1 if dir == 1 else self.loc.x + 1, \
                                    self.loc.y if dir == 1 or dir == 3 else self.loc.y - 1 if dir == 0 else self.loc.y + 1)
            if not new_location in maze:
                continue
            if maze[new_location].isalpha():        # portal
                matching_portals = [x for x in maze if maze[x]==maze[new_location] and x != new_location]
                if len(matching_portals) == 0:  # top level portals have no match and are only active on level 0
                    if new_level > 0:
                        continue
                else:
                    assert (len(matching_portals) == 1)
                    outside_portal = (self.loc.x < 5 or self.loc.y < 5 or \
                                      self.loc.x > size_x - 5 or self.loc.y > size_y - 5)
                    if outside_portal:
                        if new_level == 0:
                            continue
                        new_level -= 1
                    else:
                        new_level += 1
                    new_location = matching_portals[0]
                    jump = True
            elif maze[new_location] != '.':
                continue
            moves.append((State(new_location, new_level), 1 if not jump else 2))
            #moves.append((State(new_location, new_level, self.route + [new_location]), 1 if not jump else 2))
        #print(f'Possible moves from {self} = {moves}')
        return moves

    def at_end(self):
        return maze[self.loc]=='ZZ'

    def __hash__(self):
        return hash((self.loc, self.level))

    def __eq__(self, other):
        return (self.loc, self.level) == (other.loc, other.level)

    def __repr__(self):
        return f'{maze[self.loc]}:({self.loc.x},{self.loc.y})/{self.level} '


def get_portal(loc):
    if loc in maze and maze[(col, row)].isalpha() and len(maze[(col, row)])==1:
        for dir in range(4):            # dir = index('^<v>')
            neighbour_loc = Location(loc.x if dir == 0 or dir == 2 else loc.x - 1 if dir == 1 else loc.x + 1, \
                                     loc.y if dir == 1 or dir == 3 else loc.y - 1 if dir == 0 else loc.y + 1)
            if maze.get(neighbour_loc) == '.':
                first_portal_char = Location(loc.x if dir != 3 else loc.x - 1, loc.y if dir != 2 else loc.y - 1)
                second_portal_char = Location(loc.x if dir != 1 else loc.x + 1, loc.y if dir != 0 else loc.y + 1)
                portal = maze[first_portal_char] + maze[second_portal_char]
                return (neighbour_loc, portal)
    return None


if __name__ == '__main__':
    with open("input_day20.txt", "r") as input_file:
        maze = dict()
        number_of_keys = 0
        row = 0
        for line in input_file.readlines():
            line = line.strip('\n')
            for col in range(len(line)):
                maze[Location(col, row)] = line[col]
            row += 1

    size_x = max(x.x for x in maze)
    size_y = max(x.y for x in maze)

    for row in range(size_y):
        for col in range(size_x):
            if (col, row) in maze:
                maybe_portal = get_portal(Location(col, row))
                if maybe_portal:
                    maze[maybe_portal[0]] = maybe_portal[1]

    print('Maze:\n')
    for row in range(size_y):
        for col in range(size_x):
            if (col, row) in maze:
                if maze[(col, row)].isalpha() and len(maze[(col, row)])==1:
                    maze[(col, row)] = ' '
                print(f'{maze[(col, row)]:2}', end='')
            else:
                print('  ', end='')
        print()

    starting_location = State([x for x in maze if maze[x]=='AA'][0])
    print(starting_location)
    finder = pathfinder.Pathfinder(lambda x: x.possible_moves(), lambda y: y.at_end())
    cProfile.run('finder.find_path(starting_location)')
    result = finder.find_path(starting_location)
    print("Route: ", result, result[0].route)
    print("Visited: ", len(finder.visited))
