import numpy as np
import math
from helpers import *
from sympy import nsolve


C_a = 0.547
l_a = 2.771
x_1 = 0.153
x_2 = 1.281
x_3 = 2.681
x_a = 0.28
h_a = 0.225
t_sk = 0.0011
t_sp = 0.0029
t_st = 0.0012
h_st = 0.015
w_st = 0.02
n_st = 17
d_1 = 0.1103
d_3 = 0.1642
theta = 26
P = 9170
q = 4530


class DiscreteSection():
    def __init__(self, neutral_axis, aileron_geometry):
        self.neutral_axis = neutral_axis
        self.bending_stress = None
        self.bending_deflection = None
        self.aileron_geometry = aileron_geometry

    def calc_bending_stress(self, Mz, My, Fx, y, z):
        """
        Calculates bending stresses at given point (z, y) in the particular section of the aileron
        :param Mz: Moment distribution at given point in x
        :param My: Moment distribution at given point in x
        :param Fx: Total force in x direction at given point in x
        :param y: y-coordinate of point in cross-section where stress is calculated
        :param z: z-coordinate of point in cross-section where stress is calculated
        :return: Bending stress at given point in the cross-section at given point in x direction
        """
        inertia_term = self.aileron_geometry.Izz * self.aileron_geometry.Iyy - self.aileron_geometry.Izy ** 2
        moment_contribution = (Mz * (self.aileron_geometry.Iyy * y - self.aileron_geometry.Izy * z)
                               - My * (self.aileron_geometry.Izz * z - self.aileron_geometry.Izy * y)) / inertia_term
        area_total = sum(self.aileron_geometry.boom_areas)
        forces_contribution = Fx / area_total
        self.bending_stress = moment_contribution + forces_contribution

    def calc_bending_deflection(self, E, Mz):
        """
        Calculates bending deflection on this point in x-direction
        :param E: E-modulus of material
        :param Mz: Moment distribution at given point in x
        :return: Deflection due to bending in given point in x-direction
        """
        raise NotImplementedError

    def calc_shear_flow(self, Sz, Sy):
        Izz = self.aileron_geometry.Izz
        Iyy = self.aileron_geometry.Iyy
        Izy = self.aileron_geometry.Izy

        inertia_term_z = - (Sz * Izz - Sy * Izy) / (Izz * Iyy - Izy ** 2)
        inertia_term_y = - (Sy * Iyy - Sz * Izy) / (Izz * Iyy - Izy ** 2)
        deltas_cut = []
        deltas_totals = []
        integrals = []

        number_cells = len(self.aileron_geometry.cells)
        for num_cell in range(number_cells):
            # find the wall they have in common the two cells and make the cut there
            wall_cut = get_common_wall(self.aileron_geometry.cells)
            wall_cut.set_q_B(0.0)
            accumulation_y, accumulation_z = 0.0, 0.0
            integral, delta_total = 0.0, 0.0
            for n, wall in enumerate(self.aileron_geometry.cells[num_cell]):
                # only calculate the qB if it is not the wall that you have already cut
                if wall != wall_cut:
                    accumulation_y += self.aileron_geometry.booms[wall.booms[0]].area * \
                                      self.aileron_geometry.booms[wall.booms[0]].y_dist
                    accumulation_z += self.aileron_geometry.booms[wall.booms[0]].area * \
                                      self.aileron_geometry.booms[wall.booms[0]].z_dist
                    wall.set_q_B(inertia_term_z * accumulation_z + inertia_term_y * accumulation_y)
                integral += wall.q_B * wall.length / wall.thickness
                #print('integral value : ', integral)
               # print('q_B : ', wall.q_B)
                print('delta : ', wall.length/wall.thickness)
                delta_total += wall.length/wall.thickness
                print('qB on edge : ', wall.booms, 'value of: ', wall.q_B)
            deltas_cut.append(wall_cut.length/wall_cut.thickness)
            deltas_totals.append(delta_total)
            integrals.append(integral)
        # create system of equations that when solved gives you q_01 and q_02
        matrix_1 = np.array([[-deltas_cut[0], deltas_totals[0]], [deltas_totals[1], -deltas_cut[1]]])
        matrix_2 = np.asarray(integrals)

        q_s_0_array = np.linalg.solve(matrix_1, matrix_2)

        for i in range(number_cells):
            for wall in self.aileron_geometry.cells[i]:
                wall.q_0 = q_s_0_array[i]
        for wall in self.aileron_geometry.edges:
            wall.q_total = wall.q_0 + wall.get_q_B()


