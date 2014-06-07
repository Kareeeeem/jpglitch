import os
import random
from PIL import Image


def getBytes(image):
    with open(image, 'rb') as im:
        data = im.read()
        bytes = bytearray(data)
        return bytes


def getJpgHeaderLength(image_bytes):
    for i in (range(len(image_bytes)-1)):
        if (image_bytes[i] == 255) & (image_bytes[i+1] == 218):
            result = i
            break
    return result


def glitchJpgBytes(image, amount=None, seed=None, iterations=None):
    if amount is None:
        amount = random.randint(0, 99)
    elif amount > 99:
        amount = 99

    if seed is None:
        seed = random.randint(1, 99)
    elif seed > 99:
        seed = 99
    elif seed < 1:
        seed = 1

    if iterations is None:
        iterations = random.randint(1, 110)

    parameters = {'amount': amount, 'seed': seed, 'iterations': iterations}

    print parameters

    amount = float(amount)/100
    seed = float(seed)/100
    bytes = getBytes(image)
    headerlength = getJpgHeaderLength(bytes)

    for i in (range(iterations)):
        max_index = len(bytes) - headerlength - 4
        px_min = int((max_index / iterations) * i)
        px_max = int((max_index / iterations) * (i + 1))
        delta = (px_max - px_min) * 0.8
        px_i = int(px_min + (delta * seed))

        if (px_i > max_index):
            px_i = max_index

        byte_index = headerlength + px_i
        bytes[byte_index] = int(amount * 256.0)
    new_name = 'new_' + image
    new_name = image.rsplit('.')[0] + '_glitched.jpg'
    with open(new_name, 'wb') as output:
        output.write(bytes)

    return (new_name, image, parameters)


def savetoPNG(glitched_image):
    image = glitched_image[0]
    old_image = glitched_image[1]
    parameters = glitched_image[2]
    png_name = image.rsplit('.')[0] + '.png'

    while True:
        try:
            im = Image.open(image)
            im.save(png_name)
            os.remove(image)
            print 'succes'
            break
        except IOError:
            print 'oops'
            parameters['iterations'] -= 1
            second_attempt = (
                glitchJpgBytes(old_image,
                               amount=parameters['amount'],
                               seed=parameters['seed'],
                               iterations=(parameters['iterations'])))
            image = second_attempt[0]


def glitchJpg(image, amount=None, seed=None, iterations=None):
    glitched_image = glitchJpgBytes(image, amount, seed, iterations)
    savetoPNG(glitched_image)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("jpg", help="you need to provide a jpg image")
    parser.add_argument('-a', metavar="amount", type=int,
                        help="a number used to replace data in the image file. \
                        must be between 0 and 99")
    parser.add_argument('-s', metavar="seed", type=int,
                        help="a number used to determine which data gets replaced. \
                        Must be between 0 and 99")
    parser.add_argument('-i', metavar="iterations", type=int,
                        help="how many times over do you want to glitch the image. \
                        must be between 0 and 110")
    args = parser.parse_args()

    glitchJpg(args.jpg, amount=args.a, seed=args.s, iterations=args.i)
