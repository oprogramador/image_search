########################################
#
# Author: Piotr Sroczkowski
#
########################################

import os
import sys
import random

from skimage import data, img_as_float
from skimage import exposure
from PIL import Image

def histogram(im):
    red = [0.0]*256
    green = [0.0]*256
    blue = [0.0]*256
    count = im.size[0] * im.size[1]
    pix = im.load()
    for x in xrange(im.size[0]):
        for y in xrange(im.size[1]):
            red[pix[x,y][0]] += 1
            green[pix[x,y][1]] += 1
            blue[pix[x,y][2]] += 1
    red = map(lambda x: x/count, red)
    green = map(lambda x: x/count, green)
    blue = map(lambda x: x/count, blue)
    return (red, green, blue)


def pix_diff(a,b):
    return (1.0*(a[0]-b[0])/256)**2 + (1.0*(a[1]-b[1])/256)**2 + (1.0*(a[2]-b[2])/256)**2
