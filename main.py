########################################
#
# Author: Piotr Sroczkowski
#
########################################

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
    

im = Image.open("/home/pierre/Pictures/pict/kurz.jpg") #Can be many different formats.
im2 = Image.open("/home/pierre/Pictures/pict/sluj.jpg") #Can be many different formats.
im3 = Image.open("/home/pierre/Pictures/pict/nowi.jpg") #Can be many different formats.
im4 = Image.open("/home/pierre/Pictures/pict/zabk.jpg") #Can be many different formats.
im5 = Image.open("/home/pierre/Pictures/pict/drwa.jpg") #Can be many different formats.
im6 = Image.open("/home/pierre/Pictures/pict/kapcz.jpg") #Can be many different formats.
pix = im.load()
print im.size #Get the width and height of the image for iterating over
print pix[0,86]
#print histogram(im)
print compare_histo(im, im2)
print compare_histo(im, im3)
print compare_histo(im, im4)
print compare_histo(im, im5)
print compare_histo(im, im6)
