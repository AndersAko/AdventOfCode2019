import threading
from queue import Queue
from typing import List
from collections import defaultdict, namedtuple

"""
Instruction set:
ADD a1,a2 o     ADD #a1, #a2, o         ADD a1(REL), a2(REL) o(REL)
MUL a1,a2 o
INPUT a
OUTPUT a
JMP_NZ a1, dest
JMP_Z a1, dest
LESS a1,a2 o
EQUAL a1,a2 o
SET_REL a1
HALT
"""

Opcode = namedtuple('Opcode', 'name args length')

class Program:
    opcodes = { 1: Opcode('ADD', 2, 4), 2: Opcode('MUL', 2, 4), 3: Opcode('INPUT', 0, 2), 4: Opcode('OUTPUT', 1, 2),
                5: Opcode('JMPNZ', 2, 3), 6: Opcode('JMPZ', 2, 3), 7: Opcode('LESS', 2, 4), 8: Opcode('EQUAL', 2, 4),
                9: Opcode('SET_REL', 1, 2), 99: Opcode('HALT', 0, 0)}

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
        new_ip = self.ip + Program.opcodes[opcode].length

        args = self.get_args(modes, Program.opcodes[opcode].args)
        if opcode == 1:  # add
            self.write(3,modes, args[0] + args[1])
        elif opcode == 2:  # mul
            self.write(3, modes, args[0] * args[1])
        elif opcode == 3:  # input
            incoming = self.input.get()
#            print(f"Program: read {incoming}")
            self.write(1, modes, incoming)
        elif opcode == 4:  # output
            outgoing = args[0]
            self.output.put(args[0])
        elif opcode == 5:  # jump if true
            if args[0] != 0:
                new_ip = args[1]
        elif opcode == 6:  # jump if false
            if args[0] == 0:
                new_ip = args[1]
        elif opcode == 7:  # less than
            self.write(3, modes, 1 if args[0] < args[1] else 0)
        elif opcode == 8:  # equals
            self.write(3, modes, 1 if args[0] == args[1] else 0)
        elif opcode == 9:   # adjust relative offset
            self.rel_mode_base += args[0]

        elif opcode == 99:
            new_ip = -1
        else:
            print("Oops, found opcode", self.program[self.ip], "at", self.ip)
        self.ip = new_ip

    def list_program(self):
        ip = 0
        while ip < len(self.program):
            instr = self.program[ip]%100
            yield (f"{ip:3}: {self.opcodes[instr].name}")
            ip += 1
            for arg in range(self.opcodes[instr].args):
                yield self.program[ip]
                ip += 1
            if self.opcodes[instr].length-self.opcodes[instr].args == 2:
                yield self.program[ip]
                ip += 1




    def run(self):
        self.ip = 0
        while self.ip != -1:
            self.execute()
#            print(self.program)

#        print("Halted with output", self.output)
        return

def get_queue(q):
    while not q.empty():
        yield q.get()

if __name__ == '__main__':
    program_code = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    program = Program(1, program_code, Queue())
    program.run()
    output = list(get_queue(program.output))
    print("Output:", output)
    assert output == program_code

    program_code = [1102,34915192,34915192,7,4,7,99,0]
    program = Program(2, program_code, Queue())
