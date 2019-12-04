
def has_double(number):
    while number > 10:
        if int(number % 10) == int((number / 10) % 10):
            if int((number/100) % 10) == int((number/10) % 10):
                while int((number/100) % 10) == int((number/10) % 10) and number >= 100:
                    number /= 10
            else:
                return True
        number /= 10
    return False


def increases(number):
    for digit in range(5):
        if int((number % 100) /10) > int(number % 10):
            return False
        number /= 10
    return True


min_range = 240920
max_range = 789857
count = 0

for number in range (min_range, max_range +1):
    if has_double(number) and increases(number):
        print(number)
        count += 1

print ("A total number of ", count, "passwords are possible")
