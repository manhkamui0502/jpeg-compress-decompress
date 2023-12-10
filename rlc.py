import sys
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
            
    #print("Symbols:", symbols)
    #print("Values:", values)
    return symbols, values


def calculate_size(arr):
    # Tính kích thước của mảng dữ liệu
    original_size = sys.getsizeof(arr)

    # Áp dụng RLE để mã hóa mảng dữ liệu
    symbols, values = run_length_encode(arr)
    rle_encoded_data = symbols + values

    # Tính kích thước của dữ liệu sau khi áp dụng RLE
    rle_encoded_size = sys.getsizeof(rle_encoded_data)

    return original_size, rle_encoded_size


# Sử dụng hàm run_length_encode với một mảng arr
# data = [ 26, 3, 0, 3, 3, 6, 2, 4, 1, 4, 1, 1, 5, 1, 2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
# data = [10, 9, 8, 7, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# symbols, values = run_length_encode(data)
# In kết quả
# print("Symbols:", symbols)
# print("Values:", values)


# Sử dụng hàm để tính toán kích thước
# original_size, rle_encoded_size = calculate_size(data)

# In kết quả
# print("Kích thước ban đầu:", original_size, "bytes")
# print("Kích thước sau khi RLE:", rle_encoded_size, "bytes")
