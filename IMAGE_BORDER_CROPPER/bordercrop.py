import PIL
from PIL import Image
import cv2
import os
import numpy

# ANTICIPATED PACKAGE DEPENDENCIES (UBUNTU 14.04 LTS):
# imagemagick
# python-opencv

# WARNING: NO INPUT SANITIZATION PERFORMED OVER REQUIRED ARGS
#
# IN inputfile: input .png file
# IN OPTIONAL outputfile: output .png file (cropped version of input). If not provided, this shows a preview instead.
#
# The following arguments are expressed in % and should be between 0.0 (inclusive) and 0.5 (exclusive).
# IN x1_ratio: the "from left side" vertical cropping ratio
# IN x2_ratio: the "from right side" vertical cropping ratio
# IN y1_ratio: the "from top" horizontal cropping ratio
# IN y2_ratio: the "from bottom" horizontal cropping ratio
#
# IN verbose: verbose output
def DoWork(inputfile, outputfile, x1_ratio, x2_ratio, y1_ratio, y2_ratio, verbose):
    #if outputfile is None:
     #   outputfile = "%s_cropped.png"%(os.path.splitext(inputfile)[0])
    try:
        img = Image.open(open(inputfile))
    except IOError:
        print "Error: cannot identify image file: %s"%(inputfile)
        return False
    img_cv2 = cv2.imread(inputfile)
    img_rgb = img.convert('RGB')
    img_w, img_h = img.size
    if verbose:
        print "Image (%s) (width, height) : (%d, %d)"%(inputfile, img_w, img_h)

    x1_crop_amount = img_w * x1_ratio
    x2_crop_amount = img_w * x2_ratio
    y1_crop_amount = img_h * y1_ratio
    y2_crop_amount = img_h * y2_ratio
    x1 = int(x1_crop_amount)
    x2 = int(img_w - x2_crop_amount)
    y1 = int(y1_crop_amount)
    y2 = int(img_h - y2_crop_amount)

    if (x2 <= x1):
        print "Error: x coordinate cropping ratios are too large (reduce one or both of them): x1=%f x2=%f"%(x1_ratio, x2_ratio)
        return False
    if (y2 <= y1):
        print "Error: y coordinate cropping ratios are too large (reduce one or both of them): y1=%f y2=%f"%(y1_ratio, y2_ratio)
        return False
    bbox_4tuple = (x1, y1, x2, y2)
    if verbose:
        print "Amount to crop from left: %d"%(int(x1_crop_amount))
        print "Amount to crop from right: %d"%(int(x2_crop_amount))
        print "Amount to crop from top: %d"%(int(y1_crop_amount))
        print "Amount to crop from bottom: %d"%(int(y2_crop_amount))
        print "Proposed crop region: " + str(bbox_4tuple)
    try:
        img_cropped = img.crop(bbox_4tuple)
        img_cropped_w, img_cropped_h = img_cropped.size
        #img_cropped.save(outputfile)
    except:
        print "Error: cropping error"
        return False

    if verbose:
        s = ""
        if not outputfile is None:
            s = "(%s) "%(outputfile)
        print "Cropped image %s(width, height) : (%d, %d)"%(s, img_cropped_w, img_cropped_h) 

    if outputfile is None:
        preview_cv2 = cv2.cvtColor(numpy.array(img_cropped), cv2.COLOR_RGB2BGR)
        cv2.imshow("Original '%s'"%(inputfile), img_cv2)
        cv2.imshow("Cropped '%s' preview"%(inputfile), preview_cv2)
        cv2.waitKey(0) 
    else:
        img_cropped.save(outputfile)
 
    return True
    

