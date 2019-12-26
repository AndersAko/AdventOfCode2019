import math

if __name__ == '__main__':
    with open("input_day22.txt", "r") as input_file:
        deal_instructions = [line.strip("\n").split(" ") for line in input_file.readlines()]

    deck_size = 10007
    find_position = 2020
    number_of_shuffles = 13
    deck = list(range(deck_size))
    for i in range(1, number_of_shuffles+1):
        for instruction in deal_instructions:
            #print(instruction)
            if instruction[0] == 'deal' and instruction[1] == 'into':
                new_deck = list(reversed(deck))
            elif instruction[0] == 'cut':
                cut_cards = int(instruction[1]) % deck_size
                new_deck = deck[cut_cards:] + deck[:cut_cards]
            elif instruction[0] == 'deal' and instruction[2] == 'increment':
                increment = int(instruction[3])
                new_deck = [None] * deck_size
                for ix in range(deck_size):
                    new_deck[(ix * increment) % deck_size] = deck[ix]
            else:
                print('Not implemented instruction', instruction)
            deck = new_deck

        pos_2019 = deck.index(2019)
        print(f'After shuffle {i}: Card no 2019 is at position: {pos_2019} {deck[pos_2019]} and position {find_position} contains card {deck[find_position]}')

    position = find_position

    deck_size = 119315717514047

    # from_position = position * const_a + const_b
    const_a = 1
    const_b = 0
    for instruction in reversed(deal_instructions):
        #print(instruction)
        if instruction[0] == 'deal' and instruction[1] == 'into':
            from_position = (-position - 1)
            a = -1
            b = -1
        elif instruction[0] == 'cut':
            cut_cards = int(instruction[1]) % deck_size
            from_position = position + cut_cards
            a = 1
            b = cut_cards
        elif instruction[0] == 'deal' and instruction[2] == 'increment':
            increment = int(instruction[3])
            inverse = 0
            from_position = position * pow(increment, deck_size - 2, deck_size)
            a = pow(increment, deck_size - 2, deck_size)
            b = 0
        else:
            print('Not implemented instruction', instruction)
        position = from_position % deck_size
        const_a = const_a * a % deck_size
        const_b = (a * const_b + b) % deck_size

    print(f'Position {find_position} has card {position}, aka { (find_position * const_a + const_b) % deck_size }')
    print(f'const_a: {const_a}, const_b: {const_b}')

    a = const_a
    b = const_b
    for i in range(1, number_of_shuffles + 1):
        print(f'Calculated shuffle {i}:  Position {find_position} has card {(find_position * a + b) % deck_size}')
        a = a * const_a % deck_size
        b = (const_a * b + const_b) % deck_size

    factors = []
    a = const_a
    b = const_b
    for exponent in range(50):
        factors.append((a, b))
        print(f'Factors {exponent}:  Position {find_position} has card {(find_position * a + b) % deck_size}')
        b = (a * b + b) % deck_size
        a = (a * a) % deck_size

    number_of_shuffles = 101741582076661
    position = find_position
    a = 1
    b = 0
    while number_of_shuffles > 0:
        exponent = int(math.log2(number_of_shuffles))
        a = a * factors[exponent][0] % deck_size
        b = factors[exponent][0] * b + factors[exponent][1]
        card = (find_position * a + b) % deck_size
        number_of_shuffles -= 2 ** exponent
        print(f'Applied: 2^{exponent}={2**exponent}, {number_of_shuffles} remains. Card at {find_position} = {card}')
