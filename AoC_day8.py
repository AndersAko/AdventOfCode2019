import sys

def parse_layer(image:str):
    num_zeros = 0
    num_ones = 0
    num_twos = 0
    image_iter = iter(image)
    for x in range(25):
        for y in range(6):
            pixel = next(image_iter)
            if pixel == '0':
                num_zeros +=1
            elif pixel == '1':
                num_ones += 1
            elif pixel == '2':
                num_twos += 1
    return (num_zeros, num_ones*num_twos)



with open("input_day8.txt", "r") as input_file:
    image = input_file.readline()
#    image = "0222112222120000"
    width = 25
    height = 6
    layers = len(image)//(width * height)
    print(f"Image of len {len(image)}, with {layers} layers")

    for y in range(height):
        for x in range(width):
            pixel = ' '
            for layer in range(layers):
                ix = layer*(width*height) + y * width + x
                if image[ix] == '2':
                    continue
                else:
                    if image[ix] == '0':
                        pixel = 'X'
                    elif image[ix] == '1':
                        pixel = '-'
                    break
            print (pixel, end = '')
        print("")


