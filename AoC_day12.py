
class Moon:
    def __init__(self, string):
        self.pos = list(map(lambda c: int(c.split('=')[1]), string.strip(' <>\n').split(',')))
        self.vel = [0, 0, 0]

    def __repr__(self):
        return f'{self.pos} {self.vel}'

    def energy(self):
        return sum(map(abs, self.pos)) + sum(map(abs, self.vel))

if __name__ == '__main__':
    with open("input_day12-1.txt", "r") as input_file:
        moons = list(map(Moon, input_file.readlines()))

        print(moons)

        for step in range (1, 101):
            # Update for gravity
            for coord in range(3):
                sorted_moons = sorted(moons, key=lambda m: m.pos[coord])
                for moon_ix, moon in enumerate(sorted_moons):
                    same_ix = 0
                    while moon_ix-same_ix-1 > 0 and sorted_moons[moon_ix-same_ix-1].pos[coord] == moon.pos[coord]:
                        same_ix += 1
                    # print(f'Moon {moon_ix}: {moon} greater than {moon_ix-same_ix} other moons on coord {coord}')

                    moon.vel[coord] -= moon_ix - same_ix

                    same_ix = 0
                    while moon_ix+same_ix+1 < len(sorted_moons) and sorted_moons[moon_ix+same_ix+1].pos[coord] == moon.pos[coord]:
                        same_ix += 1
                    # print(f'Moon {moon_ix}: {moon} less than {len(sorted_moons)-moon_ix-1-same_ix} other moons on coord {coord}')

                    moon.vel[coord] += len(sorted_moons)-moon_ix-1-same_ix

            # Update for velocity
            for moon in moons:
                for coord in range(3):
                    moon.pos[coord] += moon.vel[coord]

            print('Step: ', step, 'Moons: ', moons)
            print("Total energy", sum(map(lambda m: m.energy(), moons)))
