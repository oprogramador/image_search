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

import common

def compare_histo(x,y):
    diff = 0
    xhis = common.histogram(x)
    yhis = common.histogram(y)
    for i in xrange(256):
        diff += (xhis[0][i] - yhis[0][i])**2 + (xhis[1][i] - yhis[1][i])**2 + (xhis[2][i] - yhis[2][i])**2 
    return diff

def compare_parts(a,b):
    diff = 0
    pixa = a.load()
    pixb = b.load()
    n = 10000
    for i in xrange(n):
        x = random.random()
        y = random.random()
        diff += common.pix_diff(pixa[int(x*a.size[0]), int(y*a.size[1])], pixb[int(x*b.size[0]), int(y*b.size[1])]) 
    return diff/n
