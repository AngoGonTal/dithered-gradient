import numpy as np

# Quelle: https://de.wikipedia.org/wiki/YCbCr-Farbmodell

def rgb2ycbcr( rgb ):
    
    Y  = int( round( rgb[0] *  0.299    + rgb[1] *  0.587    + rgb[2] *  0.114         , 0 ) )
    Cb = int( round( rgb[0] * -0.168736 + rgb[1] * -0.331264 + rgb[2] *  0.5      + 128, 0 ) ) 
    Cr = int( round( rgb[0] *  0.5      + rgb[1] * -0.418688 + rgb[2] * -0.081312 + 128, 0 ) ) 

    return( ( Y, Cb, Cr ) )