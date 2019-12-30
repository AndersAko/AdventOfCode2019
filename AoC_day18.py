import copy
import queue
from typing import List, Set

import pathfinder
from collections import namedtuple
import cProfile

Location = namedtuple('Location', 'x y')
Location.__repr__ = lambda l: f'L:({l.x},{l.y})'
Path = namedtuple('Path', 'loc d len')


class State:
    def __init__(self, loc, keys):
        self.loc = loc
        self.keys = keys
        self.sortedkeys = str(sorted(keys))

    def possible_moves(self):  # dir = index('^<v>')
        moves = []
        for dir in range(4):
            new_location = Location(
                self.loc.x if dir == 0 or dir == 2 else self.loc.x - 1 if dir == 1 else self.loc.x + 1, \
                self.loc.y if dir == 1 or dir == 3 else self.loc.y - 1 if dir == 0 else self.loc.y + 1)
            if maze[new_location] == '.' or maze[new_location] == '@' \
                    or maze[new_location].islower() or maze[new_location].lower() in self.keys:
                keys = set(self.keys)
                if maze[new_location].islower():
                    keys.add(maze[new_location])
                moves.append((State(new_location, keys), 1))
        # print(f'Possible moves from {self} = {moves}')
        return moves

    def all_keys(self):
        return len(self.keys) == number_of_keys

    def key_reward(self):
        return -len(self.keys) * 50

    def __hash__(self):
        return hash((self.loc, self.sortedkeys))

    def __eq__(self, other):
        return (self.loc, self.keys) == (other.loc, other.keys)

    def __repr__(self):
        return f'{self.loc} {self.keys}'


class State2:
    def __init__(self, locs: List[Location], keys: Set[str] = set(), total_length: int = 0):
        self.locs = locs
        self.keys = keys
        self.length = total_length
        self.route = []

    # follow all paths from loc, avoiding avoid_dir, until a new key is found, branching when needed
    def follow_path(self, path: Path) -> List[Path]:
        possible_stops = []
        visited: Set[Location] = set()
        search_nodes = queue.Queue()
        search_nodes.put(path)

        while not search_nodes.empty():
            node = search_nodes.get()
            neighbours = [Path(Location(node.loc.x if d == 0 or d == 2 else node.loc.x - 1 if d == 1 else node.loc.x + 1,
                                        node.loc.y if d == 1 or d == 3 else node.loc.y - 1 if d == 0 else node.loc.y + 1),
                               d, node.len+1) for d in range(4)]
            neighbours = [l for l in neighbours if not (maze[l.loc] == '#' or l.loc in visited or
                          (maze[l.loc].isupper() and maze[l.loc].lower() not in self.keys))]
            for neighbour in neighbours:
                visited.add(neighbour.loc)
                if maze[neighbour.loc].islower() and maze[neighbour.loc] not in self.keys:
                    possible_stops.append(neighbour)
                else:
                    search_nodes.put(neighbour)
        return possible_stops

    def possible_moves(self):  # dir = index('^<v>')
        moves = []
        for loc_ix, loc in enumerate(self.locs):
            #print(f'Follow path from {loc}', end='')
            new_locations = self.follow_path(Path(loc, None, 0))
            #print(f' -> {new_locations}')
            for new_location in new_locations:
                # possible locations should include: new keys
                assert maze[new_location.loc].islower() and maze[new_location.loc] not in self.keys
                possible_move = copy.deepcopy(self)
                possible_move.route.append(f'{loc_ix}:{possible_move.locs[loc_ix]} -> {new_location.loc}')
                possible_move.keys.add(maze[new_location.loc])
                possible_move.locs[loc_ix] = new_location.loc
                possible_move.length += new_location.len
                moves.append((possible_move, new_location.len))

        #print(f'Possible moves from {self} = {moves}')
        return moves

    def all_keys(self):
        return len(self.keys) == number_of_keys

    def __hash__(self):
        to_hash = tuple([(l.x, l.y) for l in self.locs]) + tuple(sorted(self.keys))
        return hash(to_hash)

    def __eq__(self, other):
        return (self.locs, self.keys) == (other.locs, other.keys)

    def __repr__(self):
        return f'{self.locs} {self.keys} ({self.route})'


if __name__ == '__main__':
    with open("input_day18.txt", "r") as input_file:
        maze = dict()
        row = 0
        for line in input_file.readlines():
            for col in range(len(line.strip('\n'))):
                maze[Location(col, row)] = line[col]
            row += 1

    size_x = max(loc.x for loc in maze) + 1
    size_y = max(loc.y for loc in maze) + 1
    starting_locations = [loc for loc in maze if maze[loc] == '@']
    number_of_keys = sum(1 for x in maze if maze[x].islower())

    print('Maze:\n')
    for row in range(size_y):
        for col in range(size_x):
            print(maze[(col, row)], end='')
        print()
    print('Starting location: ', starting_locations)
    print(f'Size = {size_x, size_y}')
    print(f'Number of keys: {number_of_keys}')

    finder = pathfinder.Pathfinder(lambda x: x.possible_moves(), lambda y: y.all_keys())
    # cProfile.run('finder.find_path(starting_location)')
    print("Route version 1: ", finder.find_path(State(starting_locations[0], set())))
    print("Visited: ", len(finder.visited))

    route2 = finder.find_path(State2(starting_locations))
    print("Route version 2: ", route2[1], route2)
    print("Visited: ", len(finder.visited))
    print("Path: ", route2[0].route)


    # part 2

    sx = starting_locations[0].x
    sy = starting_locations[0].y
    maze[Location(sx - 1, sy - 1)] = '@'
    maze[Location(sx, sy - 1)] = '#'
    maze[Location(sx + 1, sy - 1)] = '@'
    maze[Location(sx - 1, sy)] = '#'
    maze[Location(sx, sy)] = '#'
    maze[Location(sx + 1, sy)] = '#'
    maze[Location(sx - 1, sy + 1)] = '@'
    maze[Location(sx, sy + 1)] = '#'
    maze[Location(sx + 1, sy + 1)] = '@'

    print('Maze:\n')
    key_sector = dict()
    for row in range(size_y):
        for col in range(size_x):
            print(maze[(col, row)], end='')
            if maze[(col, row)].islower():
                sector = (2 * col // size_x, 2 * row // size_y)
                if sector not in key_sector:
                    key_sector[sector] = set()
                key_sector[sector].add(maze[(col, row)])
        print()

    print('Keys per sector')
    for sector in key_sector:
        print(f'Sector: {sector}: {",".join(key_sector[sector])}')

    starting_locations = [loc for loc in maze if maze[loc] == '@']
    print('Starting locations part 2: ', starting_locations)
    finder_part2 = pathfinder.Pathfinder(lambda x: x.possible_moves(), lambda y: y.all_keys())
    result = finder_part2.find_path(State2(starting_locations))
    print(f'Result of search part 2: {result[1]}   {result}')
    print('Visited:', len(finder_part2.visited))
    print("Path: ", result[0].route)
