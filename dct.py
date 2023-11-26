import numpy as np
from scipy import fftpack

def DCT_2D(block):
    DCT_matrix = fftpack.dct(fftpack.dct(block.T, norm='ortho').T, norm='ortho')
    return DCT_matrix

def iDCT_2D(DCT_block):
    block = fftpack.idct(fftpack.idct(DCT_block.T,norm='ortho').T,norm='ortho')
    return block



