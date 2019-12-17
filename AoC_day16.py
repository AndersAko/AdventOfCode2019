import cProfile
import itertools
import numpy

pattern = [0, 1, 0, -1]
len_pattern = len(pattern)

def get_digit(input_pattern, length, digit_no, pattern_offset):      # Calculate input_pattern * (pattern ^ (digit_no+1) shifted pattern_offset)
    # digit_no = 0..length-1
    # length = length of input_pattern after repeats
    # pattern = len_pattern * digit_no
    # pattern_offset = offset into pattern
    digit = 0
    idx = 0
    for in_digit in itertools.islice(input_pattern, 0, length):
        next_digit = pattern[((idx + pattern_offset) // (digit_no+1)) % len_pattern] * in_digit
        digit += next_digit
        idx += 1

    digit = abs(digit)% 10
    return digit

def phase(input_list, length):
    output = []
    for out_digit in range(length):
        digit = 0
        idx = 0
        for in_digit in itertools.islice(input_list, 0, length):
            next_digit = pattern[((idx + 1) // (out_digit + 1)) % len_pattern] * in_digit
            digit += next_digit
            idx += 1

        digit = abs(digit) % 10
        output.append(digit)
#    print("Result: ", output)
    return output

def compress_list(input_list):
    result = list()
    for ix, _ in enumerate(input_list):
        if ix % 2 == 0:
            result.append(input_list[ix] + input_list[ix + 1])
    return result


def phase_part2(input_list, length):
    compressed_lists = [[0] + input_list]       # [0] = input_list, [1] = summed in pairs, [2] = summed in fours, etc
    for out_digit in range (length):
        pattern_start = out_digit + 1
        pattern_len = out_digit + 1     # Length of the '1' or '-1' series. Interval between 1-start and -1-start = 2 pattern_len
        pattern_period = pattern_len * 4
        while pattern_len > 0:
            longest_match = 


        if pattern_len == 1:
            digit = numpy.dot(compressed_lists[0],
                              list(itertools.islice(itertools.cycle(pattern), 0, len(compressed_lists[0]) + 1)))
        elif pattern_len == 2:
            compressed_lists[1] = compress_list(compressed_lists[0])
            digit = numpy.dot(compressed_lists[1],
                              list(itertools.islice(itertools.cycle(pattern), 0, len(compressed_lists[1]) + 1)))


def part1(input_list, length):
    for i in range(100):
        input_list = phase(input_list, length)
    return (input_list)

if __name__ == '__main__':
    with open("input_day16.txt", "r") as input_file:
        input_list = list(map(int, input_file.readline().strip(" ")))

    length = len(input_list)
    offset = int(''.join(map(str, input_list[:7])))
    print(offset, input_list)
    cProfile.run('part1(input_list, length)')

    input_list = part1(input_list, length)

    print(input_list)
    print("Result part 1: ", ''.join(map(str, input_list[:8])))

    length = 10000
    cProfile.run('phase(input_list, length)')

    input_list = phase(input_list, length)
    for i in range(1):
        input_list = phase(input_list, length)
        print(i, input_list)

    print(input_list)
    print(f"Final result at offset {offset} = {''.join(map(str, input_list[offset:offset+8]))}")
