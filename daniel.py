import common
    
# comparison of histogram
def compare_histo(x,y):
    #diff - difference between two images
    diff = 0

    #load histograms of 2 images
    xhis = common.histogram(x)
    yhis = common.histogram(y)

    #calculate difference using intersection method
    for i in xrange(256):
        diff += min(xhis[0][i],yhis[0][i]) + min(xhis[1][i],yhis[1][i]) + min(xhis[2][i],yhis[2][i])
    return 3 - diff
