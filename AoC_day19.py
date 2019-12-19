import intcode
import threading

def probe(x,y):
    program = intcode.Program(0, program_code)
    program.input.put(x)
    program.input.put(y)
    program.run()
    return program.output.get()


def find_start_of_beam_at_distance(y, start=0, stop=50):
    found_0 = False
    for x in range(start, stop):
        pull = probe(x,y)
        if pull == 0:
            found_0 = True
        if found_0 and pull == 1:
            return x
    return None

def find_end_of_beam_at_distance(y, start=0, stop=50):
    found_0 = False
    for x in range(stop, start, -1):
        pull = probe(x,y)
        if pull == 0:
            found_0 = True
        if found_0 and pull == 1:
            return x
    return None

if __name__ == '__main__':
    with open("input_day19.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program = intcode.Program(0, program_code)

    '''   affected = 0
    start_beam_20 = 0
    start_beam_40 = 0
    for y in range(50):
        for x in range(50):
            pull = probe(x, y)
            if pull == 1:
                affected += 1
            print(pull, end = '')
        print()

    print(f'{affected} squares affected within closest 50x50')
    '''
    # Part 2
    slope_start = (find_start_of_beam_at_distance(40) - find_start_of_beam_at_distance(20))/20
    slope_end = (find_end_of_beam_at_distance(40) - find_end_of_beam_at_distance(20))/20
    print(f'Slope start: {slope_start} end: {slope_end}')

    guess_start_100x100_y = int(100*(slope_start+1) / (slope_end - slope_start))

    while True:
        guess_start_x = int(slope_start * (guess_start_100x100_y + 100))
        guess_end_x = int(slope_end * guess_start_100x100_y)

        xe = find_end_of_beam_at_distance(guess_start_100x100_y, guess_end_x-100, guess_end_x+50)
        xs = find_start_of_beam_at_distance(guess_start_100x100_y+99, guess_start_x-50, guess_start_x+100)

        if xe - xs == 99:
            break

        guess_start_100x100_y += int((99-(xe-xs))*(slope_start+1) // (slope_end - slope_start))

    print(f'Found a first fitting spot at {guess_start_100x100_y}, from x: {xs}-{xe}')

    # Try to see if it can be reduced further
    while True:
        xe_1 = find_end_of_beam_at_distance(guess_start_100x100_y-1, guess_end_x-100, guess_end_x+50)
        xs_1 = find_start_of_beam_at_distance(guess_start_100x100_y-1+99, guess_start_x-50, guess_start_x+100)
        if xe_1 - xs_1 < 99:
            break
        xs = xs_1
        xe = xe_1
        guess_start_100x100_y-=1
    print(f'Found a better fitting spot at {guess_start_100x100_y} from x: {xs} - {xe}')

    for y in range(guess_start_100x100_y, guess_start_100x100_y+100, 99):
        print (f'{y:5}:', end='')
        for x in range(xe+10):
            print(probe(x,y), end = '')
        print()

    print(f'Answer: {xs*10000 + guess_start_100x100_y}')
