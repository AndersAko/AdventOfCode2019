from functools import reduce


def fuel(mass):
    f = int(mass / 3) - 2
    if f > 0:
        return f + fuel(f)
    return 0

sum_part2 = 0
with open("input_day1.txt", "r") as input_file:
    for line in input_file:
        sum_part2 += fuel(int(line))

print(sum_part2)

with open("input_day1.txt", "r") as input_file:
    sum_part1 = reduce(lambda x, y: x + int(y.strip(' \n'))//3-2, input_file.readlines(), 0)


print(sum_part1)
