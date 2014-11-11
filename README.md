#jpglitch

A command line tool to create glitchart from jp[e]g's. The script will save the
glitched *image.jpg* as *image_glitched.png*. The reason to save the result as
png is for stability and to make sure the result looks the same on different
platforms. 

It uses elements of this javascript implementation.
https://github.com/snorpey/glitch-canvas/

##Usage
``
python jpglitch.py image.jpg
``

There are a few optional parameters
1. -a, --amount: This determines the hex value that is used to overwrite original
values in the image data. Value from 1 to 99
1. -s --seed: This determines where in the image data the script starts overwriting
data. Value from 1 to 99
1. -i, --iterations: This determines how many times the script overwrites data. Value
from 1-115
1. --jpg: Normally the script will output to .png for stablity. We're pretty
much corrupting files and unstabe jpegs are rendered differently by different
platforms/browsers. Png is more stable, but you might want to keep doing stuff
to it so use this if you want a jpeg.
1. -o, --output: Specify the output filename. Defaults to
originalname_glitched.extension

When the optional parameters are not given it generates random values in the
allowed ranges. This is closer to the original purpose. Glitches are
technically not engineered but they just happen. 

``
python jpglitch.py image.jpg -a 70 -s 4 -i 31
``

##Example
![alt text](http://imgur.com/bUvNMaQ.jpg "example")`
