import os
import sys
import random

from PIL import Image

import common

# comparison of histogram
compare_histo = common.make_compare_any( common.histogram )

# comparison of histogram with reduced number of considerated pixels
compare_histo_rand = common.make_compare_any( common.histogram_rand )

# comparison of direction of similar neighbour pixels
compare_direction = common.make_compare_any( common.direction )

# comparison of pixels modulo values
by_magick = common.make_compare_any( common.magick )

# comparison of gradient
def by_gradient(a,b):
    a,b = common.MyImage.to_images((a,b))
    return abs(common.gradient(a) - common.gradient(b))

# comparison of count of pixels withing edges
def by_edges_count(a,b):
    return abs(common.edges_count(a) - common.edges_count(b))

# comparison of edges direction
def by_edges_direction(a,b):
    return abs(common.edges_direction(a) - common.edges_direction(b))

# comparison of image parts
def compare_parts(a,b):
    pixa = a.load()
    pixb = b.load()
    a,b = common.MyImage.to_images((a,b))
    diff = 0
    n = 10000
    for i in xrange(n):
        x = random.random()
        y = random.random()
        diff += common.pix_diff(pixa[int(x*a.size[0]), int(y*a.size[1])], pixb[int(x*b.size[0]), int(y*b.size[1])]) 
    return diff/n

# comparison with moving
def parts_with_move(a,b):
    diff = 0
    pixa = a.load()
    pixb = b.load()
    a,b = common.MyImage.to_images((a,b))
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

# comparison of scaled small images
def compare_small(a,b):
    a,b = common.MyImage.to_images((a,b))
    size = (8,8)
    return compare_histo(a.resize(size, Image.ANTIALIAS), b.resize(size, Image.ANTIALIAS))

# comparison in reduced color palette
def function_creator(n):
    def f(a,b):
        a = a.convert('P', palette=Image.ADAPTIVE, colors=n).toRGB()
        b = b.convert('P', palette=Image.ADAPTIVE, colors=n).toRGB()
        return compare_parts(a, b)
    return f
