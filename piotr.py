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
compare_direction = common.make_compare_any( common.direction )

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
    return compare_histo(a.resize((8,8), Image.ANTIALIAS), b.resize((8,8), Image.ANTIALIAS))

def function_creator(n):
    def f(a,b):
        a = common.toRGB(a.convert('P', palette=Image.ADAPTIVE, colors=n))
        b = common.toRGB(b.convert('P', palette=Image.ADAPTIVE, colors=n))
        #b.convert('P', palette=Image.ADAPTIVE, colors=n).convert('RGBA').save('kivZLnBtzDeh1EO0DKk9_b.png')
        #a = Image.open('kivZLnBtzDeh1EO0DKk9_a.png')
        #b = Image.open('kivZLnBtzDeh1EO0DKk9_b.png')
        #os.remove('kivZLnBtzDeh1EO0DKk9_a.png')
        #os.remove('kivZLnBtzDeh1EO0DKk9_b.png')
        return compare_parts(a, b)
    return f

def by_gradient(a,b):
    return abs(common.gradient(a) - common.gradient(b))
