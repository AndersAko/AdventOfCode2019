
program = list()
output = list()
opcode_length = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 99: 0}


def get_args(modes, num) -> list:
    args = list()
    if num >= 1:
        arg = program[ip + 1]
        if (modes % 10) == 0:
            arg = program[arg]
        args.append(arg)

    if num >= 2:
        arg = program[ip + 2]
        if (modes // 10 % 10) == 0:
            arg = program[arg]
        args.append(arg)

    if num >= 3:
        arg = program[ip + 3]
        if (modes // 100 % 10) == 0:
            arg = program[arg]
            print("Surprise!!")
        args.append(arg)
    return args


def execute(ip: int) -> int:
    opcode = program[ip]%100
    modes = program[ip]//100 % 1000
    new_ip = ip + opcode_length[opcode]

    if opcode == 1:         # add
        args = get_args(modes, 2)
        program[program[ip + 3]] = args[0] + args[1]
    elif opcode == 2:       # mul
        args = get_args(modes, 2)
        program[program[ip + 3]] = args[0] * args[1]
    elif opcode == 3:       # input
        # read a "1" for now
        program[program[ip + 1]] = 5
    elif opcode == 4:       # output
        args = get_args(modes, 1)
        output.append(args[0])
    elif opcode == 5:       # jump if true
        args = get_args(modes, 2)
        if args[0]!= 0:
            new_ip = args[1]
    elif opcode == 6:  # jump if false
        args = get_args(modes, 2)
        if args[0] == 0:
            new_ip = args[1]
    elif opcode == 7:  # less than
        args = get_args(modes, 2)
        program[program[ip + 3]] = 1 if args[0] < args[1] else 0
    elif opcode == 8:  # equals
        args = get_args(modes, 2)
        program[program[ip + 3]] = 1 if args[0] == args[1] else 0
    elif opcode == 99:
        print("HALT")
        new_ip = -1
    else:
        print("Oops, found opcode", program[ip], "at", ip)

    return new_ip


with open("input_day5.txt", "r") as input_file:
    program = list(map(int, input_file.readline().strip(" ").split(",")))
    # program = [3,9,8,9,10,9,4,9,99,-1,8 ]
    # program = [3,9,7,9,10,9,4,9,99,-1,8 ]
    # program = [3,3,1108,-1,8,3,4,3,99]
    # program = [3,3,1107,-1,8,3,4,3,99]
    # program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
     #          999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

    ip = 0
    while True:
        ip = execute(ip)
        print (program)
        if ip == -1:
            break;

    print("Halted with output", output)


