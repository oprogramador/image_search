import os
import sys
import random

import PIL
from PIL import Image
import cv2
import numpy as np

# image class
class MyImage:

    # constructor
    def __init__(self, fname):
       self._image = Image.open(fname) 
       self.pix = None
       self.name = fname
       self.properties = {}

    # inheritance from PIL.Image - pools
    def __getattr__(self, key):
        if key == '_image':
            raise AttributeErrror()
        else:
            try:
                return getattr(self, key)
            except:
                a = getattr(self._image, key)
                if not hasattr(a, '__call__'):
                    return a
                else:
                    return self.make_fun(key)
    
    # inheritance from PIL.Image - methods
    def make_fun(self, key):
        def f(*args, **kwargs):
            self.__image = getattr(self._image, key)(*args, **kwargs)
            return self
        return f

    # loading pixels only once
    def load(self):
        if self.pix == None:
            self.pix = self._image.load()
        return self._image.load()

    # conversion to RGB
    def toRGB(self):
        if not isinstance(self._image, PIL.JpegImagePlugin.JpegImageFile):
           self._image.convert('RGB').save('kivZLnBtzDeh1EO0DKk9.jpg', 'JPEG') 
           self._image = Image.open('kivZLnBtzDeh1EO0DKk9.jpg')
           os.remove('kivZLnBtzDeh1EO0DKk9.jpg')
        return self

    # scale large images
    def minimize(self):
        if self._image.size[0] * self._image.size[1] > 4096:
            self.image = self._image.resize((8,8), Image.ANTIALIAS)
        return self

    # get PIL.Image object for fastest availability
    def get_image(self):
        return self._image

    # conversion arguments to PIL.Image objects
    @staticmethod
    def to_images(tup):
        return map(lambda x: x.get_image() if x.__class__ == MyImage else x, tup)



# difference of arrays using smallest squares method
def cal_diff(a,b):
    d = 0
    for i in xrange(len(a)):
        if type(a[i]) == list:
            d += cal_diff(a[i], b[i])
        else:
            d += (a[i] - b[i])**2
    return d

# general difference of images with method f
def make_compare_any(f):
    def cmp(a,b):
        a,b = MyImage.to_images((a,b))
        return cal_diff(f(a), f(b))
    return cmp



# histogram
def histogram(im):
    #define three primary colors
    red = [0.0]*256
    green = [0.0]*256
    blue = [0.0]*256
    
    #define image field X * Y
    count = im.size[0] * im.size[1]
    
    #load image array
    pix = im.load()
    
    #calculate histogram
    for x in xrange(im.size[0]):
        for y in xrange(im.size[1]):
            red[pix[x,y][0]] += 1
            green[pix[x,y][1]] += 1
            blue[pix[x,y][2]] += 1
    red = map(lambda x: x/count, red)
    green = map(lambda x: x/count, green)
    blue = map(lambda x: x/count, blue)
    return (red, green, blue)

# histogram with random pixels
def histogram_rand(im):
    #define three primary colors
    red = [0.0]*256
    green = [0.0]*256
    blue = [0.0]*256
    
    #define image field X * Y
    count = im.size[0] * im.size[1]
    
    #load image array
    pix = im.load()
    
    #calculate histogram
    n = 10000
    for i in xrange(n):
        x = random.random()
        y = random.random()
        red[pix[x,y][0]] += 1
        green[pix[x,y][1]] += 1
        blue[pix[x,y][2]] += 1
    red = map(lambda x: x/count, red)
    green = map(lambda x: x/count, green)
    blue = map(lambda x: x/count, blue)
    return (red, green, blue)

# difference between pixels
def pix_diff(a,b):
    return (1.0*(a[0]-b[0])/256)**2 + (1.0*(a[1]-b[1])/256)**2 + (1.0*(a[2]-b[2])/256)**2

# random vector
def rand_vector(x,y):
    return random.random()*x, random.random()*y

# vector distance
def distance(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)*0.5

# vector addition
def add_vec(a,b):
    return a[0]+b[0], a[1]+b[1]

# gradient (difference between pixels at small distance from each other)
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

# direction of similar neighbour pixels
def direction(a):
    n = 10000
    res = [0.0, 0.0, 0.0, 0.0]
    pix = a.load()
    for i in xrange(n):
        v = rand_vector(a.size[0], a.size[1])
        try:
            down = pix_diff(pix[v], pix[add_vec(v, (0, 1))])
            up = pix_diff(pix[v], pix[add_vec(v, (0, -1))])
            left = pix_diff(pix[v], pix[add_vec(v, (-1, 0))])
            right = pix_diff(pix[v], pix[add_vec(v, (1, 0))])
            mi = min(down, up, left, right)
            if down==mi:
                res[0] += 1
            elif up==mi:
                res[1] += 1
            elif left==mi:
                res[2] += 1
            elif right==mi:
                res[3] += 1
        except:
            pass
    return map(lambda x: x/n, res)

# pixels modulo values
def magick(im):
    im = im.resize((16,16), Image.ANTIALIAS)
    pix = im.load()
    mag_nums = [2,3,7,23]
    res = [[0.0]*len(mag_nums)]*3
    for x in xrange(im.size[0]):
        for y in xrange(im.size[1]):
            for color in xrange(3):
                for i in xrange(len(mag_nums)):
                    res[color][i] += 1.0 * (pix[x,y][color] % mag_nums[i]) / mag_nums[i]
    return map(lambda a: map(lambda x: x/im.size[0]/im.size[1], a), res)

# count of pixels withing edges
def edges_count(im):
    if not hasattr(im, 'cv2'):
        im.cv2 = cv2.Canny(cv2.imread(im.name, 0), 128, 256)
    img = im.cv2
    s = 0.0
    for x in xrange(img.shape[0]):
       for y in xrange(img.shape[1]):
           if img[x,y] != 0:
               s += 1
    return s/img.size

# edges direction
def edges_direction(im):
    if not hasattr(im, 'cv2'):
        im.cv2 = cv2.Canny(cv2.imread(im.name, 0), 128, 256)
    img = im.cv2
    ver = 1.0
    hor = 1.0
    for x in xrange(img.shape[0]):
        for y in xrange(img.shape[1]):
            try:
                if img[x,y] != 0 and (img[x+1,y] != 0 or img[x-1,y] != 0):
                    hor += 1
                if img[x,y] != 0 and (img[x,y+1] != 0 or img[x,y-1] != 0):
                    ver += 1
            except:
                pass
    return hor/ver
