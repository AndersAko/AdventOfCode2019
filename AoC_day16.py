import cProfile
import itertools

pattern = [0, 1, 0, -1]
len_pattern = len(pattern)

def phase(input_list, length):
    output = []
    for out_digit in range(length):
        digit = 0
        idx = 0
        for in_digit in itertools.islice(input_list,length):
            next_digit = pattern[((idx+1)//(out_digit+1)) % len_pattern] * in_digit
            digit += next_digit
            idx += 1
        output.append(abs(digit) % 10)
#    print("Result: ", output)
    return output

def repeated_input(input_list):
    i = 0
    while True:
        yield input_list[i % len(input_list)]
        i += 1

if __name__ == '__main__':
    with open("input_day16.txt", "r") as input_file:
        input_list = list(map(int, input_file.readline().strip(" ")))

    length = len(input_list)
    offset = int(''.join(map(str, input_list[:7])))
    cProfile.run('phase(input_list, length)')

    input_list = phase(repeated_input(input_list), length)
    for i in range(99):
        input_list = phase(input_list, length)

    print(input_list)
    print("Final result ", ''.join(map(str, input_list[:8])))

