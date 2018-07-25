"""
    Cho các dữ liệu từ file ZebraBotswana.txt có cấu trúc time(định dạng Unix), vị trí tọa độ (Longtitude, Latitude) tương ứng với time và id ngựa vằn tương ứng.
  - Đọc dữ liệu và vẽ bản đồ đường đi của mỗi con ngựa dựa vào thời gian và vị trí.
  - Đưa ra hai ngày mà khoảng cách vị trí của nó gần nhau nhất tương ứng với mỗi con ngựa.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import utils
import math
from datetime import datetime


def calc_euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


if __name__ == '__main__':
    data_path = "./Input/ZebraBotswana.txt"
    output_dir = "./Ex4_Output"
    utils.mkdirs(output_dir)

    zebra = pd.read_csv(data_path)
    print(zebra.info())

    by_animal = zebra.sort_values(["Animal", "UnixTime"]).groupby("Animal")

    animals = []
    animals.append(by_animal["Long"].apply(list))
    animals.append(by_animal["Latt"].apply(list))
    animals.append(by_animal["UnixTime"].apply(list))

    animals = pd.concat(animals, axis=1)

    print(animals.info())
    result_map = {}

    for animal in animals.index:
        fig, ax = plt.subplots()

        longs = animals.loc[animal]["Long"]
        min_long = np.min(longs)
        max_long = np.max(longs)

        latts = animals.loc[animal]["Latt"]
        min_latt = np.min(latts)
        max_latt = np.max(latts)

        unix_times = animals.loc[animal]["UnixTime"]

        vertices = list(zip(longs, latts))
        num_coordinates = len(vertices)

        print("\nAnimal : ", animal)
        print("Number coordinates : ", num_coordinates)

        # Compute min distance between 2 position by algorithm has O(nlogn) complexity

        # Build points
        points = []
        for i in range(num_coordinates):
            point = utils.Point(vertices[i][0], vertices[i][1], unix_times[i])
            points.append(point)

        point1, point2 = utils.find_closet_pair(points)
        min_distance = utils.calc_euclidean_distance(point1, point2)

        # ================================

        print("Min distance : ", min_distance)
        print("long1 : {}, latt1 = {}".format(point1.x, point1.y))
        print("long2 : {}, latt2 = {}".format(point2.x, point2.y))
        print("Time1 : ", point1.timestamp)
        print("Time2 : ", point2.timestamp)

        result_map.update({animal: (point1, point2)})

        codes = [Path.LINETO for _ in range(len(vertices))]
        codes[0] = Path.MOVETO

        print("Min Longitude : {}, Max Longitude : {}".format(min_long, max_long))
        print("Min Latitude : {}, Max Latitude : {}".format(min_latt, max_latt))

        print("Start position : ", vertices[0])
        print("Finish position : ", vertices[-1])

        path = Path(vertices, codes)

        patch = patches.PathPatch(path, lw=2, facecolor=None)
        ax.add_patch(patch)

        ax.set_xlim(min_long, max_long)
        ax.set_ylim(min_latt, max_latt)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("{}'s moves".format(animal))

        # Mark start and finish position of animal on map
        # Start position
        ax.annotate("Start", xy=vertices[0],
                    xytext=(vertices[0][0], vertices[0][1] + 0.1),
                    color="r", arrowprops=dict(arrowstyle="->"))

        # Finish position
        ax.annotate("Finish", xy=vertices[-1],
                    xytext=(vertices[-1][0], vertices[-1][1] + 0.1),
                    color="r", arrowprops=dict(arrowstyle="->"))

        # Save figure
        save_path = os.path.join(output_dir, "{}.jpg".format(animal))
        plt.savefig(save_path, dpi=100)

        # break

    # Print result
    print("\n=========== Result ===========")
    for animal, (point1, point2) in result_map.items():
        date1 = datetime.fromtimestamp(point1.timestamp).strftime('%d-%m-%Y %H:%M:%S')
        date2 = datetime.fromtimestamp(point2.timestamp).strftime('%d-%m-%Y %H:%M:%S')
        distance = utils.calc_euclidean_distance(point1, point2)
        print("Animal : {}, date1 : {}, date2 : {}, distance : {}".format(animal, date1, date2, distance))

    plt.show()
