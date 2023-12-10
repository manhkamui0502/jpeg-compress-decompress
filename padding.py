from PIL import Image
import numpy as np
from zigzag import *
import math
import argparse


def update_npmat_padding(npmat, rows_pad, cols_pad):
    # Tạo ma trận mới với kích thước đã được padding
    padded_npmat = np.zeros((rows_pad, cols_pad, 3), dtype=np.uint8)
    # Copy giá trị từ ma trận npmat ban đầu
    padded_npmat[: npmat.shape[0], : npmat.shape[1], :] = npmat

    return padded_npmat


def remove_padding(padded_image, original_shape):
    return padded_image[: original_shape[0], : original_shape[1], :]


# def main():
#    parser = argparse.ArgumentParser()
#    parser.add_argument("image_to_padding", help="path to the input image")
#    args = parser.parse_args()
#    input_image_path = args.image_to_padding
#    image_to_compress = Image.open(input_image_path)
#
#    ycbcr = image_to_compress.convert("YCbCr")
#    npmat = np.array(ycbcr, dtype=np.uint8)
#    # block size: 8x8
#    rows, cols = npmat.shape[0], npmat.shape[1]
#
#    rows_pad = math.ceil(rows / 8) * 8
#
#    cols_pad = math.ceil(cols / 8) * 8
#
#    if rows_pad > cols_pad:
#        cols_pad = rows_pad
#    elif rows_pad < cols_pad:
#        rows_pad = cols_pad
#
#    blocks_count = rows_pad // 8 * cols_pad // 8
#    npmat = update_npmat_padding(npmat, rows_pad, cols_pad)
#    # dc là ô ở góc trên bên trái của khối, ac là tất cả các ô còn lại.
#    image = Image.fromarray(npmat, "YCbCr")
#    image = image.convert("RGB")
#    image.show()
#
#
# if __name__ == "__main__":
#    main()
