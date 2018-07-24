import os
import numpy as np
import copy
import math
import random
import time


def mkdirs(path):
    if not os.path.exists(path):
        os.mkdir(path)


def rand(low=0, high=1, size=(3,3)):
    return (high - low) * np.random.rand(*size) + low


class Point:
    def __init__(self, x, y, timestamp):
        self.x = x
        self.y = y
        self.timestamp = timestamp


def min(a, b):
    return a if a < b else b


def calc_euclidean_distance(point1, point2):
    return math.sqrt((point2.y - point1.y) ** 2 + (point2.x - point1.x) ** 2)


def find_closet_distance_brute_force(points):
    # Return min distance between all pairs
    min_distance = calc_euclidean_distance(points[0], points[1])
    point1 = points[0]
    point2 = points[1]

    num_points = len(points)
    for i in range(num_points - 1):
        for j in range(i + 1, num_points):
            distance = calc_euclidean_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                point1 = points[i]
                point2 = points[j]

    return point1, point2


def find_closet_distance_between_two_half(points, max_distance):
    num_points = len(points)
    assert num_points >= 2

    min_distance = max_distance

    point1 = points[0]
    point2 = points[1]

    for i in range(num_points - 1):
        for j in range(i + 1, num_points):
            if (points[j].y - points[i].y) >= min_distance:
                break
            distance = calc_euclidean_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                point1 = points[i]
                point2 = points[j]

    return point1, point2


def find_closet_utils(points_sort_by_x, points_sort_by_y):
    point1 = point2 = Point(0,0,0)
    num_points = len(points_sort_by_x)

    if num_points <= 3:
        return find_closet_distance_brute_force(points_sort_by_x)

    # Middle point by x
    mid_idx = num_points // 2
    mid_point = points_sort_by_x[mid_idx]

    points_sort_by_y_left = []      # y-coordinate sorted points on left of vertical line
    points_sort_by_y_right = []     # y-coordinate sorted points on right of vertical line

    for point in points_sort_by_y:
        if point.x <= mid_point.x:
            points_sort_by_y_left.append(point)
        else:
            points_sort_by_y_right.append(point)

    # Divide and conquer to find closer pair on left and on right
    point1_left, point2_left = find_closet_utils(
        points_sort_by_x[:mid_idx],
        points_sort_by_y_left
    )
    min_distance_left = calc_euclidean_distance(point1_left, point2_left)

    point1_right, point2_right = find_closet_utils(
        points_sort_by_x[mid_idx:],
        points_sort_by_y_right
    )
    min_distance_right = calc_euclidean_distance(point1_right, point2_right)

    if min_distance_left < min_distance_right:
        point1 = point1_left
        point2 = point2_left
        min_distance = min_distance_left
    else:
        point1 = point1_right
        point2 = point2_right
        min_distance = min_distance_right


    candidate_points = []
    # Find y sorted points which have distance by x in range [mid.x - d, mid.x + d]
    for point in points_sort_by_y:
        if math.fabs(point.x - mid_point.x) < min_distance:
            candidate_points.append(point)

    # Find closet pair in candidate points
    if len(candidate_points) >= 2:
        candidate1, candidate2 = find_closet_distance_between_two_half(candidate_points, min_distance)

        min_candidate_distance = calc_euclidean_distance(candidate1, candidate2)

        if min_candidate_distance < min_distance:
            point1 = candidate1
            point2 = candidate2
            min_distance = min_candidate_distance

    return point1, point2


def find_closet_pair(points):
    # Return timestamp pair correspond to closet pair

    print("Find closet pair by algorithm has O(nlogn) complexity ...")

    # Create list of sorted by x-coordinate points
    points_sort_by_x = copy.deepcopy(points)
    sorted(points_sort_by_x, key=lambda p: p.x)

    # Create list of sorted by y-coordinate points
    points_sort_by_y = copy.deepcopy(points)
    sorted(points_sort_by_y, key=lambda p: p.y)

    point1, point2 = find_closet_utils(
        points_sort_by_x,
        points_sort_by_y
    )

    return point1, point2


if __name__ == "__main__":
    # Test closet pair algorithm

    num_points = 100000
    points = []

    print("Random points ... ")
    for i in range(num_points):
        x = rand(0, 10000, size=(1,))
        y = rand(0, 10000, size=(1,))
        timestamp = i
        point = Point(x, y, timestamp)
        # print("Point : (x,y,time) =  ({}, {}, {})".format(point.x, point.y, point.timestamp))
        points.append(point)

    print("Random {} points done".format(num_points))

    start_time = time.time()
    point1_algo2, point2_algo2 = find_closet_pair(points)
    finish_time = time.time()
    min_distance_algo2 = calc_euclidean_distance(point1_algo2, point2_algo2)

    print("Algo has O(nlogn) complexity result: ")
    print("Point 1 : (x,y,time) =  ({}, {}, {})".format(
        point1_algo2.x, point1_algo2.y, point1_algo2.timestamp
    ))
    print("Point 2 : (x,y,time) =  ({}, {}, {})".format(
        point2_algo2.x, point2_algo2.y, point2_algo2.timestamp
    ))
    print("Min distance : ", min_distance_algo2)
    print("Time : {} seconds".format((finish_time - start_time)))

    print("==================================================")

    # start_time = time.time()
    # point1_brute_force, point2_brute_force = find_closet_distance_brute_force(points)
    # finish_time = time.time()
    # min_distance_bf = calc_euclidean_distance(point1_brute_force, point2_brute_force)
    #
    # print("Brute force result: ")
    # print("Point 1 : (x,y,time) =  ({}, {}, {})".format(
    #     point1_brute_force.x, point1_brute_force.y, point1_brute_force.timestamp
    # ))
    # print("Point 2 : (x,y,time) =  ({}, {}, {})".format(
    #     point2_brute_force.x, point2_brute_force.y, point2_brute_force.timestamp
    # ))
    # print("Min distance : ", min_distance_bf)
    # print("Time : {} seconds".format((finish_time - start_time)))




