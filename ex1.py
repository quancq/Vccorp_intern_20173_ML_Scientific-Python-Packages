"""
Sinh ngẫu nhiên một ma trận 100*100 giá trị các phần tử nằm trong khoảng (0, 100) rồi tìm định thức, ma trận chuyển vị, trị riêng và vector riêng của ma trận. Lưu kết quả vào một file output.txt
"""

import os
import numpy as np
import numpy.linalg as LA
from ScientificPythonPackages import utils


if __name__ == '__main__':
    np.random.seed(0)

    # Generate random matrix
    arr = utils.rand(0, 100, size=(5, 5))
    matrix = np.matrix(arr)

    det = LA.det(matrix)
    transpose_matrix = np.transpose(matrix)

    eigen_values, eigen_vectors = LA.eig(matrix)

    # =========================

    print("Matrix : ", matrix)
    print("Det : {:.4f}".format(det))
    print("Transpose matrix : ", transpose_matrix)

    for i in range(eigen_values.shape[0]):
        eig_value = eigen_values[i]
        eig_vector = eigen_vectors[:,i]
        print("Eig value  : ", eig_value)
        print("Eig vector : ", eig_vector)

    # Write output to file
    output_dir = "./Ex1_Output"
    utils.mkdirs(output_dir)
    output_path = os.path.join(output_dir, "output.txt")

    with open(output_path, 'w') as f:
        f.write("Original matrix : \n")
        for row in matrix:
            np.savetxt(f, row, fmt='%.2f')

        f.write("\nDet : {:.4f}\n".format(det))

        f.write("\nTranspose matrix : \n")
        for row in transpose_matrix:
            np.savetxt(f, row, fmt='%.2f')

        f.write("\nEigen values and eigen vectors :")
        for i in range(eigen_values.shape[0]):
            eig_value = eigen_values[i]
            eig_vector = eigen_vectors[:,i]
            f.write("\n{:.4f}, ".format(eig_value))
            np.savetxt(f, eig_vector, fmt='%.2f', newline=' ')

    print("Write output to {} done".format(os.path.abspath(output_path)))

