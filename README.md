# jpglitch

A command line tool to create glitchart from jp[e]g's. The script will save the glitched *image.jpg* as *image_glitched.png* bby default. The reason to save the result as png is for stability so the result looks the same on different platforms. 

It requires **zlib** and **libjpeg**. Refer to the original PIL readme for more
info. http://pillow.readthedocs.org/en/latest/original-readme.html

It uses elements of this javascript implementation.
https://github.com/snorpey/glitch-canvas/


## Installation
You should install it in a virtualenv by running `pip install
git+https://github.com/Kareeeeem/jpglitch` or by cloning the repo and running
`python setup.py install`.

## Usage

``
python jpglitch.py input.jpg
``

There are a few optional parameters

 Flag 	| Description
--------|------------
`-a`, `--amount`		| This determines the hex value that is used to overwrite original values in the image data. Value from 1 to 99
`-s`, `--seed`			| This determines where in the image data the script starts overwriting data. Value from 1 to 99
`-i`, `--iterations`	| This determines how many times the script overwrites data. Value from 1-115
`--jpg`					| Normally the script will output to .png for stablity. We're pretty much corrupting files and unstabe jpegs are rendered differently by different platforms/browsers. Png is more stable, but you might want to keep doing stuff to it so use this if you want a jpeg.
`-o`, `--output`		| Specify the output filename. Defaults to originalname_glitched.extension

When the optional parameters are not given it generates random values in the
allowed ranges. This is closer to the original purpose. Glitches are
technically not engineered but they just happen. 

``
python jpglitch.py -a 70 -s 4 -i 31 --jpg -o garbled_mess.jpg input.jpg 
``

## Example

![alt text](http://imgur.com/bUvNMaQ.jpg "example")`
