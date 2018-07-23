"""
Một ma trận được gọi là "Matrix square" nếu đó là ma trận vuông và tổng các phần tử của các hàng ngang, cột dọc và đường chéo đều bằng nhau. Viết chương trình kiểm tra ma trận đầu vào xem có phải là ma trận "Magic Square"?
"""

import numpy as np

def is_square_matrix(matrix):
    sums = []
    sums.append(np.sum(matrix, axis=0))
    sums.append(np.sum(matrix, axis=1))

    print(sums[0].shape)

    sums.append(np.array(np.trace(matrix)).reshape(-1,))
    sums.append(np.array(np.trace(matrix[::-1])).reshape(-1,))

    print(sums[-1].shape)

    sums = np.concatenate(sums)
    max = np.max(sums)
    min = np.min(sums)

    return max == min

if __name__ == '__main__':
    matrix = np.array(
        [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
    )

    print("Is square matrix : ", is_square_matrix(matrix))
