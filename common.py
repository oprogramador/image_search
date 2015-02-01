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
import PIL
from PIL import Image

def toRGB(im):
    if not isinstance(im, PIL.JpegImagePlugin.JpegImageFile):
       im.convert('RGB').save('kivZLnBtzDeh1EO0DKk9.jpg', 'JPEG') 
       im = Image.open('kivZLnBtzDeh1EO0DKk9.jpg')
       os.remove('kivZLnBtzDeh1EO0DKk9.jpg')
       return im
    return im

def histogram(im):
    #define three primary colors
    red = [0.0]*256
    green = [0.0]*256
    blue = [0.0]*256
    
    #define image field X * Y
    count = im.size[0] * im.size[1]
    
    #load image array
    pix = im.load()
    
    #calcualte histogram
    for x in xrange(im.size[0]):
        for y in xrange(im.size[1]):
            if(type(pix[x,y])==int):
                print 'type='+str(pix[x,y])
            red[pix[x,y][0]] += 1
            green[pix[x,y][1]] += 1
            blue[pix[x,y][2]] += 1
    red = map(lambda x: x/count, red)
    green = map(lambda x: x/count, green)
    blue = map(lambda x: x/count, blue)
    return (red, green, blue)


def pix_diff(a,b):
    return (1.0*(a[0]-b[0])/256)**2 + (1.0*(a[1]-b[1])/256)**2 + (1.0*(a[2]-b[2])/256)**2

def rand_vector(x,y):
    return random.random()*x, random.random()*y

def distance(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)*0.5

def add_vec(a,b):
    return a[0]+b[0], a[1]+b[1]

def gradient(a):
    n = 10000
    d = 0
    pix = a.load()
    for i in xrange(n):
        v1 = rand_vector(a.size[0], a.size[1])
        v2 = add_vec(v1, rand_vector(a.size[0]*0.02, a.size[1]*0.02))
        try:
            d += pix_diff(pix[v1], pix[v2]) / distance(v1, v2)
        except:
            pass
    return d/n
