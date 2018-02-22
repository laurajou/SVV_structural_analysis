import math
import matplotlib.pyplot as plt

def distance(point1, point2):
    z_1, y_1 = point1[0], point1[1]
    z_2, y_2 = point2[0], point2[1]
    return math.sqrt((y_1 - y_2)**2 + (z_1 - z_2)**2)

def distance_point_line(point, line):
    """
    :param point: tuple (z, y) containing point coordinates
    :param line: tuple (A, B, C) containing line such that Az + By + C = 0
    :return: euclidean distance between line and point
    """
    z, y = point[0], point[1]
    A, B, C = line[0], line[1], line[2]
    return abs(A * z + B * y + C) / math.sqrt(A ** 2 + B ** 2)

def plot_boom_coordinates(coordinates):
    """
    Plot coordinates to verify visually that they are correct.
    :param coordinates: list of lists [z, y] containing the coordinates of each boom.
    """
    zs = []
    ys = []
    for boom_coord in coordinates:
        zs.append(boom_coord[0])
        ys.append(boom_coord[1])
    plt.axis([-500, 500, -500, 500])
    plt.scatter(zs, ys)
    plt.show()

