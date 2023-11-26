import math
import numpy as np


def zigzag_points(rows, cols):
    # hằng số cho hướng
    UP, DOWN, RIGHT, LEFT, UP_RIGHT, DOWN_LEFT = range(6)

    # di chuyển theo hướng khác nhau
    def move(direction, point):
        return {
            UP: lambda point: (point[0] - 1, point[1]),
            DOWN: lambda point: (point[0] + 1, point[1]),
            LEFT: lambda point: (point[0], point[1] - 1),
            RIGHT: lambda point: (point[0], point[1] + 1),
            UP_RIGHT: lambda point: move(UP, move(RIGHT, point)),
            DOWN_LEFT: lambda point: move(DOWN, move(LEFT, point)),
        }[direction](point)

    # trả về True nếu điểm nằm trong ranh giới của khối
    def inbounds(point):
        return 0 <= point[0] < rows and 0 <= point[1] < cols

    # bắt đầu từ ô ở góc trên bên trái.
    point = (0, 0)

    # true khi di chuyển lên phải, false khi di chuyển xuống trái
    move_up = True

    for i in range(rows * cols):
        yield point
        if move_up:
            if inbounds(move(UP_RIGHT, point)):
                point = move(UP_RIGHT, point)
            else:
                move_up = False
                if inbounds(move(RIGHT, point)):
                    point = move(RIGHT, point)
                else:
                    point = move(DOWN, point)
        else:
            if inbounds(move(DOWN_LEFT, point)):
                point = move(DOWN_LEFT, point)
            else:
                move_up = True
                if inbounds(move(DOWN, point)):
                    point = move(DOWN, point)
                else:
                    point = move(RIGHT, point)


def block_to_zigzag(block):
    return np.array([block[point] for point in zigzag_points(*block.shape)])


def zigzag_to_block(zigzag):
    rows = cols = int(math.sqrt(len(zigzag)))
    block = np.empty((rows, cols), np.int32)

    for i, point in enumerate(zigzag_points(rows, cols)):
        block[point] = zigzag[i]

    return block


def bits_required(n):
    n = abs(n)
    result = 0
    while n > 0:
        n >>= 1
        result += 1
    return result


def binstr_flip(binstr):
    # kiểm tra xem binstr có phải là 1 chuỗi nhị phân hay không
    if not set(binstr).issubset("01"):
        raise ValueError("binstr should have only '0's and '1's")
    return "".join(map(lambda c: "0" if c == "1" else "1", binstr))


def uint_to_binstr(number, size):
    return bin(number)[2:][-size:].zfill(size)


def int_to_binstr(n):
    if n == 0:
        return ""

    binstr = bin(abs(n))[2:]

    # đổi 0 thành 1 và ngược lại khi n là số âm
    return binstr if n > 0 else binstr_flip(binstr)


def flatten(lst):
    return [item for sublist in lst for item in sublist]
