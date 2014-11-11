import io
import copy
import random
import click

from PIL import Image


class Jpeg(object):

    def __init__(self, image_bytes, amount, seed, iterations):
        self.bytes = image_bytes
        self.new_bytes = None
        self.header_length = self.get_header_length()
        self.parameters = {
            'amount': amount,
            'seed': seed,
            'iterations': iterations
        }

        self.glitch_bytes()

    def get_header_length(self):
        """Get the length of the header by searching sequential 0xFF 0xDA
        values. These values mark the end of a Jpeg header. We add two to give
        us a little leeway. We don't want to mess with the header.
        """

        for i in (xrange(len(self.bytes)-1)):
            if (self.bytes[i] == 255) & (self.bytes[i+1] == 218):
                result = i + 2
                break

        return result

    def glitch_bytes(self):
        """Glitch the image bytes, after the header based on the parameters.
        'Amount' is the hex value that will be written into the file. 'Seed'
        tweaks the index where the value will be inserted, rather than just a
        simple division by iterations. 'Iterations' should be self explanatory
        """

        amount = self.parameters['amount'] / 100
        seed = self.parameters['seed'] / 100
        iterations = self.parameters['iterations']

        # work with a copy of the original bytes. We might need the original
        # bytes around if we glitch it so much we break the file.
        new_bytes = copy.copy(self.bytes)

        for i in (xrange(iterations)):
            max_index = len(self.bytes) - self.header_length - 4

            # The following operations determine where we'll overwrite a value
            # Illustrate by example

            # 36 = (600 / 50) * 3
            px_min = int((max_index / iterations) * i)

            # 48 = (600 / 50) * 3 + 1
            px_max = int((max_index / iterations) * (i + 1))

            # 12 = 48 - 36
            delta = (px_max - px_min)  # * 0.8

            # 36 + (12 * 0.8)
            px_i = int(px_min + (delta * seed))

            # If the index to be changed is beyond bytearray length file set
            # it to the max index
            if (px_i > max_index):
                px_i = max_index

            byte_index = self.header_length + px_i
            new_bytes[byte_index] = int(amount * 256)

        self.new_bytes = new_bytes

    def save_image(self, name):
        """Save the image to a file. Keep trying by re-glitching the image with
        less iterations if it fails
        """

        while True:
            try:
                stream = io.BytesIO(self.new_bytes)
                im = Image.open(stream)
                im.save(name)
                break
            except IOError:
                self.parameters['iterations'] -= 1
                self.glitch_bytes()


@click.command()
@click.option('--amount', '-a', type=click.IntRange(0, 99, clamp=True),
              default=random.randint(0, 99), help="Insert high or low values?")
@click.option('--seed', '-s', type=click.IntRange(0, 99, clamp=True),
              default=random.randint(0, 99), help="Begin glitching at the\
                      start on a bit later on")
@click.option('--iterations', '-i', type=click.IntRange(0, 115, clamp=True),
              default=random.randint(0, 115), help="How many values should\
                      get replaced")
@click.option('--jpg', is_flag=True, help="Output to jpg instead of png.\
                      Note that png is more stable")
@click.option('--output', '-o')
@click.argument('image', type=click.File('rb'))
def cli(image, amount, seed, iterations, jpg):
    image_bytes = bytearray(image.read())
    jpeg = Jpeg(image_bytes, amount, seed, iterations)

    click.echo("\nScrambling your image with the following parameters:")
    for key, value in jpeg.parameters.iteritems():
        click.echo(message=key + ': ' + str(value))

    name = image.name.rsplit('.')[0] + "_glitched%s" % ('.jpg' if jpg
                                                        else '.png')
    jpeg.save_image(name)

    output = "\nSucces! Checkout %s." % name
    click.echo(output)
