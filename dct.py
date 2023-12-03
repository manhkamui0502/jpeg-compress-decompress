import numpy as np
from scipy import fftpack

# Không dùng thư viện
def dct_2d(block):
    # Chuẩn bị ma trận kết quả DCT
    dct_block = np.zeros((8, 8))
    # Tính toán hệ số chuẩn hóa C(u) và C(v)
    c_u = np.ones(8) * np.sqrt(2) / 2
    c_u[0] = 1 / np.sqrt(2)
    c_v = np.ones(8) * np.sqrt(2) / 2
    c_v[0] = 1 / np.sqrt(2)
    # Lặp qua từng vị trí (u, v) trong ma trận kết quả DCT
    for u in range(8):
        for v in range(8):
            # Tính toán giá trị D(u, v) ban đầu
            dct_value = 0
            # Lặp qua từng vị trí (x, y) trong khối ban đầu
            for x in range(8):
                for y in range(8):
                    # Tính toán giá trị cosin tương ứng
                    cos_x = np.cos((2 * x + 1) * u * np.pi / 16)
                    cos_y = np.cos((2 * y + 1) * v * np.pi / 16)
                    # Nhân giá trị f(x, y) với cos_x và cos_y,
                    # sau đó cộng tổng vào giá trị D(u, v)
                    dct_value += block[x, y] * cos_x * cos_y
            # Nhân giá trị D(u, v) với C(u) và C(v)
            dct_value *= c_u[u] * c_v[v]
            # Gán giá trị D(u, v) vào ma trận kết quả DCT
            dct_block[u, v] = dct_value

    return dct_block


def idct_2d(dct_block):
    # Chuẩn bị khối kết quả IDCT
    block = np.zeros((8, 8))
    # Tính toán hệ số chuẩn hóa C(u) và C(v)
    c_u = np.ones(8) * np.sqrt(2) / 2
    c_u[0] = 1 / np.sqrt(2)
    c_v = np.ones(8) * np.sqrt(2) / 2
    c_v[0] = 1 / np.sqrt(2)
    # Lặp qua từng vị trí (x, y) trong khối kết quả IDCT
    for x in range(8):
        for y in range(8):
            # Tính toán giá trị f(x, y) ban đầu
            idct_value = 0
            # Lặp qua từng vị trí (u, v) trong ma trận DCT
            for u in range(8):
                for v in range(8):
                    # Tính toán giá trị cosin tương ứng
                    cos_u = np.cos((2 * x + 1) * u * np.pi / 16)
                    cos_v = np.cos((2 * y + 1) * v * np.pi / 16)

            # Nhân giá trị D(u, v) với cos_u và cos_v, sau đó cộng tổng vào giá trị f(x, y)
            idct_value += dct_block[u, v] * cos_u * cos_v * c_u[u] * c_v[v]
            # Nhân giá trị f(x, y) với hệ số 1/4 và gán vào khối kết quả IDCT
            block[x, y] = idct_value / 4

    return block

# Dùng thư viện
def DCT_2D(block):
    DCT_matrix = fftpack.dct(fftpack.dct(block.T, norm="ortho").T, norm="ortho")
    return DCT_matrix


def iDCT_2D(DCT_block):
    block = fftpack.idct(fftpack.idct(DCT_block.T, norm="ortho").T, norm="ortho")
    return block
