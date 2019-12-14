import math

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
    with open("input_day12.txt", "r") as input_file:
        moons = list(map(Moon, input_file.readlines()))

        print(moons)
        periods = [0,0,0,0]

        for coord in range(3):
            one_dimension_moon_pos = list(m.pos[coord] for m in moons)
            one_dimension_moon_vel = list(m.vel[coord] for m in moons)
            startposition = one_dimension_moon_pos + one_dimension_moon_vel
            step = 1
            while True:
                for moon_ix, moon in enumerate(one_dimension_moon_pos):
                    one_dimension_moon_vel[moon_ix] += sum(1 for m in one_dimension_moon_pos if m > moon) \
                            - sum(1 for m in one_dimension_moon_pos if m < moon)

                # Update for velocity
                for moon_ix in range(len(one_dimension_moon_pos)):
                    one_dimension_moon_pos[moon_ix] += one_dimension_moon_vel[moon_ix]

                if startposition == one_dimension_moon_pos + one_dimension_moon_vel:
                    print(f'Back to first state for coord {coord} at {step}: {one_dimension_moon_pos} {one_dimension_moon_vel}')
                    periods[coord] = step
                    break

                if step %100000 == 0 or step <10:
                    print(f'--{step}: {one_dimension_moon_pos} {one_dimension_moon_vel}')

                step += 1

        print(periods, periods[0]*periods[1]*periods[2])
        period_xy = periods[0]*periods[1] // math.gcd(periods[0], periods[1])
        period_xyz = period_xy*periods[2] / math.gcd(period_xy, periods[2])
        print(f'Combined period in xyz : {period_xyz}')
