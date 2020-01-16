from time import sleep

import intcode
import pathfinder
from collections import namedtuple
import threading
import itertools

def send_input(cmd):
    print('Sending: ', cmd)
    for char in cmd:
        program.input.put(ord(char))
    program.input.put(10)

def get_output():
    while not program.output.empty():
        read = program.output.get()
        if read < 256:
            print(chr(read),  end='')
        else:
            print(f'\nResult: {read}')

if __name__ == '__main__':
    with open("input_day21.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program = intcode.Program(0, program_code)
    #program.print()

    program_thread = threading.Thread(target=program.run)
    program_thread.start()

    sleep(1)
    get_output()
    send_input('OR E J')
    send_input('OR H J')
    send_input('NOT C T')
    send_input('AND T J')

    send_input('NOT B T')
    send_input('OR T J')

    send_input('NOT A T')
    send_input('OR T J')

    send_input('AND D J')

    get_output()

    send_input('RUN')

    while program_thread.is_alive():
        get_output()

