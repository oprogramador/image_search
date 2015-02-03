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

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

import common
<<<<<<< HEAD
=======


    
>>>>>>> fa4b718cc1d6ccc6b23cf1290cb415028e1f164b
    
def compare_histo(x,y):
    #diff - difference between two images
    diff = 0

    #load histograms of 2 images
    xhis = common.histogram(x)
    yhis = common.histogram(y)

    #calculate difference using intersection method
    for i in xrange(256):
        diff += min(xhis[0][i],yhis[0][i]) + min(xhis[1][i],yhis[1][i]) + min(xhis[2][i],yhis[2][i])
    return 3 - diff
