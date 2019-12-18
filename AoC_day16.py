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


def FFT(x):
    result = []
    for digit in range(len(x)):
        digit = numpy.dot(x, patterns[digit][:len(x)])
        result.append(abs(digit) % 10)
    return result


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


def part1(input_list, length):
    for i in range(100):
        input_list = phase(input_list, length)
    return (input_list)


def part1_FFT(x):
    for i in range(100):
        x = FFT(x)
    return x


if __name__ == '__main__':
    with open("input_day16.txt", "r") as input_file:
        input_list = list(map(int, input_file.readline().strip(" ")))

    length = len(input_list)
    offset = int(''.join(map(str, input_list[:7])))
    print(offset, input_list)
    cProfile.run('part1(input_list, length)')

    result = part1(input_list, length)

    print(result)
    print("Result part 1: ", ''.join(map(str, result[:8])))


    patterns = []
    for i in range(length):
        patterns.append ([])
        for j in range(length):
            patterns[i].append(pattern[ ((j + 1) // (i + 1)) % len_pattern ])

    result = part1_FFT(input_list)
    print(result)
    print("Result part 1_FFT: ", ''.join(map(str, result[:8])))
    print(FFT(input_list))

    print('Odd and Even')
    X_even = part1_FFT(input_list[::2])
    X_odd = part1_FFT(input_list[1::2])
    print(X_even)
    print(X_odd)

    '''
    input_list = phase(input_list, length)
    for i in range(1):
        input_list = phase(input_list, length)
        print(i, input_list)

    print(input_list)
    print(f"Final result at offset {offset} = {''.join(map(str, input_list[offset:offset+8]))}")
    '''