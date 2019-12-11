import threading
from collections import defaultdict
from queue import Queue
from intcode import Program


# Read hull, send to output
class PaintingRobot:
    def __init__(self, input_queue, output_queue):
        self.hull = defaultdict(int)
        self.paint_and_turn_directions = input_queue
        self.hull_camera = output_queue
        self.pos = (0, 0)
        self.dir = (0, -1)  # up
        self.stop = False
        self.hull[(0, 0)] = 1

    right_turn = {(0, -1): (1, 0), (1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1)}
    left_turn = {(0, -1): (-1, 0), (-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1)}

    def run(self):
        while not self.stop:
            self.hull_camera.put(self.hull[self.pos])
            paint = self.paint_and_turn_directions.get()
            #            print(f"Robot {self.pos}: paint {paint}")
            self.hull[self.pos] = paint
            turn = self.paint_and_turn_directions.get()
            #            print(f"Robot {self.pos}: turn {turn}")
            if turn == 0:
                self.dir = self.left_turn[self.dir]
            elif turn == 1:
                self.dir = self.right_turn[self.dir]
            else:
                print("Surprise!")
            self.pos = tuple(map(sum, zip(self.pos, self.dir)))


if __name__ == '__main__':
    with open("input_day11.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program_input = Queue()
    program = Program(1, program_code, program_input)
    robot = PaintingRobot(program.output, program_input)

    program_thread = threading.Thread(target=program.run)
    robot_thread = threading.Thread(target=robot.run)

    program_thread.start()
    robot_thread.start()

    # wait for finish
    program_thread.join()

    #    robot.stop = True
    #    robot_thread.join()
    print(f"Painted area: {len(robot.hull)}: {robot.hull}")
    for row in range(8):
        for col in range(50):
            print('#' if robot.hull[(col, row)] == 1 else ' ', end='')
        print()
