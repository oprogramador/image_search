########################################
#
# Author: Daniel Mikulski
# Silesian University of Technology
#
########################################

import os
import sys
import random

from skimage import data, img_as_float
from skimage import exposure
from PIL import Image

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

import common

def scipy_compare(img1,img2):
    # read images as 2D arrays (convert to grayscale for simplicity)
    img1 = to_grayscale(imread(file1).astype(float))
    img2 = to_grayscale(imread(file2).astype(float))
    
    # resize images
    
    newwidth = 200
    newheight = 200
    img1 = img.resize((newwidth, newheight), image.ANTIALIAS)
    img2 = img.resize((newwidth, newheight), image.ANTIALIAS)
    
    # compare images
    n_m, n_0 = compare_images(img1, img2)
    print "Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size
    print "Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size
    
def compare_images(img1, img2):
    # normalize to compensate for exposure difference
    img1 = normalize(img1)
    img2 = normalize(img2)
    
    # calculate the difference and its norms
    
    diff = img1 - img2 
    # Manhattan norm
    m_norm = sum(abs(diff)) 
    # Zero norm
    z_norm = norm(diff.ravel(), 0) 
    return (m_norm, z_norm)
 
def to_grayscale(arr):
    #"If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr
 
def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng
    
    
    
def compare_histogram(x,y):
    #diff - difference between two images
    diff = 0

    #load histograms of 2 images
    xhis = common.histogram(x)
    yhis = common.histogram(y)

    #calculate difference using intersection method
    for i in xrange(256):
        diff += min(xhis[0][i],yhis[0][i]) + min(xhis[1][i],yhis[1][i]) + min(xhis[2][i],yhis[2][i])
    return 3 - diff
