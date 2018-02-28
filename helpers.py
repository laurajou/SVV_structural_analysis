import math
import matplotlib.pyplot as plt
import boom
import geometry
import numpy as np

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
    n = range(len(coordinates))
    for boom_coord in coordinates:
        zs.append(boom_coord[0])
        ys.append(boom_coord[1])
    fig, ax = plt.subplots()
    ax.scatter(zs, ys)
    plt.axhline(0, color='black')
    for i, txt in enumerate(n):
        ax.annotate(txt, (zs[i], ys[i]))
    plt.show()


def get_list(booms, parameter_position):
    list = []
    for element in booms:
        num = len(element.adjacents)
        adjacent_booms = []
        for num in range(num):
            adjacent_booms.append(element.adjacents[num][parameter_position])
        list.append(adjacent_booms)
    return list

def get_thickness_list(booms):
    get_list(booms, 1)

def get_adjacents_list(booms):
    get_list(booms, 0)

def get_lengths_list(booms):
    get_list(booms, 2)

def get_common_wall(cells):
    for wall1 in cells[0]:
        if wall1 in cells[1]:
            return wall1

def get_array_x_i(file_name):
    data = np.genfromtxt(file_name, skip_header=1)[:, 0]
    return data
def get_array_Mx_i(file_name):
    data = np.genfromtxt(file_name, skip_header=1)[:, 1]
    return data
def get_array_My_i(file_name):
    data = np.genfromtxt(file_name, skip_header=1)[:, 2]
    return data
def get_array_Mz_i(file_name):
    data = np.genfromtxt(file_name, skip_header=1)[:, 3]
    return data
def get_array_Sy_i(file_name):
    data = np.genfromtxt(file_name, skip_header=1)[:, 4]
    return data
def get_array_Sz_i(file_name):
    data = np.genfromtxt(file_name, skip_header=1)[:, 5]
    return data


