import math

from collections import namedtuple, defaultdict

Reaction = namedtuple('Reaction', 'input output')
MaterialAmount = namedtuple('MaterialAmount', 'mtrl amt')

class State:
    def __init__(self, state):
        self.state = state

    def solve_problems(self):
        new_state  = self.state.copy()
        for reaction in reactions:
            if self.state[reaction.output.mtrl] < 0:
                num_reactions = math.ceil(-self.state[reaction.output.mtrl] / reaction.output.amt)
                for component in reaction.input:
                    new_state[component.mtrl] -= component.amt * num_reactions
                new_state[reaction.output.mtrl] += reaction.output.amt * num_reactions
        if self.state == new_state:
            return None
        else:
            return State(new_state)

    def __repr__(self):
        return f"State: {str(dict(self.state))}"

    def found_fuel(self):
        return self.state['FUEL'] != 0

    def only_need_ore(self):
        for mtrl, amt in self.state.items():
            if mtrl != 'ORE' and amt < 0:
                return False
        return True

if __name__ == '__main__':
    with open("input_day14.txt", "r") as input_file:
        reactions = []
        for line in input_file.readlines():
            inputs = list()
            parts = line.split('=>')
            for part_in in parts[0].split(','):
                mtrl = part_in.strip(' \n').split(' ')[1]
                amt = int(part_in.strip(' \n').split(' ')[0])
                inputs.append(MaterialAmount(mtrl, amt))
            mtrl = parts[1].strip(' \n').split(' ')[1]
            amt = int(parts[1].strip(' \n').split(' ')[0])
            reaction = Reaction(inputs, MaterialAmount(mtrl, amt))
            reactions.append(reaction)

    # Part 1
    state = State(defaultdict(int))         # material: amount
    state.state['FUEL'] = -1
    print(f'Starting state: {state} {state.only_need_ore()}')

    while not state.only_need_ore():
        state = state.solve_problems()

    ore_per_fuel = -state.state['ORE']
    print(f'part 1 -> {state}, \n  giving {ore_per_fuel} ore per fuel')

    # Part 2
    state = State(defaultdict(int))
    state.state['FUEL'] = -100
    while not state.only_need_ore():
        state = state.solve_problems()
    print(f' 100 fuel -> {state}\n   giving {-state.state["ORE"] / 100} ore per fuel')

    state = State(defaultdict(int))
    state.state['FUEL'] = -1000000
    while not state.only_need_ore():
        state = state.solve_problems()
    print(f' 1000000 fuel -> {state}\n   giving {-state.state["ORE"] / 1000000} ore per fuel')


    fuel = 1000000000000 // ore_per_fuel        # First approximation, assumed to be lower bound
    state = State(defaultdict(int))
    state.state['FUEL'] = -fuel
    print(f'Starting state: {state} {state.only_need_ore()}')

    while state.state['ORE'] > -1000000000000:
        while not state.only_need_ore():
            state = state.solve_problems()

        if state.state['ORE'] > -1000000000000:
            last_ok_state = State(state.state)
            last_ok_fuel = fuel
        ore_per_fuel = -state.state['ORE'] // fuel
        additional_fuel = (1000000000000+state.state['ORE']) // ore_per_fuel
        if additional_fuel == 0:
            break
        state.state['FUEL'] -= additional_fuel        # Try for more
        fuel += additional_fuel
        print(f'Got {fuel}, try for {additional_fuel } more fuel at: {state} {state.only_need_ore()}')

    # Incrementally last bit
    while state.state['ORE'] > -1000000000000:
        state.state['FUEL'] -= 1  # Try for one more
        fuel += 1
        while not state.only_need_ore():
            state = state.solve_problems()
        if state.state['ORE'] > -1000000000000:
            last_ok_state = State(state.state)
            last_ok_fuel = fuel

        print(f'Got {fuel}, try for 1 (ONE) more fuel at: {state} {state.only_need_ore()}')

    print(f'Last OK {last_ok_fuel}  {last_ok_state} ')
    print(f'Ore per fuel estimate: {ore_per_fuel}. Actual {-last_ok_state.state["ORE"]/ fuel}')


