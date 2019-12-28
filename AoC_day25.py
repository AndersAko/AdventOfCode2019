from time import sleep

import intcode
from collections import namedtuple
import threading
from queue import Queue


def send_input(cmd):
    #print('Sending: ', cmd)
    for char in cmd:
        program.input.put(ord(char))
    program.input.put(10)

def print_output():
    while not program.output.empty():
        read = program.output.get()
        if read < 256:
            print(chr(read),  end='')
        else:
            print(f'\nResult: {read}')

with open("input_day25.txt", "r") as input_file:
    program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program = intcode.Program(0, program_code, Queue())
    program_thread = threading.Thread(target=program.run)
    program_thread.start()

    while program_thread.is_alive():
        sleep(0.1)
        print_output()
        if not program_thread.is_alive():
            break
        user_input = input('')
        send_input(user_input)

    print('End')