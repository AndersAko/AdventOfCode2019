import numpy
import math

def hits_asteroid(origin, dir):
    debug = False
    if debug:
        print (f"Hitcheck {origin} {dir}", end = '')
    ray = [sum(x) for x in zip(origin, dir)]
    while 0 <= ray[0] < size[0] and 0 <= ray[1] < size[1]:
        if asteroids[ray[0]][ray[1]] == 1:
            if debug:
                print(f" X at {ray}")
            return ray
        ray = [sum(x) for x in zip(ray, dir)]
    if debug:
        print()
    return None

if __name__ == '__main__':
    with open("input_day10.txt", "r") as input_file:
        asteroids = list()
        for line in input_file.readlines():
            asteroids.append(list(map(lambda x: 1 if x =='#' else 0, line.strip(" \n"))))

    size = (len(asteroids), len(asteroids[0]))
    print(size, asteroids)

    hit_array = numpy.zeros(size, dtype=int)
    for x in range(size[1]):
        for y in range(size[0]):
            if asteroids[y][x] != 1:
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

    print(hit_array)
    best = 0
    for x in range(size[1]):
        for y in range(size[0]):
           if hit_array[y][x] > best:
               best = hit_array[y][x]
               best_spot = (y,x)

    print (f"Best spot: {best_spot}yx with {best} visible")

    rays = sorted(filter(lambda z: z[0]!=0 or z[1]!= 0,[(y, x) for y in range(-size[1]-1, size[1]+1) for x in range(-size[1]-1, size[1]+1) ]),
                  key=lambda a: (math.pi/2 + numpy.arctan2(a[0], a[1]))%(2*math.pi))

    hit_asteroid = []
    print(asteroids, hit_asteroid)
    for turn in range(10):
        for ray in rays:
            if math.gcd(ray[0], ray[1]) == 1:
                print (f"Ray from {best_spot} to {[sum(x) for x in zip(best_spot, ray)]} = {ray}", end = '')
                hit = hits_asteroid(best_spot, ray)
                if hit:
                    hit_asteroid.append(hit)
                    asteroids[hit[0]][hit[1]] = 2
                    print (hit)
                else:
                    print()
        print(asteroids, hit_asteroid)

    print (hit_asteroid)
    print (hit_asteroid[0:3], hit_asteroid[9], hit_asteroid[19], hit_asteroid[49], hit_asteroid[99], hit_asteroid[198], hit_asteroid[199], hit_asteroid[200])
    print (len (hit_asteroid))
    print (hit_asteroid[199])