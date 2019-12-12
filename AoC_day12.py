
def pos_from_str(string):
    return list(map(lambda c: int(c.split('=')[1]), string.strip(' <>\n').split(',')))


if __name__ == '__main__':
    with open("input_day12-1.txt", "r") as input_file:
        moons = list(map(pos_from_str, input_file.readlines()))
        velocities = list()
        for moon in moons:
            velocities.append([0,0,0])

        print(moons)
        print(velocities)

        for step in range (1):
            # Update for gravity
            for coord in range(3):
                sorted_moons = sorted(moons, key =lambda m: m[coord])
                for moon_ix, moon in enumerate(sorted_moons):
                    same_ix = 0
                    while moon_ix-same_ix-1 > 0 and sorted_moons[moon_ix-same_ix-1][coord] == moon[coord]:
                        same_ix += 1
                    print(f'Moon {moon_ix}: {moon} greater than {moon_ix-same_ix} other moons on coord {coord}')

                    velocities[moon_ix][coord] -= moon_ix - same_ix

                    same_ix = 0
                    while moon_ix+same_ix+1 < len(sorted_moons) and sorted_moons[moon_ix+same_ix+1][coord] == moon[coord]:
                        same_ix += 1
                    print(f'Moon {moon_ix}: {moon} less than {len(sorted_moons)-moon_ix-1-same_ix} other moons on coord {coord}')

                    velocities[moon_ix][coord] += len(sorted_moons)-moon_ix-1-same_ix

            # Update for velocity
            for coord in range(3):
                for moon_ix, moon in enumerate(moons):
                    moons[moon_ix][coord] += velocities[moon_ix][coord]

            print('Moons: ', moons)
            print('Velocities: ', velocities)
