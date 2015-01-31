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
import traceback

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from skimage import data, img_as_float
from skimage import exposure
from PIL import Image

import piotr
import daniel

def compare_general(x,y,ar):
    res = 1e-10
    for f in ar:
        res += 1/(f(x,y)+1e-10)
    return 1/res

def compare(x,y):
    return compare_general(x,y,[piotr.compare_histo, daniel.compare_histo, piotr.compare_parts])

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
        except IOError:
            print("\nAn Error catched:")
            print("BEGIN")
            print(traceback.format_exc())
            print("END\n")
    return sorted(res, key = lambda x: x[1])

print search(sys.argv[1], sys.argv[2])
