import unittest
import geometry
import helpers
import numpy as np
import math
import boom
import matplotlib.pyplot as plt

def main():
    stringer_area = 38.5
    neutral_axis = (0, 1, 0)
    number_booms = 19

    # CREATE LIST OF COORDINATES FOR BOOMS
    # give the coordinates of the booms with respect to the hinge point
    # for the first eight, they are on a straight line
    coordinates = []
    for n in range(8):
        coordinates.append([(43.45 - 5.43125 * (n + 1)) * 10, (1.40625 * (n + 1)) * 10])
    # booms 8, 9 and 10 are along a semi-circle
    coordinates.append([-112.5 * math.cos(math.pi / 4), 112.5 * math.cos(math.pi / 4)])  # BOOM 8
    coordinates.append([-112.5, 0.0])  # BOOM 9
    # the last 8 are symmetric to the first eight wrt the z-axis
    for i in range(8, -1, -1):
        coords = coordinates[i]
        coordinates.append([coords[0], -coords[1]])
    # the ones on the spar are always at z=0 and distributed equally along the height of the spar
    coordinates.append([0.0, 37.5])
    coordinates.append([0.0, -37.5])
    # plot for verification
    #helpers.plot_boom_coordinates(coordinates)

    # CREATE LIST OF ADJACENTS FOR BOOMS
    # Format: np.array([[adjacent1, thicnkess_edge_1, length_edge1], [adjacent2, t2, l2]], ..., [[], []])
    adjacents = [0] * 21

    # for the ones along the straight line (up and down) the first and last are special
    for i in range(1, 7):
        adjacents[i] = [[i-1, 1.1, 56.10224], [i+1, 1.1, 56.10224]]
    for n in range(12, 18):
        adjacents[n] = [[n - 1, 1.1, 56.10224], [n + 1, 1.1, 56.10224]]
    adjacents[0] = [[18, 1.1, 56.10224 * 2], [1, 1.1, 56.10224]]
    adjacents[18] = [[17, 1.1, 56.10224], [0, 1.1, 56.10224 * 2]]

    # for the ones on the semi-circle the distance is slightly different
    for j in range(3):
        boom_num = 8 + j
        adjacents[boom_num] = [[boom_num-1, 1.1, 88.35], [boom_num+1, 1.1, 88.35]]
    adjacents[7] = [[6, 1.1, 56.10225], [8, 1.1, 88.35], [19, 2.9, 75]]
    adjacents[11] = [[10, 1.1, 88.35], [12, 1.1, 56.10225], [20, 2.9, 75]]
    adjacents[19] = [[20, 2.9, 75], [7, 2.9, 75]]
    adjacents[20] = [[19, 2.9, 75], [11, 2.9, 75]]

    # CREATE BOOM INSTANCES AND INSERT THEM IN GEOMETRY
    booms = []
    boom0 = boom.Boom(coordinates[0], adjacents[0], stringer_area, neutral_axis)
    booms.append(boom0)
    boom1 = boom.Boom(coordinates[1], adjacents[1], stringer_area, neutral_axis)
    booms.append(boom1)
    boom2 = boom.Boom(coordinates[2], adjacents[2], stringer_area, neutral_axis)
    booms.append(boom2)
    boom3 = boom.Boom(coordinates[3], adjacents[3], stringer_area, neutral_axis)
    booms.append(boom3)
    boom4 = boom.Boom(coordinates[4], adjacents[4], stringer_area, neutral_axis)
    booms.append(boom4)
    boom5 = boom.Boom(coordinates[5], adjacents[5], stringer_area, neutral_axis)
    booms.append(boom5)
    boom6 = boom.Boom(coordinates[6], adjacents[6], stringer_area, neutral_axis)
    booms.append(boom6)
    boom7 = boom.Boom(coordinates[7], adjacents[7], 0.0, neutral_axis)
    booms.append(boom7)
    boom8 = boom.Boom(coordinates[8], adjacents[8], stringer_area, neutral_axis)
    booms.append(boom8)
    boom9 = boom.Boom(coordinates[9], adjacents[9], stringer_area, neutral_axis)
    booms.append(boom9)
    boom10 = boom.Boom(coordinates[10], adjacents[10], stringer_area, neutral_axis)
    booms.append(boom10)
    boom11 = boom.Boom(coordinates[11], adjacents[11], 0.0, neutral_axis)
    booms.append(boom11)
    boom12 = boom.Boom(coordinates[12], adjacents[12], stringer_area, neutral_axis)
    booms.append(boom12)
    boom13 = boom.Boom(coordinates[13], adjacents[13], stringer_area, neutral_axis)
    booms.append(boom13)
    boom14 = boom.Boom(coordinates[14], adjacents[14], stringer_area, neutral_axis)
    booms.append(boom14)
    boom15 = boom.Boom(coordinates[15], adjacents[15], stringer_area, neutral_axis)
    booms.append(boom15)
    boom16 = boom.Boom(coordinates[16], adjacents[16], stringer_area, neutral_axis)
    booms.append(boom16)
    boom17 = boom.Boom(coordinates[17], adjacents[17], stringer_area, neutral_axis)
    booms.append(boom17)
    boom18 = boom.Boom(coordinates[18], adjacents[18], stringer_area, neutral_axis)
    booms.append(boom18)
    boom19 = boom.Boom(coordinates[19], adjacents[19], 0.0, neutral_axis)
    booms.append(boom19)
    boom20 = boom.Boom(coordinates[20], adjacents[20], 0.0, neutral_axis)
    booms.append(boom20)

    # CREATE INSTANCE OF AILERON GEOMETRY WITH ALL THE BOOMS
    aileron_geometry = geometry.Geometry(21, booms)

    # calculate areas of all booms
    for element in booms:
        element.calculate_area(aileron_geometry)
    # insert them in aileron_geometry object
    aileron_geometry.get_areas()
    # calculate centroid position
    aileron_geometry.calc_centroid()
    # calculate moments of inertia
    aileron_geometry.moment_inertia_Izz()
    aileron_geometry.moment_inertia_Iyy()
    aileron_geometry.moment_inertia_Izy()

    # print data to check
    for it, el in enumerate(booms):
        print('area of boom ', it, ' : ', aileron_geometry.boom_areas[it], '[mm^2]')
    print('centroid position : ', aileron_geometry.centroid)
    print('z moment of inertia : ', aileron_geometry.Izz, ' [mm^4]')
    print('y moment of inertia : ', aileron_geometry.Iyy, ' [mm^4]')
    print('zy moment of inertia : ', aileron_geometry.Izy, '[mm^4]')






 #   areas = aileron_geometry.calc_boom_areas(1.1)
 #   print(areas)
 #   aileron_geometry.centroid = (1.0, 0.0)
  ## aileron_geometry.moment_inertia_Izz()
    #print(aileron_geometry.Izz, aileron_geometry.Iyy)

    return 0.0


main()