Should be self-explanatory what this python code does.

Look at the example input image: test.png
Look at the example output image: test_cropped.png

This is how the example output image was generated:

$ python Driver.py -i test.png -o test_cropped.png --h1=0.08 --v1=0.05 -v

Input file: test.png
Output file: test_cropped.png
h1: 0.080000
h2: 0.080000
v1: 0.050000
v2: 0.050000

Is this correct? (y/n): y

Processing...
Image (test.png) (width, height) : (922, 684)
Amount to crop from left: 73
Amount to crop from right: 73
Amount to crop from top: 34
Amount to crop from bottom: 34
Proposed crop region: (73, 34, 848, 649)
Cropped image (test_cropped.png) (width, height) : (775, 615)