#    print("Program: ", " ".join(program.list_program()))

    program.run()
    output = list(get_queue(program.output))
    print("Output:", output)
    assert output == [1219070632396864]

    program_code = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,34,1006,1101,0,689,1022,1102,27,1,1018,1102,1,38,1010,1102,1,31,1012,1101,20,0,1015,1102,1,791,1026,1102,0,1,1020,1101,24,0,1000,1101,0,682,1023,1101,788,0,1027,1101,0,37,1005,1102,21,1,1011,1102,1,28,1002,1101,0,529,1024,1101,39,0,1017,1102,30,1,1013,1101,0,23,1003,1102,524,1,1025,1101,32,0,1007,1102,25,1,1008,1101,29,0,1001,1101,33,0,1016,1101,410,0,1029,1101,419,0,1028,1101,22,0,1014,1102,26,1,1019,1102,1,35,1009,1102,36,1,1004,1102,1,1,1021,109,11,2107,22,-8,63,1005,63,199,4,187,1106,0,203,1001,64,1,64,1002,64,2,64,109,2,21108,40,40,-2,1005,1011,221,4,209,1106,0,225,1001,64,1,64,1002,64,2,64,109,13,21102,41,1,-7,1008,1019,41,63,1005,63,251,4,231,1001,64,1,64,1106,0,251,1002,64,2,64,109,-19,1202,1,1,63,1008,63,26,63,1005,63,271,1105,1,277,4,257,1001,64,1,64,1002,64,2,64,109,7,2101,0,-6,63,1008,63,24,63,1005,63,297,1106,0,303,4,283,1001,64,1,64,1002,64,2,64,109,7,1205,-1,315,1105,1,321,4,309,1001,64,1,64,1002,64,2,64,109,-11,21107,42,41,0,1005,1010,341,1001,64,1,64,1106,0,343,4,327,1002,64,2,64,109,-8,1207,6,24,63,1005,63,363,1001,64,1,64,1106,0,365,4,349,1002,64,2,64,109,11,1206,8,381,1001,64,1,64,1106,0,383,4,371,1002,64,2,64,109,4,1205,4,401,4,389,1001,64,1,64,1105,1,401,1002,64,2,64,109,14,2106,0,-3,4,407,1001,64,1,64,1106,0,419,1002,64,2,64,109,-33,1202,3,1,63,1008,63,29,63,1005,63,445,4,425,1001,64,1,64,1105,1,445,1002,64,2,64,109,-5,2102,1,7,63,1008,63,25,63,1005,63,465,1105,1,471,4,451,1001,64,1,64,1002,64,2,64,109,11,21107,43,44,7,1005,1011,489,4,477,1105,1,493,1001,64,1,64,1002,64,2,64,109,-3,1208,8,35,63,1005,63,511,4,499,1105,1,515,1001,64,1,64,1002,64,2,64,109,25,2105,1,-2,4,521,1106,0,533,1001,64,1,64,1002,64,2,64,109,-8,21108,44,47,-8,1005,1010,549,1106,0,555,4,539,1001,64,1,64,1002,64,2,64,109,-19,1207,7,35,63,1005,63,577,4,561,1001,64,1,64,1106,0,577,1002,64,2,64,109,2,2108,32,0,63,1005,63,597,1001,64,1,64,1106,0,599,4,583,1002,64,2,64,109,13,2101,0,-7,63,1008,63,32,63,1005,63,625,4,605,1001,64,1,64,1105,1,625,1002,64,2,64,109,-13,2107,24,2,63,1005,63,645,1001,64,1,64,1106,0,647,4,631,1002,64,2,64,109,18,21101,45,0,-4,1008,1015,43,63,1005,63,671,1001,64,1,64,1105,1,673,4,653,1002,64,2,64,109,-6,2105,1,10,1001,64,1,64,1105,1,691,4,679,1002,64,2,64,109,1,1208,-6,23,63,1005,63,707,1105,1,713,4,697,1001,64,1,64,1002,64,2,64,109,-2,1206,8,731,4,719,1001,64,1,64,1106,0,731,1002,64,2,64,109,-7,21102,46,1,5,1008,1010,43,63,1005,63,751,1106,0,757,4,737,1001,64,1,64,1002,64,2,64,109,-9,2108,24,4,63,1005,63,779,4,763,1001,64,1,64,1106,0,779,1002,64,2,64,109,38,2106,0,-7,1106,0,797,4,785,1001,64,1,64,1002,64,2,64,109,-27,2102,1,-6,63,1008,63,29,63,1005,63,819,4,803,1105,1,823,1001,64,1,64,1002,64,2,64,109,1,21101,47,0,7,1008,1015,47,63,1005,63,845,4,829,1105,1,849,1001,64,1,64,1002,64,2,64,109,-11,1201,5,0,63,1008,63,31,63,1005,63,869,1106,0,875,4,855,1001,64,1,64,1002,64,2,64,109,5,1201,4,0,63,1008,63,34,63,1005,63,901,4,881,1001,64,1,64,1105,1,901,4,64,99,21102,27,1,1,21101,915,0,0,1105,1,922,21201,1,58905,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1106,0,922,22101,0,1,-1,21201,-2,-3,1,21102,1,957,0,1106,0,922,22201,1,-1,-2,1106,0,968,22102,1,-2,-2,109,-3,2106,0,0]
    input_queue = Queue()
    input_queue.put(1)
    program = Program(3, program_code, input_queue)
    program.run()
    output = list(get_queue(program.output))
    print("Output:", output)
    assert output == [3280416268]

    input_queue = Queue()
    input_queue.put(2)
    program = Program(3, program_code, input_queue)
    program.run()
    output = list(get_queue(program.output))
    print("Output:", output)
    assert output == [80210]

