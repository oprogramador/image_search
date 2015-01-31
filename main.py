########################################
#
# Author: Piotr Sroczkowski
#
########################################

#
# first argument of the script is name of searched file
# seconde one is path to directory containing pictures
#

import os
import sys
import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

def compare_histo(x,y):
    diff = 0
    xhis = histogram(x)
    yhis = histogram(y)
    for i in xrange(256):
        diff += (xhis[0][i] - yhis[0][i])**2 + (xhis[1][i] - yhis[1][i])**2 + (xhis[2][i] - yhis[2][i])**2 
    return diff

def pix_diff(a,b):
    return (1.0*(a[0]-b[0])/256)**2 + (1.0*(a[1]-b[1])/256)**2 + (1.0*(a[2]-b[2])/256)**2

def compare_parts(a,b):
    diff = 0
    pixa = a.load()
    pixb = b.load()
    n = 10000
    for i in xrange(n):
        x = random.random()
        y = random.random()
        diff += pix_diff(pixa[int(x*a.size[0]), int(y*a.size[1])], pixb[int(x*b.size[0]), int(y*b.size[1])]) 
    return diff/n

def compare_general(x,y,ar):
    res = 1e-10
    for f in ar:
        res += 1/(f(x,y)+1e-10)
    return 1/res

def compare(x,y):
    return compare_general(x,y,[compare_histo, compare_parts])

def search(filename, dirname):
    res = []
    im = Image.open(filename)
    n = 1
    total = len(os.listdir(dirname))
    for i in os.listdir(dirname):
        try:
            res.append([i, compare(im, Image.open(dirname+'/'+i))])
            print 'compared '+str(n)+'/'+str(total)+' files'
            n += 1
        except:
            pass
    return sorted(res, key = lambda x: x[1])

print search(sys.argv[1], sys.argv[2])
