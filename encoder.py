import argparse
import os
import math
import numpy as np
from rlc import *
from dct import *
from padding import *
from quantization import *
from scipy import fftpack
from PIL import Image
from huffman import HuffmanTree


def write_to_file(filepath, dc, ac, blocks_count, tables, rows, cols):
    try:
        f = open(filepath, "w")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "No such directory: {}".format(os.path.dirname(filepath))
        ) from e

    # 16 bits biểu diễn chiều rộng của ảnh
    f.write(uint_to_binstr(rows, 16))
    # 16 bits biểu diễn chiều cao của ảnh
    f.write(uint_to_binstr(cols, 16))

    for table_name in ["dc_y", "ac_y", "dc_c", "ac_c"]:
        # 16 bits biểu diễn table_size
        f.write(uint_to_binstr(len(tables[table_name]), 16))

        for key, value in tables[table_name].items():
            if table_name in {"dc_y", "dc_c"}:
                # 4 bits biểu diễn cho category
                # 4 bits biểu diễn cho code_length
                # code_length bits cho huffman_code
                f.write(uint_to_binstr(key, 4))
                f.write(uint_to_binstr(len(value), 4))
                f.write(value)
            else:
                # 4 bits run_length
                # 4 bits size
                # 8 bits code_length
                # 'code_length' bits huffman_code
                f.write(uint_to_binstr(key[0], 4))
                f.write(uint_to_binstr(key[1], 4))
                f.write(uint_to_binstr(len(value), 8))
                f.write(value)

    # 32 bits blocks_count
    f.write(uint_to_binstr(blocks_count, 32))

    for b in range(blocks_count):
        for c in range(3):
            category = bits_required(dc[b, c])
            symbols, values = run_length_encode(ac[b, :, c])

            dc_table = tables["dc_y"] if c == 0 else tables["dc_c"]
            ac_table = tables["ac_y"] if c == 0 else tables["ac_c"]

            f.write(dc_table[category])
            f.write(int_to_binstr(dc[b, c]))

            for i in range(len(symbols)):
                f.write(ac_table[tuple(symbols[i])])
                f.write(values[i])
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_to_compress", help="path to the input image")
    parser.add_argument("compressed_file", help="path to the output compressed file")
    args = parser.parse_args()
    input_image_path = args.image_to_compress
    output_image_path = args.compressed_file
    image_to_compress = Image.open(input_image_path)

    ycbcr = image_to_compress.convert("YCbCr")
    npmat = np.array(ycbcr, dtype=np.uint8)
    # block size: 8x8
    rows, cols = npmat.shape[0], npmat.shape[1]

    rows_pad = math.ceil(rows / 8) * 8

    cols_pad = math.ceil(cols / 8) * 8

    if rows_pad > cols_pad:
        cols_pad = rows_pad
    elif rows_pad < cols_pad:
        rows_pad = cols_pad

    # subsampling(4:2:0) + padding
    #y = npmat[:, :, 0]
    #Cb = npmat[::2, ::2, 1]
    #Cr = npmat[::2, ::2, 2]

    blocks_count = rows_pad // 8 * cols_pad // 8
    npmat = update_npmat_padding(npmat, rows_pad, cols_pad)
    # dc là ô ở góc trên bên trái của khối, ac là tất cả các ô còn lại.
    dc = np.empty((blocks_count, 3), dtype=np.int32)
    ac = np.empty((blocks_count, 63, 3), dtype=np.int32)
    # image = Image.fromarray(npmat, "YCbCr")
    # image = image.convert("RGB")
    # image.show()
    for i in range(0, rows_pad, 8):
        for j in range(0, cols_pad, 8):
            try:
                block_index += 1
            except NameError:
                block_index = 0
            for k in range(3):
                # [0, 255] --> [-128, 127]
                block = npmat[i : i + 8, j : j + 8, k] - 128
                # print(block)
                dct_matrix = DCT_2D(block)
                # print(dct_matrix)
                quant_matrix = quant_block(dct_matrix, "lum" if k == 0 else "chrom")
                # print(quant_matrix)
                zz = block_to_zigzag(quant_matrix)
                # print(zz)
                dc[block_index, k] = zz[0]
                ac[block_index, :, k] = zz[1:]

    H_DC_Y = HuffmanTree(np.vectorize(bits_required)(dc[:, 0]))
    H_DC_C = HuffmanTree(np.vectorize(bits_required)(dc[:, 1:].flat))
    H_AC_Y = HuffmanTree(
        flatten(run_length_encode(ac[i, :, 0])[0] for i in range(blocks_count))
    )
    H_AC_C = HuffmanTree(
        flatten(
            run_length_encode(ac[i, :, j])[0]
            for i in range(blocks_count)
            for j in [1, 2]
        )
    )

    tables = {
        "dc_y": H_DC_Y.value_to_bitstring_table(),
        "ac_y": H_AC_Y.value_to_bitstring_table(),
        "dc_c": H_DC_C.value_to_bitstring_table(),
        "ac_c": H_AC_C.value_to_bitstring_table(),
    }
    write_to_file(output_image_path, dc, ac, blocks_count, tables, rows, cols)


if __name__ == "__main__":
    main()
