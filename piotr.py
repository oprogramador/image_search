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

compare_histo = common.make_compare_any( common.histogram )
compare_histo_rand = common.make_compare_any( common.histogram_rand )
compare_direction = common.make_compare_any( common.direction )
by_magick = common.make_compare_any( common.magick )

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

def parts_with_move(a,b):
    diff = 0
    pixa = a.load()
    pixb = b.load()
    n = 10000
    for i in xrange(n):
        x = random.random()
        y = random.random()
        xb = x+random.random()*0.1
        yb = y+random.random()*0.1
        try:
            diff += common.pix_diff(pixa[int(x*a.size[0]), int(y*a.size[1])], pixb[int(xb*b.size[0]), int(yb*b.size[1])])
        except:
            pass
    return diff/n

def compare_small(a,b):
    size = (8,8)
    return compare_histo(a.resize(size, Image.ANTIALIAS), b.resize(size, Image.ANTIALIAS))

def function_creator(n):
    def f(a,b):
        a = common.toRGB(a.convert('P', palette=Image.ADAPTIVE, colors=n))
        b = common.toRGB(b.convert('P', palette=Image.ADAPTIVE, colors=n))
        return compare_parts(a, b)
    return f

def by_gradient(a,b):
    return abs(common.gradient(a) - common.gradient(b))
