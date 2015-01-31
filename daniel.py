########################################
#
# Author: Daniel Mikulski
# Silesian University of Technology
#
########################################

import os
import sys
import random

from skimage import data, img_as_float
from skimage import exposure
from PIL import Image

import common

def compare_histo(x,y):
    #diff - difference between two images
    diff = 0

    #load histograms of 2 images
    xhis = histogram(x)
    yhis = histogram(y)

    #calculate difference using intersection method
    for i in xrange(256):
        diff+= min(xhis[0][i],yhis[0][i]) + min(xhis[1][i],yhis[1][i]) + min(xhis[2][i],yhis[2][i])
    return diff
