def route_to_points(input):
    directions = input.strip().split(",")
    loc = (0, 0)
    steps = 0
    points = list()

    for direction in directions:
        dist = int(direction[1:])
        for l in range(0, dist):
            steps += 1
            if direction[0] == "U":
                loc = (loc[0], loc[1] + 1)
            elif direction[0] == "D":
                loc = (loc[0], loc[1] - 1)
            elif direction[0] == "L":
                loc = (loc[0] - 1, loc[1])
            elif direction[0] == "R":
                loc = (loc[0] + 1, loc[1])
            else:
                print("Parsing error for", direction)
            points.append((loc[0], loc[1], steps))
    return points


def min_manhattan(intersections):
    min_p = intersections[0]
    for i in intersections:
        if abs(i[0]) + abs(i[1]) < abs(min_p[0]) + abs(min_p[1]):
            min_p = i

    return min_p[0] + min_p[1]


def min_steps(intersections):
    min_p = intersections[0]
    for i in intersections:
        if  i[2] < min_p[2]:
            min_p = i

    return min_p


with open("input_day3.txt", "r") as input_file:
    wire1 = input_file.readline()
    wire2 = input_file.readline()

#wire1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
#wire2 = "U62,R66,U55,R34,D71,R55,D58,R83"
#wire1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
#wire2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

#wire1 = "R8,U5,L5,D3"
#wire2 = "U7,R6,D4,L4"

print(wire1)
print(route_to_points(wire1))
print(wire2)
print(route_to_points(wire2))


p1 = route_to_points(wire1)
p2 = route_to_points(wire2)

intersections = set([(p[0], p[1]) for p in p1]).intersection([(p[0], p[1]) for p in p2])
p1 = [p for p in p1 if (p[0], p[1]) in intersections]
p2 = [p for p in p2 if (p[0], p[1]) in intersections]

print (p1, p2)

intersections = list()

for i in p1:
    matching = [x for x in p2 if x[0] == i[0] and x[1] == i[1]]
    if len(matching) > 1:
        print("multiple matches", matching)

    if matching:
        print("Intersect:", i, matching[0])
        intersections.append((i[0], i[1], i[2] + matching[0][2]))

# intersections = list(set(route_to_points(wire1)).intersection(route_to_points(wire2)))

print("Intersections: ", intersections)
print("Compare with ", list(set(route_to_points(wire1)).intersection(route_to_points(wire2))))

print("Shortest steps: ", min_steps(intersections)[2])
#    print(wire2)
