"""
    Cho các dữ liệu từ file ZebraBotswana.txt có cấu trúc time(định dạng Unix), vị trí tọa độ (Longtitude, Latitude) tương ứng với time và id ngựa vằn tương ứng.
  - Đọc dữ liệu và vẽ bản đồ đường đi của mỗi con ngựa dựa vào thời gian và vị trí.
  - Đưa ra hai ngày mà khoảng cách vị trí của nó gần nhau nhất tương ứng với mỗi con ngựa.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


if __name__ == '__main__':
    data_path = "./Input/ZebraBotswana.txt"

    zebra = pd.read_csv(data_path)
    print(zebra.info())

    by_animal = zebra.groupby("Animal")

    animals = []
    animals.append(by_animal["Long"].apply(list))
    animals.append(by_animal["Latt"].apply(list))
    animals.append(by_animal["UnixTime"].apply(list))

    animals = pd.concat(animals, axis=1)
    print(animals.info())

    # ax = plt.gca()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for animal in animals.index:
        print("Animal : ", animal)
        longs = animals.loc[animal]["Long"]
        latts = animals.loc[animal]["Latt"]
        unix_times = animals.loc[animal]["UnixTime"]
        vertices = [(long * 1e5, latt * 1e5) for long, latt in zip(longs, latts)][:5]
        codes = [Path.LINETO for _ in range(len(vertices))][:5]
        codes[0] = Path.MOVETO
        codes[-1] = Path.CLOSEPOLY

        print(vertices)
        print(codes)
        path = Path(vertices, codes)

        patch = patches.PathPatch(path, lw=2)
        ax.add_patch(patch)
        ax.set_xlim(0, 24000000)
        ax.set_ylim(-2000000, 0)

        break

    plt.show()
