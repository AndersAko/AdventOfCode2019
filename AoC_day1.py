
def fuel(mass):
    f = int(mass / 3) - 2
    if f > 0:
        return f + fuel(f)
    return 0

sum = 0
with open("input_day1.txt", "r") as input_file:
    for line in input_file:
        sum += fuel(int(line))

print(sum)
