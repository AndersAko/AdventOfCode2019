import threading
from collections import defaultdict
from itertools import permutations
from typing import List
from queue import Queue

class Program:
    opcode_length = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 0}

    def __init__(self, amp_id, _program: List[int], _input: Queue):
        self.amp_id = amp_id
        self.program = defaultdict(int)
        for i in range(len(_program)):
            self.program[i] = _program[i]
        self.input = _input
        self.ip = 0
        self.output = Queue()
        self.rel_mode_base = 0

    def get_args(self, modes, num) -> list:
        args = list()
        if num >= 1:
            arg = self.program[self.ip + 1]
            if (modes % 10) == 0:
                arg = self.program[arg]
            elif (modes % 10) == 2:
                arg = self.program[self.rel_mode_base+arg]
            args.append(arg)
        if num >= 2:
            arg = self.program[self.ip + 2]
            if (modes // 10 % 10) == 0:
                arg = self.program[arg]
            elif (modes // 10 % 10) == 2:
                arg = self.program[self.rel_mode_base+arg]
            args.append(arg)
        if num >= 3:
            print("Not supported!")
        return args

    def write(self, addr_argument_index, modes, value):
        address = self.program[self.ip + addr_argument_index]
        mode_digit = modes // pow (10, addr_argument_index-1) % 10
        if mode_digit == 0:
            self.program[address] = value
        elif mode_digit == 1:
            print ("Immediate mode addressing for write operation!")
            exit(0)
        elif mode_digit == 2:
            self.program[self.rel_mode_base + address] = value

    def execute(self):
        opcode = self.program[self.ip] % 100
        modes = self.program[self.ip] // 100 % 1000
        new_ip = self.ip + Program.opcode_length[opcode]

        if opcode == 1:  # add
            args = self.get_args(modes, 2)
            self.write(3,modes, args[0] + args[1])
        elif opcode == 2:  # mul
            args = self.get_args(modes, 2)
            self.write(3, modes, args[0] * args[1])
        elif opcode == 3:  # input
            incoming = self.input.get()
            self.write(1, modes, incoming)
        elif opcode == 4:  # output
            args = self.get_args(modes, 1)
            outgoing = args[0]
            self.output.put(args[0])
        elif opcode == 5:  # jump if true
            args = self.get_args(modes, 2)
            if args[0] != 0:
                new_ip = args[1]
        elif opcode == 6:  # jump if false
            args = self.get_args(modes, 2)
            if args[0] == 0:
                new_ip = args[1]
        elif opcode == 7:  # less than
            args = self.get_args(modes, 2)
            self.write(3, modes, 1 if args[0] < args[1] else 0)
        elif opcode == 8:  # equals
            args = self.get_args(modes, 2)
            self.write(3, modes, 1 if args[0] == args[1] else 0)
        elif opcode == 9:   # adjust relative offset
            args = self.get_args(modes, 1)
            self.rel_mode_base += args[0]

        elif opcode == 99:
            new_ip = -1
        else:
            print("Oops, found opcode", self.program[self.ip], "at", self.ip)
        self.ip = new_ip

    def run(self):
        self.ip = 0
        while self.ip != -1:
            self.execute()
#            print(self.program)

#        print("Halted with output", self.output)
        return


if __name__ == '__main__':
    with open("input_day9.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

        input_queue = Queue()
        input_queue.put(2)
        program = Program(1, program_code, input_queue)
        program.run()
        print ("Output:")
        while not program.output.empty():
            print (program.output.get_nowait())

