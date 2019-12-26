from time import sleep

import intcode
from collections import namedtuple
import threading
from queue import Queue


if __name__ == '__main__':
    with open("input_day23.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    print(f'Initializing')
    nics = []
    nic_threads = []
    for nic in range(50):
        nics.append(intcode.Program(nic, program_code, Queue(), special_mode_23=True))
        nics[nic].input.put(nic)

    print(f'Starting')
    for nic in range(50):
        nic_threads.append(threading.Thread(target=nics[nic].run))
        nic_threads[nic].start()

    print(f'Starting message broker')
    NAT_y_values = set()
    latest_NAT = None
    while True:
        idle = True
        for nic in range(50):
            if not nics[nic].output.empty():
                idle = False
                address = nics[nic].output.get()
                x = nics[nic].output.get()
                y = nics[nic].output.get()
                print(f'{nic}: Sending {x} {y} to {address}')
                if address == 255:
                    print("NAT received : ", x, y)
                    latest_NAT = (x, y)
                else:
                    nics[address].input.put(x)
                    nics[address].input.put(y)
        if idle and not [True for nic in nics if not nic.idle] and latest_NAT is not None:
            print(f'System idle, sending {latest_NAT}')
            if latest_NAT[1] in NAT_y_values:
                print(f'Resending {latest_NAT}')
                exit(0)
            NAT_y_values.add(latest_NAT[1])
            nics[0].input.put(latest_NAT[0])
            nics[0].input.put(latest_NAT[1])
            latest_NAT = None
