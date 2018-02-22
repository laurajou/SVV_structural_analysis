import numpy as np
import math


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

    def calc_shear_center(self):



