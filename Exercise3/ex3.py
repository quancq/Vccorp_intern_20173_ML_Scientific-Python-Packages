"""
Một ma trận được gọi là "Matrix square" nếu đó là ma trận vuông và tổng các phần tử của các hàng ngang, cột dọc và đường chéo đều bằng nhau. Viết chương trình kiểm tra ma trận đầu vào xem có phải là ma trận "Magic Square"?
"""

import numpy as np


def is_square_matrix(matrix):
    sums = []

    # Sum by col
    sums.append(np.sum(matrix, axis=0))
    # Sum by row
    sums.append(np.sum(matrix, axis=1))

    # Sum by diagonal
    sums.append(np.array(np.trace(matrix)).reshape(-1,))
    sums.append(np.array(np.trace(matrix[::-1])).reshape(-1,))

    sums = np.concatenate(sums)
    max_value = np.max(sums)
    min_value = np.min(sums)

    return max_value == min_value


if __name__ == '__main__':
    matrix = np.array(
        [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
    )

    print("Is square matrix : ", is_square_matrix(matrix))
