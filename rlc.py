from zigzag import *


def run_length_encode(arr):
    # Xác định nơi chuỗi kết thúc
    last_nonzero = -1
    for i, elem in enumerate(arr):
        if elem != 0:
            last_nonzero = i

    # Mỗi ký hiệu là một cặp (RUNLENGTH, SIZE)
    symbols = []

    # Giá trị biểu diễn nhị phân của các phần tử mảng bằng SIZE bit
    values = []

    run_length = 0

    for i, elem in enumerate(arr):
        if i > last_nonzero:
            symbols.append((0, 0))
            values.append(int_to_binstr(0))
            break
        elif elem == 0 and run_length < 15:
            run_length += 1
        else:
            size = bits_required(elem)
            symbols.append((run_length, size))
            values.append(int_to_binstr(elem))
            run_length = 0
    return symbols, values

