########################################
#
# Author: Piotr Sroczkowski
#
########################################

#
# first argument of the script is the name of the searched file
# second one is the path to the directory containing pictures
#

import os
import sys
import random
import traceback
import json

import PIL
from PIL import Image

import piotr
import daniel
import common

SMALL_VAL = 1e-10



# general comparison
def compare_general(x,y,ar):
    res = 1e-10
    for f in ar:
        res += 1/(correct(f(x,y))+SMALL_VAL)
    return 1/res

# define used methods
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

# correction of similarity coefficient
def correct(res):
    return 1/(1+1/(res+SMALL_VAL))


# search similar images within directory
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

# printing result in json
print json.dumps(search(sys.argv[1], sys.argv[2]))
