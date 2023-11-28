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


class JPEGFileReader:
    TABLE_SIZE_BITS = 16
    BLOCKS_COUNT_BITS = 32

    DC_CODE_LENGTH_BITS = 4
    CATEGORY_BITS = 4

    AC_CODE_LENGTH_BITS = 8
    RUN_LENGTH_BITS = 4
    SIZE_BITS = 4

    # Thêm constant cho kích thước ảnh gốc
    ORIGINAL_SIZE_BITS_H = 32  # 32 bits cho chiều cao
    ORIGINAL_SIZE_BITS_W = 32  # 32 bits cho chiều rộng

    def __init__(self, filepath):
        self.__file = open(filepath, "r")

    def read_original_size(self):
        # Đọc chiều cao và chiều rộng từ đầu file
        return (
            self.__read_uint(self.ORIGINAL_SIZE_BITS_H),
            self.__read_uint(self.ORIGINAL_SIZE_BITS_W),
        )

    def read_int(self, size):
        if size == 0:
            return 0

        # chỉ ra dấu của số
        bin_num = self.__read_str(size)
        if bin_num[0] == "1":
            return self.__int2(bin_num)
        else:
            return self.__int2(binstr_flip(bin_num)) * -1

    def read_dc_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)
        for _ in range(table_size):
            category = self.__read_uint(self.CATEGORY_BITS)
            code_length = self.__read_uint(self.DC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = category
        return table

    def read_ac_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)
        for _ in range(table_size):
            run_length = self.__read_uint(self.RUN_LENGTH_BITS)
            size = self.__read_uint(self.SIZE_BITS)
            code_length = self.__read_uint(self.AC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = (run_length, size)
        return table

    def read_blocks_count(self):
        return self.__read_uint(self.BLOCKS_COUNT_BITS)

    def read_huffman_code(self, table):
        prefix = ""
        while prefix not in table:
            prefix += self.__read_char()
        return table[prefix]

    def __read_uint(self, size):
        if size <= 0:
            raise ValueError("size of unsigned int should be greater than 0")
        return self.__int2(self.__read_str(size))

    def __read_str(self, length):
        return self.__file.read(length)

    def __read_char(self):
        return self.__read_str(1)

    def __int2(self, bin_num):
        return int(bin_num, 2)


def read_image_file(filepath):
    reader = JPEGFileReader(filepath)

    # Đọc kích thước gốc từ đầu file
    original_size = reader.read_original_size()

    tables = dict()
    for table_name in ["dc_y", "ac_y", "dc_c", "ac_c"]:
        if "dc" in table_name:
            tables[table_name] = reader.read_dc_table()
        else:
            tables[table_name] = reader.read_ac_table()

    blocks_count = reader.read_blocks_count()

    dc = np.empty((blocks_count, 3), dtype=np.int32)
    ac = np.empty((blocks_count, 63, 3), dtype=np.int32)

    for block_index in range(blocks_count):
        for component in range(3):
            dc_table = tables["dc_y"] if component == 0 else tables["dc_c"]
            ac_table = tables["ac_y"] if component == 0 else tables["ac_c"]

            category = reader.read_huffman_code(dc_table)
            dc[block_index, component] = reader.read_int(category)

            cells_count = 0

            while cells_count < 63:
                run_length, size = reader.read_huffman_code(ac_table)

                if (run_length, size) == (0, 0):
                    while cells_count < 63:
                        ac[block_index, cells_count, component] = 0
                        cells_count += 1
                else:
                    for i in range(run_length):
                        ac[block_index, cells_count, component] = 0
                        cells_count += 1
                    if size == 0:
                        ac[block_index, cells_count, component] = 0
                    else:
                        value = reader.read_int(size)
                        ac[block_index, cells_count, component] = value
                    cells_count += 1

    return dc, ac, tables, blocks_count, original_size


def zigzag_to_block(zigzag):
    rows = cols = int(math.sqrt(len(zigzag)))

    if rows * cols != len(zigzag):
        raise ValueError("length of zigzag should be a perfect square")

    block = np.empty((rows, cols), np.int32)

    for i, point in enumerate(zigzag_points(rows, cols)):
        block[point] = zigzag[i]

    return block


def dequantize(block, component):
    q = get_quantization_table(component)
    return block * q


def idct_2d(image):
    return fftpack.idct(fftpack.idct(image.T, norm="ortho").T, norm="ortho")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_to_decompress", help="file path for decompression")
    parser.add_argument("image_restored", help="restored image name")
    args = parser.parse_args()
    file_path_to_decompress = args.file_to_decompress
    image_restored_path = args.image_restored

    dc, ac, tables, blocks_count, original_size = read_image_file(
        args.file_to_decompress
    )

    block_side = 8

    image_side = int(math.sqrt(blocks_count)) * block_side

    blocks_per_line = image_side // block_side

    npmat = np.empty((image_side, image_side, 3), dtype=np.uint8)

    for block_index in range(blocks_count):
        i = block_index // blocks_per_line * block_side
        j = block_index % blocks_per_line * block_side

        for c in range(3):
            zigzag = [dc[block_index, c]] + list(ac[block_index, :, c])
            quant_matrix = zigzag_to_block(zigzag)
            dct_matrix = dequantize(quant_matrix, "lum" if c == 0 else "chrom")
            block = idct_2d(dct_matrix)
            npmat[i : i + 8, j : j + 8, c] = block + 128

    rows, cols = original_size
    npmat = remove_padding(npmat, (rows, cols))
    image = Image.fromarray(npmat, "YCbCr")
    image = image.convert("RGB")
    image.save(image_restored_path)


if __name__ == "__main__":
    main()
