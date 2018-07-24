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

    by_animal = zebra.sort_values(["Animal", "UnixTime"]).groupby("Animal")

    animals = []
    animals.append(by_animal["Long"].apply(list))
    animals.append(by_animal["Latt"].apply(list))
    animals.append(by_animal["UnixTime"].apply(list))

    animals = pd.concat(animals, axis=1)

    print(animals.info())

    # ax = plt.gca()


    # scale = 1

    for animal in animals.index:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        print("\nAnimal : ", animal)

        longs = animals.loc[animal]["Long"]
        min_long = np.min(longs)
        max_long = np.max(longs)
        print("Min Longitude : {}, Max Longitude : {}".format(min_long, max_long))

        latts = animals.loc[animal]["Latt"]
        min_latt = np.min(latts)
        max_latt = np.max(latts)
        print("Min Latitude : {}, Max Latitude : {}".format(min_latt, max_latt))

        unix_times = animals.loc[animal]["UnixTime"]

        vertices = list(zip(longs, latts))
        codes = [Path.LINETO for _ in range(len(vertices))]
        codes[0] = Path.MOVETO

        print("Number coordinates : ", len(vertices))

        path = Path(vertices, codes)

        patch = patches.PathPatch(path, lw=2)
        ax.add_patch(patch)

        ax.set_xlim(min_long, max_long)
        ax.set_ylim(min_latt, max_latt)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("{}'s moves".format(animal))

        # Mark start and finish position of animal on map
        # Start position
        ax.text(vertices[0], vertices[1], )

        # break

    plt.show()
