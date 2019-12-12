
class Moon:
    def __init__(self, string):
        self.pos = list(map(lambda c: int(c.split('=')[1]), string.strip(' <>\n').split(',')))
        self.vel = [0, 0, 0]

    def __repr__(self):
        return f'{self.pos} {self.vel}'

    def coord_hash(self, coord):
        yield self.pos[coord]
        yield self.vel[coord]

    def energy(self):
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))

if __name__ == '__main__':
    with open("input_day12-3.txt", "r") as input_file:
        moons = list(map(Moon, input_file.readlines()))

        print(moons)
        states = [list(), list(), list()]

        for step in range (1, 4686774924):
            # Update for gravity
            for coord in range(3):
                #sorted_moons = sorted(moons, key=lambda m: m.pos[coord])
                for moon in moons:
                    moon.vel[coord] -= sum(1 for m in moons if m.pos[coord] < moon.pos[coord])
                    moon.vel[coord] += sum(1 for m in moons if m.pos[coord] > moon.pos[coord])

            # Update for velocity
            for moon in moons:
                for coord in range(3):
                    moon.pos[coord] += moon.vel[coord]

            for coord in range(3):
                state = hash(tuple(m.coord_hash(coord) for m in moons))
                if state in states:
                    print ("----------     Found a repeat for coord {coord} at {step}   -------------")
                states[coord].append(state)

            if step %10000 == 0:
                print('Step: ', step, 'Moons: ')
                for m in moons:
                    print (m)

                print("Total energy", sum(map(lambda m: m.energy(), moons)))
