from PIL import Image
import numpy as np
from zigzag import *
import math


def update_npmat_padding(npmat, rows_pad, cols_pad):
    # Tạo ma trận mới với kích thước đã được padding
    padded_npmat = np.zeros((rows_pad, cols_pad, 3), dtype=np.uint8)
    # Copy giá trị từ ma trận npmat ban đầu
    padded_npmat[: npmat.shape[0], : npmat.shape[1], :] = npmat

    return padded_npmat


def remove_padding(padded_image, original_shape):
    return padded_image[: original_shape[0], : original_shape[1], :]
