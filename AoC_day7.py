import threading
from itertools import permutations
from typing import List
from queue import Queue

class Program:
    opcode_length = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 99: 0}

    def __init__(self, amp_id, _program: List[int], _input: Queue):
        self.amp_id = amp_id
        self.program = list(_program)
        self.input = _input
        self.ip = 0
        self.output = Queue()

    def get_args(self, modes, num) -> list:
        args = list()
        if num >= 1:
            arg = self.program[self.ip + 1]
            if (modes % 10) == 0:
                arg = self.program[arg]
            args.append(arg)
        if num >= 2:
            arg = self.program[self.ip + 2]
            if (modes // 10 % 10) == 0:
                arg = self.program[arg]
            args.append(arg)
        if num >= 3:
            print("Not supported!")

        return args

    def execute(self):
        opcode = self.program[self.ip] % 100
        modes = self.program[self.ip] // 100 % 1000
        new_ip = self.ip + Program.opcode_length[opcode]

        if opcode == 1:  # add
            args = self.get_args(modes, 2)
            self.program[self.program[self.ip + 3]] = args[0] + args[1]
        elif opcode == 2:  # mul
            args = self.get_args(modes, 2)
            self.program[self.program[self.ip + 3]] = args[0] * args[1]
        elif opcode == 3:  # input
            incoming = self.input.get()
            self.program[self.program[self.ip + 1]] = incoming
 #           print(f"{self.amp_id}: Read {incoming}")
        elif opcode == 4:  # output
            args = self.get_args(modes, 1)
            outgoing = args[0]
            self.output.put(args[0])
 #           print(f"{self.amp_id}: Put {args[0]}")
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
            self.program[self.program[self.ip + 3]] = 1 if args[0] < args[1] else 0
        elif opcode == 8:  # equals
            args = self.get_args(modes, 2)
            self.program[self.program[self.ip + 3]] = 1 if args[0] == args[1] else 0
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


with open("input_day7.txt", "r") as input_file:
    program_code = list(map(int, input_file.readline().strip(" ").split(",")))
    program_code = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
#    program_code = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]

    max_output = 0
    for phase_code in permutations(range(5)):
        threads = list()
        for amp in range(5):
            if amp == 0:
                input_queue = Queue()
                input_queue.put(phase_code[amp])
                input_queue.put(0)
            else:
                input_queue = program.output
                if not input_queue.empty():
                    print(f"Amp: {amp}: queue contains {input_queue.qsize()} items before priming")
                input_queue.put(phase_code[amp])

            program = Program(amp, program_code, input_queue)
            if amp == 4:
                output = program.output

            t = threading.Thread(target=program.run)
            threads.append(t)

        for t in threads:
            t.start()

        # wait for finish
        for t in threads:
            t.join()

        thruster = output.get_nowait()
        print(f"Phasecode: {phase_code} Amp: {amp} Output {thruster}")

        if thruster > max_output:
            max_output = thruster
            best_phasecode = phase_code

    print (f"Highest output {max_output} for {best_phasecode}")
