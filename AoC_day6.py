


class SpaceObject:
    def __init__(self, name: str, orbiting_this: str = None):
        self.name = name
        if orbiting_this:
            self.orbiting_this = [orbiting_this]
        else:
            self.orbiting_this = list()
        self.orbits = None

    def __repr__(self):
        return f"{self.orbits} <- {self.name}: {self.orbiting_this}"


def count_indirect_orbits(space_object_name: str, depth: int) -> int:
    if space_object_name not in tree:
        return depth
    else:
        sub_count = 0
        for sub_object in tree[space_object_name].orbiting_this:
            sub_count += count_indirect_orbits(sub_object, depth + 1)
        return sub_count + depth


with open("input_day6.txt", "r") as input_file:
    orbits = list(map(lambda o: o.strip(" \n").split(")"), input_file.readlines()))

#orbits = list(map(lambda o: o.strip(" \n").split(")"), "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L".split(" ")))
#orbits = list(map(lambda o: o.strip(" \n").split(")"), "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L K)YOU I)SAN".split(" ")))

print(orbits)

tree = dict()

for orbit in orbits:
    if orbit[0] in tree:
        tree[orbit[0]].orbiting_this.append(orbit[1])
    else:
        tree[orbit[0]] = SpaceObject(orbit[0], orbit[1])
    if orbit[1] not in tree:
        tree[orbit[1]] = SpaceObject(orbit[1])
    tree[orbit[1]].orbits = orbit[0]
print(tree)

print("Indirect orbits from COM: ", count_indirect_orbits("COM", 0))


upstream_YOU = list()
upstream_SAN = list()
node_YOU = "YOU"
node_SAN = "SAN"

while node_SAN != "COM" or node_YOU != "COM":
    if tree[node_SAN].orbits:
        node_SAN = tree[node_SAN].orbits
        upstream_SAN.append(node_SAN)

    if tree[node_YOU].orbits:
        node_YOU = tree[node_YOU].orbits
        upstream_YOU.append(node_YOU)
    else:
        if node_YOU != "COM":
            print("Surprise!")

    if set(upstream_YOU).intersection(upstream_SAN):
        print("Found a common node: ")
        print("Santa:", upstream_SAN)
        print("You:", upstream_YOU)

        if node_YOU in upstream_SAN:
            print(f"Common node: {node_YOU}, {upstream_SAN.index(node_YOU)} + {len(upstream_YOU)-1} = {upstream_SAN.index(node_YOU) + len(upstream_YOU)-1}")
        if node_SAN in upstream_YOU:
            print(f"Common node: {node_SAN}, {upstream_YOU.index(node_SAN)} + {len(upstream_SAN)-1} = {upstream_YOU.index(node_SAN) + len(upstream_SAN)-1}")

        break;

print("Santa:", node_SAN,  upstream_SAN)
print("You:", node_YOU, upstream_YOU)