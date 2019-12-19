import intcode
import threading

if __name__ == '__main__':
    with open("input_day19.txt", "r") as input_file:
        program_code = list(map(int, input_file.readline().strip(" ").split(",")))

    program = intcode.Program(0, program_code)

    affected = 0
    start_beam_20 = 0
    start_beam_40 = 0
    for y in range(50):
        for x in range(50):
            program = intcode.Program(0, program_code)
            program.input.put(x)
            program.input.put(y)
            program.run()
            pull = program.output.get()
            if pull == 1:
                affected += 1
                if y == 20:
                    end_beam_20 = x
                    if start_beam_20 == 0:
                        start_beam_20 = x
                if y == 40:
                    end_beam_40 = x
                    if start_beam_40 == 0:
                        start_beam_40 = x

            print(pull, end = '')
        print()

    print(f'{affected} squares affected within closest 50x50')
    print(f'Beam 20: {start_beam_20}, {end_beam_20}')
    print(f'Beam 40: {start_beam_40}, {end_beam_40}')

    slope_start = (start_beam_40 - start_beam_20)/20
    slope_end = (end_beam_40 - end_beam_20)/20
    print(f'Slope start: {slope_start} end: {slope_end}')

    fit_100x100_y = int(100*(slope_start+1) / (slope_end - slope_start))
    print(fit_100x100_y)
    for y in range(fit_100x100_y, fit_100x100_y+5):
        print (y, ':', end='')
        for x in range(fit_100x100_y+150):
            program = intcode.Program(0, program_code)
            program.input.put(x)
            program.input.put(y)
            program.run()
            pull = program.output.get()
            print(pull, end = '')
        print()
    for y in range(fit_100x100_y+95, fit_100x100_y+100):
        print (y, ':', end='')
        for x in range(fit_100x100_y+150):
            program = intcode.Program(0, program_code)
            program.input.put(x)
            program.input.put(y)
            program.run()
            pull = program.output.get()
            print(pull, end = '')
        print()
