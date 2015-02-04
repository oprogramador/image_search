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
import json

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from skimage import data, img_as_float
from skimage import exposure
import PIL
from PIL import Image

import piotr
import daniel
import common

SMALL_VAL = 1e-10



def compare_general(x,y,ar):
    res = 1e-10
    for f in ar:
        res += 1/(correct(f(x,y))+SMALL_VAL)
    return 1/res

def compare(x,y):
    return compare_general(x,y,[
        #piotr.compare_histo,
        #daniel.compare_histo,
        piotr.compare_parts,        #OK
        #piotr.compare_small,
        piotr.function_creator(6),  #OK
        #piotr.parts_with_move,
        #piotr.by_gradient,
        piotr.compare_direction,    #OK
        #piotr.by_magick,
        piotr.by_edges_count,       #OK
        piotr.by_edges_direction,   #OK
        ])

def correct(res):
    return 1/(1+1/(res+SMALL_VAL))


def search(filename, dirname):
    res = []
    im = common.MyImage(filename).toRGB().minimize()
    n = 1
    total = len(os.listdir(dirname))
    for i in os.listdir(dirname):
        try:
            res.append([i, compare(im, common.MyImage(dirname+'/'+i).toRGB().minimize())])
            print 'compared '+str(n)+'/'+str(total)+' files'
            n += 1
        except IOError:
            print("\nAn Error catched:")
            print("BEGIN")
            print(traceback.format_exc())
            print("END\n")
    return sorted(res, key = lambda x: x[1])

print json.dumps(search(sys.argv[1], sys.argv[2]))
