"""
Sử dụng matplotlib.pyplot.plot vẽ các đồ thị hàm số f(x) = (e^(−x/10))*sin(πx) and g(x) = x*e^(−x/3) trong khoảng [0, 10] trên cùng một biểu đồ. Bao gồm trục x, trục y, và các chú thích các đường biểu diễn của từng hàm số. Lưu đồ thì thành một file plot.jpg (“Jpeg”)
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from ScientificPythonPackages import utils


def f_func(x):
    func_name = "$\\exp(-x/10) * \\sin(\pi x)$"
    func = np.exp(-x / 10) * np.sin(np.pi * x)

    return func_name, func


def g_func(x):
    func_name = "$x * \\exp(-x/3)$"
    func = x * np.exp(-x / 3)

    return func_name, func


def plot_multi_functions(functions, output_path="./Ex5_Output/plot.jpg"):

    for func_name, (x,y) in functions.items():
        print("Plot Func name : {}".format(func_name))
        plt.plot(x, y, label=func_name)

    plt.legend()
    plt.title("Plot multi functions")
    plt.xlabel("x")
    plt.ylabel("y")

    # Save figure to output path
    dir_path = output_path[:output_path.rfind("/")]
    utils.mkdirs(dir_path)
    output_path = os.path.abspath(output_path)
    print("Save file to {} done".format(output_path))
    plt.savefig(output_path, dpi=200)

    plt.show()


if __name__ == '__main__':
    functions = {}

    x = np.arange(0, 10, 0.1)

    func_name, y = f_func(x)
    functions.update({func_name: (x, y)})

    func_name, y = g_func(x)
    functions.update({func_name: (x, y)})

    output_path = "./Ex5_Output/plot.jpg"

    plot_multi_functions(functions, output_path)
