def execute(program, ip):
    opcode = program[ip]%100

    modes = program[ip]//100 % 100

    arg1 = program[ip + 1]
    if (modes // 1000 % 10) == 0:
        arg1 = program[arg1]
    arg2 = program[ip + 2]
    if (modes // 10000 % 10) == 0:
        arg2 = program[arg2]
    arg3 = program[ip + 3]
    if (modes // 100000 % 10) == 0:
        arg3 = program[arg3]


    if opcode == 1:
        #            print("1: adding", opcodes[index + 1], opcodes[index + 2], "to", opcodes[index + 3])
        program[program[index + 3]] = program[program[index + 1]] + program[program[index + 2]]
        #           print("=>", opcodes)
    elif program[index] == 2:
        #           print("2: multiplying", opcodes[index + 1], opcodes[index + 2], "to", opcodes[index + 3])
        program[program[index + 3]] = program[program[index + 1]] * program[program[index + 2]]
        #           print("=>", opcodes)
    else:
        print("Oops, found opcode", program[index], "at", index)
        break

def execute2():


def int_code(_program, noun, verb):
    program = list(_program)
    program[1] = noun
    program[2] = verb
    index = 0

    while program[index] != 99:
        if program[index] == 1:
            #            print("1: adding", opcodes[index + 1], opcodes[index + 2], "to", opcodes[index + 3])
            program[program[index + 3]] = program[program[index + 1]] + program[program[index + 2]]
            #           print("=>", opcodes)
        elif program[index] == 2:
            #           print("2: multiplying", opcodes[index + 1], opcodes[index + 2], "to", opcodes[index + 3])
            program[program[index + 3]] = program[program[index + 1]] * program[program[index + 2]]
            #           print("=>", opcodes)
        else:
            print("Oops, found opcode", program[index], "at", index)
            break
        index += 4
    return program[0]


with open("input_day5.txt", "r") as input_file:
    opcodes = list(map(int, input_file.readline().strip(" ").split(",")))

print(int_code(opcodes, 12, 2))
print("=>", opcodes)
print(opcodes[0])


for noun in range(0,99):
    for verb in range(0,99):
        if int_code(opcodes, noun, verb) == 19690720:
            print("Noun: ", noun,"Verb:", verb, "=>", 100*noun+verb)
            break;


