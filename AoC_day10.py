import numpy
import math

def hits_asteroid(origin, dir):
    debug = False
    if debug:
        print (f"Hitcheck {origin} {dir}", end = '')
    ray = [sum(x) for x in zip(origin, dir)]
    while 0 <= ray[0] < size[0] and 0 <= ray[1] < size[1]:
        if asteroids[ray[0]][ray[1]] == '#':
            if debug:
                print(f" X at {ray}")
            return True
        ray = [sum(x) for x in zip(ray, dir)]
    if debug:
        print()
    return False

def divisible (a, b):
    if abs(a) == 1 or abs(b) == 1:
        return False
    if a == 0:
        return True if b != 1 and b != -1 else False
    if b == 0:
        return True if a != 1 and a != -1 else False

    return a % b == 0 or b % a == 0

if __name__ == '__main__':
    with open("input_day10.txt", "r") as input_file:
        asteroids = list(map(lambda x : x.strip(" \n"), input_file.readlines()))

    size = (len(asteroids), len(asteroids[0]))
    print(size, asteroids)

    hit_array = numpy.zeros(size, dtype=int)
    for x in range(size[1]):
        for y in range(size[0]):
            if asteroids[y][x] != '#':
                continue
            hits = 0
            hit_list = []
            for dir_x in range(-size[1], size[1]):
                for dir_y in range(-size[0], size[0]):
                    if math.gcd(dir_x, dir_y) != 1:
                        continue
                    if hits_asteroid((y,x), (dir_y, dir_x)):
                        hits += 1

            hit_array[y][x] = hits

#    print(hit_array)
    best = 0
    for x in range(size[1]):
        for y in range(size[0]):
           if hit_array[y][x] > best:
               best = hit_array[y][x]
               best_spot = (x,y)

    print (f"Best spot: {best_spot} with {best} visible")