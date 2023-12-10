import numpy as np


def get_quantization_table(type):
    if type == "lum":
        table = np.array(
            [
                [16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99],
            ]
        )
    elif type == "chrom":
        table = np.array(
            [
                [17, 18, 24, 47, 99, 99, 99, 99],
                [18, 21, 26, 66, 99, 99, 99, 99],
                [24, 26, 56, 99, 99, 99, 99, 99],
                [47, 66, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
            ]
        )
    return table


def quant_block(block, type):
    quant_table = get_quantization_table(type)
    quanted_block = (block / quant_table).round().astype(np.int32)
    return quanted_block


def dequant_block(block, type):
    quant_table = get_quantization_table(type)
    dequanted_block = block * quant_table.astype(np.int32)
    return dequanted_block


# t = [
#    [-415, -33, -58, 35, 58, -51, -15, -12],
#    [5, -34, 49, 18, 27, 1, -5, 3],
#    [-46, 14, 80, -35, -50, 19, 7, -18],
#    [-53, 21, 34, -20, 2, 87, 36, 12],
#    [9, -2, 9, -5, -32, -15, 45, 37],
#    [-8, 15, -16, 7, -8, 11, 4, 7],
#    [19, -28, -2, -26, -2, 7, -44, -21],
#    [18, 25, -12, -44, 35, 48, -37, -3],
# ]
#
# t2 = quant_block(t, "lum")
# print(t2)
