from dataclasses import dataclass, field
from itertools import repeat
from typing import Any
from queue import PriorityQueue


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    cost: int = field(compare=False)
    item: Any = field(compare=False)


class Pathfinder:
    def __init__(self, possible_moves, success_criteria, cost_function=None):
        self.priority_queue = PriorityQueue()
        self.possible_moves = possible_moves            # returns List[item, cost] from item
        if cost_function:
            self.cost_function = cost_function              # cost_function(item) returns remaining cost
        else:
            self.cost_function = lambda x: 0
        self.success_criteria = success_criteria
        self.visited = set()

    def put_item(self, item, cost):
        self.priority_queue.put(PrioritizedItem(priority=cost + self.cost_function(item), cost=cost, item=item))

    def find_path(self, starting_item):
        self.visited = set()
        self.put_item(starting_item, 0)
        #self.visited.add(starting_item)

        while not self.priority_queue.empty():
            next_item = self.priority_queue.get()
            if next_item.item in self.visited:
                continue
            self.visited.add(next_item.item)

            if self.success_criteria(next_item.item):
                return next_item.item, next_item.cost

            next_moves = self.possible_moves(next_item.item)
            for move in next_moves:
                self.put_item(move[0], next_item.cost+move[1])


# test code
if __name__ == '__main__':
    rooms = {0: (1,), 1: (2, 3, 4), 2: (1, 7), 3: ( 1, 6), 4: (1, 5), 5: (4,), 6: (3,), 7: (2, 8), 8: (7, 10), 10: (8,)}

    def moves(room):
        return zip(rooms[room], repeat(1, len(rooms[room])))

    def goal(room):
        return room == 10

    pathfinder = Pathfinder(moves, goal)
    print("Route with single path, should be 5 long: ", pathfinder.find_path(0))

    rooms = {0: (1,), 1: (2, 3, 4), 2: (1, 7), 3: ( 1, 6, 10), 4: (1, 5), 5: (4,), 6: (3,), 7: (2, 8), 8: (7, 10), 10: (8,3)}
    pathfinder = Pathfinder(moves, goal)
    print("Route with multiple paths, should be 3 long: ", pathfinder.find_path(0))

    # open field
    start = (0,0)
    size = 1000
    goal_pos = (-370, 400)

    def moves(pos):
        moves = list()
        for m in ((-1,0), (1,0), (0,-1), (0,1)):
            if pos[0]+m[0] < size and pos[1]+m[1] < size:
                moves.append( ((pos[0]+m[0], pos[1]+m[1]), 1) )
        return moves

    def goal(pos):
        return pos == goal_pos

    def remain(pos):
        return abs(pos[0]-goal_pos[0]) + abs(pos[1]-goal_pos[1])

    pathfinder = Pathfinder(moves, goal, remain)
    print("Route with single path, should be 770 long: ", pathfinder.find_path(start))
