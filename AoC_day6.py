def count_indirect_orbits(space_object: str, depth: int) -> int:
    if space_object not in tree:
        return depth
    else:
        sub_count = 0
        for sub_object in tree[space_object]:
            sub_count += count_indirect_orbits(sub_object, depth + 1)
        return sub_count

with open("input_day6.txt", "r") as input_file:
    orbits = list(map(lambda o: o.strip(" \n").split(")"), input_file.readlines()))

orbits = list(map(lambda o: o.strip(" \n").split(")"), """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".split("\n")))

print(orbits)

tree = dict()

for orbit in orbits:
    if orbit[0] in tree:
        tree[orbit[0]].append(orbit[1])
    else:
        tree[orbit[0]] = [orbit[1]]

print(tree)

print(count_indirect_orbits(orbits[0][0], 0))
